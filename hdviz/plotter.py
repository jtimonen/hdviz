from matplotlib import pyplot as plt
import numpy as np
from .utils import (
    create_grid_around,
    create_range_around,
    draw_plot,
    determine_nrows_ncols,
)


class Plotter:
    """Abstract plotter class."""

    def __init__(self):
        self.save_dir = "."
        self.data_points = None
        self.data_lines = []
        self.data_quiver = None
        self.axis_limits = None

    def draw(self, save_name, **save_kwargs):
        draw_plot(save_name, self.save_dir, **save_kwargs)

    def set_save_dir(self, path):
        self.save_dir = path

    def set_axis_limits(self, axis_limits=None, square=False):
        pointdata = self.data_points
        if (axis_limits is None) and (pointdata is not None):
            self.axis_limits = create_range_around(pointdata.x)
            if square:
                self.square_axis_limits()
        else:
            self.axis_limits = axis_limits

    def square_axis_limits(self):
        alims = self.axis_limits
        if alims is None:
            raise RuntimeError("cannot square non-existing limits!")
        print("should square here")


class PlotterNd(Plotter):
    """Main high-dimensional visualization class."""

    def __init__(self):
        super().__init__()
        self.save_dir = "."
        super.__init__()

    def plot(self):
        print("moi")


def plot_state_2d(model, z_samp, z_data, idx_epoch, loss, save_dir=".", **kwargs):
    u = create_grid_around(z_data, 20)
    v = model.f_numpy(u)
    epoch_str = "{0:04}".format(idx_epoch)
    loss_str = "{:.5f}".format(loss)
    title = "drift, epc = " + epoch_str + ", valid_loss = " + loss_str
    fn = "fig_" + epoch_str + ".png"

    # Create plot
    fig, axs = plt.subplots(2, 2, figsize=(14, 14))
    axs[0, 0].quiver(u[:, 0], u[:, 1], v[:, 0], v[:, 1], alpha=0.5)
    axs[0, 0].scatter(z_data[:, 0], z_data[:, 1], alpha=0.7)
    axs[0, 0].scatter(z_samp[:, 0], z_samp[:, 1], marker="x", alpha=0.7)
    axs[0, 0].set_title(title)

    x_min = np.min(u[:, 0])
    x_max = np.max(u[:, 0])
    y_min = np.min(u[:, 1])
    y_max = np.max(u[:, 1])
    axs[0, 0].set_xlim(x_min, x_max)
    axs[0, 0].set_ylim(y_min, y_max)
    axs[0, 1].set_xlim(x_min, x_max)
    axs[0, 1].set_ylim(y_min, y_max)

    S = 40
    u = create_grid_around(z_data, S)
    ut = torch.from_numpy(u).float()
    z_samp = torch.from_numpy(z_samp).float()
    v1 = model.kde(ut, z_samp)
    v1 = v1.cpu().detach().numpy()
    v2 = model.g_numpy(u)

    X = np.reshape(u[:, 0], (S, S))
    Y = np.reshape(u[:, 1], (S, S))
    Z1 = np.reshape(v1, (S, S))
    Z2 = np.reshape(v2, (S, S))

    axs[1, 0].contourf(X, Y, Z1)
    axs[0, 1].contourf(X, Y, Z2)
    axs[1, 0].set_xlim(x_min, x_max)
    axs[1, 0].set_ylim(y_min, y_max)
    axs[1, 1].set_xlim(x_min, x_max)
    axs[1, 1].set_ylim(y_min, y_max)
    axs[0, 1].set_title("diffusion")
    axs[1, 0].set_title("log(KDE) forward")
    draw_plot(fn, save_dir, **kwargs)


def plot_state_nd(
    model, z_samp, z_data, idx_epoch, loss, panel_size=None, save_dir=".", **kwargs
):
    """Pair plot with all dimension pairs."""
    alpha = 0.5
    d = z_data.shape[1]
    if d > 10:
        print("Too many pair plots! Skipping.")
        return
    nplots = int(d * (d - 1) / 2)
    if panel_size is None:
        panel_size = 6.0 if (nplots == 1) else 4.0
    nrows, ncols = determine_nrows_ncols(nplots)
    figsize = (panel_size * ncols, panel_size * nrows)
    fix, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    counter = 0
    for i in range(0, d):
        for j in range(i + 1, d):
            c = counter % ncols
            r = int(np.floor(counter / ncols))
            title = "dim " + str(i + 1) + " vs. dim " + str(j + 1)

            # Scatter plot (and possible quiver)
            if nplots > 1:
                axis = ax[r, c] if nrows > 1 else ax[c]
            else:
                axis = ax
            axis.scatter(z_data[:, i], z_data[:, j], alpha=alpha)
            axis.scatter(z_samp[:, i], z_samp[:, j], alpha=alpha, marker="x")
            axis.set_title(title)
            counter += 1

    # Remove extra subplots
    while counter < nrows * ncols:
        c = counter % ncols
        r = int(np.floor(counter / ncols))
        axis = ax[r, c] if nrows > 1 else ax[c]
        axis.axis("off")
        counter += 1

    # save
    epoch_str = "{0:04}".format(idx_epoch)
    save_name = "fig_" + epoch_str + ".png"
    draw_plot(save_name, save_dir, **kwargs)


def plot_sde_2d(model, z_data, z_traj, idx_epoch, save_dir=".", **kwargs):
    plt.figure(figsize=(8, 8))
    plt.scatter(z_data[:, 0], z_data[:, 1], color="black", alpha=0.1)
    J = z_traj.shape[1]
    for j in range(J):
        zj = z_traj[:, j, :]
        plt.plot(zj[:, 0], zj[:, 1], color="red", alpha=0.7)
    epoch_str = "{0:04}".format(idx_epoch)
    title = "sde trajectories, epoch = " + epoch_str
    fn = "sde_" + epoch_str + ".png"
    plt.title(title)
    draw_plot(fn, save_dir, **kwargs)


def plot_sde_nd(
    model, z_data, z_traj, idx_epoch, panel_size=None, save_dir=".", **kwargs
):
    """Pair plot with all dimension pairs."""
    d = z_data.shape[1]
    if d > 10:
        print("Too many pair plots! Skipping.")
        return
    nplots = int(d * (d - 1) / 2)
    if panel_size is None:
        panel_size = 6.0 if (nplots == 1) else 4.0
    nrows, ncols = determine_nrows_ncols(nplots)
    figsize = (panel_size * ncols, panel_size * nrows)
    fix, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    counter = 0
    for i in range(0, d):
        for j in range(i + 1, d):
            c = counter % ncols
            r = int(np.floor(counter / ncols))
            title = "dim " + str(i + 1) + " vs. dim " + str(j + 1)

            # Scatter plot (and possible quiver)
            if nplots > 1:
                axis = ax[r, c] if nrows > 1 else ax[c]
            else:
                axis = ax
            axis.scatter(z_data[:, i], z_data[:, j], alpha=0.3, color="black")
            n_traj = z_traj.shape[1]
            for k in range(0, n_traj):
                zi = z_traj[:, k, i]
                zj = z_traj[:, k, j]
                axis.plot(zi, zj, color="red", alpha=0.7)
                axis.plot(zi[0], zj[0], "rx", alpha=0.05)
            axis.set_title(title)
            counter += 1

    # Remove extra subplots
    while counter < nrows * ncols:
        c = counter % ncols
        r = int(np.floor(counter / ncols))
        axis = ax[r, c] if nrows > 1 else ax[c]
        axis.axis("off")
        counter += 1

    # save
    epoch_str = "{0:04}".format(idx_epoch)
    save_name = "sde_" + epoch_str + ".png"
    draw_plot(save_name, save_dir, **kwargs)
