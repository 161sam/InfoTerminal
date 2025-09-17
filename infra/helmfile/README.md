Helmfile Notes and Port Policy
------------------------------

- Cluster services (OpenSearch, Postgres) expose standard ports inside the cluster.
- Do not expose these as host ports on developer machines.
- For ad‑hoc access, use `kubectl port-forward` or `kubectl exec`.

Examples
--------

- OpenSearch health:
  - `kubectl exec -it svc/opensearch -- curl -fsS localhost:9200/_cluster/health`

- Postgres psql:
  - `kubectl exec -it deploy/postgresql -- psql -U it_user -d it_graph`

When exposing UIs (Superset, Airflow, Keycloak):
- Map to non-standard host ports (e.g., Superset 8644, Airflow 8642, Keycloak 8643) via Ingress or port‑forward.
- Follow docs/PORTS_POLICY.md for host port assignments.
