# 🚀 InfoTerminal Release TODO – v0.1.0

Ziel: Erste veröffentlichbare Version (MVP), die Datenintegration, Suche, Graph und Dokumente in einem funktionierenden Stack zeigt.

---

## 1. Microservices

### ✅ Bereits vorhanden
- [x] `search-api` (OpenSearch angebunden, Basis-Endpunkte)
- [x] `graph-api` (Neo4j angebunden, Basis-Endpunkte)
- [x] `doc-entities` (NER/Annotation vorbereitet, HTML-Render)
- [x] `nlp-service` (NER + Summarizer)

### 🟡 To-Do
- [ ] **doc-entities erweitern**
  - [x] Verbindung zu NLP-Service
  - [ ] Rückgabe von Entitäten + Kontext im JSON

---

## 2. Datenintegration (ETL)

- [ ] NiFi Flow vorbereiten:
  - [ ] `ListenFile` → OCR (Tesseract) → `PutAleph`
  - [x] Beispiel-Template `docs/dev/nifi-ingest-demo.xml`
- [x] Airflow DAG:
  - [x] Mini-Beispiel (z. B. täglicher CSV-Import in Postgres)
- [ ] dbt Modelle:
  - [x] 1 Beispiel-Transformation (CSV → Postgres Table)
- [ ] Demo-Daten Seeds
  - [x] Graph (services/graph-api/scripts/seed_graph.py)
  - [ ] PDFs/CSV (scripts/seed_demo.sh)

---

## 3. Frontend (Next.js)

- [ ] Suche-UI finalisieren (Query + Filter)
- [ ] Graph-Viewer polieren (Neighbors, Shortest Path)
- [ ] Dokumenten-Viewer:
  - [ ] PDF-Upload → OCR/NLP → Anzeige von Entitäten
- [ ] Healthcheck-Widget (Services grün/rot)
- [ ] Superset-Dashboard-Link integrieren

---

## 4. Visualisierung

- [ ] Superset:
  - [ ] Beispiel-Dashboard (Entity Counts, Dokumente pro Kategorie)
  - [ ] OIDC-Login aktivieren (Keycloak)
  - [ ] dbt Dataset Sync (`infra/analytics/superset_dbt_sync.py`)
- [ ] Grafana:
  - [ ] Mini-Dashboard (API Latency, Request Count)

---

## 5. Deployment

- [ ] **Docker Compose**
  - [ ] Alle Services (OpenSearch, Neo4j, Postgres, Aleph, Superset, Airflow, NiFi, Search-API, Graph-API, NLP-Service, Web)
  - [ ] `.env.example` mit Standardwerten
  - [ ] Make-Targets (`make dev-up`, `make dev-down`)

- [ ] **Helm Chart (minimal)**
  - [ ] Deployments für `search-api`, `graph-api`, `web`
  - [ ] Values für externe DBs
  - [ ] Doku für Erweiterung (Aleph, Superset, …)

- [ ] **Native (Kali/Debian)**
  - [ ] systemd-Units für `search-api` & `graph-api`
  - [ ] Pyproject/uv-ready Packaging

---

## 6. Security & Governance (Dev-Modus)

- [ ] Keycloak Realm + Clients für InfoTerminal
  - [ ] Automatisierter Import via `infra/auth/keycloak_import.sh`
- [x] OPA ForwardAuth Beispiel-Policy
- [ ] Basic Audit-Log für Plugin-Runs

---

## 7. Observability

- [ ] Otel Collector + Prometheus + Grafana + Loki scaffold
- [ ] /metrics Endpunkte der Services prüfen

---

## 8. Doku

- [ ] **Quickstart (Compose)**
  - [ ] Install prerequisites
  - [ ] `make dev-up`
  - [ ] Demo-Daten importieren
  - [ ] Erste Suche + Graph + Dashboard

- [ ] **Quickstart (Helm)**
  - [ ] Install Helm Chart
  - [ ] Basic values.yaml
  - [ ] Demo-Endpunkte aufrufen

- [ ] **API Examples**
  - [ ] `curl`/`httpie` für Suche
  - [ ] `curl` Graph neighbors
  - [ ] NLP-Service Test

- [ ] **Demo-Dataset**
  - [ ] 10 PDFs (Dummy Reports)
  - [ ] CSV mit Personen/Orgs
  - [ ] Screenshots für README

---

## 9. Release Management

- [ ] Version `v0.1.0` taggen
- [ ] GitHub Release mit:
  - [ ] Compose-Bundle
  - [ ] Helm Chart
  - [ ] Demo-Dataset
  - [ ] Screenshots
- [ ] README finalisieren (Badges, Install-Matrix, Screenshots)
- [ ] Lizenz & Contributing Guide prüfen

---

## 🎯 Definition of Done (v0.1.0)

- Stack startet mit **1 Befehl** (`make dev-up`)  
- Demo-Daten können geladen werden (PDFs, CSV)  
- Suche funktioniert (Treffer aus Demo-Daten sichtbar)  
- Graph funktioniert (Beziehungen sichtbar)  
- Dokumenten-Viewer zeigt OCR + NER-Highlights  
- Dashboard zeigt erste KPIs  
- README enthält **Quickstart + Screenshots**  
- Version ist als **Docker Compose + Helm Chart** installierbar  

---
