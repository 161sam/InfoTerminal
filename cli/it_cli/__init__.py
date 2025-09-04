"""InfoTerminal CLI package."""
from importlib import metadata

try:
    __version__ = metadata.version("infoterminal-cli")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0.dev"

__all__ = ["__version__"]

# Auto banner (once-per-process), can be disabled via IT_NO_BANNER=1 or --no-banner
try:
    from .banner import auto_banner_on_import as _it_banner_auto
    _it_banner_auto()
except Exception:
    # never fail import because of banner
    pass
