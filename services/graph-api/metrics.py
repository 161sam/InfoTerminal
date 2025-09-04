from prometheus_client import Counter, Histogram

GRAPH_REQS = Counter("graph_requests_total", "Graph requests", ["endpoint"])

READYZ_LATENCY = Histogram(
    "readyz_latency_seconds",
    "Latency of /readyz endpoint",
    ["service"],
)
