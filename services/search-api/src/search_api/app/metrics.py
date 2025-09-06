from prometheus_client import Counter, Histogram

SEARCH_REQUESTS = Counter(
    "search_requests_total", "Total search requests", ["rerank"]
)
SEARCH_ERRORS = Counter(
    "search_errors_total", "Search errors", ["type"]
)
SEARCH_LATENCY = Histogram(
    "search_latency_seconds",
    "Search latency seconds",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)
RERANK_REQS = Counter(
    "search_rerank_requests_total", "Rerank requests"
)
RERANK_LATENCY = Histogram(
    "search_rerank_latency_seconds",
    "Rerank latency",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2],
)

READYZ_LATENCY = Histogram(
    "readyz_latency_seconds",
    "Latency of /readyz endpoint",
    ["service"],
)
