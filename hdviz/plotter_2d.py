from matplotlib import pyplot as plt
from .utils import create_grid_around
from .plotter import Plotter
import numpy as np


class Plotter2d(Plotter):
    """Main 2d visualization class."""

    def __init__(self):
        super().__init__()
        self.num_dims = 2

    def plot(self, title=None, figsize=None, axis_limits=None, square=False, ax=None):

        # Setup and create figure
        self.plot_setup(figsize, axis_limits, square)
        if ax is None:
            fig, ax = plt.subplots(1, 1, figsize=self.figsize)

        # Plot arrows, points and lines
        self.plot_arrows(ax)
        self.plot_points(ax)
        self.plot_lines(ax)

        # Set legend, title and axis limits
        if self.num_pointsets() > 0:
            ax.legend()
        AL = self.get_axis_limits()
        if AL is not None:
            ax.set_xlim(AL[0][0], AL[0][1])
            ax.set_ylim(AL[1][0], AL[1][1])
        if title is not None:
            ax.set_title(title)
        ax.set_xlabel("Dim 1")
        ax.set_ylabel("Dim 2")
        return ax

    def plot_arrows(self, ax):
        for qs in self.quiver_sets:
            ax.quiver(
                qs.x[:, 0],
                qs.x[:, 1],
                qs.v[:, 0],
                qs.v[:, 1],
                color=qs.color,
                alpha=qs.alpha,
                label=qs.label,
                **self.quiver_kwargs
            )

    def plot_points(self, ax):
        for ps in self.point_sets:
            ax.scatter(
                ps.x[:, 0],
                ps.x[:, 1],
                color=ps.color,
                marker=ps.marker,
                alpha=ps.alpha,
                label=ps.label,
                **self.scatter_kwargs
            )

    def plot_lines(self, ax):
        for ls in self.line_sets:
            for j in range(0, ls.num_lines):
                ax.plot(
                    ls.x[j, :, 0],
                    ls.x[j, :, 1],
                    color=ls.color,
                    linestyle=ls.style,
                    alpha=ls.alpha,
                    **self.lines_kwargs
                )


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
