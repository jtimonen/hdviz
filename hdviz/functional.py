from .plotter_2d import Plotter2d
from .plotter_3d import Plotter3d
from .plotter_nd import PlotterNd
from .utils import draw_plot
import pandas as pd


def determine_dimension(points, trajectories):
    """Determine dimension based on numpy arrays."""
    if points is None:
        if trajectories is None:
            raise RuntimeError("points and trajectories can't both be None!")
        D = trajectories.shape[2]
    else:
        D = points.shape[1]
    return D


def create_plotter(D: int, no_3d: bool = False):
    """Create a plotter that can be customized.

    :param D: dimension
    :type D: int
    :param no_3d: don't create 3d plots even if D=3
    :type no_3d: bool
    """
    if D == 2:
        return Plotter2d()
    elif D == 3:
        if no_3d:
            return PlotterNd(num_dims=3)
        return Plotter3d()
    else:
        return PlotterNd(num_dims=D)


def visualize(
    points=None,
    labels=None,
    colors=None,
    u=None,
    v=None,
    trajectories=None,
    xlim=None,
    ylim=None,
    scatter_kwargs=None,
    quiver_kwargs=None,
    lines_kwargs=None,
    save_name=None,
    save_dir=".",
    azimuth=None,
    elevation=None,
    **save_kwargs
):
    """Main function.

    :param points: Points to plot.
    :param labels: Category of each point (a list).
    :param colors: Color of each point (a list).
    :param u: Vector locations.
    :param v: Vectors.
    :param trajectories: Trajectories to plot.
    :param xlim: x-axis limits.
    :param ylim: y-axis limits.
    :param azimuth: Azimuthal viewing angle (default = -60).
    :param elevation: Elevation viewing angle (default = 30).
    :save_kwargs: Keyword arguments to saving plot.
    """
    D = determine_dimension(points, trajectories)
    N = points.shape[0]
    if labels is None:
        labels = N * ["unlabeled"]
    labels, label_colors, label_names = parse_labeling(labels, colors)
    ptr = create_plotter(D)
    if scatter_kwargs is not None:
        ptr.scatter_kwargs = scatter_kwargs
    if lines_kwargs is not None:
        ptr.lines_kwargs = lines_kwargs
    if quiver_kwargs is not None:
        ptr.quiver_kwargs = quiver_kwargs
    if points is not None:
        ptr.add_pointsets(
            points,
            labels=labels,
            label_names=label_names,
            alpha=0.7,
            label_colors=label_colors,
        )
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
    if isinstance(ptr, Plotter3d):
        ptr.set_perspective(azimuth, elevation)
    ptr.plot(axis_limits=ax_limits)
    draw_plot(save_name, save_dir, **save_kwargs)


def parse_labeling(labels, label_colors):
    a = pd.Categorical(labels)
    label_names = a.categories.to_list()
    labels = a.codes
    if label_colors is not None:
        b = pd.Categorical(label_colors)
        label_colors = b.categories.to_list()

    return labels, label_colors, label_names
