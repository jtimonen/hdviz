from .plotter_2d import Plotter2d
from .plotter_3d import Plotter3d
from .plotter_nd import PlotterNd

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

package_name = "hdviz"
__version__ = importlib_metadata.version(package_name)

__all__ = ["Plotter2d", "Plotter3d", "PlotterNd"]
