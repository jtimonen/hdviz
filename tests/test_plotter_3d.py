# Test plotting 3-dimensional things
import hdviz
import numpy as np
import pytest


def create_3d_spiral(a: float = 1):
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z ** 2 + 1
    x = r * np.sin(a * theta)
    y = r * np.cos(a * theta)
    return np.vstack((x, y, z)).T


def test_point_plot():
    x = np.random.normal(size=(100, 3))
    a = hdviz.Plotter3d()
    a.add_pointset(x, label="example_data", alpha=0.3)
    x2 = np.random.normal(size=(10, 3))
    a.add_pointset(x2, label="example_other", marker="x", color="red")
    x = np.random.normal(size=(30, 3))
    a.add_pointset(x)
    assert a.num_pointsets() == 3
    b = a.plot(title="Hei", square=True)
    assert str(b)[0:13] == "Axes3DSubplot"
    a.clear_data()
    with pytest.raises(RuntimeError):
        a.get_pointrange()


def test_line_plot():
    x = np.random.normal(size=(10, 100, 3))
    a = hdviz.Plotter3d()
    a.add_lineset(x, label="lines", alpha=0.8)
    assert a.num_pointsets() == 0
    assert a.num_linesets() == 1


def test_mixed_plot():
    l1 = create_3d_spiral(1.0)
    l2 = create_3d_spiral(1.5)
    x = np.stack((l1, l2))
    a = hdviz.Plotter3d()
    a.add_lineset(x, label="lines", alpha=0.3)
    x2 = np.random.normal(size=(10, 3))
    a.add_pointset(x2, marker="x", color="red")
    assert a.num_pointsets() == 1
    assert a.num_linesets() == 1


def test_quiver_plot():
    a = hdviz.Plotter3d()
    x = np.random.normal(size=(10, 3))
    a.add_pointset(x, marker="x", color="red")
    u = a.create_grid_around_points(square=False, M=8)
    v1 = np.sin(u[:, 0])
    v2 = np.cos(u[:, 1] + 0.1 * u[:, 0])
    v3 = 0.1 * u[:, 2]
    v = np.vstack((v1, v2, v3)).T
    a.add_quiverset(u, v, color="blue", alpha=0.5)
    assert a.num_quiversets() == 1
