# Test plotting 2-dimensional things
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
    a = hdviz.create_plotter(2)
    a.add_pointset(x)
    b = a.plot(title="Hei", square=False)
    assert str(b)[0:11] == "AxesSubplot"
    a.clear_data()


def test_line_plot():
    x = np.random.normal(size=(10, 100, 2))
    a = hdviz.create_plotter(2)
    a.add_lineset(x, label="lines", alpha=0.8)
    assert a.num_pointsets() == 0
    assert a.num_linesets() == 1
    # a.plot(title="Hei")


def test_mixed_plot():
    l1 = create_2d_spiral(1.0)
    l2 = create_2d_spiral(1.5)
    x = np.stack((l1, l2))
    a = hdviz.create_plotter(2)
    a.add_lineset(x, label="lines", alpha=0.3)
    x2 = np.random.normal(size=(10, 2))
    a.add_pointset(x2, marker="x", color="red")
    assert a.num_pointsets() == 1
    assert a.num_linesets() == 1
    # a.plot(title="Hei")


def test_quiver_plot():
    x1 = np.random.normal(loc=[-1, -1], size=(100, 2))
    x2 = np.random.normal(loc=[-10, 3], size=(100, 2))
    x3 = np.random.normal(loc=[3, 2], size=(100, 2))
    a = hdviz.create_plotter(2)
    a.add_pointset(x1)
    a.add_pointset(x2)
    a.add_pointset(x3)
    u = a.create_grid_around_points(square=False)
    v1 = np.sin(u[:, 0])
    v2 = np.cos(u[:, 1] + 0.1 * u[:, 0])
    v = np.vstack((v1, v2)).T
    a.add_quiverset(u, v, color="red")
    b = a.plot(square=True)
    assert str(b)[0:11] == "AxesSubplot"
