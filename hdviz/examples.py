from .plotter_nd import PlotterNd
from .plotter_3d import Plotter3d
from .utils import draw_plot
import numpy as np
from matplotlib import pyplot as plt


def create_3d_spiral(N: int = 100, a: float = 0.5):
    theta = np.linspace(-4 * np.pi, 4 * np.pi, N)
    z = np.linspace(-2, 2, N)
    r = z ** 2 + 1
    x = r * np.sin(a * theta)
    y = r * np.cos(a * theta)
    return np.vstack((x, y, z)).T


def example(idx=1, **save_args):
    """Plot and example plot.

    :param idx: index of the example
    :type idx: int
    """
    if idx == 1:
        example_3d_spiral(**save_args)
    else:
        raise ValueError("invalid idx")


def example_3d_spiral(**save_args):
    # Create data
    N = 100
    x = create_3d_spiral(3 * N)
    x = x + 0.1 * np.random.normal(size=x.shape)
    categories = np.array((100 * [1] + 100 * [2] + 100 * [3]))

    # Create plotters
    a = PlotterNd(3)
    b = Plotter3d()
    a.add_pointsets(x, categories)
    b.add_pointsets(x, categories)

    # Create canvas
    fig = plt.figure(figsize=(8, 8))
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    b.plot(ax=ax1)

    ax2 = fig.add_subplot(2, 2, 2)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    axs = np.array([[ax2, ax3, ax4]])
    a.plot(axs=axs)
    draw_plot(**save_args)
