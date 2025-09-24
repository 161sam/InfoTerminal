# Runbook: Database Down / Degraded

## Summary
Core APIs depend on Postgres, Neo4j, and OpenSearch. When one of these data stores becomes unavailable the synthetic smoke checks turn red and readiness probes flip to `fail`. This runbook provides triage guidance for restoring service availability.

## Detection
- Grafana **Synthetic Uptime** row highlights which API is failing.
- `probe_success{service="graph-api"|"search-api"|"doc-entities"}` drops to `0` in Prometheus.
- Application `/readyz` responses show dependency checks with `status="fail"` and an error message indicating the database connection issue.
- Loki logs show repeated connection errors (e.g. `ECONNREFUSED`, `connection reset`).

## Immediate Actions
1. Identify the failing datastore from the `/readyz` payload or service logs.
2. Verify container / pod health:
   - Docker Compose: `docker compose ps <database>` and `docker compose logs <database>`.
   - Kubernetes: `kubectl get pods -l app=<database>` and `kubectl logs statefulset/<database>`.
3. Ensure storage volumes are mounted and not exhausted (`df -h`, `kubectl describe pvc`).
4. Restart the datastore component:
   - Docker: `docker compose restart <database>`.
   - Kubernetes: `kubectl rollout restart statefulset/<database>`.
5. For Postgres: run `psql -c 'SELECT 1'` using credentials from secrets. For Neo4j: `cypher-shell "RETURN 1"`. For OpenSearch: `curl -sf http://opensearch:9200/_cluster/health`.

## Stabilisation Steps
- Restore from the latest backup (`scripts/restore_postgres.sh`, `scripts/restore_neo4j.sh`, `scripts/restore_opensearch.sh`) if data corruption is detected.
- Scale dependent services down to reduce load until the database cluster is stable.
- Enable maintenance mode (feature flags or gateway rate limits) to shed traffic.
- Verify replication/cluster status (OpenSearch cluster health, Neo4j causal clustering, Postgres streaming replication if configured).

## Escalation & Communication
- Engage the data infrastructure on-call to support recovery.
- Communicate status updates every 15 minutes in the incident channel referencing dashboard screenshots.
- If failover is required, document the manual steps and update infrastructure-as-code once the incident is resolved.

## Postmortem Checklist
- Capture the root cause (hardware failure, configuration drift, long-running query) and mitigation.
- Automate detection if the issue was not caught by existing alerts.
- Update backup/restore documentation with any missing steps.
