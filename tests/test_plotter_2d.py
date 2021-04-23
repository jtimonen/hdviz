# Test creation of PlotData objects
import hdviz
import numpy as np
import pytest


def create_2d_spiral(a: float = 1):
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z ** 2 + 1
    x = r * np.sin(a * theta)
    y = r * np.cos(a * theta)
    return np.vstack((x, y)).T


def test_point_plot():
    x = np.random.normal(size=(100, 2))
    a = hdviz.Plotter2d()
    a.add_pointset(x)
    b = a.plot(title="Hei", square=False)
    assert str(b)[0:11] == "AxesSubplot"
    a.clear_data()
    with pytest.raises(RuntimeError):
        a.get_pointrange()


def test_line_plot():
    x = np.random.normal(size=(10, 100, 2))
    a = hdviz.Plotter2d()
    a.add_lineset(x, label="lines", alpha=0.8)
    assert a.num_pointsets() == 0
    assert a.num_linesets() == 1
    # a.plot(title="Hei")


def test_mixed_plot():
    l1 = create_2d_spiral(1.0)
    l2 = create_2d_spiral(1.5)
    x = np.stack((l1, l2))
    a = hdviz.Plotter2d()
    a.add_lineset(x, label="lines", alpha=0.3)
    x2 = np.random.normal(size=(10, 2))
    a.add_pointset(x2, marker="x", color="red")
    assert a.num_pointsets() == 1
    assert a.num_linesets() == 1
    # a.plot(title="Hei")