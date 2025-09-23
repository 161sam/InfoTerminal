"""Prometheus metrics for the graph-api service."""

from prometheus_client import Counter, Histogram

# Legacy request/readyz metrics retained for backwards compatibility
GRAPH_REQS = Counter("graph_requests_total", "Graph requests", ["endpoint"])

READYZ_LATENCY = Histogram(
    "readyz_latency_seconds",
    "Latency of /readyz endpoint",
    ["service"],
)

# Phase 2 Wave 1 metrics
GRAPH_ANALYSIS_QUERIES = Counter(
    "graph_analysis_queries_total",
    "Total count of graph analysis queries",
    ["algorithm", "status"],
)

GRAPH_ANALYSIS_DURATION = Histogram(
    "graph_analysis_duration_seconds",
    "Duration of graph analysis queries",
    ["algorithm", "status"],
)

GRAPH_SUBGRAPH_EXPORTS = Counter(
    "graph_subgraph_exports_total",
    "Number of dossier subgraph exports produced",
    ["format", "status"],
)

GRAPH_SUBGRAPH_EXPORT_DURATION = Histogram(
    "graph_subgraph_export_duration_seconds",
    "Duration of dossier subgraph exports",
    ["format", "status"],
)

# Wave 2 geospatial metrics
GRAPH_GEO_QUERIES = Counter(
    "graph_geo_queries_total",
    "Geospatial API queries grouped by type",
    ["type"],
)

GRAPH_GEO_QUERY_ERRORS = Counter(
    "graph_geo_query_errors_total",
    "Geospatial API errors grouped by type",
    ["type"],
)
