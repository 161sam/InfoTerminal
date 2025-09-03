# Observability

This stack wires application traces, metrics and logs through a common pipeline.

## Architecture

Applications emit OTLP data which is collected by the **OpenTelemetry Collector**. Traces are exported to **Tempo** and metrics to **Prometheus**. Logs are shipped separately by **Promtail** to **Loki**.

```
Apps → OTLP → Otel-Collector → Tempo / Prometheus
Logs → Promtail → Loki
```

Grafana provides dashboards and access to all data sources.

## Environment

Each service is configured with the following defaults:

| Variable | Value |
|----------|-------|
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://otel-collector.default.svc:4317` |
| `OTEL_SERVICE_NAME` | name of the service |
| `OTEL_TRACES_SAMPLER` | `parentbased_traceidratio` |
| `OTEL_TRACES_SAMPLER_ARG` | `0.2` |

## Dashboards

Two core dashboards are provisioned:

- **API SLO** – latency (p95/p99), throughput and error rate for HTTP endpoints.
- **Infra Overview** – pod CPU/memory, restarts and collector/promtail stats.

## Troubleshooting

- **No traces?** Ensure the sampler env vars are set and the collector is reachable.
- **No metrics?** Check that `/metrics` responds and Prometheus has a scrape config.
- **Missing logs?** Confirm promtail is running and targets are discovered in Grafana Loki.
