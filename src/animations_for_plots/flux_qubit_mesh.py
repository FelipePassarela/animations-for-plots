import numpy as np


class FluxQubitMesh:
    def __init__(self, nsamples=100) -> None:
        phi_p = np.linspace(0, 2 * np.pi, nsamples)
        phi_m = np.linspace(0, 2 * np.pi, nsamples)
        self.X, self.Y = np.meshgrid(phi_p, phi_m)
        self.Z = self.compute_potential()

    def compute_potential(
        self, alpha: float = 0.7, phi_ext: float = None
    ) -> np.ndarray:
        phi_ext = np.pi if phi_ext is None else phi_ext
        self.Z = (
            2
            + alpha
            - 2 * np.cos(self.X) * np.cos(self.Y)
            - alpha * np.cos(phi_ext - 2 * self.X)
        )
        return self.Z
