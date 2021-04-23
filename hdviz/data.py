import numpy as np
from .utils import assert_dim


class PlotData:
    """Abstract class for data to be plotted."""

    def __init__(self, num_objects):
        self.label = "data"
        self.num_objects = num_objects

    def __repr__(self):
        desc = "<PlotData (%d objects)>" % self.num_objects
        return desc


class PointData(PlotData):
    """Data to be plotted using a scatter plot.
    :param x: numpy array of shape (num_points, num_dims)
    :type x: np.ndarray
    """

    def __init__(self, x: np.ndarray, color, marker, alpha, label):
        if color is None:
            color = "black"
        assert_dim(x, 2)
        num_objects = x.shape[0]
        super().__init__(num_objects)
        self.num_points = num_objects
        self.num_dims = x.shape[1]
        self.x = x
        self.color = color
        self.marker = marker
        self.alpha = alpha
        self.label = label

    def __repr__(self):
        desc = "<PointData (%d points, %d dims)>" % (
            self.num_points,
            self.num_dims,
        )
        return desc

    def set_color(self, color):
        self.color = color

    def get_range_min(self):
        return self.x.min(0)

    def get_range_max(self):
        return self.x.max(0)


class LineData(PlotData):
    """Data to be plotted using lines.
    :param x: numpy array of shape (num_lines, num_points, num_dims)
    :type x: np.ndarray
    """

    def __init__(self, x: np.ndarray, color, style, alpha, label):
        if color is None:
            color = "black"
        assert_dim(x, 3)
        num_objects = x.shape[0]
        super().__init__(num_objects)
        self.num_lines = num_objects
        self.num_points = x.shape[1]
        self.num_dims = x.shape[2]
        self.x = x
        self.color = color
        self.style = style
        self.alpha = alpha
        self.label = label

    def __repr__(self):
        desc = "<LineData (%d lines, %d points per line, " "%d dims)>" % (
            self.num_lines,
            self.num_points,
            self.num_dims,
        )
        return desc

    def get_range_min(self):
        return self.x.min(1).min(0)

    def get_range_max(self):
        return self.x.max(1).max(0)


class QuiverData(PlotData):
    """Data to be plotted using arrows.
    :param x: numpy array of shape (num_arrows, num_dims)
    :type x: np.ndarray
    :param v: numpy array of shape (num_arrows, num_dims)
    :type v: np.ndarray
    """

    def __init__(self, x: np.ndarray, v: np.ndarray, color, alpha, label):
        if color is None:
            color = "gray30"
        assert_dim(x, 2)
        assert_dim(v, 2)
        assert x.shape == v.shape, "x and v must have same shape!"
        num_objects = x.shape[0]
        super().__init__(num_objects)
        self.num_arrows = num_objects
        self.num_dims = x.shape[1]
        self.x = x
        self.v = v
        self.color = color
        self.alpha = alpha
        self.label = label

    def __repr__(self):
        desc = "<QuiverData (%d arrows, " "%d dims)>" % (
            self.num_arrows,
            self.num_dims,
        )
        return desc

    def get_range_min(self):
        return self.x.min(1).min(0)

    def get_range_max(self):
        return self.x.max(1).max(0)
