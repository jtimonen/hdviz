from matplotlib import pyplot as plt
from .plotter import Plotter


class Plotter3d(Plotter):
    """Main 3d visualization class."""

    def __init__(self):
        super().__init__()
        self.num_dims = 3
        self.azimuth = -60
        self.elevation = 30

    def set_perspective(self, azimuth: float, elevation: float):
        """Set 3d perspective.
        :param azimuth: Azimuthal viewing angle (default = -60).
        :param elevation: Elevation viewing angle (default = 30).
        """
        self.azimuth = azimuth
        self.elevation = elevation

    def plot(self, figsize=None, axis_limits=None, square=False, ax=None, title=None):

        # Setup and create figure
        self.plot_setup(figsize, axis_limits, square)
        if ax is None:
            fig = plt.figure(figsize=self.figsize)
            ax = fig.add_subplot(1, 1, 1, projection="3d")
        ax.view_init(elev=self.elevation, azim=self.azimuth)

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
            ax.set_zlim(AL[2][0], AL[2][1])
        if title is not None:
            ax.set_title(title)
        ax.set_xlabel("Dim 1")
        ax.set_ylabel("Dim 2")
        ax.set_zlabel("Dim 3")
        return ax

    def plot_arrows(self, ax):
        for qs in self.quiver_sets:
            ax.quiver(
                qs.x[:, 0],
                qs.x[:, 1],
                qs.x[:, 2],
                qs.v[:, 0],
                qs.v[:, 1],
                qs.v[:, 2],
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
                ps.x[:, 2],
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
                    ls.x[j, :, 2],
                    color=ls.color,
                    linestyle=ls.style,
                    alpha=ls.alpha,
                    **self.lines_kwargs
                )
