"""Compatibility module exposing the standardised Graph API app.

The service implementation now lives in :mod:`graph_api.app.main_v1`. We
re-export the FastAPI application object and selected globals so existing
imports (tests, deployment scripts, uvicorn entry points) continue to work
while the service is served by the v1-compliant stack.
"""

from .main_v1 import app, driver  # noqa: F401
from _shared.health import probe_db as probe_db  # legacy compatibility

__all__ = ["app", "driver", "probe_db"]
