from prometheus_client import Counter

GRAPH_REQS = Counter("graph_requests_total", "Graph requests", ["endpoint"])
