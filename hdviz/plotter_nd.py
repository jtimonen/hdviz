from matplotlib import pyplot as plt
from .plotter import Plotter
from .utils import determine_nrows_ncols
import numpy as np


class PlotterNd(Plotter):
    """Main high-dimensional visualization class."""

    def __init__(self, num_dims: int):
        super().__init__()
        self.num_dims = num_dims

    def num_plots(self):
        d = self.num_dims
        return int(d * (d - 1) / 2)

    def create_axes(self, figsize, panelsize, nrows, ncols):
        """Create a figure for plotting dimension pairs to subplots."""
        if figsize is not None:
            raise RuntimeError("use the panelsize argument instead of figsize")
        nplots = self.num_plots()
        nrows, ncols = determine_nrows_ncols(self.num_plots(), nrows, ncols)
        if panelsize is None:
            panelsize = 6.0 if (nplots == 1) else 3.0
        figsize = (panelsize * ncols, panelsize * nrows)
        _, axs = plt.subplots(
            nrows=nrows,
            ncols=ncols,
            figsize=figsize,
            squeeze=False,
            constrained_layout=True,
        )
        return axs

    def plot(
        self,
        figsize=None,
        axis_limits=None,
        square=False,
        nrows=None,
        ncols=None,
        panelsize=None,
        axs=None,
    ):
        """Plot dimension pairs."""

        # Create figure and setup
        axs_not_given = axs is None
        if axs_not_given:
            axs = self.create_axes(figsize, panelsize, nrows, ncols)
        self.plot_setup(figsize, axis_limits, square)

        # Get information
        d = self.num_dims
        nrows, ncols = axs.shape
        AL = self.get_axis_limits()
        counter = 0

        # Loop through dimension pairs
        for i in range(0, d):
            for j in range(i + 1, d):

                # Plot data
                c = counter % ncols
                r = int(np.floor(counter / ncols))
                axis = axs[r, c]
                self.plot_proj_arrows(i, j, axis)
                self.plot_proj_points(i, j, axis)
                self.plot_proj_lines(i, j, axis)

                # Set axis labels and limits
                axis.set_xlabel("dim " + str(i + 1))
                axis.set_ylabel("dim " + str(j + 1))
                if AL is not None:
                    axis.set_xlim(AL[i][0], AL[i][1])
                    axis.set_ylim(AL[j][0], AL[j][1])
                counter += 1

        # Remove extra subplots
        while counter < nrows * ncols:
            c = counter % ncols
            r = int(np.floor(counter / ncols))
            if not axs_not_given:
                axs[r, c].axis("off")
            counter += 1

        return axs

    def plot_proj(self, idx_x: int, idx_y: int, ax):
        """Plot a projection to two of the original dimensions."""
        # Plot arrows, points and lines
        self.plot_proj_arrows(idx_x, idx_y, ax)
        self.plot_proj_points(idx_x, idx_y, ax)
        self.plot_proj_lines(idx_x, idx_y, ax)
        return ax

    def plot_proj_arrows(self, idx_x, idx_y, ax):
        for qs in self.quiver_sets:
            ax.quiver(
                qs.x[:, idx_x],
                qs.x[:, idx_y],
                qs.v[:, idx_x],
                qs.v[:, idx_y],
                color=qs.color,
                alpha=qs.alpha,
                label=qs.label,
                **self.quiver_kwargs
            )
        return ax

    def plot_proj_points(self, idx_x, idx_y, ax):
        for ps in self.point_sets:
            ax.scatter(
                ps.x[:, idx_x],
                ps.x[:, idx_y],
                color=ps.color,
                marker=ps.marker,
                alpha=ps.alpha,
                label=ps.label,
                **self.scatter_kwargs
            )

    def plot_proj_lines(self, idx_x, idx_y, ax):
        for ls in self.line_sets:
            for k in range(0, ls.num_lines):
                ax.plot(
                    ls.x[k, :, idx_x],
                    ls.x[k, :, idx_y],
                    color=ls.color,
                    linestyle=ls.style,
                    alpha=ls.alpha,
                    **self.lines_kwargs
                )
