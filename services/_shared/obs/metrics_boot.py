import os
from fastapi import FastAPI


def enable_prometheus_metrics(app: FastAPI, path: str = "/metrics") -> None:
    """Enable Prometheus metrics on the given FastAPI app.

    Metrics are exposed only when the environment variable ``IT_ENABLE_METRICS``
    or the backwards compatible ``IT_OBSERVABILITY`` is set to ``"1"``.
    The metrics endpoint path can be overridden via ``IT_METRICS_PATH``.
    The function is idempotent and safe to call multiple times.
    """
    if getattr(app.state, "metrics_enabled", False):
        return
    if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
        from starlette_exporter import PrometheusMiddleware, handle_metrics

        metrics_path = os.getenv("IT_METRICS_PATH", path)
        app.add_middleware(PrometheusMiddleware)
        app.add_route(metrics_path, handle_metrics)
        app.state.metrics_enabled = True
