# Test creation of PlotData objects
import hdviz
import numpy as np


def test_pointdata():
    x = np.random.normal(size=(10, 5))
    pd = hdviz.create_pointdata(x)
    assert pd.num_points == 10
    assert pd.num_categories == 1
    assert pd.num_dims == 5


def test_linedata():
    x = np.random.normal(size=(3, 10, 4))
    ld = hdviz.create_linedata(x, categories=["banana", "apple", "apple"])
    assert ld.num_points == 10
    assert ld.num_categories == 2
    assert ld.num_dims == 4
