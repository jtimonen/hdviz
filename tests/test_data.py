# Test creation of PlotData objects
import hdviz
import numpy as np


def test_pointdata():
    x = np.random.normal(size=(10, 5))
    pd = hdviz.create_pointdata(x)
    assert pd.x.shape == (10, 5)
