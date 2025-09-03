# 🚀 InfoTerminal Release TODO – v0.1.0

Alle Punkte sind abgeschlossen und bilden das MVP.

## 1. Microservices
- `search-api`, `graph-api`, `doc-entities`, `nlp-service` funktionsfähig
- `doc-entities` liefert Entitäten inkl. Kontext

## 2. Datenintegration (ETL)
- NiFi Flow "ingest-demo" (ListenFile→Tesseract→PutAleph)
- Airflow DAG Beispiel
- dbt Beispielmodell
- Demo Seeds (`scripts/seed_demo.sh`, `services/graph-api/scripts/seed_graph.py`)

## 3. Frontend (Next.js)
- Suche-UI mit Query & Filter
- Graph-Viewer mit Expand/Pin
- Dokumenten-Viewer mit Upload & NER-Highlights
- Healthcheck-Widget und Superset-Link

## 4. Visualisierung
- Superset Beispiel-Dashboard & OIDC
- dbt Dataset Sync (`infra/analytics/superset_dbt_sync.py`)
- Grafana Dashboard für API-Metriken

## 5. Deployment
- Docker Compose mit allen Services (`make dev-up`)
- `.env.example`
- Make Targets `dev-up` / `dev-down`
- Helm Chart (search-api, graph-api, web)
- systemd Units vorhanden

## 6. Security & Governance
- Keycloak Realm & Clients
- OPA ForwardAuth Policies
- Audit-Log für Plugin-Runs

## 7. Observability
- Otel Collector + Prometheus + Grafana + Loki scaffold
- /metrics Endpunkte geprüft

## 8. Doku
- Quickstart (Compose & Helm)
- API Examples für Suche, Graph, NLP
- Demo Dataset (PDFs + CSVs) inkl. Screenshots

## 9. Release Management
- Version `v0.1.0` getaggt
- GitHub Release (Compose-Bundle, Helm Chart, Demo-Dataset, Screenshots)
- README finalisiert
- Lizenz & Contributing Guide geprüft

## 🎯 Definition of Done (v0.1.0)
Stack startet mit einem Befehl, Demo-Daten können geladen werden, Suche & Graph funktionieren,
Dokumenten-Viewer zeigt NER-Highlights, Dashboard liefert KPIs, README enthält Quickstart,
Installation via Docker Compose und Helm möglich.
