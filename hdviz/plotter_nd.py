from matplotlib import pyplot as plt
from .plotter import Plotter
import numpy as np


class PlotterNd(Plotter):
    """Main high-dimensional visualization class."""

    def __init__(self):
        super().__init__()
        self.save_dir = "."
        super.__init__()

    def plot(self):
        print("moi")


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
