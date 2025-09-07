"""Search API application package.

The legacy ``search_api.app`` module is optionally imported for backward
compatibility, but missing it is fine when only the ``app`` package is
installed.
"""

try:  # pragma: no cover - optional compatibility shim
    from search_api.app import *  # type: ignore  # noqa: F401,F403
except ModuleNotFoundError:  # pragma: no cover - search_api not installed
    pass
