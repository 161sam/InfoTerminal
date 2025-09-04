"""InfoTerminal CLI package."""
from importlib import metadata

try:
    __version__ = metadata.version("infoterminal-cli")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0.dev"

__all__ = ["__version__"]
