import numpy as np
import pandas as pd
from .utils import assert_dim


def create_pointdata(x: np.ndarray, categories=None, name=None):
    assert_dim(x, 2)
    dat = PointData(x, categories)
    if name is not None:
        dat.set_dataname(name)
    return dat


def create_linedata(x: np.ndarray, categories=None, name=None):
    assert_dim(x, 3)
    dat = LineData(x, categories)
    if name is not None:
        dat.set_dataname(name)
    return dat


class PlotData:
    """Abstract class for data to be plotted."""

    def __init__(self, categories, num_objects):
        self.name = "datagroup"
        if categories is None:
            categories = ["group_1"] * num_objects
        n_cats = len(np.unique(categories))
        L_cats = len(categories)
        msg = "len(categories) must be %d, but found %d " % (num_objects, L_cats)
        assert L_cats == num_objects, msg
        self.categories = pd.Series(categories, dtype="category")
        self.num_objects = num_objects
        self.num_categories = n_cats

    def set_dataname(self, name):
        self.name = name

    def __repr__(self):
        desc = "PlotData containing %d objects and %d categories." % (
            self.num_objects,
            self.num_categories,
        )
        return desc


class PointData(PlotData):
    """Data to be plotted using a scatter plot.
    :param x: numpy array of shape (num_points, num_dims)
    :type x: np.ndarray
    """

    def __init__(self, x: np.ndarray, categories):
        num_objects = x.shape[0]
        super().__init__(categories, num_objects)
        self.num_points = num_objects
        self.num_dims = x.shape[1]
        self.x = x
        self.set_dataname("pointdata")

    def __repr__(self):
        desc = "PointData containing %d points, %d dims and %d categories." % (
            self.num_points,
            self.num_dims,
            self.num_categories,
        )
        return desc


class LineData(PlotData):
    """Data to be plotted using lines.
    :param x: numpy array of shape (num_lines, num_points, num_dims)
    :type x: np.ndarray
    """

    def __init__(self, x: np.ndarray, categories):
        num_objects = x.shape[0]
        super().__init__(categories, num_objects)
        self.num_lines = num_objects
        self.num_points = x.shape[1]
        self.num_dims = x.shape[2]
        self.x = x
        self.set_dataname("linedata")

    def __repr__(self):
        desc = (
            "LineData containing %d lines, %d points for each line, "
            "%d dims and %d categories."
            % (self.num_lines, self.num_points, self.num_dims, self.num_categories)
        )
        return desc
