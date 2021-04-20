from .data import create_linedata, create_pointdata

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

package_name = "hdviz"
__version__ = importlib_metadata.version(package_name)

__all__ = ["create_linedata", "create_pointdata"]
