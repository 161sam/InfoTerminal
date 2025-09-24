# Observability

This document outlines the monitoring stack for InfoTerminal.

## Architecture

```text
Services (FastAPI/Express) → Prometheus + Tempo → Grafana
```

Every service exposes metrics at `/metrics`. Prometheus scrapes the
endpoints and Grafana renders dashboards from the collected time series.
When tracing is enabled (`IT_OTEL=1`) the OpenTelemetry SDK publishes spans
to Tempo (default) or Jaeger (optional) so teams can correlate logs, metrics
and traces from a single Grafana view.

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

The `grafana/dashboards/api-slo.json` dashboard now ships Tempo-backed tiles
for trace latency (p95) and top endpoints. Use these to validate that trace
propagation is wired correctly and that slow spans surface alongside the
existing HTTP metrics.

## Tracing (Tempo / Jaeger)

### Quickstart

1. Export the tracing flags:
   ```bash
   export IT_OTEL=1
   export IT_OTEL_EXPORTER=otlp        # or `jaeger`
   export OTEL_EXPORTER_OTLP_ENDPOINT=${OTEL_EXPORTER_OTLP_ENDPOINT:-http://tempo:4318}
   ```
2. Start the gateway (or any FastAPI service using `_shared.obs.otel_boot`).
3. Call the smoke endpoint to emit a demo span:
   ```bash
   curl -H "traceparent: 00-$(openssl rand -hex 16)-$(openssl rand -hex 8)-01" \
        http://localhost:8080/demo/trace
   ```
4. Open Grafana → **API SLO** dashboard and inspect the Tempo search panels
   or query Tempo directly via TraceQL: `{ service.name = "gateway" }`.

### Environment Flags

| Variable | Default | Purpose |
| --- | --- | --- |
| `IT_OTEL` | `0` | Enables the OpenTelemetry bootstrap (FastAPI + HTTPX + Requests instrumentation). |
| `IT_OTEL_EXPORTER` | `otlp` | Selects the trace exporter: `otlp` (Tempo/OTLP HTTP) or `jaeger` (Jaeger collector). |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://tempo:4318` | OTLP/HTTP endpoint for Tempo. |
| `OTEL_EXPORTER_JAEGER_ENDPOINT` | `http://jaeger:14268/api/traces` | Collector endpoint when Jaeger export is active. |
| `OTEL_PROPAGATORS` | `tracecontext,baggage` | Default W3C propagation; override to add B3 etc. |
| `OTEL_TRACES_SAMPLER_ARG` | `0.1` | Trace sampling ratio (parent-based). |

### Log and Header Correlation

- Structured JSON logs now include `trace_id`, `span_id`, and the existing
  `request_id` field so Kibana/Loki queries can pivot between logs and
  Tempo.
- Response headers expose `X-Trace-Id` / `X-Span-Id` alongside `X-Request-Id`.
- Outbound HTTP calls (HTTPX, Requests, Express HTTP) automatically forward
  the inbound `traceparent`/`tracestate` headers, ensuring W3C propagation
  across OPA, ops-controller, and downstream APIs.

## Troubleshooting

- `/metrics` returns 404 → middleware not enabled.
- `up == 0` in Prometheus → target or port unreachable.
- Latency panels show no data → check histogram buckets match requests.
