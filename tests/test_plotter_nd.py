# Test plotting N-dimensional things
import hdviz
import numpy as np
import pytest


def test_plot_3d():
    x = np.random.normal(size=(100, 3))
    a = hdviz.PlotterNd(3)
    a.add_pointset(x, label="points", alpha=0.7)
    assert a.num_pointsets() == 1
    ax = a.plot(panelsize=2, square=True)
    assert ax.shape == (1, 3)
    with pytest.raises(RuntimeError):
        a.plot(figsize=(7, 10))
    a.clear_data()
    with pytest.raises(RuntimeError):
        a.get_pointrange()


def test_plot_4d():
    x = np.random.normal(size=(100, 4))
    a = hdviz.PlotterNd(4)
    a.add_pointset(x, label="points", alpha=0.7)
    t = -2.0 + 4.0 * np.linspace(0, 1, 100)
    y1 = t
    y2 = 0.5 * np.sin(t)
    y3 = np.cos(4 * t)
    y4 = -0.3 * t * t
    lin = np.stack((y1, y2, y3, y4)).T
    ls = np.stack((lin, lin + 0.5))
    a.add_lineset(ls, color="red")
    ax = a.plot(panelsize=3)
    assert ax.shape == (2, 3)


def test_plot_5d():
    x = np.random.normal(size=(100, 5))
    a = hdviz.PlotterNd(5)
    a.add_pointset(x, label="points", alpha=0.7, color="pink")
    t = -2.0 + 4.0 * np.linspace(0, 1, 100)
    f1 = t
    f2 = 0.5 * np.sin(t)
    f3 = np.cos(4 * t)
    f4 = -0.3 * t * t
    f5 = 0.0 * t
    v = np.stack((f1, f2, f3, f4, f5)).T
    a.add_quiverset(x, v, color="black")
    ax = a.plot()
    assert ax.shape == (3, 4)
