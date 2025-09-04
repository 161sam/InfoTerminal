# Operability

## Dev Ports
- Frontend: 3411
- search-api: 8401
- graph-api: 8402
- graph-views: 8403
- agents: 3417
- gateway: 8610
- Prometheus: 3412
- Grafana: 3413
- Alertmanager: 3414
- Loki: 3415
- Tempo: 3416

## Health Endpoints
- `GET /healthz` – liveness
- `GET /readyz` – readiness

Both endpoints return JSON in the form:
```json
{
  "status": "ok|degraded|fail",
  "service": "<name>",
  "version": "<git-sha|dev>",
  "time": "<UTC ISO8601>",
  "uptime_s": <float>,
  "checks": { ... }  // only on /readyz
}
```

`/healthz` performs no external checks. `/readyz` reports dependency checks in `checks`. Each check contains a `status` of `ok`, `fail` or `skipped` with optional details.

### `search-api`
- Probes OpenSearch with a short HTTP request (~0.8s timeout) when `OPENSEARCH_URL` is set.
- Example `checks` entry: `{ "opensearch": { "status": "ok", "latency_ms": 42.1 } }`
- If OpenSearch URL is missing the check is `skipped`.

### `graph-api`
- Probes Neo4j via `RETURN 1` with ~0.8s timeout.
- Example `checks` entry: `{ "neo4j": { "status": "ok", "latency_ms": 12.3 } }`
- Missing Neo4j connection details result in a `skipped` check.

### `graph-views`
- Probes Postgres via `SELECT 1` with ~0.8s timeout.
- Example `checks` entry: `{ "postgres": { "status": "ok", "latency_ms": 5.1 } }`
- If the connection pool cannot be initialised the check is `skipped`.

## Environment Flags
- `IT_FORCE_READY`: when set to `1`, `/readyz` skips external checks and reports ready.
- Missing connection details for a dependency result in a `skipped` check with a reason.

## CLI

Die wichtigsten Workflows laufen über den `it`-Befehl:

```bash
it start -d                         # Stack im Hintergrund starten
it status -s graph-api,search-api   # Ready-Checks für Kernservices
it logs -s neo4j -F --lines 200     # Logs folgen
it rm -v                            # Umgebung inkl. Volumes entfernen
```

Weitere Details und Optionen sind in [cli/README.md](../cli/README.md) dokumentiert.

## Structured Logs & Correlation
FastAPI services emit structured JSON logs when `IT_JSON_LOGS=1` (default in development).
Each request returns an `X-Request-Id` header which is generated if missing and echoed back
to callers. A typical access log looks like:

```json
{"ts":"2024-01-01T00:00:00.000Z","level":"info","service":"search-api","env":"dev","req_id":"abc","method":"GET","path":"/healthz","status":200,"dur_ms":1.2,"msg":"request"}
```

Set `IT_OTEL=1` to enrich logs with `trace_id` and `span_id` for correlation when tracing is enabled.

## Observability

Start the monitoring stack separately:

```bash
docker compose -f docker-compose.observability.yml --profile observability up -d
# alternativ, wenn die Dienste im Haupt-Compose ein Profil besitzen
docker compose --profile observability up -d
```

| Service      | Port |
| ------------ | ---- |
| Prometheus   | 3412 |
| Grafana      | 3413 |
| Alertmanager | 3414 |
| Loki         | 3415 |
| Tempo        | 3416 |

`IT_ENABLE_METRICS=1` aktiviert `/metrics`. Setze `IT_OTEL=1`, um Tracing zu aktivieren.

### Quickstart Observability

```bash
it status
docker compose -f docker-compose.observability.yml --profile observability up -d
open http://localhost:3413
open http://localhost:3412
```

### Logs & Traces

Loki (Logs) und Tempo (Traces) starten im gleichen Stack. Services exportieren Traces
via OTLP HTTP an `http://tempo:4318`. Die Sampling-Rate wird über
`OTEL_TRACES_SAMPLER_ARG` gesteuert (Standard `0.1` = 10 %).

### Troubleshooting
- Port-Konflikt? Andere Dienste beenden oder Ports anpassen.
- Doppelte Scrapes in Prometheus? `Status → Targets` prüfen.
- `404` an `/metrics`? `IT_ENABLE_METRICS=1` fehlt.
- Loki/Tempo nicht erreichbar? Container-Logs prüfen (`docker compose logs loki`).
- Leere Logs? Läuft Promtail und stimmen Pfade in `promtail-config.yml`?
- Keine Traces? `IT_OTEL=1` gesetzt und Tempo erreichbar?

## Troubleshooting
- Ensure the Neo4j development password has at least 8 characters.
- Restrict CORS in development to `http://localhost:3411`.
- Disable OTEL exporters in development unless needed.

## Frontend Health Matrix & Settings

- The frontend polls each configured service's `/readyz` endpoint roughly every 10 s and shows a badge per service (`ok`, `degraded`, `fail`, `unknown`). Clicking the matrix reveals latency and any `skipped` checks.
- Endpoint URLs can be overridden via the Settings page. Values are stored in `localStorage` under `it.settings.endpoints` and can be verified with the "Test" button which calls `<base>/healthz`.
