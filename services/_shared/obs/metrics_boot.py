"""Shared helpers for exposing Prometheus metrics with mandatory labels."""

from __future__ import annotations

import os
from typing import Dict, Optional

from fastapi import FastAPI


REQUIRED_LABELS = ("service", "version", "env")
OPTIONAL_LABELS = ("tenant",)


def _normalise(value: str) -> str:
    return value.strip().lower().replace(" ", "_") if value else "unknown"


def _derive_constant_labels(
    app: FastAPI,
    service_name: Optional[str],
    service_version: Optional[str],
    environment: Optional[str],
    tenant: Optional[str],
) -> Dict[str, str]:
    service = (
        service_name
        or os.getenv("IT_SERVICE_NAME")
        or getattr(app, "title", None)
        or "unknown"
    )
    version = (
        service_version
        or os.getenv("IT_SERVICE_VERSION")
        or getattr(app, "version", None)
        or "unknown"
    )
    env = environment or os.getenv("IT_ENV") or os.getenv("ENVIRONMENT") or "dev"

    labels: Dict[str, str] = {
        "service": _normalise(str(service)),
        "version": str(version),
        "env": _normalise(str(env)),
    }

    tenant_value = tenant or os.getenv("IT_TENANT") or os.getenv("IT_TENANT_ID")
    if tenant_value:
        labels["tenant"] = _normalise(str(tenant_value))

    return labels


def enable_prometheus_metrics(
    app: FastAPI,
    path: str = "/metrics",
    *,
    service_name: Optional[str] = None,
    service_version: Optional[str] = None,
    environment: Optional[str] = None,
    tenant: Optional[str] = None,
) -> None:
    """Enable Prometheus metrics on the given FastAPI app.

    Metrics are exposed only when ``IT_ENABLE_METRICS`` or the backwards
    compatible ``IT_OBSERVABILITY`` flag is set to ``"1"``. The metrics path can
    be overridden via ``IT_METRICS_PATH``. The function is idempotent and safe to
    call multiple times. When enabled, a constant label set is attached so that
    every service exports at minimum ``service``, ``version`` and ``env`` labels.
    """

    if getattr(app.state, "metrics_enabled", False):
        return

    if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
        from starlette_exporter import PrometheusMiddleware, handle_metrics

        metrics_path = os.getenv("IT_METRICS_PATH", path)
        constant_labels = _derive_constant_labels(
            app,
            service_name=service_name,
            service_version=service_version,
            environment=environment,
            tenant=tenant,
        )
        middleware_kwargs = {
            "labels": constant_labels,
            "app_name": constant_labels.get("service", "service"),
        }
        app.add_middleware(PrometheusMiddleware, **middleware_kwargs)
        app.add_route(metrics_path, handle_metrics)
        app.state.metrics_enabled = True
