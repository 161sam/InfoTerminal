from prometheus_client import Histogram

READYZ_LATENCY = Histogram(
    "readyz_latency_seconds",
    "Latency of /readyz endpoint",
    ["service"],
)
