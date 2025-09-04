# Operability

## Quickstart

```bash
pipx install ./cli
it start -d
it status
docker compose -f docker-compose.observability.yml --profile observability up -d
```

Open http://localhost:3411 and verify the health matrix. The frontend includes a **Gateway Proxy** toggle in Settings to route API calls through `http://localhost:8610`.

Metrics and tracing can be enabled with `IT_ENABLE_METRICS=1` and `IT_OTEL=1`.

## Ports

| Service      | Port |
| ------------ | ---- |
| Frontend     | 3411 |
| search-api   | 8401 |
| graph-api    | 8402 |
| graph-views  | 8403 |
| Gateway      | 8610 |
| Agents       | 3417 |
| Prometheus   | 3412 |
| Grafana      | 3413 |
| Alertmanager | 3414 |
| Loki         | 3415 |
| Tempo        | 3416 |

## Health & Readiness
- `GET /healthz` – liveness
- `GET /readyz` – readiness

### JSON Schema
`/healthz`:
```json
{
  "service": "<str>",
  "version": "<str>",
  "status": "ok",
  "time": "<UTC ISO8601>",
  "uptime_s": <float>
}
```

`/readyz`:
```json
{
  "service": "<str>",
  "version": "<str>",
  "status": "ok|degraded|fail",
  "time": "<UTC ISO8601>",
  "uptime_s": <float>,
  "checks": {
    "<dep>": {
      "status": "ok|fail|skipped",
      "latency_ms": <float|null>,
      "error": "<str|null>",
      "reason": "<str|null>"
    }
  }
}
```

### Aggregation & Codes
- Any `fail` → HTTP 503 with `status="fail"`
- No `fail` but at least one `skipped` → HTTP 200 with `status="degraded"`
- All `ok` → HTTP 200 with `status="ok"`

### Feature Flags & Timeouts
- `IT_FORCE_READY=1` skips all probes and returns `status="ok"` with empty `checks`.
- Each probe times out after ~800 ms; timeouts result in `error="timeout"`.

### Service Checks
- **search-api**: OpenSearch `OPENSEARCH_URL/_cluster/health`
- **graph-api**: Neo4j `RETURN 1`
- **graph-views**: Postgres `SELECT 1`

All services return `skipped` when a dependency is not configured.

## CORS
```bash
IT_CORS_ORIGINS=http://localhost:3411,http://127.0.0.1:3411
IT_CORS_CREDENTIALS=0
IT_CORS_MAX_AGE=600
```

If `IT_CORS_ORIGINS` is unset, services default to the development origins above. For production, always specify trusted origins explicitly and avoid wildcards. Credentials are disabled by default and only enabled when `IT_CORS_CREDENTIALS=1`. The `X-Request-Id` header is exposed for correlation.

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

### Metrics & Tracing

| Variable | Default | Beschreibung |
| --- | --- | --- |
| `IT_ENABLE_METRICS` | `0` | `/metrics`-Endpoint aktivieren (auch bei `IT_OBSERVABILITY=1`) |
| `IT_METRICS_PATH` | `/metrics` | Pfad für Prometheus-Scrapes |
| `IT_OTEL` | `0` | OpenTelemetry Tracing aktivieren |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://tempo:4318` | OTLP-Endpoint |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` | OTLP-Protokoll |
| `OTEL_SERVICE_NAME` | Dienstname | Service-Identifier |
| `OTEL_RESOURCE_ATTRIBUTES` | – | zusätzliche Attribute (`k=v,k2=v2`) |
| `OTEL_TRACES_SAMPLER` | `parentbased_traceidratio` | Sampling-Strategie |
| `OTEL_TRACES_SAMPLER_ARG` | `0.1` | Sampling-Rate (z. B. 10 %) |

#### Nur Prometheus-Metrics

```bash
IT_ENABLE_METRICS=1 \\
docker compose -f docker-compose.observability.yml --profile observability up -d
```

#### Tracing aktivieren (Tempo)

```bash
IT_OTEL=1 \\
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:3416 \\
OTEL_TRACES_SAMPLER_ARG=0.1 \\
docker compose -f docker-compose.observability.yml --profile observability up -d
```

> Prometheus findet Targets nur, wenn `/metrics` existiert; Tempo erhält OTLP-Spans nur bei gesetztem `IT_OTEL=1`.

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
- Disable OTEL exporters in development unless needed.

## Frontend Health Matrix & Settings

- The frontend polls each configured service's `/readyz` endpoint roughly every 10 s and shows a badge per service (`ok`, `degraded`, `fail`, `unknown`). Clicking the matrix reveals latency and any `skipped` checks.
- Endpoint URLs can be overridden via the Settings page. Values are stored in `localStorage` under `it.settings.endpoints` and can be verified with the "Test" button which calls `<base>/healthz`.

## Frontend Settings & Deep-Links

- `NEXT_PUBLIC_GRAPH_DEEPLINK_BASE` setzt die Standardbasis für Graph-Deep-Links. Standard ist `/graphx?focus=`.
- Einträge unter `localStorage.it.settings.graph.deeplinkBase` überschreiben den ENV-Wert.
- Fallback-Regel: **LocalStorage > ENV > Default**.
- Werte können relativ (`/graphx?focus=`) oder absolut (`https://graph.dev/graphx?focus=`) sein.
- Programmatic-Use:

```ts
import { buildGraphDeepLink } from '../apps/frontend/lib/deeplink';
const url = buildGraphDeepLink({ id: '123', type: 'entity', filters: { tag: ['a', 'b'] } });
```

- Relatives Beispiel: `/graphx?focus=123&type=entity`
- Absolutes Beispiel: `https://graph.dev/graphx?focus=123`

## Security / Gateway & OPA-Audit

Der optionale Gateway-Dienst (Port 8610) kann sämtlichen API-Verkehr unter `/api/*` bündeln. Im Frontend lässt sich dies über den Abschnitt **Gateway Proxy** aktivieren; Einstellungen werden in `localStorage.it.settings.gateway` persistiert. Bei aktivem Toggle leitet das Frontend Anfragen an `${GATEWAY_URL}/api/search`, `${GATEWAY_URL}/api/graph` und `${GATEWAY_URL}/api/views`.

Start des Gateways:

```bash
docker compose up gateway
```

oder über das CLI.

### Ports & ENV
- `TARGET_SEARCH` – Standard `http://search-api:8080` bzw. `http://127.0.0.1:8611`
- `TARGET_GRAPH` – Standard `http://graph-api:8080` bzw. `http://127.0.0.1:8612`
- `TARGET_VIEWS` – Standard `http://graph-views:8000` bzw. `http://127.0.0.1:8613`
- `CORS_ORIGINS` – erlaubt in Dev `http://localhost:3411,http://127.0.0.1:3411`
- `IT_ENABLE_METRICS=1` – `/metrics` freischalten

### OPA-Integration (Audit)
Der Gateway kann Anfragen gegen eine OPA-Policy prüfen und optional an einen Audit-Sink weiterleiten. Beispiel-Regel:

```rego
package access

default allow = false

allow {
  input.request.path = "/api/search"
  input.request.method = "get"
  input.user.roles[_] == "reader"
}
```

In Entwicklung sind Policies typischerweise permissiv. In Produktion sollten Origins und Regeln strikt konfiguriert werden.

### Troubleshooting
- **CORS 403** – `CORS_ORIGINS` und Frontend-URL prüfen.
- **Falsche Gateway-URL** – Setting im Frontend kontrollieren.
- **Healthz ok, aber Proxies 502** – Ziel-Services (`8611/8612/8613`) prüfen.

## Graph-Views / Postgres Robustheit

Graph-Views initialisiert den Postgres Connection-Pool asynchron im Hintergrund. Die Anwendung startet auch, wenn die Datenbank noch nicht bereit ist. Der Endpunkt `/readyz` liefert solange `503` mit `status="fail"`, bis `SELECT 1` erfolgreich ausgeführt werden konnte.

### ENV

| Variable | Default | Beschreibung |
| --- | --- | --- |
| `GV_DATABASE_URL` | – | vollständige DSN; überschreibt Einzelwerte |
| `GV_PG_HOST` | `127.0.0.1` | Postgres Host |
| `GV_PG_PORT` | `5432` | Postgres Port |
| `GV_PG_USER` | `it_user` | Benutzer |
| `GV_PG_PASSWORD` | `it_pass` | Passwort |
| `GV_PG_DB` | `it_graph` | Datenbankname |
| `GV_PG_CONNECT_TIMEOUT_S` | `1.0` | Connect-Timeout pro Versuch |
| `GV_PG_INIT_MAX_RETRIES` | `-1` | max. Versuche (`-1` = unendlich) |
| `GV_PG_INIT_BACKOFF_BASE_MS` | `200` | Start-Backoff in ms |
| `GV_PG_INIT_BACKOFF_MAX_MS` | `2000` | Obergrenze Backoff in ms |
| `GV_PG_QUERY_TIMEOUT_S` | `0.8` | Timeout für `SELECT 1` in `/readyz` |
| `GV_PG_POOL_MIN_SIZE` | `1` | Pool-Minimum |
| `GV_PG_POOL_MAX_SIZE` | `5` | Pool-Maximum |

### Retry/Backoff Logs
```
graph-views.db WARNING pg pool init failed: ConnectionRefusedError
graph-views.db INFO retrying pg pool in 200ms
graph-views.db INFO pg pool ready
```

### Troubleshooting
- falsche Credentials oder Host → `pool_unavailable`
- Firewall blockiert Port → Pool baut sich nicht auf
- Backoff zu klein → mehrfacher Verbindungsaufbau belastet DB
- `GV_PG_QUERY_TIMEOUT_S` zu klein → Readiness schlägt mit `timeout` fehl
