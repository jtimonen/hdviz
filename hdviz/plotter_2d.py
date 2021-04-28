from matplotlib import pyplot as plt
from .plotter import Plotter


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
