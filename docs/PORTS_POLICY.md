Host Port Policy (Dev)
----------------------

- Do not expose standard database/search ports on the host in dev:
  - OpenSearch 9200 → not exposed; access via `docker compose exec opensearch curl http://localhost:9200/...`
  - Postgres 5432 → not exposed; access via `docker compose exec postgres psql -U it_user -d it_graph`
- Application ports use the 861x/864x range:
  - search-api 8611, graph-api 8612, doc-entities 8613, ops-controller 8614, verification 8617, plugin-runner 8621
  - superset 8644, airflow 8642, aleph 8641, keycloak 8643, frontend 3411
- Observability: 3412–3416 (Prometheus, Grafana, Alertmanager, Loki, Tempo)

If you need host access to PG/OpenSearch temporarily, either:
- use the verification compose overlay which exposes them explicitly; or
- run `scripts/dev_install.sh EXPORT_HOST_PORTS=1` (temporary local containers only).
