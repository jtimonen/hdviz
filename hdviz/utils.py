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
