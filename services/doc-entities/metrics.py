from prometheus_client import Counter, Histogram

RESOLVER_RUNS = Counter(
    "resolver_runs_total", "Resolver runs total", ["mode"]
)
RESOLVER_ENTS = Counter(
    "resolver_entities_total", "Entities processed", ["status"]
)
RESOLVER_LAT = Histogram(
    "resolver_latency_seconds",
    "Resolver run latency",
    buckets=[0.1, 0.25, 0.5, 1, 2, 5, 10],
)
