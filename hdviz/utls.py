import os
import numpy as np
from matplotlib import pyplot as plt


def draw_plot(save_name, save_dir=".", **kwargs):
    """Function to be used always when a plot is to be shown or saved."""
    if save_name is None:
        plt.show()
    else:
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)
        save_path = os.path.join(save_dir, save_name)
        plt.savefig(save_path, **kwargs)
        plt.close()


def determine_nrows_ncols(nplots: int):
    """Determine number of rows and columns a grid of subplots.
    :param nplots: total number of subplots
    :type nplots: int
    """
    if nplots < 4:
        ncols = nplots
    elif nplots < 5:
        ncols = 2
    elif nplots < 10:
        ncols = 3
    else:
        ncols = 4
    nrows = int(np.ceil(nplots / ncols))
    return nrows, ncols


def create_grid_around(z, M: int, scaling: float = 0.1):
    """Create a uniform rectangular grid around points *z*.
    :param z: a numpy array of shape *[n_points, d]*
    :type z: np.ndarray
    :param M: number of points per dimension
    :type M: int
    :param scaling: How much larger should the grid be than the range of *z* for each
        dimension. If this is zero, grid is exactly the size of the data range.
    :type scaling: float
    :return: a numpy array of shape *[M^d, d]*
    :rtype: np.ndarray
    """
    umin = np.amin(z, axis=0)
    umax = np.amax(z, axis=0)
    D = len(umax)
    LS = list()
    for d in range(0, D):
        h = scaling * (umax[d] - umin[d])
        LS = LS + [np.linspace(umin[d] - h, umax[d] + h, M)]
    xs_ = np.meshgrid(*LS)
    U_grid = np.array([x.T.flatten() for x in xs_]).T
    return U_grid


def reshape_traj(z_traj):
    n_timepoints = z_traj.shape[0]
    n_samples = z_traj.shape[1]
    n_dimensions = z_traj.shape[2]
    return z_traj.view(n_timepoints * n_samples, n_dimensions)
