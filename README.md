# InfoTerminal — Open, Modular Intelligence Platform

## Quickstart (Dev • Kind + Helm)
```bash
make dev-up         # Kind-Cluster + Helm-Releases (PG, MinIO, OpenSearch, Keycloak, Traefik, Superset)
make seed-demo      # Demo-Index + Demo-User anlegen
make auth-up        # Keycloak realm import
make neo4j-up       # falls noch nicht durch dev-up angeworfen
make seed-graph     # Demo-Graph in Neo4j

make apps-up        # Startet Search-API, Graph-API, ER-Service & Frontend
```

## Start-Sequenz (kompakt)

```bash
make dev-up         # Helm + OPA + Neo4j
make seed-demo      # Demo-Index in OpenSearch
make auth-up        # Keycloak realm import
make neo4j-up       # (optional) Neo4j Manifeste
make seed-graph     # Demo-Graph
make apps-up        # Search-API + Graph-API + ER-Service + Frontend
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
* Superset → [http://localhost:8088](http://localhost:8088)
* Neo4j Browser → [http://localhost:7474](http://localhost:7474)

**Services (Dev Endpoints)**

```
Frontend:        http://localhost:3000
Search-API:      http://127.0.0.1:8001/healthz
Graph-API:       http://127.0.0.1:8002/healthz
ER-Service:      http://127.0.0.1:8003/docs
Keycloak:        http://localhost:8081
Superset:        http://localhost:8088
Neo4j Browser:   http://localhost:7474
```

**Beispielaufrufe**

```bash
curl 'http://127.0.0.1:8002/neighbors?node_id=P:alice'
curl -X POST 'http://127.0.0.1:8003/match' -H 'content-type: application/json' \
  -d '{"query":"ACME Incorporated","candidates":["ACME Inc.","Globex","Acme, Inc."],"limit":3}'
```

**Ordner**

* `infra/` Kubernetes, Helmfile, Kind
* `services/` Microservices (FastAPI, ETL-Utils, OpenBB-Connector)
* `apps/` Frontend (Next.js) & Agents
* `etl/` Airflow DAGs, dbt, Schemas
* `docs/` ADRs, Runbooks, Governance


## Extras: Airflow & OPA Gateway

```bash
kubectl apply -f infra/k8s/airflow/dags-configmap.yaml
make dev-up   # helmfile deployt jetzt auch Airflow
kubectl apply -f infra/k8s/opa/authz-proxy.yaml
kubectl apply -f infra/k8s/traefik/middleware-authz.yaml
kubectl apply -f infra/k8s/apis/search-api.yaml
cd apps/frontend && pnpm i && pnpm dev
```

**UIs**

* Facetten: http://localhost:3000
* Graph:    http://localhost:3000/graph
* Airflow:  http://localhost:8084
* OPA-Test: http://search.127.0.0.1.nip.io/search?q=info
