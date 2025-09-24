# Observability

This document outlines the monitoring stack for InfoTerminal.

## Architecture

```text
Services (FastAPI) → Prometheus → Grafana
```

Every service exposes metrics at `/metrics`. Prometheus scrapes the
endpoints and Grafana renders dashboards from the collected time series.

## Service Metrics

| Service | Key metrics |
| --- | --- |
| `search-api` | `search_requests_total`, `search_errors_total`, `search_latency_seconds`, `search_rerank_requests_total`, `search_rerank_latency_seconds` |
| `graph-api` | `graph_requests_total`, `graph_geo_queries_total`, `geo_query_count`, `graph_geo_query_errors_total` |
| `doc-entities` | `doc_entities_resolver_runs_total`, `doc_entities_resolver_outcomes_total`, `doc_entities_linking_status_total`, `doc_entities_resolver_latency_seconds` |
| `graph-views` | `graph_views_requests_total`, `graph_views_errors_total` |

## Label Baseline & CI Gate

- Every FastAPI service enables metrics via `_shared.obs.metrics_boot.enable_prometheus_metrics`, which injects constant labels `service`, `version`, and `env` (optionally `tenant`).
- `/healthz`, `/readyz`, and `/metrics` endpoints are mandatory. The generated `inventory/observability.json` captures coverage per service.
- CI runs the **Observability Baseline** job (`python scripts/generate_inventory.py` → `python scripts/check_observability_baseline.py`) to fail fast if endpoints or labels are missing.

## Prometheus

- Scrape interval: **10s**
- Scrape timeout: **5s**
- Retention: **7d**

Configuration lives in `deploy/prometheus/prometheus.yml`.

## Grafana

Grafana is pre-provisioned with a Prometheus datasource and dashboards under the folder **InfoTerminal**. Wave 2 adds resolver outcome and geospatial panels to `monitoring/grafana-dashboards/infoterminal-overview.json` so teams can track linking status splits and `/geo` query volumes at a glance.

## Troubleshooting

- `/metrics` returns 404 → middleware not enabled.
- `up == 0` in Prometheus → target or port unreachable.
- Latency panels show no data → check histogram buckets match requests.
