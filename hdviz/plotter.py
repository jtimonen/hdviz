import numpy as np
from .data import PointData, LineData, QuiverData
from .colors import category_palette
from .utils import create_grid, square_axis_limits


def inf_range(D):
    mins = np.full(shape=D, fill_value=np.inf)
    maxs = np.full(shape=D, fill_value=-np.inf)
    return mins, maxs


def assert_num_dims(D1, D2):
    assert D1 == D2, "number of dimensions should be %d, but found %d" % (D2, D1)


class Plotter:
    """Abstract plotter class."""

    def __init__(self):
        self.point_sets = []
        self.line_sets = []
        self.quiver_sets = []
        self.scatter_kwargs = dict()
        self.lines_kwargs = dict()
        self.quiver_kwargs = dict()

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
        amin, amax = self.get_max_ranges()
        # todo: informative error if ranges are (-inf, inf)
        amin = amin - scale_margin * (amax - amin)
        amax = amax + scale_margin * (amax - amin)
        a = np.vstack((amin, amax)).T
        if square:
            a = square_axis_limits(a)
        return a.tolist()

    def get_axis_limits(self):
        if self.axis_limits is None:
            raise RuntimeError("axis limits not set!")
        return self.axis_limits

    def add_pointset(
        self, x: np.ndarray, color=None, marker="o", alpha=1.0, label=None
    ):
        """Add a point set."""
        if label is None:
            label = "points %d" % (self.num_pointsets() + 1)
        ps = PointData(x, color, marker, alpha, label)
        assert_num_dims(ps.num_dims, self.num_dims)
        self.point_sets += [ps]
        if color is None:
            self.recolor_pointsets()

    def add_lineset(self, x: np.ndarray, color=None, style="-", alpha=1.0, label=None):
        """Add a line set."""
        if label is None:
            label = "lines %d" % (self.num_linesets() + 1)
        ls = LineData(x, color, style, alpha, label)
        assert_num_dims(ls.num_dims, self.num_dims)
        self.line_sets += [ls]

    def add_quiverset(
        self, x: np.ndarray, v: np.ndarray, color=None, alpha=1.0, label=None
    ):
        """Add an arrows set."""
        if label is None:
            label = "arrows %d" % (self.num_quiversets() + 1)
        # TODO: allow creation by passing only x and a function that computes v from x
        qs = QuiverData(x, v, color, alpha, label)
        assert_num_dims(qs.num_dims, self.num_dims)
        self.quiver_sets += [qs]

    def get_pointrange(self):
        if self.num_pointsets() == 0:
            return inf_range(self.num_dims)
        mins = np.vstack([ps.get_range_min() for ps in self.point_sets]).min(0)
        maxs = np.vstack([ps.get_range_max() for ps in self.point_sets]).max(0)
        return mins, maxs

    def get_linerange(self):
        if self.num_linesets() == 0:
            return inf_range(self.num_dims)
        mins = np.vstack([ls.get_range_min() for ls in self.line_sets]).min(0)
        maxs = np.vstack([ls.get_range_max() for ls in self.line_sets]).max(0)
        return mins, maxs

    def get_quiverrange(self):
        if self.num_quiversets() == 0:
            return inf_range(self.num_dims)
        mins = np.vstack([qs.get_range_min() for qs in self.quiver_sets]).min(0)
        maxs = np.vstack([qs.get_range_max() for qs in self.quiver_sets]).max(0)
        return mins, maxs

    def get_all_ranges(self):
        r1, R1 = self.get_pointrange()
        r2, R2 = self.get_linerange()
        r3, R3 = self.get_quiverrange()
        mins = np.vstack((r1, r2, r3))
        maxs = np.vstack((R1, R2, R3))
        return mins, maxs

    def get_max_ranges(self):
        mins, maxs = self.get_all_ranges()
        return mins.min(0), maxs.max(0)

    def create_grid_around_points(self, M: int = 30, square=True, scaling: float = 0.1):
        ar = self.create_axis_limits(square, scale_margin=0.0)
        ar = np.array(ar)
        amin = ar[:, 0].tolist()
        amax = ar[:, 1].tolist()
        return create_grid(amin, amax, M, scaling)

    def add_pointsets(
        self,
        x: np.ndarray,
        categories,
        labels=None,
        colors=None,
        marker="o",
        alpha: float = 1.0,
        categ_prefix: str = "group",
    ):
        """Add multiple point sets.

        :param x: a numpy array  of shape (n_points, n_dims)
        :type x: np.ndarray
        :param categories: an integer numpy array of length n_points
        :type categories: np.ndarray
        :param labels: Label of each category. Must be a dictionary where categories
        are keys and label strings are values.
        :param colors: Color of each category. Must be a dictionary where categories
        are keys and colors are values.
        :param marker: point marker
        :param alpha: point  opacity
        :param categ_prefix: prefix for categories if labels is None
        """
        ucat = np.unique(categories)
        for u in ucat:
            inds = np.where(categories == u)[0]
            xu = x[inds, :]
            label = (categ_prefix + " %d" % u) if (labels is None) else labels[u]
            color = None if (colors is None) else colors[u]
            ps = PointData(xu, color, marker, alpha, label)
            assert_num_dims(ps.num_dims, self.num_dims)
            self.point_sets += [ps]
        if colors is None:
            self.recolor_pointsets()
