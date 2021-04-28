import numpy as np


def assert_dim(x, expected_dim):
    L = len(x.shape)
    msg = "expected %d-dimensional array, found %d-dimensional" % (expected_dim, L)
    assert expected_dim == L, msg
    return True


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


def create_grid_around(x, M: int, scaling: float = 0.1):
    """Create a uniform rectangular grid around points *z*.

    :param x: a numpy array of shape *[n_points, D]*
    :type x: np.ndarray
    :param M: number of points per dimension
    :type M: int
    :param scaling: How much larger should the grid be than the range of *z* for each
        dimension. If this is zero, grid is exactly the size of the data range.
    :type scaling: float
    :return: a numpy array of shape *[M^d, d]*
    :rtype: np.ndarray
    """
    amin = np.amin(x, axis=0)
    amax = np.amax(x, axis=0)
    return create_grid(amin, amax, M, scaling)


def create_grid(axis_ranges_min, axis_ranges_max, M, scaling=0.1):
    amin = axis_ranges_min
    amax = axis_ranges_max
    D = len(amax)
    LS = list()
    for d in range(0, D):
        h = scaling * (amax[d] - amin[d])
        LS = LS + [np.linspace(amin[d] - h, amax[d] + h, M)]
    xs_ = np.meshgrid(*LS)
    x_grid = np.array([y.T.flatten() for y in xs_]).T
    return x_grid


def reshape_traj(z_traj):
    n_timepoints = z_traj.shape[0]
    n_samples = z_traj.shape[1]
    n_dimensions = z_traj.shape[2]
    return z_traj.view(n_timepoints * n_samples, n_dimensions)


def square_axis_limits(ax_limits):
    D = ax_limits.shape[0]
    ran = np.array([ax_limits.min(), ax_limits.max()])
    return ran.repeat(D).reshape(-1, D).T
