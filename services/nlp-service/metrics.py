from prometheus_client import Counter, Histogram

NLP_REQS = Counter("nlp_requests_total", "NLP requests", ["type"])
NLP_LATENCY = Histogram(
    "nlp_latency_seconds",
    "NLP latency",
    ["type"],
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)
