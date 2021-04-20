import numpy as np
from .utils import create_range_around, draw_plot
from .data import PointData, LineData


def assert_num_dims(D1, D2):
    assert D1 == D2, "number of dimensions should be %d, but found %d" % (D2, D1)


class Plotter:
    """Abstract plotter class."""

    def __init__(self):
        self.point_sets = []
        self.line_sets = []
        self.quiver_sets = []
        self.figsize = (7, 7)
        self.axis_limits = None
        self.num_dims = None

    def clear_data(self):
        self.point_sets = []
        self.line_sets = []
        self.quiver_sets = []

    def num_pointsets(self):
        return len(self.point_sets)

    def num_linesets(self):
        return len(self.line_sets)

    def pointset_names(self):
        return [ps.name for ps in self.point_sets]

    def lineset_names(self):
        return [ls.name for ls in self.line_sets]

    def draw(self, save_name, save_dir=".", **save_kwargs):
        draw_plot(save_name, save_dir, **save_kwargs)

    def plot_setup(self, figsize=None, axis_limits=None, square=False):
        if figsize is not None:
            self.figsize = figsize
        if axis_limits is not None:
            self.axis_limits = axis_limits
        else:
            self.set_axis_limits(axis_limits)
        if square:
            self.square_axis_limits()

    def set_axis_limits(self, axis_limits):
        pointdata = self.point_sets[0]
        if axis_limits is None:
            self.axis_limits = create_range_around(pointdata.x)
        else:
            self.axis_limits = axis_limits

    def get_axis_limits(self):
        if self.axis_limits is None:
            raise RuntimeError("axis limits not set!")
        return self.axis_limits

    def square_axis_limits(self):
        alims = self.axis_limits
        if alims is None:
            raise RuntimeError("cannot square non-existing limits!")
        print("should square here")

    def add_pointset(
        self, x: np.ndarray, color="blue", marker="o", alpha=1.0, label="points"
    ):
        ps = PointData(x, color, marker, alpha, label)
        assert_num_dims(ps.num_dims, self.num_dims)
        self.point_sets += [ps]

    def add_lineset(
        self, x: np.ndarray, color="red", style="-", alpha=1.0, label="lines"
    ):
        ls = LineData(x, color, style, alpha, label)
        assert_num_dims(ps.num_dims, self.num_dims)
        self.line_sets += [ls]
