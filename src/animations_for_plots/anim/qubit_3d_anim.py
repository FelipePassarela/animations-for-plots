import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from animations_for_plots.anim.base_anim import BaseAnim
from animations_for_plots.flux_qubit_mesh import FluxQubitMesh


class Qubit3DAnim(BaseAnim):
    def __init__(
        self,
        mesh: FluxQubitMesh,
        rotate: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.rotate = rotate
        self.ax: Axes3D
        self.fig, self.ax = plt.subplots(
            figsize=self.figsize, subplot_kw={"projection": "3d"}
        )
        self.__mesh = mesh

    def setup(self) -> plt.Figure:
        X, Y, Z = self.__mesh.X, self.__mesh.Y, self.__mesh.Z.T
        self.plot_surface(X, Y, Z)
        return self.fig

    def update(self, frame: int) -> tuple:
        end = "\n" if frame == self.frames - 1 else ""
        print(f"\rRendering frame {frame + 1}/{self.frames}", end=end)

        phi_ext = 2 * np.pi * frame / self.frames
        Z = self.__mesh.compute_potential(phi_ext=phi_ext).T
        X, Y = self.__mesh.X, self.__mesh.Y

        self.ax.cla()
        self.plot_surface(X, Y, Z)

        if self.rotate:
            elev = 30 + 15 * np.sin(2 * np.pi * frame / self.frames)
            azim = 120 + 360 * frame / self.frames
            self.ax.view_init(elev=elev, azim=azim)

        self.ax.set_title(
            r"Flux Qubit Potential, $\phi_{ext} = %.2f \pi$" % (phi_ext / np.pi)
        )
        self.fig.tight_layout()

        return (self.ax,)

    def plot_surface(self, X: np.ndarray, Y: np.ndarray, Z: np.ndarray) -> None:
        self.ax.plot_surface(X, Y, Z, cmap=self.cmap, rstride=4, cstride=4)

        xlim = -np.pi, 2 * np.pi
        ylim = 0, 3 * np.pi
        zlim = -np.pi, 2 * np.pi

        self.ax.contour(X, Y, Z, zdir="x", offset=xlim[0], cmap=self.cmap)
        self.ax.contour(X, Y, Z, zdir="y", offset=ylim[1], cmap=self.cmap)
        self.ax.contour(X, Y, Z, zdir="z", offset=zlim[0], cmap=self.cmap)

        self.ax.set_xlim3d(xlim)
        self.ax.set_ylim3d(ylim)
        self.ax.set_zlim3d(zlim)

        self.ax.set_title("3D Flux Qubit Potential Animation")
        self.ax.set_xlabel(r"$\phi_p$", fontsize=14)
        self.ax.set_ylabel(r"$\phi_m$", fontsize=14)
        self.ax.set_zlabel("Potential", fontsize=12)
