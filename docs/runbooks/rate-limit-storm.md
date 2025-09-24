# Runbook: Rate Limit Storm

## Summary
A rate limit storm occurs when inbound traffic or internal retries overwhelm the gateway or downstream APIs, triggering 429/503 responses. The synthetic smoke checks remain green for unaffected services but latency and error panels spike for the throttled component.

## Detection
- Grafana **API SLO** dashboard shows latency spikes and `429` error buckets.
- Gateway metrics (`gateway_rate_limit_dropped_total`, `gateway_request_duration_seconds`) surge.
- Synthetic Uptime panels may stay green but request rate drops sharply; verify with `API Request Rate` chart.
- Loki logs contain `rate_limit_exceeded` events or explicit warnings from `services/gateway`.

## Immediate Actions
1. Identify the source of traffic: check gateway access logs (`kubectl logs deploy/gateway --tail 200`) for IP/user spikes.
2. If synthetic smoke remains green but customer traffic fails, enable feature flag `GATEWAY_MAINTENANCE_MODE=1` to shed load temporarily.
3. Increase burst limits cautiously:
   - Update gateway config map or `.env` (`IT_RATE_LIMIT_*`) and redeploy.
   - For FastAPI services, adjust `MAX_CONCURRENT_REQUESTS` and restart.
4. Coordinate with upstream clients to reduce request volume or add jitter/backoff.
5. Verify dependent services (search-api, graph-api, doc-entities) are healthy; rate limiting may hide latent failures.

## Stabilisation Steps
- Deploy cache or CDN layer if repeated queries cause the storm.
- Add circuit breakers / bulkheads in client SDKs.
- Extend synthetic smoke coverage with stress probes to reproduce issue in staging.
- Document safe operating limits in `docs/dev/performance.md`.

## Escalation & Communication
- Notify stakeholders about throttling, expected recovery timeline, and temporary mitigations.
- Engage platform engineering to review autoscaling and gateway policies.
- Capture metrics snapshots (Grafana, Prometheus queries) for the incident report.

## Postmortem Checklist
- Review rate limit policies and update thresholds based on observed traffic.
- Automate anomaly detection for `gateway_rate_limit_dropped_total`.
- Ensure clients implement exponential backoff and respect `Retry-After` headers.
