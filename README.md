# InfoTerminal — Open, Modular Intelligence Platform

## Quickstart (Dev • Kind + Helm)
```bash
make dev-up         # Kind-Cluster + Helm-Releases (PG, MinIO, OpenSearch, Keycloak, Traefik)
make seed-demo      # Demo-Index + Demo-User anlegen
make apps-up        # Startet Search-API (FastAPI) & Frontend (Next.js) lokal mit OIDC
```

**Services (Dev)**

* Auth: Keycloak (OIDC) → [http://localhost:8081](http://localhost:8081)
* Gateway: Traefik Ingress → [http://localhost](http://localhost)
* OpenSearch (Elasticsearch API) → [http://localhost:9200](http://localhost:9200)
* PostgreSQL → localhost:5432
* MinIO (S3) → [http://localhost:9000](http://localhost:9000)

**Ordner**

* `infra/` Kubernetes, Helmfile, Kind
* `services/` Microservices (FastAPI, ETL-Utils, OpenBB-Connector)
* `apps/` Frontend (Next.js) & Agents
* `etl/` Airflow DAGs, dbt, Schemas
* `docs/` ADRs, Runbooks, Governance

