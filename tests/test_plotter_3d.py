# Test creation of PlotData objects
import hdviz
import numpy as np


def test_point_plot():
    x = np.random.normal(size=(100, 3))
    a = hdviz.Plotter3d()
    a.add_pointset(x, label="example_data", alpha=0.3)
    x2 = np.random.normal(size=(10, 3))
    a.add_pointset(x2, label="example_other", marker="x", color="orange")
    assert a.num_pointsets() == 2
    # a.plot(title="Hei")
