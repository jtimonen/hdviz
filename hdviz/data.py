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


class LineData(PlotData):
    """Data to be plotted using lines.
    :param x: numpy array of shape (num_lines, num_points, num_dims)
    :type x: np.ndarray
    """

    def __init__(self, x: np.ndarray, color, style, alpha, label):
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
