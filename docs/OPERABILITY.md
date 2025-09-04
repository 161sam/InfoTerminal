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

## Environment Flags
- `IT_FORCE_READY`: when set to `1`, `/readyz` skips external checks and reports ready.
- `OPENSEARCH_URL`: if set, `/readyz` probes OpenSearch with a short timeout. When unset, the check is marked `skipped`.

## Troubleshooting
- Ensure the Neo4j development password has at least 8 characters.
- Restrict CORS in development to `http://localhost:3411`.
- Disable OTEL exporters in development unless needed.
