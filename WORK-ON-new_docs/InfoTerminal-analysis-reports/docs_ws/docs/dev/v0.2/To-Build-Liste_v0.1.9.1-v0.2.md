# 📌 To-Build-Liste InfoTerminal v0.1.9.1 → v0.2

## 1. Core & APIs

* [ ] **REST-API konsolidieren**

  * Alle Services (search-api, graph-api, graph-views, gateway) standardisieren auf:

    * `/healthz` (liveness), `/readyz` (readiness)
    * Konsistente Error-Schemas (JSON-Problem-Detail).
  * Swagger/OpenAPI prüfen und für alle Services verfügbar machen.
* [ ] **OAuth2 / OIDC** (Basis-Auth)

  * JWT-Auth im Gateway implementieren.
  * Option für OIDC-Provider (Keycloak/ORY/DEX).
  * Vorbereitung für Attribute-Level-ACLs (Langfristziel: Gotham-Niveau).

## 2. Graph & Ontologie

* [ ] **Ontologie-Layer**

  * Basis-Ontologie definieren (Entities, Events, Relations, Properties).
  * Import/Export als JSON-Schema oder GraphML.
  * UI-Integration im Frontend (/graphx).
* [ ] **Graph-Algorithmen v1**

  * Centrality (Degree, Betweenness).
  * Community Detection (Louvain).
  * Path-Finding (Dijkstra, BFS).
  * Erste KPIs über Superset/Grafana-Dashboards.

## 3. Search & NLP

* [ ] **NLP Service v1**

  * Named Entity Recognition (NER).
  * Relation Extraction (Person ↔ Organisation ↔ Ort).
  * Summarization (kurze Text-Zusammenfassung).
  * Embedding Reranking (optional Feature-Flag).
* [ ] **NiFi Ingest Pipelines**

  * File ingest (CSV, PDF → Aleph).
  * API ingest (REST/JSON).
  * Streaming ingest (Kafka).
* [ ] **n8n Playbooks**

  * Automatisierte Case-Flows (z. B. Upload → Ingest → NER → Graph-Link).

## 4. Frontend

* [ ] **/search**

  * SSR-safe Inputs, unify theming.
  * Facettenfilter + Ranking-Kontrolle.
* [ ] **/graphx**

  * Visualisierung Ontologie + Graph-Algorithmen.
  * Cross-links zu Search Results.
* [ ] **/settings**

  * Endpoints editable; Auth/SSO settings sichtbar.
* [ ] **Dossier-Lite (Gap zu Gotham)**

  * Erste Reports/Notes aus Graph-/Search-Ergebnissen erstellen.
  * Download als PDF/Markdown.
  * Superset-Deep-Links integrieren.

## 5. Observability & Ops

* [ ] **Observability Profile**

  * Prometheus, Grafana, Loki, Tempo, Alertmanager auf Ports 3412–3416.
  * Structured JSON Logs mit X-Request-Id.
* [ ] **Backups**

  * Neo4j/Postgres/OpenSearch Snapshots automatisieren.
  * Scripts + Docs (lokal & S3/GCS).
* [ ] **CI/CD Stabilisierung**

  * Coverage Gate fixen.
  * Frontend Build: Settings-Page Konflikt lösen.
  * Tests für OAuth2-Flow.

## 6. Gotham-Gap Features (neu ergänzt)

* [ ] **Geospatial-Layer (Gap)**

  * Leaflet.js/MapLibre Integration in Frontend (/graphx).
  * Ingest von GeoJSON/OSM-Daten.
  * Queries: Entities mit Location + Bewegungspfad.
* [ ] **Audit/Compliance (Gap)**

  * Immutable Audit-Logs (z. B. über Loki/Tempo persistiert).
  * User-Action-Tracking im Frontend.
* [ ] **Collaboration (Gap)**

  * Basis: Multi-User Notizen (linked to Dossiers).
  * Future: Echtzeit-Kollaboration (CRDT/ShareDB).
* [ ] **Video-Pipeline (Gap, optional)**

  * NiFi → FFmpeg → ML-Inference (nur als Tech-Demo).
  * Kein Core-Feature, aber Proof-of-Concept möglich.
* [ ] **Export/Offboarding (Gap)**

  * Alle Daten/Reports exportierbar (JSON, CSV, GraphML, PDF).
  * CLI (`infoterminal-cli export …`) für reproducible exports.

---

## 🎯 Priorisierung v0.1.9.1 → v0.2

* **Muss**: Ontologie-Layer, Graph-Algorithmen v1, NLP v1, OAuth2, Observability Profile, Dossier-Lite.
* **Soll**: Geospatial-Layer, NiFi Pipelines, Export/Offboarding.
* **Kann**: Video-Pipeline Demo, Collaboration Features.
