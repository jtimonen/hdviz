from matplotlib import pyplot as plt
from .utils import create_grid_around, draw_plot
from .plotter import Plotter


class Plotter3d(Plotter):
    """Main 3d visualization class.

    :param azimuth: 3d plot azimuth
    :param elevation: 3d plot elevation
    """

    def __init__(self, azimuth: float = 45, elevation: float = 45):
        super().__init__()
        self.azimuth = azimuth
        self.elevation = elevation

    def set_perspective(self, azimuth: float, elevation: float):
        self.azimuth = azimuth
        self.elevation = elevation


def plot_state_3d(model, z_samp, z_data, idx_epoch, loss, save_dir=".", **kwargs):
    fig = plt.figure(figsize=(13, 13))
    H = model.H_3d
    azim = model.azimuth_3d
    elev = model.elevation_3d
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax1.view_init(elev=elev, azim=azim)
    ax2.view_init(elev=elev, azim=azim)
    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)

    ax1.scatter(z_data[:, 0], z_data[:, 1], z_data[:, 2], alpha=0.3)
    ax1.set_xlim(-H, H)
    ax1.set_ylim(-H, H)
    ax1.set_zlim(-H, H)

    ax2.scatter(z_samp[:, 0], z_samp[:, 1], z_samp[:, 2], color="orange", alpha=0.3)
    ax2.set_xlim(-H, H)
    ax2.set_ylim(-H, H)
    ax2.set_zlim(-H, H)

    ax3.scatter(z_data[:, 0], z_data[:, 1], alpha=0.7)
    ax3.scatter(z_samp[:, 0], z_samp[:, 1], marker="x", alpha=0.7)
    ax3.set_xlim(-H, H)
    ax3.set_ylim(-H, H)

    ax4.scatter(z_data[:, 1], z_data[:, 2], alpha=0.7)
    ax4.scatter(z_samp[:, 1], z_samp[:, 2], marker="x", alpha=0.7)
    ax4.set_xlim(-H, H)
    ax4.set_ylim(-H, H)

    epoch_str = "{0:04}".format(idx_epoch)
    loss_str = "{:.5f}".format(loss)
    title = "epoch " + epoch_str + ", valid_loss = " + loss_str
    fn = "fig_" + epoch_str + ".png"
    ax1.set_title(title)
    ax2.set_title("forward")
    ax3.set_title("dim 1 vs. dim 2")
    ax4.set_title("dim 2 vs. dim 3")
    draw_plot(fn, save_dir, **kwargs)


def plot_sde_3d(model, z_data, z_traj, idx_epoch, save_dir=".", **kwargs):
    fig = plt.figure(figsize=(13, 13))
    H = model.H_3d
    azim = model.azimuth_3d
    elev = model.elevation_3d
    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    ax1.view_init(elev=elev, azim=azim)
    ax2.view_init(elev=elev, azim=azim)

    ax3 = fig.add_subplot(2, 2, 3)
    ax4 = fig.add_subplot(2, 2, 4)
    J = z_traj.shape[1]

    ax1.scatter(z_data[:, 0], z_data[:, 1], z_data[:, 2], color="black", alpha=0.3)
    ax1.set_xlim(-H, H)
    ax1.set_ylim(-H, H)
    ax1.set_zlim(-H, H)

    ax2.set_xlim(-H, H)
    ax2.set_ylim(-H, H)
    ax2.set_zlim(-H, H)

    ax3.scatter(z_data[:, 0], z_data[:, 1], color="black", alpha=0.7)
    ax4.scatter(z_data[:, 1], z_data[:, 2], color="black", alpha=0.7)
    ax3.set_xlim(-H, H)
    ax3.set_ylim(-H, H)
    ax4.set_xlim(-H, H)
    ax4.set_ylim(-H, H)
    for j in range(J):
        ax2.plot(
            z_traj[:, j, 0], z_traj[:, j, 1], z_traj[:, j, 2], color="red", alpha=0.7
        )
        ax3.plot(z_traj[:, j, 0], z_traj[:, j, 1], color="red", alpha=0.7)
        ax4.plot(z_traj[:, j, 1], z_traj[:, j, 2], color="red", alpha=0.7)

    epoch_str = "{0:04}".format(idx_epoch)
    title = "epoch " + epoch_str
    fn = "sde_" + epoch_str + ".png"
    ax1.set_title(title)
    ax2.set_title("forward")
    ax3.set_title("dim 1 vs. dim 2")
    ax4.set_title("dim 2 vs. dim 3")
    draw_plot(fn, save_dir, **kwargs)
