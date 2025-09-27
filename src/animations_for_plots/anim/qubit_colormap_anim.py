import numpy as np
from matplotlib import pyplot as plt

from animations_for_plots.anim.base_anim import BaseAnim
from animations_for_plots.flux_qubit_mesh import FluxQubitMesh


class QubitColormapAnim(BaseAnim):
    def __init__(
        self,
        mesh: FluxQubitMesh,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        self.mesh = mesh
        self.im = None

    def setup(self) -> plt.Figure:
        self.ax.set_title("Flux Qubit Potential")
        self.ax.set_xlabel(r"$\phi_p$", fontsize=14)
        self.ax.set_ylabel(r"$\phi_m$", fontsize=14)

        Z = self.mesh.Z
        self.im = self.ax.imshow(
            Z, cmap=self.cmap, vmin=abs(Z).min(), vmax=abs(Z).max(), extent=[0, 1, 0, 1]
        )
        self.im.set_interpolation("bilinear")
        self.fig.colorbar(self.im, ax=self.ax)
        self.fig.tight_layout()

        return self.fig

    def update(self, frame: int) -> tuple:
        end = "\n" if frame == self.frames - 1 else ""
        print(f"\rRendering frame {frame + 1}/{self.frames}", end=end)

        phi_ext = 2 * np.pi * frame / self.frames
        Z = self.mesh.compute_potential(phi_ext=phi_ext).T

        self.im.set_array(Z)
        self.im.set_clim(vmin=abs(Z).min(), vmax=abs(Z).max())
        self.ax.set_title(
            r"Flux Qubit Potential, $\phi_{ext} = %.2f \pi$" % (phi_ext / np.pi)
        )

        return (self.im,)
