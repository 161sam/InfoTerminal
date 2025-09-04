# Operability

## Dev Ports
- Frontend: 3411
- search-api: 8401
- graph-api: 8402
- graph-views: 8403
- agents: 3417
- gateway: 8610

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

## Troubleshooting
- Ensure the Neo4j development password has at least 8 characters.
- Restrict CORS in development to `http://localhost:3411`.
- Disable OTEL exporters in development unless needed.
