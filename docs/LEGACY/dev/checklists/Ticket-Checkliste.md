

> **Legacy Notice (v0.1)**  
> This document describes pre-v0.2 behavior and is kept for historical reference.  
> See the updated docs in `docs/` and the v0.2 roadmap for current guidance.

# 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2)

> Checkliste aller Tickets / Features für den Weg von v0.1.9.1 bis v0.2  
> Inspiriert von Palantir Gotham, erweitert durch eigene Differenzierungsfeatures.

---

## 1. Core APIs (FastAPI Services)
- [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints
- [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail)
- [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services
- [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration
- [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID)

## 2. Graph-API (Neo4j)
- [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties)
- [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra)
- [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff)
- [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON)
- [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics

## 3. Search-API (OpenSearch)
- [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization)
- [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert)
- [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“
- [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index
- [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus

## 4. Graph-Views (Postgres)
- [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency)
- [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres)
- [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views)
- [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors)

## 5. Frontend (Next.js)
- [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren)
- [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler
- [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse
- [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre)
- [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar
- [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD)
- [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT)
- [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User)

## 6. Gateway & OPA
- [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation)
- [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern
- [ ] **[GATE-3]** Attribute-Level Security vorbereiten
- [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten

## 7. NiFi Pipelines
- [ ] **[NIFI-1]** RSS/Atom Ingest Flow
- [ ] **[NIFI-2]** API Ingest Flow
- [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP)
- [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR)
- [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference)
- [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon)

## 8. n8n Playbooks
- [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries)
- [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email)
- [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins)
- [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot)
- [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph)

## 9. CLI (infoterminal-cli)
- [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs)
- [ ] **[CLI-2]** Export Command (`it export [graph|search|dossier]`)
- [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`)
- [ ] **[CLI-4]** Auth Command (`it login --oidc`)
- [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table)

## 10. Infra & Observability
- [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager)
- [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID)
- [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch)
- [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren
- [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen

---

### 📌 Hinweis
- **Prio Muss**: Ontologie-Layer, Graph-Algorithmen, NLP v1, OAuth2, Observability Profile, Dossier-Lite  
- **Prio Soll**: Geospatial-Layer, NiFi Pipelines, Export/Offboarding  
- **Prio Kann**: Video-Pipeline Demo, Collaboration Features

---

<!-- merged:20250913-101006 -->
