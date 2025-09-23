"""Core v1 routes for graph-views service."""
from __future__ import annotations

import time
from typing import Any, Callable

from fastapi import APIRouter


def build_core_router(
    *,
    health_check: Callable[[], Any],
    ready_check: Callable[[], Any],
    service_name: str,
    version: str,
    start_ts: float,
) -> APIRouter:
    """Create the core router exposing health, readiness, and info endpoints."""
    router = APIRouter(tags=["core"])

    @router.get("/healthz")
    def healthz() -> Any:
        return health_check()

    @router.get("/readyz")
    def readyz() -> Any:
        return ready_check()

    @router.get("/info")
    def info() -> dict[str, Any]:
        return {
            "service": service_name,
            "version": version,
            "uptime_seconds": time.monotonic() - start_ts,
        }

    return router
