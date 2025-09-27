from abc import ABC, abstractmethod

from matplotlib import pyplot as plt


class BaseAnim(ABC):
    def __init__(
        self,
        frames: int = 120,
        figsize: tuple[float, float] = (7, 7),
        cmap: str = "RdBu",
    ) -> None:
        self.frames = frames
        self.figsize = figsize
        self.cmap = cmap

    @abstractmethod
    def setup() -> plt.Figure:
        pass

    @abstractmethod
    def update(frame: int) -> tuple:
        pass
