| ID | File | Line | Text |
|---|---|---|---|
| T0001-123e | docs/SECURITY_SWEEP.md | 3 | - TODO: Secrets rotieren (Keycloak admin, oauth2-proxy cookie, DB-Passwörter). |
| T0002-9f6d | docs/SECURITY_SWEEP.md | 4 | - TODO: TLS/Ingress für Prod (Cert-Manager). |
| T0003-95be | docs/SECURITY_SWEEP.md | 5 | - TODO: Backups für PG/OpenSearch/Neo4j. |
| T0004-0877 | docs/TODO-Index.md | 1 | # TODO-Index |
| T0005-eebd | docs/release-checklist-v0.1.md | 10 | - [ ] Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). |
| T0006-6c05 | docs/release-checklist-v0.1.md | 11 | - [ ] **Conftest/OPA Policies** laufen sauber (`make ci-policy`). |
| T0007-7b3c | docs/release-checklist-v0.1.md | 12 | - [ ] **Secrets entfernt** aus Manifests/Code (`grep -R "password" infra/ services/ \\| grep -v example` → leer). |
| T0008-1054 | docs/release-checklist-v0.1.md | 13 | - [ ] **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. |
| T0009-eca0 | docs/release-checklist-v0.1.md | 14 | - [ ] **Ingress TLS** aktiv (cert-manager, staging Issuer OK). |
| T0010-32fc | docs/release-checklist-v0.1.md | 15 | - [ ] Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). |
| T0011-4f3a | docs/release-checklist-v0.1.md | 21 | - [ ] **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). |
| T0012-d26e | docs/release-checklist-v0.1.md | 22 | - [ ] **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). |
| T0013-d31f | docs/release-checklist-v0.1.md | 23 | - [ ] **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. |
| T0014-685a | docs/release-checklist-v0.1.md | 24 | - [ ] **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. |
| T0015-ab33 | docs/release-checklist-v0.1.md | 25 | - [ ] **Dependabot** aktiviert (pip, npm, GitHub Actions). |
| T0016-8f65 | docs/release-checklist-v0.1.md | 26 | - [ ] **Trivy Scan** ohne kritische Findings. |
| T0017-3458 | docs/release-checklist-v0.1.md | 32 | - [ ] **dbt build/test** grün (Seeds, Models, Tests). |
| T0018-2aca | docs/release-checklist-v0.1.md | 33 | - [ ] **dbt docs generate** erzeugt Artefakt (Docs erreichbar). |
| T0019-8c28 | docs/release-checklist-v0.1.md | 34 | - [ ] **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). |
| T0020-3e64 | docs/release-checklist-v0.1.md | 35 | - [ ] **Exposures** definiert (Superset Dashboards verlinkt). |
| T0021-5a64 | docs/release-checklist-v0.1.md | 36 | - [ ] **Freshness Checks** für Sources ohne Errors. |
| T0022-d46f | docs/release-checklist-v0.1.md | 42 | - [ ] **Superset Dashboard** „analytics_prices“ importiert: |
| T0023-887e | docs/release-checklist-v0.1.md | 45 | - [ ] **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. |
| T0024-7e0b | docs/release-checklist-v0.1.md | 46 | - [ ] Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). |
| T0025-b8e1 | docs/release-checklist-v0.1.md | 47 | - [ ] **Vitest/Playwright Tests** decken Detailseiten ab. |
| T0026-8521 | docs/release-checklist-v0.1.md | 53 | - [ ] **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. |
| T0027-6e44 | docs/release-checklist-v0.1.md | 54 | - [ ] **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. |
| T0028-d0e1 | docs/release-checklist-v0.1.md | 55 | - [ ] **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). |
| T0029-574b | docs/release-checklist-v0.1.md | 56 | - [ ] Restore-Runbook einmal **trocken getestet**. |
| T0030-a42b | docs/release-checklist-v0.1.md | 62 | - [ ] **OTel Collector** deployed (4317/4318/9464 erreichbar). |
| T0031-3686 | docs/release-checklist-v0.1.md | 63 | - [ ] **Python Services** exportieren Traces + `/metrics`. |
| T0032-50c9 | docs/release-checklist-v0.1.md | 64 | - [ ] **Node Services** exportieren Traces + `/metrics`. |
| T0033-fd89 | docs/release-checklist-v0.1.md | 65 | - [ ] **Prometheus** scrapt Services; Grafana Panels gefüllt. |
| T0034-8197 | docs/release-checklist-v0.1.md | 66 | - [ ] **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). |
| T0035-b3e9 | docs/release-checklist-v0.1.md | 67 | - [ ] **Loki** enthält Logs aller Services (Promtail shipping OK). |
| T0036-206b | docs/release-checklist-v0.1.md | 68 | - [ ] **Grafana Dashboards**: |
| T0037-f9ff | docs/release-checklist-v0.1.md | 76 | - [ ] **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). |
| T0038-f0be | docs/release-checklist-v0.1.md | 77 | - [ ] **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. |
| T0039-e2d9 | docs/release-checklist-v0.1.md | 78 | - [ ] **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. |
| T0040-8dc3 | docs/release-checklist-v0.1.md | 79 | - [ ] **Language Policy**: Docs in EN, DE als Appendix. |
| T0041-72f3 | docs/release-checklist-v0.1.md | 80 | - [ ] **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. |
| T0042-ffe9 | docs/release-checklist-v0.1.md | 81 | - [ ] **CI Docs-Checks** grün (markdownlint, link check, doctoc). |
| T0043-60e9 | docs/release-checklist-v0.1.md | 87 | - [ ] **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. |
| T0044-c003 | docs/release-checklist-v0.1.md | 88 | - [ ] **Ingress Hosts** & TLS validiert. |
| T0045-c622 | docs/release-checklist-v0.1.md | 89 | - [ ] **Demo-Data Seed** erfolgreich (`make seed-demo`). |
| T0046-1aba | docs/release-checklist-v0.1.md | 90 | - [ ] **Smoke-Test** im Staging: |
| T0047-63c7 | docs/release-checklist-v0.1.md | 103 | - [ ] `main` eingefroren, `release/v0.1` Branch erstellt. |
| T0048-0400 | docs/release-checklist-v0.1.md | 104 | - [ ] **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). |
| T0049-b6c0 | docs/release-checklist-v0.1.md | 105 | - [ ] **Release Notes** erstellt (Features, Breaking Changes, Known Issues). |
| T0050-bac8 | docs/release-checklist-v0.1.md | 106 | - [ ] **Tag v0.1.0** gesetzt und Release publiziert. |
| T0051-3445 | docs/release-checklist-v0.1.md | 107 | - [ ] Dokumentation zur Installation/Exploration angehängt. |
| T0052-d5d2 | docs/waveterm/README.md | 388 | ### **TODO-Index – Ergänzung** |
| T0053-4704 | docs/waveterm/README.md | 390 | > Hänge an `docs/TODO-Index.md` an: |
| T0054-5f70 | docs/waveterm/README.md | 394 | - [ ] **[WT-EMBED-1]** Webview Tab `/terminal` + SSO (OIDC) |
| T0055-9759 | docs/waveterm/README.md | 395 | - [ ] **[WT-EMBED-2]** Profiles Loader (journalism/compliance/crisis/…) |
| T0056-929c | docs/waveterm/README.md | 396 | - [ ] **[WT-EMBED-3]** “Send to WaveTerm” Actions (+context payload) |
| T0057-b9f3 | docs/waveterm/README.md | 397 | - [ ] **[WT-EMBED-4]** Session Recording → Dossier Appendix |
| T0058-6730 | docs/waveterm/README.md | 398 | - [ ] **[WT-PLUGIN-1]** WaveTerm Plugin Manifest (`it` commands, panels) |
| T0059-4a48 | docs/waveterm/README.md | 399 | - [ ] **[WT-PLUGIN-2]** Dossier/Graph Previews (MD/SVG) |
| T0060-e18e | docs/waveterm/README.md | 400 | - [ ] **[WT-PLUGIN-3]** Command Palettes & Snippets |
| T0061-6f2a | docs/waveterm/README.md | 401 | - [ ] **[WT-JOBS-1]** `/api/jobs` (queue, artifacts) |
| T0062-3758 | docs/waveterm/README.md | 402 | - [ ] **[WT-JOBS-2]** n8n Node `waveterm.run` |
| T0063-6246 | docs/waveterm/README.md | 403 | - [ ] **[WT-JOBS-3]** NiFi Processor `WaveTermInvoker` |
| T0064-179c | docs/waveterm/README.md | 404 | - [ ] **[WT-SEC-1]** gVisor/Kata runtime + default no-net |
| T0065-b2c8 | docs/waveterm/README.md | 405 | - [ ] **[WT-SEC-2]** OPA policies (tool allowlist, export gates) |
| T0066-f4c5 | docs/waveterm/README.md | 406 | - [ ] **[WT-SEC-3]** Vault tokens (short-lived) for CLI/API |
| T0067-bbf5 | docs/waveterm/README.md | 407 | - [ ] **[WT-DOC-1]** `docs/waveterm/README.md` (Setup, Profiles, Safety) |
| T0068-b6f6 | docs/waveterm/README.md | 408 | - [ ] **[WT-DOC-2]** `docs/waveterm/presets/*.yaml` Beispiele |
| T0069-3430 | docs/waveterm/README.md | 409 | - [ ] **[WT-DOC-3]** `docs/api/jobs.md` Spezifikation |
| T0070-974f | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 443 | ### **TODO-Index Ergänzung (neuer Abschnitt)** |
| T0071-5eb5 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 445 | > füge ans Ende von `docs/TODO-Index.md` hinzu: |
| T0072-b2e9 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 449 | - [ ] **[FLOWISE-1]** Flowise Deployment (Container, OIDC via Agent-Gateway) |
| T0073-8199 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 450 | - [ ] **[FLOWISE-2]** Agent-Gateway (Auth, RBAC, Rate-Limit, Audit, Vault) |
| T0074-d7da | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 451 | - [ ] **[FLOWISE-3]** Tool-Adapter v1 (search, graph, rag) |
| T0075-4c75 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 452 | - [ ] **[FLOWISE-4]** Agent-Registry (PG + YAML Sign + API) |
| T0076-c3ee | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 453 | - [ ] **[FLOWISE-5]** Starter-Agents (Research, Graph, Dossier) |
| T0077-3482 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 454 | - [ ] **[FLOWISE-6]** n8n Node `Run Flowise Agent` |
| T0078-a491 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 455 | - [ ] **[FLOWISE-7]** NiFi Processor `InvokeFlowiseAgent` |
| T0079-2479 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 456 | - [ ] **[FLOWISE-8]** Tool-Adapter v2 (verify, geo, forensics) |
| T0080-9c7e | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 457 | - [ ] **[FLOWISE-9]** Security Policies (OPA Rego + Sandbox Profiles) |
| T0081-ed8f | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 458 | - [ ] **[FLOWISE-10]** Preset Wiring (default_agents) |
| T0082-5f86 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 459 | - [ ] **[FLOWISE-11]** Eval Suites + CI Scorer |
| T0083-be8b | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 460 | - [ ] **[FLOWISE-12]** Meta-Planner Agent (v1.0) |
| T0084-350c | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 461 | - [ ] **[FLOWISE-13]** Cost/Token Budgets + Alerts |
| T0085-6bfd | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 462 | - [ ] **[FLOWISE-14]** Canary & Rollback Mechanik |
| T0086-e8f4 | docs/blueprints/SECURITY-BLUEPRINT.md | 120 | ## ✅ Tickets (Erweiterung zum TODO-Index) |
| T0087-d4ba | docs/blueprints/VERIFICATION-BLUEPRINT.md | 171 | # 🧩 Tickets (zum Ergänzen deines TODO-Index) |
| T0088-a03b | docs/blueprints/VERIFICATION-BLUEPRINT.md | 504 | ## ✅ Tickets (zum TODO-Index ergänzen) |
| T0089-9923 | docs/dev/Checkliste.md | 10 | Weitere Details siehe `TODO-Index.md`. |
| T0090-a178 | docs/dev/README.md | 429 | # TODO: filter by OPA decision (resource tags vs user attributes) |
| T0091-9add | docs/dev/SECURITY-BLUEPRINT.md | 120 | ## ✅ Tickets (Erweiterung zum TODO-Index) |
| T0092-a02a | docs/dev/VERIFICATION-BLUEPRINT.md | 360 | ## ✅ Tickets (zum TODO-Index ergänzen) |
| T0093-38a5 | docs/dev/frontend_modernization_guide.md | 205 | - [ ] Design System implementiert |
| T0094-8f4a | docs/dev/frontend_modernization_guide.md | 206 | - [ ] Layout System eingerichtet |
| T0095-064f | docs/dev/frontend_modernization_guide.md | 207 | - [ ] Komponenten modernisiert |
| T0096-f94f | docs/dev/frontend_modernization_guide.md | 208 | - [ ] Responsive Design getestet |
| T0097-0d03 | docs/dev/frontend_modernization_guide.md | 209 | - [ ] Performance optimiert |
| T0098-599d | docs/dev/frontend_modernization_guide.md | 210 | - [ ] Tests aktualisiert |
| T0099-df6d | docs/dev/frontend_modernization_guide.md | 211 | - [ ] Accessibility geprüft |
| T0100-e4bc | docs/dev/frontend_modernization_guide.md | 212 | - [ ] Cross-Browser Tests |
| T0101-eb76 | docs/dev/frontend_modernization_guide.md | 213 | - [ ] Mobile Experience validiert |
| T0102-8937 | docs/dev/frontend_modernization_guide.md | 214 | - [ ] Documentation aktualisiert |
| T0103-f92e | docs/dev/superset-nifi-flowise.md | 184 | - [ ] **Superset-Composer**: JS/Python Helper eingebaut → Link öffnet Dashboard mit Filtern |
| T0104-bf72 | docs/dev/superset-nifi-flowise.md | 185 | - [ ] **NiFi→Aleph**: InvokeHTTP Multipart konfiguriert, 200/202 Rückgabe sichtbar |
| T0105-0b79 | docs/dev/superset-nifi-flowise.md | 186 | - [ ] **Flowise Agent**: Tools/Schemas registriert, Guardrail-Prompt gesetzt, Tool-Limit aktiv |
| T0106-c015 | docs/dev/superset-nifi-flowise.md | 187 | - [ ] **Smoke Tests**: |
| T0107-c900 | docs/dev/roadmap/v0.2-overview.md | 103 | - [ ] T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T0108-993d | docs/dev/roadmap/v0.2-overview.md | 104 | - [ ] T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T0109-a50e | docs/dev/roadmap/v0.2-overview.md | 105 | - [ ] T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T0110-aa9c | docs/dev/roadmap/v0.2-overview.md | 106 | - [ ] T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T0111-029c | docs/dev/roadmap/v0.2-overview.md | 107 | - [ ] T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T0112-f95d | docs/dev/roadmap/v0.2-overview.md | 108 | - [ ] T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T0113-9052 | docs/dev/roadmap/v0.2-overview.md | 109 | - [ ] T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T0114-73c9 | docs/dev/roadmap/v0.2-overview.md | 110 | - [ ] T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T0115-4d3f | docs/dev/roadmap/v0.2-overview.md | 111 | - [ ] T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T0116-07a6 | docs/dev/roadmap/v0.2-overview.md | 112 | - [ ] T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T0117-4b6d | docs/dev/roadmap/v0.2-overview.md | 113 | - [ ] T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T0118-0eb7 | docs/dev/roadmap/v0.2-overview.md | 114 | - [ ] T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T0119-bf23 | docs/dev/roadmap/v0.2-overview.md | 115 | - [ ] T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T0120-e436 | docs/dev/roadmap/v0.2-overview.md | 116 | - [ ] T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T0121-23d3 | docs/dev/roadmap/v0.2-overview.md | 117 | - [ ] T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T0122-d79e | docs/dev/roadmap/v0.2-overview.md | 118 | - [ ] T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T0123-17bb | docs/dev/roadmap/v0.2-overview.md | 119 | - [ ] T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T0124-6fe0 | docs/dev/roadmap/v0.2-overview.md | 120 | - [ ] T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T0125-9422 | docs/dev/roadmap/v0.2-overview.md | 121 | - [ ] T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T0126-1648 | docs/dev/roadmap/v0.2-overview.md | 122 | - [ ] T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T0127-04d4 | docs/dev/roadmap/v0.2-overview.md | 123 | - [ ] T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T0128-504c | docs/dev/roadmap/v0.2-overview.md | 124 | - [ ] T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T0129-8642 | docs/dev/roadmap/v0.2-overview.md | 125 | - [ ] T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T0130-8ea1 | docs/dev/roadmap/v0.2-overview.md | 126 | - [ ] T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T0131-4396 | docs/dev/roadmap/v0.2-overview.md | 127 | - [ ] T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T0132-f8e4 | docs/dev/roadmap/v0.2-overview.md | 128 | - [ ] T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T0133-fa5e | docs/dev/roadmap/v0.2-overview.md | 129 | - [ ] T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T0134-2334 | docs/dev/roadmap/v0.2-overview.md | 130 | - [ ] T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T0135-dfe5 | docs/dev/roadmap/v0.2-overview.md | 131 | - [ ] T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T0136-b1a3 | docs/dev/roadmap/v0.2-overview.md | 132 | - [ ] T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T0137-60ad | docs/dev/roadmap/v0.2-overview.md | 133 | - [ ] T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T0138-0b24 | docs/dev/roadmap/v0.2-overview.md | 134 | - [ ] T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T0139-e439 | docs/dev/roadmap/v0.2-overview.md | 135 | - [ ] T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T0140-bc80 | docs/dev/roadmap/v0.2-overview.md | 136 | - [ ] T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T0141-46b0 | docs/dev/roadmap/v0.2-overview.md | 137 | - [ ] T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T0142-21f0 | docs/dev/roadmap/v0.2-overview.md | 138 | - [ ] T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T0143-6637 | docs/dev/roadmap/v0.2-overview.md | 139 | - [ ] T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T0144-203c | docs/dev/roadmap/v0.2-overview.md | 140 | - [ ] T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T0145-5dc5 | docs/dev/roadmap/v0.2-overview.md | 141 | - [ ] T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T0146-10b0 | docs/dev/roadmap/v0.2-overview.md | 142 | - [ ] T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T0147-90e5 | docs/dev/roadmap/v0.2-overview.md | 143 | - [ ] T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T0148-3465 | docs/dev/roadmap/v0.2-overview.md | 144 | - [ ] T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T0149-ea22 | docs/dev/roadmap/v0.2-overview.md | 145 | - [ ] T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T0150-4c65 | docs/dev/roadmap/v0.2-overview.md | 146 | - [ ] T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T0151-2fd6 | docs/dev/roadmap/v0.2-overview.md | 147 | - [ ] T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T0152-3de7 | docs/dev/roadmap/v0.2-overview.md | 148 | - [ ] T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T0153-1141 | docs/dev/roadmap/v0.2-overview.md | 149 | - [ ] T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T0154-e25b | docs/dev/roadmap/v0.2-overview.md | 150 | - [ ] T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T0155-52ee | docs/dev/roadmap/v0.2-overview.md | 151 | - [ ] T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T0156-a970 | docs/dev/roadmap/v0.2-overview.md | 152 | - [ ] T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T0157-eb70 | docs/dev/roadmap/v0.2-overview.md | 153 | - [ ] T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T0158-c59f | docs/dev/roadmap/v0.2-overview.md | 154 | - [ ] T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T0159-e81e | docs/dev/roadmap/v0.2-overview.md | 155 | - [ ] T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T0160-f48b | docs/dev/roadmap/v0.2-overview.md | 156 | - [ ] T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T0161-4486 | docs/dev/roadmap/v0.2-overview.md | 157 | - [ ] T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T0162-2a68 | docs/dev/roadmap/v0.2-overview.md | 158 | - [ ] T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T0163-3932 | docs/dev/roadmap/v0.2-overview.md | 159 | - [ ] T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T0164-a424 | docs/dev/roadmap/v0.2-overview.md | 160 | - [ ] T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T0165-0267 | docs/dev/roadmap/v0.2-overview.md | 161 | - [ ] T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T0166-de78 | docs/dev/roadmap/v0.2-overview.md | 162 | - [ ] T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T0167-3d4f | docs/dev/roadmap/v0.2-overview.md | 163 | - [ ] T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T0168-3c90 | docs/dev/roadmap/v0.2-overview.md | 164 | - [ ] T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T0169-661b | docs/dev/roadmap/v0.2-overview.md | 165 | - [ ] T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T0170-ebca | docs/dev/roadmap/v0.2-overview.md | 166 | - [ ] T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T0171-ce42 | docs/dev/roadmap/v0.2-overview.md | 167 | - [ ] T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T0172-13c7 | docs/dev/roadmap/v0.2-overview.md | 168 | - [ ] T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T0173-d114 | docs/dev/roadmap/v0.2-overview.md | 169 | - [ ] T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T0174-b7c8 | docs/dev/roadmap/v0.2-overview.md | 170 | - [ ] T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T0175-5b1e | docs/dev/roadmap/v0.2-overview.md | 171 | - [ ] T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T0176-e2a0 | docs/dev/roadmap/v0.2-overview.md | 172 | - [ ] T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T0177-b641 | docs/dev/roadmap/v0.2-overview.md | 173 | - [ ] T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T0178-644e | docs/dev/roadmap/v0.2-overview.md | 174 | - [ ] T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T0179-60b4 | docs/dev/roadmap/v0.2-overview.md | 175 | - [ ] T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T0180-817f | docs/dev/roadmap/v0.2-overview.md | 176 | - [ ] T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T0181-f016 | docs/dev/roadmap/v0.2-overview.md | 177 | - [ ] T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T0182-462f | docs/dev/roadmap/v0.2-overview.md | 178 | - [ ] T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T0183-b7c4 | docs/dev/roadmap/v0.2-overview.md | 179 | - [ ] T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T0184-e931 | docs/dev/roadmap/v0.2-overview.md | 180 | - [ ] T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T0185-9d65 | docs/dev/roadmap/v0.2-overview.md | 181 | - [ ] T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T0186-d08d | docs/dev/roadmap/v0.2-overview.md | 182 | - [ ] T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T0187-1ae5 | docs/dev/roadmap/v0.2-overview.md | 183 | - [ ] T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T0188-2593 | docs/dev/roadmap/v0.2-overview.md | 184 | - [ ] T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T0189-0db8 | docs/dev/roadmap/v0.2-overview.md | 185 | - [ ] T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T0190-21b4 | docs/dev/roadmap/v0.2-overview.md | 186 | - [ ] T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T0191-6abe | docs/dev/roadmap/v0.2-overview.md | 187 | - [ ] T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T0192-6cf6 | docs/dev/roadmap/v0.2-overview.md | 188 | - [ ] T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T0193-402b | docs/dev/roadmap/v0.2-overview.md | 189 | - [ ] T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T0194-9595 | docs/dev/roadmap/v0.2-overview.md | 190 | - [ ] T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T0195-dae5 | docs/dev/roadmap/v0.2-overview.md | 191 | - [ ] T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T0196-e896 | docs/dev/roadmap/v0.2-overview.md | 192 | - [ ] T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T0197-1ee3 | docs/dev/roadmap/v0.2-overview.md | 193 | - [ ] T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T0198-06e7 | docs/dev/roadmap/v0.2-overview.md | 194 | - [ ] T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T0199-513a | docs/dev/roadmap/v0.2-overview.md | 195 | - [ ] T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T0200-28c4 | docs/dev/roadmap/v0.2-overview.md | 196 | - [ ] T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T0201-42c3 | docs/dev/roadmap/v0.2-overview.md | 197 | - [ ] T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T0202-bd4e | docs/dev/roadmap/v0.2-overview.md | 198 | - [ ] T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T0203-495f | docs/dev/roadmap/v0.2-overview.md | 199 | - [ ] T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T0204-be79 | docs/dev/roadmap/v0.2-overview.md | 200 | - [ ] T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T0205-75ce | docs/dev/roadmap/v0.2-overview.md | 201 | - [ ] T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T0206-0fa4 | docs/dev/roadmap/v0.2-overview.md | 202 | - [ ] T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T0207-45f9 | docs/dev/roadmap/v0.2-overview.md | 203 | - [ ] T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T0208-604a | docs/dev/roadmap/v0.2-overview.md | 204 | - [ ] T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T0209-8385 | docs/dev/roadmap/v0.2-overview.md | 205 | - [ ] T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T0210-83e9 | docs/dev/roadmap/v0.2-overview.md | 206 | - [ ] T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T0211-c2da | docs/dev/roadmap/v0.2-overview.md | 207 | - [ ] T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T0212-e321 | docs/dev/roadmap/v0.2-overview.md | 208 | - [ ] T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T0213-90c2 | docs/dev/roadmap/v0.2-overview.md | 209 | - [ ] T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T0214-dbb7 | docs/dev/roadmap/v0.2-overview.md | 210 | - [ ] T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T0215-45f9 | docs/dev/roadmap/v0.2-overview.md | 211 | - [ ] T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T0216-c57b | docs/dev/roadmap/v0.2-overview.md | 212 | - [ ] T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T0217-24e1 | docs/dev/roadmap/v0.2-overview.md | 213 | - [ ] T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T0218-68cf | docs/dev/roadmap/v0.2-overview.md | 214 | - [ ] T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T0219-45ed | docs/dev/roadmap/v0.2-overview.md | 215 | - [ ] T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T0220-6c4d | docs/dev/roadmap/v0.2-overview.md | 216 | - [ ] T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T0221-d81b | docs/dev/roadmap/v0.2-overview.md | 217 | - [ ] T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T0222-1afc | docs/dev/roadmap/v0.2-overview.md | 218 | - [ ] T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T0223-cc17 | docs/dev/roadmap/v0.2-overview.md | 219 | - [ ] T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T0224-ffd8 | docs/dev/roadmap/v0.2-overview.md | 220 | - [ ] T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T0225-1977 | docs/dev/roadmap/v0.2-overview.md | 221 | - [ ] T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T0226-8f55 | docs/dev/roadmap/v0.2-overview.md | 222 | - [ ] T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T0227-1fb4 | docs/dev/roadmap/v0.2-overview.md | 223 | - [ ] T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T0228-f631 | docs/dev/roadmap/v0.2-overview.md | 224 | - [ ] T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T0229-5b09 | docs/dev/roadmap/v0.2-overview.md | 225 | - [ ] T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T0230-0992 | docs/dev/roadmap/v0.2-overview.md | 226 | - [ ] T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T0231-2147 | docs/dev/roadmap/v0.2-overview.md | 227 | - [ ] T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T0232-2c69 | docs/dev/roadmap/v0.2-overview.md | 228 | - [ ] T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T0233-f8fe | docs/dev/roadmap/v0.2-overview.md | 229 | - [ ] T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T0234-c938 | docs/dev/roadmap/v0.2-overview.md | 230 | - [ ] T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T0235-6a56 | docs/dev/roadmap/v0.2-overview.md | 231 | - [ ] T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T0236-b0d4 | docs/dev/roadmap/v0.2-overview.md | 232 | - [ ] T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T0237-7052 | docs/dev/roadmap/v0.2-overview.md | 233 | - [ ] T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T0238-fa2f | docs/dev/roadmap/v0.2-overview.md | 234 | - [ ] T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T0239-3b7d | docs/dev/roadmap/v0.2-overview.md | 235 | - [ ] T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T0240-d830 | docs/dev/roadmap/v0.2-overview.md | 236 | - [ ] T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T0241-c27f | docs/dev/roadmap/v0.2-overview.md | 237 | - [ ] T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T0242-9665 | docs/dev/roadmap/v0.2-overview.md | 238 | - [ ] T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T0243-9fbd | docs/dev/roadmap/v0.2-overview.md | 239 | - [ ] T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T0244-40aa | docs/dev/roadmap/v0.2-overview.md | 240 | - [ ] T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T0245-6f20 | docs/dev/roadmap/v0.2-overview.md | 241 | - [ ] T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T0246-a197 | docs/dev/roadmap/v0.2-overview.md | 242 | - [ ] T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T0247-096c | docs/dev/roadmap/v0.2-overview.md | 243 | - [ ] T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T0248-fd6c | docs/dev/roadmap/v0.2-overview.md | 244 | - [ ] T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T0249-6364 | docs/dev/roadmap/v0.2-overview.md | 245 | - [ ] T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T0250-07e7 | docs/dev/roadmap/v0.2-overview.md | 246 | - [ ] T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T0251-6d34 | docs/dev/roadmap/v0.2-overview.md | 247 | - [ ] T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T0252-df35 | docs/dev/roadmap/v0.2-overview.md | 248 | - [ ] T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T0253-d812 | docs/dev/roadmap/v0.2-overview.md | 249 | - [ ] T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T0254-6215 | docs/dev/roadmap/v0.2-overview.md | 250 | - [ ] T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T0255-38eb | docs/dev/roadmap/v0.2-overview.md | 251 | - [ ] T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T0256-7713 | docs/dev/roadmap/v0.2-overview.md | 252 | - [ ] T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T0257-698e | docs/dev/roadmap/v0.2-overview.md | 253 | - [ ] T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T0258-6de5 | docs/dev/roadmap/v0.2-overview.md | 254 | - [ ] T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T0259-8bd2 | docs/dev/roadmap/v0.2-overview.md | 255 | - [ ] T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T0260-111d | docs/dev/roadmap/v0.2-overview.md | 256 | - [ ] T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T0261-bb0f | docs/dev/roadmap/v0.2-overview.md | 257 | - [ ] T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T0262-a94d | docs/dev/roadmap/v0.2-overview.md | 258 | - [ ] T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T0263-2ede | docs/dev/roadmap/v0.2-overview.md | 259 | - [ ] T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T0264-d22a | docs/dev/roadmap/v0.2-overview.md | 260 | - [ ] T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T0265-7d1a | docs/dev/roadmap/v0.2-overview.md | 261 | - [ ] T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T0266-c7ab | docs/dev/roadmap/v0.2-overview.md | 262 | - [ ] T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T0267-0cf5 | docs/dev/roadmap/v0.2-overview.md | 263 | - [ ] T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T0268-8bdd | docs/dev/roadmap/v0.2-overview.md | 264 | - [ ] T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T0269-09d0 | docs/dev/roadmap/v0.2-overview.md | 265 | - [ ] T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T0270-0a32 | docs/dev/roadmap/v0.2-overview.md | 266 | - [ ] T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T0271-4601 | docs/dev/roadmap/v0.2-overview.md | 267 | - [ ] T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T0272-547e | docs/dev/roadmap/v0.2-overview.md | 268 | - [ ] T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T0273-4c9f | docs/dev/roadmap/v0.2-overview.md | 269 | - [ ] T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T0274-2185 | docs/dev/roadmap/v0.2-overview.md | 270 | - [ ] T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T0275-8ba6 | docs/dev/roadmap/v0.2-overview.md | 271 | - [ ] T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T0276-0886 | docs/dev/roadmap/v0.2-overview.md | 272 | - [ ] T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T0277-9b3c | docs/dev/roadmap/v0.2-overview.md | 273 | - [ ] T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T0278-8770 | docs/dev/roadmap/v0.2-overview.md | 274 | - [ ] T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T0279-65a3 | docs/dev/roadmap/v0.2-overview.md | 275 | - [ ] T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T0280-59b1 | docs/dev/roadmap/v0.2-overview.md | 276 | - [ ] T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T0281-404e | docs/dev/roadmap/v0.2-overview.md | 277 | - [ ] T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T0282-faf0 | docs/dev/roadmap/v0.2-overview.md | 278 | - [ ] T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T0283-87f9 | docs/dev/roadmap/v0.2-overview.md | 279 | - [ ] T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T0284-1140 | docs/dev/roadmap/v0.2-overview.md | 280 | - [ ] T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T0285-d98b | docs/dev/roadmap/v0.2-overview.md | 281 | - [ ] T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T0286-016a | docs/dev/roadmap/v0.2-overview.md | 282 | - [ ] T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T0287-db81 | docs/dev/roadmap/v0.2-overview.md | 283 | - [ ] T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T0288-2f06 | docs/dev/roadmap/v0.2-overview.md | 284 | - [ ] T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T0289-665f | docs/dev/roadmap/v0.2-overview.md | 285 | - [ ] T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T0290-cae7 | docs/dev/roadmap/v0.2-overview.md | 286 | - [ ] T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T0291-77df | docs/dev/roadmap/v0.2-overview.md | 287 | - [ ] T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T0292-effb | docs/dev/roadmap/v0.2-overview.md | 288 | - [ ] T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T0293-5185 | docs/dev/roadmap/v0.2-overview.md | 289 | - [ ] T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T0294-db1c | docs/dev/roadmap/v0.2-overview.md | 290 | - [ ] T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T0295-a73a | docs/dev/roadmap/v0.2-overview.md | 291 | - [ ] T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T0296-6ded | docs/dev/roadmap/v0.2-overview.md | 292 | - [ ] T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T0297-c86b | docs/dev/roadmap/v0.2-overview.md | 293 | - [ ] T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T0298-5be9 | docs/dev/roadmap/v0.2-overview.md | 294 | - [ ] T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T0299-5adc | docs/dev/roadmap/v0.2-overview.md | 295 | - [ ] T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T0300-ceff | docs/dev/roadmap/v0.2-overview.md | 296 | - [ ] T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T0301-0486 | docs/dev/roadmap/v0.2-overview.md | 297 | - [ ] T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T0302-ea26 | docs/dev/roadmap/v0.2-overview.md | 298 | - [ ] T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T0303-004d | docs/dev/roadmap/v0.2-overview.md | 299 | - [ ] T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T0304-0dc1 | docs/dev/roadmap/v0.2-overview.md | 300 | - [ ] T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T0305-adc8 | docs/dev/roadmap/v0.2-overview.md | 301 | - [ ] T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T0306-48eb | docs/dev/roadmap/v0.2-overview.md | 302 | - [ ] T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T0307-5ed6 | docs/dev/roadmap/v0.2-overview.md | 303 | - [ ] T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T0308-d86f | docs/dev/roadmap/v0.2-overview.md | 304 | - [ ] T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T0309-8393 | docs/dev/roadmap/v0.2-overview.md | 305 | - [ ] T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T0310-8d04 | docs/dev/roadmap/v0.2-overview.md | 306 | - [ ] T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T0311-a424 | docs/dev/roadmap/v0.2-overview.md | 307 | - [ ] T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T0312-9cfd | docs/dev/roadmap/v0.2-overview.md | 308 | - [ ] T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T0313-41b0 | docs/dev/roadmap/v0.2-overview.md | 309 | - [ ] T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T0314-0b12 | docs/dev/roadmap/v0.2-overview.md | 310 | - [ ] T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T0315-640a | docs/dev/roadmap/v0.2-overview.md | 311 | - [ ] T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T0316-1516 | docs/dev/roadmap/v0.2-overview.md | 312 | - [ ] T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T0317-9ec6 | docs/dev/roadmap/v0.2-overview.md | 313 | - [ ] T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T0318-a391 | docs/dev/roadmap/v0.2-overview.md | 314 | - [ ] T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T0319-991c | docs/dev/roadmap/v0.2-overview.md | 315 | - [ ] T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T0320-5b39 | docs/dev/roadmap/v0.2-overview.md | 316 | - [ ] T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T0321-4526 | docs/dev/roadmap/v0.2-overview.md | 317 | - [ ] T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T0322-39ab | docs/dev/roadmap/v0.2-overview.md | 318 | - [ ] T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T0323-0b47 | docs/dev/roadmap/v0.2-overview.md | 319 | - [ ] T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T0324-4cb0 | docs/dev/roadmap/v0.2-overview.md | 320 | - [ ] T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T0325-9818 | docs/dev/roadmap/v0.2-overview.md | 321 | - [ ] T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T0326-e1ad | docs/dev/roadmap/v0.2-overview.md | 322 | - [ ] T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T0327-9936 | docs/dev/roadmap/v0.2-overview.md | 323 | - [ ] T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T0328-e569 | docs/dev/roadmap/v0.2-overview.md | 324 | - [ ] T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T0329-58a8 | docs/dev/roadmap/v0.2-overview.md | 325 | - [ ] T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T0330-dfa0 | docs/dev/roadmap/v0.2-overview.md | 326 | - [ ] T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T0331-5799 | docs/dev/roadmap/v0.2-overview.md | 327 | - [ ] T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T0332-4485 | docs/dev/roadmap/v0.2-overview.md | 328 | - [ ] T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T0333-d0f6 | docs/dev/roadmap/v0.2-overview.md | 329 | - [ ] T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T0334-ff96 | docs/dev/roadmap/v0.2-overview.md | 330 | - [ ] T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T0335-9703 | docs/dev/roadmap/v0.2-overview.md | 331 | - [ ] T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T0336-209c | docs/dev/roadmap/v0.2-overview.md | 332 | - [ ] T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T0337-31ca | docs/dev/roadmap/v0.2-overview.md | 333 | - [ ] T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T0338-abf1 | docs/dev/roadmap/v0.2-overview.md | 334 | - [ ] T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T0339-a36a | docs/dev/roadmap/v0.2-overview.md | 335 | - [ ] T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T0340-bb3f | docs/dev/roadmap/v0.2-overview.md | 336 | - [ ] T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T0341-708f | docs/dev/roadmap/v0.2-overview.md | 337 | - [ ] T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T0342-2e90 | docs/dev/roadmap/v0.2-overview.md | 338 | - [ ] T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T0343-83f7 | docs/dev/roadmap/v0.2-overview.md | 339 | - [ ] T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T0344-0793 | docs/dev/roadmap/v0.2-overview.md | 340 | - [ ] T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T0345-5dd2 | docs/dev/roadmap/v0.2-overview.md | 341 | - [ ] T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T0346-9ce8 | docs/dev/roadmap/v0.2-overview.md | 342 | - [ ] T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T0347-957c | docs/dev/roadmap/v0.2-overview.md | 343 | - [ ] T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T0348-d289 | docs/dev/roadmap/v0.2-overview.md | 344 | - [ ] T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T0349-36b6 | docs/dev/roadmap/v0.2-overview.md | 345 | - [ ] T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T0350-2797 | docs/dev/roadmap/v0.2-overview.md | 346 | - [ ] T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T0351-00bb | docs/dev/roadmap/v0.2-overview.md | 347 | - [ ] T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T0352-f33d | docs/dev/roadmap/v0.2-overview.md | 348 | - [ ] T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T0353-fa4f | docs/dev/roadmap/v0.2-overview.md | 349 | - [ ] T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T0354-eb32 | docs/dev/roadmap/v0.2-overview.md | 350 | - [ ] T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T0355-df06 | docs/dev/roadmap/v0.2-overview.md | 351 | - [ ] T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T0356-e364 | docs/dev/roadmap/v0.2-overview.md | 352 | - [ ] T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T0357-d372 | docs/dev/roadmap/v0.2-overview.md | 353 | - [ ] T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T0358-411f | docs/dev/roadmap/v0.2-overview.md | 354 | - [ ] T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T0359-609d | docs/dev/roadmap/v0.2-overview.md | 355 | - [ ] T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T0360-a163 | docs/dev/roadmap/v0.2-overview.md | 356 | - [ ] T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T0361-e3f7 | docs/dev/roadmap/v0.2-overview.md | 357 | - [ ] T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T0362-0fc9 | docs/dev/roadmap/v0.2-overview.md | 358 | - [ ] T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T0363-7e62 | docs/dev/roadmap/v0.2-overview.md | 359 | - [ ] T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T0364-c662 | docs/dev/roadmap/v0.2-overview.md | 360 | - [ ] T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T0365-c8a1 | docs/dev/roadmap/v0.2-overview.md | 361 | - [ ] T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T0366-fb89 | docs/dev/roadmap/v0.2-overview.md | 362 | - [ ] T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T0367-f414 | docs/dev/roadmap/v0.2-overview.md | 363 | - [ ] T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T0368-c9f9 | docs/dev/roadmap/v0.2-overview.md | 364 | - [ ] T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T0369-b47d | docs/dev/roadmap/v0.2-overview.md | 365 | - [ ] T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T0370-8b59 | docs/dev/roadmap/v0.2-overview.md | 366 | - [ ] T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T0371-c576 | docs/dev/roadmap/v0.2-overview.md | 367 | - [ ] T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T0372-25d0 | docs/dev/roadmap/v0.2-overview.md | 368 | - [ ] T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T0373-ee91 | docs/dev/roadmap/v0.2-overview.md | 369 | - [ ] T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T0374-48e9 | docs/dev/roadmap/v0.2-overview.md | 370 | - [ ] T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T0375-bc2b | docs/dev/roadmap/v0.2-overview.md | 371 | - [ ] T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T0376-1026 | docs/dev/roadmap/v0.2-overview.md | 372 | - [ ] T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T0377-6445 | docs/dev/roadmap/v0.2-overview.md | 373 | - [ ] T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T0378-9d1f | docs/dev/roadmap/v0.2-overview.md | 374 | - [ ] T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T0379-8488 | docs/dev/roadmap/v0.2-overview.md | 375 | - [ ] T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T0380-bb04 | docs/dev/roadmap/v0.2-overview.md | 376 | - [ ] T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T0381-9815 | docs/dev/roadmap/v0.2-overview.md | 377 | - [ ] T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T0382-36f3 | docs/dev/roadmap/v0.2-overview.md | 378 | - [ ] T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T0383-dbc9 | docs/dev/roadmap/v0.2-overview.md | 379 | - [ ] T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T0384-eb3f | docs/dev/roadmap/v0.2-overview.md | 380 | - [ ] T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T0385-ec08 | docs/dev/roadmap/v0.2-overview.md | 381 | - [ ] T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T0386-5337 | docs/dev/roadmap/v0.2-overview.md | 382 | - [ ] T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T0387-294c | docs/dev/roadmap/v0.2-overview.md | 383 | - [ ] T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T0388-ac9f | docs/dev/roadmap/v0.2-overview.md | 384 | - [ ] T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T0389-87f9 | docs/dev/roadmap/v0.2-overview.md | 385 | - [ ] T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T0390-b2f6 | docs/dev/roadmap/v0.2-overview.md | 386 | - [ ] T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T0391-5af2 | docs/dev/roadmap/v0.2-overview.md | 387 | - [ ] T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T0392-b5f9 | docs/dev/roadmap/v0.2-overview.md | 388 | - [ ] T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T0393-f9f9 | docs/dev/roadmap/v0.2-overview.md | 389 | - [ ] T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T0394-5750 | docs/dev/roadmap/v0.2-overview.md | 390 | - [ ] T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T0395-617a | docs/dev/roadmap/v0.2-overview.md | 391 | - [ ] T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T0396-1b6b | docs/dev/roadmap/v0.2-overview.md | 392 | - [ ] T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T0397-42f6 | docs/dev/roadmap/v0.2-overview.md | 393 | - [ ] T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T0398-c5e5 | docs/dev/roadmap/v0.2-overview.md | 394 | - [ ] T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T0399-8f5a | docs/dev/roadmap/v0.2-overview.md | 395 | - [ ] T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T0400-9dd2 | docs/dev/roadmap/v0.2-overview.md | 396 | - [ ] T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T0401-3c46 | docs/dev/roadmap/v0.2-overview.md | 397 | - [ ] T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T0402-4454 | docs/dev/roadmap/v0.2-overview.md | 398 | - [ ] T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T0403-147a | docs/dev/roadmap/v0.2-overview.md | 399 | - [ ] T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T0404-9c10 | docs/dev/roadmap/v0.2-overview.md | 400 | - [ ] T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T0405-2e18 | docs/dev/roadmap/v0.2-overview.md | 401 | - [ ] T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T0406-3617 | docs/dev/roadmap/v0.2-overview.md | 402 | - [ ] T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T0407-10b9 | docs/dev/roadmap/v0.2-overview.md | 403 | - [ ] T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T0408-00c0 | docs/dev/roadmap/v0.2-overview.md | 404 | - [ ] T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T0409-13fe | docs/dev/roadmap/v0.2-overview.md | 405 | - [ ] T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T0410-8137 | docs/dev/roadmap/v0.2-overview.md | 406 | - [ ] T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T0411-9f65 | docs/dev/roadmap/v0.2-overview.md | 407 | - [ ] T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T0412-285e | docs/dev/roadmap/v0.2-overview.md | 408 | - [ ] T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T0413-50d0 | docs/dev/roadmap/v0.2-overview.md | 409 | - [ ] T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T0414-a18e | docs/dev/roadmap/v0.2-overview.md | 410 | - [ ] T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T0415-8a8a | docs/dev/roadmap/v0.2-overview.md | 411 | - [ ] T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T0416-45d6 | docs/dev/roadmap/v0.2-overview.md | 412 | - [ ] T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T0417-2e67 | docs/dev/roadmap/v0.2-overview.md | 413 | - [ ] T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T0418-7a82 | docs/dev/roadmap/v0.2-overview.md | 414 | - [ ] T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T0419-8a3a | docs/dev/roadmap/v0.2-overview.md | 415 | - [ ] T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T0420-9453 | docs/dev/roadmap/v0.2-overview.md | 416 | - [ ] T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T0421-32d2 | docs/dev/roadmap/v0.2-overview.md | 417 | - [ ] T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T0422-fd2c | docs/dev/roadmap/v0.2-overview.md | 418 | - [ ] T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T0423-6119 | docs/dev/roadmap/v0.2-overview.md | 419 | - [ ] T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T0424-851a | docs/dev/roadmap/v0.2-overview.md | 420 | - [ ] T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T0425-b2e3 | docs/dev/roadmap/v0.2-overview.md | 421 | - [ ] T0107-c900 T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.2-overview.md:103) |
| T0426-c2ec | docs/dev/roadmap/v0.2-overview.md | 422 | - [ ] T0108-993d T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.2-overview.md:104) |
| T0427-aabd | docs/dev/roadmap/v0.2-overview.md | 423 | - [ ] T0109-a50e T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.2-overview.md:105) |
| T0428-ad50 | docs/dev/roadmap/v0.2-overview.md | 424 | - [ ] T0110-aa9c T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.2-overview.md:106) |
| T0429-44d8 | docs/dev/roadmap/v0.2-overview.md | 425 | - [ ] T0111-029c T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.2-overview.md:107) |
| T0430-0771 | docs/dev/roadmap/v0.2-overview.md | 426 | - [ ] T0112-f95d T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.2-overview.md:108) |
| T0431-283b | docs/dev/roadmap/v0.2-overview.md | 427 | - [ ] T0113-9052 T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:109) |
| T0432-9acd | docs/dev/roadmap/v0.2-overview.md | 428 | - [ ] T0114-73c9 T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:110) |
| T0433-3ab9 | docs/dev/roadmap/v0.2-overview.md | 429 | - [ ] T0115-4d3f T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:111) |
| T0434-52a0 | docs/dev/roadmap/v0.2-overview.md | 430 | - [ ] T0116-07a6 T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:112) |
| T0435-b317 | docs/dev/roadmap/v0.2-overview.md | 431 | - [ ] T0117-4b6d T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:113) |
| T0436-b860 | docs/dev/roadmap/v0.2-overview.md | 432 | - [ ] T0118-0eb7 T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:114) |
| T0437-da11 | docs/dev/roadmap/v0.2-overview.md | 433 | - [ ] T0119-bf23 T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:115) |
| T0438-60c8 | docs/dev/roadmap/v0.2-overview.md | 434 | - [ ] T0120-e436 T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:116) |
| T0439-d5c5 | docs/dev/roadmap/v0.2-overview.md | 435 | - [ ] T0121-23d3 T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:117) |
| T0440-3e89 | docs/dev/roadmap/v0.2-overview.md | 436 | - [ ] T0122-d79e T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:118) |
| T0441-dd87 | docs/dev/roadmap/v0.2-overview.md | 437 | - [ ] T0123-17bb T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:119) |
| T0442-d13f | docs/dev/roadmap/v0.2-overview.md | 438 | - [ ] T0124-6fe0 T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:120) |
| T0443-c2b1 | docs/dev/roadmap/v0.2-overview.md | 439 | - [ ] T0125-9422 T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:121) |
| T0444-1eda | docs/dev/roadmap/v0.2-overview.md | 440 | - [ ] T0126-1648 T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:122) |
| T0445-56c0 | docs/dev/roadmap/v0.2-overview.md | 441 | - [ ] T0127-04d4 T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:123) |
| T0446-77a4 | docs/dev/roadmap/v0.2-overview.md | 442 | - [ ] T0128-504c T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:124) |
| T0447-7c01 | docs/dev/roadmap/v0.2-overview.md | 443 | - [ ] T0129-8642 T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:125) |
| T0448-827d | docs/dev/roadmap/v0.2-overview.md | 444 | - [ ] T0130-8ea1 T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:126) |
| T0449-030b | docs/dev/roadmap/v0.2-overview.md | 445 | - [ ] T0131-4396 T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:127) |
| T0450-25a2 | docs/dev/roadmap/v0.2-overview.md | 446 | - [ ] T0132-f8e4 T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:128) |
| T0451-641a | docs/dev/roadmap/v0.2-overview.md | 447 | - [ ] T0133-fa5e T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:129) |
| T0452-e68a | docs/dev/roadmap/v0.2-overview.md | 448 | - [ ] T0134-2334 T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:130) |
| T0453-ea33 | docs/dev/roadmap/v0.2-overview.md | 449 | - [ ] T0135-dfe5 T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:131) |
| T0454-951b | docs/dev/roadmap/v0.2-overview.md | 450 | - [ ] T0136-b1a3 T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:132) |
| T0455-7ccf | docs/dev/roadmap/v0.2-overview.md | 451 | - [ ] T0137-60ad T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:133) |
| T0456-956a | docs/dev/roadmap/v0.2-overview.md | 452 | - [ ] T0138-0b24 T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:134) |
| T0457-3609 | docs/dev/roadmap/v0.2-overview.md | 453 | - [ ] T0139-e439 T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:135) |
| T0458-9e54 | docs/dev/roadmap/v0.2-overview.md | 454 | - [ ] T0140-bc80 T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:136) |
| T0459-2933 | docs/dev/roadmap/v0.2-overview.md | 455 | - [ ] T0141-46b0 T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:137) |
| T0460-fffe | docs/dev/roadmap/v0.2-overview.md | 456 | - [ ] T0142-21f0 T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:138) |
| T0461-31f8 | docs/dev/roadmap/v0.2-overview.md | 457 | - [ ] T0143-6637 T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:139) |
| T0462-176d | docs/dev/roadmap/v0.2-overview.md | 458 | - [ ] T0144-203c T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:140) |
| T0463-ece0 | docs/dev/roadmap/v0.2-overview.md | 459 | - [ ] T0145-5dc5 T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:141) |
| T0464-f216 | docs/dev/roadmap/v0.2-overview.md | 460 | - [ ] T0146-10b0 T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:142) |
| T0465-12b6 | docs/dev/roadmap/v0.2-overview.md | 461 | - [ ] T0147-90e5 T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:143) |
| T0466-0530 | docs/dev/roadmap/v0.2-overview.md | 462 | - [ ] T0148-3465 T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:144) |
| T0467-89ba | docs/dev/roadmap/v0.2-overview.md | 463 | - [ ] T0149-ea22 T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:145) |
| T0468-9df9 | docs/dev/roadmap/v0.2-overview.md | 464 | - [ ] T0150-4c65 T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:146) |
| T0469-9399 | docs/dev/roadmap/v0.2-overview.md | 465 | - [ ] T0151-2fd6 T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:147) |
| T0470-8d04 | docs/dev/roadmap/v0.2-overview.md | 466 | - [ ] T0152-3de7 T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:148) |
| T0471-647f | docs/dev/roadmap/v0.2-overview.md | 467 | - [ ] T0153-1141 T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:149) |
| T0472-2f7b | docs/dev/roadmap/v0.2-overview.md | 468 | - [ ] T0154-e25b T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:150) |
| T0473-8ff9 | docs/dev/roadmap/v0.2-overview.md | 469 | - [ ] T0155-52ee T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:151) |
| T0474-38d3 | docs/dev/roadmap/v0.2-overview.md | 470 | - [ ] T0156-a970 T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:152) |
| T0475-b545 | docs/dev/roadmap/v0.2-overview.md | 471 | - [ ] T0157-eb70 T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:153) |
| T0476-f78f | docs/dev/roadmap/v0.2-overview.md | 472 | - [ ] T0158-c59f T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:154) |
| T0477-d8e1 | docs/dev/roadmap/v0.2-overview.md | 473 | - [ ] T0159-e81e T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:155) |
| T0478-9cfd | docs/dev/roadmap/v0.2-overview.md | 474 | - [ ] T0160-f48b T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:156) |
| T0479-fc68 | docs/dev/roadmap/v0.2-overview.md | 475 | - [ ] T0161-4486 T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:157) |
| T0480-6790 | docs/dev/roadmap/v0.2-overview.md | 476 | - [ ] T0162-2a68 T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:158) |
| T0481-4d10 | docs/dev/roadmap/v0.2-overview.md | 477 | - [ ] T0163-3932 T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:159) |
| T0482-c2a0 | docs/dev/roadmap/v0.2-overview.md | 478 | - [ ] T0164-a424 T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:160) |
| T0483-d3f1 | docs/dev/roadmap/v0.2-overview.md | 479 | - [ ] T0165-0267 T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:161) |
| T0484-172d | docs/dev/roadmap/v0.2-overview.md | 480 | - [ ] T0166-de78 T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:162) |
| T0485-42c9 | docs/dev/roadmap/v0.2-overview.md | 481 | - [ ] T0167-3d4f T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:163) |
| T0486-581a | docs/dev/roadmap/v0.2-overview.md | 482 | - [ ] T0168-3c90 T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:164) |
| T0487-4f5c | docs/dev/roadmap/v0.2-overview.md | 483 | - [ ] T0169-661b T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:165) |
| T0488-8fcc | docs/dev/roadmap/v0.2-overview.md | 484 | - [ ] T0170-ebca T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:166) |
| T0489-684d | docs/dev/roadmap/v0.2-overview.md | 485 | - [ ] T0171-ce42 T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:167) |
| T0490-306b | docs/dev/roadmap/v0.2-overview.md | 486 | - [ ] T0172-13c7 T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:168) |
| T0491-09ab | docs/dev/roadmap/v0.2-overview.md | 487 | - [ ] T0173-d114 T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:169) |
| T0492-88a9 | docs/dev/roadmap/v0.2-overview.md | 488 | - [ ] T0174-b7c8 T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:170) |
| T0493-df03 | docs/dev/roadmap/v0.2-overview.md | 489 | - [ ] T0175-5b1e T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:171) |
| T0494-13e2 | docs/dev/roadmap/v0.2-overview.md | 490 | - [ ] T0176-e2a0 T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:172) |
| T0495-4f75 | docs/dev/roadmap/v0.2-overview.md | 491 | - [ ] T0177-b641 T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:173) |
| T0496-ce72 | docs/dev/roadmap/v0.2-overview.md | 492 | - [ ] T0178-644e T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:174) |
| T0497-1f67 | docs/dev/roadmap/v0.2-overview.md | 493 | - [ ] T0179-60b4 T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:175) |
| T0498-e171 | docs/dev/roadmap/v0.2-overview.md | 494 | - [ ] T0180-817f T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:176) |
| T0499-2607 | docs/dev/roadmap/v0.2-overview.md | 495 | - [ ] T0181-f016 T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:177) |
| T0500-500a | docs/dev/roadmap/v0.2-overview.md | 496 | - [ ] T0182-462f T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:178) |
| T0501-fea3 | docs/dev/roadmap/v0.2-overview.md | 497 | - [ ] T0183-b7c4 T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:179) |
| T0502-a459 | docs/dev/roadmap/v0.2-overview.md | 498 | - [ ] T0184-e931 T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:180) |
| T0503-da92 | docs/dev/roadmap/v0.2-overview.md | 499 | - [ ] T0185-9d65 T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:181) |
| T0504-1a46 | docs/dev/roadmap/v0.2-overview.md | 500 | - [ ] T0186-d08d T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:182) |
| T0505-168d | docs/dev/roadmap/v0.2-overview.md | 501 | - [ ] T0187-1ae5 T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:183) |
| T0506-7171 | docs/dev/roadmap/v0.2-overview.md | 502 | - [ ] T0188-2593 T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:184) |
| T0507-48a1 | docs/dev/roadmap/v0.2-overview.md | 503 | - [ ] T0189-0db8 T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:185) |
| T0508-f03d | docs/dev/roadmap/v0.2-overview.md | 504 | - [ ] T0190-21b4 T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:186) |
| T0509-a301 | docs/dev/roadmap/v0.2-overview.md | 505 | - [ ] T0191-6abe T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:187) |
| T0510-a1ef | docs/dev/roadmap/v0.2-overview.md | 506 | - [ ] T0192-6cf6 T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:188) |
| T0511-0e38 | docs/dev/roadmap/v0.2-overview.md | 507 | - [ ] T0193-402b T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:189) |
| T0512-ba77 | docs/dev/roadmap/v0.2-overview.md | 508 | - [ ] T0194-9595 T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.2-overview.md:190) |
| T0513-d0c7 | docs/dev/roadmap/v0.2-overview.md | 509 | - [ ] T0195-dae5 T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.2-overview.md:191) |
| T0514-fed2 | docs/dev/roadmap/v0.2-overview.md | 510 | - [ ] T0196-e896 T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.2-overview.md:192) |
| T0515-9043 | docs/dev/roadmap/v0.2-overview.md | 511 | - [ ] T0197-1ee3 T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.2-overview.md:193) |
| T0516-a737 | docs/dev/roadmap/v0.2-overview.md | 512 | - [ ] T0198-06e7 T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.2-overview.md:194) |
| T0517-ece6 | docs/dev/roadmap/v0.2-overview.md | 513 | - [ ] T0199-513a T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.2-overview.md:195) |
| T0518-8e53 | docs/dev/roadmap/v0.2-overview.md | 514 | - [ ] T0200-28c4 T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.2-overview.md:196) |
| T0519-87ad | docs/dev/roadmap/v0.2-overview.md | 515 | - [ ] T0201-42c3 T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.2-overview.md:197) |
| T0520-d866 | docs/dev/roadmap/v0.2-overview.md | 516 | - [ ] T0202-bd4e T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.2-overview.md:198) |
| T0521-4fed | docs/dev/roadmap/v0.2-overview.md | 517 | - [ ] T0203-495f T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.2-overview.md:199) |
| T0522-e4a1 | docs/dev/roadmap/v0.2-overview.md | 518 | - [ ] T0204-be79 T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.2-overview.md:200) |
| T0523-e070 | docs/dev/roadmap/v0.2-overview.md | 519 | - [ ] T0205-75ce T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.2-overview.md:201) |
| T0524-ffc4 | docs/dev/roadmap/v0.2-overview.md | 520 | - [ ] T0206-0fa4 T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.2-overview.md:202) |
| T0525-b394 | docs/dev/roadmap/v0.2-overview.md | 521 | - [ ] T0207-45f9 T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.2-overview.md:203) |
| T0526-d609 | docs/dev/roadmap/v0.2-overview.md | 522 | - [ ] T0208-604a T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.2-overview.md:204) |
| T0527-b1cc | docs/dev/roadmap/v0.2-overview.md | 523 | - [ ] T0209-8385 T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.2-overview.md:205) |
| T0528-4e8c | docs/dev/roadmap/v0.2-overview.md | 524 | - [ ] T0210-83e9 T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.2-overview.md:206) |
| T0529-912f | docs/dev/roadmap/v0.2-overview.md | 525 | - [ ] T0211-c2da T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.2-overview.md:207) |
| T0530-2530 | docs/dev/roadmap/v0.2-overview.md | 526 | - [ ] T0212-e321 T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.2-overview.md:208) |
| T0531-f9f3 | docs/dev/roadmap/v0.2-overview.md | 527 | - [ ] T0213-90c2 T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.2-overview.md:209) |
| T0532-2054 | docs/dev/roadmap/v0.2-overview.md | 528 | - [ ] T0214-dbb7 T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.2-overview.md:210) |
| T0533-ba4d | docs/dev/roadmap/v0.2-overview.md | 529 | - [ ] T0215-45f9 T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.2-overview.md:211) |
| T0534-ef90 | docs/dev/roadmap/v0.2-overview.md | 530 | - [ ] T0216-c57b T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.2-overview.md:212) |
| T0535-0cda | docs/dev/roadmap/v0.2-overview.md | 531 | - [ ] T0217-24e1 T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.2-overview.md:213) |
| T0536-0157 | docs/dev/roadmap/v0.2-overview.md | 532 | - [ ] T0218-68cf T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.2-overview.md:214) |
| T0537-f8e7 | docs/dev/roadmap/v0.2-overview.md | 533 | - [ ] T0219-45ed T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.2-overview.md:215) |
| T0538-4ce2 | docs/dev/roadmap/v0.2-overview.md | 534 | - [ ] T0220-6c4d T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.2-overview.md:216) |
| T0539-0d80 | docs/dev/roadmap/v0.2-overview.md | 535 | - [ ] T0221-d81b T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.2-overview.md:217) |
| T0540-9b29 | docs/dev/roadmap/v0.2-overview.md | 536 | - [ ] T0222-1afc T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.2-overview.md:218) |
| T0541-cff0 | docs/dev/roadmap/v0.2-overview.md | 537 | - [ ] T0223-cc17 T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.2-overview.md:219) |
| T0542-0d28 | docs/dev/roadmap/v0.2-overview.md | 538 | - [ ] T0224-ffd8 T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.2-overview.md:220) |
| T0543-a8f5 | docs/dev/roadmap/v0.2-overview.md | 539 | - [ ] T0225-1977 T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.2-overview.md:221) |
| T0544-3636 | docs/dev/roadmap/v0.2-overview.md | 540 | - [ ] T0226-8f55 T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.2-overview.md:222) |
| T0545-9c68 | docs/dev/roadmap/v0.2-overview.md | 541 | - [ ] T0227-1fb4 T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.2-overview.md:223) |
| T0546-53fd | docs/dev/roadmap/v0.2-overview.md | 542 | - [ ] T0228-f631 T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.2-overview.md:224) |
| T0547-3ada | docs/dev/roadmap/v0.2-overview.md | 543 | - [ ] T0229-5b09 T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.2-overview.md:225) |
| T0548-3cdd | docs/dev/roadmap/v0.2-overview.md | 544 | - [ ] T0230-0992 T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.2-overview.md:226) |
| T0549-add0 | docs/dev/roadmap/v0.2-overview.md | 545 | - [ ] T0231-2147 T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.2-overview.md:227) |
| T0550-428b | docs/dev/roadmap/v0.2-overview.md | 546 | - [ ] T0232-2c69 T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.2-overview.md:228) |
| T0551-7b12 | docs/dev/roadmap/v0.2-overview.md | 547 | - [ ] T0233-f8fe T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.2-overview.md:229) |
| T0552-a1d1 | docs/dev/roadmap/v0.2-overview.md | 548 | - [ ] T0234-c938 T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.2-overview.md:230) |
| T0553-7697 | docs/dev/roadmap/v0.2-overview.md | 549 | - [ ] T0235-6a56 T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.2-overview.md:231) |
| T0554-4333 | docs/dev/roadmap/v0.2-overview.md | 550 | - [ ] T0236-b0d4 T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.2-overview.md:232) |
| T0555-aef3 | docs/dev/roadmap/v0.2-overview.md | 551 | - [ ] T0237-7052 T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.2-overview.md:233) |
| T0556-39b5 | docs/dev/roadmap/v0.2-overview.md | 552 | - [ ] T0238-fa2f T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.2-overview.md:234) |
| T0557-ebd7 | docs/dev/roadmap/v0.2-overview.md | 553 | - [ ] T0239-3b7d T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.2-overview.md:235) |
| T0558-f101 | docs/dev/roadmap/v0.2-overview.md | 554 | - [ ] T0240-d830 T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.2-overview.md:236) |
| T0559-e4da | docs/dev/roadmap/v0.2-overview.md | 555 | - [ ] T0241-c27f T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.2-overview.md:237) |
| T0560-6aea | docs/dev/roadmap/v0.2-overview.md | 556 | - [ ] T0242-9665 T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.2-overview.md:238) |
| T0561-26ea | docs/dev/roadmap/v0.2-overview.md | 557 | - [ ] T0243-9fbd T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.2-overview.md:239) |
| T0562-02fa | docs/dev/roadmap/v0.2-overview.md | 558 | - [ ] T0244-40aa T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.2-overview.md:240) |
| T0563-7eec | docs/dev/roadmap/v0.2-overview.md | 559 | - [ ] T0245-6f20 T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.2-overview.md:241) |
| T0564-3b0e | docs/dev/roadmap/v0.2-overview.md | 560 | - [ ] T0246-a197 T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.2-overview.md:242) |
| T0565-f1c0 | docs/dev/roadmap/v0.2-overview.md | 561 | - [ ] T0247-096c T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.2-overview.md:243) |
| T0566-f2f8 | docs/dev/roadmap/v0.2-overview.md | 562 | - [ ] T0248-fd6c T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:244) |
| T0567-0f91 | docs/dev/roadmap/v0.2-overview.md | 563 | - [ ] T0249-6364 T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:245) |
| T0568-7b04 | docs/dev/roadmap/v0.2-overview.md | 564 | - [ ] T0250-07e7 T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:246) |
| T0569-5aa8 | docs/dev/roadmap/v0.2-overview.md | 565 | - [ ] T0251-6d34 T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:247) |
| T0570-77c2 | docs/dev/roadmap/v0.2-overview.md | 566 | - [ ] T0252-df35 T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:248) |
| T0571-cb78 | docs/dev/roadmap/v0.2-overview.md | 567 | - [ ] T0253-d812 T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:249) |
| T0572-05ac | docs/dev/roadmap/v0.2-overview.md | 568 | - [ ] T0254-6215 T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:250) |
| T0573-13a7 | docs/dev/roadmap/v0.2-overview.md | 569 | - [ ] T0255-38eb T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:251) |
| T0574-5038 | docs/dev/roadmap/v0.2-overview.md | 570 | - [ ] T0256-7713 T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:252) |
| T0575-8178 | docs/dev/roadmap/v0.2-overview.md | 571 | - [ ] T0257-698e T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:253) |
| T0576-1f21 | docs/dev/roadmap/v0.2-overview.md | 572 | - [ ] T0258-6de5 T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:254) |
| T0577-1df0 | docs/dev/roadmap/v0.2-overview.md | 573 | - [ ] T0259-8bd2 T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:255) |
| T0578-d48c | docs/dev/roadmap/v0.2-overview.md | 574 | - [ ] T0260-111d T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:256) |
| T0579-2a0d | docs/dev/roadmap/v0.2-overview.md | 575 | - [ ] T0261-bb0f T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:257) |
| T0580-2df3 | docs/dev/roadmap/v0.2-overview.md | 576 | - [ ] T0262-a94d T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:258) |
| T0581-b2bb | docs/dev/roadmap/v0.2-overview.md | 577 | - [ ] T0263-2ede T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:259) |
| T0582-0a0f | docs/dev/roadmap/v0.2-overview.md | 578 | - [ ] T0264-d22a T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:260) |
| T0583-2340 | docs/dev/roadmap/v0.2-overview.md | 579 | - [ ] T0265-7d1a T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:261) |
| T0584-4cad | docs/dev/roadmap/v0.2-overview.md | 580 | - [ ] T0266-c7ab T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:262) |
| T0585-45cb | docs/dev/roadmap/v0.2-overview.md | 581 | - [ ] T0267-0cf5 T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:263) |
| T0586-0a76 | docs/dev/roadmap/v0.2-overview.md | 582 | - [ ] T0268-8bdd T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:264) |
| T0587-9e75 | docs/dev/roadmap/v0.2-overview.md | 583 | - [ ] T0269-09d0 T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:265) |
| T0588-c0bf | docs/dev/roadmap/v0.2-overview.md | 584 | - [ ] T0270-0a32 T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:266) |
| T0589-e9ba | docs/dev/roadmap/v0.2-overview.md | 585 | - [ ] T0271-4601 T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:267) |
| T0590-495d | docs/dev/roadmap/v0.2-overview.md | 586 | - [ ] T0272-547e T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:268) |
| T0591-b336 | docs/dev/roadmap/v0.2-overview.md | 587 | - [ ] T0273-4c9f T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:269) |
| T0592-bdcc | docs/dev/roadmap/v0.2-overview.md | 588 | - [ ] T0274-2185 T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:270) |
| T0593-a8fc | docs/dev/roadmap/v0.2-overview.md | 589 | - [ ] T0275-8ba6 T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:271) |
| T0594-c96b | docs/dev/roadmap/v0.2-overview.md | 590 | - [ ] T0276-0886 T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:272) |
| T0595-5d58 | docs/dev/roadmap/v0.2-overview.md | 591 | - [ ] T0277-9b3c T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:273) |
| T0596-a282 | docs/dev/roadmap/v0.2-overview.md | 592 | - [ ] T0278-8770 T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:274) |
| T0597-d285 | docs/dev/roadmap/v0.2-overview.md | 593 | - [ ] T0279-65a3 T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:275) |
| T0598-5354 | docs/dev/roadmap/v0.2-overview.md | 594 | - [ ] T0280-59b1 T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:276) |
| T0599-37c2 | docs/dev/roadmap/v0.2-overview.md | 595 | - [ ] T0281-404e T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:277) |
| T0600-e3cf | docs/dev/roadmap/v0.2-overview.md | 596 | - [ ] T0282-faf0 T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:278) |
| T0601-95b0 | docs/dev/roadmap/v0.2-overview.md | 597 | - [ ] T0283-87f9 T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:279) |
| T0602-d274 | docs/dev/roadmap/v0.2-overview.md | 598 | - [ ] T0284-1140 T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:280) |
| T0603-3dea | docs/dev/roadmap/v0.2-overview.md | 599 | - [ ] T0285-d98b T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:281) |
| T0604-696d | docs/dev/roadmap/v0.2-overview.md | 600 | - [ ] T0286-016a T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:282) |
| T0605-2e3f | docs/dev/roadmap/v0.2-overview.md | 601 | - [ ] T0287-db81 T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:283) |
| T0606-4e7b | docs/dev/roadmap/v0.2-overview.md | 602 | - [ ] T0288-2f06 T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:284) |
| T0607-1c9e | docs/dev/roadmap/v0.2-overview.md | 603 | - [ ] T0289-665f T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:285) |
| T0608-629c | docs/dev/roadmap/v0.2-overview.md | 604 | - [ ] T0290-cae7 T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:286) |
| T0609-05f7 | docs/dev/roadmap/v0.2-overview.md | 605 | - [ ] T0291-77df T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:287) |
| T0610-879a | docs/dev/roadmap/v0.2-overview.md | 606 | - [ ] T0292-effb T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:288) |
| T0611-25f7 | docs/dev/roadmap/v0.2-overview.md | 607 | - [ ] T0293-5185 T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:289) |
| T0612-6112 | docs/dev/roadmap/v0.2-overview.md | 608 | - [ ] T0294-db1c T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:290) |
| T0613-b6fd | docs/dev/roadmap/v0.2-overview.md | 609 | - [ ] T0295-a73a T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:291) |
| T0614-e2cf | docs/dev/roadmap/v0.2-overview.md | 610 | - [ ] T0296-6ded T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:292) |
| T0615-41c4 | docs/dev/roadmap/v0.2-overview.md | 611 | - [ ] T0297-c86b T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:293) |
| T0616-5759 | docs/dev/roadmap/v0.2-overview.md | 612 | - [ ] T0298-5be9 T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:294) |
| T0617-391e | docs/dev/roadmap/v0.2-overview.md | 613 | - [ ] T0299-5adc T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:295) |
| T0618-8620 | docs/dev/roadmap/v0.2-overview.md | 614 | - [ ] T0300-ceff T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:296) |
| T0619-ed18 | docs/dev/roadmap/v0.2-overview.md | 615 | - [ ] T0301-0486 T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:297) |
| T0620-5360 | docs/dev/roadmap/v0.2-overview.md | 616 | - [ ] T0302-ea26 T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:298) |
| T0621-1a4d | docs/dev/roadmap/v0.2-overview.md | 617 | - [ ] T0303-004d T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:299) |
| T0622-dcef | docs/dev/roadmap/v0.2-overview.md | 618 | - [ ] T0304-0dc1 T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:300) |
| T0623-2a43 | docs/dev/roadmap/v0.2-overview.md | 619 | - [ ] T0305-adc8 T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:301) |
| T0624-71fc | docs/dev/roadmap/v0.2-overview.md | 620 | - [ ] T0306-48eb T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:302) |
| T0625-0cd0 | docs/dev/roadmap/v0.2-overview.md | 621 | - [ ] T0307-5ed6 T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:303) |
| T0626-fb6c | docs/dev/roadmap/v0.2-overview.md | 622 | - [ ] T0308-d86f T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:304) |
| T0627-f25c | docs/dev/roadmap/v0.2-overview.md | 623 | - [ ] T0309-8393 T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:305) |
| T0628-2f6a | docs/dev/roadmap/v0.2-overview.md | 624 | - [ ] T0310-8d04 T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:306) |
| T0629-e4bd | docs/dev/roadmap/v0.2-overview.md | 625 | - [ ] T0311-a424 T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:307) |
| T0630-3a38 | docs/dev/roadmap/v0.2-overview.md | 626 | - [ ] T0312-9cfd T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:308) |
| T0631-7afe | docs/dev/roadmap/v0.2-overview.md | 627 | - [ ] T0313-41b0 T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:309) |
| T0632-95d6 | docs/dev/roadmap/v0.2-overview.md | 628 | - [ ] T0314-0b12 T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:310) |
| T0633-0504 | docs/dev/roadmap/v0.2-overview.md | 629 | - [ ] T0315-640a T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:311) |
| T0634-4c2e | docs/dev/roadmap/v0.2-overview.md | 630 | - [ ] T0316-1516 T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:312) |
| T0635-8571 | docs/dev/roadmap/v0.2-overview.md | 631 | - [ ] T0317-9ec6 T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:313) |
| T0636-50a5 | docs/dev/roadmap/v0.2-overview.md | 632 | - [ ] T0318-a391 T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:314) |
| T0637-f3b3 | docs/dev/roadmap/v0.2-overview.md | 633 | - [ ] T0319-991c T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:315) |
| T0638-852b | docs/dev/roadmap/v0.2-overview.md | 634 | - [ ] T0320-5b39 T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.2-overview.md:316) |
| T0639-c457 | docs/dev/roadmap/v0.2-overview.md | 635 | - [ ] T0321-4526 T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.2-overview.md:317) |
| T0640-04a6 | docs/dev/roadmap/v0.2-overview.md | 636 | - [ ] T0322-39ab T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:318) |
| T0641-39e8 | docs/dev/roadmap/v0.2-overview.md | 637 | - [ ] T0323-0b47 T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:319) |
| T0642-06e0 | docs/dev/roadmap/v0.2-overview.md | 638 | - [ ] T0324-4cb0 T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:320) |
| T0643-7a79 | docs/dev/roadmap/v0.2-overview.md | 639 | - [ ] T0325-9818 T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:321) |
| T0644-92c0 | docs/dev/roadmap/v0.2-overview.md | 640 | - [ ] T0326-e1ad T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:322) |
| T0645-12e9 | docs/dev/roadmap/v0.2-overview.md | 641 | - [ ] T0327-9936 T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:323) |
| T0646-f373 | docs/dev/roadmap/v0.2-overview.md | 642 | - [ ] T0328-e569 T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:324) |
| T0647-0fc0 | docs/dev/roadmap/v0.2-overview.md | 643 | - [ ] T0329-58a8 T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:325) |
| T0648-3520 | docs/dev/roadmap/v0.2-overview.md | 644 | - [ ] T0330-dfa0 T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:326) |
| T0649-d70a | docs/dev/roadmap/v0.2-overview.md | 645 | - [ ] T0331-5799 T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.2-overview.md:327) |
| T0650-7cc0 | docs/dev/roadmap/v0.2-overview.md | 646 | - [ ] T0332-4485 T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.2-overview.md:328) |
| T0651-f63c | docs/dev/roadmap/v0.2-overview.md | 647 | - [ ] T0333-d0f6 T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.2-overview.md:329) |
| T0652-6ab8 | docs/dev/roadmap/v0.2-overview.md | 648 | - [ ] T0334-ff96 T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.2-overview.md:330) |
| T0653-3826 | docs/dev/roadmap/v0.2-overview.md | 649 | - [ ] T0335-9703 T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.2-overview.md:331) |
| T0654-ff35 | docs/dev/roadmap/v0.2-overview.md | 650 | - [ ] T0336-209c T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.2-overview.md:332) |
| T0655-b47f | docs/dev/roadmap/v0.2-overview.md | 651 | - [ ] T0337-31ca T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.2-overview.md:333) |
| T0656-a285 | docs/dev/roadmap/v0.2-overview.md | 652 | - [ ] T0338-abf1 T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.2-overview.md:334) |
| T0657-e8ad | docs/dev/roadmap/v0.2-overview.md | 653 | - [ ] T0339-a36a T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.2-overview.md:335) |
| T0658-c734 | docs/dev/roadmap/v0.2-overview.md | 654 | - [ ] T0340-bb3f T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.2-overview.md:336) |
| T0659-3286 | docs/dev/roadmap/v0.2-overview.md | 655 | - [ ] T0341-708f T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.2-overview.md:337) |
| T0660-0afb | docs/dev/roadmap/v0.2-overview.md | 656 | - [ ] T0342-2e90 T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.2-overview.md:338) |
| T0661-68b3 | docs/dev/roadmap/v0.2-overview.md | 657 | - [ ] T0343-83f7 T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.2-overview.md:339) |
| T0662-aa6d | docs/dev/roadmap/v0.2-overview.md | 658 | - [ ] T0344-0793 T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.2-overview.md:340) |
| T0663-2657 | docs/dev/roadmap/v0.2-overview.md | 659 | - [ ] T0345-5dd2 T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.2-overview.md:341) |
| T0664-2496 | docs/dev/roadmap/v0.2-overview.md | 660 | - [ ] T0346-9ce8 T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.2-overview.md:342) |
| T0665-acb7 | docs/dev/roadmap/v0.2-overview.md | 661 | - [ ] T0347-957c T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.2-overview.md:343) |
| T0666-bd15 | docs/dev/roadmap/v0.2-overview.md | 662 | - [ ] T0348-d289 T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.2-overview.md:344) |
| T0667-8d32 | docs/dev/roadmap/v0.2-overview.md | 663 | - [ ] T0349-36b6 T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.2-overview.md:345) |
| T0668-d3cd | docs/dev/roadmap/v0.2-overview.md | 664 | - [ ] T0350-2797 T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.2-overview.md:346) |
| T0669-9765 | docs/dev/roadmap/v0.2-overview.md | 665 | - [ ] T0351-00bb T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.2-overview.md:347) |
| T0670-8df3 | docs/dev/roadmap/v0.2-overview.md | 666 | - [ ] T0352-f33d T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.2-overview.md:348) |
| T0671-6099 | docs/dev/roadmap/v0.2-overview.md | 667 | - [ ] T0353-fa4f T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.2-overview.md:349) |
| T0672-8bb9 | docs/dev/roadmap/v0.2-overview.md | 668 | - [ ] T0354-eb32 T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.2-overview.md:350) |
| T0673-ac5a | docs/dev/roadmap/v0.2-overview.md | 669 | - [ ] T0355-df06 T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.2-overview.md:351) |
| T0674-84eb | docs/dev/roadmap/v0.2-overview.md | 670 | - [ ] T0356-e364 T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.2-overview.md:352) |
| T0675-ca90 | docs/dev/roadmap/v0.2-overview.md | 671 | - [ ] T0357-d372 T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.2-overview.md:353) |
| T0676-ab0e | docs/dev/roadmap/v0.2-overview.md | 672 | - [ ] T0358-411f T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.2-overview.md:354) |
| T0677-6047 | docs/dev/roadmap/v0.2-overview.md | 673 | - [ ] T0359-609d T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.2-overview.md:355) |
| T0678-0d98 | docs/dev/roadmap/v0.2-overview.md | 674 | - [ ] T0360-a163 T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.2-overview.md:356) |
| T0679-9a3a | docs/dev/roadmap/v0.2-overview.md | 675 | - [ ] T0361-e3f7 T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.2-overview.md:357) |
| T0680-8bb5 | docs/dev/roadmap/v0.2-overview.md | 676 | - [ ] T0362-0fc9 T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.2-overview.md:358) |
| T0681-c099 | docs/dev/roadmap/v0.2-overview.md | 677 | - [ ] T0363-7e62 T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.2-overview.md:359) |
| T0682-36b8 | docs/dev/roadmap/v0.2-overview.md | 678 | - [ ] T0364-c662 T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.2-overview.md:360) |
| T0683-9db6 | docs/dev/roadmap/v0.2-overview.md | 679 | - [ ] T0365-c8a1 T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.2-overview.md:361) |
| T0684-0f1e | docs/dev/roadmap/v0.2-overview.md | 680 | - [ ] T0366-fb89 T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.2-overview.md:362) |
| T0685-03d0 | docs/dev/roadmap/v0.2-overview.md | 681 | - [ ] T0367-f414 T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.2-overview.md:363) |
| T0686-3297 | docs/dev/roadmap/v0.2-overview.md | 682 | - [ ] T0368-c9f9 T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.2-overview.md:364) |
| T0687-fa42 | docs/dev/roadmap/v0.2-overview.md | 683 | - [ ] T0369-b47d T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.2-overview.md:365) |
| T0688-fddd | docs/dev/roadmap/v0.2-overview.md | 684 | - [ ] T0370-8b59 T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.2-overview.md:366) |
| T0689-fa1d | docs/dev/roadmap/v0.2-overview.md | 685 | - [ ] T0371-c576 T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.2-overview.md:367) |
| T0690-32f5 | docs/dev/roadmap/v0.2-overview.md | 686 | - [ ] T0372-25d0 T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.2-overview.md:368) |
| T0691-b18d | docs/dev/roadmap/v0.2-overview.md | 687 | - [ ] T0373-ee91 T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.2-overview.md:369) |
| T0692-d763 | docs/dev/roadmap/v0.2-overview.md | 688 | - [ ] T0374-48e9 T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.2-overview.md:370) |
| T0693-73bb | docs/dev/roadmap/v0.2-overview.md | 689 | - [ ] T0375-bc2b T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.2-overview.md:371) |
| T0694-17d2 | docs/dev/roadmap/v0.2-overview.md | 690 | - [ ] T0376-1026 T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.2-overview.md:372) |
| T0695-4e98 | docs/dev/roadmap/v0.2-overview.md | 691 | - [ ] T0377-6445 T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.2-overview.md:373) |
| T0696-6510 | docs/dev/roadmap/v0.2-overview.md | 692 | - [ ] T0378-9d1f T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.2-overview.md:374) |
| T0697-4641 | docs/dev/roadmap/v0.2-overview.md | 693 | - [ ] T0379-8488 T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.2-overview.md:375) |
| T0698-5cae | docs/dev/roadmap/v0.2-overview.md | 694 | - [ ] T0380-bb04 T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.2-overview.md:376) |
| T0699-9fce | docs/dev/roadmap/v0.2-overview.md | 695 | - [ ] T0381-9815 T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.2-overview.md:377) |
| T0700-e220 | docs/dev/roadmap/v0.2-overview.md | 696 | - [ ] T0382-36f3 T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.2-overview.md:378) |
| T0701-414e | docs/dev/roadmap/v0.2-overview.md | 697 | - [ ] T0383-dbc9 T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.2-overview.md:379) |
| T0702-76cc | docs/dev/roadmap/v0.2-overview.md | 698 | - [ ] T0384-eb3f T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.2-overview.md:380) |
| T0703-de7d | docs/dev/roadmap/v0.2-overview.md | 699 | - [ ] T0385-ec08 T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.2-overview.md:381) |
| T0704-44d2 | docs/dev/roadmap/v0.2-overview.md | 700 | - [ ] T0386-5337 T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.2-overview.md:382) |
| T0705-0f18 | docs/dev/roadmap/v0.2-overview.md | 701 | - [ ] T0387-294c T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.2-overview.md:383) |
| T0706-269b | docs/dev/roadmap/v0.2-overview.md | 702 | - [ ] T0388-ac9f T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.2-overview.md:384) |
| T0707-48cb | docs/dev/roadmap/v0.2-overview.md | 703 | - [ ] T0389-87f9 T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.2-overview.md:385) |
| T0708-7f09 | docs/dev/roadmap/v0.2-overview.md | 704 | - [ ] T0390-b2f6 T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.2-overview.md:386) |
| T0709-7388 | docs/dev/roadmap/v0.2-overview.md | 705 | - [ ] T0391-5af2 T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.2-overview.md:387) |
| T0710-4323 | docs/dev/roadmap/v0.2-overview.md | 706 | - [ ] T0392-b5f9 T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.2-overview.md:388) |
| T0711-e944 | docs/dev/roadmap/v0.2-overview.md | 707 | - [ ] T0393-f9f9 T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.2-overview.md:389) |
| T0712-8335 | docs/dev/roadmap/v0.2-overview.md | 708 | - [ ] T0394-5750 T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.2-overview.md:390) |
| T0713-1449 | docs/dev/roadmap/v0.2-overview.md | 709 | - [ ] T0395-617a T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.2-overview.md:391) |
| T0714-2ed4 | docs/dev/roadmap/v0.2-overview.md | 710 | - [ ] T0396-1b6b T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.2-overview.md:392) |
| T0715-d889 | docs/dev/roadmap/v0.2-overview.md | 711 | - [ ] T0397-42f6 T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.2-overview.md:393) |
| T0716-55d2 | docs/dev/roadmap/v0.2-overview.md | 712 | - [ ] T0398-c5e5 T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.2-overview.md:394) |
| T0717-5484 | docs/dev/roadmap/v0.2-overview.md | 713 | - [ ] T0399-8f5a T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.2-overview.md:395) |
| T0718-29cf | docs/dev/roadmap/v0.2-overview.md | 714 | - [ ] T0400-9dd2 T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.2-overview.md:396) |
| T0719-fd01 | docs/dev/roadmap/v0.2-overview.md | 715 | - [ ] T0401-3c46 T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.2-overview.md:397) |
| T0720-81fa | docs/dev/roadmap/v0.2-overview.md | 716 | - [ ] T0402-4454 T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.2-overview.md:398) |
| T0721-a971 | docs/dev/roadmap/v0.2-overview.md | 717 | - [ ] T0403-147a T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.2-overview.md:399) |
| T0722-6259 | docs/dev/roadmap/v0.2-overview.md | 718 | - [ ] T0404-9c10 T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.2-overview.md:400) |
| T0723-2e9e | docs/dev/roadmap/v0.2-overview.md | 719 | - [ ] T0405-2e18 T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.2-overview.md:401) |
| T0724-8c3e | docs/dev/roadmap/v0.2-overview.md | 720 | - [ ] T0406-3617 T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.2-overview.md:402) |
| T0725-35b4 | docs/dev/roadmap/v0.2-overview.md | 721 | - [ ] T0407-10b9 T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.2-overview.md:403) |
| T0726-85d8 | docs/dev/roadmap/v0.2-overview.md | 722 | - [ ] T0408-00c0 T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.2-overview.md:404) |
| T0727-98fd | docs/dev/roadmap/v0.2-overview.md | 723 | - [ ] T0409-13fe T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.2-overview.md:405) |
| T0728-b8c7 | docs/dev/roadmap/v0.2-overview.md | 724 | - [ ] T0410-8137 T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.2-overview.md:406) |
| T0729-0115 | docs/dev/roadmap/v0.2-overview.md | 725 | - [ ] T0411-9f65 T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.2-overview.md:407) |
| T0730-21a0 | docs/dev/roadmap/v0.2-overview.md | 726 | - [ ] T0412-285e T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.2-overview.md:408) |
| T0731-c433 | docs/dev/roadmap/v0.2-overview.md | 727 | - [ ] T0413-50d0 T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.2-overview.md:409) |
| T0732-216c | docs/dev/roadmap/v0.2-overview.md | 728 | - [ ] T0414-a18e T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.2-overview.md:410) |
| T0733-5687 | docs/dev/roadmap/v0.2-overview.md | 729 | - [ ] T0415-8a8a T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.2-overview.md:411) |
| T0734-fe81 | docs/dev/roadmap/v0.2-overview.md | 730 | - [ ] T0416-45d6 T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.2-overview.md:412) |
| T0735-a5f8 | docs/dev/roadmap/v0.2-overview.md | 731 | - [ ] T0417-2e67 T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.2-overview.md:413) |
| T0736-b3d2 | docs/dev/roadmap/v0.2-overview.md | 732 | - [ ] T0418-7a82 T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.2-overview.md:414) |
| T0737-11d6 | docs/dev/roadmap/v0.2-overview.md | 733 | - [ ] T0419-8a3a T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.2-overview.md:415) |
| T0738-71c2 | docs/dev/roadmap/v0.2-overview.md | 734 | - [ ] T0420-9453 T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.2-overview.md:416) |
| T0739-bcdc | docs/dev/roadmap/v0.2-overview.md | 735 | - [ ] T0421-32d2 T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.2-overview.md:417) |
| T0740-9a33 | docs/dev/roadmap/v0.2-overview.md | 736 | - [ ] T0422-fd2c T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.2-overview.md:418) |
| T0741-b140 | docs/dev/roadmap/v0.2-overview.md | 737 | - [ ] T0423-6119 T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.2-overview.md:419) |
| T0742-a269 | docs/dev/roadmap/v0.2-overview.md | 738 | - [ ] T0424-851a T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.2-overview.md:420) |
| T0743-8949 | docs/dev/roadmap/v0.2-overview.md | 739 | - [ ] T0842-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T0744-2c39 | docs/dev/roadmap/v0.2-overview.md | 740 | - [ ] T0843-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T0745-f706 | docs/dev/roadmap/v0.2-overview.md | 741 | - [ ] T0844-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T0746-ed76 | docs/dev/roadmap/v0.2-overview.md | 742 | - [ ] T0845-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T0747-b343 | docs/dev/roadmap/v0.2-overview.md | 743 | - [ ] T0846-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T0748-192d | docs/dev/roadmap/v0.2-overview.md | 744 | - [ ] T0847-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T0749-a813 | docs/dev/roadmap/v0.2-overview.md | 745 | - [ ] T0848-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T0750-83e3 | docs/dev/roadmap/v0.2-overview.md | 746 | - [ ] T0849-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T0751-cfee | docs/dev/roadmap/v0.2-overview.md | 747 | - [ ] T0850-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T0752-71ac | docs/dev/roadmap/v0.2-overview.md | 748 | - [ ] T0851-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T0753-edb6 | docs/dev/roadmap/v0.2-overview.md | 749 | - [ ] T0852-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T0754-7f5e | docs/dev/roadmap/v0.2-overview.md | 750 | - [ ] T0853-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T0755-795c | docs/dev/roadmap/v0.2-overview.md | 751 | - [ ] T0854-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T0756-eff7 | docs/dev/roadmap/v0.2-overview.md | 752 | - [ ] T0855-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T0757-fa0a | docs/dev/roadmap/v0.2-overview.md | 753 | - [ ] T0856-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T0758-433d | docs/dev/roadmap/v0.2-overview.md | 754 | - [ ] T0857-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T0759-32cf | docs/dev/roadmap/v0.2-overview.md | 755 | - [ ] T0858-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T0760-7ca6 | docs/dev/roadmap/v0.2-overview.md | 756 | - [ ] T0859-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T0761-ea46 | docs/dev/roadmap/v0.2-overview.md | 757 | - [ ] T0860-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T0762-fbcd | docs/dev/roadmap/v0.2-overview.md | 758 | - [ ] T0861-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T0763-94e0 | docs/dev/roadmap/v0.2-overview.md | 759 | - [ ] T0862-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T0764-6d72 | docs/dev/roadmap/v0.2-overview.md | 760 | - [ ] T0863-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T0765-4d33 | docs/dev/roadmap/v0.2-overview.md | 761 | - [ ] T0864-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T0766-2f2f | docs/dev/roadmap/v0.2-overview.md | 762 | - [ ] T0865-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T0767-add9 | docs/dev/roadmap/v0.2-overview.md | 763 | - [ ] T0866-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T0768-c70d | docs/dev/roadmap/v0.2-overview.md | 764 | - [ ] T0867-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T0769-401c | docs/dev/roadmap/v0.2-overview.md | 765 | - [ ] T0868-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T0770-5eff | docs/dev/roadmap/v0.2-overview.md | 766 | - [ ] T0869-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T0771-9bec | docs/dev/roadmap/v0.2-overview.md | 767 | - [ ] T0870-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T0772-e847 | docs/dev/roadmap/v0.2-overview.md | 768 | - [ ] T0871-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T0773-99a0 | docs/dev/roadmap/v0.2-overview.md | 769 | - [ ] T0872-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T0774-7600 | docs/dev/roadmap/v0.2-overview.md | 770 | - [ ] T0873-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T0775-77f0 | docs/dev/roadmap/v0.2-overview.md | 771 | - [ ] T0874-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T0776-e32b | docs/dev/roadmap/v0.2-overview.md | 772 | - [ ] T0875-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T0777-aec5 | docs/dev/roadmap/v0.2-overview.md | 773 | - [ ] T0876-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T0778-303a | docs/dev/roadmap/v0.2-overview.md | 774 | - [ ] T0877-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T0779-b81c | docs/dev/roadmap/v0.2-overview.md | 775 | - [ ] T0878-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T0780-53af | docs/dev/roadmap/v0.2-overview.md | 776 | - [ ] T0879-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T0781-f044 | docs/dev/roadmap/v0.2-overview.md | 777 | - [ ] T0880-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T0782-67e2 | docs/dev/roadmap/v0.2-overview.md | 778 | - [ ] T0881-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T0783-b62a | docs/dev/roadmap/v0.2-overview.md | 779 | - [ ] T0882-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T0784-72e5 | docs/dev/roadmap/v0.2-overview.md | 780 | - [ ] T0883-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T0785-d364 | docs/dev/roadmap/v0.2-overview.md | 781 | - [ ] T0884-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T0786-94b0 | docs/dev/roadmap/v0.2-overview.md | 782 | - [ ] T0885-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T0787-0b29 | docs/dev/roadmap/v0.2-overview.md | 783 | - [ ] T0886-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T0788-bbe3 | docs/dev/roadmap/v0.2-overview.md | 784 | - [ ] T0887-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T0789-8248 | docs/dev/roadmap/v0.2-overview.md | 785 | - [ ] T0888-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T0790-ec7f | docs/dev/roadmap/v0.2-overview.md | 786 | - [ ] T0889-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T0791-62af | docs/dev/roadmap/v0.2-overview.md | 787 | - [ ] T0890-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T0792-5044 | docs/dev/roadmap/v0.2-overview.md | 788 | - [ ] T0891-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T0793-144d | docs/dev/roadmap/v0.2-overview.md | 789 | - [ ] T0892-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T0794-2421 | docs/dev/roadmap/v0.2-overview.md | 790 | - [ ] T0893-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T0795-f476 | docs/dev/roadmap/v0.2-overview.md | 791 | - [ ] T0894-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T0796-6ba3 | docs/dev/roadmap/v0.2-overview.md | 792 | - [ ] T0895-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T0797-2092 | docs/dev/roadmap/v0.2-overview.md | 793 | - [ ] T0896-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T0798-5c56 | docs/dev/roadmap/v0.2-overview.md | 794 | - [ ] T0898-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T0799-ae77 | docs/dev/roadmap/v0.2-overview.md | 795 | - [ ] T0899-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T0800-9eba | docs/dev/roadmap/v0.2-overview.md | 796 | - [ ] T0900-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T0801-6187 | docs/dev/roadmap/v0.2-overview.md | 797 | - [ ] T0901-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T0802-475d | docs/dev/roadmap/v0.2-overview.md | 798 | - [ ] T0902-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T0803-8d1a | docs/dev/roadmap/v0.2-overview.md | 799 | - [ ] T0903-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T0804-7a7c | docs/dev/roadmap/v0.2-overview.md | 800 | - [ ] T0904-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T0805-be30 | docs/dev/roadmap/v0.2-overview.md | 801 | - [ ] T0905-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T0806-fb9d | docs/dev/roadmap/v0.2-overview.md | 802 | - [ ] T0906-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T0807-042a | docs/dev/roadmap/v0.2-overview.md | 803 | - [ ] T0907-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T0808-73a6 | docs/dev/roadmap/v0.2-overview.md | 804 | - [ ] T0908-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T0809-9fff | docs/dev/roadmap/v0.2-overview.md | 805 | - [ ] T0909-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T0810-7aae | docs/dev/roadmap/v0.2-overview.md | 806 | - [ ] T0910-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T0811-d5e3 | docs/dev/roadmap/v0.2-overview.md | 807 | - [ ] T0911-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T0812-0fd8 | docs/dev/roadmap/v0.2-overview.md | 808 | - [ ] T0912-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T0813-ce85 | docs/dev/roadmap/v0.2-overview.md | 809 | - [ ] T0913-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T0814-90e0 | docs/dev/roadmap/v0.2-overview.md | 810 | - [ ] T0914-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T0815-9cac | docs/dev/roadmap/v0.2-overview.md | 811 | - [ ] T0915-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T0816-2ac0 | docs/dev/roadmap/v0.2-overview.md | 812 | - [ ] T0916-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T0817-08c6 | docs/dev/roadmap/v0.2-overview.md | 813 | - [ ] T0917-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T0818-8471 | docs/dev/roadmap/v0.2-overview.md | 814 | - [ ] T0918-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T0819-8e4d | docs/dev/roadmap/v0.2-overview.md | 815 | - [ ] T0919-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T0820-fff5 | docs/dev/roadmap/v0.2-overview.md | 816 | - [ ] T0920-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T0821-f6a7 | docs/dev/roadmap/v0.2-overview.md | 817 | - [ ] T0921-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T0822-69e0 | docs/dev/roadmap/v0.2-overview.md | 818 | - [ ] T0922-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T0823-1598 | docs/dev/roadmap/v0.2-overview.md | 819 | - [ ] T0923-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T0824-cfea | docs/dev/roadmap/v0.2-overview.md | 820 | - [ ] T0924-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T0825-b281 | docs/dev/roadmap/v0.2-overview.md | 821 | - [ ] T0925-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T0826-664e | docs/dev/roadmap/v0.2-overview.md | 822 | - [ ] T0926-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T0827-23bb | docs/dev/roadmap/v0.2-overview.md | 823 | - [ ] T0927-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T0828-788f | docs/dev/roadmap/v0.2-overview.md | 824 | - [ ] T0928-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T0829-ffda | docs/dev/roadmap/v0.2-overview.md | 825 | - [ ] T0929-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T0830-04c8 | docs/dev/roadmap/v0.2-overview.md | 826 | - [ ] T0930-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T0831-5586 | docs/dev/roadmap/v0.2-overview.md | 827 | - [ ] T0931-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T0832-2426 | docs/dev/roadmap/v0.2-overview.md | 828 | - [ ] T0932-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T0833-7a8a | docs/dev/roadmap/v0.2-overview.md | 829 | - [ ] T0933-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T0834-318d | docs/dev/roadmap/v0.2-overview.md | 830 | - [ ] T0934-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T0835-8f20 | docs/dev/roadmap/v0.2-overview.md | 831 | - [ ] T0935-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T0836-e854 | docs/dev/roadmap/v0.2-overview.md | 832 | - [ ] T0936-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T0837-35f9 | docs/dev/roadmap/v0.2-overview.md | 833 | - [ ] T0937-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T0838-3b5f | docs/dev/roadmap/v0.2-overview.md | 834 | - [ ] T0938-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T0839-b52a | docs/dev/roadmap/v0.2-overview.md | 835 | - [ ] T0939-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T0840-70e3 | docs/dev/roadmap/v0.2-overview.md | 836 | - [ ] T0940-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T0841-6143 | docs/dev/roadmap/v0.2-overview.md | 837 | - [ ] T0941-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T0842-5f58 | docs/dev/roadmap/v0.2-overview.md | 838 | - [ ] T0942-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T0843-dc98 | docs/dev/roadmap/v0.2-overview.md | 839 | - [ ] T0943-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T0844-97d0 | docs/dev/roadmap/v0.2-overview.md | 840 | - [ ] T0944-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T0845-7152 | docs/dev/roadmap/v0.2-overview.md | 841 | - [ ] T0945-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T0846-cd20 | docs/dev/roadmap/v0.2-overview.md | 842 | - [ ] T0946-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T0847-36b3 | docs/dev/roadmap/v0.2-overview.md | 843 | - [ ] T0947-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T0848-f5e5 | docs/dev/roadmap/v0.2-overview.md | 844 | - [ ] T0948-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T0849-9e53 | docs/dev/roadmap/v0.2-overview.md | 845 | - [ ] T0949-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T0850-c4a9 | docs/dev/roadmap/v0.2-overview.md | 846 | - [ ] T0950-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T0851-0f43 | docs/dev/roadmap/v0.2-overview.md | 847 | - [ ] T0951-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T0852-9835 | docs/dev/roadmap/v0.2-overview.md | 848 | - [ ] T0952-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T0853-a338 | docs/dev/roadmap/v0.2-overview.md | 849 | - [ ] T0953-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T0854-f1ee | docs/dev/roadmap/v0.2-overview.md | 850 | - [ ] T0954-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T0855-8dfc | docs/dev/roadmap/v0.2-overview.md | 851 | - [ ] T0955-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T0856-e9f7 | docs/dev/roadmap/v0.2-overview.md | 852 | - [ ] T0956-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T0857-42d3 | docs/dev/roadmap/v0.2-overview.md | 853 | - [ ] T0957-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T0858-4f5b | docs/dev/roadmap/v0.2-overview.md | 854 | - [ ] T0958-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T0859-c844 | docs/dev/roadmap/v0.2-overview.md | 855 | - [ ] T0959-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T0860-b7d2 | docs/dev/roadmap/v0.2-overview.md | 856 | - [ ] T0960-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T0861-8744 | docs/dev/roadmap/v0.2-overview.md | 857 | - [ ] T0961-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T0862-e2d7 | docs/dev/roadmap/v0.2-overview.md | 858 | - [ ] T0962-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T0863-5fec | docs/dev/roadmap/v0.2-overview.md | 859 | - [ ] T0963-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T0864-99bf | docs/dev/roadmap/v0.2-overview.md | 860 | - [ ] T0964-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T0865-7336 | docs/dev/roadmap/v0.2-overview.md | 861 | - [ ] T0965-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T0866-18f0 | docs/dev/roadmap/v0.2-overview.md | 862 | - [ ] T0966-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T0867-be43 | docs/dev/roadmap/v0.2-overview.md | 863 | - [ ] T0967-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T0868-54bc | docs/dev/roadmap/v0.2-overview.md | 864 | - [ ] T0968-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T0869-280d | docs/dev/roadmap/v0.2-overview.md | 865 | - [ ] T0969-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T0870-882b | docs/dev/roadmap/v0.2-overview.md | 866 | - [ ] T0970-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T0871-0e2c | docs/dev/roadmap/v0.2-overview.md | 867 | - [ ] T0971-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T0872-39c0 | docs/dev/roadmap/v0.2-overview.md | 868 | - [ ] T0972-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T0873-2ef0 | docs/dev/roadmap/v0.2-overview.md | 869 | - [ ] T0973-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T0874-3a4e | docs/dev/roadmap/v0.2-overview.md | 870 | - [ ] T0974-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T0875-ee62 | docs/dev/roadmap/v0.2-overview.md | 871 | - [ ] T0975-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T0876-96ce | docs/dev/roadmap/v0.2-overview.md | 872 | - [ ] T0977-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T0877-5c15 | docs/dev/roadmap/v0.2-overview.md | 873 | - [ ] T0978-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T0878-beda | docs/dev/roadmap/v0.2-overview.md | 874 | - [ ] T0979-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T0879-0763 | docs/dev/roadmap/v0.2-overview.md | 875 | - [ ] T0980-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T0880-b325 | docs/dev/roadmap/v0.2-overview.md | 876 | - [ ] T0981-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T0881-04d3 | docs/dev/roadmap/v0.2-overview.md | 877 | - [ ] T0982-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T0882-f598 | docs/dev/roadmap/v0.2-overview.md | 878 | - [ ] T0983-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T0883-7cac | docs/dev/roadmap/v0.2-overview.md | 879 | - [ ] T0984-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T0884-ec85 | docs/dev/roadmap/v0.2-overview.md | 880 | - [ ] T0985-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T0885-1200 | docs/dev/roadmap/v0.2-overview.md | 881 | - [ ] T0986-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T0886-e840 | docs/dev/roadmap/v0.2-overview.md | 882 | - [ ] T0987-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T0887-fcd2 | docs/dev/roadmap/v0.2-overview.md | 883 | - [ ] T0988-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T0888-5364 | docs/dev/roadmap/v0.2-overview.md | 884 | - [ ] T0989-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T0889-2d04 | docs/dev/roadmap/v0.2-overview.md | 885 | - [ ] T0990-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T0890-03c2 | docs/dev/roadmap/v0.2-overview.md | 886 | - [ ] T0991-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T0891-2f35 | docs/dev/roadmap/v0.2-overview.md | 887 | - [ ] T0992-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T0892-3625 | docs/dev/roadmap/v0.2-overview.md | 888 | - [ ] T0993-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T0893-dd15 | docs/dev/roadmap/v0.2-overview.md | 889 | - [ ] T0994-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T0894-1be9 | docs/dev/roadmap/v0.2-overview.md | 890 | - [ ] T0995-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T0895-75e1 | docs/dev/roadmap/v0.2-overview.md | 891 | - [ ] T0996-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T0896-fe80 | docs/dev/roadmap/v0.2-overview.md | 892 | - [ ] T0997-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T0897-c848 | docs/dev/roadmap/v0.2-overview.md | 893 | - [ ] T0998-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T0898-b033 | docs/dev/roadmap/v0.2-overview.md | 894 | - [ ] T0999-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T0899-232d | docs/dev/roadmap/v0.2-overview.md | 895 | - [ ] T1000-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T0900-c180 | docs/dev/roadmap/v0.2-overview.md | 896 | - [ ] T1001-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T0901-3402 | docs/dev/roadmap/v0.2-overview.md | 897 | - [ ] T1002-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T0902-b2df | docs/dev/roadmap/v0.2-overview.md | 898 | - [ ] T1003-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T0903-b5a7 | docs/dev/roadmap/v0.2-overview.md | 899 | - [ ] T1004-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T0904-a9df | docs/dev/roadmap/v0.2-overview.md | 900 | - [ ] T1005-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T0905-184a | docs/dev/roadmap/v0.2-overview.md | 901 | - [ ] T1006-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T0906-4678 | docs/dev/roadmap/v0.2-overview.md | 902 | - [ ] T1007-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T0907-981f | docs/dev/roadmap/v0.2-overview.md | 903 | - [ ] T1008-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T0908-1ff5 | docs/dev/roadmap/v0.2-overview.md | 904 | - [ ] T1009-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T0909-77f0 | docs/dev/roadmap/v0.2-overview.md | 905 | - [ ] T1010-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T0910-4a05 | docs/dev/roadmap/v0.2-overview.md | 906 | - [ ] T1011-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T0911-5bb7 | docs/dev/roadmap/v0.2-overview.md | 907 | - [ ] T1012-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T0912-db32 | docs/dev/roadmap/v0.2-overview.md | 908 | - [ ] T1013-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T0913-b5e9 | docs/dev/roadmap/v0.2-overview.md | 909 | - [ ] T1014-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T0914-7d15 | docs/dev/roadmap/v0.2-overview.md | 910 | - [ ] T1015-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T0915-0a4f | docs/dev/roadmap/v0.2-overview.md | 911 | - [ ] T1016-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T0916-f9f1 | docs/dev/roadmap/v0.2-overview.md | 912 | - [ ] T1017-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T0917-cb6b | docs/dev/roadmap/v0.2-overview.md | 913 | - [ ] T1018-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T0918-a142 | docs/dev/roadmap/v0.2-overview.md | 914 | - [ ] T1019-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T0919-ffbc | docs/dev/roadmap/v0.2-overview.md | 915 | - [ ] T1020-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T0920-e3d9 | docs/dev/roadmap/v0.2-overview.md | 916 | - [ ] T1021-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T0921-39ef | docs/dev/roadmap/v0.2-overview.md | 917 | - [ ] T1022-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T0922-1305 | docs/dev/roadmap/v0.2-overview.md | 918 | - [ ] T1023-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T0923-3683 | docs/dev/roadmap/v0.2-overview.md | 919 | - [ ] T1024-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T0924-4070 | docs/dev/roadmap/v0.2-overview.md | 920 | - [ ] T1025-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T0925-2b5a | docs/dev/roadmap/v0.2-overview.md | 921 | - [ ] T1026-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T0926-9573 | docs/dev/roadmap/v0.2-overview.md | 922 | - [ ] T1027-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T0927-76cb | docs/dev/roadmap/v0.2-overview.md | 923 | - [ ] T1028-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T0928-b052 | docs/dev/roadmap/v0.2-overview.md | 924 | - [ ] T1029-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T0929-87f2 | docs/dev/roadmap/v0.2-overview.md | 925 | - [ ] T1030-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T0930-608a | docs/dev/roadmap/v0.2-overview.md | 926 | - [ ] T1031-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T0931-8bda | docs/dev/roadmap/v0.2-overview.md | 927 | - [ ] T1032-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T0932-2431 | docs/dev/roadmap/v0.2-overview.md | 928 | - [ ] T1033-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T0933-6d77 | docs/dev/roadmap/v0.2-overview.md | 929 | - [ ] T1035-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T0934-717d | docs/dev/roadmap/v0.2-overview.md | 930 | - [ ] T1036-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T0935-984e | docs/dev/roadmap/v0.2-overview.md | 931 | - [ ] T1037-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T0936-4a59 | docs/dev/roadmap/v0.2-overview.md | 932 | - [ ] T1038-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T0937-8bfd | docs/dev/roadmap/v0.2-overview.md | 933 | - [ ] T1039-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T0938-70a5 | docs/dev/roadmap/v0.2-overview.md | 934 | - [ ] T1040-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T0939-df18 | docs/dev/roadmap/v0.2-overview.md | 935 | - [ ] T1041-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T0940-f918 | docs/dev/roadmap/v0.2-overview.md | 936 | - [ ] T1042-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T0941-0cea | docs/dev/roadmap/v0.2-overview.md | 937 | - [ ] T1043-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T0942-ddc2 | docs/dev/roadmap/v0.2-overview.md | 938 | - [ ] T1044-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T0943-81c0 | docs/dev/roadmap/v0.2-overview.md | 939 | - [ ] T1045-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T0944-ee3f | docs/dev/roadmap/v0.2-overview.md | 940 | - [ ] T1046-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T0945-735b | docs/dev/roadmap/v0.2-overview.md | 941 | - [ ] T1047-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T0946-c695 | docs/dev/roadmap/v0.2-overview.md | 942 | - [ ] T1048-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T0947-ffaa | docs/dev/roadmap/v0.2-overview.md | 943 | - [ ] T1049-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T0948-3e68 | docs/dev/roadmap/v0.2-overview.md | 944 | - [ ] T1050-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T0949-e008 | docs/dev/roadmap/v0.2-overview.md | 945 | - [ ] T1051-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T0950-196b | docs/dev/roadmap/v0.2-overview.md | 946 | - [ ] T1052-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T0951-f6f5 | docs/dev/roadmap/v0.2-overview.md | 947 | - [ ] T1053-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T0952-ebec | docs/dev/roadmap/v0.2-overview.md | 948 | - [ ] T1054-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T0953-2164 | docs/dev/roadmap/v0.2-overview.md | 949 | - [ ] T1055-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T0954-18ff | docs/dev/roadmap/v0.2-overview.md | 950 | - [ ] T1056-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T0955-47f5 | docs/dev/roadmap/v0.2-overview.md | 951 | - [ ] T1057-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T0956-9e1f | docs/dev/roadmap/v0.2-overview.md | 952 | - [ ] T1058-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T0957-9d67 | docs/dev/roadmap/v0.2-overview.md | 953 | - [ ] T1059-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T0958-8a98 | docs/dev/roadmap/v0.2-overview.md | 954 | - [ ] T1060-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T0959-b2c7 | docs/dev/roadmap/v0.2-overview.md | 955 | - [ ] T1061-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T0960-684c | docs/dev/roadmap/v0.2-overview.md | 956 | - [ ] T1062-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T0961-e6ed | docs/dev/roadmap/v0.2-overview.md | 957 | - [ ] T1063-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T0962-99c7 | docs/dev/roadmap/v0.2-overview.md | 958 | - [ ] T1064-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T0963-de25 | docs/dev/roadmap/v0.2-overview.md | 959 | - [ ] T1065-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T0964-481a | docs/dev/roadmap/v0.2-overview.md | 960 | - [ ] T1066-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T0965-b9b1 | docs/dev/roadmap/v0.2-overview.md | 961 | - [ ] T1067-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T0966-6717 | docs/dev/roadmap/v0.2-overview.md | 962 | - [ ] T1068-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T0967-02c4 | docs/dev/roadmap/v0.2-overview.md | 963 | - [ ] T1069-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T0968-802f | docs/dev/roadmap/v0.2-overview.md | 964 | - [ ] T1070-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T0969-d305 | docs/dev/roadmap/v0.2-overview.md | 965 | - [ ] T1071-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T0970-efd0 | docs/dev/roadmap/v0.2-overview.md | 966 | - [ ] T1072-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T0971-988c | docs/dev/roadmap/v0.2-overview.md | 967 | - [ ] T1073-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T0972-cc59 | docs/dev/roadmap/v0.2-overview.md | 968 | - [ ] T1074-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T0973-b971 | docs/dev/roadmap/v0.2-overview.md | 969 | - [ ] T1075-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T0974-59c8 | docs/dev/roadmap/v0.2-overview.md | 970 | - [ ] T1076-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T0975-5bf4 | docs/dev/roadmap/v0.2-overview.md | 971 | - [ ] T1077-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T0976-6f2e | docs/dev/roadmap/v0.2-overview.md | 972 | - [ ] T1078-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T0977-787f | docs/dev/roadmap/v0.2-overview.md | 973 | - [ ] T1079-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T0978-b7ae | docs/dev/roadmap/v0.2-overview.md | 974 | - [ ] T1080-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T0979-b206 | docs/dev/roadmap/v0.2-overview.md | 975 | - [ ] T1081-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T0980-5d0d | docs/dev/roadmap/v0.2-overview.md | 976 | - [ ] T1082-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T0981-cdb8 | docs/dev/roadmap/v0.2-overview.md | 977 | - [ ] T1083-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T0982-4943 | docs/dev/roadmap/v0.2-overview.md | 978 | - [ ] T1084-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T0983-d166 | docs/dev/roadmap/v0.2-overview.md | 979 | - [ ] T1085-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T0984-00b6 | docs/dev/roadmap/v0.2-overview.md | 980 | - [ ] T1086-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T0985-2c05 | docs/dev/roadmap/v0.2-overview.md | 981 | - [ ] T1087-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T0986-55f7 | docs/dev/roadmap/v0.2-overview.md | 982 | - [ ] T1088-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T0987-6800 | docs/dev/roadmap/v0.2-overview.md | 983 | - [ ] T1089-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T0988-4ff2 | docs/dev/roadmap/v0.2-overview.md | 984 | - [ ] T1090-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T0989-4419 | docs/dev/roadmap/v0.2-overview.md | 985 | - [ ] T1091-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T0990-6396 | docs/dev/roadmap/v0.2-overview.md | 986 | - [ ] T1092-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T0991-0a22 | docs/dev/roadmap/v0.2-overview.md | 987 | - [ ] T1093-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T0992-085f | docs/dev/roadmap/v0.2-overview.md | 988 | - [ ] T1094-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T0993-cc1e | docs/dev/roadmap/v0.2-overview.md | 989 | - [ ] T1095-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T0994-fddc | docs/dev/roadmap/v0.2-overview.md | 990 | - [ ] T1096-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T0995-8d91 | docs/dev/roadmap/v0.2-overview.md | 991 | - [ ] T1097-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T0996-5d8e | docs/dev/roadmap/v0.2-overview.md | 992 | - [ ] T1098-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T0997-66f8 | docs/dev/roadmap/v0.2-overview.md | 993 | - [ ] T1099-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T0998-4773 | docs/dev/roadmap/v0.2-overview.md | 994 | - [ ] T1100-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T0999-666c | docs/dev/roadmap/v0.2-overview.md | 995 | - [ ] T1101-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T1000-2001 | docs/dev/roadmap/v0.2-overview.md | 996 | - [ ] T1102-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T1001-f436 | docs/dev/roadmap/v0.2-overview.md | 997 | - [ ] T1103-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T1002-656a | docs/dev/roadmap/v0.2-overview.md | 998 | - [ ] T1104-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T1003-dd59 | docs/dev/roadmap/v0.2-overview.md | 999 | - [ ] T1105-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T1004-4ba4 | docs/dev/roadmap/v0.2-overview.md | 1000 | - [ ] T1106-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T1005-66e5 | docs/dev/roadmap/v0.2-overview.md | 1001 | - [ ] T1107-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T1006-4b31 | docs/dev/roadmap/v0.2-overview.md | 1002 | - [ ] T1108-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T1007-8f97 | docs/dev/roadmap/v0.2-overview.md | 1003 | - [ ] T1109-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T1008-d36f | docs/dev/roadmap/v0.2-overview.md | 1004 | - [ ] T1110-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T1009-6c28 | docs/dev/roadmap/v0.2-overview.md | 1005 | - [ ] T1111-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T1010-383c | docs/dev/roadmap/v0.2-overview.md | 1006 | - [ ] T1112-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T1011-3925 | docs/dev/roadmap/v0.2-overview.md | 1007 | - [ ] T1113-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T1012-fa1a | docs/dev/roadmap/v0.2-overview.md | 1008 | - [ ] T1114-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T1013-d659 | docs/dev/roadmap/v0.2-overview.md | 1009 | - [ ] T1115-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T1014-cf0f | docs/dev/roadmap/v0.2-overview.md | 1010 | - [ ] T1116-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T1015-f041 | docs/dev/roadmap/v0.2-overview.md | 1011 | - [ ] T1117-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T1016-f6c2 | docs/dev/roadmap/v0.2-overview.md | 1012 | - [ ] T1118-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T1017-4635 | docs/dev/roadmap/v0.2-overview.md | 1013 | - [ ] T1119-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T1018-f664 | docs/dev/roadmap/v0.2-overview.md | 1014 | - [ ] T1120-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T1019-d796 | docs/dev/roadmap/v0.2-overview.md | 1015 | - [ ] T1121-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T1020-c8cf | docs/dev/roadmap/v0.2-overview.md | 1016 | - [ ] T1122-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T1021-0da4 | docs/dev/roadmap/v0.2-overview.md | 1017 | - [ ] T1123-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T1022-8313 | docs/dev/roadmap/v0.2-overview.md | 1018 | - [ ] T1124-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T1023-08c4 | docs/dev/roadmap/v0.2-overview.md | 1019 | - [ ] T1125-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T1024-64e5 | docs/dev/roadmap/v0.2-overview.md | 1020 | - [ ] T1126-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T1025-fbb4 | docs/dev/roadmap/v0.2-overview.md | 1021 | - [ ] T1127-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T1026-610d | docs/dev/roadmap/v0.2-overview.md | 1022 | - [ ] T1128-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T1027-329b | docs/dev/roadmap/v0.2-overview.md | 1023 | - [ ] T1129-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T1028-15cf | docs/dev/roadmap/v0.2-overview.md | 1024 | - [ ] T1130-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T1029-4491 | docs/dev/roadmap/v0.2-overview.md | 1025 | - [ ] T1131-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T1030-789b | docs/dev/roadmap/v0.2-overview.md | 1026 | - [ ] T1132-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T1031-87ff | docs/dev/roadmap/v0.2-overview.md | 1027 | - [ ] T1133-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T1032-2426 | docs/dev/roadmap/v0.2-overview.md | 1028 | - [ ] T1134-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T1033-7f02 | docs/dev/roadmap/v0.2-overview.md | 1029 | - [ ] T1135-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T1034-7f41 | docs/dev/roadmap/v0.2-overview.md | 1030 | - [ ] T1136-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T1035-fc8b | docs/dev/roadmap/v0.2-overview.md | 1031 | - [ ] T1137-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T1036-3a27 | docs/dev/roadmap/v0.2-overview.md | 1032 | - [ ] T1138-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T1037-8d53 | docs/dev/roadmap/v0.2-overview.md | 1033 | - [ ] T1139-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T1038-2833 | docs/dev/roadmap/v0.2-overview.md | 1034 | - [ ] T1140-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T1039-304b | docs/dev/roadmap/v0.2-overview.md | 1035 | - [ ] T1141-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T1040-930c | docs/dev/roadmap/v0.2-overview.md | 1036 | - [ ] T1142-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T1041-ea84 | docs/dev/roadmap/v0.2-overview.md | 1037 | - [ ] T1143-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T1042-0a0e | docs/dev/roadmap/v0.2-overview.md | 1038 | - [ ] T1144-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T1043-f3d9 | docs/dev/roadmap/v0.2-overview.md | 1039 | - [ ] T1145-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T1044-d61b | docs/dev/roadmap/v0.2-overview.md | 1040 | - [ ] T1146-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T1045-1432 | docs/dev/roadmap/v0.2-overview.md | 1041 | - [ ] T1147-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T1046-ba47 | docs/dev/roadmap/v0.2-overview.md | 1042 | - [ ] T1148-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T1047-5f35 | docs/dev/roadmap/v0.2-overview.md | 1043 | - [ ] T1149-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T1048-db90 | docs/dev/roadmap/v0.2-overview.md | 1044 | - [ ] T1150-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T1049-3fd3 | docs/dev/roadmap/v0.2-overview.md | 1045 | - [ ] T1151-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T1050-ff08 | docs/dev/roadmap/v0.2-overview.md | 1046 | - [ ] T1152-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T1051-20cb | docs/dev/roadmap/v0.2-overview.md | 1047 | - [ ] T1153-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T1052-af9b | docs/dev/roadmap/v0.2-overview.md | 1048 | - [ ] T1154-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T1053-e604 | docs/dev/roadmap/v0.2-overview.md | 1049 | - [ ] T1155-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T1054-6800 | docs/dev/roadmap/v0.2-overview.md | 1050 | - [ ] T1156-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T1055-3263 | docs/dev/roadmap/v0.2-overview.md | 1051 | - [ ] T1157-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T1056-56e6 | docs/dev/roadmap/v0.2-overview.md | 1052 | - [ ] T1158-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T1057-7567 | docs/dev/roadmap/v0.2-overview.md | 1053 | - [ ] T1159-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T1058-4194 | docs/dev/roadmap/v0.2-overview.md | 1054 | - [ ] T1160-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T1059-b186 | docs/dev/roadmap/v0.2-overview.md | 1055 | - [ ] T1161-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T1060-8db7 | docs/dev/roadmap/v0.2-overview.md | 1056 | - [ ] T1162-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T1061-6401 | docs/dev/roadmap/v0.3-plus/master-todo.md | 4 | ## Master TODO |
| T1062-9a06 | docs/dev/roadmap/v0.3-plus/master-todo.md | 5 | - [ ] T0005-eebd Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). (docs/release-checklist-v0.1.md:10) |
| T1063-26cb | docs/dev/roadmap/v0.3-plus/master-todo.md | 6 | - [ ] T0006-6c05 **Conftest/OPA Policies** laufen sauber (`make ci-policy`). (docs/release-checklist-v0.1.md:11) |
| T1064-536c | docs/dev/roadmap/v0.3-plus/master-todo.md | 7 | - [ ] T0008-1054 **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. (docs/release-checklist-v0.1.md:13) |
| T1065-12f7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 8 | - [ ] T0009-eca0 **Ingress TLS** aktiv (cert-manager, staging Issuer OK). (docs/release-checklist-v0.1.md:14) |
| T1066-6c94 | docs/dev/roadmap/v0.3-plus/master-todo.md | 9 | - [ ] T0010-32fc Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). (docs/release-checklist-v0.1.md:15) |
| T1067-6544 | docs/dev/roadmap/v0.3-plus/master-todo.md | 10 | - [ ] T0011-4f3a **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). (docs/release-checklist-v0.1.md:21) |
| T1068-06d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 11 | - [ ] T0012-d26e **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). (docs/release-checklist-v0.1.md:22) |
| T1069-52fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 12 | - [ ] T0013-d31f **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. (docs/release-checklist-v0.1.md:23) |
| T1070-45db | docs/dev/roadmap/v0.3-plus/master-todo.md | 13 | - [ ] T0014-685a **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. (docs/release-checklist-v0.1.md:24) |
| T1071-130f | docs/dev/roadmap/v0.3-plus/master-todo.md | 14 | - [ ] T0015-ab33 **Dependabot** aktiviert (pip, npm, GitHub Actions). (docs/release-checklist-v0.1.md:25) |
| T1072-e5ab | docs/dev/roadmap/v0.3-plus/master-todo.md | 15 | - [ ] T0016-8f65 **Trivy Scan** ohne kritische Findings. (docs/release-checklist-v0.1.md:26) |
| T1073-c7e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 16 | - [ ] T0017-3458 **dbt build/test** grün (Seeds, Models, Tests). (docs/release-checklist-v0.1.md:32) |
| T1074-cf27 | docs/dev/roadmap/v0.3-plus/master-todo.md | 17 | - [ ] T0018-2aca **dbt docs generate** erzeugt Artefakt (Docs erreichbar). (docs/release-checklist-v0.1.md:33) |
| T1075-fe92 | docs/dev/roadmap/v0.3-plus/master-todo.md | 18 | - [ ] T0019-8c28 **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). (docs/release-checklist-v0.1.md:34) |
| T1076-7501 | docs/dev/roadmap/v0.3-plus/master-todo.md | 19 | - [ ] T0020-3e64 **Exposures** definiert (Superset Dashboards verlinkt). (docs/release-checklist-v0.1.md:35) |
| T1077-9009 | docs/dev/roadmap/v0.3-plus/master-todo.md | 20 | - [ ] T0021-5a64 **Freshness Checks** für Sources ohne Errors. (docs/release-checklist-v0.1.md:36) |
| T1078-a60a | docs/dev/roadmap/v0.3-plus/master-todo.md | 21 | - [ ] T0022-d46f **Superset Dashboard** „analytics_prices“ importiert: (docs/release-checklist-v0.1.md:42) |
| T1079-7f53 | docs/dev/roadmap/v0.3-plus/master-todo.md | 22 | - [ ] T0023-887e **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. (docs/release-checklist-v0.1.md:45) |
| T1080-f768 | docs/dev/roadmap/v0.3-plus/master-todo.md | 23 | - [ ] T0024-7e0b Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). (docs/release-checklist-v0.1.md:46) |
| T1081-714f | docs/dev/roadmap/v0.3-plus/master-todo.md | 24 | - [ ] T0025-b8e1 **Vitest/Playwright Tests** decken Detailseiten ab. (docs/release-checklist-v0.1.md:47) |
| T1082-b45d | docs/dev/roadmap/v0.3-plus/master-todo.md | 25 | - [ ] T0026-8521 **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. (docs/release-checklist-v0.1.md:53) |
| T1083-608f | docs/dev/roadmap/v0.3-plus/master-todo.md | 26 | - [ ] T0027-6e44 **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. (docs/release-checklist-v0.1.md:54) |
| T1084-0d43 | docs/dev/roadmap/v0.3-plus/master-todo.md | 27 | - [ ] T0028-d0e1 **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). (docs/release-checklist-v0.1.md:55) |
| T1085-61b2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 28 | - [ ] T0029-574b Restore-Runbook einmal **trocken getestet**. (docs/release-checklist-v0.1.md:56) |
| T1086-9258 | docs/dev/roadmap/v0.3-plus/master-todo.md | 29 | - [ ] T0030-a42b **OTel Collector** deployed (4317/4318/9464 erreichbar). (docs/release-checklist-v0.1.md:62) |
| T1087-d097 | docs/dev/roadmap/v0.3-plus/master-todo.md | 30 | - [ ] T0031-3686 **Python Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:63) |
| T1088-e8dd | docs/dev/roadmap/v0.3-plus/master-todo.md | 31 | - [ ] T0032-50c9 **Node Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:64) |
| T1089-f838 | docs/dev/roadmap/v0.3-plus/master-todo.md | 32 | - [ ] T0033-fd89 **Prometheus** scrapt Services; Grafana Panels gefüllt. (docs/release-checklist-v0.1.md:65) |
| T1090-66c6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 33 | - [ ] T0034-8197 **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). (docs/release-checklist-v0.1.md:66) |
| T1091-48cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 34 | - [ ] T0035-b3e9 **Loki** enthält Logs aller Services (Promtail shipping OK). (docs/release-checklist-v0.1.md:67) |
| T1092-4e7e | docs/dev/roadmap/v0.3-plus/master-todo.md | 35 | - [ ] T0036-206b **Grafana Dashboards**: (docs/release-checklist-v0.1.md:68) |
| T1093-74cc | docs/dev/roadmap/v0.3-plus/master-todo.md | 36 | - [ ] T0037-f9ff **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). (docs/release-checklist-v0.1.md:76) |
| T1094-ae07 | docs/dev/roadmap/v0.3-plus/master-todo.md | 37 | - [ ] T0038-f0be **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. (docs/release-checklist-v0.1.md:77) |
| T1095-7ce4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 38 | - [ ] T0039-e2d9 **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. (docs/release-checklist-v0.1.md:78) |
| T1096-298b | docs/dev/roadmap/v0.3-plus/master-todo.md | 39 | - [ ] T0040-8dc3 **Language Policy**: Docs in EN, DE als Appendix. (docs/release-checklist-v0.1.md:79) |
| T1097-c6ce | docs/dev/roadmap/v0.3-plus/master-todo.md | 40 | - [ ] T0041-72f3 **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. (docs/release-checklist-v0.1.md:80) |
| T1098-1a42 | docs/dev/roadmap/v0.3-plus/master-todo.md | 41 | - [ ] T0042-ffe9 **CI Docs-Checks** grün (markdownlint, link check, doctoc). (docs/release-checklist-v0.1.md:81) |
| T1099-1b57 | docs/dev/roadmap/v0.3-plus/master-todo.md | 42 | - [ ] T0043-60e9 **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. (docs/release-checklist-v0.1.md:87) |
| T1100-99f5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 43 | - [ ] T0044-c003 **Ingress Hosts** & TLS validiert. (docs/release-checklist-v0.1.md:88) |
| T1101-adfd | docs/dev/roadmap/v0.3-plus/master-todo.md | 44 | - [ ] T0045-c622 **Demo-Data Seed** erfolgreich (`make seed-demo`). (docs/release-checklist-v0.1.md:89) |
| T1102-b264 | docs/dev/roadmap/v0.3-plus/master-todo.md | 45 | - [ ] T0046-1aba **Smoke-Test** im Staging: (docs/release-checklist-v0.1.md:90) |
| T1103-1c3c | docs/dev/roadmap/v0.3-plus/master-todo.md | 46 | - [ ] T0047-63c7 `main` eingefroren, `release/v0.1` Branch erstellt. (docs/release-checklist-v0.1.md:103) |
| T1104-4b1d | docs/dev/roadmap/v0.3-plus/master-todo.md | 47 | - [ ] T0048-0400 **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). (docs/release-checklist-v0.1.md:104) |
| T1105-2245 | docs/dev/roadmap/v0.3-plus/master-todo.md | 48 | - [ ] T0049-b6c0 **Release Notes** erstellt (Features, Breaking Changes, Known Issues). (docs/release-checklist-v0.1.md:105) |
| T1106-d98e | docs/dev/roadmap/v0.3-plus/master-todo.md | 49 | - [ ] T0050-bac8 **Tag v0.1.0** gesetzt und Release publiziert. (docs/release-checklist-v0.1.md:106) |
| T1107-b8e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 50 | - [ ] T0051-3445 Dokumentation zur Installation/Exploration angehängt. (docs/release-checklist-v0.1.md:107) |
| T1108-9ca4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 51 | - [ ] T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T1109-2d42 | docs/dev/roadmap/v0.3-plus/master-todo.md | 52 | - [ ] T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T1110-ab4f | docs/dev/roadmap/v0.3-plus/master-todo.md | 53 | - [ ] T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T1111-3503 | docs/dev/roadmap/v0.3-plus/master-todo.md | 54 | - [ ] T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T1112-27d4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 55 | - [ ] T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T1113-2a27 | docs/dev/roadmap/v0.3-plus/master-todo.md | 56 | - [ ] T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T1114-c5b8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 57 | - [ ] T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T1115-965d | docs/dev/roadmap/v0.3-plus/master-todo.md | 58 | - [ ] T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T1116-051f | docs/dev/roadmap/v0.3-plus/master-todo.md | 59 | - [ ] T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T1117-7c7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 60 | - [ ] T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T1118-d3d4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 61 | - [ ] T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T1119-074e | docs/dev/roadmap/v0.3-plus/master-todo.md | 62 | - [ ] T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T1120-0734 | docs/dev/roadmap/v0.3-plus/master-todo.md | 63 | - [ ] T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T1121-2a5c | docs/dev/roadmap/v0.3-plus/master-todo.md | 64 | - [ ] T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T1122-71d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 65 | - [ ] T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T1123-0750 | docs/dev/roadmap/v0.3-plus/master-todo.md | 66 | - [ ] T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T1124-5602 | docs/dev/roadmap/v0.3-plus/master-todo.md | 67 | - [ ] T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T1125-ebd5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 68 | - [ ] T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T1126-88e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 69 | - [ ] T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T1127-016c | docs/dev/roadmap/v0.3-plus/master-todo.md | 70 | - [ ] T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T1128-4372 | docs/dev/roadmap/v0.3-plus/master-todo.md | 71 | - [ ] T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T1129-1e7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 72 | - [ ] T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T1130-71ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 73 | - [ ] T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T1131-ad81 | docs/dev/roadmap/v0.3-plus/master-todo.md | 74 | - [ ] T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T1132-e7b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 75 | - [ ] T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T1133-85ac | docs/dev/roadmap/v0.3-plus/master-todo.md | 76 | - [ ] T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T1134-b097 | docs/dev/roadmap/v0.3-plus/master-todo.md | 77 | - [ ] T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T1135-49c1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 78 | - [ ] T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T1136-cd7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 79 | - [ ] T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T1137-3f1d | docs/dev/roadmap/v0.3-plus/master-todo.md | 80 | - [ ] T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T1138-f88f | docs/dev/roadmap/v0.3-plus/master-todo.md | 81 | - [ ] T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T1139-311e | docs/dev/roadmap/v0.3-plus/master-todo.md | 82 | - [ ] T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T1140-6011 | docs/dev/roadmap/v0.3-plus/master-todo.md | 83 | - [ ] T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T1141-8124 | docs/dev/roadmap/v0.3-plus/master-todo.md | 84 | - [ ] T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T1142-7991 | docs/dev/roadmap/v0.3-plus/master-todo.md | 85 | - [ ] T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T1143-1d26 | docs/dev/roadmap/v0.3-plus/master-todo.md | 86 | - [ ] T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T1144-0b2d | docs/dev/roadmap/v0.3-plus/master-todo.md | 87 | - [ ] T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T1145-4dd3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 88 | - [ ] T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T1146-aee5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 89 | - [ ] T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T1147-7c6b | docs/dev/roadmap/v0.3-plus/master-todo.md | 90 | - [ ] T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T1148-3f1a | docs/dev/roadmap/v0.3-plus/master-todo.md | 91 | - [ ] T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T1149-3dc4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 92 | - [ ] T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T1150-c69f | docs/dev/roadmap/v0.3-plus/master-todo.md | 93 | - [ ] T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T1151-2b03 | docs/dev/roadmap/v0.3-plus/master-todo.md | 94 | - [ ] T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T1152-5f51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 95 | - [ ] T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T1153-9e6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 96 | - [ ] T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T1154-517a | docs/dev/roadmap/v0.3-plus/master-todo.md | 97 | - [ ] T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T1155-2362 | docs/dev/roadmap/v0.3-plus/master-todo.md | 98 | - [ ] T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T1156-11fd | docs/dev/roadmap/v0.3-plus/master-todo.md | 99 | - [ ] T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T1157-2178 | docs/dev/roadmap/v0.3-plus/master-todo.md | 100 | - [ ] T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T1158-ea7a | docs/dev/roadmap/v0.3-plus/master-todo.md | 101 | - [ ] T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T1159-dd84 | docs/dev/roadmap/v0.3-plus/master-todo.md | 102 | - [ ] T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T1160-f1c5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 103 | - [ ] T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T1161-7c83 | docs/dev/roadmap/v0.3-plus/master-todo.md | 104 | - [ ] T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T1162-dba2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 105 | - [ ] T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T1163-a519 | docs/dev/roadmap/v0.3-plus/master-todo.md | 106 | - [ ] T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T1164-b982 | docs/dev/roadmap/v0.3-plus/master-todo.md | 107 | - [ ] T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T1165-fa6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 108 | - [ ] T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T1166-7a84 | docs/dev/roadmap/v0.3-plus/master-todo.md | 109 | - [ ] T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T1167-554a | docs/dev/roadmap/v0.3-plus/master-todo.md | 110 | - [ ] T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T1168-5ecc | docs/dev/roadmap/v0.3-plus/master-todo.md | 111 | - [ ] T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T1169-7fe8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 112 | - [ ] T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T1170-14f9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 113 | - [ ] T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T1171-85ab | docs/dev/roadmap/v0.3-plus/master-todo.md | 114 | - [ ] T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T1172-0c49 | docs/dev/roadmap/v0.3-plus/master-todo.md | 115 | - [ ] T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T1173-f8c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 116 | - [ ] T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T1174-ec90 | docs/dev/roadmap/v0.3-plus/master-todo.md | 117 | - [ ] T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T1175-7803 | docs/dev/roadmap/v0.3-plus/master-todo.md | 118 | - [ ] T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T1176-e904 | docs/dev/roadmap/v0.3-plus/master-todo.md | 119 | - [ ] T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T1177-61e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 120 | - [ ] T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T1178-fc3f | docs/dev/roadmap/v0.3-plus/master-todo.md | 121 | - [ ] T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T1179-039f | docs/dev/roadmap/v0.3-plus/master-todo.md | 122 | - [ ] T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T1180-8ac0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 123 | - [ ] T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T1181-df8c | docs/dev/roadmap/v0.3-plus/master-todo.md | 124 | - [ ] T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T1182-5240 | docs/dev/roadmap/v0.3-plus/master-todo.md | 125 | - [ ] T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T1183-d5a4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 126 | - [ ] T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T1184-ff3b | docs/dev/roadmap/v0.3-plus/master-todo.md | 127 | - [ ] T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T1185-566b | docs/dev/roadmap/v0.3-plus/master-todo.md | 128 | - [ ] T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T1186-3c09 | docs/dev/roadmap/v0.3-plus/master-todo.md | 129 | - [ ] T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T1187-294c | docs/dev/roadmap/v0.3-plus/master-todo.md | 130 | - [ ] T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T1188-6b02 | docs/dev/roadmap/v0.3-plus/master-todo.md | 131 | - [ ] T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T1189-27dc | docs/dev/roadmap/v0.3-plus/master-todo.md | 132 | - [ ] T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T1190-2e5e | docs/dev/roadmap/v0.3-plus/master-todo.md | 133 | - [ ] T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T1191-886e | docs/dev/roadmap/v0.3-plus/master-todo.md | 134 | - [ ] T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T1192-ca6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 135 | - [ ] T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T1193-1e1e | docs/dev/roadmap/v0.3-plus/master-todo.md | 136 | - [ ] T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T1194-2c36 | docs/dev/roadmap/v0.3-plus/master-todo.md | 137 | - [ ] T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T1195-1b27 | docs/dev/roadmap/v0.3-plus/master-todo.md | 138 | - [ ] T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T1196-6907 | docs/dev/roadmap/v0.3-plus/master-todo.md | 139 | - [ ] T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T1197-9669 | docs/dev/roadmap/v0.3-plus/master-todo.md | 140 | - [ ] T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T1198-896d | docs/dev/roadmap/v0.3-plus/master-todo.md | 141 | - [ ] T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T1199-e74b | docs/dev/roadmap/v0.3-plus/master-todo.md | 142 | - [ ] T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T1200-2f17 | docs/dev/roadmap/v0.3-plus/master-todo.md | 143 | - [ ] T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T1201-4ce3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 144 | - [ ] T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T1202-85eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 145 | - [ ] T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T1203-7ba4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 146 | - [ ] T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T1204-ed19 | docs/dev/roadmap/v0.3-plus/master-todo.md | 147 | - [ ] T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T1205-603b | docs/dev/roadmap/v0.3-plus/master-todo.md | 148 | - [ ] T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T1206-519f | docs/dev/roadmap/v0.3-plus/master-todo.md | 149 | - [ ] T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T1207-1e67 | docs/dev/roadmap/v0.3-plus/master-todo.md | 150 | - [ ] T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T1208-3783 | docs/dev/roadmap/v0.3-plus/master-todo.md | 151 | - [ ] T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T1209-a61b | docs/dev/roadmap/v0.3-plus/master-todo.md | 152 | - [ ] T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T1210-421d | docs/dev/roadmap/v0.3-plus/master-todo.md | 153 | - [ ] T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T1211-b3cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 154 | - [ ] T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T1212-e363 | docs/dev/roadmap/v0.3-plus/master-todo.md | 155 | - [ ] T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T1213-50cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 156 | - [ ] T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T1214-2063 | docs/dev/roadmap/v0.3-plus/master-todo.md | 157 | - [ ] T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T1215-1004 | docs/dev/roadmap/v0.3-plus/master-todo.md | 158 | - [ ] T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T1216-b497 | docs/dev/roadmap/v0.3-plus/master-todo.md | 159 | - [ ] T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T1217-4ba1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 160 | - [ ] T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T1218-ab2a | docs/dev/roadmap/v0.3-plus/master-todo.md | 161 | - [ ] T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T1219-7301 | docs/dev/roadmap/v0.3-plus/master-todo.md | 162 | - [ ] T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T1220-b327 | docs/dev/roadmap/v0.3-plus/master-todo.md | 163 | - [ ] T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T1221-f2e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 164 | - [ ] T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T1222-0cf1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 165 | - [ ] T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T1223-e442 | docs/dev/roadmap/v0.3-plus/master-todo.md | 166 | - [ ] T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T1224-13c5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 167 | - [ ] T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T1225-88b6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 168 | - [ ] T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T1226-99ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 169 | - [ ] T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T1227-ebf5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 170 | - [ ] T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T1228-c6d4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 171 | - [ ] T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T1229-4467 | docs/dev/roadmap/v0.3-plus/master-todo.md | 172 | - [ ] T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T1230-8ae7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 173 | - [ ] T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T1231-559d | docs/dev/roadmap/v0.3-plus/master-todo.md | 174 | - [ ] T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T1232-1c0f | docs/dev/roadmap/v0.3-plus/master-todo.md | 175 | - [ ] T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T1233-7476 | docs/dev/roadmap/v0.3-plus/master-todo.md | 176 | - [ ] T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T1234-7aed | docs/dev/roadmap/v0.3-plus/master-todo.md | 177 | - [ ] T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T1235-80d0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 178 | - [ ] T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T1236-c5e2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 179 | - [ ] T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T1237-1d74 | docs/dev/roadmap/v0.3-plus/master-todo.md | 180 | - [ ] T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T1238-21fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 181 | - [ ] T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T1239-06dc | docs/dev/roadmap/v0.3-plus/master-todo.md | 182 | - [ ] T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T1240-374b | docs/dev/roadmap/v0.3-plus/master-todo.md | 183 | - [ ] T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T1241-be73 | docs/dev/roadmap/v0.3-plus/master-todo.md | 184 | - [ ] T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T1242-2eac | docs/dev/roadmap/v0.3-plus/master-todo.md | 185 | - [ ] T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T1243-e38b | docs/dev/roadmap/v0.3-plus/master-todo.md | 186 | - [ ] T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T1244-3fc3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 187 | - [ ] T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T1245-e623 | docs/dev/roadmap/v0.3-plus/master-todo.md | 188 | - [ ] T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T1246-41e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 189 | - [ ] T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T1247-3e54 | docs/dev/roadmap/v0.3-plus/master-todo.md | 190 | - [ ] T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T1248-49cc | docs/dev/roadmap/v0.3-plus/master-todo.md | 191 | - [ ] T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T1249-a48f | docs/dev/roadmap/v0.3-plus/master-todo.md | 192 | - [ ] T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T1250-30e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 193 | - [ ] T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T1251-6688 | docs/dev/roadmap/v0.3-plus/master-todo.md | 194 | - [ ] T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T1252-7337 | docs/dev/roadmap/v0.3-plus/master-todo.md | 195 | - [ ] T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T1253-e90d | docs/dev/roadmap/v0.3-plus/master-todo.md | 196 | - [ ] T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T1254-533c | docs/dev/roadmap/v0.3-plus/master-todo.md | 197 | - [ ] T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T1255-68a7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 198 | - [ ] T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T1256-dbf7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 199 | - [ ] T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T1257-a0dd | docs/dev/roadmap/v0.3-plus/master-todo.md | 200 | - [ ] T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T1258-d6e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 201 | - [ ] T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T1259-5476 | docs/dev/roadmap/v0.3-plus/master-todo.md | 202 | - [ ] T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T1260-29fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 203 | - [ ] T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T1261-2eb5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 204 | - [ ] T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T1262-0cd3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 205 | - [ ] T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T1263-eed9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 206 | - [ ] T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T1264-1557 | docs/dev/roadmap/v0.3-plus/master-todo.md | 207 | - [ ] T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T1265-9636 | docs/dev/roadmap/v0.3-plus/master-todo.md | 208 | - [ ] T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T1266-e748 | docs/dev/roadmap/v0.3-plus/master-todo.md | 209 | - [ ] T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T1267-40d8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 210 | - [ ] T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T1268-3249 | docs/dev/roadmap/v0.3-plus/master-todo.md | 211 | - [ ] T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T1269-7cc2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 212 | - [ ] T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T1270-2c34 | docs/dev/roadmap/v0.3-plus/master-todo.md | 213 | - [ ] T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T1271-30ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 214 | - [ ] T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T1272-16cf | docs/dev/roadmap/v0.3-plus/master-todo.md | 215 | - [ ] T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T1273-a41a | docs/dev/roadmap/v0.3-plus/master-todo.md | 216 | - [ ] T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T1274-febf | docs/dev/roadmap/v0.3-plus/master-todo.md | 217 | - [ ] T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T1275-3eed | docs/dev/roadmap/v0.3-plus/master-todo.md | 218 | - [ ] T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T1276-d86c | docs/dev/roadmap/v0.3-plus/master-todo.md | 219 | - [ ] T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T1277-4f16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 220 | - [ ] T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T1278-eba0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 221 | - [ ] T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T1279-eb35 | docs/dev/roadmap/v0.3-plus/master-todo.md | 222 | - [ ] T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T1280-3679 | docs/dev/roadmap/v0.3-plus/master-todo.md | 223 | - [ ] T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T1281-5351 | docs/dev/roadmap/v0.3-plus/master-todo.md | 224 | - [ ] T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T1282-6438 | docs/dev/roadmap/v0.3-plus/master-todo.md | 225 | - [ ] T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T1283-24d5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 226 | - [ ] T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T1284-015f | docs/dev/roadmap/v0.3-plus/master-todo.md | 227 | - [ ] T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T1285-53b3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 228 | - [ ] T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T1286-693c | docs/dev/roadmap/v0.3-plus/master-todo.md | 229 | - [ ] T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T1287-8fb2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 230 | - [ ] T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T1288-6102 | docs/dev/roadmap/v0.3-plus/master-todo.md | 231 | - [ ] T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T1289-3441 | docs/dev/roadmap/v0.3-plus/master-todo.md | 232 | - [ ] T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T1290-4ade | docs/dev/roadmap/v0.3-plus/master-todo.md | 233 | - [ ] T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T1291-3991 | docs/dev/roadmap/v0.3-plus/master-todo.md | 234 | - [ ] T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T1292-282a | docs/dev/roadmap/v0.3-plus/master-todo.md | 235 | - [ ] T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T1293-342b | docs/dev/roadmap/v0.3-plus/master-todo.md | 236 | - [ ] T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T1294-130b | docs/dev/roadmap/v0.3-plus/master-todo.md | 237 | - [ ] T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T1295-29f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 238 | - [ ] T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T1296-484c | docs/dev/roadmap/v0.3-plus/master-todo.md | 239 | - [ ] T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T1297-1370 | docs/dev/roadmap/v0.3-plus/master-todo.md | 240 | - [ ] T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T1298-f84c | docs/dev/roadmap/v0.3-plus/master-todo.md | 241 | - [ ] T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T1299-a236 | docs/dev/roadmap/v0.3-plus/master-todo.md | 242 | - [ ] T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T1300-5ce4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 243 | - [ ] T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T1301-45a5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 244 | - [ ] T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T1302-47d5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 245 | - [ ] T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T1303-36c7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 246 | - [ ] T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T1304-775d | docs/dev/roadmap/v0.3-plus/master-todo.md | 247 | - [ ] T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T1305-6ce7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 248 | - [ ] T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T1306-bdfe | docs/dev/roadmap/v0.3-plus/master-todo.md | 249 | - [ ] T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T1307-167a | docs/dev/roadmap/v0.3-plus/master-todo.md | 250 | - [ ] T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T1308-fed5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 251 | - [ ] T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T1309-2b7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 252 | - [ ] T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T1310-7c0a | docs/dev/roadmap/v0.3-plus/master-todo.md | 253 | - [ ] T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T1311-1dad | docs/dev/roadmap/v0.3-plus/master-todo.md | 254 | - [ ] T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T1312-062d | docs/dev/roadmap/v0.3-plus/master-todo.md | 255 | - [ ] T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T1313-5a40 | docs/dev/roadmap/v0.3-plus/master-todo.md | 256 | - [ ] T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T1314-839d | docs/dev/roadmap/v0.3-plus/master-todo.md | 257 | - [ ] T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T1315-2a74 | docs/dev/roadmap/v0.3-plus/master-todo.md | 258 | - [ ] T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T1316-3ac0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 259 | - [ ] T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T1317-305e | docs/dev/roadmap/v0.3-plus/master-todo.md | 260 | - [ ] T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T1318-a8c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 261 | - [ ] T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T1319-1a8f | docs/dev/roadmap/v0.3-plus/master-todo.md | 262 | - [ ] T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T1320-509e | docs/dev/roadmap/v0.3-plus/master-todo.md | 263 | - [ ] T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T1321-05c7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 264 | - [ ] T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T1322-d3ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 265 | - [ ] T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T1323-64e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 266 | - [ ] T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T1324-05d0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 267 | - [ ] T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T1325-9c69 | docs/dev/roadmap/v0.3-plus/master-todo.md | 268 | - [ ] T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T1326-05cb | docs/dev/roadmap/v0.3-plus/master-todo.md | 269 | - [ ] T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T1327-dbf2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 270 | - [ ] T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T1328-75b9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 271 | - [ ] T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T1329-a46c | docs/dev/roadmap/v0.3-plus/master-todo.md | 272 | - [ ] T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T1330-a450 | docs/dev/roadmap/v0.3-plus/master-todo.md | 273 | - [ ] T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T1331-f9a5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 274 | - [ ] T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T1332-f22d | docs/dev/roadmap/v0.3-plus/master-todo.md | 275 | - [ ] T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T1333-d766 | docs/dev/roadmap/v0.3-plus/master-todo.md | 276 | - [ ] T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T1334-386b | docs/dev/roadmap/v0.3-plus/master-todo.md | 277 | - [ ] T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T1335-3aa7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 278 | - [ ] T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T1336-990b | docs/dev/roadmap/v0.3-plus/master-todo.md | 279 | - [ ] T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T1337-c4ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 280 | - [ ] T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T1338-764a | docs/dev/roadmap/v0.3-plus/master-todo.md | 281 | - [ ] T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T1339-a453 | docs/dev/roadmap/v0.3-plus/master-todo.md | 282 | - [ ] T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T1340-5c4b | docs/dev/roadmap/v0.3-plus/master-todo.md | 283 | - [ ] T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T1341-eaf7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 284 | - [ ] T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T1342-5ac0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 285 | - [ ] T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T1343-9a20 | docs/dev/roadmap/v0.3-plus/master-todo.md | 286 | - [ ] T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T1344-6965 | docs/dev/roadmap/v0.3-plus/master-todo.md | 287 | - [ ] T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T1345-e285 | docs/dev/roadmap/v0.3-plus/master-todo.md | 288 | - [ ] T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T1346-1e03 | docs/dev/roadmap/v0.3-plus/master-todo.md | 289 | - [ ] T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T1347-df6c | docs/dev/roadmap/v0.3-plus/master-todo.md | 290 | - [ ] T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T1348-8e7c | docs/dev/roadmap/v0.3-plus/master-todo.md | 291 | - [ ] T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T1349-a4be | docs/dev/roadmap/v0.3-plus/master-todo.md | 292 | - [ ] T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T1350-d29c | docs/dev/roadmap/v0.3-plus/master-todo.md | 293 | - [ ] T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T1351-466c | docs/dev/roadmap/v0.3-plus/master-todo.md | 294 | - [ ] T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T1352-d0c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 295 | - [ ] T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T1353-a7f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 296 | - [ ] T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T1354-c33d | docs/dev/roadmap/v0.3-plus/master-todo.md | 297 | - [ ] T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T1355-e0e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 298 | - [ ] T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T1356-79eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 299 | - [ ] T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T1357-6cd7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 300 | - [ ] T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T1358-5d19 | docs/dev/roadmap/v0.3-plus/master-todo.md | 301 | - [ ] T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T1359-3721 | docs/dev/roadmap/v0.3-plus/master-todo.md | 302 | - [ ] T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T1360-786a | docs/dev/roadmap/v0.3-plus/master-todo.md | 303 | - [ ] T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T1361-f6a7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 304 | - [ ] T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T1362-52df | docs/dev/roadmap/v0.3-plus/master-todo.md | 305 | - [ ] T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T1363-be71 | docs/dev/roadmap/v0.3-plus/master-todo.md | 306 | - [ ] T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T1364-3b45 | docs/dev/roadmap/v0.3-plus/master-todo.md | 307 | - [ ] T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T1365-a0ae | docs/dev/roadmap/v0.3-plus/master-todo.md | 308 | - [ ] T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T1366-17c8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 309 | - [ ] T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T1367-7c0b | docs/dev/roadmap/v0.3-plus/master-todo.md | 310 | - [ ] T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T1368-a137 | docs/dev/roadmap/v0.3-plus/master-todo.md | 311 | - [ ] T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T1369-51fb | docs/dev/roadmap/v0.3-plus/master-todo.md | 312 | - [ ] T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T1370-2754 | docs/dev/roadmap/v0.3-plus/master-todo.md | 313 | - [ ] T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T1371-a419 | docs/dev/roadmap/v0.3-plus/master-todo.md | 314 | - [ ] T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T1372-0d68 | docs/dev/roadmap/v0.3-plus/master-todo.md | 315 | - [ ] T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T1373-8372 | docs/dev/roadmap/v0.3-plus/master-todo.md | 316 | - [ ] T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T1374-5732 | docs/dev/roadmap/v0.3-plus/master-todo.md | 317 | - [ ] T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T1375-7189 | docs/dev/roadmap/v0.3-plus/master-todo.md | 318 | - [ ] T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T1376-83e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 319 | - [ ] T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T1377-d78f | docs/dev/roadmap/v0.3-plus/master-todo.md | 320 | - [ ] T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T1378-ea9c | docs/dev/roadmap/v0.3-plus/master-todo.md | 321 | - [ ] T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T1379-4d82 | docs/dev/roadmap/v0.3-plus/master-todo.md | 322 | - [ ] T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T1380-7b96 | docs/dev/roadmap/v0.3-plus/master-todo.md | 323 | - [ ] T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T1381-41a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 324 | - [ ] T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T1382-25e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 325 | - [ ] T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T1383-9f7e | docs/dev/roadmap/v0.3-plus/master-todo.md | 326 | - [ ] T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T1384-c83f | docs/dev/roadmap/v0.3-plus/master-todo.md | 327 | - [ ] T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T1385-0a93 | docs/dev/roadmap/v0.3-plus/master-todo.md | 328 | - [ ] T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T1386-1b2b | docs/dev/roadmap/v0.3-plus/master-todo.md | 329 | - [ ] T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T1387-faf8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 330 | - [ ] T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T1388-91ab | docs/dev/roadmap/v0.3-plus/master-todo.md | 331 | - [ ] T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T1389-4def | docs/dev/roadmap/v0.3-plus/master-todo.md | 332 | - [ ] T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T1390-425a | docs/dev/roadmap/v0.3-plus/master-todo.md | 333 | - [ ] T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T1391-04b8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 334 | - [ ] T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T1392-2ea4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 335 | - [ ] T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T1393-238d | docs/dev/roadmap/v0.3-plus/master-todo.md | 336 | - [ ] T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T1394-9245 | docs/dev/roadmap/v0.3-plus/master-todo.md | 337 | - [ ] T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T1395-4b84 | docs/dev/roadmap/v0.3-plus/master-todo.md | 338 | - [ ] T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T1396-42d0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 339 | - [ ] T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T1397-ff4c | docs/dev/roadmap/v0.3-plus/master-todo.md | 340 | - [ ] T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T1398-1fe8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 341 | - [ ] T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T1399-0aa2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 342 | - [ ] T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T1400-9680 | docs/dev/roadmap/v0.3-plus/master-todo.md | 343 | - [ ] T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T1401-22e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 344 | - [ ] T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T1402-7902 | docs/dev/roadmap/v0.3-plus/master-todo.md | 345 | - [ ] T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T1403-dbc8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 346 | - [ ] T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T1404-360e | docs/dev/roadmap/v0.3-plus/master-todo.md | 347 | - [ ] T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T1405-3c16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 348 | - [ ] T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T1406-a3a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 349 | - [ ] T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T1407-d420 | docs/dev/roadmap/v0.3-plus/master-todo.md | 350 | - [ ] T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T1408-7ef2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 351 | - [ ] T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T1409-583f | docs/dev/roadmap/v0.3-plus/master-todo.md | 352 | - [ ] T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T1410-5e45 | docs/dev/roadmap/v0.3-plus/master-todo.md | 353 | - [ ] T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T1411-9f2a | docs/dev/roadmap/v0.3-plus/master-todo.md | 354 | - [ ] T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T1412-52e3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 355 | - [ ] T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T1413-1bed | docs/dev/roadmap/v0.3-plus/master-todo.md | 356 | - [ ] T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T1414-d143 | docs/dev/roadmap/v0.3-plus/master-todo.md | 357 | - [ ] T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T1415-5f5d | docs/dev/roadmap/v0.3-plus/master-todo.md | 358 | - [ ] T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T1416-1349 | docs/dev/roadmap/v0.3-plus/master-todo.md | 359 | - [ ] T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T1417-929c | docs/dev/roadmap/v0.3-plus/master-todo.md | 360 | - [ ] T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T1418-4f9d | docs/dev/roadmap/v0.3-plus/master-todo.md | 361 | - [ ] T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T1419-8794 | docs/dev/roadmap/v0.3-plus/master-todo.md | 362 | - [ ] T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T1420-cb3b | docs/dev/roadmap/v0.3-plus/master-todo.md | 363 | - [ ] T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T1421-712b | docs/dev/roadmap/v0.3-plus/master-todo.md | 364 | - [ ] T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T1422-6663 | docs/dev/roadmap/v0.3-plus/master-todo.md | 365 | - [ ] T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T1423-2270 | docs/dev/roadmap/v0.3-plus/master-todo.md | 366 | - [ ] T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T1424-ea5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 367 | - [ ] T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T1425-1398 | docs/dev/roadmap/v0.3-plus/master-todo.md | 368 | - [ ] T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T1426-5fd4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 369 | - [ ] T0107-c900 T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.2-overview.md:103) |
| T1427-26fb | docs/dev/roadmap/v0.3-plus/master-todo.md | 370 | - [ ] T0108-993d T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.2-overview.md:104) |
| T1428-33ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 371 | - [ ] T0109-a50e T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.2-overview.md:105) |
| T1429-ec56 | docs/dev/roadmap/v0.3-plus/master-todo.md | 372 | - [ ] T0110-aa9c T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.2-overview.md:106) |
| T1430-620f | docs/dev/roadmap/v0.3-plus/master-todo.md | 373 | - [ ] T0111-029c T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.2-overview.md:107) |
| T1431-0bee | docs/dev/roadmap/v0.3-plus/master-todo.md | 374 | - [ ] T0112-f95d T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.2-overview.md:108) |
| T1432-dd63 | docs/dev/roadmap/v0.3-plus/master-todo.md | 375 | - [ ] T0113-9052 T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:109) |
| T1433-a51d | docs/dev/roadmap/v0.3-plus/master-todo.md | 376 | - [ ] T0114-73c9 T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:110) |
| T1434-ecba | docs/dev/roadmap/v0.3-plus/master-todo.md | 377 | - [ ] T0115-4d3f T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:111) |
| T1435-64c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 378 | - [ ] T0116-07a6 T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:112) |
| T1436-bbd9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 379 | - [ ] T0117-4b6d T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:113) |
| T1437-8f7e | docs/dev/roadmap/v0.3-plus/master-todo.md | 380 | - [ ] T0118-0eb7 T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:114) |
| T1438-30eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 381 | - [ ] T0119-bf23 T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:115) |
| T1439-64ee | docs/dev/roadmap/v0.3-plus/master-todo.md | 382 | - [ ] T0120-e436 T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:116) |
| T1440-bf20 | docs/dev/roadmap/v0.3-plus/master-todo.md | 383 | - [ ] T0121-23d3 T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:117) |
| T1441-dc2b | docs/dev/roadmap/v0.3-plus/master-todo.md | 384 | - [ ] T0122-d79e T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:118) |
| T1442-6beb | docs/dev/roadmap/v0.3-plus/master-todo.md | 385 | - [ ] T0123-17bb T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:119) |
| T1443-fca1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 386 | - [ ] T0124-6fe0 T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:120) |
| T1444-fd49 | docs/dev/roadmap/v0.3-plus/master-todo.md | 387 | - [ ] T0125-9422 T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:121) |
| T1445-e94a | docs/dev/roadmap/v0.3-plus/master-todo.md | 388 | - [ ] T0126-1648 T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:122) |
| T1446-55bb | docs/dev/roadmap/v0.3-plus/master-todo.md | 389 | - [ ] T0127-04d4 T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:123) |
| T1447-9e12 | docs/dev/roadmap/v0.3-plus/master-todo.md | 390 | - [ ] T0128-504c T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:124) |
| T1448-2cb9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 391 | - [ ] T0129-8642 T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:125) |
| T1449-0f69 | docs/dev/roadmap/v0.3-plus/master-todo.md | 392 | - [ ] T0130-8ea1 T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:126) |
| T1450-04fa | docs/dev/roadmap/v0.3-plus/master-todo.md | 393 | - [ ] T0131-4396 T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:127) |
| T1451-cdf7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 394 | - [ ] T0132-f8e4 T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:128) |
| T1452-0e41 | docs/dev/roadmap/v0.3-plus/master-todo.md | 395 | - [ ] T0133-fa5e T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:129) |
| T1453-6d35 | docs/dev/roadmap/v0.3-plus/master-todo.md | 396 | - [ ] T0134-2334 T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:130) |
| T1454-db52 | docs/dev/roadmap/v0.3-plus/master-todo.md | 397 | - [ ] T0135-dfe5 T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:131) |
| T1455-8b82 | docs/dev/roadmap/v0.3-plus/master-todo.md | 398 | - [ ] T0136-b1a3 T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:132) |
| T1456-ed41 | docs/dev/roadmap/v0.3-plus/master-todo.md | 399 | - [ ] T0137-60ad T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:133) |
| T1457-dd63 | docs/dev/roadmap/v0.3-plus/master-todo.md | 400 | - [ ] T0138-0b24 T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:134) |
| T1458-4993 | docs/dev/roadmap/v0.3-plus/master-todo.md | 401 | - [ ] T0139-e439 T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:135) |
| T1459-553b | docs/dev/roadmap/v0.3-plus/master-todo.md | 402 | - [ ] T0140-bc80 T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:136) |
| T1460-2033 | docs/dev/roadmap/v0.3-plus/master-todo.md | 403 | - [ ] T0141-46b0 T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:137) |
| T1461-3382 | docs/dev/roadmap/v0.3-plus/master-todo.md | 404 | - [ ] T0142-21f0 T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:138) |
| T1462-c951 | docs/dev/roadmap/v0.3-plus/master-todo.md | 405 | - [ ] T0143-6637 T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:139) |
| T1463-24ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 406 | - [ ] T0144-203c T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:140) |
| T1464-c75f | docs/dev/roadmap/v0.3-plus/master-todo.md | 407 | - [ ] T0145-5dc5 T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:141) |
| T1465-451d | docs/dev/roadmap/v0.3-plus/master-todo.md | 408 | - [ ] T0146-10b0 T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:142) |
| T1466-50ca | docs/dev/roadmap/v0.3-plus/master-todo.md | 409 | - [ ] T0147-90e5 T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:143) |
| T1467-537b | docs/dev/roadmap/v0.3-plus/master-todo.md | 410 | - [ ] T0148-3465 T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:144) |
| T1468-ee47 | docs/dev/roadmap/v0.3-plus/master-todo.md | 411 | - [ ] T0149-ea22 T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:145) |
| T1469-7875 | docs/dev/roadmap/v0.3-plus/master-todo.md | 412 | - [ ] T0150-4c65 T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:146) |
| T1470-f9e1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 413 | - [ ] T0151-2fd6 T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:147) |
| T1471-6cff | docs/dev/roadmap/v0.3-plus/master-todo.md | 414 | - [ ] T0152-3de7 T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:148) |
| T1472-fa2f | docs/dev/roadmap/v0.3-plus/master-todo.md | 415 | - [ ] T0153-1141 T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:149) |
| T1473-a667 | docs/dev/roadmap/v0.3-plus/master-todo.md | 416 | - [ ] T0154-e25b T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:150) |
| T1474-009b | docs/dev/roadmap/v0.3-plus/master-todo.md | 417 | - [ ] T0155-52ee T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:151) |
| T1475-ba6c | docs/dev/roadmap/v0.3-plus/master-todo.md | 418 | - [ ] T0156-a970 T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:152) |
| T1476-449a | docs/dev/roadmap/v0.3-plus/master-todo.md | 419 | - [ ] T0157-eb70 T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:153) |
| T1477-14f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 420 | - [ ] T0158-c59f T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:154) |
| T1478-ead0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 421 | - [ ] T0159-e81e T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:155) |
| T1479-d35f | docs/dev/roadmap/v0.3-plus/master-todo.md | 422 | - [ ] T0160-f48b T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:156) |
| T1480-3d3b | docs/dev/roadmap/v0.3-plus/master-todo.md | 423 | - [ ] T0161-4486 T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:157) |
| T1481-42b2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 424 | - [ ] T0162-2a68 T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:158) |
| T1482-8fee | docs/dev/roadmap/v0.3-plus/master-todo.md | 425 | - [ ] T0163-3932 T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:159) |
| T1483-883d | docs/dev/roadmap/v0.3-plus/master-todo.md | 426 | - [ ] T0164-a424 T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:160) |
| T1484-5a94 | docs/dev/roadmap/v0.3-plus/master-todo.md | 427 | - [ ] T0165-0267 T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:161) |
| T1485-9bb1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 428 | - [ ] T0166-de78 T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:162) |
| T1486-e44e | docs/dev/roadmap/v0.3-plus/master-todo.md | 429 | - [ ] T0167-3d4f T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:163) |
| T1487-6dae | docs/dev/roadmap/v0.3-plus/master-todo.md | 430 | - [ ] T0168-3c90 T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:164) |
| T1488-4dde | docs/dev/roadmap/v0.3-plus/master-todo.md | 431 | - [ ] T0169-661b T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:165) |
| T1489-e585 | docs/dev/roadmap/v0.3-plus/master-todo.md | 432 | - [ ] T0170-ebca T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:166) |
| T1490-03f3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 433 | - [ ] T0171-ce42 T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:167) |
| T1491-c648 | docs/dev/roadmap/v0.3-plus/master-todo.md | 434 | - [ ] T0172-13c7 T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:168) |
| T1492-79fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 435 | - [ ] T0173-d114 T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:169) |
| T1493-efcb | docs/dev/roadmap/v0.3-plus/master-todo.md | 436 | - [ ] T0174-b7c8 T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:170) |
| T1494-013f | docs/dev/roadmap/v0.3-plus/master-todo.md | 437 | - [ ] T0175-5b1e T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:171) |
| T1495-adef | docs/dev/roadmap/v0.3-plus/master-todo.md | 438 | - [ ] T0176-e2a0 T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:172) |
| T1496-36fa | docs/dev/roadmap/v0.3-plus/master-todo.md | 439 | - [ ] T0177-b641 T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:173) |
| T1497-5e06 | docs/dev/roadmap/v0.3-plus/master-todo.md | 440 | - [ ] T0178-644e T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:174) |
| T1498-5420 | docs/dev/roadmap/v0.3-plus/master-todo.md | 441 | - [ ] T0179-60b4 T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:175) |
| T1499-a409 | docs/dev/roadmap/v0.3-plus/master-todo.md | 442 | - [ ] T0180-817f T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:176) |
| T1500-bbbc | docs/dev/roadmap/v0.3-plus/master-todo.md | 443 | - [ ] T0181-f016 T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:177) |
| T1501-c89b | docs/dev/roadmap/v0.3-plus/master-todo.md | 444 | - [ ] T0182-462f T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:178) |
| T1502-90b1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 445 | - [ ] T0183-b7c4 T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:179) |
| T1503-f3d8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 446 | - [ ] T0184-e931 T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:180) |
| T1504-a1f3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 447 | - [ ] T0185-9d65 T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:181) |
| T1505-9825 | docs/dev/roadmap/v0.3-plus/master-todo.md | 448 | - [ ] T0186-d08d T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:182) |
| T1506-db62 | docs/dev/roadmap/v0.3-plus/master-todo.md | 449 | - [ ] T0187-1ae5 T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:183) |
| T1507-89cb | docs/dev/roadmap/v0.3-plus/master-todo.md | 450 | - [ ] T0188-2593 T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:184) |
| T1508-82e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 451 | - [ ] T0189-0db8 T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:185) |
| T1509-40fb | docs/dev/roadmap/v0.3-plus/master-todo.md | 452 | - [ ] T0190-21b4 T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:186) |
| T1510-f67c | docs/dev/roadmap/v0.3-plus/master-todo.md | 453 | - [ ] T0191-6abe T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:187) |
| T1511-50a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 454 | - [ ] T0192-6cf6 T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:188) |
| T1512-2689 | docs/dev/roadmap/v0.3-plus/master-todo.md | 455 | - [ ] T0193-402b T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:189) |
| T1513-729c | docs/dev/roadmap/v0.3-plus/master-todo.md | 456 | - [ ] T0194-9595 T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.2-overview.md:190) |
| T1514-2d9b | docs/dev/roadmap/v0.3-plus/master-todo.md | 457 | - [ ] T0195-dae5 T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.2-overview.md:191) |
| T1515-39ea | docs/dev/roadmap/v0.3-plus/master-todo.md | 458 | - [ ] T0196-e896 T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.2-overview.md:192) |
| T1516-d240 | docs/dev/roadmap/v0.3-plus/master-todo.md | 459 | - [ ] T0197-1ee3 T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.2-overview.md:193) |
| T1517-35b8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 460 | - [ ] T0198-06e7 T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.2-overview.md:194) |
| T1518-1343 | docs/dev/roadmap/v0.3-plus/master-todo.md | 461 | - [ ] T0199-513a T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.2-overview.md:195) |
| T1519-2a47 | docs/dev/roadmap/v0.3-plus/master-todo.md | 462 | - [ ] T0200-28c4 T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.2-overview.md:196) |
| T1520-36fd | docs/dev/roadmap/v0.3-plus/master-todo.md | 463 | - [ ] T0201-42c3 T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.2-overview.md:197) |
| T1521-6e2f | docs/dev/roadmap/v0.3-plus/master-todo.md | 464 | - [ ] T0202-bd4e T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.2-overview.md:198) |
| T1522-4f68 | docs/dev/roadmap/v0.3-plus/master-todo.md | 465 | - [ ] T0203-495f T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.2-overview.md:199) |
| T1523-1359 | docs/dev/roadmap/v0.3-plus/master-todo.md | 466 | - [ ] T0204-be79 T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.2-overview.md:200) |
| T1524-8904 | docs/dev/roadmap/v0.3-plus/master-todo.md | 467 | - [ ] T0205-75ce T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.2-overview.md:201) |
| T1525-8d39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 468 | - [ ] T0206-0fa4 T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.2-overview.md:202) |
| T1526-1d2a | docs/dev/roadmap/v0.3-plus/master-todo.md | 469 | - [ ] T0207-45f9 T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.2-overview.md:203) |
| T1527-33eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 470 | - [ ] T0208-604a T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.2-overview.md:204) |
| T1528-9184 | docs/dev/roadmap/v0.3-plus/master-todo.md | 471 | - [ ] T0209-8385 T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.2-overview.md:205) |
| T1529-446a | docs/dev/roadmap/v0.3-plus/master-todo.md | 472 | - [ ] T0210-83e9 T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.2-overview.md:206) |
| T1530-cbe3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 473 | - [ ] T0211-c2da T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.2-overview.md:207) |
| T1531-15b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 474 | - [ ] T0212-e321 T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.2-overview.md:208) |
| T1532-dd64 | docs/dev/roadmap/v0.3-plus/master-todo.md | 475 | - [ ] T0213-90c2 T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.2-overview.md:209) |
| T1533-8011 | docs/dev/roadmap/v0.3-plus/master-todo.md | 476 | - [ ] T0214-dbb7 T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.2-overview.md:210) |
| T1534-12d8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 477 | - [ ] T0215-45f9 T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.2-overview.md:211) |
| T1535-a231 | docs/dev/roadmap/v0.3-plus/master-todo.md | 478 | - [ ] T0216-c57b T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.2-overview.md:212) |
| T1536-2f73 | docs/dev/roadmap/v0.3-plus/master-todo.md | 479 | - [ ] T0217-24e1 T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.2-overview.md:213) |
| T1537-5888 | docs/dev/roadmap/v0.3-plus/master-todo.md | 480 | - [ ] T0218-68cf T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.2-overview.md:214) |
| T1538-247e | docs/dev/roadmap/v0.3-plus/master-todo.md | 481 | - [ ] T0219-45ed T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.2-overview.md:215) |
| T1539-5e00 | docs/dev/roadmap/v0.3-plus/master-todo.md | 482 | - [ ] T0220-6c4d T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.2-overview.md:216) |
| T1540-6cdc | docs/dev/roadmap/v0.3-plus/master-todo.md | 483 | - [ ] T0221-d81b T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.2-overview.md:217) |
| T1541-2224 | docs/dev/roadmap/v0.3-plus/master-todo.md | 484 | - [ ] T0222-1afc T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.2-overview.md:218) |
| T1542-b148 | docs/dev/roadmap/v0.3-plus/master-todo.md | 485 | - [ ] T0223-cc17 T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.2-overview.md:219) |
| T1543-bff2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 486 | - [ ] T0224-ffd8 T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.2-overview.md:220) |
| T1544-0382 | docs/dev/roadmap/v0.3-plus/master-todo.md | 487 | - [ ] T0225-1977 T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.2-overview.md:221) |
| T1545-f621 | docs/dev/roadmap/v0.3-plus/master-todo.md | 488 | - [ ] T0226-8f55 T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.2-overview.md:222) |
| T1546-4efb | docs/dev/roadmap/v0.3-plus/master-todo.md | 489 | - [ ] T0227-1fb4 T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.2-overview.md:223) |
| T1547-e604 | docs/dev/roadmap/v0.3-plus/master-todo.md | 490 | - [ ] T0228-f631 T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.2-overview.md:224) |
| T1548-07ce | docs/dev/roadmap/v0.3-plus/master-todo.md | 491 | - [ ] T0229-5b09 T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.2-overview.md:225) |
| T1549-1c0e | docs/dev/roadmap/v0.3-plus/master-todo.md | 492 | - [ ] T0230-0992 T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.2-overview.md:226) |
| T1550-58e1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 493 | - [ ] T0231-2147 T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.2-overview.md:227) |
| T1551-043e | docs/dev/roadmap/v0.3-plus/master-todo.md | 494 | - [ ] T0232-2c69 T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.2-overview.md:228) |
| T1552-f9ad | docs/dev/roadmap/v0.3-plus/master-todo.md | 495 | - [ ] T0233-f8fe T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.2-overview.md:229) |
| T1553-f356 | docs/dev/roadmap/v0.3-plus/master-todo.md | 496 | - [ ] T0234-c938 T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.2-overview.md:230) |
| T1554-18ec | docs/dev/roadmap/v0.3-plus/master-todo.md | 497 | - [ ] T0235-6a56 T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.2-overview.md:231) |
| T1555-cd51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 498 | - [ ] T0236-b0d4 T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.2-overview.md:232) |
| T1556-74c3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 499 | - [ ] T0237-7052 T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.2-overview.md:233) |
| T1557-f35c | docs/dev/roadmap/v0.3-plus/master-todo.md | 500 | - [ ] T0238-fa2f T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.2-overview.md:234) |
| T1558-61f7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 501 | - [ ] T0239-3b7d T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.2-overview.md:235) |
| T1559-93fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 502 | - [ ] T0240-d830 T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.2-overview.md:236) |
| T1560-65f1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 503 | - [ ] T0241-c27f T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.2-overview.md:237) |
| T1561-46e0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 504 | - [ ] T0242-9665 T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.2-overview.md:238) |
| T1562-d70b | docs/dev/roadmap/v0.3-plus/master-todo.md | 505 | - [ ] T0243-9fbd T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.2-overview.md:239) |
| T1563-9fa8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 506 | - [ ] T0244-40aa T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.2-overview.md:240) |
| T1564-3485 | docs/dev/roadmap/v0.3-plus/master-todo.md | 507 | - [ ] T0245-6f20 T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.2-overview.md:241) |
| T1565-56c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 508 | - [ ] T0246-a197 T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.2-overview.md:242) |
| T1566-5364 | docs/dev/roadmap/v0.3-plus/master-todo.md | 509 | - [ ] T0247-096c T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.2-overview.md:243) |
| T1567-3c8e | docs/dev/roadmap/v0.3-plus/master-todo.md | 510 | - [ ] T0248-fd6c T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:244) |
| T1568-b0ca | docs/dev/roadmap/v0.3-plus/master-todo.md | 511 | - [ ] T0249-6364 T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:245) |
| T1569-b11b | docs/dev/roadmap/v0.3-plus/master-todo.md | 512 | - [ ] T0250-07e7 T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:246) |
| T1570-10eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 513 | - [ ] T0251-6d34 T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:247) |
| T1571-7771 | docs/dev/roadmap/v0.3-plus/master-todo.md | 514 | - [ ] T0252-df35 T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:248) |
| T1572-e08a | docs/dev/roadmap/v0.3-plus/master-todo.md | 515 | - [ ] T0253-d812 T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:249) |
| T1573-bdd4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 516 | - [ ] T0254-6215 T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:250) |
| T1574-bcf0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 517 | - [ ] T0255-38eb T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:251) |
| T1575-f51c | docs/dev/roadmap/v0.3-plus/master-todo.md | 518 | - [ ] T0256-7713 T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:252) |
| T1576-4cac | docs/dev/roadmap/v0.3-plus/master-todo.md | 519 | - [ ] T0257-698e T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:253) |
| T1577-db4b | docs/dev/roadmap/v0.3-plus/master-todo.md | 520 | - [ ] T0258-6de5 T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:254) |
| T1578-5d4d | docs/dev/roadmap/v0.3-plus/master-todo.md | 521 | - [ ] T0259-8bd2 T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:255) |
| T1579-a1ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 522 | - [ ] T0260-111d T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:256) |
| T1580-354b | docs/dev/roadmap/v0.3-plus/master-todo.md | 523 | - [ ] T0261-bb0f T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:257) |
| T1581-9b93 | docs/dev/roadmap/v0.3-plus/master-todo.md | 524 | - [ ] T0262-a94d T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:258) |
| T1582-4e5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 525 | - [ ] T0263-2ede T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:259) |
| T1583-6a8d | docs/dev/roadmap/v0.3-plus/master-todo.md | 526 | - [ ] T0264-d22a T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:260) |
| T1584-5063 | docs/dev/roadmap/v0.3-plus/master-todo.md | 527 | - [ ] T0265-7d1a T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:261) |
| T1585-fad0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 528 | - [ ] T0266-c7ab T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:262) |
| T1586-9dba | docs/dev/roadmap/v0.3-plus/master-todo.md | 529 | - [ ] T0267-0cf5 T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:263) |
| T1587-0560 | docs/dev/roadmap/v0.3-plus/master-todo.md | 530 | - [ ] T0268-8bdd T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:264) |
| T1588-3fc3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 531 | - [ ] T0269-09d0 T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:265) |
| T1589-1a8e | docs/dev/roadmap/v0.3-plus/master-todo.md | 532 | - [ ] T0270-0a32 T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:266) |
| T1590-b132 | docs/dev/roadmap/v0.3-plus/master-todo.md | 533 | - [ ] T0271-4601 T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:267) |
| T1591-6ca5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 534 | - [ ] T0272-547e T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:268) |
| T1592-5ee5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 535 | - [ ] T0273-4c9f T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:269) |
| T1593-6716 | docs/dev/roadmap/v0.3-plus/master-todo.md | 536 | - [ ] T0274-2185 T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:270) |
| T1594-2d70 | docs/dev/roadmap/v0.3-plus/master-todo.md | 537 | - [ ] T0275-8ba6 T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:271) |
| T1595-65b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 538 | - [ ] T0276-0886 T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:272) |
| T1596-31a8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 539 | - [ ] T0277-9b3c T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:273) |
| T1597-43b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 540 | - [ ] T0278-8770 T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:274) |
| T1598-8416 | docs/dev/roadmap/v0.3-plus/master-todo.md | 541 | - [ ] T0279-65a3 T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:275) |
| T1599-affa | docs/dev/roadmap/v0.3-plus/master-todo.md | 542 | - [ ] T0280-59b1 T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:276) |
| T1600-8754 | docs/dev/roadmap/v0.3-plus/master-todo.md | 543 | - [ ] T0281-404e T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:277) |
| T1601-7fbf | docs/dev/roadmap/v0.3-plus/master-todo.md | 544 | - [ ] T0282-faf0 T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:278) |
| T1602-62b4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 545 | - [ ] T0283-87f9 T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:279) |
| T1603-b40e | docs/dev/roadmap/v0.3-plus/master-todo.md | 546 | - [ ] T0284-1140 T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:280) |
| T1604-1614 | docs/dev/roadmap/v0.3-plus/master-todo.md | 547 | - [ ] T0285-d98b T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:281) |
| T1605-20e4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 548 | - [ ] T0286-016a T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:282) |
| T1606-daf5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 549 | - [ ] T0287-db81 T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:283) |
| T1607-f403 | docs/dev/roadmap/v0.3-plus/master-todo.md | 550 | - [ ] T0288-2f06 T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:284) |
| T1608-e3a0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 551 | - [ ] T0289-665f T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:285) |
| T1609-639d | docs/dev/roadmap/v0.3-plus/master-todo.md | 552 | - [ ] T0290-cae7 T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:286) |
| T1610-8cba | docs/dev/roadmap/v0.3-plus/master-todo.md | 553 | - [ ] T0291-77df T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:287) |
| T1611-38c9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 554 | - [ ] T0292-effb T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:288) |
| T1612-268f | docs/dev/roadmap/v0.3-plus/master-todo.md | 555 | - [ ] T0293-5185 T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:289) |
| T1613-f6c9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 556 | - [ ] T0294-db1c T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:290) |
| T1614-78fd | docs/dev/roadmap/v0.3-plus/master-todo.md | 557 | - [ ] T0295-a73a T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:291) |
| T1615-ae49 | docs/dev/roadmap/v0.3-plus/master-todo.md | 558 | - [ ] T0296-6ded T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:292) |
| T1616-3c2c | docs/dev/roadmap/v0.3-plus/master-todo.md | 559 | - [ ] T0297-c86b T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:293) |
| T1617-9778 | docs/dev/roadmap/v0.3-plus/master-todo.md | 560 | - [ ] T0298-5be9 T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:294) |
| T1618-736a | docs/dev/roadmap/v0.3-plus/master-todo.md | 561 | - [ ] T0299-5adc T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:295) |
| T1619-0d16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 562 | - [ ] T0300-ceff T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:296) |
| T1620-db4e | docs/dev/roadmap/v0.3-plus/master-todo.md | 563 | - [ ] T0301-0486 T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:297) |
| T1621-c3fc | docs/dev/roadmap/v0.3-plus/master-todo.md | 564 | - [ ] T0302-ea26 T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:298) |
| T1622-4da6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 565 | - [ ] T0303-004d T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:299) |
| T1623-cd3f | docs/dev/roadmap/v0.3-plus/master-todo.md | 566 | - [ ] T0304-0dc1 T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:300) |
| T1624-e154 | docs/dev/roadmap/v0.3-plus/master-todo.md | 567 | - [ ] T0305-adc8 T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:301) |
| T1625-9545 | docs/dev/roadmap/v0.3-plus/master-todo.md | 568 | - [ ] T0306-48eb T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:302) |
| T1626-9992 | docs/dev/roadmap/v0.3-plus/master-todo.md | 569 | - [ ] T0307-5ed6 T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:303) |
| T1627-5c05 | docs/dev/roadmap/v0.3-plus/master-todo.md | 570 | - [ ] T0308-d86f T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:304) |
| T1628-5586 | docs/dev/roadmap/v0.3-plus/master-todo.md | 571 | - [ ] T0309-8393 T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:305) |
| T1629-93d7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 572 | - [ ] T0310-8d04 T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:306) |
| T1630-967a | docs/dev/roadmap/v0.3-plus/master-todo.md | 573 | - [ ] T0311-a424 T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:307) |
| T1631-062d | docs/dev/roadmap/v0.3-plus/master-todo.md | 574 | - [ ] T0312-9cfd T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:308) |
| T1632-65d8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 575 | - [ ] T0313-41b0 T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:309) |
| T1633-62b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 576 | - [ ] T0314-0b12 T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:310) |
| T1634-b8fc | docs/dev/roadmap/v0.3-plus/master-todo.md | 577 | - [ ] T0315-640a T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:311) |
| T1635-d2e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 578 | - [ ] T0316-1516 T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:312) |
| T1636-3498 | docs/dev/roadmap/v0.3-plus/master-todo.md | 579 | - [ ] T0317-9ec6 T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:313) |
| T1637-6974 | docs/dev/roadmap/v0.3-plus/master-todo.md | 580 | - [ ] T0318-a391 T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:314) |
| T1638-e390 | docs/dev/roadmap/v0.3-plus/master-todo.md | 581 | - [ ] T0319-991c T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:315) |
| T1639-99e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 582 | - [ ] T0320-5b39 T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.2-overview.md:316) |
| T1640-98e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 583 | - [ ] T0321-4526 T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.2-overview.md:317) |
| T1641-de78 | docs/dev/roadmap/v0.3-plus/master-todo.md | 584 | - [ ] T0322-39ab T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:318) |
| T1642-b7a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 585 | - [ ] T0323-0b47 T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:319) |
| T1643-5d97 | docs/dev/roadmap/v0.3-plus/master-todo.md | 586 | - [ ] T0324-4cb0 T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:320) |
| T1644-5384 | docs/dev/roadmap/v0.3-plus/master-todo.md | 587 | - [ ] T0325-9818 T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:321) |
| T1645-3582 | docs/dev/roadmap/v0.3-plus/master-todo.md | 588 | - [ ] T0326-e1ad T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:322) |
| T1646-0205 | docs/dev/roadmap/v0.3-plus/master-todo.md | 589 | - [ ] T0327-9936 T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:323) |
| T1647-d1d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 590 | - [ ] T0328-e569 T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:324) |
| T1648-7e73 | docs/dev/roadmap/v0.3-plus/master-todo.md | 591 | - [ ] T0329-58a8 T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:325) |
| T1649-46fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 592 | - [ ] T0330-dfa0 T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:326) |
| T1650-2aad | docs/dev/roadmap/v0.3-plus/master-todo.md | 593 | - [ ] T0331-5799 T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.2-overview.md:327) |
| T1651-c85c | docs/dev/roadmap/v0.3-plus/master-todo.md | 594 | - [ ] T0332-4485 T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.2-overview.md:328) |
| T1652-c7ac | docs/dev/roadmap/v0.3-plus/master-todo.md | 595 | - [ ] T0333-d0f6 T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.2-overview.md:329) |
| T1653-01e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 596 | - [ ] T0334-ff96 T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.2-overview.md:330) |
| T1654-0868 | docs/dev/roadmap/v0.3-plus/master-todo.md | 597 | - [ ] T0335-9703 T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.2-overview.md:331) |
| T1655-6ddc | docs/dev/roadmap/v0.3-plus/master-todo.md | 598 | - [ ] T0336-209c T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.2-overview.md:332) |
| T1656-f537 | docs/dev/roadmap/v0.3-plus/master-todo.md | 599 | - [ ] T0337-31ca T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.2-overview.md:333) |
| T1657-07c8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 600 | - [ ] T0338-abf1 T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.2-overview.md:334) |
| T1658-f00a | docs/dev/roadmap/v0.3-plus/master-todo.md | 601 | - [ ] T0339-a36a T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.2-overview.md:335) |
| T1659-9305 | docs/dev/roadmap/v0.3-plus/master-todo.md | 602 | - [ ] T0340-bb3f T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.2-overview.md:336) |
| T1660-4dcf | docs/dev/roadmap/v0.3-plus/master-todo.md | 603 | - [ ] T0341-708f T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.2-overview.md:337) |
| T1661-b0ec | docs/dev/roadmap/v0.3-plus/master-todo.md | 604 | - [ ] T0342-2e90 T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.2-overview.md:338) |
| T1662-71b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 605 | - [ ] T0343-83f7 T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.2-overview.md:339) |
| T1663-b0f4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 606 | - [ ] T0344-0793 T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.2-overview.md:340) |
| T1664-7e88 | docs/dev/roadmap/v0.3-plus/master-todo.md | 607 | - [ ] T0345-5dd2 T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.2-overview.md:341) |
| T1665-da64 | docs/dev/roadmap/v0.3-plus/master-todo.md | 608 | - [ ] T0346-9ce8 T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.2-overview.md:342) |
| T1666-be3f | docs/dev/roadmap/v0.3-plus/master-todo.md | 609 | - [ ] T0347-957c T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.2-overview.md:343) |
| T1667-5017 | docs/dev/roadmap/v0.3-plus/master-todo.md | 610 | - [ ] T0348-d289 T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.2-overview.md:344) |
| T1668-5c15 | docs/dev/roadmap/v0.3-plus/master-todo.md | 611 | - [ ] T0349-36b6 T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.2-overview.md:345) |
| T1669-b12d | docs/dev/roadmap/v0.3-plus/master-todo.md | 612 | - [ ] T0350-2797 T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.2-overview.md:346) |
| T1670-4b49 | docs/dev/roadmap/v0.3-plus/master-todo.md | 613 | - [ ] T0351-00bb T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.2-overview.md:347) |
| T1671-2447 | docs/dev/roadmap/v0.3-plus/master-todo.md | 614 | - [ ] T0352-f33d T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.2-overview.md:348) |
| T1672-1232 | docs/dev/roadmap/v0.3-plus/master-todo.md | 615 | - [ ] T0353-fa4f T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.2-overview.md:349) |
| T1673-ad6a | docs/dev/roadmap/v0.3-plus/master-todo.md | 616 | - [ ] T0354-eb32 T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.2-overview.md:350) |
| T1674-5312 | docs/dev/roadmap/v0.3-plus/master-todo.md | 617 | - [ ] T0355-df06 T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.2-overview.md:351) |
| T1675-9556 | docs/dev/roadmap/v0.3-plus/master-todo.md | 618 | - [ ] T0356-e364 T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.2-overview.md:352) |
| T1676-fbb7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 619 | - [ ] T0357-d372 T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.2-overview.md:353) |
| T1677-f5ea | docs/dev/roadmap/v0.3-plus/master-todo.md | 620 | - [ ] T0358-411f T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.2-overview.md:354) |
| T1678-9ab9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 621 | - [ ] T0359-609d T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.2-overview.md:355) |
| T1679-e335 | docs/dev/roadmap/v0.3-plus/master-todo.md | 622 | - [ ] T0360-a163 T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.2-overview.md:356) |
| T1680-0d02 | docs/dev/roadmap/v0.3-plus/master-todo.md | 623 | - [ ] T0361-e3f7 T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.2-overview.md:357) |
| T1681-982b | docs/dev/roadmap/v0.3-plus/master-todo.md | 624 | - [ ] T0362-0fc9 T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.2-overview.md:358) |
| T1682-919b | docs/dev/roadmap/v0.3-plus/master-todo.md | 625 | - [ ] T0363-7e62 T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.2-overview.md:359) |
| T1683-3108 | docs/dev/roadmap/v0.3-plus/master-todo.md | 626 | - [ ] T0364-c662 T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.2-overview.md:360) |
| T1684-c7fc | docs/dev/roadmap/v0.3-plus/master-todo.md | 627 | - [ ] T0365-c8a1 T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.2-overview.md:361) |
| T1685-efe7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 628 | - [ ] T0366-fb89 T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.2-overview.md:362) |
| T1686-2224 | docs/dev/roadmap/v0.3-plus/master-todo.md | 629 | - [ ] T0367-f414 T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.2-overview.md:363) |
| T1687-4dbf | docs/dev/roadmap/v0.3-plus/master-todo.md | 630 | - [ ] T0368-c9f9 T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.2-overview.md:364) |
| T1688-e76d | docs/dev/roadmap/v0.3-plus/master-todo.md | 631 | - [ ] T0369-b47d T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.2-overview.md:365) |
| T1689-478c | docs/dev/roadmap/v0.3-plus/master-todo.md | 632 | - [ ] T0370-8b59 T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.2-overview.md:366) |
| T1690-45a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 633 | - [ ] T0371-c576 T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.2-overview.md:367) |
| T1691-2180 | docs/dev/roadmap/v0.3-plus/master-todo.md | 634 | - [ ] T0372-25d0 T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.2-overview.md:368) |
| T1692-d23c | docs/dev/roadmap/v0.3-plus/master-todo.md | 635 | - [ ] T0373-ee91 T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.2-overview.md:369) |
| T1693-bc8a | docs/dev/roadmap/v0.3-plus/master-todo.md | 636 | - [ ] T0374-48e9 T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.2-overview.md:370) |
| T1694-3377 | docs/dev/roadmap/v0.3-plus/master-todo.md | 637 | - [ ] T0375-bc2b T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.2-overview.md:371) |
| T1695-d361 | docs/dev/roadmap/v0.3-plus/master-todo.md | 638 | - [ ] T0376-1026 T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.2-overview.md:372) |
| T1696-6eba | docs/dev/roadmap/v0.3-plus/master-todo.md | 639 | - [ ] T0377-6445 T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.2-overview.md:373) |
| T1697-7be8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 640 | - [ ] T0378-9d1f T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.2-overview.md:374) |
| T1698-5d38 | docs/dev/roadmap/v0.3-plus/master-todo.md | 641 | - [ ] T0379-8488 T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.2-overview.md:375) |
| T1699-4169 | docs/dev/roadmap/v0.3-plus/master-todo.md | 642 | - [ ] T0380-bb04 T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.2-overview.md:376) |
| T1700-7ab3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 643 | - [ ] T0381-9815 T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.2-overview.md:377) |
| T1701-3d3f | docs/dev/roadmap/v0.3-plus/master-todo.md | 644 | - [ ] T0382-36f3 T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.2-overview.md:378) |
| T1702-1ed8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 645 | - [ ] T0383-dbc9 T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.2-overview.md:379) |
| T1703-38a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 646 | - [ ] T0384-eb3f T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.2-overview.md:380) |
| T1704-a377 | docs/dev/roadmap/v0.3-plus/master-todo.md | 647 | - [ ] T0385-ec08 T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.2-overview.md:381) |
| T1705-34b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 648 | - [ ] T0386-5337 T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.2-overview.md:382) |
| T1706-8b54 | docs/dev/roadmap/v0.3-plus/master-todo.md | 649 | - [ ] T0387-294c T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.2-overview.md:383) |
| T1707-dea0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 650 | - [ ] T0388-ac9f T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.2-overview.md:384) |
| T1708-fb32 | docs/dev/roadmap/v0.3-plus/master-todo.md | 651 | - [ ] T0389-87f9 T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.2-overview.md:385) |
| T1709-5abb | docs/dev/roadmap/v0.3-plus/master-todo.md | 652 | - [ ] T0390-b2f6 T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.2-overview.md:386) |
| T1710-299a | docs/dev/roadmap/v0.3-plus/master-todo.md | 653 | - [ ] T0391-5af2 T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.2-overview.md:387) |
| T1711-a287 | docs/dev/roadmap/v0.3-plus/master-todo.md | 654 | - [ ] T0392-b5f9 T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.2-overview.md:388) |
| T1712-0bd8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 655 | - [ ] T0393-f9f9 T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.2-overview.md:389) |
| T1713-add1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 656 | - [ ] T0394-5750 T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.2-overview.md:390) |
| T1714-8f53 | docs/dev/roadmap/v0.3-plus/master-todo.md | 657 | - [ ] T0395-617a T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.2-overview.md:391) |
| T1715-08a0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 658 | - [ ] T0396-1b6b T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.2-overview.md:392) |
| T1716-9514 | docs/dev/roadmap/v0.3-plus/master-todo.md | 659 | - [ ] T0397-42f6 T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.2-overview.md:393) |
| T1717-50af | docs/dev/roadmap/v0.3-plus/master-todo.md | 660 | - [ ] T0398-c5e5 T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.2-overview.md:394) |
| T1718-9dd5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 661 | - [ ] T0399-8f5a T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.2-overview.md:395) |
| T1719-154a | docs/dev/roadmap/v0.3-plus/master-todo.md | 662 | - [ ] T0400-9dd2 T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.2-overview.md:396) |
| T1720-b17d | docs/dev/roadmap/v0.3-plus/master-todo.md | 663 | - [ ] T0401-3c46 T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.2-overview.md:397) |
| T1721-3a1e | docs/dev/roadmap/v0.3-plus/master-todo.md | 664 | - [ ] T0402-4454 T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.2-overview.md:398) |
| T1722-42ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 665 | - [ ] T0403-147a T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.2-overview.md:399) |
| T1723-3bc4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 666 | - [ ] T0404-9c10 T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.2-overview.md:400) |
| T1724-a187 | docs/dev/roadmap/v0.3-plus/master-todo.md | 667 | - [ ] T0405-2e18 T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.2-overview.md:401) |
| T1725-032c | docs/dev/roadmap/v0.3-plus/master-todo.md | 668 | - [ ] T0406-3617 T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.2-overview.md:402) |
| T1726-3031 | docs/dev/roadmap/v0.3-plus/master-todo.md | 669 | - [ ] T0407-10b9 T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.2-overview.md:403) |
| T1727-cead | docs/dev/roadmap/v0.3-plus/master-todo.md | 670 | - [ ] T0408-00c0 T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.2-overview.md:404) |
| T1728-b0ec | docs/dev/roadmap/v0.3-plus/master-todo.md | 671 | - [ ] T0409-13fe T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.2-overview.md:405) |
| T1729-3f5d | docs/dev/roadmap/v0.3-plus/master-todo.md | 672 | - [ ] T0410-8137 T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.2-overview.md:406) |
| T1730-a12c | docs/dev/roadmap/v0.3-plus/master-todo.md | 673 | - [ ] T0411-9f65 T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.2-overview.md:407) |
| T1731-abc9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 674 | - [ ] T0412-285e T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.2-overview.md:408) |
| T1732-f713 | docs/dev/roadmap/v0.3-plus/master-todo.md | 675 | - [ ] T0413-50d0 T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.2-overview.md:409) |
| T1733-5b83 | docs/dev/roadmap/v0.3-plus/master-todo.md | 676 | - [ ] T0414-a18e T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.2-overview.md:410) |
| T1734-3b8a | docs/dev/roadmap/v0.3-plus/master-todo.md | 677 | - [ ] T0415-8a8a T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.2-overview.md:411) |
| T1735-b6e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 678 | - [ ] T0416-45d6 T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.2-overview.md:412) |
| T1736-19f9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 679 | - [ ] T0417-2e67 T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.2-overview.md:413) |
| T1737-3371 | docs/dev/roadmap/v0.3-plus/master-todo.md | 680 | - [ ] T0418-7a82 T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.2-overview.md:414) |
| T1738-e95d | docs/dev/roadmap/v0.3-plus/master-todo.md | 681 | - [ ] T0419-8a3a T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.2-overview.md:415) |
| T1739-6d98 | docs/dev/roadmap/v0.3-plus/master-todo.md | 682 | - [ ] T0420-9453 T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.2-overview.md:416) |
| T1740-4245 | docs/dev/roadmap/v0.3-plus/master-todo.md | 683 | - [ ] T0421-32d2 T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.2-overview.md:417) |
| T1741-bc48 | docs/dev/roadmap/v0.3-plus/master-todo.md | 684 | - [ ] T0422-fd2c T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.2-overview.md:418) |
| T1742-76c2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 685 | - [ ] T0423-6119 T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.2-overview.md:419) |
| T1743-9a6b | docs/dev/roadmap/v0.3-plus/master-todo.md | 686 | - [ ] T0424-851a T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.2-overview.md:420) |
| T1744-021c | docs/dev/roadmap/v0.3-plus/master-todo.md | 687 | - [ ] T0425-6401 ## Master TODO (docs/dev/roadmap/v0.3-plus/master-todo.md:4) |
| T1745-2404 | docs/dev/roadmap/v0.3-plus/master-todo.md | 688 | - [ ] T0426-9a06 T0005-eebd Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). (docs/release-checklist-v0.1.md:10) (docs/dev/roadmap/v0.3-plus/master-todo.md:5) |
| T1746-920f | docs/dev/roadmap/v0.3-plus/master-todo.md | 689 | - [ ] T0427-26cb T0006-6c05 **Conftest/OPA Policies** laufen sauber (`make ci-policy`). (docs/release-checklist-v0.1.md:11) (docs/dev/roadmap/v0.3-plus/master-todo.md:6) |
| T1747-dcd3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 690 | - [ ] T0428-536c T0008-1054 **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. (docs/release-checklist-v0.1.md:13) (docs/dev/roadmap/v0.3-plus/master-todo.md:7) |
| T1748-af2b | docs/dev/roadmap/v0.3-plus/master-todo.md | 691 | - [ ] T0429-12f7 T0009-eca0 **Ingress TLS** aktiv (cert-manager, staging Issuer OK). (docs/release-checklist-v0.1.md:14) (docs/dev/roadmap/v0.3-plus/master-todo.md:8) |
| T1749-b25f | docs/dev/roadmap/v0.3-plus/master-todo.md | 692 | - [ ] T0430-6c94 T0010-32fc Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). (docs/release-checklist-v0.1.md:15) (docs/dev/roadmap/v0.3-plus/master-todo.md:9) |
| T1750-13c1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 693 | - [ ] T0431-6544 T0011-4f3a **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). (docs/release-checklist-v0.1.md:21) (docs/dev/roadmap/v0.3-plus/master-todo.md:10) |
| T1751-2d0b | docs/dev/roadmap/v0.3-plus/master-todo.md | 694 | - [ ] T0432-06d2 T0012-d26e **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). (docs/release-checklist-v0.1.md:22) (docs/dev/roadmap/v0.3-plus/master-todo.md:11) |
| T1752-1049 | docs/dev/roadmap/v0.3-plus/master-todo.md | 695 | - [ ] T0433-52fe T0013-d31f **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. (docs/release-checklist-v0.1.md:23) (docs/dev/roadmap/v0.3-plus/master-todo.md:12) |
| T1753-df25 | docs/dev/roadmap/v0.3-plus/master-todo.md | 696 | - [ ] T0434-45db T0014-685a **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. (docs/release-checklist-v0.1.md:24) (docs/dev/roadmap/v0.3-plus/master-todo.md:13) |
| T1754-d3b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 697 | - [ ] T0435-130f T0015-ab33 **Dependabot** aktiviert (pip, npm, GitHub Actions). (docs/release-checklist-v0.1.md:25) (docs/dev/roadmap/v0.3-plus/master-todo.md:14) |
| T1755-5206 | docs/dev/roadmap/v0.3-plus/master-todo.md | 698 | - [ ] T0436-e5ab T0016-8f65 **Trivy Scan** ohne kritische Findings. (docs/release-checklist-v0.1.md:26) (docs/dev/roadmap/v0.3-plus/master-todo.md:15) |
| T1756-f349 | docs/dev/roadmap/v0.3-plus/master-todo.md | 699 | - [ ] T0437-c7e5 T0017-3458 **dbt build/test** grün (Seeds, Models, Tests). (docs/release-checklist-v0.1.md:32) (docs/dev/roadmap/v0.3-plus/master-todo.md:16) |
| T1757-78fa | docs/dev/roadmap/v0.3-plus/master-todo.md | 700 | - [ ] T0438-cf27 T0018-2aca **dbt docs generate** erzeugt Artefakt (Docs erreichbar). (docs/release-checklist-v0.1.md:33) (docs/dev/roadmap/v0.3-plus/master-todo.md:17) |
| T1758-7d2a | docs/dev/roadmap/v0.3-plus/master-todo.md | 701 | - [ ] T0439-fe92 T0019-8c28 **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). (docs/release-checklist-v0.1.md:34) (docs/dev/roadmap/v0.3-plus/master-todo.md:18) |
| T1759-32d5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 702 | - [ ] T0440-7501 T0020-3e64 **Exposures** definiert (Superset Dashboards verlinkt). (docs/release-checklist-v0.1.md:35) (docs/dev/roadmap/v0.3-plus/master-todo.md:19) |
| T1760-c49b | docs/dev/roadmap/v0.3-plus/master-todo.md | 703 | - [ ] T0441-9009 T0021-5a64 **Freshness Checks** für Sources ohne Errors. (docs/release-checklist-v0.1.md:36) (docs/dev/roadmap/v0.3-plus/master-todo.md:20) |
| T1761-5315 | docs/dev/roadmap/v0.3-plus/master-todo.md | 704 | - [ ] T0442-a60a T0022-d46f **Superset Dashboard** „analytics_prices“ importiert: (docs/release-checklist-v0.1.md:42) (docs/dev/roadmap/v0.3-plus/master-todo.md:21) |
| T1762-4aa1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 705 | - [ ] T0443-7f53 T0023-887e **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. (docs/release-checklist-v0.1.md:45) (docs/dev/roadmap/v0.3-plus/master-todo.md:22) |
| T1763-bb35 | docs/dev/roadmap/v0.3-plus/master-todo.md | 706 | - [ ] T0444-f768 T0024-7e0b Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). (docs/release-checklist-v0.1.md:46) (docs/dev/roadmap/v0.3-plus/master-todo.md:23) |
| T1764-a6d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 707 | - [ ] T0445-714f T0025-b8e1 **Vitest/Playwright Tests** decken Detailseiten ab. (docs/release-checklist-v0.1.md:47) (docs/dev/roadmap/v0.3-plus/master-todo.md:24) |
| T1765-9de4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 708 | - [ ] T0446-b45d T0026-8521 **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. (docs/release-checklist-v0.1.md:53) (docs/dev/roadmap/v0.3-plus/master-todo.md:25) |
| T1766-51d6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 709 | - [ ] T0447-608f T0027-6e44 **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. (docs/release-checklist-v0.1.md:54) (docs/dev/roadmap/v0.3-plus/master-todo.md:26) |
| T1767-9b75 | docs/dev/roadmap/v0.3-plus/master-todo.md | 710 | - [ ] T0448-0d43 T0028-d0e1 **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). (docs/release-checklist-v0.1.md:55) (docs/dev/roadmap/v0.3-plus/master-todo.md:27) |
| T1768-c61f | docs/dev/roadmap/v0.3-plus/master-todo.md | 711 | - [ ] T0449-61b2 T0029-574b Restore-Runbook einmal **trocken getestet**. (docs/release-checklist-v0.1.md:56) (docs/dev/roadmap/v0.3-plus/master-todo.md:28) |
| T1769-dbfe | docs/dev/roadmap/v0.3-plus/master-todo.md | 712 | - [ ] T0450-9258 T0030-a42b **OTel Collector** deployed (4317/4318/9464 erreichbar). (docs/release-checklist-v0.1.md:62) (docs/dev/roadmap/v0.3-plus/master-todo.md:29) |
| T1770-1d8d | docs/dev/roadmap/v0.3-plus/master-todo.md | 713 | - [ ] T0451-d097 T0031-3686 **Python Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:63) (docs/dev/roadmap/v0.3-plus/master-todo.md:30) |
| T1771-49f7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 714 | - [ ] T0452-e8dd T0032-50c9 **Node Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:64) (docs/dev/roadmap/v0.3-plus/master-todo.md:31) |
| T1772-807c | docs/dev/roadmap/v0.3-plus/master-todo.md | 715 | - [ ] T0453-f838 T0033-fd89 **Prometheus** scrapt Services; Grafana Panels gefüllt. (docs/release-checklist-v0.1.md:65) (docs/dev/roadmap/v0.3-plus/master-todo.md:32) |
| T1773-0e09 | docs/dev/roadmap/v0.3-plus/master-todo.md | 716 | - [ ] T0454-66c6 T0034-8197 **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). (docs/release-checklist-v0.1.md:66) (docs/dev/roadmap/v0.3-plus/master-todo.md:33) |
| T1774-2d55 | docs/dev/roadmap/v0.3-plus/master-todo.md | 717 | - [ ] T0455-48cd T0035-b3e9 **Loki** enthält Logs aller Services (Promtail shipping OK). (docs/release-checklist-v0.1.md:67) (docs/dev/roadmap/v0.3-plus/master-todo.md:34) |
| T1775-fe77 | docs/dev/roadmap/v0.3-plus/master-todo.md | 718 | - [ ] T0456-4e7e T0036-206b **Grafana Dashboards**: (docs/release-checklist-v0.1.md:68) (docs/dev/roadmap/v0.3-plus/master-todo.md:35) |
| T1776-2cce | docs/dev/roadmap/v0.3-plus/master-todo.md | 719 | - [ ] T0457-74cc T0037-f9ff **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). (docs/release-checklist-v0.1.md:76) (docs/dev/roadmap/v0.3-plus/master-todo.md:36) |
| T1777-7cea | docs/dev/roadmap/v0.3-plus/master-todo.md | 720 | - [ ] T0458-ae07 T0038-f0be **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. (docs/release-checklist-v0.1.md:77) (docs/dev/roadmap/v0.3-plus/master-todo.md:37) |
| T1778-f3d1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 721 | - [ ] T0459-7ce4 T0039-e2d9 **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. (docs/release-checklist-v0.1.md:78) (docs/dev/roadmap/v0.3-plus/master-todo.md:38) |
| T1779-0b46 | docs/dev/roadmap/v0.3-plus/master-todo.md | 722 | - [ ] T0460-298b T0040-8dc3 **Language Policy**: Docs in EN, DE als Appendix. (docs/release-checklist-v0.1.md:79) (docs/dev/roadmap/v0.3-plus/master-todo.md:39) |
| T1780-1e7d | docs/dev/roadmap/v0.3-plus/master-todo.md | 723 | - [ ] T0461-c6ce T0041-72f3 **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. (docs/release-checklist-v0.1.md:80) (docs/dev/roadmap/v0.3-plus/master-todo.md:40) |
| T1781-2274 | docs/dev/roadmap/v0.3-plus/master-todo.md | 724 | - [ ] T0462-1a42 T0042-ffe9 **CI Docs-Checks** grün (markdownlint, link check, doctoc). (docs/release-checklist-v0.1.md:81) (docs/dev/roadmap/v0.3-plus/master-todo.md:41) |
| T1782-0a4f | docs/dev/roadmap/v0.3-plus/master-todo.md | 725 | - [ ] T0463-1b57 T0043-60e9 **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. (docs/release-checklist-v0.1.md:87) (docs/dev/roadmap/v0.3-plus/master-todo.md:42) |
| T1783-e877 | docs/dev/roadmap/v0.3-plus/master-todo.md | 726 | - [ ] T0464-99f5 T0044-c003 **Ingress Hosts** & TLS validiert. (docs/release-checklist-v0.1.md:88) (docs/dev/roadmap/v0.3-plus/master-todo.md:43) |
| T1784-4247 | docs/dev/roadmap/v0.3-plus/master-todo.md | 727 | - [ ] T0465-adfd T0045-c622 **Demo-Data Seed** erfolgreich (`make seed-demo`). (docs/release-checklist-v0.1.md:89) (docs/dev/roadmap/v0.3-plus/master-todo.md:44) |
| T1785-f51c | docs/dev/roadmap/v0.3-plus/master-todo.md | 728 | - [ ] T0466-b264 T0046-1aba **Smoke-Test** im Staging: (docs/release-checklist-v0.1.md:90) (docs/dev/roadmap/v0.3-plus/master-todo.md:45) |
| T1786-ef08 | docs/dev/roadmap/v0.3-plus/master-todo.md | 729 | - [ ] T0467-1c3c T0047-63c7 `main` eingefroren, `release/v0.1` Branch erstellt. (docs/release-checklist-v0.1.md:103) (docs/dev/roadmap/v0.3-plus/master-todo.md:46) |
| T1787-8a87 | docs/dev/roadmap/v0.3-plus/master-todo.md | 730 | - [ ] T0468-4b1d T0048-0400 **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). (docs/release-checklist-v0.1.md:104) (docs/dev/roadmap/v0.3-plus/master-todo.md:47) |
| T1788-21e4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 731 | - [ ] T0469-2245 T0049-b6c0 **Release Notes** erstellt (Features, Breaking Changes, Known Issues). (docs/release-checklist-v0.1.md:105) (docs/dev/roadmap/v0.3-plus/master-todo.md:48) |
| T1789-a8f9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 732 | - [ ] T0470-d98e T0050-bac8 **Tag v0.1.0** gesetzt und Release publiziert. (docs/release-checklist-v0.1.md:106) (docs/dev/roadmap/v0.3-plus/master-todo.md:49) |
| T1790-5c1e | docs/dev/roadmap/v0.3-plus/master-todo.md | 733 | - [ ] T0471-b8e8 T0051-3445 Dokumentation zur Installation/Exploration angehängt. (docs/release-checklist-v0.1.md:107) (docs/dev/roadmap/v0.3-plus/master-todo.md:50) |
| T1791-0a39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 734 | - [ ] T0472-9ca4 T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.3-plus/master-todo.md:51) |
| T1792-217c | docs/dev/roadmap/v0.3-plus/master-todo.md | 735 | - [ ] T0473-2d42 T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.3-plus/master-todo.md:52) |
| T1793-5a47 | docs/dev/roadmap/v0.3-plus/master-todo.md | 736 | - [ ] T0474-ab4f T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.3-plus/master-todo.md:53) |
| T1794-5086 | docs/dev/roadmap/v0.3-plus/master-todo.md | 737 | - [ ] T0475-3503 T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.3-plus/master-todo.md:54) |
| T1795-30c2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 738 | - [ ] T0476-27d4 T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.3-plus/master-todo.md:55) |
| T1796-9daf | docs/dev/roadmap/v0.3-plus/master-todo.md | 739 | - [ ] T0477-2a27 T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.3-plus/master-todo.md:56) |
| T1797-d741 | docs/dev/roadmap/v0.3-plus/master-todo.md | 740 | - [ ] T0478-c5b8 T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.3-plus/master-todo.md:57) |
| T1798-9010 | docs/dev/roadmap/v0.3-plus/master-todo.md | 741 | - [ ] T0479-965d T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.3-plus/master-todo.md:58) |
| T1799-d569 | docs/dev/roadmap/v0.3-plus/master-todo.md | 742 | - [ ] T0480-051f T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.3-plus/master-todo.md:59) |
| T1800-5f68 | docs/dev/roadmap/v0.3-plus/master-todo.md | 743 | - [ ] T0481-7c7f T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.3-plus/master-todo.md:60) |
| T1801-6882 | docs/dev/roadmap/v0.3-plus/master-todo.md | 744 | - [ ] T0482-d3d4 T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.3-plus/master-todo.md:61) |
| T1802-090a | docs/dev/roadmap/v0.3-plus/master-todo.md | 745 | - [ ] T0483-074e T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.3-plus/master-todo.md:62) |
| T1803-5d15 | docs/dev/roadmap/v0.3-plus/master-todo.md | 746 | - [ ] T0484-0734 T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.3-plus/master-todo.md:63) |
| T1804-054f | docs/dev/roadmap/v0.3-plus/master-todo.md | 747 | - [ ] T0485-2a5c T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.3-plus/master-todo.md:64) |
| T1805-81f0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 748 | - [ ] T0486-71d2 T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.3-plus/master-todo.md:65) |
| T1806-3caf | docs/dev/roadmap/v0.3-plus/master-todo.md | 749 | - [ ] T0487-0750 T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.3-plus/master-todo.md:66) |
| T1807-42b6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 750 | - [ ] T0488-5602 T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.3-plus/master-todo.md:67) |
| T1808-8b39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 751 | - [ ] T0489-ebd5 T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.3-plus/master-todo.md:68) |
| T1809-9067 | docs/dev/roadmap/v0.3-plus/master-todo.md | 752 | - [ ] T0490-88e9 T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.3-plus/master-todo.md:69) |
| T1810-28a5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 753 | - [ ] T0491-016c T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.3-plus/master-todo.md:70) |
| T1811-8980 | docs/dev/roadmap/v0.3-plus/master-todo.md | 754 | - [ ] T0492-4372 T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.3-plus/master-todo.md:71) |
| T1812-1261 | docs/dev/roadmap/v0.3-plus/master-todo.md | 755 | - [ ] T0493-1e7f T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.3-plus/master-todo.md:72) |
| T1813-cfd3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 756 | - [ ] T0494-71ba T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.3-plus/master-todo.md:73) |
| T1814-fd0e | docs/dev/roadmap/v0.3-plus/master-todo.md | 757 | - [ ] T0495-ad81 T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.3-plus/master-todo.md:74) |
| T1815-4fb7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 758 | - [ ] T0496-e7b7 T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.3-plus/master-todo.md:75) |
| T1816-5a89 | docs/dev/roadmap/v0.3-plus/master-todo.md | 759 | - [ ] T0497-85ac T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.3-plus/master-todo.md:76) |
| T1817-8db4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 760 | - [ ] T0498-b097 T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.3-plus/master-todo.md:77) |
| T1818-2366 | docs/dev/roadmap/v0.3-plus/master-todo.md | 761 | - [ ] T0499-49c1 T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.3-plus/master-todo.md:78) |
| T1819-f978 | docs/dev/roadmap/v0.3-plus/master-todo.md | 762 | - [ ] T0500-cd7f T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.3-plus/master-todo.md:79) |
| T1820-2193 | docs/dev/roadmap/v0.3-plus/master-todo.md | 763 | - [ ] T0501-3f1d T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.3-plus/master-todo.md:80) |
| T1821-5df4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 764 | - [ ] T0502-f88f T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.3-plus/master-todo.md:81) |
| T1822-805b | docs/dev/roadmap/v0.3-plus/master-todo.md | 765 | - [ ] T0503-311e T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.3-plus/master-todo.md:82) |
| T1823-2482 | docs/dev/roadmap/v0.3-plus/master-todo.md | 766 | - [ ] T0504-6011 T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.3-plus/master-todo.md:83) |
| T1824-75c5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 767 | - [ ] T0505-8124 T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.3-plus/master-todo.md:84) |
| T1825-8510 | docs/dev/roadmap/v0.3-plus/master-todo.md | 768 | - [ ] T0506-7991 T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.3-plus/master-todo.md:85) |
| T1826-5d3d | docs/dev/roadmap/v0.3-plus/master-todo.md | 769 | - [ ] T0507-1d26 T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.3-plus/master-todo.md:86) |
| T1827-45ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 770 | - [ ] T0508-0b2d T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.3-plus/master-todo.md:87) |
| T1828-b9f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 771 | - [ ] T0509-4dd3 T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.3-plus/master-todo.md:88) |
| T1829-41e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 772 | - [ ] T0510-aee5 T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.3-plus/master-todo.md:89) |
| T1830-e2d7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 773 | - [ ] T0511-7c6b T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.3-plus/master-todo.md:90) |
| T1831-6ab1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 774 | - [ ] T0512-3f1a T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.3-plus/master-todo.md:91) |
| T1832-de64 | docs/dev/roadmap/v0.3-plus/master-todo.md | 775 | - [ ] T0513-3dc4 T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.3-plus/master-todo.md:92) |
| T1833-a951 | docs/dev/roadmap/v0.3-plus/master-todo.md | 776 | - [ ] T0514-c69f T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.3-plus/master-todo.md:93) |
| T1834-c1ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 777 | - [ ] T0515-2b03 T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.3-plus/master-todo.md:94) |
| T1835-536a | docs/dev/roadmap/v0.3-plus/master-todo.md | 778 | - [ ] T0516-5f51 T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.3-plus/master-todo.md:95) |
| T1836-7f2b | docs/dev/roadmap/v0.3-plus/master-todo.md | 779 | - [ ] T0517-9e6d T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.3-plus/master-todo.md:96) |
| T1837-a726 | docs/dev/roadmap/v0.3-plus/master-todo.md | 780 | - [ ] T0518-517a T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.3-plus/master-todo.md:97) |
| T1838-d17e | docs/dev/roadmap/v0.3-plus/master-todo.md | 781 | - [ ] T0519-2362 T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.3-plus/master-todo.md:98) |
| T1839-2fe5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 782 | - [ ] T0520-11fd T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.3-plus/master-todo.md:99) |
| T1840-465d | docs/dev/roadmap/v0.3-plus/master-todo.md | 783 | - [ ] T0521-2178 T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.3-plus/master-todo.md:100) |
| T1841-f0e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 784 | - [ ] T0522-ea7a T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.3-plus/master-todo.md:101) |
| T1842-656c | docs/dev/roadmap/v0.3-plus/master-todo.md | 785 | - [ ] T0523-dd84 T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.3-plus/master-todo.md:102) |
| T1843-0962 | docs/dev/roadmap/v0.3-plus/master-todo.md | 786 | - [ ] T0524-f1c5 T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.3-plus/master-todo.md:103) |
| T1844-10f1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 787 | - [ ] T0525-7c83 T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.3-plus/master-todo.md:104) |
| T1845-5da7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 788 | - [ ] T0526-dba2 T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.3-plus/master-todo.md:105) |
| T1846-b15e | docs/dev/roadmap/v0.3-plus/master-todo.md | 789 | - [ ] T0527-a519 T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.3-plus/master-todo.md:106) |
| T1847-d5da | docs/dev/roadmap/v0.3-plus/master-todo.md | 790 | - [ ] T0528-b982 T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.3-plus/master-todo.md:107) |
| T1848-b874 | docs/dev/roadmap/v0.3-plus/master-todo.md | 791 | - [ ] T0529-fa6d T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.3-plus/master-todo.md:108) |
| T1849-d8c3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 792 | - [ ] T0530-7a84 T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.3-plus/master-todo.md:109) |
| T1850-5d9d | docs/dev/roadmap/v0.3-plus/master-todo.md | 793 | - [ ] T0531-554a T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.3-plus/master-todo.md:110) |
| T1851-bc36 | docs/dev/roadmap/v0.3-plus/master-todo.md | 794 | - [ ] T0532-5ecc T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.3-plus/master-todo.md:111) |
| T1852-c7a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 795 | - [ ] T0533-7fe8 T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.3-plus/master-todo.md:112) |
| T1853-f8b8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 796 | - [ ] T0534-14f9 T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.3-plus/master-todo.md:113) |
| T1854-966f | docs/dev/roadmap/v0.3-plus/master-todo.md | 797 | - [ ] T0535-85ab T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.3-plus/master-todo.md:114) |
| T1855-dc5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 798 | - [ ] T0536-0c49 T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.3-plus/master-todo.md:115) |
| T1856-b7cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 799 | - [ ] T0537-f8c0 T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.3-plus/master-todo.md:116) |
| T1857-5968 | docs/dev/roadmap/v0.3-plus/master-todo.md | 800 | - [ ] T0538-ec90 T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.3-plus/master-todo.md:117) |
| T1858-4a94 | docs/dev/roadmap/v0.3-plus/master-todo.md | 801 | - [ ] T0539-7803 T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.3-plus/master-todo.md:118) |
| T1859-e091 | docs/dev/roadmap/v0.3-plus/master-todo.md | 802 | - [ ] T0540-e904 T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.3-plus/master-todo.md:119) |
| T1860-cf95 | docs/dev/roadmap/v0.3-plus/master-todo.md | 803 | - [ ] T0541-61e6 T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.3-plus/master-todo.md:120) |
| T1861-7987 | docs/dev/roadmap/v0.3-plus/master-todo.md | 804 | - [ ] T0542-fc3f T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.3-plus/master-todo.md:121) |
| T1862-a31e | docs/dev/roadmap/v0.3-plus/master-todo.md | 805 | - [ ] T0543-039f T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.3-plus/master-todo.md:122) |
| T1863-75bf | docs/dev/roadmap/v0.3-plus/master-todo.md | 806 | - [ ] T0544-8ac0 T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.3-plus/master-todo.md:123) |
| T1864-f1ee | docs/dev/roadmap/v0.3-plus/master-todo.md | 807 | - [ ] T0545-df8c T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.3-plus/master-todo.md:124) |
| T1865-1cd1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 808 | - [ ] T0546-5240 T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.3-plus/master-todo.md:125) |
| T1866-5aa5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 809 | - [ ] T0547-d5a4 T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.3-plus/master-todo.md:126) |
| T1867-8116 | docs/dev/roadmap/v0.3-plus/master-todo.md | 810 | - [ ] T0548-ff3b T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.3-plus/master-todo.md:127) |
| T1868-9e7a | docs/dev/roadmap/v0.3-plus/master-todo.md | 811 | - [ ] T0549-566b T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.3-plus/master-todo.md:128) |
| T1869-f5a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 812 | - [ ] T0550-3c09 T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.3-plus/master-todo.md:129) |
| T1870-340a | docs/dev/roadmap/v0.3-plus/master-todo.md | 813 | - [ ] T0551-294c T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.3-plus/master-todo.md:130) |
| T1871-f5f3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 814 | - [ ] T0552-6b02 T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.3-plus/master-todo.md:131) |
| T1872-222f | docs/dev/roadmap/v0.3-plus/master-todo.md | 815 | - [ ] T0553-27dc T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.3-plus/master-todo.md:132) |
| T1873-08a8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 816 | - [ ] T0554-2e5e T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.3-plus/master-todo.md:133) |
| T1874-50df | docs/dev/roadmap/v0.3-plus/master-todo.md | 817 | - [ ] T0555-886e T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.3-plus/master-todo.md:134) |
| T1875-a4e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 818 | - [ ] T0556-ca6d T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.3-plus/master-todo.md:135) |
| T1876-3915 | docs/dev/roadmap/v0.3-plus/master-todo.md | 819 | - [ ] T0557-1e1e T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.3-plus/master-todo.md:136) |
| T1877-2236 | docs/dev/roadmap/v0.3-plus/master-todo.md | 820 | - [ ] T0558-2c36 T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.3-plus/master-todo.md:137) |
| T1878-f3a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 821 | - [ ] T0559-1b27 T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.3-plus/master-todo.md:138) |
| T1879-37d7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 822 | - [ ] T0560-6907 T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.3-plus/master-todo.md:139) |
| T1880-f302 | docs/dev/roadmap/v0.3-plus/master-todo.md | 823 | - [ ] T0561-9669 T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.3-plus/master-todo.md:140) |
| T1881-0497 | docs/dev/roadmap/v0.3-plus/master-todo.md | 824 | - [ ] T0562-896d T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.3-plus/master-todo.md:141) |
| T1882-8556 | docs/dev/roadmap/v0.3-plus/master-todo.md | 825 | - [ ] T0563-e74b T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.3-plus/master-todo.md:142) |
| T1883-0e25 | docs/dev/roadmap/v0.3-plus/master-todo.md | 826 | - [ ] T0564-2f17 T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.3-plus/master-todo.md:143) |
| T1884-7008 | docs/dev/roadmap/v0.3-plus/master-todo.md | 827 | - [ ] T0565-4ce3 T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.3-plus/master-todo.md:144) |
| T1885-edea | docs/dev/roadmap/v0.3-plus/master-todo.md | 828 | - [ ] T0566-85eb T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.3-plus/master-todo.md:145) |
| T1886-ff19 | docs/dev/roadmap/v0.3-plus/master-todo.md | 829 | - [ ] T0567-7ba4 T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.3-plus/master-todo.md:146) |
| T1887-8e89 | docs/dev/roadmap/v0.3-plus/master-todo.md | 830 | - [ ] T0568-ed19 T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.3-plus/master-todo.md:147) |
| T1888-54bd | docs/dev/roadmap/v0.3-plus/master-todo.md | 831 | - [ ] T0569-603b T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.3-plus/master-todo.md:148) |
| T1889-a5d7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 832 | - [ ] T0570-519f T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.3-plus/master-todo.md:149) |
| T1890-cfb9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 833 | - [ ] T0571-1e67 T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.3-plus/master-todo.md:150) |
| T1891-72e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 834 | - [ ] T0572-3783 T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.3-plus/master-todo.md:151) |
| T1892-e673 | docs/dev/roadmap/v0.3-plus/master-todo.md | 835 | - [ ] T0573-a61b T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.3-plus/master-todo.md:152) |
| T1893-3ff5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 836 | - [ ] T0574-421d T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.3-plus/master-todo.md:153) |
| T1894-6090 | docs/dev/roadmap/v0.3-plus/master-todo.md | 837 | - [ ] T0575-b3cd T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.3-plus/master-todo.md:154) |
| T1895-d0ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 838 | - [ ] T0576-e363 T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.3-plus/master-todo.md:155) |
| T1896-d662 | docs/dev/roadmap/v0.3-plus/master-todo.md | 839 | - [ ] T0577-50cd T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.3-plus/master-todo.md:156) |
| T1897-3cad | docs/dev/roadmap/v0.3-plus/master-todo.md | 840 | - [ ] T0578-2063 T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.3-plus/master-todo.md:157) |
| T1898-2504 | docs/dev/roadmap/v0.3-plus/master-todo.md | 841 | - [ ] T0579-1004 T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.3-plus/master-todo.md:158) |
| T1899-72df | docs/dev/roadmap/v0.3-plus/master-todo.md | 842 | - [ ] T0580-b497 T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.3-plus/master-todo.md:159) |
| T1900-50dd | docs/dev/roadmap/v0.3-plus/master-todo.md | 843 | - [ ] T0581-4ba1 T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.3-plus/master-todo.md:160) |
| T1901-c7fd | docs/dev/roadmap/v0.3-plus/master-todo.md | 844 | - [ ] T0582-ab2a T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.3-plus/master-todo.md:161) |
| T1902-a059 | docs/dev/roadmap/v0.3-plus/master-todo.md | 845 | - [ ] T0583-7301 T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.3-plus/master-todo.md:162) |
| T1903-b9c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 846 | - [ ] T0584-b327 T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.3-plus/master-todo.md:163) |
| T1904-02f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 847 | - [ ] T0585-f2e6 T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.3-plus/master-todo.md:164) |
| T1905-3bb9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 848 | - [ ] T0586-0cf1 T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.3-plus/master-todo.md:165) |
| T1906-8182 | docs/dev/roadmap/v0.3-plus/master-todo.md | 849 | - [ ] T0587-e442 T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.3-plus/master-todo.md:166) |
| T1907-0ff9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 850 | - [ ] T0588-13c5 T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.3-plus/master-todo.md:167) |
| T1908-9f7d | docs/dev/roadmap/v0.3-plus/master-todo.md | 851 | - [ ] T0589-88b6 T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.3-plus/master-todo.md:168) |
| T1909-d938 | docs/dev/roadmap/v0.3-plus/master-todo.md | 852 | - [ ] T0590-99ed T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.3-plus/master-todo.md:169) |
| T1910-55d1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 853 | - [ ] T0591-ebf5 T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.3-plus/master-todo.md:170) |
| T1911-0e7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 854 | - [ ] T0592-c6d4 T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.3-plus/master-todo.md:171) |
| T1912-3368 | docs/dev/roadmap/v0.3-plus/master-todo.md | 855 | - [ ] T0593-4467 T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.3-plus/master-todo.md:172) |
| T1913-2738 | docs/dev/roadmap/v0.3-plus/master-todo.md | 856 | - [ ] T0594-8ae7 T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.3-plus/master-todo.md:173) |
| T1914-59de | docs/dev/roadmap/v0.3-plus/master-todo.md | 857 | - [ ] T0595-559d T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.3-plus/master-todo.md:174) |
| T1915-9c68 | docs/dev/roadmap/v0.3-plus/master-todo.md | 858 | - [ ] T0596-1c0f T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.3-plus/master-todo.md:175) |
| T1916-6543 | docs/dev/roadmap/v0.3-plus/master-todo.md | 859 | - [ ] T0597-7476 T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.3-plus/master-todo.md:176) |
| T1917-dea1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 860 | - [ ] T0598-7aed T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.3-plus/master-todo.md:177) |
| T1918-edee | docs/dev/roadmap/v0.3-plus/master-todo.md | 861 | - [ ] T0599-80d0 T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.3-plus/master-todo.md:178) |
| T1919-42b3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 862 | - [ ] T0600-c5e2 T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.3-plus/master-todo.md:179) |
| T1920-911f | docs/dev/roadmap/v0.3-plus/master-todo.md | 863 | - [ ] T0601-1d74 T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.3-plus/master-todo.md:180) |
| T1921-cf03 | docs/dev/roadmap/v0.3-plus/master-todo.md | 864 | - [ ] T0602-21fe T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.3-plus/master-todo.md:181) |
| T1922-f532 | docs/dev/roadmap/v0.3-plus/master-todo.md | 865 | - [ ] T0603-06dc T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.3-plus/master-todo.md:182) |
| T1923-9618 | docs/dev/roadmap/v0.3-plus/master-todo.md | 866 | - [ ] T0604-374b T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.3-plus/master-todo.md:183) |
| T1924-dfeb | docs/dev/roadmap/v0.3-plus/master-todo.md | 867 | - [ ] T0605-be73 T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.3-plus/master-todo.md:184) |
| T1925-acbd | docs/dev/roadmap/v0.3-plus/master-todo.md | 868 | - [ ] T0606-2eac T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.3-plus/master-todo.md:185) |
| T1926-d2a9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 869 | - [ ] T0607-e38b T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.3-plus/master-todo.md:186) |
| T1927-7d37 | docs/dev/roadmap/v0.3-plus/master-todo.md | 870 | - [ ] T0608-3fc3 T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.3-plus/master-todo.md:187) |
| T1928-881d | docs/dev/roadmap/v0.3-plus/master-todo.md | 871 | - [ ] T0609-e623 T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.3-plus/master-todo.md:188) |
| T1929-24c1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 872 | - [ ] T0610-41e5 T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.3-plus/master-todo.md:189) |
| T1930-a0f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 873 | - [ ] T0611-3e54 T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.3-plus/master-todo.md:190) |
| T1931-4f3c | docs/dev/roadmap/v0.3-plus/master-todo.md | 874 | - [ ] T0612-49cc T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.3-plus/master-todo.md:191) |
| T1932-be21 | docs/dev/roadmap/v0.3-plus/master-todo.md | 875 | - [ ] T0613-a48f T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.3-plus/master-todo.md:192) |
| T1933-4720 | docs/dev/roadmap/v0.3-plus/master-todo.md | 876 | - [ ] T0614-30e9 T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.3-plus/master-todo.md:193) |
| T1934-1ec3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 877 | - [ ] T0615-6688 T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.3-plus/master-todo.md:194) |
| T1935-a478 | docs/dev/roadmap/v0.3-plus/master-todo.md | 878 | - [ ] T0616-7337 T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.3-plus/master-todo.md:195) |
| T1936-c57f | docs/dev/roadmap/v0.3-plus/master-todo.md | 879 | - [ ] T0617-e90d T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.3-plus/master-todo.md:196) |
| T1937-6ba9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 880 | - [ ] T0618-533c T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.3-plus/master-todo.md:197) |
| T1938-8480 | docs/dev/roadmap/v0.3-plus/master-todo.md | 881 | - [ ] T0619-68a7 T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.3-plus/master-todo.md:198) |
| T1939-74fb | docs/dev/roadmap/v0.3-plus/master-todo.md | 882 | - [ ] T0620-dbf7 T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.3-plus/master-todo.md:199) |
| T1940-e761 | docs/dev/roadmap/v0.3-plus/master-todo.md | 883 | - [ ] T0621-a0dd T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.3-plus/master-todo.md:200) |
| T1941-d52f | docs/dev/roadmap/v0.3-plus/master-todo.md | 884 | - [ ] T0622-d6e9 T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.3-plus/master-todo.md:201) |
| T1942-3e66 | docs/dev/roadmap/v0.3-plus/master-todo.md | 885 | - [ ] T0623-5476 T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.3-plus/master-todo.md:202) |
| T1943-e47f | docs/dev/roadmap/v0.3-plus/master-todo.md | 886 | - [ ] T0624-29fe T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.3-plus/master-todo.md:203) |
| T1944-b9bc | docs/dev/roadmap/v0.3-plus/master-todo.md | 887 | - [ ] T0625-2eb5 T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.3-plus/master-todo.md:204) |
| T1945-5230 | docs/dev/roadmap/v0.3-plus/master-todo.md | 888 | - [ ] T0626-0cd3 T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.3-plus/master-todo.md:205) |
| T1946-bcff | docs/dev/roadmap/v0.3-plus/master-todo.md | 889 | - [ ] T0627-eed9 T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.3-plus/master-todo.md:206) |
| T1947-d93a | docs/dev/roadmap/v0.3-plus/master-todo.md | 890 | - [ ] T0628-1557 T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.3-plus/master-todo.md:207) |
| T1948-a70a | docs/dev/roadmap/v0.3-plus/master-todo.md | 891 | - [ ] T0629-9636 T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.3-plus/master-todo.md:208) |
| T1949-cce7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 892 | - [ ] T0630-e748 T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.3-plus/master-todo.md:209) |
| T1950-c130 | docs/dev/roadmap/v0.3-plus/master-todo.md | 893 | - [ ] T0631-40d8 T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.3-plus/master-todo.md:210) |
| T1951-2e42 | docs/dev/roadmap/v0.3-plus/master-todo.md | 894 | - [ ] T0632-3249 T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.3-plus/master-todo.md:211) |
| T1952-1d3d | docs/dev/roadmap/v0.3-plus/master-todo.md | 895 | - [ ] T0633-7cc2 T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.3-plus/master-todo.md:212) |
| T1953-b74e | docs/dev/roadmap/v0.3-plus/master-todo.md | 896 | - [ ] T0634-2c34 T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.3-plus/master-todo.md:213) |
| T1954-5d00 | docs/dev/roadmap/v0.3-plus/master-todo.md | 897 | - [ ] T0635-30ed T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.3-plus/master-todo.md:214) |
| T1955-846f | docs/dev/roadmap/v0.3-plus/master-todo.md | 898 | - [ ] T0636-16cf T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.3-plus/master-todo.md:215) |
| T1956-15a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 899 | - [ ] T0637-a41a T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.3-plus/master-todo.md:216) |
| T1957-a073 | docs/dev/roadmap/v0.3-plus/master-todo.md | 900 | - [ ] T0638-febf T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.3-plus/master-todo.md:217) |
| T1958-f4a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 901 | - [ ] T0639-3eed T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.3-plus/master-todo.md:218) |
| T1959-fe6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 902 | - [ ] T0640-d86c T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.3-plus/master-todo.md:219) |
| T1960-7bf3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 903 | - [ ] T0641-4f16 T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.3-plus/master-todo.md:220) |
| T1961-8028 | docs/dev/roadmap/v0.3-plus/master-todo.md | 904 | - [ ] T0642-eba0 T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.3-plus/master-todo.md:221) |
| T1962-8ce8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 905 | - [ ] T0643-eb35 T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.3-plus/master-todo.md:222) |
| T1963-e014 | docs/dev/roadmap/v0.3-plus/master-todo.md | 906 | - [ ] T0644-3679 T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.3-plus/master-todo.md:223) |
| T1964-20b9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 907 | - [ ] T0645-5351 T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.3-plus/master-todo.md:224) |
| T1965-73e0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 908 | - [ ] T0646-6438 T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.3-plus/master-todo.md:225) |
| T1966-ec51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 909 | - [ ] T0647-24d5 T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.3-plus/master-todo.md:226) |
| T1967-37b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 910 | - [ ] T0648-015f T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.3-plus/master-todo.md:227) |
| T1968-b7c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 911 | - [ ] T0649-53b3 T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.3-plus/master-todo.md:228) |
| T1969-baf1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 912 | - [ ] T0650-693c T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.3-plus/master-todo.md:229) |
| T1970-ffae | docs/dev/roadmap/v0.3-plus/master-todo.md | 913 | - [ ] T0651-8fb2 T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.3-plus/master-todo.md:230) |
| T1971-c617 | docs/dev/roadmap/v0.3-plus/master-todo.md | 914 | - [ ] T0652-6102 T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.3-plus/master-todo.md:231) |
| T1972-d3d1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 915 | - [ ] T0653-3441 T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.3-plus/master-todo.md:232) |
| T1973-2441 | docs/dev/roadmap/v0.3-plus/master-todo.md | 916 | - [ ] T0654-4ade T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.3-plus/master-todo.md:233) |
| T1974-c892 | docs/dev/roadmap/v0.3-plus/master-todo.md | 917 | - [ ] T0655-3991 T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.3-plus/master-todo.md:234) |
| T1975-a11e | docs/dev/roadmap/v0.3-plus/master-todo.md | 918 | - [ ] T0656-282a T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.3-plus/master-todo.md:235) |
| T1976-6a5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 919 | - [ ] T0657-342b T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.3-plus/master-todo.md:236) |
| T1977-cb80 | docs/dev/roadmap/v0.3-plus/master-todo.md | 920 | - [ ] T0658-130b T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.3-plus/master-todo.md:237) |
| T1978-7c3d | docs/dev/roadmap/v0.3-plus/master-todo.md | 921 | - [ ] T0659-29f8 T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.3-plus/master-todo.md:238) |
| T1979-dd96 | docs/dev/roadmap/v0.3-plus/master-todo.md | 922 | - [ ] T0660-484c T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.3-plus/master-todo.md:239) |
| T1980-7e35 | docs/dev/roadmap/v0.3-plus/master-todo.md | 923 | - [ ] T0661-1370 T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.3-plus/master-todo.md:240) |
| T1981-5f3c | docs/dev/roadmap/v0.3-plus/master-todo.md | 924 | - [ ] T0662-f84c T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.3-plus/master-todo.md:241) |
| T1982-2ea0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 925 | - [ ] T0663-a236 T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.3-plus/master-todo.md:242) |
| T1983-42d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 926 | - [ ] T0664-5ce4 T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.3-plus/master-todo.md:243) |
| T1984-948b | docs/dev/roadmap/v0.3-plus/master-todo.md | 927 | - [ ] T0665-45a5 T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.3-plus/master-todo.md:244) |
| T1985-b641 | docs/dev/roadmap/v0.3-plus/master-todo.md | 928 | - [ ] T0666-47d5 T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.3-plus/master-todo.md:245) |
| T1986-671a | docs/dev/roadmap/v0.3-plus/master-todo.md | 929 | - [ ] T0667-36c7 T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.3-plus/master-todo.md:246) |
| T1987-c6e0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 930 | - [ ] T0668-775d T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.3-plus/master-todo.md:247) |
| T1988-49ac | docs/dev/roadmap/v0.3-plus/master-todo.md | 931 | - [ ] T0669-6ce7 T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.3-plus/master-todo.md:248) |
| T1989-5d29 | docs/dev/roadmap/v0.3-plus/master-todo.md | 932 | - [ ] T0670-bdfe T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.3-plus/master-todo.md:249) |
| T1990-cd91 | docs/dev/roadmap/v0.3-plus/master-todo.md | 933 | - [ ] T0671-167a T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.3-plus/master-todo.md:250) |
| T1991-6668 | docs/dev/roadmap/v0.3-plus/master-todo.md | 934 | - [ ] T0672-fed5 T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.3-plus/master-todo.md:251) |
| T1992-8ee4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 935 | - [ ] T0673-2b7f T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.3-plus/master-todo.md:252) |
| T1993-9920 | docs/dev/roadmap/v0.3-plus/master-todo.md | 936 | - [ ] T0674-7c0a T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.3-plus/master-todo.md:253) |
| T1994-01e9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 937 | - [ ] T0675-1dad T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.3-plus/master-todo.md:254) |
| T1995-3c04 | docs/dev/roadmap/v0.3-plus/master-todo.md | 938 | - [ ] T0676-062d T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.3-plus/master-todo.md:255) |
| T1996-bf90 | docs/dev/roadmap/v0.3-plus/master-todo.md | 939 | - [ ] T0677-5a40 T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.3-plus/master-todo.md:256) |
| T1997-5212 | docs/dev/roadmap/v0.3-plus/master-todo.md | 940 | - [ ] T0678-839d T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.3-plus/master-todo.md:257) |
| T1998-d25a | docs/dev/roadmap/v0.3-plus/master-todo.md | 941 | - [ ] T0679-2a74 T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.3-plus/master-todo.md:258) |
| T1999-2c45 | docs/dev/roadmap/v0.3-plus/master-todo.md | 942 | - [ ] T0680-3ac0 T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.3-plus/master-todo.md:259) |
| T2000-fe7c | docs/dev/roadmap/v0.3-plus/master-todo.md | 943 | - [ ] T0681-305e T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.3-plus/master-todo.md:260) |
| T2001-4c4b | docs/dev/roadmap/v0.3-plus/master-todo.md | 944 | - [ ] T0682-a8c4 T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.3-plus/master-todo.md:261) |
| T2002-fb37 | docs/dev/roadmap/v0.3-plus/master-todo.md | 945 | - [ ] T0683-1a8f T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.3-plus/master-todo.md:262) |
| T2003-4e98 | docs/dev/roadmap/v0.3-plus/master-todo.md | 946 | - [ ] T0684-509e T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.3-plus/master-todo.md:263) |
| T2004-197a | docs/dev/roadmap/v0.3-plus/master-todo.md | 947 | - [ ] T0685-05c7 T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.3-plus/master-todo.md:264) |
| T2005-a763 | docs/dev/roadmap/v0.3-plus/master-todo.md | 948 | - [ ] T0686-d3ba T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.3-plus/master-todo.md:265) |
| T2006-2594 | docs/dev/roadmap/v0.3-plus/master-todo.md | 949 | - [ ] T0687-64e8 T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.3-plus/master-todo.md:266) |
| T2007-762f | docs/dev/roadmap/v0.3-plus/master-todo.md | 950 | - [ ] T0688-05d0 T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.3-plus/master-todo.md:267) |
| T2008-edb1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 951 | - [ ] T0689-9c69 T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.3-plus/master-todo.md:268) |
| T2009-8660 | docs/dev/roadmap/v0.3-plus/master-todo.md | 952 | - [ ] T0690-05cb T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.3-plus/master-todo.md:269) |
| T2010-5d02 | docs/dev/roadmap/v0.3-plus/master-todo.md | 953 | - [ ] T0691-dbf2 T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.3-plus/master-todo.md:270) |
| T2011-de85 | docs/dev/roadmap/v0.3-plus/master-todo.md | 954 | - [ ] T0692-75b9 T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.3-plus/master-todo.md:271) |
| T2012-5ad1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 955 | - [ ] T0693-a46c T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.3-plus/master-todo.md:272) |
| T2013-4fcc | docs/dev/roadmap/v0.3-plus/master-todo.md | 956 | - [ ] T0694-a450 T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.3-plus/master-todo.md:273) |
| T2014-cf1f | docs/dev/roadmap/v0.3-plus/master-todo.md | 957 | - [ ] T0695-f9a5 T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.3-plus/master-todo.md:274) |
| T2015-5064 | docs/dev/roadmap/v0.3-plus/master-todo.md | 958 | - [ ] T0696-f22d T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.3-plus/master-todo.md:275) |
| T2016-7ce1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 959 | - [ ] T0697-d766 T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.3-plus/master-todo.md:276) |
| T2017-cc0a | docs/dev/roadmap/v0.3-plus/master-todo.md | 960 | - [ ] T0698-386b T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.3-plus/master-todo.md:277) |
| T2018-54ca | docs/dev/roadmap/v0.3-plus/master-todo.md | 961 | - [ ] T0699-3aa7 T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.3-plus/master-todo.md:278) |
| T2019-c411 | docs/dev/roadmap/v0.3-plus/master-todo.md | 962 | - [ ] T0700-990b T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.3-plus/master-todo.md:279) |
| T2020-22f4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 963 | - [ ] T0701-c4ba T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.3-plus/master-todo.md:280) |
| T2021-a769 | docs/dev/roadmap/v0.3-plus/master-todo.md | 964 | - [ ] T0702-764a T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.3-plus/master-todo.md:281) |
| T2022-1212 | docs/dev/roadmap/v0.3-plus/master-todo.md | 965 | - [ ] T0703-a453 T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.3-plus/master-todo.md:282) |
| T2023-d3b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 966 | - [ ] T0704-5c4b T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.3-plus/master-todo.md:283) |
| T2024-9cae | docs/dev/roadmap/v0.3-plus/master-todo.md | 967 | - [ ] T0705-eaf7 T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.3-plus/master-todo.md:284) |
| T2025-5563 | docs/dev/roadmap/v0.3-plus/master-todo.md | 968 | - [ ] T0706-5ac0 T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.3-plus/master-todo.md:285) |
| T2026-24f3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 969 | - [ ] T0707-9a20 T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.3-plus/master-todo.md:286) |
| T2027-a19e | docs/dev/roadmap/v0.3-plus/master-todo.md | 970 | - [ ] T0708-6965 T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.3-plus/master-todo.md:287) |
| T2028-f9c1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 971 | - [ ] T0709-e285 T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.3-plus/master-todo.md:288) |
| T2029-27bb | docs/dev/roadmap/v0.3-plus/master-todo.md | 972 | - [ ] T0710-1e03 T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.3-plus/master-todo.md:289) |
| T2030-8f39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 973 | - [ ] T0711-df6c T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.3-plus/master-todo.md:290) |
| T2031-f163 | docs/dev/roadmap/v0.3-plus/master-todo.md | 974 | - [ ] T0712-8e7c T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.3-plus/master-todo.md:291) |
| T2032-764b | docs/dev/roadmap/v0.3-plus/master-todo.md | 975 | - [ ] T0713-a4be T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.3-plus/master-todo.md:292) |
| T2033-c54b | docs/dev/roadmap/v0.3-plus/master-todo.md | 976 | - [ ] T0714-d29c T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.3-plus/master-todo.md:293) |
| T2034-4d0a | docs/dev/roadmap/v0.3-plus/master-todo.md | 977 | - [ ] T0715-466c T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.3-plus/master-todo.md:294) |
| T2035-722c | docs/dev/roadmap/v0.3-plus/master-todo.md | 978 | - [ ] T0716-d0c0 T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.3-plus/master-todo.md:295) |
| T2036-c13a | docs/dev/roadmap/v0.3-plus/master-todo.md | 979 | - [ ] T0717-a7f2 T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.3-plus/master-todo.md:296) |
| T2037-7403 | docs/dev/roadmap/v0.3-plus/master-todo.md | 980 | - [ ] T0718-c33d T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.3-plus/master-todo.md:297) |
| T2038-4cb3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 981 | - [ ] T0719-e0e8 T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.3-plus/master-todo.md:298) |
| T2039-8283 | docs/dev/roadmap/v0.3-plus/master-todo.md | 982 | - [ ] T0720-79eb T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.3-plus/master-todo.md:299) |
| T2040-9d6c | docs/dev/roadmap/v0.3-plus/master-todo.md | 983 | - [ ] T0721-6cd7 T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.3-plus/master-todo.md:300) |
| T2041-ee79 | docs/dev/roadmap/v0.3-plus/master-todo.md | 984 | - [ ] T0722-5d19 T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.3-plus/master-todo.md:301) |
| T2042-cdad | docs/dev/roadmap/v0.3-plus/master-todo.md | 985 | - [ ] T0723-3721 T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.3-plus/master-todo.md:302) |
| T2043-a5aa | docs/dev/roadmap/v0.3-plus/master-todo.md | 986 | - [ ] T0724-786a T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.3-plus/master-todo.md:303) |
| T2044-f1e4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 987 | - [ ] T0725-f6a7 T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.3-plus/master-todo.md:304) |
| T2045-57c2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 988 | - [ ] T0726-52df T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.3-plus/master-todo.md:305) |
| T2046-cb00 | docs/dev/roadmap/v0.3-plus/master-todo.md | 989 | - [ ] T0727-be71 T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.3-plus/master-todo.md:306) |
| T2047-75b6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 990 | - [ ] T0728-3b45 T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.3-plus/master-todo.md:307) |
| T2048-1310 | docs/dev/roadmap/v0.3-plus/master-todo.md | 991 | - [ ] T0729-a0ae T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.3-plus/master-todo.md:308) |
| T2049-5d2f | docs/dev/roadmap/v0.3-plus/master-todo.md | 992 | - [ ] T0730-17c8 T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.3-plus/master-todo.md:309) |
| T2050-0743 | docs/dev/roadmap/v0.3-plus/master-todo.md | 993 | - [ ] T0731-7c0b T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.3-plus/master-todo.md:310) |
| T2051-6b47 | docs/dev/roadmap/v0.3-plus/master-todo.md | 994 | - [ ] T0732-a137 T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.3-plus/master-todo.md:311) |
| T2052-21eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 995 | - [ ] T0733-51fb T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.3-plus/master-todo.md:312) |
| T2053-b370 | docs/dev/roadmap/v0.3-plus/master-todo.md | 996 | - [ ] T0734-2754 T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.3-plus/master-todo.md:313) |
| T2054-410c | docs/dev/roadmap/v0.3-plus/master-todo.md | 997 | - [ ] T0735-a419 T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.3-plus/master-todo.md:314) |
| T2055-e296 | docs/dev/roadmap/v0.3-plus/master-todo.md | 998 | - [ ] T0736-0d68 T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.3-plus/master-todo.md:315) |
| T2056-c17e | docs/dev/roadmap/v0.3-plus/master-todo.md | 999 | - [ ] T0737-8372 T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.3-plus/master-todo.md:316) |
| T2057-12ea | docs/dev/roadmap/v0.3-plus/master-todo.md | 1000 | - [ ] T0738-5732 T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.3-plus/master-todo.md:317) |
| T2058-e981 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1001 | - [ ] T0739-7189 T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.3-plus/master-todo.md:318) |
| T2059-1f0a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1002 | - [ ] T0740-83e7 T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.3-plus/master-todo.md:319) |
| T2060-d2d0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1003 | - [ ] T0741-d78f T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.3-plus/master-todo.md:320) |
| T2061-81f9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1004 | - [ ] T0742-ea9c T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.3-plus/master-todo.md:321) |
| T2062-2225 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1005 | - [ ] T0743-4d82 T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.3-plus/master-todo.md:322) |
| T2063-9865 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1006 | - [ ] T0744-7b96 T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.3-plus/master-todo.md:323) |
| T2064-0b5e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1007 | - [ ] T0745-41a2 T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.3-plus/master-todo.md:324) |
| T2065-4fc3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1008 | - [ ] T0746-25e8 T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.3-plus/master-todo.md:325) |
| T2066-8432 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1009 | - [ ] T0747-9f7e T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.3-plus/master-todo.md:326) |
| T2067-3aec | docs/dev/roadmap/v0.3-plus/master-todo.md | 1010 | - [ ] T0748-c83f T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.3-plus/master-todo.md:327) |
| T2068-e58e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1011 | - [ ] T0749-0a93 T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.3-plus/master-todo.md:328) |
| T2069-5053 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1012 | - [ ] T0750-1b2b T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.3-plus/master-todo.md:329) |
| T2070-a81c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1013 | - [ ] T0751-faf8 T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.3-plus/master-todo.md:330) |
| T2071-d099 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1014 | - [ ] T0752-91ab T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.3-plus/master-todo.md:331) |
| T2072-cf72 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1015 | - [ ] T0753-4def T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.3-plus/master-todo.md:332) |
| T2073-150a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1016 | - [ ] T0754-425a T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.3-plus/master-todo.md:333) |
| T2074-445c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1017 | - [ ] T0755-04b8 T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.3-plus/master-todo.md:334) |
| T2075-744a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1018 | - [ ] T0756-2ea4 T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.3-plus/master-todo.md:335) |
| T2076-de10 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1019 | - [ ] T0757-238d T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.3-plus/master-todo.md:336) |
| T2077-32de | docs/dev/roadmap/v0.3-plus/master-todo.md | 1020 | - [ ] T0758-9245 T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.3-plus/master-todo.md:337) |
| T2078-11a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1021 | - [ ] T0759-4b84 T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.3-plus/master-todo.md:338) |
| T2079-0c88 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1022 | - [ ] T0760-42d0 T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.3-plus/master-todo.md:339) |
| T2080-2807 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1023 | - [ ] T0761-ff4c T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.3-plus/master-todo.md:340) |
| T2081-9f16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1024 | - [ ] T0762-1fe8 T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.3-plus/master-todo.md:341) |
| T2082-460c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1025 | - [ ] T0763-0aa2 T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.3-plus/master-todo.md:342) |
| T2083-8e5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1026 | - [ ] T0764-9680 T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.3-plus/master-todo.md:343) |
| T2084-a539 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1027 | - [ ] T0765-22e7 T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.3-plus/master-todo.md:344) |
| T2085-1b5d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1028 | - [ ] T0766-7902 T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.3-plus/master-todo.md:345) |
| T2086-9a39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1029 | - [ ] T0767-dbc8 T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.3-plus/master-todo.md:346) |
| T2087-a427 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1030 | - [ ] T0768-360e T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.3-plus/master-todo.md:347) |
| T2088-c055 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1031 | - [ ] T0769-3c16 T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.3-plus/master-todo.md:348) |
| T2089-c009 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1032 | - [ ] T0770-a3a1 T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.3-plus/master-todo.md:349) |
| T2090-f71c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1033 | - [ ] T0771-d420 T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.3-plus/master-todo.md:350) |
| T2091-d864 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1034 | - [ ] T0772-7ef2 T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.3-plus/master-todo.md:351) |
| T2092-1d16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1035 | - [ ] T0773-583f T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.3-plus/master-todo.md:352) |
| T2093-28f9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1036 | - [ ] T0774-5e45 T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.3-plus/master-todo.md:353) |
| T2094-c3a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1037 | - [ ] T0775-9f2a T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.3-plus/master-todo.md:354) |
| T2095-5de5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1038 | - [ ] T0776-52e3 T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.3-plus/master-todo.md:355) |
| T2096-ac15 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1039 | - [ ] T0777-1bed T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.3-plus/master-todo.md:356) |
| T2097-3a84 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1040 | - [ ] T0778-d143 T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.3-plus/master-todo.md:357) |
| T2098-3420 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1041 | - [ ] T0779-5f5d T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.3-plus/master-todo.md:358) |
| T2099-a7ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 1042 | - [ ] T0780-1349 T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.3-plus/master-todo.md:359) |
| T2100-7ba4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1043 | - [ ] T0781-929c T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.3-plus/master-todo.md:360) |
| T2101-6dea | docs/dev/roadmap/v0.3-plus/master-todo.md | 1044 | - [ ] T0782-4f9d T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.3-plus/master-todo.md:361) |
| T2102-e88c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1045 | - [ ] T0783-8794 T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.3-plus/master-todo.md:362) |
| T2103-e42c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1046 | - [ ] T0784-cb3b T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.3-plus/master-todo.md:363) |
| T2104-9c3a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1047 | - [ ] T0785-712b T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.3-plus/master-todo.md:364) |
| T2105-66e0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1048 | - [ ] T0786-6663 T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.3-plus/master-todo.md:365) |
| T2106-7b65 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1049 | - [ ] T0787-2270 T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.3-plus/master-todo.md:366) |
| T2107-2718 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1050 | - [ ] T0788-ea5f T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.3-plus/master-todo.md:367) |
| T2108-ff01 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1051 | - [ ] T0789-1398 T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.3-plus/master-todo.md:368) |
| T2109-49d9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1052 | - [ ] T0842-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T2110-3727 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1053 | - [ ] T0843-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T2111-dd16 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1054 | - [ ] T0844-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T2112-6b80 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1055 | - [ ] T0845-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T2113-4edd | docs/dev/roadmap/v0.3-plus/master-todo.md | 1056 | - [ ] T0846-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T2114-fb7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1057 | - [ ] T0847-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T2115-1ffd | docs/dev/roadmap/v0.3-plus/master-todo.md | 1058 | - [ ] T0848-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T2116-0c7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1059 | - [ ] T0849-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T2117-17fd | docs/dev/roadmap/v0.3-plus/master-todo.md | 1060 | - [ ] T0850-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T2118-92a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1061 | - [ ] T0851-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T2119-2612 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1062 | - [ ] T0852-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T2120-1102 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1063 | - [ ] T0853-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T2121-c49c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1064 | - [ ] T0854-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T2122-43eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1065 | - [ ] T0855-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T2123-c6bf | docs/dev/roadmap/v0.3-plus/master-todo.md | 1066 | - [ ] T0856-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T2124-d755 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1067 | - [ ] T0857-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T2125-5710 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1068 | - [ ] T0858-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T2126-9ff8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1069 | - [ ] T0859-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T2127-89a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1070 | - [ ] T0860-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T2128-7a5a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1071 | - [ ] T0861-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T2129-cd21 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1072 | - [ ] T0862-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T2130-a3ae | docs/dev/roadmap/v0.3-plus/master-todo.md | 1073 | - [ ] T0863-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T2131-fd82 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1074 | - [ ] T0864-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T2132-09e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1075 | - [ ] T0865-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T2133-e931 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1076 | - [ ] T0866-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T2134-9696 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1077 | - [ ] T0867-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T2135-b0a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1078 | - [ ] T0868-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T2136-7e1d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1079 | - [ ] T0869-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T2137-e52c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1080 | - [ ] T0870-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T2138-e806 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1081 | - [ ] T0871-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T2139-c932 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1082 | - [ ] T0872-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T2140-1c6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1083 | - [ ] T0873-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T2141-93ab | docs/dev/roadmap/v0.3-plus/master-todo.md | 1084 | - [ ] T0874-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T2142-06d8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1085 | - [ ] T0875-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T2143-c8ee | docs/dev/roadmap/v0.3-plus/master-todo.md | 1086 | - [ ] T0876-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T2144-9141 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1087 | - [ ] T0877-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T2145-f683 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1088 | - [ ] T0878-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T2146-755a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1089 | - [ ] T0879-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T2147-b5ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1090 | - [ ] T0880-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T2148-161f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1091 | - [ ] T0881-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T2149-6464 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1092 | - [ ] T0882-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T2150-e98e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1093 | - [ ] T0883-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T2151-9026 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1094 | - [ ] T0884-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T2152-b589 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1095 | - [ ] T0885-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T2153-c85a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1096 | - [ ] T0886-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T2154-533d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1097 | - [ ] T0887-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T2155-afff | docs/dev/roadmap/v0.3-plus/master-todo.md | 1098 | - [ ] T0888-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T2156-cb3f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1099 | - [ ] T0889-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T2157-85eb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1100 | - [ ] T0890-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T2158-6fd4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1101 | - [ ] T0891-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T2159-517a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1102 | - [ ] T0892-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T2160-f85c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1103 | - [ ] T0893-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T2161-3fbb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1104 | - [ ] T0894-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T2162-ab75 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1105 | - [ ] T0895-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T2163-bf1e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1106 | - [ ] T0896-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T2164-6ec5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1107 | - [ ] T0898-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T2165-cdc7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1108 | - [ ] T0899-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T2166-c8d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1109 | - [ ] T0900-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T2167-740b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1110 | - [ ] T0901-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T2168-0023 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1111 | - [ ] T0902-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T2169-9ff9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1112 | - [ ] T0903-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T2170-1229 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1113 | - [ ] T0904-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T2171-f4b7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1114 | - [ ] T0905-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T2172-c417 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1115 | - [ ] T0906-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T2173-3f57 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1116 | - [ ] T0907-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T2174-e188 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1117 | - [ ] T0908-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T2175-0ab8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1118 | - [ ] T0909-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T2176-afe5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1119 | - [ ] T0910-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T2177-ed9d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1120 | - [ ] T0911-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T2178-1e01 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1121 | - [ ] T0912-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T2179-e4ec | docs/dev/roadmap/v0.3-plus/master-todo.md | 1122 | - [ ] T0913-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T2180-b809 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1123 | - [ ] T0914-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T2181-bebb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1124 | - [ ] T0915-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T2182-1c07 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1125 | - [ ] T0916-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T2183-5aab | docs/dev/roadmap/v0.3-plus/master-todo.md | 1126 | - [ ] T0917-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T2184-cff5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1127 | - [ ] T0918-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T2185-69bb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1128 | - [ ] T0919-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T2186-4f6d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1129 | - [ ] T0920-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T2187-3b8a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1130 | - [ ] T0921-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T2188-5522 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1131 | - [ ] T0922-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T2189-1250 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1132 | - [ ] T0923-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T2190-4d73 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1133 | - [ ] T0924-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T2191-e139 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1134 | - [ ] T0925-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T2192-ebac | docs/dev/roadmap/v0.3-plus/master-todo.md | 1135 | - [ ] T0926-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T2193-055c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1136 | - [ ] T0927-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T2194-41ee | docs/dev/roadmap/v0.3-plus/master-todo.md | 1137 | - [ ] T0928-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T2195-9720 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1138 | - [ ] T0929-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T2196-ea86 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1139 | - [ ] T0930-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T2197-b8d9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1140 | - [ ] T0931-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T2198-02d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1141 | - [ ] T0932-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T2199-9a6f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1142 | - [ ] T0933-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T2200-4e24 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1143 | - [ ] T0934-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T2201-fbf4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1144 | - [ ] T0935-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T2202-bb2f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1145 | - [ ] T0936-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T2203-f484 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1146 | - [ ] T0937-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T2204-7acc | docs/dev/roadmap/v0.3-plus/master-todo.md | 1147 | - [ ] T0938-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T2205-66d9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1148 | - [ ] T0939-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T2206-c58a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1149 | - [ ] T0940-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T2207-b630 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1150 | - [ ] T0941-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T2208-8708 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1151 | - [ ] T0942-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T2209-69a9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1152 | - [ ] T0943-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T2210-7db4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1153 | - [ ] T0944-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T2211-3ecd | docs/dev/roadmap/v0.3-plus/master-todo.md | 1154 | - [ ] T0945-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T2212-a7c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1155 | - [ ] T0946-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T2213-0b54 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1156 | - [ ] T0947-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T2214-324b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1157 | - [ ] T0948-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T2215-aa85 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1158 | - [ ] T0949-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T2216-e0ae | docs/dev/roadmap/v0.3-plus/master-todo.md | 1159 | - [ ] T0950-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T2217-d183 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1160 | - [ ] T0951-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T2218-9bc7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1161 | - [ ] T0952-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T2219-aa5c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1162 | - [ ] T0953-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T2220-8c8e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1163 | - [ ] T0954-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T2221-c9fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 1164 | - [ ] T0955-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T2222-b763 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1165 | - [ ] T0956-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T2223-5b65 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1166 | - [ ] T0957-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T2224-821d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1167 | - [ ] T0958-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T2225-7d4d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1168 | - [ ] T0959-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T2226-7bf3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1169 | - [ ] T0960-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T2227-8579 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1170 | - [ ] T0961-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T2228-4c34 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1171 | - [ ] T0962-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T2229-cfc4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1172 | - [ ] T0963-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T2230-188b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1173 | - [ ] T0964-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T2231-ad89 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1174 | - [ ] T0965-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T2232-34cc | docs/dev/roadmap/v0.3-plus/master-todo.md | 1175 | - [ ] T0966-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T2233-8ef0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1176 | - [ ] T0967-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T2234-b854 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1177 | - [ ] T0968-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T2235-550b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1178 | - [ ] T0969-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T2236-e96d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1179 | - [ ] T0970-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T2237-6b44 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1180 | - [ ] T0971-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T2238-b180 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1181 | - [ ] T0972-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T2239-d467 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1182 | - [ ] T0973-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T2240-8a09 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1183 | - [ ] T0974-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T2241-be2c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1184 | - [ ] T0975-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T2242-1d20 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1185 | - [ ] T0977-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T2243-00a9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1186 | - [ ] T0978-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T2244-a0a7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1187 | - [ ] T0979-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T2245-db9f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1188 | - [ ] T0980-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T2246-26c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1189 | - [ ] T0981-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T2247-4342 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1190 | - [ ] T0982-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T2248-f734 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1191 | - [ ] T0983-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T2249-3ea8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1192 | - [ ] T0984-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T2250-f4ea | docs/dev/roadmap/v0.3-plus/master-todo.md | 1193 | - [ ] T0985-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T2251-8ec6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1194 | - [ ] T0986-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T2252-d1c3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1195 | - [ ] T0987-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T2253-d3a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1196 | - [ ] T0988-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T2254-8778 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1197 | - [ ] T0989-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T2255-fa36 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1198 | - [ ] T0990-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T2256-759b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1199 | - [ ] T0991-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T2257-f5ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1200 | - [ ] T0992-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T2258-4734 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1201 | - [ ] T0993-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T2259-12b9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1202 | - [ ] T0994-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T2260-9192 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1203 | - [ ] T0995-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T2261-211e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1204 | - [ ] T0996-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T2262-0bff | docs/dev/roadmap/v0.3-plus/master-todo.md | 1205 | - [ ] T0997-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T2263-1238 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1206 | - [ ] T0998-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T2264-18c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1207 | - [ ] T0999-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T2265-a080 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1208 | - [ ] T1000-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T2266-f234 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1209 | - [ ] T1001-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T2267-34a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1210 | - [ ] T1002-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T2268-0565 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1211 | - [ ] T1003-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T2269-f974 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1212 | - [ ] T1004-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T2270-8c51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1213 | - [ ] T1005-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T2271-0fdc | docs/dev/roadmap/v0.3-plus/master-todo.md | 1214 | - [ ] T1006-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T2272-7749 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1215 | - [ ] T1007-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T2273-71e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1216 | - [ ] T1008-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T2274-69cf | docs/dev/roadmap/v0.3-plus/master-todo.md | 1217 | - [ ] T1009-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T2275-3146 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1218 | - [ ] T1010-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T2276-29e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1219 | - [ ] T1011-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T2277-31ef | docs/dev/roadmap/v0.3-plus/master-todo.md | 1220 | - [ ] T1012-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T2278-d389 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1221 | - [ ] T1013-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T2279-20f7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1222 | - [ ] T1014-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T2280-d426 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1223 | - [ ] T1015-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T2281-13b2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1224 | - [ ] T1016-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T2282-bab1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1225 | - [ ] T1017-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T2283-6de5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1226 | - [ ] T1018-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T2284-cc3e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1227 | - [ ] T1019-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T2285-f9b2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1228 | - [ ] T1020-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T2286-f7c6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1229 | - [ ] T1021-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T2287-d878 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1230 | - [ ] T1022-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T2288-03c0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1231 | - [ ] T1023-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T2289-c366 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1232 | - [ ] T1024-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T2290-e80b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1233 | - [ ] T1025-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T2291-a611 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1234 | - [ ] T1026-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T2292-3b58 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1235 | - [ ] T1027-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T2293-5731 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1236 | - [ ] T1028-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T2294-c58a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1237 | - [ ] T1029-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T2295-ea2e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1238 | - [ ] T1030-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T2296-00ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 1239 | - [ ] T1031-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T2297-551b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1240 | - [ ] T1032-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T2298-7e1a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1241 | - [ ] T1033-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T2299-41a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1242 | - [ ] T1035-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T2300-2448 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1243 | - [ ] T1036-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T2301-99e2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1244 | - [ ] T1037-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T2302-11f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1245 | - [ ] T1038-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T2303-d333 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1246 | - [ ] T1039-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T2304-5ec3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1247 | - [ ] T1040-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T2305-4e6b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1248 | - [ ] T1041-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T2306-1079 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1249 | - [ ] T1042-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T2307-2cca | docs/dev/roadmap/v0.3-plus/master-todo.md | 1250 | - [ ] T1043-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T2308-23ac | docs/dev/roadmap/v0.3-plus/master-todo.md | 1251 | - [ ] T1044-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T2309-68cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 1252 | - [ ] T1045-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T2310-4dd7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1253 | - [ ] T1046-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T2311-7d8f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1254 | - [ ] T1047-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T2312-03c9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1255 | - [ ] T1048-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T2313-ca4f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1256 | - [ ] T1049-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T2314-d085 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1257 | - [ ] T1050-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T2315-e0c8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1258 | - [ ] T1051-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T2316-609b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1259 | - [ ] T1052-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T2317-d896 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1260 | - [ ] T1053-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T2318-26e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1261 | - [ ] T1054-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T2319-cd8e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1262 | - [ ] T1055-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T2320-1e14 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1263 | - [ ] T1056-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T2321-88c8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1264 | - [ ] T1057-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T2322-5aa4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1265 | - [ ] T1058-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T2323-d963 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1266 | - [ ] T1059-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T2324-a535 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1267 | - [ ] T1060-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T2325-2cfa | docs/dev/roadmap/v0.3-plus/master-todo.md | 1268 | - [ ] T1061-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T2326-c403 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1269 | - [ ] T1062-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T2327-b808 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1270 | - [ ] T1063-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T2328-b732 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1271 | - [ ] T1064-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T2329-21d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1272 | - [ ] T1065-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T2330-226f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1273 | - [ ] T1066-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T2331-11e5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1274 | - [ ] T1067-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T2332-1b40 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1275 | - [ ] T1068-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T2333-0189 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1276 | - [ ] T1069-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T2334-e8d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1277 | - [ ] T1070-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T2335-d0d1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1278 | - [ ] T1071-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T2336-3366 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1279 | - [ ] T1072-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T2337-1837 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1280 | - [ ] T1073-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T2338-6b03 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1281 | - [ ] T1074-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T2339-352f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1282 | - [ ] T1075-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T2340-5e3c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1283 | - [ ] T1076-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T2341-7667 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1284 | - [ ] T1077-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T2342-66c5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1285 | - [ ] T1078-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T2343-5f56 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1286 | - [ ] T1079-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T2344-a4e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1287 | - [ ] T1080-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T2345-1397 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1288 | - [ ] T1081-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T2346-af12 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1289 | - [ ] T1082-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T2347-dc56 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1290 | - [ ] T1083-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T2348-44ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1291 | - [ ] T1084-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T2349-d518 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1292 | - [ ] T1085-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T2350-940e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1293 | - [ ] T1086-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T2351-d349 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1294 | - [ ] T1087-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T2352-0e91 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1295 | - [ ] T1088-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T2353-94b4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1296 | - [ ] T1089-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T2354-df80 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1297 | - [ ] T1090-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T2355-a476 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1298 | - [ ] T1091-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T2356-8629 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1299 | - [ ] T1092-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T2357-116b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1300 | - [ ] T1093-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T2358-d174 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1301 | - [ ] T1094-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T2359-e607 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1302 | - [ ] T1095-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T2360-c6b5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1303 | - [ ] T1096-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T2361-ac17 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1304 | - [ ] T1097-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T2362-1ab3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1305 | - [ ] T1098-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T2363-b28c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1306 | - [ ] T1099-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T2364-5411 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1307 | - [ ] T1100-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T2365-729b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1308 | - [ ] T1101-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T2366-9a67 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1309 | - [ ] T1102-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T2367-1eed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1310 | - [ ] T1103-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T2368-cd6a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1311 | - [ ] T1104-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T2369-428c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1312 | - [ ] T1105-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T2370-9019 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1313 | - [ ] T1106-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T2371-08b5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1314 | - [ ] T1107-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T2372-783d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1315 | - [ ] T1108-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T2373-9585 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1316 | - [ ] T1109-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T2374-7f63 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1317 | - [ ] T1110-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T2375-0aff | docs/dev/roadmap/v0.3-plus/master-todo.md | 1318 | - [ ] T1111-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T2376-d84b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1319 | - [ ] T1112-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T2377-cdcb | docs/dev/roadmap/v0.3-plus/master-todo.md | 1320 | - [ ] T1113-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T2378-c64a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1321 | - [ ] T1114-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T2379-238b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1322 | - [ ] T1115-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T2380-399f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1323 | - [ ] T1116-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T2381-ff2c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1324 | - [ ] T1117-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T2382-ad9c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1325 | - [ ] T1118-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T2383-c07f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1326 | - [ ] T1119-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T2384-ece8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1327 | - [ ] T1120-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T2385-fce5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1328 | - [ ] T1121-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T2386-1858 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1329 | - [ ] T1122-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T2387-f407 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1330 | - [ ] T1123-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T2388-2c5d | docs/dev/roadmap/v0.3-plus/master-todo.md | 1331 | - [ ] T1124-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T2389-b19e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1332 | - [ ] T1125-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T2390-a9ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1333 | - [ ] T1126-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T2391-11e1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1334 | - [ ] T1127-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T2392-13d9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1335 | - [ ] T1128-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T2393-3eb1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1336 | - [ ] T1129-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T2394-6258 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1337 | - [ ] T1130-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T2395-f46e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1338 | - [ ] T1131-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T2396-cc23 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1339 | - [ ] T1132-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T2397-374f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1340 | - [ ] T1133-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T2398-094e | docs/dev/roadmap/v0.3-plus/master-todo.md | 1341 | - [ ] T1134-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T2399-ffc7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1342 | - [ ] T1135-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T2400-1837 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1343 | - [ ] T1136-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T2401-9055 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1344 | - [ ] T1137-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T2402-2ac5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1345 | - [ ] T1138-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T2403-de32 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1346 | - [ ] T1139-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T2404-d855 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1347 | - [ ] T1140-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T2405-90c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1348 | - [ ] T1141-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T2406-afb6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1349 | - [ ] T1142-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T2407-50d0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1350 | - [ ] T1143-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T2408-6f6b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1351 | - [ ] T1144-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T2409-788f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1352 | - [ ] T1145-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T2410-e2ed | docs/dev/roadmap/v0.3-plus/master-todo.md | 1353 | - [ ] T1146-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T2411-8dae | docs/dev/roadmap/v0.3-plus/master-todo.md | 1354 | - [ ] T1147-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T2412-248b | docs/dev/roadmap/v0.3-plus/master-todo.md | 1355 | - [ ] T1148-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T2413-aaee | docs/dev/roadmap/v0.3-plus/master-todo.md | 1356 | - [ ] T1149-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T2414-f263 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1357 | - [ ] T1150-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T2415-eeb7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1358 | - [ ] T1151-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T2416-de37 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1359 | - [ ] T1152-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T2417-e48f | docs/dev/roadmap/v0.3-plus/master-todo.md | 1360 | - [ ] T1153-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T2418-29bf | docs/dev/roadmap/v0.3-plus/master-todo.md | 1361 | - [ ] T1154-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T2419-ec3c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1362 | - [ ] T1155-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T2420-d420 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1363 | - [ ] T1156-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T2421-bd92 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1364 | - [ ] T1157-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T2422-68a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1365 | - [ ] T1158-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T2423-4489 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1366 | - [ ] T1159-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T2424-c98a | docs/dev/roadmap/v0.3-plus/master-todo.md | 1367 | - [ ] T1160-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T2425-920c | docs/dev/roadmap/v0.3-plus/master-todo.md | 1368 | - [ ] T1161-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T2426-0b07 | docs/dev/roadmap/v0.3-plus/master-todo.md | 1369 | - [ ] T1162-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T2427-f3b4 | docs/dev/guides/frontend-modernization-setup-guide.md | 282 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T2428-c2f8 | docs/dev/guides/frontend-modernization-setup-guide.md | 283 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T2429-0b66 | docs/dev/guides/frontend-modernization-setup-guide.md | 284 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T2430-4c7a | docs/dev/guides/frontend-modernization-setup-guide.md | 285 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T2431-f285 | docs/dev/guides/frontend-modernization-setup-guide.md | 286 | - [ ] **Search Functionality** - Faceted Search + Results |
| T2432-a6b7 | docs/dev/guides/frontend-modernization-setup-guide.md | 287 | - [ ] **Form Validation** - Error States + Success |
| T2433-1f4d | docs/dev/guides/frontend-modernization-setup-guide.md | 288 | - [ ] **Real-time Updates** - WebSocket Connection |
| T2434-799d | docs/dev/guides/frontend-modernization-setup-guide.md | 289 | - [ ] **Notifications** - Toast Messages |
| T2435-5cbe | docs/dev/guides/frontend-modernization-setup-guide.md | 290 | - [ ] **Charts** - Interactive Visualizations |
| T2436-ea16 | docs/dev/guides/frontend-modernization-setup-guide.md | 291 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T2437-8209 | docs/dev/guides/frontend-modernization-setup-guide.md | 292 | - [ ] **Authentication** - Login/Logout Flow |
| T2438-c63d | docs/dev/guides/frontend-modernization-setup-guide.md | 316 | - [ ] **Bundle Size** < 500KB gzipped |
| T2439-a237 | docs/dev/guides/frontend-modernization-setup-guide.md | 317 | - [ ] **First Contentful Paint** < 1.8s |
| T2440-ca4c | docs/dev/guides/frontend-modernization-setup-guide.md | 318 | - [ ] **Largest Contentful Paint** < 2.5s |
| T2441-ef27 | docs/dev/guides/frontend-modernization-setup-guide.md | 319 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T2442-7b81 | docs/dev/guides/frontend-modernization-setup-guide.md | 320 | - [ ] **First Input Delay** < 100ms |
| T2443-873d | docs/dev/guides/frontend-modernization-setup-guide.md | 450 | - [ ] **Alle Tests bestanden** |
| T2444-ecba | docs/dev/guides/frontend-modernization-setup-guide.md | 451 | - [ ] **Performance Benchmarks erreicht** |
| T2445-ef04 | docs/dev/guides/frontend-modernization-setup-guide.md | 452 | - [ ] **Mobile Testing abgeschlossen** |
| T2446-1f29 | docs/dev/guides/frontend-modernization-setup-guide.md | 453 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T2447-9db3 | docs/dev/guides/frontend-modernization-setup-guide.md | 454 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T2448-ef3a | docs/dev/guides/frontend-modernization-setup-guide.md | 455 | - [ ] **User Acceptance Testing** abgeschlossen |
| T2449-840b | docs/dev/guides/frontend-modernization-setup-guide.md | 456 | - [ ] **Documentation aktualisiert** |
| T2450-b72a | docs/dev/guides/frontend-modernization-setup-guide.md | 457 | - [ ] **Deployment Pipeline getestet** |
| T2451-a573 | docs/dev/guides/frontend-modernization-setup-guide.md | 458 | - [ ] **Monitoring Setup** aktiv |
| T2452-6e20 | docs/dev/guides/frontend-modernization-setup-guide.md | 459 | - [ ] **Rollback Plan** definiert |
| T2453-077a | docs/dev/guides/frontend-modernization.md | 293 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T2454-efe0 | docs/dev/guides/frontend-modernization.md | 294 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T2455-062c | docs/dev/guides/frontend-modernization.md | 295 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T2456-6d5f | docs/dev/guides/frontend-modernization.md | 296 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T2457-7013 | docs/dev/guides/frontend-modernization.md | 297 | - [ ] **Search Functionality** - Faceted Search + Results |
| T2458-d006 | docs/dev/guides/frontend-modernization.md | 298 | - [ ] **Form Validation** - Error States + Success |
| T2459-4533 | docs/dev/guides/frontend-modernization.md | 299 | - [ ] **Real-time Updates** - WebSocket Connection |
| T2460-fc4b | docs/dev/guides/frontend-modernization.md | 300 | - [ ] **Notifications** - Toast Messages |
| T2461-799e | docs/dev/guides/frontend-modernization.md | 301 | - [ ] **Charts** - Interactive Visualizations |
| T2462-2225 | docs/dev/guides/frontend-modernization.md | 302 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T2463-56b4 | docs/dev/guides/frontend-modernization.md | 303 | - [ ] **Authentication** - Login/Logout Flow |
| T2464-8bcb | docs/dev/guides/frontend-modernization.md | 327 | - [ ] **Bundle Size** < 500KB gzipped |
| T2465-78a4 | docs/dev/guides/frontend-modernization.md | 328 | - [ ] **First Contentful Paint** < 1.8s |
| T2466-5b5b | docs/dev/guides/frontend-modernization.md | 329 | - [ ] **Largest Contentful Paint** < 2.5s |
| T2467-aa01 | docs/dev/guides/frontend-modernization.md | 330 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T2468-dddb | docs/dev/guides/frontend-modernization.md | 331 | - [ ] **First Input Delay** < 100ms |
| T2469-5cea | docs/dev/guides/frontend-modernization.md | 461 | - [ ] **Alle Tests bestanden** |
| T2470-ddcd | docs/dev/guides/frontend-modernization.md | 462 | - [ ] **Performance Benchmarks erreicht** |
| T2471-9ff6 | docs/dev/guides/frontend-modernization.md | 463 | - [ ] **Mobile Testing abgeschlossen** |
| T2472-98f3 | docs/dev/guides/frontend-modernization.md | 464 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T2473-7f72 | docs/dev/guides/frontend-modernization.md | 465 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T2474-019f | docs/dev/guides/frontend-modernization.md | 466 | - [ ] **User Acceptance Testing** abgeschlossen |
| T2475-62f0 | docs/dev/guides/frontend-modernization.md | 467 | - [ ] **Documentation aktualisiert** |
| T2476-34a3 | docs/dev/guides/frontend-modernization.md | 468 | - [ ] **Deployment Pipeline getestet** |
| T2477-591e | docs/dev/guides/frontend-modernization.md | 469 | - [ ] **Monitoring Setup** aktiv |
| T2478-4872 | docs/dev/guides/frontend-modernization.md | 470 | - [ ] **Rollback Plan** definiert |
| T2479-49f1 | docs/dev/v0.2/Datenquellen-Cluster.md | 89 | TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! |
| T2480-32c8 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 186 | ## 📋 Tickets (zum TODO-Index hinzufügen) |
| T2481-b2f3 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 233 | ## TODO: |
| T2482-ba97 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 236 | * `TODO-Index.md` (FLOWISE-Tickets anhängen) |
| T2483-f6a2 | docs/dev/v0.2/Preset-Profile.md | 276 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
| T2484-7bc9 | docs/dev/v0.2/Preset-Profile.md | 288 | TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. |
| T2485-7fda | docs/dev/v0.2/TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T2486-96c6 | docs/dev/v0.2/TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T2487-6b53 | docs/dev/v0.2/TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T2488-daa2 | docs/dev/v0.2/TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T2489-f9c4 | docs/dev/v0.2/TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T2490-4020 | docs/dev/v0.2/TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T2491-6751 | docs/dev/v0.2/TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T2492-af05 | docs/dev/v0.2/TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T2493-59b8 | docs/dev/v0.2/TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T2494-67ad | docs/dev/v0.2/TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T2495-b2f1 | docs/dev/v0.2/TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T2496-5835 | docs/dev/v0.2/TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T2497-d447 | docs/dev/v0.2/TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T2498-b65a | docs/dev/v0.2/TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T2499-55a9 | docs/dev/v0.2/TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T2500-691f | docs/dev/v0.2/TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T2501-820c | docs/dev/v0.2/TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T2502-712e | docs/dev/v0.2/TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T2503-2b97 | docs/dev/v0.2/TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T2504-cb63 | docs/dev/v0.2/TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T2505-3943 | docs/dev/v0.2/TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T2506-2398 | docs/dev/v0.2/TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T2507-1740 | docs/dev/v0.2/TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T2508-9abc | docs/dev/v0.2/TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T2509-23ac | docs/dev/v0.2/TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T2510-c222 | docs/dev/v0.2/TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T2511-937e | docs/dev/v0.2/TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T2512-bb52 | docs/dev/v0.2/TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T2513-8977 | docs/dev/v0.2/TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T2514-fcc1 | docs/dev/v0.2/TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T2515-6700 | docs/dev/v0.2/TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T2516-7bb0 | docs/dev/v0.2/TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T2517-aa57 | docs/dev/v0.2/TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T2518-2d51 | docs/dev/v0.2/TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T2519-41cc | docs/dev/v0.2/TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T2520-b872 | docs/dev/v0.2/TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T2521-d2c7 | docs/dev/v0.2/TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T2522-2f80 | docs/dev/v0.2/TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T2523-538c | docs/dev/v0.2/TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T2524-4cbb | docs/dev/v0.2/TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T2525-a931 | docs/dev/v0.2/TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation |
| T2526-f81c | docs/dev/v0.2/TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T2527-a2ff | docs/dev/v0.2/TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T2528-edef | docs/dev/v0.2/TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T2529-0551 | docs/dev/v0.2/TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T2530-2792 | docs/dev/v0.2/TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T2531-6703 | docs/dev/v0.2/TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T2532-83fe | docs/dev/v0.2/TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T2533-2296 | docs/dev/v0.2/TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T2534-0711 | docs/dev/v0.2/TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T2535-bb75 | docs/dev/v0.2/TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T2536-b21c | docs/dev/v0.2/TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T2537-858d | docs/dev/v0.2/TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T2538-fa9a | docs/dev/v0.2/TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T2539-e9a6 | docs/dev/v0.2/TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T2540-12a4 | docs/dev/v0.2/TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T2541-6a23 | docs/dev/v0.2/TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T2542-50df | docs/dev/v0.2/TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T2543-e417 | docs/dev/v0.2/TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T2544-7686 | docs/dev/v0.2/TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T2545-0902 | docs/dev/v0.2/TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T2546-312b | docs/dev/v0.2/TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T2547-486e | docs/dev/v0.2/TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T2548-1fb0 | docs/dev/v0.2/TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T2549-e046 | docs/dev/v0.2/TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T2550-16c0 | docs/dev/v0.2/TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T2551-07d9 | docs/dev/v0.2/TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T2552-120d | docs/dev/v0.2/TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T2553-37a4 | docs/dev/v0.2/TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T2554-f6f0 | docs/dev/v0.2/TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T2555-f47e | docs/dev/v0.2/TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T2556-1e77 | docs/dev/v0.2/TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T2557-7fb2 | docs/dev/v0.2/TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T2558-1c9c | docs/dev/v0.2/TODO-Index.md | 107 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T2559-2fc5 | docs/dev/v0.2/TODO-Index.md | 108 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T2560-5950 | docs/dev/v0.2/TODO-Index.md | 109 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T2561-1e61 | docs/dev/v0.2/TODO-Index.md | 110 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T2562-3e09 | docs/dev/v0.2/TODO-Index.md | 111 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T2563-df0f | docs/dev/v0.2/TODO-Index.md | 112 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T2564-f079 | docs/dev/v0.2/TODO-Index.md | 113 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T2565-5ad2 | docs/dev/v0.2/TODO-Index.md | 114 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T2566-0c05 | docs/dev/v0.2/TODO-Index.md | 115 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T2567-6a13 | docs/dev/v0.2/TODO-Index.md | 116 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T2568-2a9e | docs/dev/v0.2/TODO-Index.md | 117 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T2569-c3e7 | docs/dev/v0.2/Ticket-Checkliste.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T2570-3c74 | docs/dev/v0.2/Ticket-Checkliste.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T2571-8638 | docs/dev/v0.2/Ticket-Checkliste.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T2572-f1eb | docs/dev/v0.2/Ticket-Checkliste.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T2573-ef38 | docs/dev/v0.2/Ticket-Checkliste.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T2574-2c4e | docs/dev/v0.2/Ticket-Checkliste.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T2575-260e | docs/dev/v0.2/Ticket-Checkliste.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T2576-cf39 | docs/dev/v0.2/Ticket-Checkliste.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T2577-c292 | docs/dev/v0.2/Ticket-Checkliste.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T2578-99a5 | docs/dev/v0.2/Ticket-Checkliste.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T2579-bd7b | docs/dev/v0.2/Ticket-Checkliste.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T2580-fd8d | docs/dev/v0.2/Ticket-Checkliste.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T2581-fe9c | docs/dev/v0.2/Ticket-Checkliste.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T2582-fb88 | docs/dev/v0.2/Ticket-Checkliste.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T2583-930a | docs/dev/v0.2/Ticket-Checkliste.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T2584-4371 | docs/dev/v0.2/Ticket-Checkliste.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T2585-a124 | docs/dev/v0.2/Ticket-Checkliste.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T2586-8031 | docs/dev/v0.2/Ticket-Checkliste.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T2587-4e3a | docs/dev/v0.2/Ticket-Checkliste.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T2588-2ecc | docs/dev/v0.2/Ticket-Checkliste.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T2589-2e7e | docs/dev/v0.2/Ticket-Checkliste.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T2590-f5ef | docs/dev/v0.2/Ticket-Checkliste.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T2591-8249 | docs/dev/v0.2/Ticket-Checkliste.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T2592-5343 | docs/dev/v0.2/Ticket-Checkliste.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T2593-f471 | docs/dev/v0.2/Ticket-Checkliste.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T2594-2e62 | docs/dev/v0.2/Ticket-Checkliste.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T2595-7965 | docs/dev/v0.2/Ticket-Checkliste.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T2596-361b | docs/dev/v0.2/Ticket-Checkliste.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T2597-5733 | docs/dev/v0.2/Ticket-Checkliste.md | 46 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T2598-3f9b | docs/dev/v0.2/Ticket-Checkliste.md | 47 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T2599-b3a4 | docs/dev/v0.2/Ticket-Checkliste.md | 48 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T2600-3d06 | docs/dev/v0.2/Ticket-Checkliste.md | 49 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T2601-9f55 | docs/dev/v0.2/Ticket-Checkliste.md | 52 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T2602-5754 | docs/dev/v0.2/Ticket-Checkliste.md | 53 | - [ ] **[NIFI-2]** API Ingest Flow |
| T2603-5b96 | docs/dev/v0.2/Ticket-Checkliste.md | 54 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T2604-33e5 | docs/dev/v0.2/Ticket-Checkliste.md | 55 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T2605-a3e0 | docs/dev/v0.2/Ticket-Checkliste.md | 56 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T2606-61ea | docs/dev/v0.2/Ticket-Checkliste.md | 57 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T2607-916b | docs/dev/v0.2/Ticket-Checkliste.md | 60 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T2608-4960 | docs/dev/v0.2/Ticket-Checkliste.md | 61 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T2609-8ca4 | docs/dev/v0.2/Ticket-Checkliste.md | 62 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T2610-7ca5 | docs/dev/v0.2/Ticket-Checkliste.md | 63 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T2611-0356 | docs/dev/v0.2/Ticket-Checkliste.md | 64 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T2612-212d | docs/dev/v0.2/Ticket-Checkliste.md | 67 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T2613-31f1 | docs/dev/v0.2/Ticket-Checkliste.md | 68 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T2614-4657 | docs/dev/v0.2/Ticket-Checkliste.md | 69 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T2615-cddb | docs/dev/v0.2/Ticket-Checkliste.md | 70 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T2616-f7bd | docs/dev/v0.2/Ticket-Checkliste.md | 71 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T2617-5a2d | docs/dev/v0.2/Ticket-Checkliste.md | 74 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T2618-d15b | docs/dev/v0.2/Ticket-Checkliste.md | 75 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T2619-0844 | docs/dev/v0.2/Ticket-Checkliste.md | 76 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T2620-d223 | docs/dev/v0.2/Ticket-Checkliste.md | 77 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T2621-9bd6 | docs/dev/v0.2/Ticket-Checkliste.md | 78 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T2622-9b01 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) |
| T2623-98e9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T2624-65a0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T2625-bf0a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T2626-c7b2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T2627-a895 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T2628-80a2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T2629-2c6a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T2630-1030 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T2631-3c05 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T2632-7e80 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T2633-d255 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T2634-041e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T2635-fd93 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T2636-3c21 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T2637-41fe | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T2638-9e56 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T2639-3721 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T2640-66bd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T2641-6e54 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T2642-c05d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T2643-0998 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T2644-7ca3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T2645-bfd4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T2646-6ecc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T2647-7ca7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T2648-1b1d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T2649-e05d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T2650-2ffc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T2651-45fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T2652-0b8d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T2653-a0c3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T2654-3f86 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T2655-6b86 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T2656-1d77 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T2657-0c39 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T2658-2ef3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T2659-fc5e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T2660-51d4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T2661-153d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T2662-ddc6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) |
| T2663-ac36 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T2664-a931 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T2665-372c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T2666-fd4e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T2667-8215 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T2668-7ca1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T2669-1981 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T2670-1576 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T2671-68c4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T2672-8604 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T2673-c399 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T2674-106b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T2675-d37d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T2676-9334 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T2677-0715 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T2678-c658 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T2679-8b2d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T2680-7db0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T2681-16e2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T2682-92b0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T2683-4020 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T2684-d4f1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T2685-f488 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T2686-446f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T2687-31b9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T2688-dbcf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T2689-8ce4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T2690-99a1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T2691-a791 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T2692-7d18 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T2693-d21d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T2694-2238 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T2695-6bc3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 105 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T2696-a4e8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 106 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T2697-1c33 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 107 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T2698-a6b4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 108 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T2699-8b5f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 109 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T2700-180b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 110 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T2701-c4b9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 111 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T2702-77fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 112 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T2703-ce13 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 113 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T2704-69fa | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 114 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T2705-f3ee | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 115 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T2706-14e5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 120 | - [ ] **[LEGAL-1]** RAG-Service für Gesetzestexte |
| T2707-4ead | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 121 | - [ ] **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) |
| T2708-2047 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 122 | - [ ] **[LEGAL-3]** NiFi ingest_laws + rag_index |
| T2709-6762 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 123 | - [ ] **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports |
| T2710-2e6c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 124 | - [ ] **[LEGAL-5]** Frontend Tab „Legal/Compliance“ |
| T2711-f1e0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 125 | - [ ] **[LEGAL-6]** Dossier-Vorlage Compliance Report |
| T2712-4708 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 128 | - [ ] **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) |
| T2713-31fc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 129 | - [ ] **[DISINFO-2]** Bot-Likelihood Modul |
| T2714-4f04 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 130 | - [ ] **[DISINFO-3]** Temporal Pattern Detection |
| T2715-9568 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 131 | - [ ] **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier |
| T2716-b1c0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 132 | - [ ] **[DISINFO-5]** Frontend Dashboard Top Narratives |
| T2717-1dcd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 133 | - [ ] **[DISINFO-6]** Fact-Check API Integration |
| T2718-46c1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 136 | - [ ] **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions |
| T2719-a533 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 137 | - [ ] **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions |
| T2720-bb7e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 138 | - [ ] **[SUPPLY-3]** Simulation Engine (Event → Impact) |
| T2721-50dc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 139 | - [ ] **[SUPPLY-4]** n8n Risk Alerts + Impact Reports |
| T2722-2a9c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 140 | - [ ] **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool |
| T2723-08f6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 141 | - [ ] **[SUPPLY-6]** Dossier Supply Chain Risk Report |
| T2724-1d1b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 144 | - [ ] **[FIN-1]** Graph-Schema Accounts/Transfers |
| T2725-a3cc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 145 | - [ ] **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions |
| T2726-fd36 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 146 | - [ ] **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) |
| T2727-3327 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 147 | - [ ] **[FIN-4]** Anomaly Detection Module |
| T2728-2069 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 148 | - [ ] **[FIN-5]** n8n Red Flag Alerts + Escalations |
| T2729-c621 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 149 | - [ ] **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard |
| T2730-6ff2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 150 | - [ ] **[FIN-7]** Dossier Financial Red Flags |
| T2731-67f7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 153 | - [ ] **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social |
| T2732-bf12 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 154 | - [ ] **[GEO-2]** Graph-Schema Events/Assets/Conflicts |
| T2733-aea2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 155 | - [ ] **[GEO-3]** Geo-Time Anomaly Detection |
| T2734-1a1a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 156 | - [ ] **[GEO-4]** n8n Alerts + Conflict Reports |
| T2735-19f9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 157 | - [ ] **[GEO-5]** Frontend Map Dashboard + Timeline |
| T2736-2ee2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 158 | - [ ] **[GEO-6]** Simulation Engine (Eskalations-Szenarien) |
| T2737-2f84 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 159 | - [ ] **[GEO-7]** Dossier Geopolitical Report |
| T2738-e37f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 162 | - [ ] **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators |
| T2739-506b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 163 | - [ ] **[HUM-2]** Graph-Schema Crisis/Indicators/Regions |
| T2740-2b4c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 164 | - [ ] **[HUM-3]** Risk Assessment Modul (ML) |
| T2741-4c5e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 165 | - [ ] **[HUM-4]** n8n Crisis Alerts + Reports |
| T2742-592b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 166 | - [ ] **[HUM-5]** Frontend Crisis Dashboard + Forecast |
| T2743-e6a5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 167 | - [ ] **[HUM-6]** Dossier Humanitarian Crisis Report |
| T2744-dae0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 172 | - [ ] **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) |
| T2745-d4b8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 173 | - [ ] **[CLIMATE-2]** Graph-Schema ClimateIndicators |
| T2746-1637 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 174 | - [ ] **[CLIMATE-3]** CO₂/Emission Scoring Modul |
| T2747-c7e3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 175 | - [ ] **[CLIMATE-4]** n8n Alerts (Emission Targets) |
| T2748-e2e1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 176 | - [ ] **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap |
| T2749-ee18 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 177 | - [ ] **[CLIMATE-6]** Dossier Climate Risk Report |
| T2750-3fb5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 180 | - [ ] **[TECH-1]** NiFi ingest_patents + research_data |
| T2751-3a76 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 181 | - [ ] **[TECH-2]** Graph-Schema Patents/TechTrends |
| T2752-79ca | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 182 | - [ ] **[TECH-3]** Innovation Hotspot Detection |
| T2753-e066 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 183 | - [ ] **[TECH-4]** n8n Tech Trend Reports |
| T2754-2bc7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 184 | - [ ] **[TECH-5]** Frontend Patent/Innovation Graph |
| T2755-9331 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 185 | - [ ] **[TECH-6]** Dossier Technology Trends |
| T2756-1a7d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 188 | - [ ] **[TERROR-1]** Ingest Propaganda Sources (Social, Web) |
| T2757-b3f1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 189 | - [ ] **[TERROR-2]** Graph-Schema TerrorNetworks |
| T2758-27a1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 190 | - [ ] **[TERROR-3]** Finance Flow Analysis |
| T2759-2298 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 191 | - [ ] **[TERROR-4]** n8n Alerts Suspicious Networks |
| T2760-a992 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 192 | - [ ] **[TERROR-5]** Frontend Terror Network Graph |
| T2761-556f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 193 | - [ ] **[TERROR-6]** Dossier Terrorism Threat Report |
| T2762-33d4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 196 | - [ ] **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) |
| T2763-28b2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 197 | - [ ] **[HEALTH-2]** Graph-Schema HealthEvents/Regions |
| T2764-285e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 198 | - [ ] **[HEALTH-3]** Epidemic Outbreak Detection |
| T2765-e099 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 199 | - [ ] **[HEALTH-4]** n8n Health Alerts + Reports |
| T2766-7e5b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 200 | - [ ] **[HEALTH-5]** Frontend Health Dashboard |
| T2767-9566 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 201 | - [ ] **[HEALTH-6]** Dossier Health/Epidemic Report |
| T2768-9be3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 204 | - [ ] **[ETHICS-1]** Ingest Model Cards + AI Incident Data |
| T2769-0224 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 205 | - [ ] **[ETHICS-2]** Graph-Schema Bias/Models/Orgs |
| T2770-72d2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 206 | - [ ] **[ETHICS-3]** Bias Detection Modul |
| T2771-b207 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 207 | - [ ] **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) |
| T2772-2b54 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 208 | - [ ] **[ETHICS-5]** Frontend AI Ethics Dashboard |
| T2773-626b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 209 | - [ ] **[ETHICS-6]** Dossier AI Ethics Report |
| T2774-2501 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 212 | - [ ] **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) |
| T2775-589c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 213 | - [ ] **[MEDIA-2]** Deepfake Detection Modul |
| T2776-695a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 214 | - [ ] **[MEDIA-3]** Graph-Schema MediaAuthenticity |
| T2777-376a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 215 | - [ ] **[MEDIA-4]** n8n Alerts Fake Media |
| T2778-0a9f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 216 | - [ ] **[MEDIA-5]** Frontend Media Forensics Panel |
| T2779-ba2e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 217 | - [ ] **[MEDIA-6]** Dossier Media Authenticity Report |
| T2780-4d93 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 220 | - [ ] **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) |
| T2781-14dc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 221 | - [ ] **[ECON-2]** Graph-Schema EconomicIndicators/Trades |
| T2782-f3ec | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 222 | - [ ] **[ECON-3]** Market Risk Analysis Modul |
| T2783-0cd0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 223 | - [ ] **[ECON-4]** n8n Economic Reports |
| T2784-0bf6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 224 | - [ ] **[ECON-5]** Frontend Economic Dashboard |
| T2785-df2a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 225 | - [ ] **[ECON-6]** Dossier Economic Intelligence Report |
| T2786-6a5b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 228 | - [ ] **[CULTURE-1]** Ingest Social/News/Blog Data |
| T2787-8739 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 229 | - [ ] **[CULTURE-2]** Graph-Schema Narratives/Discourse |
| T2788-0478 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 230 | - [ ] **[CULTURE-3]** Meme/Hashtag Cluster Detection |
| T2789-6ff5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 231 | - [ ] **[CULTURE-4]** n8n Cultural Trend Reports |
| T2790-227c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 232 | - [ ] **[CULTURE-5]** Frontend Cultural Trends Dashboard |
| T2791-d40a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 233 | - [ ] **[CULTURE-6]** Dossier Cultural Intelligence Report |
| T2792-04f8 | docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md | 103 | # 📌 Tickets (zum TODO-Index ergänzen) |
| T2793-72f7 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 3 | - [ ] **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) |
| T2794-5a1c | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 4 | - [ ] **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden |
| T2795-da3e | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 5 | - [ ] **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen |
| T2796-4a5c | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 6 | - [ ] **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix |
| T2797-abac | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 7 | - [ ] **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos |
| T2798-b3ad | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 8 | - [ ] **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle |
| T2799-829b | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 9 | - [ ] **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) |
| T2800-e320 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG-2.md | 27 | - [ ] T0123-abcd1234 Implement NER API in `services/nlp` (docs/dev/roadmap/v0.2-to-build.md:14) |
| T2801-8db7 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG-2.md | 89 | * `docs: integrate TODO index into roadmap files (idempotent)` |
| T2802-6588 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 73 | * `WORK-ON-new_docs/out/todo_index.md` (alle Checkboxen `- [ ]`/`- [x]`/nummerierte, plus `TODO:`/`FIXME:`/`NOTE:`; **mit IDs T####-hash, Datei, Zeile, Text**) |
| T2803-e28e | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 256 | * **Alle** TODOs (Checkboxen + TODO/FIXME/NOTE) in `todo_index.md` mit **IDs + Quelle+Zeile**. |
| T2804-65cf | docs/export/AFFINE.md | 189 | ### **TODO-Index – Ergänzungen** |
| T2805-23b5 | docs/export/AFFINE.md | 191 | > Hänge diesen Block an `docs/TODO-Index.md` an. |
| T2806-d4c0 | docs/export/AFFINE.md | 195 | - [ ] **[EXPORT-1]** Bundle-Builder (md + assets + meta/export.json) |
| T2807-1551 | docs/export/AFFINE.md | 196 | - [ ] **[EXPORT-2]** Graph-Exporter (mermaid.mmd, dot, svg) |
| T2808-66f7 | docs/export/AFFINE.md | 197 | - [ ] **[EXPORT-3]** Canvas-Exporter (excalidraw.json) |
| T2809-35bc | docs/export/AFFINE.md | 198 | - [ ] **[EXPORT-4]** Geo-Exporter (geojson + map.png/svg) |
| T2810-f628 | docs/export/AFFINE.md | 199 | - [ ] **[APPFLOWY-1]** AppFlowy Adapter – Watched Folder |
| T2811-dafa | docs/export/AFFINE.md | 200 | - [ ] **[APPFLOWY-2]** AppFlowy Adapter – API Mode (optional) |
| T2812-52af | docs/export/AFFINE.md | 201 | - [ ] **[AFFINE-1]** AFFiNE Adapter – Watched Folder + Edgeless Import |
| T2813-33b2 | docs/export/AFFINE.md | 202 | - [ ] **[AFFINE-2]** AFFiNE Adapter – API Mode (optional) |
| T2814-5e0d | docs/export/AFFINE.md | 203 | - [ ] **[FE-EXPORT-1]** Frontend Export-Dialog (Targets + Formate) |
| T2815-bb2c | docs/export/AFFINE.md | 204 | - [ ] **[CLI-EXP-1]** CLI `it export dossier/graph/canvas` |
| T2816-678e | docs/export/AFFINE.md | 205 | - [ ] **[N8N-EXP-1]** n8n Nodes `export_to_appflowy` / `export_to_affine` |
| T2817-414d | docs/export/AFFINE.md | 206 | - [ ] **[POLICY-EXP-1]** OPA-Regeln (classification gates) |
| T2818-6936 | docs/export/AFFINE.md | 207 | - [ ] **[VAULT-EXP-1]** Secrets Handling für Adapter-APIs |
| T2819-f262 | docs/export/AFFINE.md | 208 | - [ ] **[QA-EXP-1]** Golden Bundle Tests |
| T2820-63db | docs/export/AFFINE.md | 209 | - [ ] **[QA-EXP-2]** Roundtrip Import Tests |
| T2821-071f | docs/presets/Presets(Profile).md | 303 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
