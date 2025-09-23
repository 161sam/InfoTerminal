"""Compatibility module exposing the standardised Search API app.

The service implementation now lives in :mod:`search_api.app.main_v1`.  We
re-export the FastAPI application object and common globals so existing
imports (tests, deployment scripts, uvicorn entry points) continue to work
without change while benefitting from the v1 API contracts.
"""

from .main_v1 import app, client, settings  # noqa: F401

__all__ = ["app", "client", "settings"]
