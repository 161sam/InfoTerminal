# Runbook: HTTP 5xx Burst

## Summary
A sudden spike in HTTP 5xx responses indicates that one or more upstream services are failing to process requests. The synthetic smoke checks and API SLO dashboards surface these bursts within minutes. This runbook triages the failure, isolates the faulty component, and documents stabilisation actions.

## Detection
- Grafana dashboards: **API SLO** (`probe_success` and error-rate panels) and **Synthetic Uptime** row in `infoterminal-overview`.
- Prometheus alerts: `HighErrorRate` and `SLOFastBurn` rules in `monitoring/alerts/performance-alerts.yml`.
- Synthetic smoke CI gate (`python scripts/synthetic_smoke.py`) failing on the corresponding service.

## Immediate Actions
1. Confirm the scope via Grafana – identify which service/endpoint panel shows the error burst.
2. Inspect synthetic smoke logs (`kubectl logs deploy/blackbox-exporter` or `docker compose logs blackbox-exporter`) for timeouts or HTTP 5xx codes.
3. Check service health:
   - `curl -sf http://gateway:8080/readyz`
   - `curl -sf http://search-api:8080/readyz`
   - `curl -sf http://graph-api:8080/readyz`
   - `curl -sf http://doc-entities:8000/readyz`
4. Review application logs in Loki (`{service="<name>", level="error"}`) or local stdout for stack traces.
5. If the gateway is failing, disable optional feature flags (`IT_FEATURE_*`) and redeploy with last known good image.

## Stabilisation Steps
- Roll back the last deployment (`kubectl rollout undo deployment/<service>` or `docker compose restart <service>`).
- Scale the affected deployment horizontally to relieve backpressure.
- Clear transient queues/caches if error payloads mention timeouts or upstream saturation.
- Coordinate with database runbook (`db-down.md`) if backend connectivity errors appear.

## Escalation & Communication
- Notify the observability channel with impacted services, time window, and mitigation plan.
- Create an incident entry referencing Grafana panel screenshots and relevant Loki queries.
- When resolved, update post-incident notes in `docs/reports/incident-log.md` (if missing, create entry).

## Postmortem Checklist
- Add regression tests or synthetic probes covering the failing endpoint.
- Ensure dashboards and alerts include the new failure mode.
- Document remediation in `CHANGELOG.md` or service-specific docs.
