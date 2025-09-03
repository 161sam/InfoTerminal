"""Background entity resolver skeleton.

Future implementation will pull pending entities from the database and
resolve them against Neo4j. The functions here are stubs so that the API
can schedule work without crashing.
"""
from typing import Iterable
import time

from metrics import RESOLVER_RUNS, RESOLVER_ENTS, RESOLVER_LAT


def resolve_entities(entity_ids: Iterable[str], mode: str = "async") -> None:
    """Placeholder resolver with metrics hooks."""
    RESOLVER_RUNS.labels(mode=mode).inc()
    start = time.perf_counter()
    n_unmatched = 0
    for _ in entity_ids:
        n_unmatched += 1
    RESOLVER_ENTS.labels(status="unmatched").inc(n_unmatched)
    RESOLVER_LAT.observe(time.perf_counter() - start)
