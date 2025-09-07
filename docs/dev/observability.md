# Observability

This document outlines the monitoring stack for InfoTerminal.

## Architecture

```text
Services (FastAPI) → Prometheus → Grafana
```

Every service exposes metrics at `/metrics`. Prometheus scrapes the
endpoints and Grafana renders dashboards from the collected time series.

## Service Metrics

| Service        | Metrics                                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `search-api`   | `search_requests_total`, `search_errors_total`, `search_latency_seconds`, `search_rerank_requests_total`, `search_rerank_latency_seconds` |
| `graph-api`    | `graph_requests_total`                                                                                                                    |
| `doc-entities` | `resolver_runs_total`, `resolver_entities_total`, `resolver_latency_seconds`                                                              |
| `nlp-service`  | `nlp_requests_total`, `nlp_latency_seconds`                                                                                               |

## Prometheus

- Scrape interval: **10s**
- Scrape timeout: **5s**
- Retention: **7d**

Configuration lives in `deploy/prometheus/prometheus.yml`.

## Grafana

Grafana is pre-provisioned with a Prometheus datasource and three dashboards
(API Overview, Search Rerank, Doc Resolver) under the folder **InfoTerminal**.

## Troubleshooting

- `/metrics` returns 404 → middleware not enabled.
- `up == 0` in Prometheus → target or port unreachable.
- Latency panels show no data → check histogram buckets match requests.
