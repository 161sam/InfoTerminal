"""Prometheus collectors for the plugin runner service."""

from __future__ import annotations

from prometheus_client import Counter, Histogram


PLUGIN_RUN_TOTAL = Counter(
    "plugin_run_total",
    "Total number of plugin executions",
    labelnames=("plugin",),
)

PLUGIN_RUN_FAILURE_TOTAL = Counter(
    "plugin_run_failures_total",
    "Total number of failed plugin executions",
    labelnames=("plugin",),
)

PLUGIN_RUN_DURATION_SECONDS = Histogram(
    "plugin_run_duration_seconds",
    "Observed runtime of plugin executions",
    labelnames=("plugin",),
    buckets=(0.5, 1, 2, 5, 10, 30, 60, 120, 300, 600),
)


__all__ = [
    "PLUGIN_RUN_TOTAL",
    "PLUGIN_RUN_FAILURE_TOTAL",
    "PLUGIN_RUN_DURATION_SECONDS",
]

