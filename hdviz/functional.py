from .plotter_2d import Plotter2d
from .plotter_3d import Plotter3d
from .plotter_nd import PlotterNd
from .utils import draw_plot


def determine_dimension(points, trajectories):
    """Determine dimension based on numpy arrays."""
    if points is None:
        if trajectories is None:
            raise RuntimeError("points and trajectories can't both be None!")
        D = trajectories.shape[2]
    else:
        D = points.shape[1]
    return D


def create_plotter(D: int):
    """Create a plotter that can be customized.

    :param D: dimension
    :type D: int
    """
    if D == 2:
        return Plotter2d()
    elif D == 3:
        return Plotter3d()
    else:
        return PlotterNd(num_dims=D)


def visualize(
    points=None,
    categories=None,
    labels=None,
    u=None,
    v=None,
    trajectories=None,
    xlim=None,
    ylim=None,
    save_name=None,
    save_dir=".",
    **save_kwargs
):
    """Main function."""
    D = determine_dimension(points, trajectories)
    ptr = create_plotter(D)
    if points is not None:
        ptr.add_pointsets(points, categories=categories, labels=labels, alpha=0.7)
    if u is not None:
        ptr.add_quiverset(u, v, alpha=0.5)
    if trajectories is not None:
        ptr.add_lineset(trajectories, alpha=0.3)
        x_first = trajectories[:, 0, :]
        ptr.add_pointset(x_first, marker="x", color="k", alpha=0.3, label="start")
    if xlim is not None:
        if ylim is None:
            ylim = xlim
        ax_limits = [xlim, ylim]
    else:
        ax_limits = None
    ptr.plot(axis_limits=ax_limits)
    draw_plot(save_name, save_dir, **save_kwargs)
