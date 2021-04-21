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


def test_line_plot():
    x = np.random.normal(size=(10, 100, 3))
    a = hdviz.Plotter3d()
    a.add_lineset(x, label="lines", alpha=0.8)
    assert a.num_pointsets() == 0
    assert a.num_linesets() == 1
    # a.plot(title="Hei")


def test_mixed_plot():
    x = np.random.normal(size=(10, 100, 3))
    a = hdviz.Plotter3d()
    a.add_lineset(x, label="lines", alpha=0.8)
    x2 = np.random.normal(size=(10, 3))
    a.add_pointset(x2, label="example_other", marker="x", color="orange")
    assert a.num_pointsets() == 1
    assert a.num_linesets() == 1
    # a.plot(title="Hei")
