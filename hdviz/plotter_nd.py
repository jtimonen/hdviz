from matplotlib import pyplot as plt
from .plotter import Plotter
from .utils import determine_nrows_ncols
import numpy as np


class PlotterNd(Plotter):
    """Main high-dimensional visualization class."""

    def __init__(self, num_dims: int):
        super().__init__()
        if num_dims > 10:
            raise RuntimeError("too many dimensions!")
        if num_dims < 3:
            raise RuntimeError("num_dims must be at least 3!")
        self.num_dims = num_dims

    def num_plots(self):
        d = self.num_dims
        return int(d * (d - 1) / 2)

    def axes_array_shape(self):
        nrows, ncols = determine_nrows_ncols(self.num_plots())
        return nrows, ncols

    def create_figure(self, figsize=None):
        nplots = self.num_plots()
        nrows, ncols = self.axes_array_shape()
        if figsize is None:
            panel_size = 6.0 if (nplots == 1) else 4.0
        else:
            panel_size = min(figsize[0] / ncols, figsize[1] / nrows)
        figsize = (panel_size * ncols, panel_size * nrows)
        fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        return fig, axs

    def plot(self, title=None, figsize=None, axis_limits=None, square=False):

        # Setup and create figure
        fig, axs = self.create_figure(figsize)
        self.plot_setup(figsize, axis_limits, square)

        # Plot arrows, points and lines
        self.plot_arrows(axs)
        self.plot_points(axs)
        self.plot_lines(axs)
        self.finish_plot(axs)
        return fig, axs

    def finish_plot(self, axs):
        d = self.num_dims
        nrows, ncols = self.axes_array_shape()
        counter = 0

        # Set titles and axis limits
        AL = self.get_axis_limits()
        for i in range(0, d):
            for j in range(i + 1, d):
                c = counter % ncols
                r = int(np.floor(counter / ncols))
                title = "dim " + str(i + 1) + " vs. dim " + str(j + 1)
                axis = axs[r, c] if nrows > 1 else axs[c]
                if AL is not None:
                    axis.set_xlim(AL[i][0], AL[i][1])
                    axis.set_ylim(AL[j][0], AL[j][1])
                axis.set_title(title)
                counter += 1

        # Remove extra subplots
        while counter < nrows * ncols:
            c = counter % ncols
            r = int(np.floor(counter / ncols))
            axis = axs[r, c] if nrows > 1 else axs[c]
            axis.axis("off")
            counter += 1

    def plot_arrows(self, axs):
        d = self.num_dims
        nrows, ncols = self.axes_array_shape()
        counter = 0
        for i in range(0, d):
            for j in range(i + 1, d):
                c = counter % ncols
                r = int(np.floor(counter / ncols))
                axis = axs[r, c] if nrows > 1 else axs[c]
                for qs in self.quiver_sets:
                    axis.quiver(
                        qs.x[:, i],
                        qs.x[:, j],
                        qs.v[:, i],
                        qs.v[:, j],
                        color=qs.color,
                        alpha=qs.alpha,
                        label=qs.label,
                        **self.quiver_kwargs
                    )
                counter += 1

    def plot_points(self, axs):
        d = self.num_dims
        nrows, ncols = self.axes_array_shape()
        counter = 0
        for i in range(0, d):
            for j in range(i + 1, d):
                c = counter % ncols
                r = int(np.floor(counter / ncols))
                axis = axs[r, c] if nrows > 1 else axs[c]
                for ps in self.point_sets:
                    axis.scatter(
                        ps.x[:, i],
                        ps.x[:, j],
                        color=ps.color,
                        marker=ps.marker,
                        alpha=ps.alpha,
                        label=ps.label,
                        **self.scatter_kwargs
                    )
                counter += 1

    def plot_lines(self, axs):
        d = self.num_dims
        nrows, ncols = self.axes_array_shape()
        counter = 0
        for i in range(0, d):
            for j in range(i + 1, d):
                c = counter % ncols
                r = int(np.floor(counter / ncols))
                axis = axs[r, c] if nrows > 1 else axs[c]
                for ls in self.line_sets:
                    for k in range(0, ls.num_lines):
                        axis.plot(
                            ls.x[k, :, i],
                            ls.x[k, :, j],
                            color=ls.color,
                            linestyle=ls.style,
                            alpha=ls.alpha,
                            **self.lines_kwargs
                        )
                counter += 1


def plot_state_nd(
    model, z_samp, z_data, idx_epoch, loss, panel_size=None, save_dir=".", **kwargs
):
    """Pair plot with all dimension pairs."""
    alpha = 0.5
    d = z_data.shape[1]

    # save
    epoch_str = "{0:04}".format(idx_epoch)
    save_name = "fig_" + epoch_str + ".png"
    draw_plot(save_name, save_dir, **kwargs)
