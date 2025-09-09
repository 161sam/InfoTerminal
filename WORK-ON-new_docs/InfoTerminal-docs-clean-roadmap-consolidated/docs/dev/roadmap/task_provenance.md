# Provenance – Importierte Tasks

| Status | Task | Quelle | Zeile |
|---|---|---|---|
| open | Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). | `release-checklist-v0.1.md` | 10 |
| open | **Conftest/OPA Policies** laufen sauber (`make ci-policy`). | `release-checklist-v0.1.md` | 11 |
| open | **Secrets entfernt** aus Manifests/Code (`grep -R "password" infra/ services/ \| grep -v example` → leer). | `release-checklist-v0.1.md` | 12 |
| open | **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. | `release-checklist-v0.1.md` | 13 |
| open | **Ingress TLS** aktiv (cert-manager, staging Issuer OK). | `release-checklist-v0.1.md` | 14 |
| open | Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). | `release-checklist-v0.1.md` | 15 |
| open | **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). | `release-checklist-v0.1.md` | 21 |
| open | **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). | `release-checklist-v0.1.md` | 22 |
| open | **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. | `release-checklist-v0.1.md` | 23 |
| open | **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. | `release-checklist-v0.1.md` | 24 |
| open | **Dependabot** aktiviert (pip, npm, GitHub Actions). | `release-checklist-v0.1.md` | 25 |
| open | **Trivy Scan** ohne kritische Findings. | `release-checklist-v0.1.md` | 26 |
| open | **dbt build/test** grün (Seeds, Models, Tests). | `release-checklist-v0.1.md` | 32 |
| open | **dbt docs generate** erzeugt Artefakt (Docs erreichbar). | `release-checklist-v0.1.md` | 33 |
| open | **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). | `release-checklist-v0.1.md` | 34 |
| open | **Exposures** definiert (Superset Dashboards verlinkt). | `release-checklist-v0.1.md` | 35 |
| open | **Freshness Checks** für Sources ohne Errors. | `release-checklist-v0.1.md` | 36 |
| open | **Superset Dashboard** „analytics_prices“ importiert: | `release-checklist-v0.1.md` | 42 |
| open | **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. | `release-checklist-v0.1.md` | 45 |
| open | Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). | `release-checklist-v0.1.md` | 46 |
| open | **Vitest/Playwright Tests** decken Detailseiten ab. | `release-checklist-v0.1.md` | 47 |
| open | **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. | `release-checklist-v0.1.md` | 53 |
| open | **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. | `release-checklist-v0.1.md` | 54 |
| open | **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). | `release-checklist-v0.1.md` | 55 |
| open | Restore-Runbook einmal **trocken getestet**. | `release-checklist-v0.1.md` | 56 |
| open | **OTel Collector** deployed (4317/4318/9464 erreichbar). | `release-checklist-v0.1.md` | 62 |
| open | **Python Services** exportieren Traces + `/metrics`. | `release-checklist-v0.1.md` | 63 |
| open | **Node Services** exportieren Traces + `/metrics`. | `release-checklist-v0.1.md` | 64 |
| open | **Prometheus** scrapt Services; Grafana Panels gefüllt. | `release-checklist-v0.1.md` | 65 |
| open | **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). | `release-checklist-v0.1.md` | 66 |
| open | **Loki** enthält Logs aller Services (Promtail shipping OK). | `release-checklist-v0.1.md` | 67 |
| open | **Grafana Dashboards**: | `release-checklist-v0.1.md` | 68 |
| open | **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). | `release-checklist-v0.1.md` | 76 |
| open | **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. | `release-checklist-v0.1.md` | 77 |
| open | **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. | `release-checklist-v0.1.md` | 78 |
| open | **Language Policy**: Docs in EN, DE als Appendix. | `release-checklist-v0.1.md` | 79 |
| open | **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. | `release-checklist-v0.1.md` | 80 |
| open | **CI Docs-Checks** grün (markdownlint, link check, doctoc). | `release-checklist-v0.1.md` | 81 |
| open | **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. | `release-checklist-v0.1.md` | 87 |
| open | **Ingress Hosts** & TLS validiert. | `release-checklist-v0.1.md` | 88 |
| open | **Demo-Data Seed** erfolgreich (`make seed-demo`). | `release-checklist-v0.1.md` | 89 |
| open | **Smoke-Test** im Staging: | `release-checklist-v0.1.md` | 90 |
| open | `main` eingefroren, `release/v0.1` Branch erstellt. | `release-checklist-v0.1.md` | 103 |
| open | **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). | `release-checklist-v0.1.md` | 104 |
| open | **Release Notes** erstellt (Features, Breaking Changes, Known Issues). | `release-checklist-v0.1.md` | 105 |
| open | **Tag v0.1.0** gesetzt und Release publiziert. | `release-checklist-v0.1.md` | 106 |
| open | Dokumentation zur Installation/Exploration angehängt. | `release-checklist-v0.1.md` | 107 |
| open | Secrets rotieren (Keycloak admin, oauth2-proxy cookie, DB-Passwörter). | `SECURITY_SWEEP.md` | 3 |
| open | TLS/Ingress für Prod (Cert-Manager). | `SECURITY_SWEEP.md` | 4 |
| open | Backups für PG/OpenSearch/Neo4j. | `SECURITY_SWEEP.md` | 5 |
| open | **Superset-Composer**: JS/Python Helper eingebaut → Link öffnet Dashboard mit Filtern | `dev/superset-nifi-flowise.md` | 184 |
| open | **NiFi→Aleph**: InvokeHTTP Multipart konfiguriert, 200/202 Rückgabe sichtbar | `dev/superset-nifi-flowise.md` | 185 |
| open | **Flowise Agent**: Tools/Schemas registriert, Guardrail-Prompt gesetzt, Tool-Limit aktiv | `dev/superset-nifi-flowise.md` | 186 |
| open | **Smoke Tests**: | `dev/superset-nifi-flowise.md` | 187 |
| open | Design System implementiert | `dev/frontend_modernization_guide.md` | 205 |
| open | Layout System eingerichtet | `dev/frontend_modernization_guide.md` | 206 |
| open | Komponenten modernisiert | `dev/frontend_modernization_guide.md` | 207 |
| open | Responsive Design getestet | `dev/frontend_modernization_guide.md` | 208 |
| open | Performance optimiert | `dev/frontend_modernization_guide.md` | 209 |
| open | Tests aktualisiert | `dev/frontend_modernization_guide.md` | 210 |
| open | Accessibility geprüft | `dev/frontend_modernization_guide.md` | 211 |
| open | Cross-Browser Tests | `dev/frontend_modernization_guide.md` | 212 |
| open | Mobile Experience validiert | `dev/frontend_modernization_guide.md` | 213 |
| open | Documentation aktualisiert | `dev/frontend_modernization_guide.md` | 214 |
| open | **Desktop Navigation** - Sidebar funktioniert | `dev/guides/frontend-modernization.md` | 304 |
| open | **Mobile Navigation** - Hamburger Menu + Bottom Tabs | `dev/guides/frontend-modernization.md` | 305 |
| open | **Dark/Light Mode** - Toggle funktioniert | `dev/guides/frontend-modernization.md` | 306 |
| open | **Command Palette** - Cmd+K öffnet Palette | `dev/guides/frontend-modernization.md` | 307 |
| open | **Search Functionality** - Faceted Search + Results | `dev/guides/frontend-modernization.md` | 308 |
| open | **Form Validation** - Error States + Success | `dev/guides/frontend-modernization.md` | 309 |
| open | **Real-time Updates** - WebSocket Connection | `dev/guides/frontend-modernization.md` | 310 |
| open | **Notifications** - Toast Messages | `dev/guides/frontend-modernization.md` | 311 |
| open | **Charts** - Interactive Visualizations | `dev/guides/frontend-modernization.md` | 312 |
| open | **Data Tables** - Sorting + Filtering + Pagination | `dev/guides/frontend-modernization.md` | 313 |
| open | **Authentication** - Login/Logout Flow | `dev/guides/frontend-modernization.md` | 314 |
| open | **Bundle Size** < 500KB gzipped | `dev/guides/frontend-modernization.md` | 338 |
| open | **First Contentful Paint** < 1.8s | `dev/guides/frontend-modernization.md` | 339 |
| open | **Largest Contentful Paint** < 2.5s | `dev/guides/frontend-modernization.md` | 340 |
| open | **Cumulative Layout Shift** < 0.1 | `dev/guides/frontend-modernization.md` | 341 |
| open | **First Input Delay** < 100ms | `dev/guides/frontend-modernization.md` | 342 |
| open | **Alle Tests bestanden** | `dev/guides/frontend-modernization.md` | 472 |
| open | **Performance Benchmarks erreicht** | `dev/guides/frontend-modernization.md` | 473 |
| open | **Mobile Testing abgeschlossen** | `dev/guides/frontend-modernization.md` | 474 |
| open | **Accessibility validiert** (WCAG 2.1) | `dev/guides/frontend-modernization.md` | 475 |
| open | **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) | `dev/guides/frontend-modernization.md` | 476 |
| open | **User Acceptance Testing** abgeschlossen | `dev/guides/frontend-modernization.md` | 477 |
| open | **Documentation aktualisiert** | `dev/guides/frontend-modernization.md` | 478 |
| open | **Deployment Pipeline getestet** | `dev/guides/frontend-modernization.md` | 479 |
| open | **Monitoring Setup** aktiv | `dev/guides/frontend-modernization.md` | 480 |
| open | **Rollback Plan** definiert | `dev/guides/frontend-modernization.md` | 481 |
| open | **Desktop Navigation** - Sidebar funktioniert | `dev/guides/frontend-modernization.md` | 781 |
| open | **Mobile Navigation** - Hamburger Menu + Bottom Tabs | `dev/guides/frontend-modernization.md` | 782 |
| open | **Dark/Light Mode** - Toggle funktioniert | `dev/guides/frontend-modernization.md` | 783 |
| open | **Command Palette** - Cmd+K öffnet Palette | `dev/guides/frontend-modernization.md` | 784 |
| open | **Search Functionality** - Faceted Search + Results | `dev/guides/frontend-modernization.md` | 785 |
| open | **Form Validation** - Error States + Success | `dev/guides/frontend-modernization.md` | 786 |
| open | **Real-time Updates** - WebSocket Connection | `dev/guides/frontend-modernization.md` | 787 |
| open | **Notifications** - Toast Messages | `dev/guides/frontend-modernization.md` | 788 |
| open | **Charts** - Interactive Visualizations | `dev/guides/frontend-modernization.md` | 789 |
| open | **Data Tables** - Sorting + Filtering + Pagination | `dev/guides/frontend-modernization.md` | 790 |
| open | **Authentication** - Login/Logout Flow | `dev/guides/frontend-modernization.md` | 791 |
| open | **Bundle Size** < 500KB gzipped | `dev/guides/frontend-modernization.md` | 815 |
| open | **First Contentful Paint** < 1.8s | `dev/guides/frontend-modernization.md` | 816 |
| open | **Largest Contentful Paint** < 2.5s | `dev/guides/frontend-modernization.md` | 817 |
| open | **Cumulative Layout Shift** < 0.1 | `dev/guides/frontend-modernization.md` | 818 |
| open | **First Input Delay** < 100ms | `dev/guides/frontend-modernization.md` | 819 |
| open | **Alle Tests bestanden** | `dev/guides/frontend-modernization.md` | 949 |
| open | **Performance Benchmarks erreicht** | `dev/guides/frontend-modernization.md` | 950 |
| open | **Mobile Testing abgeschlossen** | `dev/guides/frontend-modernization.md` | 951 |
| open | **Accessibility validiert** (WCAG 2.1) | `dev/guides/frontend-modernization.md` | 952 |
| open | **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) | `dev/guides/frontend-modernization.md` | 953 |
| open | **User Acceptance Testing** abgeschlossen | `dev/guides/frontend-modernization.md` | 954 |
| open | **Documentation aktualisiert** | `dev/guides/frontend-modernization.md` | 955 |
| open | **Deployment Pipeline getestet** | `dev/guides/frontend-modernization.md` | 956 |
| open | **Monitoring Setup** aktiv | `dev/guides/frontend-modernization.md` | 957 |
| open | **Rollback Plan** definiert | `dev/guides/frontend-modernization.md` | 958 |
| open | **REST-API konsolidieren** | `dev/roadmap/v0.2-to-build.md` | 5 |
| open | **OAuth2 / OIDC** (Basis-Auth) | `dev/roadmap/v0.2-to-build.md` | 12 |
| open | **Ontologie-Layer** | `dev/roadmap/v0.2-to-build.md` | 20 |
| open | **Graph-Algorithmen v1** | `dev/roadmap/v0.2-to-build.md` | 25 |
| open | **NLP Service v1** | `dev/roadmap/v0.2-to-build.md` | 34 |
| open | **NiFi Ingest Pipelines** | `dev/roadmap/v0.2-to-build.md` | 40 |
| open | **n8n Playbooks** | `dev/roadmap/v0.2-to-build.md` | 45 |
| open | **/search** | `dev/roadmap/v0.2-to-build.md` | 51 |
| open | **/graphx** | `dev/roadmap/v0.2-to-build.md` | 55 |
| open | **/settings** | `dev/roadmap/v0.2-to-build.md` | 59 |
| open | **Dossier-Lite (Gap zu Gotham)** | `dev/roadmap/v0.2-to-build.md` | 62 |
| open | **Observability Profile** | `dev/roadmap/v0.2-to-build.md` | 70 |
| open | **Backups** | `dev/roadmap/v0.2-to-build.md` | 74 |
| open | **CI/CD Stabilisierung** | `dev/roadmap/v0.2-to-build.md` | 78 |
| open | **Geospatial-Layer (Gap)** | `dev/roadmap/v0.2-to-build.md` | 86 |
| open | **Audit/Compliance (Gap)** | `dev/roadmap/v0.2-to-build.md` | 91 |
| open | **Collaboration (Gap)** | `dev/roadmap/v0.2-to-build.md` | 95 |
| open | **Video-Pipeline (Gap, optional)** | `dev/roadmap/v0.2-to-build.md` | 99 |
| open | **Export/Offboarding (Gap)** | `dev/roadmap/v0.2-to-build.md` | 103 |
| open | **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints | `dev/roadmap/v0.2-to-build-75fb87.md` | 9 |
| open | **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) | `dev/roadmap/v0.2-to-build-75fb87.md` | 10 |
| open | **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services | `dev/roadmap/v0.2-to-build-75fb87.md` | 11 |
| open | **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration | `dev/roadmap/v0.2-to-build-75fb87.md` | 12 |
| open | **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) | `dev/roadmap/v0.2-to-build-75fb87.md` | 13 |
| open | **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) | `dev/roadmap/v0.2-to-build-75fb87.md` | 16 |
| open | **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) | `dev/roadmap/v0.2-to-build-75fb87.md` | 17 |
| open | **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) | `dev/roadmap/v0.2-to-build-75fb87.md` | 18 |
| open | **[GRAPH-4]** Graph-Export (GraphML, JSON) | `dev/roadmap/v0.2-to-build-75fb87.md` | 19 |
| open | **[GRAPH-5]** Audit: Query-Logs + Query-Metrics | `dev/roadmap/v0.2-to-build-75fb87.md` | 20 |
| open | **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) | `dev/roadmap/v0.2-to-build-75fb87.md` | 23 |
| open | **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) | `dev/roadmap/v0.2-to-build-75fb87.md` | 24 |
| open | **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ | `dev/roadmap/v0.2-to-build-75fb87.md` | 25 |
| open | **[SEARCH-4]** Export: JSON/CSV Dumps pro Index | `dev/roadmap/v0.2-to-build-75fb87.md` | 26 |
| open | **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus | `dev/roadmap/v0.2-to-build-75fb87.md` | 27 |
| open | **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) | `dev/roadmap/v0.2-to-build-75fb87.md` | 30 |
| open | **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) | `dev/roadmap/v0.2-to-build-75fb87.md` | 31 |
| open | **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) | `dev/roadmap/v0.2-to-build-75fb87.md` | 32 |
| open | **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) | `dev/roadmap/v0.2-to-build-75fb87.md` | 33 |
| open | **[FE-1]** Einheitliches Theme (globals.css konsolidieren) | `dev/roadmap/v0.2-to-build-75fb87.md` | 36 |
| open | **[FE-2]** /search: Facettenfilter + Ranking-Regler | `dev/roadmap/v0.2-to-build-75fb87.md` | 37 |
| open | **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse | `dev/roadmap/v0.2-to-build-75fb87.md` | 38 |
| open | **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) | `dev/roadmap/v0.2-to-build-75fb87.md` | 39 |
| open | **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar | `dev/roadmap/v0.2-to-build-75fb87.md` | 40 |
| open | **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) | `dev/roadmap/v0.2-to-build-75fb87.md` | 41 |
| open | **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) | `dev/roadmap/v0.2-to-build-75fb87.md` | 42 |
| open | **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) | `dev/roadmap/v0.2-to-build-75fb87.md` | 43 |
| open | **[GATE-1]** OAuth2/OIDC Support (JWT Validation) | `dev/roadmap/v0.2-to-build-75fb87.md` | 46 |
| open | **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern | `dev/roadmap/v0.2-to-build-75fb87.md` | 47 |
| open | **[GATE-3]** Attribute-Level Security vorbereiten | `dev/roadmap/v0.2-to-build-75fb87.md` | 48 |
| open | **[GATE-4]** Audit-Logs in Loki weiterleiten | `dev/roadmap/v0.2-to-build-75fb87.md` | 49 |
| open | **[NIFI-1]** RSS/Atom Ingest Flow | `dev/roadmap/v0.2-to-build-75fb87.md` | 52 |
| open | **[NIFI-2]** API Ingest Flow | `dev/roadmap/v0.2-to-build-75fb87.md` | 53 |
| open | **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) | `dev/roadmap/v0.2-to-build-75fb87.md` | 54 |
| open | **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) | `dev/roadmap/v0.2-to-build-75fb87.md` | 55 |
| open | **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) | `dev/roadmap/v0.2-to-build-75fb87.md` | 56 |
| open | **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) | `dev/roadmap/v0.2-to-build-75fb87.md` | 57 |
| open | **[N8N-1]** Investigation Assistant Flow (search+graph queries) | `dev/roadmap/v0.2-to-build-75fb87.md` | 60 |
| open | **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) | `dev/roadmap/v0.2-to-build-75fb87.md` | 61 |
| open | **[N8N-3]** Cross-Source Correlation (news+social+plugins) | `dev/roadmap/v0.2-to-build-75fb87.md` | 62 |
| open | **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) | `dev/roadmap/v0.2-to-build-75fb87.md` | 63 |
| open | **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) | `dev/roadmap/v0.2-to-build-75fb87.md` | 64 |
| open | **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) | `dev/roadmap/v0.2-to-build-75fb87.md` | 67 |
| open | **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) | `dev/roadmap/v0.2-to-build-75fb87.md` | 68 |
| open | **[CLI-3]** Plugin Command (`it plugin run <tool>`) | `dev/roadmap/v0.2-to-build-75fb87.md` | 69 |
| open | **[CLI-4]** Auth Command (`it login --oidc`) | `dev/roadmap/v0.2-to-build-75fb87.md` | 70 |
| open | **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) | `dev/roadmap/v0.2-to-build-75fb87.md` | 71 |
| open | **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) | `dev/roadmap/v0.2-to-build-75fb87.md` | 74 |
| open | **[OBS-2]** Structured JSON Logs (X-Request-ID) | `dev/roadmap/v0.2-to-build-75fb87.md` | 75 |
| open | **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) | `dev/roadmap/v0.2-to-build-75fb87.md` | 76 |
| open | **[OBS-4]** Coverage Gate fixen + CI stabilisieren | `dev/roadmap/v0.2-to-build-75fb87.md` | 77 |
| open | **[OBS-5]** Frontend Build Konflikt (settings page) lösen | `dev/roadmap/v0.2-to-build-75fb87.md` | 78 |
| open | **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints | `dev/roadmap/v0.2-to-build-175b6f.md` | 9 |
| open | **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) | `dev/roadmap/v0.2-to-build-175b6f.md` | 10 |
| open | **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services | `dev/roadmap/v0.2-to-build-175b6f.md` | 11 |
| open | **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration | `dev/roadmap/v0.2-to-build-175b6f.md` | 12 |
| open | **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) | `dev/roadmap/v0.2-to-build-175b6f.md` | 13 |
| open | **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) | `dev/roadmap/v0.2-to-build-175b6f.md` | 16 |
| open | **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) | `dev/roadmap/v0.2-to-build-175b6f.md` | 17 |
| open | **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) | `dev/roadmap/v0.2-to-build-175b6f.md` | 18 |
| open | **[GRAPH-4]** Graph-Export (GraphML, JSON) | `dev/roadmap/v0.2-to-build-175b6f.md` | 19 |
| open | **[GRAPH-5]** Audit: Query-Logs + Query-Metrics | `dev/roadmap/v0.2-to-build-175b6f.md` | 20 |
| open | **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) | `dev/roadmap/v0.2-to-build-175b6f.md` | 23 |
| open | **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) | `dev/roadmap/v0.2-to-build-175b6f.md` | 24 |
| open | **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ | `dev/roadmap/v0.2-to-build-175b6f.md` | 25 |
| open | **[SEARCH-4]** Export: JSON/CSV Dumps pro Index | `dev/roadmap/v0.2-to-build-175b6f.md` | 26 |
| open | **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus | `dev/roadmap/v0.2-to-build-175b6f.md` | 27 |
| open | **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) | `dev/roadmap/v0.2-to-build-175b6f.md` | 30 |
| open | **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) | `dev/roadmap/v0.2-to-build-175b6f.md` | 31 |
| open | **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) | `dev/roadmap/v0.2-to-build-175b6f.md` | 32 |
| open | **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) | `dev/roadmap/v0.2-to-build-175b6f.md` | 33 |
| open | **[FE-1]** Einheitliches Theme (globals.css konsolidieren) | `dev/roadmap/v0.2-to-build-175b6f.md` | 36 |
| open | **[FE-2]** /search: Facettenfilter + Ranking-Regler | `dev/roadmap/v0.2-to-build-175b6f.md` | 37 |
| open | **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse | `dev/roadmap/v0.2-to-build-175b6f.md` | 38 |
| open | **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) | `dev/roadmap/v0.2-to-build-175b6f.md` | 39 |
| open | **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar | `dev/roadmap/v0.2-to-build-175b6f.md` | 40 |
| open | **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) | `dev/roadmap/v0.2-to-build-175b6f.md` | 41 |
| open | **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) | `dev/roadmap/v0.2-to-build-175b6f.md` | 42 |
| open | **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) | `dev/roadmap/v0.2-to-build-175b6f.md` | 43 |
| open | **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) | `dev/roadmap/v0.2-to-build-175b6f.md` | 44 |
| open | **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) | `dev/roadmap/v0.2-to-build-175b6f.md` | 45 |
| open | **[GATE-1]** OAuth2/OIDC Support (JWT Validation) | `dev/roadmap/v0.2-to-build-175b6f.md` | 48 |
| open | **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern | `dev/roadmap/v0.2-to-build-175b6f.md` | 49 |
| open | **[GATE-3]** Attribute-Level Security vorbereiten | `dev/roadmap/v0.2-to-build-175b6f.md` | 50 |
| open | **[GATE-4]** Audit-Logs in Loki weiterleiten | `dev/roadmap/v0.2-to-build-175b6f.md` | 51 |
| open | **[NIFI-1]** RSS/Atom Ingest Flow | `dev/roadmap/v0.2-to-build-175b6f.md` | 54 |
| open | **[NIFI-2]** API Ingest Flow | `dev/roadmap/v0.2-to-build-175b6f.md` | 55 |
| open | **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) | `dev/roadmap/v0.2-to-build-175b6f.md` | 56 |
| open | **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) | `dev/roadmap/v0.2-to-build-175b6f.md` | 57 |
| open | **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) | `dev/roadmap/v0.2-to-build-175b6f.md` | 58 |
| open | **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) | `dev/roadmap/v0.2-to-build-175b6f.md` | 59 |
| open | **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation | `dev/roadmap/v0.2-to-build-175b6f.md` | 60 |
| open | **[N8N-1]** Investigation Assistant Flow (search+graph queries) | `dev/roadmap/v0.2-to-build-175b6f.md` | 63 |
| open | **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) | `dev/roadmap/v0.2-to-build-175b6f.md` | 64 |
| open | **[N8N-3]** Cross-Source Correlation (news+social+plugins) | `dev/roadmap/v0.2-to-build-175b6f.md` | 65 |
| open | **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) | `dev/roadmap/v0.2-to-build-175b6f.md` | 66 |
| open | **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) | `dev/roadmap/v0.2-to-build-175b6f.md` | 67 |
| open | **[N8N-6]** Veracity Alerts (false/manipulative → escalate) | `dev/roadmap/v0.2-to-build-175b6f.md` | 68 |
| open | **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) | `dev/roadmap/v0.2-to-build-175b6f.md` | 69 |
| open | **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) | `dev/roadmap/v0.2-to-build-175b6f.md` | 72 |
| open | **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) | `dev/roadmap/v0.2-to-build-175b6f.md` | 73 |
| open | **[CLI-3]** Plugin Command (`it plugin run <tool>`) | `dev/roadmap/v0.2-to-build-175b6f.md` | 74 |
| open | **[CLI-4]** Auth Command (`it login --oidc`) | `dev/roadmap/v0.2-to-build-175b6f.md` | 75 |
| open | **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) | `dev/roadmap/v0.2-to-build-175b6f.md` | 76 |
| open | **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) | `dev/roadmap/v0.2-to-build-175b6f.md` | 79 |
| open | **[OBS-2]** Structured JSON Logs (X-Request-ID) | `dev/roadmap/v0.2-to-build-175b6f.md` | 80 |
| open | **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) | `dev/roadmap/v0.2-to-build-175b6f.md` | 81 |
| open | **[OBS-4]** Coverage Gate fixen + CI stabilisieren | `dev/roadmap/v0.2-to-build-175b6f.md` | 82 |
| open | **[OBS-5]** Frontend Build Konflikt (settings page) lösen | `dev/roadmap/v0.2-to-build-175b6f.md` | 83 |
| open | **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) | `dev/roadmap/v0.2-to-build-175b6f.md` | 88 |
| open | **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway | `dev/roadmap/v0.2-to-build-175b6f.md` | 89 |
| open | **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion | `dev/roadmap/v0.2-to-build-175b6f.md` | 90 |
| open | **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 | `dev/roadmap/v0.2-to-build-175b6f.md` | 91 |
| open | **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) | `dev/roadmap/v0.2-to-build-175b6f.md` | 92 |
| open | **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys | `dev/roadmap/v0.2-to-build-175b6f.md` | 93 |
| open | **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte | `dev/roadmap/v0.2-to-build-175b6f.md` | 94 |
| open | **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) | `dev/roadmap/v0.2-to-build-175b6f.md` | 95 |
| open | **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) | `dev/roadmap/v0.2-to-build-175b6f.md` | 96 |
| open | **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist | `dev/roadmap/v0.2-to-build-175b6f.md` | 97 |
| open | **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) | `dev/roadmap/v0.2-to-build-175b6f.md` | 98 |
| open | **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) | `dev/roadmap/v0.2-to-build-175b6f.md` | 99 |
| open | **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) | `dev/roadmap/v0.2-to-build-175b6f.md` | 100 |
| open | **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) | `dev/roadmap/v0.2-to-build-175b6f.md` | 101 |
| open | **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI | `dev/roadmap/v0.2-to-build-175b6f.md` | 102 |
| open | **[VERIF-1]** Source Reputation & Bot-Likelihood Modul | `dev/roadmap/v0.2-to-build-175b6f.md` | 107 |
| open | **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs | `dev/roadmap/v0.2-to-build-175b6f.md` | 108 |
| open | **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) | `dev/roadmap/v0.2-to-build-175b6f.md` | 109 |
| open | **[VERIF-4]** RTE/Stance Classifier + Aggregation | `dev/roadmap/v0.2-to-build-175b6f.md` | 110 |
| open | **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) | `dev/roadmap/v0.2-to-build-175b6f.md` | 111 |
| open | **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) | `dev/roadmap/v0.2-to-build-175b6f.md` | 112 |
| open | **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) | `dev/roadmap/v0.2-to-build-175b6f.md` | 113 |
| open | **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) | `dev/roadmap/v0.2-to-build-175b6f.md` | 114 |
| open | **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) | `dev/roadmap/v0.2-to-build-175b6f.md` | 115 |
| open | **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) | `dev/roadmap/v0.2-to-build-175b6f.md` | 116 |
| open | **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) | `dev/roadmap/v0.2-to-build-175b6f.md` | 117 |
| open | **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints | `dev/roadmap/v0.2-to-build-a988fb.md` | 9 |
| open | **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) | `dev/roadmap/v0.2-to-build-a988fb.md` | 10 |
| open | **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services | `dev/roadmap/v0.2-to-build-a988fb.md` | 11 |
| open | **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration | `dev/roadmap/v0.2-to-build-a988fb.md` | 12 |
| open | **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) | `dev/roadmap/v0.2-to-build-a988fb.md` | 13 |
| open | **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) | `dev/roadmap/v0.2-to-build-a988fb.md` | 16 |
| open | **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) | `dev/roadmap/v0.2-to-build-a988fb.md` | 17 |
| open | **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) | `dev/roadmap/v0.2-to-build-a988fb.md` | 18 |
| open | **[GRAPH-4]** Graph-Export (GraphML, JSON) | `dev/roadmap/v0.2-to-build-a988fb.md` | 19 |
| open | **[GRAPH-5]** Audit: Query-Logs + Query-Metrics | `dev/roadmap/v0.2-to-build-a988fb.md` | 20 |
| open | **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) | `dev/roadmap/v0.2-to-build-a988fb.md` | 23 |
| open | **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) | `dev/roadmap/v0.2-to-build-a988fb.md` | 24 |
| open | **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ | `dev/roadmap/v0.2-to-build-a988fb.md` | 25 |
| open | **[SEARCH-4]** Export: JSON/CSV Dumps pro Index | `dev/roadmap/v0.2-to-build-a988fb.md` | 26 |
| open | **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus | `dev/roadmap/v0.2-to-build-a988fb.md` | 27 |
| open | **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) | `dev/roadmap/v0.2-to-build-a988fb.md` | 30 |
| open | **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) | `dev/roadmap/v0.2-to-build-a988fb.md` | 31 |
| open | **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) | `dev/roadmap/v0.2-to-build-a988fb.md` | 32 |
| open | **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) | `dev/roadmap/v0.2-to-build-a988fb.md` | 33 |
| open | **[FE-1]** Einheitliches Theme (globals.css konsolidieren) | `dev/roadmap/v0.2-to-build-a988fb.md` | 36 |
| open | **[FE-2]** /search: Facettenfilter + Ranking-Regler | `dev/roadmap/v0.2-to-build-a988fb.md` | 37 |
| open | **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse | `dev/roadmap/v0.2-to-build-a988fb.md` | 38 |
| open | **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) | `dev/roadmap/v0.2-to-build-a988fb.md` | 39 |
| open | **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar | `dev/roadmap/v0.2-to-build-a988fb.md` | 40 |
| open | **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) | `dev/roadmap/v0.2-to-build-a988fb.md` | 41 |
| open | **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) | `dev/roadmap/v0.2-to-build-a988fb.md` | 42 |
| open | **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) | `dev/roadmap/v0.2-to-build-a988fb.md` | 43 |
| open | **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) | `dev/roadmap/v0.2-to-build-a988fb.md` | 44 |
| open | **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) | `dev/roadmap/v0.2-to-build-a988fb.md` | 45 |
| open | **[GATE-1]** OAuth2/OIDC Support (JWT Validation) | `dev/roadmap/v0.2-to-build-a988fb.md` | 48 |
| open | **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern | `dev/roadmap/v0.2-to-build-a988fb.md` | 49 |
| open | **[GATE-3]** Attribute-Level Security vorbereiten | `dev/roadmap/v0.2-to-build-a988fb.md` | 50 |
| open | **[GATE-4]** Audit-Logs in Loki weiterleiten | `dev/roadmap/v0.2-to-build-a988fb.md` | 51 |
| open | **[NIFI-1]** RSS/Atom Ingest Flow | `dev/roadmap/v0.2-to-build-a988fb.md` | 54 |
| open | **[NIFI-2]** API Ingest Flow | `dev/roadmap/v0.2-to-build-a988fb.md` | 55 |
| open | **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) | `dev/roadmap/v0.2-to-build-a988fb.md` | 56 |
| open | **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) | `dev/roadmap/v0.2-to-build-a988fb.md` | 57 |
| open | **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) | `dev/roadmap/v0.2-to-build-a988fb.md` | 58 |
| open | **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) | `dev/roadmap/v0.2-to-build-a988fb.md` | 59 |
| open | **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) | `dev/roadmap/v0.2-to-build-a988fb.md` | 60 |
| open | **[N8N-1]** Investigation Assistant Flow (search+graph queries) | `dev/roadmap/v0.2-to-build-a988fb.md` | 63 |
| open | **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) | `dev/roadmap/v0.2-to-build-a988fb.md` | 64 |
| open | **[N8N-3]** Cross-Source Correlation (news+social+plugins) | `dev/roadmap/v0.2-to-build-a988fb.md` | 65 |
| open | **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) | `dev/roadmap/v0.2-to-build-a988fb.md` | 66 |
| open | **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) | `dev/roadmap/v0.2-to-build-a988fb.md` | 67 |
| open | **[N8N-6]** Veracity Alerts (false/manipulative → escalate) | `dev/roadmap/v0.2-to-build-a988fb.md` | 68 |
| open | **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) | `dev/roadmap/v0.2-to-build-a988fb.md` | 69 |
| open | **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) | `dev/roadmap/v0.2-to-build-a988fb.md` | 72 |
| open | **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) | `dev/roadmap/v0.2-to-build-a988fb.md` | 73 |
| open | **[CLI-3]** Plugin Command (`it plugin run <tool>`) | `dev/roadmap/v0.2-to-build-a988fb.md` | 74 |
| open | **[CLI-4]** Auth Command (`it login --oidc`) | `dev/roadmap/v0.2-to-build-a988fb.md` | 75 |
| open | **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) | `dev/roadmap/v0.2-to-build-a988fb.md` | 76 |
| open | **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) | `dev/roadmap/v0.2-to-build-a988fb.md` | 79 |
| open | **[OBS-2]** Structured JSON Logs (X-Request-ID) | `dev/roadmap/v0.2-to-build-a988fb.md` | 80 |
| open | **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) | `dev/roadmap/v0.2-to-build-a988fb.md` | 81 |
| open | **[OBS-4]** Coverage Gate fixen + CI stabilisieren | `dev/roadmap/v0.2-to-build-a988fb.md` | 82 |
| open | **[OBS-5]** Frontend Build Konflikt (settings page) lösen | `dev/roadmap/v0.2-to-build-a988fb.md` | 83 |
| open | **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) | `dev/roadmap/v0.2-to-build-a988fb.md` | 88 |
| open | **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway | `dev/roadmap/v0.2-to-build-a988fb.md` | 89 |
| open | **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion | `dev/roadmap/v0.2-to-build-a988fb.md` | 90 |
| open | **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 | `dev/roadmap/v0.2-to-build-a988fb.md` | 91 |
| open | **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) | `dev/roadmap/v0.2-to-build-a988fb.md` | 92 |
| open | **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys | `dev/roadmap/v0.2-to-build-a988fb.md` | 93 |
| open | **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte | `dev/roadmap/v0.2-to-build-a988fb.md` | 94 |
| open | **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) | `dev/roadmap/v0.2-to-build-a988fb.md` | 95 |
| open | **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) | `dev/roadmap/v0.2-to-build-a988fb.md` | 96 |
| open | **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist | `dev/roadmap/v0.2-to-build-a988fb.md` | 97 |
| open | **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) | `dev/roadmap/v0.2-to-build-a988fb.md` | 98 |
| open | **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) | `dev/roadmap/v0.2-to-build-a988fb.md` | 99 |
| open | **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) | `dev/roadmap/v0.2-to-build-a988fb.md` | 100 |
| open | **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) | `dev/roadmap/v0.2-to-build-a988fb.md` | 101 |
| open | **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI | `dev/roadmap/v0.2-to-build-a988fb.md` | 102 |
| open | **[VERIF-1]** Source Reputation & Bot-Likelihood Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 105 |
| open | **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs | `dev/roadmap/v0.2-to-build-a988fb.md` | 106 |
| open | **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) | `dev/roadmap/v0.2-to-build-a988fb.md` | 107 |
| open | **[VERIF-4]** RTE/Stance Classifier + Aggregation | `dev/roadmap/v0.2-to-build-a988fb.md` | 108 |
| open | **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) | `dev/roadmap/v0.2-to-build-a988fb.md` | 109 |
| open | **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) | `dev/roadmap/v0.2-to-build-a988fb.md` | 110 |
| open | **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) | `dev/roadmap/v0.2-to-build-a988fb.md` | 111 |
| open | **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) | `dev/roadmap/v0.2-to-build-a988fb.md` | 112 |
| open | **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) | `dev/roadmap/v0.2-to-build-a988fb.md` | 113 |
| open | **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) | `dev/roadmap/v0.2-to-build-a988fb.md` | 114 |
| open | **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) | `dev/roadmap/v0.2-to-build-a988fb.md` | 115 |
| open | **[LEGAL-1]** RAG-Service für Gesetzestexte | `dev/roadmap/v0.2-to-build-a988fb.md` | 120 |
| open | **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) | `dev/roadmap/v0.2-to-build-a988fb.md` | 121 |
| open | **[LEGAL-3]** NiFi ingest_laws + rag_index | `dev/roadmap/v0.2-to-build-a988fb.md` | 122 |
| open | **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 123 |
| open | **[LEGAL-5]** Frontend Tab „Legal/Compliance“ | `dev/roadmap/v0.2-to-build-a988fb.md` | 124 |
| open | **[LEGAL-6]** Dossier-Vorlage Compliance Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 125 |
| open | **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) | `dev/roadmap/v0.2-to-build-a988fb.md` | 128 |
| open | **[DISINFO-2]** Bot-Likelihood Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 129 |
| open | **[DISINFO-3]** Temporal Pattern Detection | `dev/roadmap/v0.2-to-build-a988fb.md` | 130 |
| open | **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier | `dev/roadmap/v0.2-to-build-a988fb.md` | 131 |
| open | **[DISINFO-5]** Frontend Dashboard Top Narratives | `dev/roadmap/v0.2-to-build-a988fb.md` | 132 |
| open | **[DISINFO-6]** Fact-Check API Integration | `dev/roadmap/v0.2-to-build-a988fb.md` | 133 |
| open | **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions | `dev/roadmap/v0.2-to-build-a988fb.md` | 136 |
| open | **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions | `dev/roadmap/v0.2-to-build-a988fb.md` | 137 |
| open | **[SUPPLY-3]** Simulation Engine (Event → Impact) | `dev/roadmap/v0.2-to-build-a988fb.md` | 138 |
| open | **[SUPPLY-4]** n8n Risk Alerts + Impact Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 139 |
| open | **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool | `dev/roadmap/v0.2-to-build-a988fb.md` | 140 |
| open | **[SUPPLY-6]** Dossier Supply Chain Risk Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 141 |
| open | **[FIN-1]** Graph-Schema Accounts/Transfers | `dev/roadmap/v0.2-to-build-a988fb.md` | 144 |
| open | **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions | `dev/roadmap/v0.2-to-build-a988fb.md` | 145 |
| open | **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) | `dev/roadmap/v0.2-to-build-a988fb.md` | 146 |
| open | **[FIN-4]** Anomaly Detection Module | `dev/roadmap/v0.2-to-build-a988fb.md` | 147 |
| open | **[FIN-5]** n8n Red Flag Alerts + Escalations | `dev/roadmap/v0.2-to-build-a988fb.md` | 148 |
| open | **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard | `dev/roadmap/v0.2-to-build-a988fb.md` | 149 |
| open | **[FIN-7]** Dossier Financial Red Flags | `dev/roadmap/v0.2-to-build-a988fb.md` | 150 |
| open | **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social | `dev/roadmap/v0.2-to-build-a988fb.md` | 153 |
| open | **[GEO-2]** Graph-Schema Events/Assets/Conflicts | `dev/roadmap/v0.2-to-build-a988fb.md` | 154 |
| open | **[GEO-3]** Geo-Time Anomaly Detection | `dev/roadmap/v0.2-to-build-a988fb.md` | 155 |
| open | **[GEO-4]** n8n Alerts + Conflict Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 156 |
| open | **[GEO-5]** Frontend Map Dashboard + Timeline | `dev/roadmap/v0.2-to-build-a988fb.md` | 157 |
| open | **[GEO-6]** Simulation Engine (Eskalations-Szenarien) | `dev/roadmap/v0.2-to-build-a988fb.md` | 158 |
| open | **[GEO-7]** Dossier Geopolitical Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 159 |
| open | **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators | `dev/roadmap/v0.2-to-build-a988fb.md` | 162 |
| open | **[HUM-2]** Graph-Schema Crisis/Indicators/Regions | `dev/roadmap/v0.2-to-build-a988fb.md` | 163 |
| open | **[HUM-3]** Risk Assessment Modul (ML) | `dev/roadmap/v0.2-to-build-a988fb.md` | 164 |
| open | **[HUM-4]** n8n Crisis Alerts + Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 165 |
| open | **[HUM-5]** Frontend Crisis Dashboard + Forecast | `dev/roadmap/v0.2-to-build-a988fb.md` | 166 |
| open | **[HUM-6]** Dossier Humanitarian Crisis Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 167 |
| open | **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) | `dev/roadmap/v0.2-to-build-a988fb.md` | 172 |
| open | **[CLIMATE-2]** Graph-Schema ClimateIndicators | `dev/roadmap/v0.2-to-build-a988fb.md` | 173 |
| open | **[CLIMATE-3]** CO₂/Emission Scoring Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 174 |
| open | **[CLIMATE-4]** n8n Alerts (Emission Targets) | `dev/roadmap/v0.2-to-build-a988fb.md` | 175 |
| open | **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap | `dev/roadmap/v0.2-to-build-a988fb.md` | 176 |
| open | **[CLIMATE-6]** Dossier Climate Risk Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 177 |
| open | **[TECH-1]** NiFi ingest_patents + research_data | `dev/roadmap/v0.2-to-build-a988fb.md` | 180 |
| open | **[TECH-2]** Graph-Schema Patents/TechTrends | `dev/roadmap/v0.2-to-build-a988fb.md` | 181 |
| open | **[TECH-3]** Innovation Hotspot Detection | `dev/roadmap/v0.2-to-build-a988fb.md` | 182 |
| open | **[TECH-4]** n8n Tech Trend Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 183 |
| open | **[TECH-5]** Frontend Patent/Innovation Graph | `dev/roadmap/v0.2-to-build-a988fb.md` | 184 |
| open | **[TECH-6]** Dossier Technology Trends | `dev/roadmap/v0.2-to-build-a988fb.md` | 185 |
| open | **[TERROR-1]** Ingest Propaganda Sources (Social, Web) | `dev/roadmap/v0.2-to-build-a988fb.md` | 188 |
| open | **[TERROR-2]** Graph-Schema TerrorNetworks | `dev/roadmap/v0.2-to-build-a988fb.md` | 189 |
| open | **[TERROR-3]** Finance Flow Analysis | `dev/roadmap/v0.2-to-build-a988fb.md` | 190 |
| open | **[TERROR-4]** n8n Alerts Suspicious Networks | `dev/roadmap/v0.2-to-build-a988fb.md` | 191 |
| open | **[TERROR-5]** Frontend Terror Network Graph | `dev/roadmap/v0.2-to-build-a988fb.md` | 192 |
| open | **[TERROR-6]** Dossier Terrorism Threat Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 193 |
| open | **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) | `dev/roadmap/v0.2-to-build-a988fb.md` | 196 |
| open | **[HEALTH-2]** Graph-Schema HealthEvents/Regions | `dev/roadmap/v0.2-to-build-a988fb.md` | 197 |
| open | **[HEALTH-3]** Epidemic Outbreak Detection | `dev/roadmap/v0.2-to-build-a988fb.md` | 198 |
| open | **[HEALTH-4]** n8n Health Alerts + Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 199 |
| open | **[HEALTH-5]** Frontend Health Dashboard | `dev/roadmap/v0.2-to-build-a988fb.md` | 200 |
| open | **[HEALTH-6]** Dossier Health/Epidemic Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 201 |
| open | **[ETHICS-1]** Ingest Model Cards + AI Incident Data | `dev/roadmap/v0.2-to-build-a988fb.md` | 204 |
| open | **[ETHICS-2]** Graph-Schema Bias/Models/Orgs | `dev/roadmap/v0.2-to-build-a988fb.md` | 205 |
| open | **[ETHICS-3]** Bias Detection Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 206 |
| open | **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) | `dev/roadmap/v0.2-to-build-a988fb.md` | 207 |
| open | **[ETHICS-5]** Frontend AI Ethics Dashboard | `dev/roadmap/v0.2-to-build-a988fb.md` | 208 |
| open | **[ETHICS-6]** Dossier AI Ethics Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 209 |
| open | **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) | `dev/roadmap/v0.2-to-build-a988fb.md` | 212 |
| open | **[MEDIA-2]** Deepfake Detection Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 213 |
| open | **[MEDIA-3]** Graph-Schema MediaAuthenticity | `dev/roadmap/v0.2-to-build-a988fb.md` | 214 |
| open | **[MEDIA-4]** n8n Alerts Fake Media | `dev/roadmap/v0.2-to-build-a988fb.md` | 215 |
| open | **[MEDIA-5]** Frontend Media Forensics Panel | `dev/roadmap/v0.2-to-build-a988fb.md` | 216 |
| open | **[MEDIA-6]** Dossier Media Authenticity Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 217 |
| open | **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) | `dev/roadmap/v0.2-to-build-a988fb.md` | 220 |
| open | **[ECON-2]** Graph-Schema EconomicIndicators/Trades | `dev/roadmap/v0.2-to-build-a988fb.md` | 221 |
| open | **[ECON-3]** Market Risk Analysis Modul | `dev/roadmap/v0.2-to-build-a988fb.md` | 222 |
| open | **[ECON-4]** n8n Economic Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 223 |
| open | **[ECON-5]** Frontend Economic Dashboard | `dev/roadmap/v0.2-to-build-a988fb.md` | 224 |
| open | **[ECON-6]** Dossier Economic Intelligence Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 225 |
| open | **[CULTURE-1]** Ingest Social/News/Blog Data | `dev/roadmap/v0.2-to-build-a988fb.md` | 228 |
| open | **[CULTURE-2]** Graph-Schema Narratives/Discourse | `dev/roadmap/v0.2-to-build-a988fb.md` | 229 |
| open | **[CULTURE-3]** Meme/Hashtag Cluster Detection | `dev/roadmap/v0.2-to-build-a988fb.md` | 230 |
| open | **[CULTURE-4]** n8n Cultural Trend Reports | `dev/roadmap/v0.2-to-build-a988fb.md` | 231 |
| open | **[CULTURE-5]** Frontend Cultural Trends Dashboard | `dev/roadmap/v0.2-to-build-a988fb.md` | 232 |
| open | **[CULTURE-6]** Dossier Cultural Intelligence Report | `dev/roadmap/v0.2-to-build-a988fb.md` | 233 |
| open | **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) | `dev/roadmap/v0.2-to-build-49a88e.md` | 3 |
| open | **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden | `dev/roadmap/v0.2-to-build-49a88e.md` | 4 |
| open | **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen | `dev/roadmap/v0.2-to-build-49a88e.md` | 5 |
| open | **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix | `dev/roadmap/v0.2-to-build-49a88e.md` | 6 |
| open | **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos | `dev/roadmap/v0.2-to-build-49a88e.md` | 7 |
| open | **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle | `dev/roadmap/v0.2-to-build-49a88e.md` | 8 |
| open | **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) | `dev/roadmap/v0.2-to-build-49a88e.md` | 9 |
| open | **[FLOWISE-1]** Flowise Deployment (Container, OIDC via Agent-Gateway) | `blueprints/blueprint-flowise-agents.md` | 449 |
| open | **[FLOWISE-2]** Agent-Gateway (Auth, RBAC, Rate-Limit, Audit, Vault) | `blueprints/blueprint-flowise-agents.md` | 450 |
| open | **[FLOWISE-3]** Tool-Adapter v1 (search, graph, rag) | `blueprints/blueprint-flowise-agents.md` | 451 |
| open | **[FLOWISE-4]** Agent-Registry (PG + YAML Sign + API) | `blueprints/blueprint-flowise-agents.md` | 452 |
| open | **[FLOWISE-5]** Starter-Agents (Research, Graph, Dossier) | `blueprints/blueprint-flowise-agents.md` | 453 |
| open | **[FLOWISE-6]** n8n Node `Run Flowise Agent` | `blueprints/blueprint-flowise-agents.md` | 454 |
| open | **[FLOWISE-7]** NiFi Processor `InvokeFlowiseAgent` | `blueprints/blueprint-flowise-agents.md` | 455 |
| open | **[FLOWISE-8]** Tool-Adapter v2 (verify, geo, forensics) | `blueprints/blueprint-flowise-agents.md` | 456 |
| open | **[FLOWISE-9]** Security Policies (OPA Rego + Sandbox Profiles) | `blueprints/blueprint-flowise-agents.md` | 457 |
| open | **[FLOWISE-10]** Preset Wiring (default_agents) | `blueprints/blueprint-flowise-agents.md` | 458 |
| open | **[FLOWISE-11]** Eval Suites + CI Scorer | `blueprints/blueprint-flowise-agents.md` | 459 |
| open | **[FLOWISE-12]** Meta-Planner Agent (v1.0) | `blueprints/blueprint-flowise-agents.md` | 460 |
| open | **[FLOWISE-13]** Cost/Token Budgets + Alerts | `blueprints/blueprint-flowise-agents.md` | 461 |
| open | **[FLOWISE-14]** Canary & Rollback Mechanik | `blueprints/blueprint-flowise-agents.md` | 462 |
| open | **[WT-EMBED-1]** Webview Tab `/terminal` + SSO (OIDC) | `integrations/waveterm/README.md` | 394 |
| open | **[WT-EMBED-2]** Profiles Loader (journalism/compliance/crisis/…) | `integrations/waveterm/README.md` | 395 |
| open | **[WT-EMBED-3]** “Send to WaveTerm” Actions (+context payload) | `integrations/waveterm/README.md` | 396 |
| open | **[WT-EMBED-4]** Session Recording → Dossier Appendix | `integrations/waveterm/README.md` | 397 |
| open | **[WT-PLUGIN-1]** WaveTerm Plugin Manifest (`it` commands, panels) | `integrations/waveterm/README.md` | 398 |
| open | **[WT-PLUGIN-2]** Dossier/Graph Previews (MD/SVG) | `integrations/waveterm/README.md` | 399 |
| open | **[WT-PLUGIN-3]** Command Palettes & Snippets | `integrations/waveterm/README.md` | 400 |
| open | **[WT-JOBS-1]** `/api/jobs` (queue, artifacts) | `integrations/waveterm/README.md` | 401 |
| open | **[WT-JOBS-2]** n8n Node `waveterm.run` | `integrations/waveterm/README.md` | 402 |
| open | **[WT-JOBS-3]** NiFi Processor `WaveTermInvoker` | `integrations/waveterm/README.md` | 403 |
| open | **[WT-SEC-1]** gVisor/Kata runtime + default no-net | `integrations/waveterm/README.md` | 404 |
| open | **[WT-SEC-2]** OPA policies (tool allowlist, export gates) | `integrations/waveterm/README.md` | 405 |
| open | **[WT-SEC-3]** Vault tokens (short-lived) for CLI/API | `integrations/waveterm/README.md` | 406 |
| open | **[WT-DOC-1]** `docs/waveterm/README.md` (Setup, Profiles, Safety) | `integrations/waveterm/README.md` | 407 |
| open | **[WT-DOC-2]** `docs/waveterm/presets/*.yaml` Beispiele | `integrations/waveterm/README.md` | 408 |
| open | **[WT-DOC-3]** `docs/api/jobs.md` Spezifikation | `integrations/waveterm/README.md` | 409 |
| open | **[EXPORT-1]** Bundle-Builder (md + assets + meta/export.json) | `integrations/export/AFFINE.md` | 195 |
| open | **[EXPORT-2]** Graph-Exporter (mermaid.mmd, dot, svg) | `integrations/export/AFFINE.md` | 196 |
| open | **[EXPORT-3]** Canvas-Exporter (excalidraw.json) | `integrations/export/AFFINE.md` | 197 |
| open | **[EXPORT-4]** Geo-Exporter (geojson + map.png/svg) | `integrations/export/AFFINE.md` | 198 |
| open | **[APPFLOWY-1]** AppFlowy Adapter – Watched Folder | `integrations/export/AFFINE.md` | 199 |
| open | **[APPFLOWY-2]** AppFlowy Adapter – API Mode (optional) | `integrations/export/AFFINE.md` | 200 |
| open | **[AFFINE-1]** AFFiNE Adapter – Watched Folder + Edgeless Import | `integrations/export/AFFINE.md` | 201 |
| open | **[AFFINE-2]** AFFiNE Adapter – API Mode (optional) | `integrations/export/AFFINE.md` | 202 |
| open | **[FE-EXPORT-1]** Frontend Export-Dialog (Targets + Formate) | `integrations/export/AFFINE.md` | 203 |
| open | **[CLI-EXP-1]** CLI `it export dossier/graph/canvas` | `integrations/export/AFFINE.md` | 204 |
| open | **[N8N-EXP-1]** n8n Nodes `export_to_appflowy` / `export_to_affine` | `integrations/export/AFFINE.md` | 205 |
| open | **[POLICY-EXP-1]** OPA-Regeln (classification gates) | `integrations/export/AFFINE.md` | 206 |
| open | **[VAULT-EXP-1]** Secrets Handling für Adapter-APIs | `integrations/export/AFFINE.md` | 207 |
| open | **[QA-EXP-1]** Golden Bundle Tests | `integrations/export/AFFINE.md` | 208 |
| open | **[QA-EXP-2]** Roundtrip Import Tests | `integrations/export/AFFINE.md` | 209 |
