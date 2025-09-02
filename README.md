# InfoTerminal — Open, Modular Intelligence Platform

## Quickstart (Dev • Kind + Helm)
```bash
make dev-up         # Kind-Cluster + Helm-Releases (PG, MinIO, OpenSearch, Keycloak, Traefik)
make seed-demo      # Demo-Index + Demo-User anlegen
make apps-up        # Startet Search-API (FastAPI) & Frontend (Next.js) lokal mit OIDC
```

## Start-Sequenz (kompakt)

```bash
make dev-up         # Helm + OPA + Neo4j
make seed-demo      # Demo-Index in OpenSearch
make auth-up        # Keycloak realm import
make apps-up        # Search-API + Frontend
```

**Optional**: Auth wirklich erzwingen

```bash
# in services/search-api/dev.sh
export REQUIRE_AUTH=1
uvicorn app:app --host 127.0.0.1 --port 8001 --reload
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

