import numpy as np
from .data import PointData, LineData
from .colors import category_palette


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

    def num_quiversets(self):
        return len(self.quiver_sets)

    def pointset_names(self):
        return [ps.name for ps in self.point_sets]

    def lineset_names(self):
        return [ls.name for ls in self.line_sets]

    def quiverset_names(self):
        return [qs.name for qs in self.quiver_sets]

    def recolor_pointsets(self):
        N = self.num_pointsets()
        colors = category_palette(N)
        for i in range(0, N):
            self.point_sets[i].set_color(colors[i])

    def plot_setup(self, figsize=None, axis_limits=None, square=False):
        if figsize is not None:
            self.figsize = figsize
        if axis_limits is not None:
            self.axis_limits = axis_limits
        else:
            self.set_axis_limits(axis_limits, square)

    def set_axis_limits(self, axis_limits=None, square=True, scale_margin=0.1):
        if axis_limits is None:
            self.axis_limits = self.create_axis_limits(square, scale_margin)
        else:
            # TODO: make impossible to add wrong dim axis limits
            self.axis_limits = axis_limits

    def create_axis_limits(self, square=True, scale_margin=0.1):
        if self.num_quiversets() > 0:
            amin, amax = self.get_quiverrange()
        elif self.num_pointsets() > 0:
            amin, amax = self.get_pointrange()
        elif self.num_linesets() > 0:
            amin, amax = self.get_linerange()
        else:
            raise RuntimeError("No points, lines, or arrows added!")
        amin = amin - scale_margin * (amax - amin)
        amax = amax + scale_margin * (amax - amin)
        a = np.vstack((amin, amax)).T
        if square:
            D = a.shape[0]
            a = a.max(0).repeat(D).reshape(-1, D).T
        return a.tolist()

    def get_axis_limits(self):
        if self.axis_limits is None:
            raise RuntimeError("axis limits not set!")
        return self.axis_limits

    def add_pointset(
        self, x: np.ndarray, color=None, marker="o", alpha=1.0, label=None
    ):
        if label is None:
            label = "points %d" % (self.num_pointsets() + 1)
        ps = PointData(x, color, marker, alpha, label)
        assert_num_dims(ps.num_dims, self.num_dims)
        self.point_sets += [ps]
        if color is None:
            self.recolor_pointsets()

    def add_lineset(self, x: np.ndarray, color=None, style="-", alpha=1.0, label=None):
        if label is None:
            label = "lines %d" % (self.num_linesets() + 1)
        ls = LineData(x, color, style, alpha, label)
        assert_num_dims(ls.num_dims, self.num_dims)
        self.line_sets += [ls]

    def get_pointrange(self):
        if self.num_pointsets() == 0:
            raise RuntimeError("no pointsets defined!")
        mins = np.vstack([ps.get_range_min() for ps in self.point_sets]).min(0)
        maxs = np.vstack([ps.get_range_max() for ps in self.point_sets]).max(0)
        return mins, maxs

    def get_linerange(self):
        if self.num_linesets() == 0:
            raise RuntimeError("no linesets defined!")
        mins = np.vstack([ls.get_range_min() for ls in self.line_sets]).min(0)
        maxs = np.vstack([ls.get_range_max() for ls in self.line_sets]).max(0)
        return mins, maxs

    def get_quiverrange(self):
        if self.num_quiversets() == 0:
            raise RuntimeError("no quiversets defined!")
        mins = np.vstack([qs.get_range_min() for qs in self.quiver_sets]).min(0)
        maxs = np.vstack([qs.get_range_max() for qs in self.quiver_sets]).max(0)
        return mins, maxs
