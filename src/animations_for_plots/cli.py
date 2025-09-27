import argparse

from matplotlib.animation import FuncAnimation

from animations_for_plots.anim.qubit_3d_anim import Qubit3DAnim
from animations_for_plots.anim.qubit_colormap_anim import QubitColormapAnim
from animations_for_plots.flux_qubit_mesh import FluxQubitMesh


def main() -> None:
    args = parse_args()
    frames = args.frames
    cmap = args.cmap
    anim_type = args.type
    rotate = args.rotate
    output = args.output
    figsize = args.figsize

    anim = None
    mesh = FluxQubitMesh()
    common_kwargs = dict(
        frames=frames,
        figsize=figsize,
        cmap=cmap,
    )

    match anim_type:
        case "colormap":
            anim = QubitColormapAnim(mesh, **common_kwargs)
        case "3d":
            anim = Qubit3DAnim(mesh, rotate=rotate, **common_kwargs)
        case _:
            raise ValueError(f"Unknown animation type: {anim_type}")

    func_anim = FuncAnimation(anim.setup(), anim.update, frames=frames)
    func_anim.save(output, writer="pillow", fps=30)
    print(f"Animation saved as {output}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate flux qubit potential animations."
    )
    parser.add_argument(
        "--frames", type=int, default=120, help="Number of frames in the animation."
    )
    parser.add_argument(
        "--cmap", type=str, default="RdBu", help="Colormap for the colormap animation."
    )
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        choices=["colormap", "3d"],
        default="3d",
        help="Type of animation to generate.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="animation.gif",
        help="Output filename for the animation.",
    )
    parser.add_argument(
        "-r",
        "--rotate",
        action="store_true",
        help="Enable rotation for the 3D animation.",
    )
    parser.add_argument(
        "-fs",
        "--figsize",
        type=float,
        nargs=2,
        default=(7, 7),
        help="Figure size as width height (e.g., --figsize 8 6).",
    )

    args = parser.parse_args()
    return args
