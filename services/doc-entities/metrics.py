"""Prometheus metrics used by the doc-entities service."""

from __future__ import annotations

from typing import Callable, TypeVar

from prometheus_client import Counter, Histogram, REGISTRY

T = TypeVar("T", Counter, Histogram)


def _get_or_register(name: str, factory: Callable[[], T]) -> T:
    """Return an existing collector from the global registry or create it.

    In development the FastAPI reloader instantiates the module multiple times.
    We therefore reuse registered collectors instead of raising duplicate-name
    errors. The helper keeps the behaviour idempotent for tests and local runs.
    """

    existing = REGISTRY._names_to_collectors.get(name)
    if existing is not None:
        return existing  # type: ignore[return-value]
    collector = factory()
    return collector


RESOLVER_RUNS = _get_or_register(
    "doc_entities_resolver_runs_total",
    lambda: Counter(
        "doc_entities_resolver_runs_total",
        "Total resolver executions grouped by mode",
        ["mode"],
    ),
)

RESOLVER_OUTCOMES = _get_or_register(
    "doc_entities_resolver_outcomes_total",
    lambda: Counter(
        "doc_entities_resolver_outcomes_total",
        "Resolver outcomes (resolved / unmatched / ambiguous / error)",
        ["status"],
    ),
)

RESOLVER_STATUS_COUNTS = _get_or_register(
    "doc_entities_linking_status_total",
    lambda: Counter(
        "doc_entities_linking_status_total",
        "Cumulative count of entity linking statuses surfaced to clients",
        ["status"],
    ),
)

RESOLVER_CONFIDENCE = _get_or_register(
    "doc_entities_resolver_best_candidate_confidence",
    lambda: Histogram(
        "doc_entities_resolver_best_candidate_confidence",
        "Confidence distribution for best resolver candidates",
        buckets=[0.0, 0.25, 0.5, 0.65, 0.75, 0.85, 0.9, 0.95, 1.0],
    ),
)

RESOLVER_LATENCY = _get_or_register(
    "doc_entities_resolver_latency_seconds",
    lambda: Histogram(
        "doc_entities_resolver_latency_seconds",
        "Resolver execution latency",
        ["mode"],
        buckets=(0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0),
    ),
)

