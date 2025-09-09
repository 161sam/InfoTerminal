| ID | File | Line | Text |
|---|---|---|---|
| T0001-123eec7a | docs/SECURITY_SWEEP.md | 3 | - TODO: Secrets rotieren (Keycloak admin, oauth2-proxy cookie, DB-Passwörter). |
| T0002-9f6d4e2b | docs/SECURITY_SWEEP.md | 4 | - TODO: TLS/Ingress für Prod (Cert-Manager). |
| T0003-95beeb03 | docs/SECURITY_SWEEP.md | 5 | - TODO: Backups für PG/OpenSearch/Neo4j. |
| T0004-08770c5a | docs/TODO-Index.md | 1 | # TODO-Index |
| T0005-eebdb0bc | docs/release-checklist-v0.1.md | 10 | - [ ] Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). |
| T0006-6c054b93 | docs/release-checklist-v0.1.md | 11 | - [ ] **Conftest/OPA Policies** laufen sauber (`make ci-policy`). |
| T0007-7b3c6a97 | docs/release-checklist-v0.1.md | 12 | - [ ] **Secrets entfernt** aus Manifests/Code (`grep -R "password" infra/ services/ \\| grep -v example` → leer). |
| T0008-105487d6 | docs/release-checklist-v0.1.md | 13 | - [ ] **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. |
| T0009-eca070fc | docs/release-checklist-v0.1.md | 14 | - [ ] **Ingress TLS** aktiv (cert-manager, staging Issuer OK). |
| T0010-32fc4428 | docs/release-checklist-v0.1.md | 15 | - [ ] Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). |
| T0011-4f3a4fbb | docs/release-checklist-v0.1.md | 21 | - [ ] **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). |
| T0012-d26eb117 | docs/release-checklist-v0.1.md | 22 | - [ ] **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). |
| T0013-d31f6320 | docs/release-checklist-v0.1.md | 23 | - [ ] **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. |
| T0014-685a9f1c | docs/release-checklist-v0.1.md | 24 | - [ ] **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. |
| T0015-ab336203 | docs/release-checklist-v0.1.md | 25 | - [ ] **Dependabot** aktiviert (pip, npm, GitHub Actions). |
| T0016-8f6509a4 | docs/release-checklist-v0.1.md | 26 | - [ ] **Trivy Scan** ohne kritische Findings. |
| T0017-34585d61 | docs/release-checklist-v0.1.md | 32 | - [ ] **dbt build/test** grün (Seeds, Models, Tests). |
| T0018-2acaec2b | docs/release-checklist-v0.1.md | 33 | - [ ] **dbt docs generate** erzeugt Artefakt (Docs erreichbar). |
| T0019-8c283abc | docs/release-checklist-v0.1.md | 34 | - [ ] **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). |
| T0020-3e64a531 | docs/release-checklist-v0.1.md | 35 | - [ ] **Exposures** definiert (Superset Dashboards verlinkt). |
| T0021-5a64e8a4 | docs/release-checklist-v0.1.md | 36 | - [ ] **Freshness Checks** für Sources ohne Errors. |
| T0022-d46f9a42 | docs/release-checklist-v0.1.md | 42 | - [ ] **Superset Dashboard** „analytics_prices“ importiert: |
| T0023-887e2ee6 | docs/release-checklist-v0.1.md | 45 | - [ ] **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. |
| T0024-7e0be2e1 | docs/release-checklist-v0.1.md | 46 | - [ ] Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). |
| T0025-b8e15dc1 | docs/release-checklist-v0.1.md | 47 | - [ ] **Vitest/Playwright Tests** decken Detailseiten ab. |
| T0026-852109aa | docs/release-checklist-v0.1.md | 53 | - [ ] **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. |
| T0027-6e44531b | docs/release-checklist-v0.1.md | 54 | - [ ] **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. |
| T0028-d0e1d9c3 | docs/release-checklist-v0.1.md | 55 | - [ ] **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). |
| T0029-574bfa1d | docs/release-checklist-v0.1.md | 56 | - [ ] Restore-Runbook einmal **trocken getestet**. |
| T0030-a42b9b1e | docs/release-checklist-v0.1.md | 62 | - [ ] **OTel Collector** deployed (4317/4318/9464 erreichbar). |
| T0031-3686a8ea | docs/release-checklist-v0.1.md | 63 | - [ ] **Python Services** exportieren Traces + `/metrics`. |
| T0032-50c95364 | docs/release-checklist-v0.1.md | 64 | - [ ] **Node Services** exportieren Traces + `/metrics`. |
| T0033-fd890733 | docs/release-checklist-v0.1.md | 65 | - [ ] **Prometheus** scrapt Services; Grafana Panels gefüllt. |
| T0034-81973fbd | docs/release-checklist-v0.1.md | 66 | - [ ] **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). |
| T0035-b3e96bed | docs/release-checklist-v0.1.md | 67 | - [ ] **Loki** enthält Logs aller Services (Promtail shipping OK). |
| T0036-206b6181 | docs/release-checklist-v0.1.md | 68 | - [ ] **Grafana Dashboards**: |
| T0037-f9ff8ace | docs/release-checklist-v0.1.md | 76 | - [ ] **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). |
| T0038-f0bed26f | docs/release-checklist-v0.1.md | 77 | - [ ] **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. |
| T0039-e2d936fa | docs/release-checklist-v0.1.md | 78 | - [ ] **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. |
| T0040-8dc3e1de | docs/release-checklist-v0.1.md | 79 | - [ ] **Language Policy**: Docs in EN, DE als Appendix. |
| T0041-72f3bcfb | docs/release-checklist-v0.1.md | 80 | - [ ] **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. |
| T0042-ffe9d529 | docs/release-checklist-v0.1.md | 81 | - [ ] **CI Docs-Checks** grün (markdownlint, link check, doctoc). |
| T0043-60e9ff73 | docs/release-checklist-v0.1.md | 87 | - [ ] **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. |
| T0044-c0036628 | docs/release-checklist-v0.1.md | 88 | - [ ] **Ingress Hosts** & TLS validiert. |
| T0045-c622e84c | docs/release-checklist-v0.1.md | 89 | - [ ] **Demo-Data Seed** erfolgreich (`make seed-demo`). |
| T0046-1aba4558 | docs/release-checklist-v0.1.md | 90 | - [ ] **Smoke-Test** im Staging: |
| T0047-63c7922a | docs/release-checklist-v0.1.md | 103 | - [ ] `main` eingefroren, `release/v0.1` Branch erstellt. |
| T0048-0400782a | docs/release-checklist-v0.1.md | 104 | - [ ] **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). |
| T0049-b6c0d1dc | docs/release-checklist-v0.1.md | 105 | - [ ] **Release Notes** erstellt (Features, Breaking Changes, Known Issues). |
| T0050-bac8349c | docs/release-checklist-v0.1.md | 106 | - [ ] **Tag v0.1.0** gesetzt und Release publiziert. |
| T0051-34456b6a | docs/release-checklist-v0.1.md | 107 | - [ ] Dokumentation zur Installation/Exploration angehängt. |
| T0052-65cf57fc | docs/export/AFFINE.md | 189 | ### **TODO-Index – Ergänzungen** |
| T0053-23b56cb5 | docs/export/AFFINE.md | 191 | > Hänge diesen Block an `docs/TODO-Index.md` an. |
| T0054-d4c05623 | docs/export/AFFINE.md | 195 | - [ ] **[EXPORT-1]** Bundle-Builder (md + assets + meta/export.json) |
| T0055-1551263f | docs/export/AFFINE.md | 196 | - [ ] **[EXPORT-2]** Graph-Exporter (mermaid.mmd, dot, svg) |
| T0056-66f7054e | docs/export/AFFINE.md | 197 | - [ ] **[EXPORT-3]** Canvas-Exporter (excalidraw.json) |
| T0057-35bcacfc | docs/export/AFFINE.md | 198 | - [ ] **[EXPORT-4]** Geo-Exporter (geojson + map.png/svg) |
| T0058-f6289b76 | docs/export/AFFINE.md | 199 | - [ ] **[APPFLOWY-1]** AppFlowy Adapter – Watched Folder |
| T0059-dafa68d5 | docs/export/AFFINE.md | 200 | - [ ] **[APPFLOWY-2]** AppFlowy Adapter – API Mode (optional) |
| T0060-52af8638 | docs/export/AFFINE.md | 201 | - [ ] **[AFFINE-1]** AFFiNE Adapter – Watched Folder + Edgeless Import |
| T0061-33b2eddd | docs/export/AFFINE.md | 202 | - [ ] **[AFFINE-2]** AFFiNE Adapter – API Mode (optional) |
| T0062-5e0d0572 | docs/export/AFFINE.md | 203 | - [ ] **[FE-EXPORT-1]** Frontend Export-Dialog (Targets + Formate) |
| T0063-bb2cc692 | docs/export/AFFINE.md | 204 | - [ ] **[CLI-EXP-1]** CLI `it export dossier/graph/canvas` |
| T0064-678e914c | docs/export/AFFINE.md | 205 | - [ ] **[N8N-EXP-1]** n8n Nodes `export_to_appflowy` / `export_to_affine` |
| T0065-414d2db2 | docs/export/AFFINE.md | 206 | - [ ] **[POLICY-EXP-1]** OPA-Regeln (classification gates) |
| T0066-6936730f | docs/export/AFFINE.md | 207 | - [ ] **[VAULT-EXP-1]** Secrets Handling für Adapter-APIs |
| T0067-f262bbe0 | docs/export/AFFINE.md | 208 | - [ ] **[QA-EXP-1]** Golden Bundle Tests |
| T0068-63db88d6 | docs/export/AFFINE.md | 209 | - [ ] **[QA-EXP-2]** Roundtrip Import Tests |
| T0069-ac36a5a3 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 425 | ### **TODO-Index Ergänzung (neuer Abschnitt)** |
| T0070-66280530 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 427 | > füge ans Ende von `docs/TODO-Index.md` hinzu: |
| T0071-52c7f6bc | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 431 | - [ ] **[FLOWISE-1]** Flowise Deployment (Container, OIDC via Agent-Gateway) |
| T0072-96226590 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 432 | - [ ] **[FLOWISE-2]** Agent-Gateway (Auth, RBAC, Rate-Limit, Audit, Vault) |
| T0073-f23432a5 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 433 | - [ ] **[FLOWISE-3]** Tool-Adapter v1 (search, graph, rag) |
| T0074-ae6d7332 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 434 | - [ ] **[FLOWISE-4]** Agent-Registry (PG + YAML Sign + API) |
| T0075-97531667 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 435 | - [ ] **[FLOWISE-5]** Starter-Agents (Research, Graph, Dossier) |
| T0076-cc2eb02e | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 436 | - [ ] **[FLOWISE-6]** n8n Node `Run Flowise Agent` |
| T0077-db960318 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 437 | - [ ] **[FLOWISE-7]** NiFi Processor `InvokeFlowiseAgent` |
| T0078-37013536 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 438 | - [ ] **[FLOWISE-8]** Tool-Adapter v2 (verify, geo, forensics) |
| T0079-74001f34 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 439 | - [ ] **[FLOWISE-9]** Security Policies (OPA Rego + Sandbox Profiles) |
| T0080-fc5794eb | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 440 | - [ ] **[FLOWISE-10]** Preset Wiring (default_agents) |
| T0081-2789df69 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 441 | - [ ] **[FLOWISE-11]** Eval Suites + CI Scorer |
| T0082-1d7db07e | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 442 | - [ ] **[FLOWISE-12]** Meta-Planner Agent (v1.0) |
| T0083-266589e2 | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 443 | - [ ] **[FLOWISE-13]** Cost/Token Budgets + Alerts |
| T0084-c04b823b | docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md | 444 | - [ ] **[FLOWISE-14]** Canary & Rollback Mechanik |
| T0085-e8f46288 | docs/blueprints/SECURITY-BLUEPRINT.md | 120 | ## ✅ Tickets (Erweiterung zum TODO-Index) |
| T0086-d4ba2caa | docs/blueprints/VERIFICATION-BLUEPRINT.md | 171 | # 🧩 Tickets (zum Ergänzen deines TODO-Index) |
| T0087-a03b5205 | docs/blueprints/VERIFICATION-BLUEPRINT.md | 504 | ## ✅ Tickets (zum TODO-Index ergänzen) |
| T0088-9923a9b4 | docs/dev/Checkliste.md | 10 | Weitere Details siehe `TODO-Index.md`. |
| T0089-a178ef20 | docs/dev/README.md | 429 | # TODO: filter by OPA decision (resource tags vs user attributes) |
| T0090-9addc53a | docs/dev/SECURITY-BLUEPRINT.md | 120 | ## ✅ Tickets (Erweiterung zum TODO-Index) |
| T0091-a02a31b3 | docs/dev/VERIFICATION-BLUEPRINT.md | 360 | ## ✅ Tickets (zum TODO-Index ergänzen) |
| T0092-d8b0857d | docs/dev/frontend_modernization_guide.md | 204 | - [ ] Design System implementiert |
| T0093-bb21b40b | docs/dev/frontend_modernization_guide.md | 205 | - [ ] Layout System eingerichtet |
| T0094-08bb46e8 | docs/dev/frontend_modernization_guide.md | 206 | - [ ] Komponenten modernisiert |
| T0095-7444d943 | docs/dev/frontend_modernization_guide.md | 207 | - [ ] Responsive Design getestet |
| T0096-0ee98700 | docs/dev/frontend_modernization_guide.md | 208 | - [ ] Performance optimiert |
| T0097-7e920285 | docs/dev/frontend_modernization_guide.md | 209 | - [ ] Tests aktualisiert |
| T0098-cc265ba0 | docs/dev/frontend_modernization_guide.md | 210 | - [ ] Accessibility geprüft |
| T0099-77a60cdf | docs/dev/frontend_modernization_guide.md | 211 | - [ ] Cross-Browser Tests |
| T0100-34e07270 | docs/dev/frontend_modernization_guide.md | 212 | - [ ] Mobile Experience validiert |
| T0101-18ad350b | docs/dev/frontend_modernization_guide.md | 213 | - [ ] Documentation aktualisiert |
| T0102-f92eaf1d | docs/dev/superset-nifi-flowise.md | 184 | - [ ] **Superset-Composer**: JS/Python Helper eingebaut → Link öffnet Dashboard mit Filtern |
| T0103-bf72ef17 | docs/dev/superset-nifi-flowise.md | 185 | - [ ] **NiFi→Aleph**: InvokeHTTP Multipart konfiguriert, 200/202 Rückgabe sichtbar |
| T0104-0b791bfe | docs/dev/superset-nifi-flowise.md | 186 | - [ ] **Flowise Agent**: Tools/Schemas registriert, Guardrail-Prompt gesetzt, Tool-Limit aktiv |
| T0105-c01505d6 | docs/dev/superset-nifi-flowise.md | 187 | - [ ] **Smoke Tests**: |
| T0106-c900eac2 | docs/dev/roadmap/v0.2-overview.md | 103 | - [ ] T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T0107-993da743 | docs/dev/roadmap/v0.2-overview.md | 104 | - [ ] T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T0108-a50ea467 | docs/dev/roadmap/v0.2-overview.md | 105 | - [ ] T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T0109-aa9cfd4d | docs/dev/roadmap/v0.2-overview.md | 106 | - [ ] T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T0110-029ca9a1 | docs/dev/roadmap/v0.2-overview.md | 107 | - [ ] T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T0111-f95dac19 | docs/dev/roadmap/v0.2-overview.md | 108 | - [ ] T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T0112-9052f09c | docs/dev/roadmap/v0.2-overview.md | 109 | - [ ] T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T0113-73c9ef76 | docs/dev/roadmap/v0.2-overview.md | 110 | - [ ] T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T0114-4d3ff61b | docs/dev/roadmap/v0.2-overview.md | 111 | - [ ] T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T0115-07a61ab2 | docs/dev/roadmap/v0.2-overview.md | 112 | - [ ] T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T0116-4b6def4b | docs/dev/roadmap/v0.2-overview.md | 113 | - [ ] T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T0117-0eb73ecd | docs/dev/roadmap/v0.2-overview.md | 114 | - [ ] T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T0118-bf23f9b2 | docs/dev/roadmap/v0.2-overview.md | 115 | - [ ] T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T0119-e436924f | docs/dev/roadmap/v0.2-overview.md | 116 | - [ ] T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T0120-23d313ee | docs/dev/roadmap/v0.2-overview.md | 117 | - [ ] T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T0121-d79e1c21 | docs/dev/roadmap/v0.2-overview.md | 118 | - [ ] T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T0122-17bb03b2 | docs/dev/roadmap/v0.2-overview.md | 119 | - [ ] T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T0123-6fe08a25 | docs/dev/roadmap/v0.2-overview.md | 120 | - [ ] T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T0124-942240ee | docs/dev/roadmap/v0.2-overview.md | 121 | - [ ] T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T0125-16484ed3 | docs/dev/roadmap/v0.2-overview.md | 122 | - [ ] T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T0126-04d4a8b5 | docs/dev/roadmap/v0.2-overview.md | 123 | - [ ] T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T0127-504c080e | docs/dev/roadmap/v0.2-overview.md | 124 | - [ ] T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T0128-86426f67 | docs/dev/roadmap/v0.2-overview.md | 125 | - [ ] T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T0129-8ea18def | docs/dev/roadmap/v0.2-overview.md | 126 | - [ ] T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T0130-43963210 | docs/dev/roadmap/v0.2-overview.md | 127 | - [ ] T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T0131-f8e489cb | docs/dev/roadmap/v0.2-overview.md | 128 | - [ ] T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T0132-fa5e045b | docs/dev/roadmap/v0.2-overview.md | 129 | - [ ] T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T0133-2334e9c3 | docs/dev/roadmap/v0.2-overview.md | 130 | - [ ] T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T0134-dfe53d7e | docs/dev/roadmap/v0.2-overview.md | 131 | - [ ] T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T0135-b1a3241a | docs/dev/roadmap/v0.2-overview.md | 132 | - [ ] T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T0136-60adf0e5 | docs/dev/roadmap/v0.2-overview.md | 133 | - [ ] T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T0137-0b249178 | docs/dev/roadmap/v0.2-overview.md | 134 | - [ ] T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T0138-e4394bbb | docs/dev/roadmap/v0.2-overview.md | 135 | - [ ] T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T0139-bc806cf7 | docs/dev/roadmap/v0.2-overview.md | 136 | - [ ] T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T0140-46b04ac3 | docs/dev/roadmap/v0.2-overview.md | 137 | - [ ] T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T0141-21f0aea0 | docs/dev/roadmap/v0.2-overview.md | 138 | - [ ] T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T0142-66376184 | docs/dev/roadmap/v0.2-overview.md | 139 | - [ ] T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T0143-203c693f | docs/dev/roadmap/v0.2-overview.md | 140 | - [ ] T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T0144-5dc5f454 | docs/dev/roadmap/v0.2-overview.md | 141 | - [ ] T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T0145-10b0c8af | docs/dev/roadmap/v0.2-overview.md | 142 | - [ ] T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T0146-90e5827c | docs/dev/roadmap/v0.2-overview.md | 143 | - [ ] T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T0147-346508fd | docs/dev/roadmap/v0.2-overview.md | 144 | - [ ] T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T0148-ea227f45 | docs/dev/roadmap/v0.2-overview.md | 145 | - [ ] T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T0149-4c659e3f | docs/dev/roadmap/v0.2-overview.md | 146 | - [ ] T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T0150-2fd63aa9 | docs/dev/roadmap/v0.2-overview.md | 147 | - [ ] T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T0151-3de74d7a | docs/dev/roadmap/v0.2-overview.md | 148 | - [ ] T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T0152-11410bc5 | docs/dev/roadmap/v0.2-overview.md | 149 | - [ ] T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T0153-e25b9dde | docs/dev/roadmap/v0.2-overview.md | 150 | - [ ] T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T0154-52ee1185 | docs/dev/roadmap/v0.2-overview.md | 151 | - [ ] T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T0155-a970df97 | docs/dev/roadmap/v0.2-overview.md | 152 | - [ ] T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T0156-eb70a60b | docs/dev/roadmap/v0.2-overview.md | 153 | - [ ] T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T0157-c59fccc1 | docs/dev/roadmap/v0.2-overview.md | 154 | - [ ] T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T0158-e81effed | docs/dev/roadmap/v0.2-overview.md | 155 | - [ ] T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T0159-f48b50e2 | docs/dev/roadmap/v0.2-overview.md | 156 | - [ ] T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T0160-4486510d | docs/dev/roadmap/v0.2-overview.md | 157 | - [ ] T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T0161-2a689dfd | docs/dev/roadmap/v0.2-overview.md | 158 | - [ ] T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T0162-3932b30f | docs/dev/roadmap/v0.2-overview.md | 159 | - [ ] T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T0163-a424d84a | docs/dev/roadmap/v0.2-overview.md | 160 | - [ ] T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T0164-02673b7b | docs/dev/roadmap/v0.2-overview.md | 161 | - [ ] T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T0165-de784fa3 | docs/dev/roadmap/v0.2-overview.md | 162 | - [ ] T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T0166-3d4f77b3 | docs/dev/roadmap/v0.2-overview.md | 163 | - [ ] T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T0167-3c902a8e | docs/dev/roadmap/v0.2-overview.md | 164 | - [ ] T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T0168-661b9b61 | docs/dev/roadmap/v0.2-overview.md | 165 | - [ ] T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T0169-ebcaff40 | docs/dev/roadmap/v0.2-overview.md | 166 | - [ ] T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T0170-ce423dfe | docs/dev/roadmap/v0.2-overview.md | 167 | - [ ] T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T0171-13c7b3e4 | docs/dev/roadmap/v0.2-overview.md | 168 | - [ ] T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T0172-d1148c8e | docs/dev/roadmap/v0.2-overview.md | 169 | - [ ] T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T0173-b7c8eb89 | docs/dev/roadmap/v0.2-overview.md | 170 | - [ ] T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T0174-5b1ea5e6 | docs/dev/roadmap/v0.2-overview.md | 171 | - [ ] T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T0175-e2a0d6f7 | docs/dev/roadmap/v0.2-overview.md | 172 | - [ ] T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T0176-b6410e4f | docs/dev/roadmap/v0.2-overview.md | 173 | - [ ] T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T0177-644e10e6 | docs/dev/roadmap/v0.2-overview.md | 174 | - [ ] T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T0178-60b4ec5a | docs/dev/roadmap/v0.2-overview.md | 175 | - [ ] T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T0179-817f1819 | docs/dev/roadmap/v0.2-overview.md | 176 | - [ ] T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T0180-f016b354 | docs/dev/roadmap/v0.2-overview.md | 177 | - [ ] T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T0181-462fb556 | docs/dev/roadmap/v0.2-overview.md | 178 | - [ ] T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T0182-b7c40b38 | docs/dev/roadmap/v0.2-overview.md | 179 | - [ ] T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T0183-e9314fc7 | docs/dev/roadmap/v0.2-overview.md | 180 | - [ ] T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T0184-9d656a38 | docs/dev/roadmap/v0.2-overview.md | 181 | - [ ] T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T0185-d08d5223 | docs/dev/roadmap/v0.2-overview.md | 182 | - [ ] T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T0186-1ae5ad6f | docs/dev/roadmap/v0.2-overview.md | 183 | - [ ] T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T0187-2593d46e | docs/dev/roadmap/v0.2-overview.md | 184 | - [ ] T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T0188-0db8c8ae | docs/dev/roadmap/v0.2-overview.md | 185 | - [ ] T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T0189-21b4bd6c | docs/dev/roadmap/v0.2-overview.md | 186 | - [ ] T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T0190-6abe0f15 | docs/dev/roadmap/v0.2-overview.md | 187 | - [ ] T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T0191-6cf639e1 | docs/dev/roadmap/v0.2-overview.md | 188 | - [ ] T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T0192-402b9045 | docs/dev/roadmap/v0.2-overview.md | 189 | - [ ] T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T0193-9595ae47 | docs/dev/roadmap/v0.2-overview.md | 190 | - [ ] T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T0194-dae5542d | docs/dev/roadmap/v0.2-overview.md | 191 | - [ ] T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T0195-e896224b | docs/dev/roadmap/v0.2-overview.md | 192 | - [ ] T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T0196-1ee30000 | docs/dev/roadmap/v0.2-overview.md | 193 | - [ ] T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T0197-06e78fcc | docs/dev/roadmap/v0.2-overview.md | 194 | - [ ] T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T0198-513a0fca | docs/dev/roadmap/v0.2-overview.md | 195 | - [ ] T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T0199-28c49b10 | docs/dev/roadmap/v0.2-overview.md | 196 | - [ ] T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T0200-42c388e1 | docs/dev/roadmap/v0.2-overview.md | 197 | - [ ] T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T0201-bd4e4ccf | docs/dev/roadmap/v0.2-overview.md | 198 | - [ ] T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T0202-495feca8 | docs/dev/roadmap/v0.2-overview.md | 199 | - [ ] T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T0203-be79824c | docs/dev/roadmap/v0.2-overview.md | 200 | - [ ] T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T0204-75ce9b49 | docs/dev/roadmap/v0.2-overview.md | 201 | - [ ] T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T0205-0fa4f434 | docs/dev/roadmap/v0.2-overview.md | 202 | - [ ] T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T0206-45f95f34 | docs/dev/roadmap/v0.2-overview.md | 203 | - [ ] T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T0207-604a10fb | docs/dev/roadmap/v0.2-overview.md | 204 | - [ ] T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T0208-8385c00c | docs/dev/roadmap/v0.2-overview.md | 205 | - [ ] T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T0209-83e91e14 | docs/dev/roadmap/v0.2-overview.md | 206 | - [ ] T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T0210-c2dac8da | docs/dev/roadmap/v0.2-overview.md | 207 | - [ ] T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T0211-e321f927 | docs/dev/roadmap/v0.2-overview.md | 208 | - [ ] T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T0212-90c202cd | docs/dev/roadmap/v0.2-overview.md | 209 | - [ ] T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T0213-dbb77892 | docs/dev/roadmap/v0.2-overview.md | 210 | - [ ] T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T0214-45f9d266 | docs/dev/roadmap/v0.2-overview.md | 211 | - [ ] T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T0215-c57b91bf | docs/dev/roadmap/v0.2-overview.md | 212 | - [ ] T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T0216-24e1408a | docs/dev/roadmap/v0.2-overview.md | 213 | - [ ] T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T0217-68cfef58 | docs/dev/roadmap/v0.2-overview.md | 214 | - [ ] T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T0218-45edf2f8 | docs/dev/roadmap/v0.2-overview.md | 215 | - [ ] T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T0219-6c4dfa5f | docs/dev/roadmap/v0.2-overview.md | 216 | - [ ] T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T0220-d81bd293 | docs/dev/roadmap/v0.2-overview.md | 217 | - [ ] T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T0221-1afc65db | docs/dev/roadmap/v0.2-overview.md | 218 | - [ ] T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T0222-cc17bc49 | docs/dev/roadmap/v0.2-overview.md | 219 | - [ ] T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T0223-ffd8b81d | docs/dev/roadmap/v0.2-overview.md | 220 | - [ ] T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T0224-19776de8 | docs/dev/roadmap/v0.2-overview.md | 221 | - [ ] T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T0225-8f556173 | docs/dev/roadmap/v0.2-overview.md | 222 | - [ ] T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T0226-1fb46b8b | docs/dev/roadmap/v0.2-overview.md | 223 | - [ ] T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T0227-f6311825 | docs/dev/roadmap/v0.2-overview.md | 224 | - [ ] T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T0228-5b095bc6 | docs/dev/roadmap/v0.2-overview.md | 225 | - [ ] T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T0229-09922ee6 | docs/dev/roadmap/v0.2-overview.md | 226 | - [ ] T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T0230-2147463e | docs/dev/roadmap/v0.2-overview.md | 227 | - [ ] T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T0231-2c6954a9 | docs/dev/roadmap/v0.2-overview.md | 228 | - [ ] T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T0232-f8fe6b6f | docs/dev/roadmap/v0.2-overview.md | 229 | - [ ] T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T0233-c9387dec | docs/dev/roadmap/v0.2-overview.md | 230 | - [ ] T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T0234-6a5648e3 | docs/dev/roadmap/v0.2-overview.md | 231 | - [ ] T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T0235-b0d4de97 | docs/dev/roadmap/v0.2-overview.md | 232 | - [ ] T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T0236-7052e7d7 | docs/dev/roadmap/v0.2-overview.md | 233 | - [ ] T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T0237-fa2f6e72 | docs/dev/roadmap/v0.2-overview.md | 234 | - [ ] T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T0238-3b7dafef | docs/dev/roadmap/v0.2-overview.md | 235 | - [ ] T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T0239-d830fbf6 | docs/dev/roadmap/v0.2-overview.md | 236 | - [ ] T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T0240-c27f9ac3 | docs/dev/roadmap/v0.2-overview.md | 237 | - [ ] T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T0241-9665763c | docs/dev/roadmap/v0.2-overview.md | 238 | - [ ] T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T0242-9fbd9171 | docs/dev/roadmap/v0.2-overview.md | 239 | - [ ] T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T0243-40aa1d1c | docs/dev/roadmap/v0.2-overview.md | 240 | - [ ] T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T0244-6f20648f | docs/dev/roadmap/v0.2-overview.md | 241 | - [ ] T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T0245-a19796c3 | docs/dev/roadmap/v0.2-overview.md | 242 | - [ ] T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T0246-096cf8f0 | docs/dev/roadmap/v0.2-overview.md | 243 | - [ ] T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T0247-fd6c9c57 | docs/dev/roadmap/v0.2-overview.md | 244 | - [ ] T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T0248-6364c6e5 | docs/dev/roadmap/v0.2-overview.md | 245 | - [ ] T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T0249-07e7d355 | docs/dev/roadmap/v0.2-overview.md | 246 | - [ ] T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T0250-6d34f40b | docs/dev/roadmap/v0.2-overview.md | 247 | - [ ] T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T0251-df35711b | docs/dev/roadmap/v0.2-overview.md | 248 | - [ ] T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T0252-d8120cff | docs/dev/roadmap/v0.2-overview.md | 249 | - [ ] T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T0253-62154bb6 | docs/dev/roadmap/v0.2-overview.md | 250 | - [ ] T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T0254-38eb5b65 | docs/dev/roadmap/v0.2-overview.md | 251 | - [ ] T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T0255-7713be21 | docs/dev/roadmap/v0.2-overview.md | 252 | - [ ] T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T0256-698e70bb | docs/dev/roadmap/v0.2-overview.md | 253 | - [ ] T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T0257-6de54a00 | docs/dev/roadmap/v0.2-overview.md | 254 | - [ ] T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T0258-8bd2c8c0 | docs/dev/roadmap/v0.2-overview.md | 255 | - [ ] T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T0259-111d197c | docs/dev/roadmap/v0.2-overview.md | 256 | - [ ] T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T0260-bb0f243b | docs/dev/roadmap/v0.2-overview.md | 257 | - [ ] T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T0261-a94dc41b | docs/dev/roadmap/v0.2-overview.md | 258 | - [ ] T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T0262-2edebae5 | docs/dev/roadmap/v0.2-overview.md | 259 | - [ ] T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T0263-d22a7364 | docs/dev/roadmap/v0.2-overview.md | 260 | - [ ] T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T0264-7d1a6d31 | docs/dev/roadmap/v0.2-overview.md | 261 | - [ ] T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T0265-c7ab472f | docs/dev/roadmap/v0.2-overview.md | 262 | - [ ] T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T0266-0cf5cbf4 | docs/dev/roadmap/v0.2-overview.md | 263 | - [ ] T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T0267-8bdddd87 | docs/dev/roadmap/v0.2-overview.md | 264 | - [ ] T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T0268-09d0380e | docs/dev/roadmap/v0.2-overview.md | 265 | - [ ] T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T0269-0a323272 | docs/dev/roadmap/v0.2-overview.md | 266 | - [ ] T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T0270-46015712 | docs/dev/roadmap/v0.2-overview.md | 267 | - [ ] T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T0271-547e5853 | docs/dev/roadmap/v0.2-overview.md | 268 | - [ ] T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T0272-4c9f3da7 | docs/dev/roadmap/v0.2-overview.md | 269 | - [ ] T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T0273-21858d45 | docs/dev/roadmap/v0.2-overview.md | 270 | - [ ] T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T0274-8ba6b53b | docs/dev/roadmap/v0.2-overview.md | 271 | - [ ] T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T0275-08869d74 | docs/dev/roadmap/v0.2-overview.md | 272 | - [ ] T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T0276-9b3ceb33 | docs/dev/roadmap/v0.2-overview.md | 273 | - [ ] T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T0277-8770fd12 | docs/dev/roadmap/v0.2-overview.md | 274 | - [ ] T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T0278-65a32531 | docs/dev/roadmap/v0.2-overview.md | 275 | - [ ] T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T0279-59b17e88 | docs/dev/roadmap/v0.2-overview.md | 276 | - [ ] T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T0280-404ef755 | docs/dev/roadmap/v0.2-overview.md | 277 | - [ ] T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T0281-faf09aef | docs/dev/roadmap/v0.2-overview.md | 278 | - [ ] T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T0282-87f99862 | docs/dev/roadmap/v0.2-overview.md | 279 | - [ ] T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T0283-1140cee0 | docs/dev/roadmap/v0.2-overview.md | 280 | - [ ] T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T0284-d98b84f3 | docs/dev/roadmap/v0.2-overview.md | 281 | - [ ] T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T0285-016a7ade | docs/dev/roadmap/v0.2-overview.md | 282 | - [ ] T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T0286-db818c2a | docs/dev/roadmap/v0.2-overview.md | 283 | - [ ] T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T0287-2f0638ae | docs/dev/roadmap/v0.2-overview.md | 284 | - [ ] T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T0288-665f39fe | docs/dev/roadmap/v0.2-overview.md | 285 | - [ ] T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T0289-cae7474b | docs/dev/roadmap/v0.2-overview.md | 286 | - [ ] T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T0290-77df06c4 | docs/dev/roadmap/v0.2-overview.md | 287 | - [ ] T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T0291-effb90f1 | docs/dev/roadmap/v0.2-overview.md | 288 | - [ ] T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T0292-518572a2 | docs/dev/roadmap/v0.2-overview.md | 289 | - [ ] T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T0293-db1c9800 | docs/dev/roadmap/v0.2-overview.md | 290 | - [ ] T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T0294-a73a2b5c | docs/dev/roadmap/v0.2-overview.md | 291 | - [ ] T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T0295-6ded6ccf | docs/dev/roadmap/v0.2-overview.md | 292 | - [ ] T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T0296-c86bece1 | docs/dev/roadmap/v0.2-overview.md | 293 | - [ ] T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T0297-5be90ac6 | docs/dev/roadmap/v0.2-overview.md | 294 | - [ ] T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T0298-5adcdb50 | docs/dev/roadmap/v0.2-overview.md | 295 | - [ ] T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T0299-ceff2e55 | docs/dev/roadmap/v0.2-overview.md | 296 | - [ ] T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T0300-0486f8e9 | docs/dev/roadmap/v0.2-overview.md | 297 | - [ ] T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T0301-ea26ba06 | docs/dev/roadmap/v0.2-overview.md | 298 | - [ ] T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T0302-004d00f8 | docs/dev/roadmap/v0.2-overview.md | 299 | - [ ] T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T0303-0dc17eda | docs/dev/roadmap/v0.2-overview.md | 300 | - [ ] T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T0304-adc855cd | docs/dev/roadmap/v0.2-overview.md | 301 | - [ ] T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T0305-48eb1408 | docs/dev/roadmap/v0.2-overview.md | 302 | - [ ] T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T0306-5ed63b8f | docs/dev/roadmap/v0.2-overview.md | 303 | - [ ] T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T0307-d86fa5b3 | docs/dev/roadmap/v0.2-overview.md | 304 | - [ ] T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T0308-83938a43 | docs/dev/roadmap/v0.2-overview.md | 305 | - [ ] T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T0309-8d04cf51 | docs/dev/roadmap/v0.2-overview.md | 306 | - [ ] T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T0310-a4248164 | docs/dev/roadmap/v0.2-overview.md | 307 | - [ ] T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T0311-9cfda7ef | docs/dev/roadmap/v0.2-overview.md | 308 | - [ ] T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T0312-41b083ef | docs/dev/roadmap/v0.2-overview.md | 309 | - [ ] T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T0313-0b1227d7 | docs/dev/roadmap/v0.2-overview.md | 310 | - [ ] T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T0314-640ae038 | docs/dev/roadmap/v0.2-overview.md | 311 | - [ ] T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T0315-1516db90 | docs/dev/roadmap/v0.2-overview.md | 312 | - [ ] T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T0316-9ec6cee2 | docs/dev/roadmap/v0.2-overview.md | 313 | - [ ] T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T0317-a391f335 | docs/dev/roadmap/v0.2-overview.md | 314 | - [ ] T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T0318-991cf0cd | docs/dev/roadmap/v0.2-overview.md | 315 | - [ ] T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T0319-5b395238 | docs/dev/roadmap/v0.2-overview.md | 316 | - [ ] T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T0320-4526634f | docs/dev/roadmap/v0.2-overview.md | 317 | - [ ] T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T0321-39abc22f | docs/dev/roadmap/v0.2-overview.md | 318 | - [ ] T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T0322-0b47a34e | docs/dev/roadmap/v0.2-overview.md | 319 | - [ ] T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T0323-4cb0e5e5 | docs/dev/roadmap/v0.2-overview.md | 320 | - [ ] T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T0324-9818f245 | docs/dev/roadmap/v0.2-overview.md | 321 | - [ ] T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T0325-e1adf3d6 | docs/dev/roadmap/v0.2-overview.md | 322 | - [ ] T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T0326-9936cf25 | docs/dev/roadmap/v0.2-overview.md | 323 | - [ ] T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T0327-e5694f4b | docs/dev/roadmap/v0.2-overview.md | 324 | - [ ] T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T0328-58a8b95a | docs/dev/roadmap/v0.2-overview.md | 325 | - [ ] T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T0329-dfa056a3 | docs/dev/roadmap/v0.2-overview.md | 326 | - [ ] T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T0330-57992821 | docs/dev/roadmap/v0.2-overview.md | 327 | - [ ] T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T0331-4485bd3f | docs/dev/roadmap/v0.2-overview.md | 328 | - [ ] T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T0332-d0f6f6b5 | docs/dev/roadmap/v0.2-overview.md | 329 | - [ ] T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T0333-ff960c0f | docs/dev/roadmap/v0.2-overview.md | 330 | - [ ] T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T0334-97030547 | docs/dev/roadmap/v0.2-overview.md | 331 | - [ ] T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T0335-209c3155 | docs/dev/roadmap/v0.2-overview.md | 332 | - [ ] T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T0336-31cab99f | docs/dev/roadmap/v0.2-overview.md | 333 | - [ ] T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T0337-abf17bb2 | docs/dev/roadmap/v0.2-overview.md | 334 | - [ ] T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T0338-a36a47a3 | docs/dev/roadmap/v0.2-overview.md | 335 | - [ ] T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T0339-bb3f83d9 | docs/dev/roadmap/v0.2-overview.md | 336 | - [ ] T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T0340-708f6539 | docs/dev/roadmap/v0.2-overview.md | 337 | - [ ] T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T0341-2e9004e6 | docs/dev/roadmap/v0.2-overview.md | 338 | - [ ] T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T0342-83f7efbf | docs/dev/roadmap/v0.2-overview.md | 339 | - [ ] T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T0343-079314a0 | docs/dev/roadmap/v0.2-overview.md | 340 | - [ ] T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T0344-5dd21a3f | docs/dev/roadmap/v0.2-overview.md | 341 | - [ ] T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T0345-9ce8d5e5 | docs/dev/roadmap/v0.2-overview.md | 342 | - [ ] T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T0346-957cb56a | docs/dev/roadmap/v0.2-overview.md | 343 | - [ ] T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T0347-d289680e | docs/dev/roadmap/v0.2-overview.md | 344 | - [ ] T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T0348-36b6dc1f | docs/dev/roadmap/v0.2-overview.md | 345 | - [ ] T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T0349-2797769d | docs/dev/roadmap/v0.2-overview.md | 346 | - [ ] T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T0350-00bb222d | docs/dev/roadmap/v0.2-overview.md | 347 | - [ ] T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T0351-f33d3105 | docs/dev/roadmap/v0.2-overview.md | 348 | - [ ] T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T0352-fa4f82d0 | docs/dev/roadmap/v0.2-overview.md | 349 | - [ ] T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T0353-eb327034 | docs/dev/roadmap/v0.2-overview.md | 350 | - [ ] T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T0354-df068f5e | docs/dev/roadmap/v0.2-overview.md | 351 | - [ ] T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T0355-e3643977 | docs/dev/roadmap/v0.2-overview.md | 352 | - [ ] T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T0356-d372a12b | docs/dev/roadmap/v0.2-overview.md | 353 | - [ ] T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T0357-411f766a | docs/dev/roadmap/v0.2-overview.md | 354 | - [ ] T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T0358-609de980 | docs/dev/roadmap/v0.2-overview.md | 355 | - [ ] T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T0359-a163b15b | docs/dev/roadmap/v0.2-overview.md | 356 | - [ ] T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T0360-e3f7844b | docs/dev/roadmap/v0.2-overview.md | 357 | - [ ] T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T0361-0fc93024 | docs/dev/roadmap/v0.2-overview.md | 358 | - [ ] T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T0362-7e62811f | docs/dev/roadmap/v0.2-overview.md | 359 | - [ ] T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T0363-c662ac02 | docs/dev/roadmap/v0.2-overview.md | 360 | - [ ] T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T0364-c8a14c6d | docs/dev/roadmap/v0.2-overview.md | 361 | - [ ] T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T0365-fb89d845 | docs/dev/roadmap/v0.2-overview.md | 362 | - [ ] T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T0366-f414378e | docs/dev/roadmap/v0.2-overview.md | 363 | - [ ] T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T0367-c9f9aa03 | docs/dev/roadmap/v0.2-overview.md | 364 | - [ ] T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T0368-b47d2ef3 | docs/dev/roadmap/v0.2-overview.md | 365 | - [ ] T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T0369-8b598b74 | docs/dev/roadmap/v0.2-overview.md | 366 | - [ ] T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T0370-c576ee36 | docs/dev/roadmap/v0.2-overview.md | 367 | - [ ] T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T0371-25d034d2 | docs/dev/roadmap/v0.2-overview.md | 368 | - [ ] T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T0372-ee91211d | docs/dev/roadmap/v0.2-overview.md | 369 | - [ ] T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T0373-48e95ee3 | docs/dev/roadmap/v0.2-overview.md | 370 | - [ ] T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T0374-bc2b145c | docs/dev/roadmap/v0.2-overview.md | 371 | - [ ] T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T0375-1026066c | docs/dev/roadmap/v0.2-overview.md | 372 | - [ ] T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T0376-64451e12 | docs/dev/roadmap/v0.2-overview.md | 373 | - [ ] T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T0377-9d1f31b3 | docs/dev/roadmap/v0.2-overview.md | 374 | - [ ] T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T0378-84883db8 | docs/dev/roadmap/v0.2-overview.md | 375 | - [ ] T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T0379-bb04e154 | docs/dev/roadmap/v0.2-overview.md | 376 | - [ ] T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T0380-9815628e | docs/dev/roadmap/v0.2-overview.md | 377 | - [ ] T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T0381-36f34718 | docs/dev/roadmap/v0.2-overview.md | 378 | - [ ] T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T0382-dbc9b7f6 | docs/dev/roadmap/v0.2-overview.md | 379 | - [ ] T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T0383-eb3ff636 | docs/dev/roadmap/v0.2-overview.md | 380 | - [ ] T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T0384-ec08e60a | docs/dev/roadmap/v0.2-overview.md | 381 | - [ ] T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T0385-5337c834 | docs/dev/roadmap/v0.2-overview.md | 382 | - [ ] T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T0386-294c59f3 | docs/dev/roadmap/v0.2-overview.md | 383 | - [ ] T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T0387-ac9f0519 | docs/dev/roadmap/v0.2-overview.md | 384 | - [ ] T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T0388-87f9d545 | docs/dev/roadmap/v0.2-overview.md | 385 | - [ ] T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T0389-b2f62d31 | docs/dev/roadmap/v0.2-overview.md | 386 | - [ ] T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T0390-5af2f5e0 | docs/dev/roadmap/v0.2-overview.md | 387 | - [ ] T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T0391-b5f9cb53 | docs/dev/roadmap/v0.2-overview.md | 388 | - [ ] T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T0392-f9f94016 | docs/dev/roadmap/v0.2-overview.md | 389 | - [ ] T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T0393-5750fe6f | docs/dev/roadmap/v0.2-overview.md | 390 | - [ ] T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T0394-617a8369 | docs/dev/roadmap/v0.2-overview.md | 391 | - [ ] T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T0395-1b6b3639 | docs/dev/roadmap/v0.2-overview.md | 392 | - [ ] T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T0396-42f69730 | docs/dev/roadmap/v0.2-overview.md | 393 | - [ ] T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T0397-c5e57168 | docs/dev/roadmap/v0.2-overview.md | 394 | - [ ] T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T0398-8f5a0a33 | docs/dev/roadmap/v0.2-overview.md | 395 | - [ ] T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T0399-9dd28f7b | docs/dev/roadmap/v0.2-overview.md | 396 | - [ ] T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T0400-3c463318 | docs/dev/roadmap/v0.2-overview.md | 397 | - [ ] T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T0401-4454f350 | docs/dev/roadmap/v0.2-overview.md | 398 | - [ ] T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T0402-147af567 | docs/dev/roadmap/v0.2-overview.md | 399 | - [ ] T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T0403-9c108e95 | docs/dev/roadmap/v0.2-overview.md | 400 | - [ ] T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T0404-2e1878d9 | docs/dev/roadmap/v0.2-overview.md | 401 | - [ ] T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T0405-3617b061 | docs/dev/roadmap/v0.2-overview.md | 402 | - [ ] T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T0406-10b93529 | docs/dev/roadmap/v0.2-overview.md | 403 | - [ ] T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T0407-00c03a09 | docs/dev/roadmap/v0.2-overview.md | 404 | - [ ] T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T0408-13feba2d | docs/dev/roadmap/v0.2-overview.md | 405 | - [ ] T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T0409-8137de0e | docs/dev/roadmap/v0.2-overview.md | 406 | - [ ] T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T0410-9f655354 | docs/dev/roadmap/v0.2-overview.md | 407 | - [ ] T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T0411-285e45b4 | docs/dev/roadmap/v0.2-overview.md | 408 | - [ ] T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T0412-50d0322a | docs/dev/roadmap/v0.2-overview.md | 409 | - [ ] T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T0413-a18e97a0 | docs/dev/roadmap/v0.2-overview.md | 410 | - [ ] T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T0414-8a8a4fc1 | docs/dev/roadmap/v0.2-overview.md | 411 | - [ ] T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T0415-45d6cec2 | docs/dev/roadmap/v0.2-overview.md | 412 | - [ ] T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T0416-2e675912 | docs/dev/roadmap/v0.2-overview.md | 413 | - [ ] T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T0417-7a82087b | docs/dev/roadmap/v0.2-overview.md | 414 | - [ ] T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T0418-8a3adac3 | docs/dev/roadmap/v0.2-overview.md | 415 | - [ ] T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T0419-9453c4a0 | docs/dev/roadmap/v0.2-overview.md | 416 | - [ ] T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T0420-32d2ddb9 | docs/dev/roadmap/v0.2-overview.md | 417 | - [ ] T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T0421-fd2ccf85 | docs/dev/roadmap/v0.2-overview.md | 418 | - [ ] T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T0422-6119855d | docs/dev/roadmap/v0.2-overview.md | 419 | - [ ] T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T0423-851a597f | docs/dev/roadmap/v0.2-overview.md | 420 | - [ ] T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T0424-b2e3f07a | docs/dev/roadmap/v0.2-overview.md | 421 | - [ ] T0107-c900 T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.2-overview.md:103) |
| T0425-c2ec37fb | docs/dev/roadmap/v0.2-overview.md | 422 | - [ ] T0108-993d T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.2-overview.md:104) |
| T0426-aabd64bf | docs/dev/roadmap/v0.2-overview.md | 423 | - [ ] T0109-a50e T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.2-overview.md:105) |
| T0427-ad507e6b | docs/dev/roadmap/v0.2-overview.md | 424 | - [ ] T0110-aa9c T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.2-overview.md:106) |
| T0428-44d82c40 | docs/dev/roadmap/v0.2-overview.md | 425 | - [ ] T0111-029c T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.2-overview.md:107) |
| T0429-07713b04 | docs/dev/roadmap/v0.2-overview.md | 426 | - [ ] T0112-f95d T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.2-overview.md:108) |
| T0430-283b248f | docs/dev/roadmap/v0.2-overview.md | 427 | - [ ] T0113-9052 T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:109) |
| T0431-9acdac25 | docs/dev/roadmap/v0.2-overview.md | 428 | - [ ] T0114-73c9 T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:110) |
| T0432-3ab9dc03 | docs/dev/roadmap/v0.2-overview.md | 429 | - [ ] T0115-4d3f T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:111) |
| T0433-52a058fd | docs/dev/roadmap/v0.2-overview.md | 430 | - [ ] T0116-07a6 T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:112) |
| T0434-b3175bb7 | docs/dev/roadmap/v0.2-overview.md | 431 | - [ ] T0117-4b6d T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:113) |
| T0435-b86083af | docs/dev/roadmap/v0.2-overview.md | 432 | - [ ] T0118-0eb7 T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:114) |
| T0436-da11ecec | docs/dev/roadmap/v0.2-overview.md | 433 | - [ ] T0119-bf23 T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:115) |
| T0437-60c8604e | docs/dev/roadmap/v0.2-overview.md | 434 | - [ ] T0120-e436 T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:116) |
| T0438-d5c52248 | docs/dev/roadmap/v0.2-overview.md | 435 | - [ ] T0121-23d3 T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:117) |
| T0439-3e89fdbb | docs/dev/roadmap/v0.2-overview.md | 436 | - [ ] T0122-d79e T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:118) |
| T0440-dd87fbf0 | docs/dev/roadmap/v0.2-overview.md | 437 | - [ ] T0123-17bb T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:119) |
| T0441-d13fc1e4 | docs/dev/roadmap/v0.2-overview.md | 438 | - [ ] T0124-6fe0 T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:120) |
| T0442-c2b1beaa | docs/dev/roadmap/v0.2-overview.md | 439 | - [ ] T0125-9422 T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:121) |
| T0443-1eda0a7e | docs/dev/roadmap/v0.2-overview.md | 440 | - [ ] T0126-1648 T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:122) |
| T0444-56c07534 | docs/dev/roadmap/v0.2-overview.md | 441 | - [ ] T0127-04d4 T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:123) |
| T0445-77a4bd3d | docs/dev/roadmap/v0.2-overview.md | 442 | - [ ] T0128-504c T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:124) |
| T0446-7c018454 | docs/dev/roadmap/v0.2-overview.md | 443 | - [ ] T0129-8642 T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:125) |
| T0447-827d98a5 | docs/dev/roadmap/v0.2-overview.md | 444 | - [ ] T0130-8ea1 T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:126) |
| T0448-030bf58d | docs/dev/roadmap/v0.2-overview.md | 445 | - [ ] T0131-4396 T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:127) |
| T0449-25a23884 | docs/dev/roadmap/v0.2-overview.md | 446 | - [ ] T0132-f8e4 T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:128) |
| T0450-641a0ccf | docs/dev/roadmap/v0.2-overview.md | 447 | - [ ] T0133-fa5e T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:129) |
| T0451-e68a07d3 | docs/dev/roadmap/v0.2-overview.md | 448 | - [ ] T0134-2334 T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:130) |
| T0452-ea33b17a | docs/dev/roadmap/v0.2-overview.md | 449 | - [ ] T0135-dfe5 T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:131) |
| T0453-951bcffc | docs/dev/roadmap/v0.2-overview.md | 450 | - [ ] T0136-b1a3 T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:132) |
| T0454-7ccf0905 | docs/dev/roadmap/v0.2-overview.md | 451 | - [ ] T0137-60ad T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:133) |
| T0455-956ae6cc | docs/dev/roadmap/v0.2-overview.md | 452 | - [ ] T0138-0b24 T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:134) |
| T0456-36098aa3 | docs/dev/roadmap/v0.2-overview.md | 453 | - [ ] T0139-e439 T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:135) |
| T0457-9e54be78 | docs/dev/roadmap/v0.2-overview.md | 454 | - [ ] T0140-bc80 T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:136) |
| T0458-2933f7bc | docs/dev/roadmap/v0.2-overview.md | 455 | - [ ] T0141-46b0 T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:137) |
| T0459-fffe5e7f | docs/dev/roadmap/v0.2-overview.md | 456 | - [ ] T0142-21f0 T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:138) |
| T0460-31f819b2 | docs/dev/roadmap/v0.2-overview.md | 457 | - [ ] T0143-6637 T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:139) |
| T0461-176d545e | docs/dev/roadmap/v0.2-overview.md | 458 | - [ ] T0144-203c T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:140) |
| T0462-ece0b0ae | docs/dev/roadmap/v0.2-overview.md | 459 | - [ ] T0145-5dc5 T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:141) |
| T0463-f216dc66 | docs/dev/roadmap/v0.2-overview.md | 460 | - [ ] T0146-10b0 T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:142) |
| T0464-12b6d9de | docs/dev/roadmap/v0.2-overview.md | 461 | - [ ] T0147-90e5 T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:143) |
| T0465-0530ebad | docs/dev/roadmap/v0.2-overview.md | 462 | - [ ] T0148-3465 T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:144) |
| T0466-89baed1b | docs/dev/roadmap/v0.2-overview.md | 463 | - [ ] T0149-ea22 T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:145) |
| T0467-9df91670 | docs/dev/roadmap/v0.2-overview.md | 464 | - [ ] T0150-4c65 T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:146) |
| T0468-9399f8dc | docs/dev/roadmap/v0.2-overview.md | 465 | - [ ] T0151-2fd6 T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:147) |
| T0469-8d047b06 | docs/dev/roadmap/v0.2-overview.md | 466 | - [ ] T0152-3de7 T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:148) |
| T0470-647fb771 | docs/dev/roadmap/v0.2-overview.md | 467 | - [ ] T0153-1141 T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:149) |
| T0471-2f7b97f5 | docs/dev/roadmap/v0.2-overview.md | 468 | - [ ] T0154-e25b T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:150) |
| T0472-8ff97c54 | docs/dev/roadmap/v0.2-overview.md | 469 | - [ ] T0155-52ee T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:151) |
| T0473-38d36bf6 | docs/dev/roadmap/v0.2-overview.md | 470 | - [ ] T0156-a970 T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:152) |
| T0474-b5453642 | docs/dev/roadmap/v0.2-overview.md | 471 | - [ ] T0157-eb70 T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:153) |
| T0475-f78f0fed | docs/dev/roadmap/v0.2-overview.md | 472 | - [ ] T0158-c59f T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:154) |
| T0476-d8e16dd5 | docs/dev/roadmap/v0.2-overview.md | 473 | - [ ] T0159-e81e T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:155) |
| T0477-9cfd00c4 | docs/dev/roadmap/v0.2-overview.md | 474 | - [ ] T0160-f48b T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:156) |
| T0478-fc688b48 | docs/dev/roadmap/v0.2-overview.md | 475 | - [ ] T0161-4486 T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:157) |
| T0479-6790cbab | docs/dev/roadmap/v0.2-overview.md | 476 | - [ ] T0162-2a68 T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:158) |
| T0480-4d10dc4c | docs/dev/roadmap/v0.2-overview.md | 477 | - [ ] T0163-3932 T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:159) |
| T0481-c2a08fe1 | docs/dev/roadmap/v0.2-overview.md | 478 | - [ ] T0164-a424 T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:160) |
| T0482-d3f1bf8e | docs/dev/roadmap/v0.2-overview.md | 479 | - [ ] T0165-0267 T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:161) |
| T0483-172dffd8 | docs/dev/roadmap/v0.2-overview.md | 480 | - [ ] T0166-de78 T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:162) |
| T0484-42c9f7db | docs/dev/roadmap/v0.2-overview.md | 481 | - [ ] T0167-3d4f T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:163) |
| T0485-581a8285 | docs/dev/roadmap/v0.2-overview.md | 482 | - [ ] T0168-3c90 T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:164) |
| T0486-4f5cafc3 | docs/dev/roadmap/v0.2-overview.md | 483 | - [ ] T0169-661b T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:165) |
| T0487-8fcc5ae0 | docs/dev/roadmap/v0.2-overview.md | 484 | - [ ] T0170-ebca T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:166) |
| T0488-684dd40d | docs/dev/roadmap/v0.2-overview.md | 485 | - [ ] T0171-ce42 T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:167) |
| T0489-306b38c5 | docs/dev/roadmap/v0.2-overview.md | 486 | - [ ] T0172-13c7 T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:168) |
| T0490-09ab2ec3 | docs/dev/roadmap/v0.2-overview.md | 487 | - [ ] T0173-d114 T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:169) |
| T0491-88a992c8 | docs/dev/roadmap/v0.2-overview.md | 488 | - [ ] T0174-b7c8 T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:170) |
| T0492-df03d56f | docs/dev/roadmap/v0.2-overview.md | 489 | - [ ] T0175-5b1e T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:171) |
| T0493-13e2007e | docs/dev/roadmap/v0.2-overview.md | 490 | - [ ] T0176-e2a0 T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:172) |
| T0494-4f751253 | docs/dev/roadmap/v0.2-overview.md | 491 | - [ ] T0177-b641 T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:173) |
| T0495-ce72d815 | docs/dev/roadmap/v0.2-overview.md | 492 | - [ ] T0178-644e T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:174) |
| T0496-1f67eba2 | docs/dev/roadmap/v0.2-overview.md | 493 | - [ ] T0179-60b4 T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:175) |
| T0497-e1710326 | docs/dev/roadmap/v0.2-overview.md | 494 | - [ ] T0180-817f T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:176) |
| T0498-2607be0e | docs/dev/roadmap/v0.2-overview.md | 495 | - [ ] T0181-f016 T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:177) |
| T0499-500a59d2 | docs/dev/roadmap/v0.2-overview.md | 496 | - [ ] T0182-462f T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:178) |
| T0500-fea32fe8 | docs/dev/roadmap/v0.2-overview.md | 497 | - [ ] T0183-b7c4 T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:179) |
| T0501-a4595294 | docs/dev/roadmap/v0.2-overview.md | 498 | - [ ] T0184-e931 T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:180) |
| T0502-da92ec45 | docs/dev/roadmap/v0.2-overview.md | 499 | - [ ] T0185-9d65 T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:181) |
| T0503-1a469dcf | docs/dev/roadmap/v0.2-overview.md | 500 | - [ ] T0186-d08d T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:182) |
| T0504-168db6ae | docs/dev/roadmap/v0.2-overview.md | 501 | - [ ] T0187-1ae5 T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:183) |
| T0505-71713c1f | docs/dev/roadmap/v0.2-overview.md | 502 | - [ ] T0188-2593 T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:184) |
| T0506-48a1ab40 | docs/dev/roadmap/v0.2-overview.md | 503 | - [ ] T0189-0db8 T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:185) |
| T0507-f03d68dd | docs/dev/roadmap/v0.2-overview.md | 504 | - [ ] T0190-21b4 T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:186) |
| T0508-a301edd0 | docs/dev/roadmap/v0.2-overview.md | 505 | - [ ] T0191-6abe T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:187) |
| T0509-a1efc3bf | docs/dev/roadmap/v0.2-overview.md | 506 | - [ ] T0192-6cf6 T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:188) |
| T0510-0e38a1d3 | docs/dev/roadmap/v0.2-overview.md | 507 | - [ ] T0193-402b T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:189) |
| T0511-ba77f939 | docs/dev/roadmap/v0.2-overview.md | 508 | - [ ] T0194-9595 T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.2-overview.md:190) |
| T0512-d0c7e208 | docs/dev/roadmap/v0.2-overview.md | 509 | - [ ] T0195-dae5 T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.2-overview.md:191) |
| T0513-fed2cfc6 | docs/dev/roadmap/v0.2-overview.md | 510 | - [ ] T0196-e896 T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.2-overview.md:192) |
| T0514-9043d2c8 | docs/dev/roadmap/v0.2-overview.md | 511 | - [ ] T0197-1ee3 T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.2-overview.md:193) |
| T0515-a7371371 | docs/dev/roadmap/v0.2-overview.md | 512 | - [ ] T0198-06e7 T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.2-overview.md:194) |
| T0516-ece64d92 | docs/dev/roadmap/v0.2-overview.md | 513 | - [ ] T0199-513a T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.2-overview.md:195) |
| T0517-8e5366be | docs/dev/roadmap/v0.2-overview.md | 514 | - [ ] T0200-28c4 T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.2-overview.md:196) |
| T0518-87ad7e59 | docs/dev/roadmap/v0.2-overview.md | 515 | - [ ] T0201-42c3 T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.2-overview.md:197) |
| T0519-d8665d34 | docs/dev/roadmap/v0.2-overview.md | 516 | - [ ] T0202-bd4e T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.2-overview.md:198) |
| T0520-4fed5d02 | docs/dev/roadmap/v0.2-overview.md | 517 | - [ ] T0203-495f T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.2-overview.md:199) |
| T0521-e4a1c4f2 | docs/dev/roadmap/v0.2-overview.md | 518 | - [ ] T0204-be79 T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.2-overview.md:200) |
| T0522-e07027bc | docs/dev/roadmap/v0.2-overview.md | 519 | - [ ] T0205-75ce T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.2-overview.md:201) |
| T0523-ffc47ab3 | docs/dev/roadmap/v0.2-overview.md | 520 | - [ ] T0206-0fa4 T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.2-overview.md:202) |
| T0524-b394abd9 | docs/dev/roadmap/v0.2-overview.md | 521 | - [ ] T0207-45f9 T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.2-overview.md:203) |
| T0525-d609f4ff | docs/dev/roadmap/v0.2-overview.md | 522 | - [ ] T0208-604a T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.2-overview.md:204) |
| T0526-b1ccefbe | docs/dev/roadmap/v0.2-overview.md | 523 | - [ ] T0209-8385 T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.2-overview.md:205) |
| T0527-4e8cceba | docs/dev/roadmap/v0.2-overview.md | 524 | - [ ] T0210-83e9 T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.2-overview.md:206) |
| T0528-912fb444 | docs/dev/roadmap/v0.2-overview.md | 525 | - [ ] T0211-c2da T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.2-overview.md:207) |
| T0529-253016c4 | docs/dev/roadmap/v0.2-overview.md | 526 | - [ ] T0212-e321 T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.2-overview.md:208) |
| T0530-f9f3bd8f | docs/dev/roadmap/v0.2-overview.md | 527 | - [ ] T0213-90c2 T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.2-overview.md:209) |
| T0531-20540aba | docs/dev/roadmap/v0.2-overview.md | 528 | - [ ] T0214-dbb7 T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.2-overview.md:210) |
| T0532-ba4d32d5 | docs/dev/roadmap/v0.2-overview.md | 529 | - [ ] T0215-45f9 T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.2-overview.md:211) |
| T0533-ef904e1f | docs/dev/roadmap/v0.2-overview.md | 530 | - [ ] T0216-c57b T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.2-overview.md:212) |
| T0534-0cdaa428 | docs/dev/roadmap/v0.2-overview.md | 531 | - [ ] T0217-24e1 T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.2-overview.md:213) |
| T0535-0157f952 | docs/dev/roadmap/v0.2-overview.md | 532 | - [ ] T0218-68cf T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.2-overview.md:214) |
| T0536-f8e7d58b | docs/dev/roadmap/v0.2-overview.md | 533 | - [ ] T0219-45ed T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.2-overview.md:215) |
| T0537-4ce21557 | docs/dev/roadmap/v0.2-overview.md | 534 | - [ ] T0220-6c4d T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.2-overview.md:216) |
| T0538-0d803c30 | docs/dev/roadmap/v0.2-overview.md | 535 | - [ ] T0221-d81b T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.2-overview.md:217) |
| T0539-9b29d50f | docs/dev/roadmap/v0.2-overview.md | 536 | - [ ] T0222-1afc T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.2-overview.md:218) |
| T0540-cff083c5 | docs/dev/roadmap/v0.2-overview.md | 537 | - [ ] T0223-cc17 T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.2-overview.md:219) |
| T0541-0d28d8c7 | docs/dev/roadmap/v0.2-overview.md | 538 | - [ ] T0224-ffd8 T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.2-overview.md:220) |
| T0542-a8f54432 | docs/dev/roadmap/v0.2-overview.md | 539 | - [ ] T0225-1977 T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.2-overview.md:221) |
| T0543-3636a1db | docs/dev/roadmap/v0.2-overview.md | 540 | - [ ] T0226-8f55 T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.2-overview.md:222) |
| T0544-9c683205 | docs/dev/roadmap/v0.2-overview.md | 541 | - [ ] T0227-1fb4 T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.2-overview.md:223) |
| T0545-53fd101d | docs/dev/roadmap/v0.2-overview.md | 542 | - [ ] T0228-f631 T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.2-overview.md:224) |
| T0546-3adae25a | docs/dev/roadmap/v0.2-overview.md | 543 | - [ ] T0229-5b09 T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.2-overview.md:225) |
| T0547-3cdd8e98 | docs/dev/roadmap/v0.2-overview.md | 544 | - [ ] T0230-0992 T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.2-overview.md:226) |
| T0548-add0961a | docs/dev/roadmap/v0.2-overview.md | 545 | - [ ] T0231-2147 T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.2-overview.md:227) |
| T0549-428b9842 | docs/dev/roadmap/v0.2-overview.md | 546 | - [ ] T0232-2c69 T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.2-overview.md:228) |
| T0550-7b12d172 | docs/dev/roadmap/v0.2-overview.md | 547 | - [ ] T0233-f8fe T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.2-overview.md:229) |
| T0551-a1d1a887 | docs/dev/roadmap/v0.2-overview.md | 548 | - [ ] T0234-c938 T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.2-overview.md:230) |
| T0552-769748ab | docs/dev/roadmap/v0.2-overview.md | 549 | - [ ] T0235-6a56 T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.2-overview.md:231) |
| T0553-4333aebc | docs/dev/roadmap/v0.2-overview.md | 550 | - [ ] T0236-b0d4 T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.2-overview.md:232) |
| T0554-aef31e34 | docs/dev/roadmap/v0.2-overview.md | 551 | - [ ] T0237-7052 T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.2-overview.md:233) |
| T0555-39b5595c | docs/dev/roadmap/v0.2-overview.md | 552 | - [ ] T0238-fa2f T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.2-overview.md:234) |
| T0556-ebd7d2cc | docs/dev/roadmap/v0.2-overview.md | 553 | - [ ] T0239-3b7d T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.2-overview.md:235) |
| T0557-f1011bfd | docs/dev/roadmap/v0.2-overview.md | 554 | - [ ] T0240-d830 T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.2-overview.md:236) |
| T0558-e4da0b1a | docs/dev/roadmap/v0.2-overview.md | 555 | - [ ] T0241-c27f T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.2-overview.md:237) |
| T0559-6aea5277 | docs/dev/roadmap/v0.2-overview.md | 556 | - [ ] T0242-9665 T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.2-overview.md:238) |
| T0560-26eacac3 | docs/dev/roadmap/v0.2-overview.md | 557 | - [ ] T0243-9fbd T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.2-overview.md:239) |
| T0561-02faf12e | docs/dev/roadmap/v0.2-overview.md | 558 | - [ ] T0244-40aa T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.2-overview.md:240) |
| T0562-7eecefbf | docs/dev/roadmap/v0.2-overview.md | 559 | - [ ] T0245-6f20 T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.2-overview.md:241) |
| T0563-3b0ed370 | docs/dev/roadmap/v0.2-overview.md | 560 | - [ ] T0246-a197 T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.2-overview.md:242) |
| T0564-f1c0d9fb | docs/dev/roadmap/v0.2-overview.md | 561 | - [ ] T0247-096c T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.2-overview.md:243) |
| T0565-f2f875c3 | docs/dev/roadmap/v0.2-overview.md | 562 | - [ ] T0248-fd6c T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:244) |
| T0566-0f918e50 | docs/dev/roadmap/v0.2-overview.md | 563 | - [ ] T0249-6364 T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:245) |
| T0567-7b04b4e5 | docs/dev/roadmap/v0.2-overview.md | 564 | - [ ] T0250-07e7 T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:246) |
| T0568-5aa82668 | docs/dev/roadmap/v0.2-overview.md | 565 | - [ ] T0251-6d34 T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:247) |
| T0569-77c241a4 | docs/dev/roadmap/v0.2-overview.md | 566 | - [ ] T0252-df35 T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:248) |
| T0570-cb7805af | docs/dev/roadmap/v0.2-overview.md | 567 | - [ ] T0253-d812 T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:249) |
| T0571-05ac2fb0 | docs/dev/roadmap/v0.2-overview.md | 568 | - [ ] T0254-6215 T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:250) |
| T0572-13a77a23 | docs/dev/roadmap/v0.2-overview.md | 569 | - [ ] T0255-38eb T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:251) |
| T0573-50380dfa | docs/dev/roadmap/v0.2-overview.md | 570 | - [ ] T0256-7713 T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:252) |
| T0574-8178068a | docs/dev/roadmap/v0.2-overview.md | 571 | - [ ] T0257-698e T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:253) |
| T0575-1f21d6a0 | docs/dev/roadmap/v0.2-overview.md | 572 | - [ ] T0258-6de5 T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:254) |
| T0576-1df015cd | docs/dev/roadmap/v0.2-overview.md | 573 | - [ ] T0259-8bd2 T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:255) |
| T0577-d48ca6aa | docs/dev/roadmap/v0.2-overview.md | 574 | - [ ] T0260-111d T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:256) |
| T0578-2a0d70ca | docs/dev/roadmap/v0.2-overview.md | 575 | - [ ] T0261-bb0f T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:257) |
| T0579-2df35d9d | docs/dev/roadmap/v0.2-overview.md | 576 | - [ ] T0262-a94d T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:258) |
| T0580-b2bb2f89 | docs/dev/roadmap/v0.2-overview.md | 577 | - [ ] T0263-2ede T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:259) |
| T0581-0a0f6370 | docs/dev/roadmap/v0.2-overview.md | 578 | - [ ] T0264-d22a T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:260) |
| T0582-23407841 | docs/dev/roadmap/v0.2-overview.md | 579 | - [ ] T0265-7d1a T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:261) |
| T0583-4cad0535 | docs/dev/roadmap/v0.2-overview.md | 580 | - [ ] T0266-c7ab T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:262) |
| T0584-45cbae5a | docs/dev/roadmap/v0.2-overview.md | 581 | - [ ] T0267-0cf5 T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:263) |
| T0585-0a761c0b | docs/dev/roadmap/v0.2-overview.md | 582 | - [ ] T0268-8bdd T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:264) |
| T0586-9e7506ed | docs/dev/roadmap/v0.2-overview.md | 583 | - [ ] T0269-09d0 T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:265) |
| T0587-c0bf1b3d | docs/dev/roadmap/v0.2-overview.md | 584 | - [ ] T0270-0a32 T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:266) |
| T0588-e9ba964e | docs/dev/roadmap/v0.2-overview.md | 585 | - [ ] T0271-4601 T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:267) |
| T0589-495d753a | docs/dev/roadmap/v0.2-overview.md | 586 | - [ ] T0272-547e T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:268) |
| T0590-b3368012 | docs/dev/roadmap/v0.2-overview.md | 587 | - [ ] T0273-4c9f T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:269) |
| T0591-bdccfaac | docs/dev/roadmap/v0.2-overview.md | 588 | - [ ] T0274-2185 T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:270) |
| T0592-a8fc3741 | docs/dev/roadmap/v0.2-overview.md | 589 | - [ ] T0275-8ba6 T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:271) |
| T0593-c96b9ab3 | docs/dev/roadmap/v0.2-overview.md | 590 | - [ ] T0276-0886 T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:272) |
| T0594-5d587fcf | docs/dev/roadmap/v0.2-overview.md | 591 | - [ ] T0277-9b3c T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:273) |
| T0595-a282107e | docs/dev/roadmap/v0.2-overview.md | 592 | - [ ] T0278-8770 T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:274) |
| T0596-d285f245 | docs/dev/roadmap/v0.2-overview.md | 593 | - [ ] T0279-65a3 T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:275) |
| T0597-5354139e | docs/dev/roadmap/v0.2-overview.md | 594 | - [ ] T0280-59b1 T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:276) |
| T0598-37c2e5a7 | docs/dev/roadmap/v0.2-overview.md | 595 | - [ ] T0281-404e T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:277) |
| T0599-e3cf8dbf | docs/dev/roadmap/v0.2-overview.md | 596 | - [ ] T0282-faf0 T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:278) |
| T0600-95b06b9c | docs/dev/roadmap/v0.2-overview.md | 597 | - [ ] T0283-87f9 T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:279) |
| T0601-d274c143 | docs/dev/roadmap/v0.2-overview.md | 598 | - [ ] T0284-1140 T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:280) |
| T0602-3dead2ef | docs/dev/roadmap/v0.2-overview.md | 599 | - [ ] T0285-d98b T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:281) |
| T0603-696dcb1d | docs/dev/roadmap/v0.2-overview.md | 600 | - [ ] T0286-016a T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:282) |
| T0604-2e3f8f84 | docs/dev/roadmap/v0.2-overview.md | 601 | - [ ] T0287-db81 T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:283) |
| T0605-4e7be069 | docs/dev/roadmap/v0.2-overview.md | 602 | - [ ] T0288-2f06 T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:284) |
| T0606-1c9e390f | docs/dev/roadmap/v0.2-overview.md | 603 | - [ ] T0289-665f T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:285) |
| T0607-629c04f1 | docs/dev/roadmap/v0.2-overview.md | 604 | - [ ] T0290-cae7 T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:286) |
| T0608-05f7f0d7 | docs/dev/roadmap/v0.2-overview.md | 605 | - [ ] T0291-77df T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:287) |
| T0609-879a3a09 | docs/dev/roadmap/v0.2-overview.md | 606 | - [ ] T0292-effb T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:288) |
| T0610-25f7f08f | docs/dev/roadmap/v0.2-overview.md | 607 | - [ ] T0293-5185 T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:289) |
| T0611-6112b94b | docs/dev/roadmap/v0.2-overview.md | 608 | - [ ] T0294-db1c T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:290) |
| T0612-b6fdbc67 | docs/dev/roadmap/v0.2-overview.md | 609 | - [ ] T0295-a73a T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:291) |
| T0613-e2cfa892 | docs/dev/roadmap/v0.2-overview.md | 610 | - [ ] T0296-6ded T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:292) |
| T0614-41c45ed1 | docs/dev/roadmap/v0.2-overview.md | 611 | - [ ] T0297-c86b T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:293) |
| T0615-5759bcf3 | docs/dev/roadmap/v0.2-overview.md | 612 | - [ ] T0298-5be9 T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:294) |
| T0616-391e1d6f | docs/dev/roadmap/v0.2-overview.md | 613 | - [ ] T0299-5adc T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:295) |
| T0617-8620434d | docs/dev/roadmap/v0.2-overview.md | 614 | - [ ] T0300-ceff T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:296) |
| T0618-ed184723 | docs/dev/roadmap/v0.2-overview.md | 615 | - [ ] T0301-0486 T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:297) |
| T0619-5360c039 | docs/dev/roadmap/v0.2-overview.md | 616 | - [ ] T0302-ea26 T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:298) |
| T0620-1a4d3d10 | docs/dev/roadmap/v0.2-overview.md | 617 | - [ ] T0303-004d T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:299) |
| T0621-dcef2498 | docs/dev/roadmap/v0.2-overview.md | 618 | - [ ] T0304-0dc1 T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:300) |
| T0622-2a4356fe | docs/dev/roadmap/v0.2-overview.md | 619 | - [ ] T0305-adc8 T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:301) |
| T0623-71fc5ed8 | docs/dev/roadmap/v0.2-overview.md | 620 | - [ ] T0306-48eb T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:302) |
| T0624-0cd0809a | docs/dev/roadmap/v0.2-overview.md | 621 | - [ ] T0307-5ed6 T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:303) |
| T0625-fb6c8af1 | docs/dev/roadmap/v0.2-overview.md | 622 | - [ ] T0308-d86f T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:304) |
| T0626-f25c1046 | docs/dev/roadmap/v0.2-overview.md | 623 | - [ ] T0309-8393 T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:305) |
| T0627-2f6ace61 | docs/dev/roadmap/v0.2-overview.md | 624 | - [ ] T0310-8d04 T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:306) |
| T0628-e4bd1e0e | docs/dev/roadmap/v0.2-overview.md | 625 | - [ ] T0311-a424 T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:307) |
| T0629-3a38f7e0 | docs/dev/roadmap/v0.2-overview.md | 626 | - [ ] T0312-9cfd T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:308) |
| T0630-7afee5b8 | docs/dev/roadmap/v0.2-overview.md | 627 | - [ ] T0313-41b0 T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:309) |
| T0631-95d670f0 | docs/dev/roadmap/v0.2-overview.md | 628 | - [ ] T0314-0b12 T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:310) |
| T0632-050410de | docs/dev/roadmap/v0.2-overview.md | 629 | - [ ] T0315-640a T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:311) |
| T0633-4c2e29df | docs/dev/roadmap/v0.2-overview.md | 630 | - [ ] T0316-1516 T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:312) |
| T0634-85710a82 | docs/dev/roadmap/v0.2-overview.md | 631 | - [ ] T0317-9ec6 T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:313) |
| T0635-50a5982b | docs/dev/roadmap/v0.2-overview.md | 632 | - [ ] T0318-a391 T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:314) |
| T0636-f3b3836e | docs/dev/roadmap/v0.2-overview.md | 633 | - [ ] T0319-991c T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:315) |
| T0637-852bc405 | docs/dev/roadmap/v0.2-overview.md | 634 | - [ ] T0320-5b39 T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.2-overview.md:316) |
| T0638-c4575de4 | docs/dev/roadmap/v0.2-overview.md | 635 | - [ ] T0321-4526 T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.2-overview.md:317) |
| T0639-04a6499b | docs/dev/roadmap/v0.2-overview.md | 636 | - [ ] T0322-39ab T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:318) |
| T0640-39e8f0be | docs/dev/roadmap/v0.2-overview.md | 637 | - [ ] T0323-0b47 T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:319) |
| T0641-06e06a9a | docs/dev/roadmap/v0.2-overview.md | 638 | - [ ] T0324-4cb0 T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:320) |
| T0642-7a79438e | docs/dev/roadmap/v0.2-overview.md | 639 | - [ ] T0325-9818 T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:321) |
| T0643-92c016bf | docs/dev/roadmap/v0.2-overview.md | 640 | - [ ] T0326-e1ad T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:322) |
| T0644-12e9aa86 | docs/dev/roadmap/v0.2-overview.md | 641 | - [ ] T0327-9936 T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:323) |
| T0645-f3737cc1 | docs/dev/roadmap/v0.2-overview.md | 642 | - [ ] T0328-e569 T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:324) |
| T0646-0fc044c2 | docs/dev/roadmap/v0.2-overview.md | 643 | - [ ] T0329-58a8 T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:325) |
| T0647-3520249d | docs/dev/roadmap/v0.2-overview.md | 644 | - [ ] T0330-dfa0 T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:326) |
| T0648-d70a3613 | docs/dev/roadmap/v0.2-overview.md | 645 | - [ ] T0331-5799 T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.2-overview.md:327) |
| T0649-7cc02d5a | docs/dev/roadmap/v0.2-overview.md | 646 | - [ ] T0332-4485 T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.2-overview.md:328) |
| T0650-f63c78f3 | docs/dev/roadmap/v0.2-overview.md | 647 | - [ ] T0333-d0f6 T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.2-overview.md:329) |
| T0651-6ab84c82 | docs/dev/roadmap/v0.2-overview.md | 648 | - [ ] T0334-ff96 T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.2-overview.md:330) |
| T0652-38264be8 | docs/dev/roadmap/v0.2-overview.md | 649 | - [ ] T0335-9703 T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.2-overview.md:331) |
| T0653-ff35fb9d | docs/dev/roadmap/v0.2-overview.md | 650 | - [ ] T0336-209c T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.2-overview.md:332) |
| T0654-b47fb198 | docs/dev/roadmap/v0.2-overview.md | 651 | - [ ] T0337-31ca T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.2-overview.md:333) |
| T0655-a285b32e | docs/dev/roadmap/v0.2-overview.md | 652 | - [ ] T0338-abf1 T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.2-overview.md:334) |
| T0656-e8ad93a1 | docs/dev/roadmap/v0.2-overview.md | 653 | - [ ] T0339-a36a T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.2-overview.md:335) |
| T0657-c7349976 | docs/dev/roadmap/v0.2-overview.md | 654 | - [ ] T0340-bb3f T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.2-overview.md:336) |
| T0658-3286e109 | docs/dev/roadmap/v0.2-overview.md | 655 | - [ ] T0341-708f T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.2-overview.md:337) |
| T0659-0afb4015 | docs/dev/roadmap/v0.2-overview.md | 656 | - [ ] T0342-2e90 T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.2-overview.md:338) |
| T0660-68b3666e | docs/dev/roadmap/v0.2-overview.md | 657 | - [ ] T0343-83f7 T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.2-overview.md:339) |
| T0661-aa6d7a63 | docs/dev/roadmap/v0.2-overview.md | 658 | - [ ] T0344-0793 T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.2-overview.md:340) |
| T0662-26574a74 | docs/dev/roadmap/v0.2-overview.md | 659 | - [ ] T0345-5dd2 T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.2-overview.md:341) |
| T0663-2496ea7d | docs/dev/roadmap/v0.2-overview.md | 660 | - [ ] T0346-9ce8 T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.2-overview.md:342) |
| T0664-acb73d3a | docs/dev/roadmap/v0.2-overview.md | 661 | - [ ] T0347-957c T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.2-overview.md:343) |
| T0665-bd156a1e | docs/dev/roadmap/v0.2-overview.md | 662 | - [ ] T0348-d289 T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.2-overview.md:344) |
| T0666-8d32b281 | docs/dev/roadmap/v0.2-overview.md | 663 | - [ ] T0349-36b6 T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.2-overview.md:345) |
| T0667-d3cd3fca | docs/dev/roadmap/v0.2-overview.md | 664 | - [ ] T0350-2797 T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.2-overview.md:346) |
| T0668-97651123 | docs/dev/roadmap/v0.2-overview.md | 665 | - [ ] T0351-00bb T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.2-overview.md:347) |
| T0669-8df33a88 | docs/dev/roadmap/v0.2-overview.md | 666 | - [ ] T0352-f33d T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.2-overview.md:348) |
| T0670-6099a93c | docs/dev/roadmap/v0.2-overview.md | 667 | - [ ] T0353-fa4f T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.2-overview.md:349) |
| T0671-8bb9e5c2 | docs/dev/roadmap/v0.2-overview.md | 668 | - [ ] T0354-eb32 T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.2-overview.md:350) |
| T0672-ac5a091f | docs/dev/roadmap/v0.2-overview.md | 669 | - [ ] T0355-df06 T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.2-overview.md:351) |
| T0673-84eb7ff3 | docs/dev/roadmap/v0.2-overview.md | 670 | - [ ] T0356-e364 T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.2-overview.md:352) |
| T0674-ca903445 | docs/dev/roadmap/v0.2-overview.md | 671 | - [ ] T0357-d372 T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.2-overview.md:353) |
| T0675-ab0e5f35 | docs/dev/roadmap/v0.2-overview.md | 672 | - [ ] T0358-411f T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.2-overview.md:354) |
| T0676-6047a8e8 | docs/dev/roadmap/v0.2-overview.md | 673 | - [ ] T0359-609d T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.2-overview.md:355) |
| T0677-0d98107f | docs/dev/roadmap/v0.2-overview.md | 674 | - [ ] T0360-a163 T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.2-overview.md:356) |
| T0678-9a3af589 | docs/dev/roadmap/v0.2-overview.md | 675 | - [ ] T0361-e3f7 T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.2-overview.md:357) |
| T0679-8bb58346 | docs/dev/roadmap/v0.2-overview.md | 676 | - [ ] T0362-0fc9 T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.2-overview.md:358) |
| T0680-c099b674 | docs/dev/roadmap/v0.2-overview.md | 677 | - [ ] T0363-7e62 T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.2-overview.md:359) |
| T0681-36b8fb06 | docs/dev/roadmap/v0.2-overview.md | 678 | - [ ] T0364-c662 T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.2-overview.md:360) |
| T0682-9db6ffa0 | docs/dev/roadmap/v0.2-overview.md | 679 | - [ ] T0365-c8a1 T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.2-overview.md:361) |
| T0683-0f1eeb3d | docs/dev/roadmap/v0.2-overview.md | 680 | - [ ] T0366-fb89 T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.2-overview.md:362) |
| T0684-03d01200 | docs/dev/roadmap/v0.2-overview.md | 681 | - [ ] T0367-f414 T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.2-overview.md:363) |
| T0685-3297976d | docs/dev/roadmap/v0.2-overview.md | 682 | - [ ] T0368-c9f9 T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.2-overview.md:364) |
| T0686-fa4223b4 | docs/dev/roadmap/v0.2-overview.md | 683 | - [ ] T0369-b47d T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.2-overview.md:365) |
| T0687-fddd8c19 | docs/dev/roadmap/v0.2-overview.md | 684 | - [ ] T0370-8b59 T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.2-overview.md:366) |
| T0688-fa1deec9 | docs/dev/roadmap/v0.2-overview.md | 685 | - [ ] T0371-c576 T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.2-overview.md:367) |
| T0689-32f59127 | docs/dev/roadmap/v0.2-overview.md | 686 | - [ ] T0372-25d0 T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.2-overview.md:368) |
| T0690-b18d1291 | docs/dev/roadmap/v0.2-overview.md | 687 | - [ ] T0373-ee91 T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.2-overview.md:369) |
| T0691-d7632cc1 | docs/dev/roadmap/v0.2-overview.md | 688 | - [ ] T0374-48e9 T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.2-overview.md:370) |
| T0692-73bb79c4 | docs/dev/roadmap/v0.2-overview.md | 689 | - [ ] T0375-bc2b T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.2-overview.md:371) |
| T0693-17d2930d | docs/dev/roadmap/v0.2-overview.md | 690 | - [ ] T0376-1026 T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.2-overview.md:372) |
| T0694-4e98dfa2 | docs/dev/roadmap/v0.2-overview.md | 691 | - [ ] T0377-6445 T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.2-overview.md:373) |
| T0695-6510d70a | docs/dev/roadmap/v0.2-overview.md | 692 | - [ ] T0378-9d1f T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.2-overview.md:374) |
| T0696-4641a687 | docs/dev/roadmap/v0.2-overview.md | 693 | - [ ] T0379-8488 T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.2-overview.md:375) |
| T0697-5caee4df | docs/dev/roadmap/v0.2-overview.md | 694 | - [ ] T0380-bb04 T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.2-overview.md:376) |
| T0698-9fcec23b | docs/dev/roadmap/v0.2-overview.md | 695 | - [ ] T0381-9815 T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.2-overview.md:377) |
| T0699-e2209df4 | docs/dev/roadmap/v0.2-overview.md | 696 | - [ ] T0382-36f3 T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.2-overview.md:378) |
| T0700-414e4bf0 | docs/dev/roadmap/v0.2-overview.md | 697 | - [ ] T0383-dbc9 T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.2-overview.md:379) |
| T0701-76cc28e6 | docs/dev/roadmap/v0.2-overview.md | 698 | - [ ] T0384-eb3f T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.2-overview.md:380) |
| T0702-de7d7a6e | docs/dev/roadmap/v0.2-overview.md | 699 | - [ ] T0385-ec08 T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.2-overview.md:381) |
| T0703-44d25c4c | docs/dev/roadmap/v0.2-overview.md | 700 | - [ ] T0386-5337 T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.2-overview.md:382) |
| T0704-0f188a58 | docs/dev/roadmap/v0.2-overview.md | 701 | - [ ] T0387-294c T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.2-overview.md:383) |
| T0705-269b5a23 | docs/dev/roadmap/v0.2-overview.md | 702 | - [ ] T0388-ac9f T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.2-overview.md:384) |
| T0706-48cbcb22 | docs/dev/roadmap/v0.2-overview.md | 703 | - [ ] T0389-87f9 T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.2-overview.md:385) |
| T0707-7f098eda | docs/dev/roadmap/v0.2-overview.md | 704 | - [ ] T0390-b2f6 T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.2-overview.md:386) |
| T0708-7388ffaa | docs/dev/roadmap/v0.2-overview.md | 705 | - [ ] T0391-5af2 T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.2-overview.md:387) |
| T0709-4323c6a0 | docs/dev/roadmap/v0.2-overview.md | 706 | - [ ] T0392-b5f9 T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.2-overview.md:388) |
| T0710-e9442663 | docs/dev/roadmap/v0.2-overview.md | 707 | - [ ] T0393-f9f9 T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.2-overview.md:389) |
| T0711-833596f9 | docs/dev/roadmap/v0.2-overview.md | 708 | - [ ] T0394-5750 T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.2-overview.md:390) |
| T0712-144982f1 | docs/dev/roadmap/v0.2-overview.md | 709 | - [ ] T0395-617a T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.2-overview.md:391) |
| T0713-2ed4db6a | docs/dev/roadmap/v0.2-overview.md | 710 | - [ ] T0396-1b6b T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.2-overview.md:392) |
| T0714-d889d97d | docs/dev/roadmap/v0.2-overview.md | 711 | - [ ] T0397-42f6 T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.2-overview.md:393) |
| T0715-55d230dd | docs/dev/roadmap/v0.2-overview.md | 712 | - [ ] T0398-c5e5 T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.2-overview.md:394) |
| T0716-54847a0e | docs/dev/roadmap/v0.2-overview.md | 713 | - [ ] T0399-8f5a T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.2-overview.md:395) |
| T0717-29cfefe2 | docs/dev/roadmap/v0.2-overview.md | 714 | - [ ] T0400-9dd2 T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.2-overview.md:396) |
| T0718-fd012b97 | docs/dev/roadmap/v0.2-overview.md | 715 | - [ ] T0401-3c46 T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.2-overview.md:397) |
| T0719-81fa713a | docs/dev/roadmap/v0.2-overview.md | 716 | - [ ] T0402-4454 T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.2-overview.md:398) |
| T0720-a971ac57 | docs/dev/roadmap/v0.2-overview.md | 717 | - [ ] T0403-147a T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.2-overview.md:399) |
| T0721-62599dff | docs/dev/roadmap/v0.2-overview.md | 718 | - [ ] T0404-9c10 T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.2-overview.md:400) |
| T0722-2e9e3e70 | docs/dev/roadmap/v0.2-overview.md | 719 | - [ ] T0405-2e18 T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.2-overview.md:401) |
| T0723-8c3ea828 | docs/dev/roadmap/v0.2-overview.md | 720 | - [ ] T0406-3617 T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.2-overview.md:402) |
| T0724-35b44684 | docs/dev/roadmap/v0.2-overview.md | 721 | - [ ] T0407-10b9 T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.2-overview.md:403) |
| T0725-85d83a4d | docs/dev/roadmap/v0.2-overview.md | 722 | - [ ] T0408-00c0 T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.2-overview.md:404) |
| T0726-98fde222 | docs/dev/roadmap/v0.2-overview.md | 723 | - [ ] T0409-13fe T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.2-overview.md:405) |
| T0727-b8c77f29 | docs/dev/roadmap/v0.2-overview.md | 724 | - [ ] T0410-8137 T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.2-overview.md:406) |
| T0728-01159c4d | docs/dev/roadmap/v0.2-overview.md | 725 | - [ ] T0411-9f65 T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.2-overview.md:407) |
| T0729-21a08346 | docs/dev/roadmap/v0.2-overview.md | 726 | - [ ] T0412-285e T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.2-overview.md:408) |
| T0730-c43308b8 | docs/dev/roadmap/v0.2-overview.md | 727 | - [ ] T0413-50d0 T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.2-overview.md:409) |
| T0731-216cf537 | docs/dev/roadmap/v0.2-overview.md | 728 | - [ ] T0414-a18e T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.2-overview.md:410) |
| T0732-568743a5 | docs/dev/roadmap/v0.2-overview.md | 729 | - [ ] T0415-8a8a T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.2-overview.md:411) |
| T0733-fe817097 | docs/dev/roadmap/v0.2-overview.md | 730 | - [ ] T0416-45d6 T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.2-overview.md:412) |
| T0734-a5f83bd8 | docs/dev/roadmap/v0.2-overview.md | 731 | - [ ] T0417-2e67 T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.2-overview.md:413) |
| T0735-b3d2fa83 | docs/dev/roadmap/v0.2-overview.md | 732 | - [ ] T0418-7a82 T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.2-overview.md:414) |
| T0736-11d6b280 | docs/dev/roadmap/v0.2-overview.md | 733 | - [ ] T0419-8a3a T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.2-overview.md:415) |
| T0737-71c2d45d | docs/dev/roadmap/v0.2-overview.md | 734 | - [ ] T0420-9453 T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.2-overview.md:416) |
| T0738-bcdc70ab | docs/dev/roadmap/v0.2-overview.md | 735 | - [ ] T0421-32d2 T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.2-overview.md:417) |
| T0739-9a339749 | docs/dev/roadmap/v0.2-overview.md | 736 | - [ ] T0422-fd2c T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.2-overview.md:418) |
| T0740-b140cad7 | docs/dev/roadmap/v0.2-overview.md | 737 | - [ ] T0423-6119 T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.2-overview.md:419) |
| T0741-a2692188 | docs/dev/roadmap/v0.2-overview.md | 738 | - [ ] T0424-851a T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.2-overview.md:420) |
| T0742-8949c067 | docs/dev/roadmap/v0.2-overview.md | 739 | - [ ] T0842-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T0743-2c39769a | docs/dev/roadmap/v0.2-overview.md | 740 | - [ ] T0843-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T0744-f706bc27 | docs/dev/roadmap/v0.2-overview.md | 741 | - [ ] T0844-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T0745-ed766d53 | docs/dev/roadmap/v0.2-overview.md | 742 | - [ ] T0845-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T0746-b3430038 | docs/dev/roadmap/v0.2-overview.md | 743 | - [ ] T0846-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T0747-192d516d | docs/dev/roadmap/v0.2-overview.md | 744 | - [ ] T0847-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T0748-a813a129 | docs/dev/roadmap/v0.2-overview.md | 745 | - [ ] T0848-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T0749-83e38be2 | docs/dev/roadmap/v0.2-overview.md | 746 | - [ ] T0849-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T0750-cfee3ca7 | docs/dev/roadmap/v0.2-overview.md | 747 | - [ ] T0850-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T0751-71aca73f | docs/dev/roadmap/v0.2-overview.md | 748 | - [ ] T0851-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T0752-edb6d516 | docs/dev/roadmap/v0.2-overview.md | 749 | - [ ] T0852-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T0753-7f5ee41a | docs/dev/roadmap/v0.2-overview.md | 750 | - [ ] T0853-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T0754-795c6cb0 | docs/dev/roadmap/v0.2-overview.md | 751 | - [ ] T0854-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T0755-eff7064c | docs/dev/roadmap/v0.2-overview.md | 752 | - [ ] T0855-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T0756-fa0ab3b3 | docs/dev/roadmap/v0.2-overview.md | 753 | - [ ] T0856-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T0757-433dc040 | docs/dev/roadmap/v0.2-overview.md | 754 | - [ ] T0857-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T0758-32cfbf27 | docs/dev/roadmap/v0.2-overview.md | 755 | - [ ] T0858-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T0759-7ca6f27e | docs/dev/roadmap/v0.2-overview.md | 756 | - [ ] T0859-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T0760-ea46adcd | docs/dev/roadmap/v0.2-overview.md | 757 | - [ ] T0860-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T0761-fbcd0e3b | docs/dev/roadmap/v0.2-overview.md | 758 | - [ ] T0861-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T0762-94e0c52e | docs/dev/roadmap/v0.2-overview.md | 759 | - [ ] T0862-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T0763-6d72bac7 | docs/dev/roadmap/v0.2-overview.md | 760 | - [ ] T0863-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T0764-4d33d935 | docs/dev/roadmap/v0.2-overview.md | 761 | - [ ] T0864-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T0765-2f2fd772 | docs/dev/roadmap/v0.2-overview.md | 762 | - [ ] T0865-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T0766-add94dc2 | docs/dev/roadmap/v0.2-overview.md | 763 | - [ ] T0866-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T0767-c70d299c | docs/dev/roadmap/v0.2-overview.md | 764 | - [ ] T0867-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T0768-401ced0e | docs/dev/roadmap/v0.2-overview.md | 765 | - [ ] T0868-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T0769-5eff4aa5 | docs/dev/roadmap/v0.2-overview.md | 766 | - [ ] T0869-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T0770-9bec9811 | docs/dev/roadmap/v0.2-overview.md | 767 | - [ ] T0870-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T0771-e8475418 | docs/dev/roadmap/v0.2-overview.md | 768 | - [ ] T0871-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T0772-99a00801 | docs/dev/roadmap/v0.2-overview.md | 769 | - [ ] T0872-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T0773-76005b8a | docs/dev/roadmap/v0.2-overview.md | 770 | - [ ] T0873-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T0774-77f0ca76 | docs/dev/roadmap/v0.2-overview.md | 771 | - [ ] T0874-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T0775-e32b7367 | docs/dev/roadmap/v0.2-overview.md | 772 | - [ ] T0875-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T0776-aec5e204 | docs/dev/roadmap/v0.2-overview.md | 773 | - [ ] T0876-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T0777-303ae4e2 | docs/dev/roadmap/v0.2-overview.md | 774 | - [ ] T0877-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T0778-b81c5c70 | docs/dev/roadmap/v0.2-overview.md | 775 | - [ ] T0878-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T0779-53af72b3 | docs/dev/roadmap/v0.2-overview.md | 776 | - [ ] T0879-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T0780-f044bc9d | docs/dev/roadmap/v0.2-overview.md | 777 | - [ ] T0880-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T0781-67e22dcb | docs/dev/roadmap/v0.2-overview.md | 778 | - [ ] T0881-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T0782-b62a0c0e | docs/dev/roadmap/v0.2-overview.md | 779 | - [ ] T0882-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T0783-72e5d95f | docs/dev/roadmap/v0.2-overview.md | 780 | - [ ] T0883-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T0784-d364110e | docs/dev/roadmap/v0.2-overview.md | 781 | - [ ] T0884-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T0785-94b0448b | docs/dev/roadmap/v0.2-overview.md | 782 | - [ ] T0885-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T0786-0b29601b | docs/dev/roadmap/v0.2-overview.md | 783 | - [ ] T0886-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T0787-bbe3edd2 | docs/dev/roadmap/v0.2-overview.md | 784 | - [ ] T0887-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T0788-8248e8b6 | docs/dev/roadmap/v0.2-overview.md | 785 | - [ ] T0888-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T0789-ec7fbe3a | docs/dev/roadmap/v0.2-overview.md | 786 | - [ ] T0889-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T0790-62af5cdb | docs/dev/roadmap/v0.2-overview.md | 787 | - [ ] T0890-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T0791-504433b3 | docs/dev/roadmap/v0.2-overview.md | 788 | - [ ] T0891-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T0792-144d761e | docs/dev/roadmap/v0.2-overview.md | 789 | - [ ] T0892-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T0793-2421fcd1 | docs/dev/roadmap/v0.2-overview.md | 790 | - [ ] T0893-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T0794-f476b11a | docs/dev/roadmap/v0.2-overview.md | 791 | - [ ] T0894-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T0795-6ba34206 | docs/dev/roadmap/v0.2-overview.md | 792 | - [ ] T0895-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T0796-2092d909 | docs/dev/roadmap/v0.2-overview.md | 793 | - [ ] T0896-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T0797-5c5620eb | docs/dev/roadmap/v0.2-overview.md | 794 | - [ ] T0898-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T0798-ae77fe68 | docs/dev/roadmap/v0.2-overview.md | 795 | - [ ] T0899-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T0799-9eba81ca | docs/dev/roadmap/v0.2-overview.md | 796 | - [ ] T0900-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T0800-61873a19 | docs/dev/roadmap/v0.2-overview.md | 797 | - [ ] T0901-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T0801-475d66ae | docs/dev/roadmap/v0.2-overview.md | 798 | - [ ] T0902-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T0802-8d1a9bce | docs/dev/roadmap/v0.2-overview.md | 799 | - [ ] T0903-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T0803-7a7ccb8a | docs/dev/roadmap/v0.2-overview.md | 800 | - [ ] T0904-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T0804-be300f41 | docs/dev/roadmap/v0.2-overview.md | 801 | - [ ] T0905-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T0805-fb9d66b7 | docs/dev/roadmap/v0.2-overview.md | 802 | - [ ] T0906-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T0806-042a558d | docs/dev/roadmap/v0.2-overview.md | 803 | - [ ] T0907-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T0807-73a6d9cb | docs/dev/roadmap/v0.2-overview.md | 804 | - [ ] T0908-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T0808-9fff9b71 | docs/dev/roadmap/v0.2-overview.md | 805 | - [ ] T0909-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T0809-7aae5675 | docs/dev/roadmap/v0.2-overview.md | 806 | - [ ] T0910-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T0810-d5e389fe | docs/dev/roadmap/v0.2-overview.md | 807 | - [ ] T0911-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T0811-0fd801f5 | docs/dev/roadmap/v0.2-overview.md | 808 | - [ ] T0912-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T0812-ce854c00 | docs/dev/roadmap/v0.2-overview.md | 809 | - [ ] T0913-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T0813-90e059ab | docs/dev/roadmap/v0.2-overview.md | 810 | - [ ] T0914-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T0814-9cacbce6 | docs/dev/roadmap/v0.2-overview.md | 811 | - [ ] T0915-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T0815-2ac04cf7 | docs/dev/roadmap/v0.2-overview.md | 812 | - [ ] T0916-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T0816-08c6aa98 | docs/dev/roadmap/v0.2-overview.md | 813 | - [ ] T0917-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T0817-84717d50 | docs/dev/roadmap/v0.2-overview.md | 814 | - [ ] T0918-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T0818-8e4d9964 | docs/dev/roadmap/v0.2-overview.md | 815 | - [ ] T0919-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T0819-fff536e7 | docs/dev/roadmap/v0.2-overview.md | 816 | - [ ] T0920-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T0820-f6a71dfd | docs/dev/roadmap/v0.2-overview.md | 817 | - [ ] T0921-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T0821-69e0075f | docs/dev/roadmap/v0.2-overview.md | 818 | - [ ] T0922-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T0822-1598486e | docs/dev/roadmap/v0.2-overview.md | 819 | - [ ] T0923-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T0823-cfea2900 | docs/dev/roadmap/v0.2-overview.md | 820 | - [ ] T0924-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T0824-b2814823 | docs/dev/roadmap/v0.2-overview.md | 821 | - [ ] T0925-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T0825-664e7080 | docs/dev/roadmap/v0.2-overview.md | 822 | - [ ] T0926-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T0826-23bb5f0d | docs/dev/roadmap/v0.2-overview.md | 823 | - [ ] T0927-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T0827-788fc9c1 | docs/dev/roadmap/v0.2-overview.md | 824 | - [ ] T0928-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T0828-ffdac77e | docs/dev/roadmap/v0.2-overview.md | 825 | - [ ] T0929-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T0829-04c8a64a | docs/dev/roadmap/v0.2-overview.md | 826 | - [ ] T0930-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T0830-558676e5 | docs/dev/roadmap/v0.2-overview.md | 827 | - [ ] T0931-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T0831-24266d1a | docs/dev/roadmap/v0.2-overview.md | 828 | - [ ] T0932-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T0832-7a8ae619 | docs/dev/roadmap/v0.2-overview.md | 829 | - [ ] T0933-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T0833-318d9d0b | docs/dev/roadmap/v0.2-overview.md | 830 | - [ ] T0934-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T0834-8f201ec7 | docs/dev/roadmap/v0.2-overview.md | 831 | - [ ] T0935-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T0835-e854c35f | docs/dev/roadmap/v0.2-overview.md | 832 | - [ ] T0936-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T0836-35f98cda | docs/dev/roadmap/v0.2-overview.md | 833 | - [ ] T0937-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T0837-3b5f96dc | docs/dev/roadmap/v0.2-overview.md | 834 | - [ ] T0938-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T0838-b52a2dda | docs/dev/roadmap/v0.2-overview.md | 835 | - [ ] T0939-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T0839-70e32d52 | docs/dev/roadmap/v0.2-overview.md | 836 | - [ ] T0940-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T0840-6143fda8 | docs/dev/roadmap/v0.2-overview.md | 837 | - [ ] T0941-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T0841-5f5822ff | docs/dev/roadmap/v0.2-overview.md | 838 | - [ ] T0942-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T0842-dc98bdd8 | docs/dev/roadmap/v0.2-overview.md | 839 | - [ ] T0943-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T0843-97d09690 | docs/dev/roadmap/v0.2-overview.md | 840 | - [ ] T0944-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T0844-715201db | docs/dev/roadmap/v0.2-overview.md | 841 | - [ ] T0945-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T0845-cd20ea89 | docs/dev/roadmap/v0.2-overview.md | 842 | - [ ] T0946-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T0846-36b384aa | docs/dev/roadmap/v0.2-overview.md | 843 | - [ ] T0947-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T0847-f5e560a8 | docs/dev/roadmap/v0.2-overview.md | 844 | - [ ] T0948-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T0848-9e530d0e | docs/dev/roadmap/v0.2-overview.md | 845 | - [ ] T0949-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T0849-c4a98613 | docs/dev/roadmap/v0.2-overview.md | 846 | - [ ] T0950-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T0850-0f43e45a | docs/dev/roadmap/v0.2-overview.md | 847 | - [ ] T0951-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T0851-983571ef | docs/dev/roadmap/v0.2-overview.md | 848 | - [ ] T0952-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T0852-a338e220 | docs/dev/roadmap/v0.2-overview.md | 849 | - [ ] T0953-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T0853-f1eefca6 | docs/dev/roadmap/v0.2-overview.md | 850 | - [ ] T0954-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T0854-8dfc6865 | docs/dev/roadmap/v0.2-overview.md | 851 | - [ ] T0955-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T0855-e9f7d41f | docs/dev/roadmap/v0.2-overview.md | 852 | - [ ] T0956-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T0856-42d304d5 | docs/dev/roadmap/v0.2-overview.md | 853 | - [ ] T0957-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T0857-4f5ba7d8 | docs/dev/roadmap/v0.2-overview.md | 854 | - [ ] T0958-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T0858-c844c447 | docs/dev/roadmap/v0.2-overview.md | 855 | - [ ] T0959-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T0859-b7d2819c | docs/dev/roadmap/v0.2-overview.md | 856 | - [ ] T0960-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T0860-87447a9c | docs/dev/roadmap/v0.2-overview.md | 857 | - [ ] T0961-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T0861-e2d7b7cc | docs/dev/roadmap/v0.2-overview.md | 858 | - [ ] T0962-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T0862-5fecf860 | docs/dev/roadmap/v0.2-overview.md | 859 | - [ ] T0963-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T0863-99bf6c7d | docs/dev/roadmap/v0.2-overview.md | 860 | - [ ] T0964-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T0864-73366f4a | docs/dev/roadmap/v0.2-overview.md | 861 | - [ ] T0965-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T0865-18f0c5dd | docs/dev/roadmap/v0.2-overview.md | 862 | - [ ] T0966-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T0866-be4361e6 | docs/dev/roadmap/v0.2-overview.md | 863 | - [ ] T0967-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T0867-54bcebe0 | docs/dev/roadmap/v0.2-overview.md | 864 | - [ ] T0968-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T0868-280d3cb5 | docs/dev/roadmap/v0.2-overview.md | 865 | - [ ] T0969-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T0869-882bdd01 | docs/dev/roadmap/v0.2-overview.md | 866 | - [ ] T0970-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T0870-0e2c6e44 | docs/dev/roadmap/v0.2-overview.md | 867 | - [ ] T0971-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T0871-39c08b1b | docs/dev/roadmap/v0.2-overview.md | 868 | - [ ] T0972-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T0872-2ef02dfc | docs/dev/roadmap/v0.2-overview.md | 869 | - [ ] T0973-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T0873-3a4ec3b0 | docs/dev/roadmap/v0.2-overview.md | 870 | - [ ] T0974-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T0874-ee62fd2a | docs/dev/roadmap/v0.2-overview.md | 871 | - [ ] T0975-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T0875-96ce902e | docs/dev/roadmap/v0.2-overview.md | 872 | - [ ] T0977-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T0876-5c156a06 | docs/dev/roadmap/v0.2-overview.md | 873 | - [ ] T0978-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T0877-beda5f4b | docs/dev/roadmap/v0.2-overview.md | 874 | - [ ] T0979-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T0878-076313b1 | docs/dev/roadmap/v0.2-overview.md | 875 | - [ ] T0980-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T0879-b3256b8c | docs/dev/roadmap/v0.2-overview.md | 876 | - [ ] T0981-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T0880-04d37b14 | docs/dev/roadmap/v0.2-overview.md | 877 | - [ ] T0982-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T0881-f5986de1 | docs/dev/roadmap/v0.2-overview.md | 878 | - [ ] T0983-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T0882-7cacfd6d | docs/dev/roadmap/v0.2-overview.md | 879 | - [ ] T0984-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T0883-ec851c11 | docs/dev/roadmap/v0.2-overview.md | 880 | - [ ] T0985-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T0884-12009afc | docs/dev/roadmap/v0.2-overview.md | 881 | - [ ] T0986-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T0885-e840637b | docs/dev/roadmap/v0.2-overview.md | 882 | - [ ] T0987-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T0886-fcd2424c | docs/dev/roadmap/v0.2-overview.md | 883 | - [ ] T0988-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T0887-53644c28 | docs/dev/roadmap/v0.2-overview.md | 884 | - [ ] T0989-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T0888-2d04dcbc | docs/dev/roadmap/v0.2-overview.md | 885 | - [ ] T0990-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T0889-03c2b4cc | docs/dev/roadmap/v0.2-overview.md | 886 | - [ ] T0991-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T0890-2f35b699 | docs/dev/roadmap/v0.2-overview.md | 887 | - [ ] T0992-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T0891-36259680 | docs/dev/roadmap/v0.2-overview.md | 888 | - [ ] T0993-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T0892-dd15f49c | docs/dev/roadmap/v0.2-overview.md | 889 | - [ ] T0994-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T0893-1be9413d | docs/dev/roadmap/v0.2-overview.md | 890 | - [ ] T0995-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T0894-75e10574 | docs/dev/roadmap/v0.2-overview.md | 891 | - [ ] T0996-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T0895-fe802c07 | docs/dev/roadmap/v0.2-overview.md | 892 | - [ ] T0997-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T0896-c8481841 | docs/dev/roadmap/v0.2-overview.md | 893 | - [ ] T0998-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T0897-b03302d3 | docs/dev/roadmap/v0.2-overview.md | 894 | - [ ] T0999-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T0898-232de387 | docs/dev/roadmap/v0.2-overview.md | 895 | - [ ] T1000-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T0899-c1809c06 | docs/dev/roadmap/v0.2-overview.md | 896 | - [ ] T1001-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T0900-34020cbe | docs/dev/roadmap/v0.2-overview.md | 897 | - [ ] T1002-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T0901-b2df199e | docs/dev/roadmap/v0.2-overview.md | 898 | - [ ] T1003-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T0902-b5a77ea1 | docs/dev/roadmap/v0.2-overview.md | 899 | - [ ] T1004-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T0903-a9dfff7c | docs/dev/roadmap/v0.2-overview.md | 900 | - [ ] T1005-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T0904-184aab81 | docs/dev/roadmap/v0.2-overview.md | 901 | - [ ] T1006-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T0905-4678f69e | docs/dev/roadmap/v0.2-overview.md | 902 | - [ ] T1007-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T0906-981f6b23 | docs/dev/roadmap/v0.2-overview.md | 903 | - [ ] T1008-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T0907-1ff573af | docs/dev/roadmap/v0.2-overview.md | 904 | - [ ] T1009-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T0908-77f0d981 | docs/dev/roadmap/v0.2-overview.md | 905 | - [ ] T1010-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T0909-4a05d167 | docs/dev/roadmap/v0.2-overview.md | 906 | - [ ] T1011-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T0910-5bb7e823 | docs/dev/roadmap/v0.2-overview.md | 907 | - [ ] T1012-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T0911-db322361 | docs/dev/roadmap/v0.2-overview.md | 908 | - [ ] T1013-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T0912-b5e96a2e | docs/dev/roadmap/v0.2-overview.md | 909 | - [ ] T1014-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T0913-7d1548e0 | docs/dev/roadmap/v0.2-overview.md | 910 | - [ ] T1015-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T0914-0a4f3754 | docs/dev/roadmap/v0.2-overview.md | 911 | - [ ] T1016-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T0915-f9f1f96d | docs/dev/roadmap/v0.2-overview.md | 912 | - [ ] T1017-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T0916-cb6b8833 | docs/dev/roadmap/v0.2-overview.md | 913 | - [ ] T1018-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T0917-a142c1dd | docs/dev/roadmap/v0.2-overview.md | 914 | - [ ] T1019-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T0918-ffbc0da5 | docs/dev/roadmap/v0.2-overview.md | 915 | - [ ] T1020-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T0919-e3d9825c | docs/dev/roadmap/v0.2-overview.md | 916 | - [ ] T1021-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T0920-39ef862e | docs/dev/roadmap/v0.2-overview.md | 917 | - [ ] T1022-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T0921-130582d1 | docs/dev/roadmap/v0.2-overview.md | 918 | - [ ] T1023-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T0922-368340b8 | docs/dev/roadmap/v0.2-overview.md | 919 | - [ ] T1024-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T0923-4070c0b3 | docs/dev/roadmap/v0.2-overview.md | 920 | - [ ] T1025-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T0924-2b5a21a9 | docs/dev/roadmap/v0.2-overview.md | 921 | - [ ] T1026-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T0925-957326a0 | docs/dev/roadmap/v0.2-overview.md | 922 | - [ ] T1027-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T0926-76cbd46f | docs/dev/roadmap/v0.2-overview.md | 923 | - [ ] T1028-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T0927-b052e0be | docs/dev/roadmap/v0.2-overview.md | 924 | - [ ] T1029-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T0928-87f29fcd | docs/dev/roadmap/v0.2-overview.md | 925 | - [ ] T1030-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T0929-608a06df | docs/dev/roadmap/v0.2-overview.md | 926 | - [ ] T1031-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T0930-8bdac235 | docs/dev/roadmap/v0.2-overview.md | 927 | - [ ] T1032-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T0931-24311450 | docs/dev/roadmap/v0.2-overview.md | 928 | - [ ] T1033-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T0932-6d771030 | docs/dev/roadmap/v0.2-overview.md | 929 | - [ ] T1035-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T0933-717d4fe5 | docs/dev/roadmap/v0.2-overview.md | 930 | - [ ] T1036-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T0934-984e561c | docs/dev/roadmap/v0.2-overview.md | 931 | - [ ] T1037-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T0935-4a591e67 | docs/dev/roadmap/v0.2-overview.md | 932 | - [ ] T1038-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T0936-8bfd2ce0 | docs/dev/roadmap/v0.2-overview.md | 933 | - [ ] T1039-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T0937-70a5400a | docs/dev/roadmap/v0.2-overview.md | 934 | - [ ] T1040-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T0938-df18581e | docs/dev/roadmap/v0.2-overview.md | 935 | - [ ] T1041-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T0939-f91889a6 | docs/dev/roadmap/v0.2-overview.md | 936 | - [ ] T1042-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T0940-0cea4564 | docs/dev/roadmap/v0.2-overview.md | 937 | - [ ] T1043-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T0941-ddc2a322 | docs/dev/roadmap/v0.2-overview.md | 938 | - [ ] T1044-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T0942-81c0ef4a | docs/dev/roadmap/v0.2-overview.md | 939 | - [ ] T1045-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T0943-ee3f9e85 | docs/dev/roadmap/v0.2-overview.md | 940 | - [ ] T1046-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T0944-735b0483 | docs/dev/roadmap/v0.2-overview.md | 941 | - [ ] T1047-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T0945-c695152f | docs/dev/roadmap/v0.2-overview.md | 942 | - [ ] T1048-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T0946-ffaabc94 | docs/dev/roadmap/v0.2-overview.md | 943 | - [ ] T1049-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T0947-3e68e0fa | docs/dev/roadmap/v0.2-overview.md | 944 | - [ ] T1050-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T0948-e0080ce1 | docs/dev/roadmap/v0.2-overview.md | 945 | - [ ] T1051-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T0949-196bfc72 | docs/dev/roadmap/v0.2-overview.md | 946 | - [ ] T1052-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T0950-f6f5f102 | docs/dev/roadmap/v0.2-overview.md | 947 | - [ ] T1053-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T0951-ebec206b | docs/dev/roadmap/v0.2-overview.md | 948 | - [ ] T1054-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T0952-2164b542 | docs/dev/roadmap/v0.2-overview.md | 949 | - [ ] T1055-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T0953-18ffac34 | docs/dev/roadmap/v0.2-overview.md | 950 | - [ ] T1056-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T0954-47f59355 | docs/dev/roadmap/v0.2-overview.md | 951 | - [ ] T1057-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T0955-9e1f011c | docs/dev/roadmap/v0.2-overview.md | 952 | - [ ] T1058-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T0956-9d67cd80 | docs/dev/roadmap/v0.2-overview.md | 953 | - [ ] T1059-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T0957-8a98848a | docs/dev/roadmap/v0.2-overview.md | 954 | - [ ] T1060-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T0958-b2c73133 | docs/dev/roadmap/v0.2-overview.md | 955 | - [ ] T1061-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T0959-684c84ee | docs/dev/roadmap/v0.2-overview.md | 956 | - [ ] T1062-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T0960-e6ed070e | docs/dev/roadmap/v0.2-overview.md | 957 | - [ ] T1063-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T0961-99c71591 | docs/dev/roadmap/v0.2-overview.md | 958 | - [ ] T1064-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T0962-de2506a2 | docs/dev/roadmap/v0.2-overview.md | 959 | - [ ] T1065-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T0963-481ab037 | docs/dev/roadmap/v0.2-overview.md | 960 | - [ ] T1066-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T0964-b9b17721 | docs/dev/roadmap/v0.2-overview.md | 961 | - [ ] T1067-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T0965-67179a20 | docs/dev/roadmap/v0.2-overview.md | 962 | - [ ] T1068-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T0966-02c473d6 | docs/dev/roadmap/v0.2-overview.md | 963 | - [ ] T1069-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T0967-802f1788 | docs/dev/roadmap/v0.2-overview.md | 964 | - [ ] T1070-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T0968-d30539f5 | docs/dev/roadmap/v0.2-overview.md | 965 | - [ ] T1071-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T0969-efd00fde | docs/dev/roadmap/v0.2-overview.md | 966 | - [ ] T1072-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T0970-988ce28e | docs/dev/roadmap/v0.2-overview.md | 967 | - [ ] T1073-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T0971-cc599198 | docs/dev/roadmap/v0.2-overview.md | 968 | - [ ] T1074-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T0972-b971a233 | docs/dev/roadmap/v0.2-overview.md | 969 | - [ ] T1075-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T0973-59c84b00 | docs/dev/roadmap/v0.2-overview.md | 970 | - [ ] T1076-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T0974-5bf46e79 | docs/dev/roadmap/v0.2-overview.md | 971 | - [ ] T1077-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T0975-6f2e1ad8 | docs/dev/roadmap/v0.2-overview.md | 972 | - [ ] T1078-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T0976-787f5168 | docs/dev/roadmap/v0.2-overview.md | 973 | - [ ] T1079-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T0977-b7ae4fcd | docs/dev/roadmap/v0.2-overview.md | 974 | - [ ] T1080-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T0978-b20656c4 | docs/dev/roadmap/v0.2-overview.md | 975 | - [ ] T1081-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T0979-5d0d845f | docs/dev/roadmap/v0.2-overview.md | 976 | - [ ] T1082-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T0980-cdb8773d | docs/dev/roadmap/v0.2-overview.md | 977 | - [ ] T1083-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T0981-49430cc3 | docs/dev/roadmap/v0.2-overview.md | 978 | - [ ] T1084-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T0982-d16625f0 | docs/dev/roadmap/v0.2-overview.md | 979 | - [ ] T1085-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T0983-00b691e8 | docs/dev/roadmap/v0.2-overview.md | 980 | - [ ] T1086-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T0984-2c058ea2 | docs/dev/roadmap/v0.2-overview.md | 981 | - [ ] T1087-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T0985-55f7edf4 | docs/dev/roadmap/v0.2-overview.md | 982 | - [ ] T1088-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T0986-6800e9d6 | docs/dev/roadmap/v0.2-overview.md | 983 | - [ ] T1089-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T0987-4ff2c104 | docs/dev/roadmap/v0.2-overview.md | 984 | - [ ] T1090-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T0988-4419a89f | docs/dev/roadmap/v0.2-overview.md | 985 | - [ ] T1091-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T0989-639648b9 | docs/dev/roadmap/v0.2-overview.md | 986 | - [ ] T1092-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T0990-0a224f83 | docs/dev/roadmap/v0.2-overview.md | 987 | - [ ] T1093-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T0991-085ffeaf | docs/dev/roadmap/v0.2-overview.md | 988 | - [ ] T1094-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T0992-cc1e4523 | docs/dev/roadmap/v0.2-overview.md | 989 | - [ ] T1095-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T0993-fddcbecc | docs/dev/roadmap/v0.2-overview.md | 990 | - [ ] T1096-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T0994-8d91c2e9 | docs/dev/roadmap/v0.2-overview.md | 991 | - [ ] T1097-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T0995-5d8e0765 | docs/dev/roadmap/v0.2-overview.md | 992 | - [ ] T1098-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T0996-66f84016 | docs/dev/roadmap/v0.2-overview.md | 993 | - [ ] T1099-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T0997-47739681 | docs/dev/roadmap/v0.2-overview.md | 994 | - [ ] T1100-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T0998-666cafcf | docs/dev/roadmap/v0.2-overview.md | 995 | - [ ] T1101-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T0999-20011d55 | docs/dev/roadmap/v0.2-overview.md | 996 | - [ ] T1102-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T1000-f43696b6 | docs/dev/roadmap/v0.2-overview.md | 997 | - [ ] T1103-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T1001-656a8c9a | docs/dev/roadmap/v0.2-overview.md | 998 | - [ ] T1104-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T1002-dd59db0f | docs/dev/roadmap/v0.2-overview.md | 999 | - [ ] T1105-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T1003-4ba4dd01 | docs/dev/roadmap/v0.2-overview.md | 1000 | - [ ] T1106-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T1004-66e570f7 | docs/dev/roadmap/v0.2-overview.md | 1001 | - [ ] T1107-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T1005-4b3194b6 | docs/dev/roadmap/v0.2-overview.md | 1002 | - [ ] T1108-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T1006-8f977fc0 | docs/dev/roadmap/v0.2-overview.md | 1003 | - [ ] T1109-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T1007-d36fd75c | docs/dev/roadmap/v0.2-overview.md | 1004 | - [ ] T1110-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T1008-6c28b9e9 | docs/dev/roadmap/v0.2-overview.md | 1005 | - [ ] T1111-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T1009-383c2547 | docs/dev/roadmap/v0.2-overview.md | 1006 | - [ ] T1112-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T1010-3925961f | docs/dev/roadmap/v0.2-overview.md | 1007 | - [ ] T1113-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T1011-fa1afa92 | docs/dev/roadmap/v0.2-overview.md | 1008 | - [ ] T1114-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T1012-d659e163 | docs/dev/roadmap/v0.2-overview.md | 1009 | - [ ] T1115-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T1013-cf0f1dfb | docs/dev/roadmap/v0.2-overview.md | 1010 | - [ ] T1116-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T1014-f041b858 | docs/dev/roadmap/v0.2-overview.md | 1011 | - [ ] T1117-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T1015-f6c295dc | docs/dev/roadmap/v0.2-overview.md | 1012 | - [ ] T1118-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T1016-46359296 | docs/dev/roadmap/v0.2-overview.md | 1013 | - [ ] T1119-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T1017-f6648432 | docs/dev/roadmap/v0.2-overview.md | 1014 | - [ ] T1120-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T1018-d7961b8f | docs/dev/roadmap/v0.2-overview.md | 1015 | - [ ] T1121-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T1019-c8cfa981 | docs/dev/roadmap/v0.2-overview.md | 1016 | - [ ] T1122-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T1020-0da4cc03 | docs/dev/roadmap/v0.2-overview.md | 1017 | - [ ] T1123-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T1021-83135f1a | docs/dev/roadmap/v0.2-overview.md | 1018 | - [ ] T1124-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T1022-08c4ac71 | docs/dev/roadmap/v0.2-overview.md | 1019 | - [ ] T1125-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T1023-64e55d15 | docs/dev/roadmap/v0.2-overview.md | 1020 | - [ ] T1126-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T1024-fbb461c0 | docs/dev/roadmap/v0.2-overview.md | 1021 | - [ ] T1127-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T1025-610d751c | docs/dev/roadmap/v0.2-overview.md | 1022 | - [ ] T1128-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T1026-329b112f | docs/dev/roadmap/v0.2-overview.md | 1023 | - [ ] T1129-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T1027-15cf891b | docs/dev/roadmap/v0.2-overview.md | 1024 | - [ ] T1130-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T1028-4491f6c3 | docs/dev/roadmap/v0.2-overview.md | 1025 | - [ ] T1131-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T1029-789bb449 | docs/dev/roadmap/v0.2-overview.md | 1026 | - [ ] T1132-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T1030-87ff7849 | docs/dev/roadmap/v0.2-overview.md | 1027 | - [ ] T1133-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T1031-2426d90c | docs/dev/roadmap/v0.2-overview.md | 1028 | - [ ] T1134-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T1032-7f026d04 | docs/dev/roadmap/v0.2-overview.md | 1029 | - [ ] T1135-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T1033-7f41c7d0 | docs/dev/roadmap/v0.2-overview.md | 1030 | - [ ] T1136-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T1034-fc8b4cd5 | docs/dev/roadmap/v0.2-overview.md | 1031 | - [ ] T1137-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T1035-3a27ecc2 | docs/dev/roadmap/v0.2-overview.md | 1032 | - [ ] T1138-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T1036-8d539bb0 | docs/dev/roadmap/v0.2-overview.md | 1033 | - [ ] T1139-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T1037-28335e26 | docs/dev/roadmap/v0.2-overview.md | 1034 | - [ ] T1140-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T1038-304b3a56 | docs/dev/roadmap/v0.2-overview.md | 1035 | - [ ] T1141-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T1039-930c5b15 | docs/dev/roadmap/v0.2-overview.md | 1036 | - [ ] T1142-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T1040-ea84d16a | docs/dev/roadmap/v0.2-overview.md | 1037 | - [ ] T1143-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T1041-0a0e6caf | docs/dev/roadmap/v0.2-overview.md | 1038 | - [ ] T1144-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T1042-f3d97bd3 | docs/dev/roadmap/v0.2-overview.md | 1039 | - [ ] T1145-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T1043-d61b7e7b | docs/dev/roadmap/v0.2-overview.md | 1040 | - [ ] T1146-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T1044-1432124b | docs/dev/roadmap/v0.2-overview.md | 1041 | - [ ] T1147-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T1045-ba47d0cb | docs/dev/roadmap/v0.2-overview.md | 1042 | - [ ] T1148-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T1046-5f35bbaf | docs/dev/roadmap/v0.2-overview.md | 1043 | - [ ] T1149-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T1047-db90fe50 | docs/dev/roadmap/v0.2-overview.md | 1044 | - [ ] T1150-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T1048-3fd331d1 | docs/dev/roadmap/v0.2-overview.md | 1045 | - [ ] T1151-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T1049-ff08a8ab | docs/dev/roadmap/v0.2-overview.md | 1046 | - [ ] T1152-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T1050-20cbfde9 | docs/dev/roadmap/v0.2-overview.md | 1047 | - [ ] T1153-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T1051-af9b6b95 | docs/dev/roadmap/v0.2-overview.md | 1048 | - [ ] T1154-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T1052-e6041996 | docs/dev/roadmap/v0.2-overview.md | 1049 | - [ ] T1155-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T1053-6800c042 | docs/dev/roadmap/v0.2-overview.md | 1050 | - [ ] T1156-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T1054-32631ce6 | docs/dev/roadmap/v0.2-overview.md | 1051 | - [ ] T1157-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T1055-56e6183a | docs/dev/roadmap/v0.2-overview.md | 1052 | - [ ] T1158-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T1056-756725ff | docs/dev/roadmap/v0.2-overview.md | 1053 | - [ ] T1159-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T1057-419456ce | docs/dev/roadmap/v0.2-overview.md | 1054 | - [ ] T1160-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T1058-b186d743 | docs/dev/roadmap/v0.2-overview.md | 1055 | - [ ] T1161-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T1059-8db74c4f | docs/dev/roadmap/v0.2-overview.md | 1056 | - [ ] T1162-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T1060-5cb0be47 | docs/dev/roadmap/v0.2-overview.md | 1057 | - [ ] T0425-b2e3 T0107-c900 T0159-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.2-overview.md:103) (docs/dev/roadmap/v0.2-overview.md:421) |
| T1061-1d79d190 | docs/dev/roadmap/v0.2-overview.md | 1058 | - [ ] T0426-c2ec T0108-993d T0160-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.2-overview.md:104) (docs/dev/roadmap/v0.2-overview.md:422) |
| T1062-da11f877 | docs/dev/roadmap/v0.2-overview.md | 1059 | - [ ] T0427-aabd T0109-a50e T0161-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.2-overview.md:105) (docs/dev/roadmap/v0.2-overview.md:423) |
| T1063-b27c4d26 | docs/dev/roadmap/v0.2-overview.md | 1060 | - [ ] T0428-ad50 T0110-aa9c T0162-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.2-overview.md:106) (docs/dev/roadmap/v0.2-overview.md:424) |
| T1064-47567416 | docs/dev/roadmap/v0.2-overview.md | 1061 | - [ ] T0429-44d8 T0111-029c T0163-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.2-overview.md:107) (docs/dev/roadmap/v0.2-overview.md:425) |
| T1065-a5a3adb0 | docs/dev/roadmap/v0.2-overview.md | 1062 | - [ ] T0430-0771 T0112-f95d T0164-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.2-overview.md:108) (docs/dev/roadmap/v0.2-overview.md:426) |
| T1066-c06ff692 | docs/dev/roadmap/v0.2-overview.md | 1063 | - [ ] T0431-283b T0113-9052 T0165-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:109) (docs/dev/roadmap/v0.2-overview.md:427) |
| T1067-74a79267 | docs/dev/roadmap/v0.2-overview.md | 1064 | - [ ] T0432-9acd T0114-73c9 T0166-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:110) (docs/dev/roadmap/v0.2-overview.md:428) |
| T1068-604c8058 | docs/dev/roadmap/v0.2-overview.md | 1065 | - [ ] T0433-3ab9 T0115-4d3f T0167-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:111) (docs/dev/roadmap/v0.2-overview.md:429) |
| T1069-0b65f987 | docs/dev/roadmap/v0.2-overview.md | 1066 | - [ ] T0434-52a0 T0116-07a6 T0168-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:112) (docs/dev/roadmap/v0.2-overview.md:430) |
| T1070-fc851e47 | docs/dev/roadmap/v0.2-overview.md | 1067 | - [ ] T0435-b317 T0117-4b6d T0169-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:113) (docs/dev/roadmap/v0.2-overview.md:431) |
| T1071-7767dbe2 | docs/dev/roadmap/v0.2-overview.md | 1068 | - [ ] T0436-b860 T0118-0eb7 T0170-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:114) (docs/dev/roadmap/v0.2-overview.md:432) |
| T1072-8eade5f3 | docs/dev/roadmap/v0.2-overview.md | 1069 | - [ ] T0437-da11 T0119-bf23 T0171-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:115) (docs/dev/roadmap/v0.2-overview.md:433) |
| T1073-b7a42e5d | docs/dev/roadmap/v0.2-overview.md | 1070 | - [ ] T0438-60c8 T0120-e436 T0172-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:116) (docs/dev/roadmap/v0.2-overview.md:434) |
| T1074-246556a0 | docs/dev/roadmap/v0.2-overview.md | 1071 | - [ ] T0439-d5c5 T0121-23d3 T0173-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:117) (docs/dev/roadmap/v0.2-overview.md:435) |
| T1075-be789a15 | docs/dev/roadmap/v0.2-overview.md | 1072 | - [ ] T0440-3e89 T0122-d79e T0174-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:118) (docs/dev/roadmap/v0.2-overview.md:436) |
| T1076-132a6984 | docs/dev/roadmap/v0.2-overview.md | 1073 | - [ ] T0441-dd87 T0123-17bb T0175-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:119) (docs/dev/roadmap/v0.2-overview.md:437) |
| T1077-a8a5fe4b | docs/dev/roadmap/v0.2-overview.md | 1074 | - [ ] T0442-d13f T0124-6fe0 T0176-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:120) (docs/dev/roadmap/v0.2-overview.md:438) |
| T1078-78b6ca87 | docs/dev/roadmap/v0.2-overview.md | 1075 | - [ ] T0443-c2b1 T0125-9422 T0177-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:121) (docs/dev/roadmap/v0.2-overview.md:439) |
| T1079-2f0f2275 | docs/dev/roadmap/v0.2-overview.md | 1076 | - [ ] T0444-1eda T0126-1648 T0178-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:122) (docs/dev/roadmap/v0.2-overview.md:440) |
| T1080-215c49b0 | docs/dev/roadmap/v0.2-overview.md | 1077 | - [ ] T0445-56c0 T0127-04d4 T0179-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:123) (docs/dev/roadmap/v0.2-overview.md:441) |
| T1081-2544adf4 | docs/dev/roadmap/v0.2-overview.md | 1078 | - [ ] T0446-77a4 T0128-504c T0180-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:124) (docs/dev/roadmap/v0.2-overview.md:442) |
| T1082-f3c445a6 | docs/dev/roadmap/v0.2-overview.md | 1079 | - [ ] T0447-7c01 T0129-8642 T0181-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:125) (docs/dev/roadmap/v0.2-overview.md:443) |
| T1083-047dcf74 | docs/dev/roadmap/v0.2-overview.md | 1080 | - [ ] T0448-827d T0130-8ea1 T0182-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:126) (docs/dev/roadmap/v0.2-overview.md:444) |
| T1084-fb5f1358 | docs/dev/roadmap/v0.2-overview.md | 1081 | - [ ] T0449-030b T0131-4396 T0183-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:127) (docs/dev/roadmap/v0.2-overview.md:445) |
| T1085-1886c722 | docs/dev/roadmap/v0.2-overview.md | 1082 | - [ ] T0450-25a2 T0132-f8e4 T0184-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:128) (docs/dev/roadmap/v0.2-overview.md:446) |
| T1086-7fba03fe | docs/dev/roadmap/v0.2-overview.md | 1083 | - [ ] T0451-641a T0133-fa5e T0185-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:129) (docs/dev/roadmap/v0.2-overview.md:447) |
| T1087-26e711de | docs/dev/roadmap/v0.2-overview.md | 1084 | - [ ] T0452-e68a T0134-2334 T0186-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:130) (docs/dev/roadmap/v0.2-overview.md:448) |
| T1088-e8476f9f | docs/dev/roadmap/v0.2-overview.md | 1085 | - [ ] T0453-ea33 T0135-dfe5 T0187-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:131) (docs/dev/roadmap/v0.2-overview.md:449) |
| T1089-97641e48 | docs/dev/roadmap/v0.2-overview.md | 1086 | - [ ] T0454-951b T0136-b1a3 T0188-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:132) (docs/dev/roadmap/v0.2-overview.md:450) |
| T1090-4061afa0 | docs/dev/roadmap/v0.2-overview.md | 1087 | - [ ] T0455-7ccf T0137-60ad T0189-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:133) (docs/dev/roadmap/v0.2-overview.md:451) |
| T1091-9390898a | docs/dev/roadmap/v0.2-overview.md | 1088 | - [ ] T0456-956a T0138-0b24 T0190-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:134) (docs/dev/roadmap/v0.2-overview.md:452) |
| T1092-fca1c51b | docs/dev/roadmap/v0.2-overview.md | 1089 | - [ ] T0457-3609 T0139-e439 T0191-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:135) (docs/dev/roadmap/v0.2-overview.md:453) |
| T1093-f62b5657 | docs/dev/roadmap/v0.2-overview.md | 1090 | - [ ] T0458-9e54 T0140-bc80 T0192-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:136) (docs/dev/roadmap/v0.2-overview.md:454) |
| T1094-a2cdf3ef | docs/dev/roadmap/v0.2-overview.md | 1091 | - [ ] T0459-2933 T0141-46b0 T0193-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:137) (docs/dev/roadmap/v0.2-overview.md:455) |
| T1095-fd8c2a30 | docs/dev/roadmap/v0.2-overview.md | 1092 | - [ ] T0460-fffe T0142-21f0 T0194-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:138) (docs/dev/roadmap/v0.2-overview.md:456) |
| T1096-3e3f50ca | docs/dev/roadmap/v0.2-overview.md | 1093 | - [ ] T0461-31f8 T0143-6637 T0195-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:139) (docs/dev/roadmap/v0.2-overview.md:457) |
| T1097-6620fe1c | docs/dev/roadmap/v0.2-overview.md | 1094 | - [ ] T0462-176d T0144-203c T0196-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:140) (docs/dev/roadmap/v0.2-overview.md:458) |
| T1098-f0e3bf9d | docs/dev/roadmap/v0.2-overview.md | 1095 | - [ ] T0463-ece0 T0145-5dc5 T0197-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:141) (docs/dev/roadmap/v0.2-overview.md:459) |
| T1099-fb2223c0 | docs/dev/roadmap/v0.2-overview.md | 1096 | - [ ] T0464-f216 T0146-10b0 T0198-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:142) (docs/dev/roadmap/v0.2-overview.md:460) |
| T1100-19944031 | docs/dev/roadmap/v0.2-overview.md | 1097 | - [ ] T0465-12b6 T0147-90e5 T0199-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:143) (docs/dev/roadmap/v0.2-overview.md:461) |
| T1101-d83f2395 | docs/dev/roadmap/v0.2-overview.md | 1098 | - [ ] T0466-0530 T0148-3465 T0200-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:144) (docs/dev/roadmap/v0.2-overview.md:462) |
| T1102-8a5ff5b7 | docs/dev/roadmap/v0.2-overview.md | 1099 | - [ ] T0467-89ba T0149-ea22 T0201-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:145) (docs/dev/roadmap/v0.2-overview.md:463) |
| T1103-bd0d3363 | docs/dev/roadmap/v0.2-overview.md | 1100 | - [ ] T0468-9df9 T0150-4c65 T0202-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:146) (docs/dev/roadmap/v0.2-overview.md:464) |
| T1104-5d4a4ba1 | docs/dev/roadmap/v0.2-overview.md | 1101 | - [ ] T0469-9399 T0151-2fd6 T0203-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:147) (docs/dev/roadmap/v0.2-overview.md:465) |
| T1105-6229f93a | docs/dev/roadmap/v0.2-overview.md | 1102 | - [ ] T0470-8d04 T0152-3de7 T0204-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:148) (docs/dev/roadmap/v0.2-overview.md:466) |
| T1106-30609a09 | docs/dev/roadmap/v0.2-overview.md | 1103 | - [ ] T0471-647f T0153-1141 T0205-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:149) (docs/dev/roadmap/v0.2-overview.md:467) |
| T1107-1d2527b7 | docs/dev/roadmap/v0.2-overview.md | 1104 | - [ ] T0472-2f7b T0154-e25b T0206-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:150) (docs/dev/roadmap/v0.2-overview.md:468) |
| T1108-68ba6345 | docs/dev/roadmap/v0.2-overview.md | 1105 | - [ ] T0473-8ff9 T0155-52ee T0207-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:151) (docs/dev/roadmap/v0.2-overview.md:469) |
| T1109-c47fb6f9 | docs/dev/roadmap/v0.2-overview.md | 1106 | - [ ] T0474-38d3 T0156-a970 T0208-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:152) (docs/dev/roadmap/v0.2-overview.md:470) |
| T1110-7a3f3f12 | docs/dev/roadmap/v0.2-overview.md | 1107 | - [ ] T0475-b545 T0157-eb70 T0209-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:153) (docs/dev/roadmap/v0.2-overview.md:471) |
| T1111-60f281a3 | docs/dev/roadmap/v0.2-overview.md | 1108 | - [ ] T0476-f78f T0158-c59f T0210-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:154) (docs/dev/roadmap/v0.2-overview.md:472) |
| T1112-e4860a52 | docs/dev/roadmap/v0.2-overview.md | 1109 | - [ ] T0477-d8e1 T0159-e81e T0211-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:155) (docs/dev/roadmap/v0.2-overview.md:473) |
| T1113-07c38c0e | docs/dev/roadmap/v0.2-overview.md | 1110 | - [ ] T0478-9cfd T0160-f48b T0212-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:156) (docs/dev/roadmap/v0.2-overview.md:474) |
| T1114-207a7e76 | docs/dev/roadmap/v0.2-overview.md | 1111 | - [ ] T0479-fc68 T0161-4486 T0213-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:157) (docs/dev/roadmap/v0.2-overview.md:475) |
| T1115-b1d391df | docs/dev/roadmap/v0.2-overview.md | 1112 | - [ ] T0480-6790 T0162-2a68 T0215-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:158) (docs/dev/roadmap/v0.2-overview.md:476) |
| T1116-48324c08 | docs/dev/roadmap/v0.2-overview.md | 1113 | - [ ] T0481-4d10 T0163-3932 T0216-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:159) (docs/dev/roadmap/v0.2-overview.md:477) |
| T1117-bbc7cd62 | docs/dev/roadmap/v0.2-overview.md | 1114 | - [ ] T0482-c2a0 T0164-a424 T0217-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:160) (docs/dev/roadmap/v0.2-overview.md:478) |
| T1118-b4c4f9b8 | docs/dev/roadmap/v0.2-overview.md | 1115 | - [ ] T0483-d3f1 T0165-0267 T0218-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:161) (docs/dev/roadmap/v0.2-overview.md:479) |
| T1119-d154e6c5 | docs/dev/roadmap/v0.2-overview.md | 1116 | - [ ] T0484-172d T0166-de78 T0219-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:162) (docs/dev/roadmap/v0.2-overview.md:480) |
| T1120-fe0eda39 | docs/dev/roadmap/v0.2-overview.md | 1117 | - [ ] T0485-42c9 T0167-3d4f T0220-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:163) (docs/dev/roadmap/v0.2-overview.md:481) |
| T1121-38a0422c | docs/dev/roadmap/v0.2-overview.md | 1118 | - [ ] T0486-581a T0168-3c90 T0221-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:164) (docs/dev/roadmap/v0.2-overview.md:482) |
| T1122-f8fd85df | docs/dev/roadmap/v0.2-overview.md | 1119 | - [ ] T0487-4f5c T0169-661b T0222-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:165) (docs/dev/roadmap/v0.2-overview.md:483) |
| T1123-6e589828 | docs/dev/roadmap/v0.2-overview.md | 1120 | - [ ] T0488-8fcc T0170-ebca T0223-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:166) (docs/dev/roadmap/v0.2-overview.md:484) |
| T1124-353659f2 | docs/dev/roadmap/v0.2-overview.md | 1121 | - [ ] T0489-684d T0171-ce42 T0224-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:167) (docs/dev/roadmap/v0.2-overview.md:485) |
| T1125-2c538289 | docs/dev/roadmap/v0.2-overview.md | 1122 | - [ ] T0490-306b T0172-13c7 T0225-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:168) (docs/dev/roadmap/v0.2-overview.md:486) |
| T1126-08678e5b | docs/dev/roadmap/v0.2-overview.md | 1123 | - [ ] T0491-09ab T0173-d114 T0226-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:169) (docs/dev/roadmap/v0.2-overview.md:487) |
| T1127-08dbe81d | docs/dev/roadmap/v0.2-overview.md | 1124 | - [ ] T0492-88a9 T0174-b7c8 T0227-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:170) (docs/dev/roadmap/v0.2-overview.md:488) |
| T1128-fa753b60 | docs/dev/roadmap/v0.2-overview.md | 1125 | - [ ] T0493-df03 T0175-5b1e T0228-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:171) (docs/dev/roadmap/v0.2-overview.md:489) |
| T1129-48f8c743 | docs/dev/roadmap/v0.2-overview.md | 1126 | - [ ] T0494-13e2 T0176-e2a0 T0229-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:172) (docs/dev/roadmap/v0.2-overview.md:490) |
| T1130-3eb96f8d | docs/dev/roadmap/v0.2-overview.md | 1127 | - [ ] T0495-4f75 T0177-b641 T0230-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:173) (docs/dev/roadmap/v0.2-overview.md:491) |
| T1131-39cfb9dc | docs/dev/roadmap/v0.2-overview.md | 1128 | - [ ] T0496-ce72 T0178-644e T0231-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:174) (docs/dev/roadmap/v0.2-overview.md:492) |
| T1132-2a08a746 | docs/dev/roadmap/v0.2-overview.md | 1129 | - [ ] T0497-1f67 T0179-60b4 T0232-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:175) (docs/dev/roadmap/v0.2-overview.md:493) |
| T1133-00beb98f | docs/dev/roadmap/v0.2-overview.md | 1130 | - [ ] T0498-e171 T0180-817f T0233-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:176) (docs/dev/roadmap/v0.2-overview.md:494) |
| T1134-83db0f94 | docs/dev/roadmap/v0.2-overview.md | 1131 | - [ ] T0499-2607 T0181-f016 T0234-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:177) (docs/dev/roadmap/v0.2-overview.md:495) |
| T1135-c3dac82f | docs/dev/roadmap/v0.2-overview.md | 1132 | - [ ] T0500-500a T0182-462f T0235-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:178) (docs/dev/roadmap/v0.2-overview.md:496) |
| T1136-5ecb3e85 | docs/dev/roadmap/v0.2-overview.md | 1133 | - [ ] T0501-fea3 T0183-b7c4 T0236-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:179) (docs/dev/roadmap/v0.2-overview.md:497) |
| T1137-8589a60d | docs/dev/roadmap/v0.2-overview.md | 1134 | - [ ] T0502-a459 T0184-e931 T0237-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:180) (docs/dev/roadmap/v0.2-overview.md:498) |
| T1138-bbcea7d1 | docs/dev/roadmap/v0.2-overview.md | 1135 | - [ ] T0503-da92 T0185-9d65 T0238-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:181) (docs/dev/roadmap/v0.2-overview.md:499) |
| T1139-d68ccd42 | docs/dev/roadmap/v0.2-overview.md | 1136 | - [ ] T0504-1a46 T0186-d08d T0239-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:182) (docs/dev/roadmap/v0.2-overview.md:500) |
| T1140-0f6d33fa | docs/dev/roadmap/v0.2-overview.md | 1137 | - [ ] T0505-168d T0187-1ae5 T0240-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:183) (docs/dev/roadmap/v0.2-overview.md:501) |
| T1141-4ef2637c | docs/dev/roadmap/v0.2-overview.md | 1138 | - [ ] T0506-7171 T0188-2593 T0241-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:184) (docs/dev/roadmap/v0.2-overview.md:502) |
| T1142-39cffeac | docs/dev/roadmap/v0.2-overview.md | 1139 | - [ ] T0507-48a1 T0189-0db8 T0242-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:185) (docs/dev/roadmap/v0.2-overview.md:503) |
| T1143-240a144e | docs/dev/roadmap/v0.2-overview.md | 1140 | - [ ] T0508-f03d T0190-21b4 T0243-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:186) (docs/dev/roadmap/v0.2-overview.md:504) |
| T1144-3bfd786b | docs/dev/roadmap/v0.2-overview.md | 1141 | - [ ] T0509-a301 T0191-6abe T0244-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:187) (docs/dev/roadmap/v0.2-overview.md:505) |
| T1145-134ef02b | docs/dev/roadmap/v0.2-overview.md | 1142 | - [ ] T0510-a1ef T0192-6cf6 T0245-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:188) (docs/dev/roadmap/v0.2-overview.md:506) |
| T1146-c3f2f17f | docs/dev/roadmap/v0.2-overview.md | 1143 | - [ ] T0511-0e38 T0193-402b T0246-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:189) (docs/dev/roadmap/v0.2-overview.md:507) |
| T1147-d188d4a9 | docs/dev/roadmap/v0.2-overview.md | 1144 | - [ ] T0512-ba77 T0194-9595 T0247-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.2-overview.md:190) (docs/dev/roadmap/v0.2-overview.md:508) |
| T1148-e9ca02f2 | docs/dev/roadmap/v0.2-overview.md | 1145 | - [ ] T0513-d0c7 T0195-dae5 T0248-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.2-overview.md:191) (docs/dev/roadmap/v0.2-overview.md:509) |
| T1149-497c02da | docs/dev/roadmap/v0.2-overview.md | 1146 | - [ ] T0514-fed2 T0196-e896 T0249-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.2-overview.md:192) (docs/dev/roadmap/v0.2-overview.md:510) |
| T1150-2bb63058 | docs/dev/roadmap/v0.2-overview.md | 1147 | - [ ] T0515-9043 T0197-1ee3 T0250-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.2-overview.md:193) (docs/dev/roadmap/v0.2-overview.md:511) |
| T1151-7e5fd441 | docs/dev/roadmap/v0.2-overview.md | 1148 | - [ ] T0516-a737 T0198-06e7 T0251-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.2-overview.md:194) (docs/dev/roadmap/v0.2-overview.md:512) |
| T1152-4be7399e | docs/dev/roadmap/v0.2-overview.md | 1149 | - [ ] T0517-ece6 T0199-513a T0252-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.2-overview.md:195) (docs/dev/roadmap/v0.2-overview.md:513) |
| T1153-824ce896 | docs/dev/roadmap/v0.2-overview.md | 1150 | - [ ] T0518-8e53 T0200-28c4 T0253-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.2-overview.md:196) (docs/dev/roadmap/v0.2-overview.md:514) |
| T1154-1fb6288e | docs/dev/roadmap/v0.2-overview.md | 1151 | - [ ] T0519-87ad T0201-42c3 T0254-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.2-overview.md:197) (docs/dev/roadmap/v0.2-overview.md:515) |
| T1155-853fa387 | docs/dev/roadmap/v0.2-overview.md | 1152 | - [ ] T0520-d866 T0202-bd4e T0255-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.2-overview.md:198) (docs/dev/roadmap/v0.2-overview.md:516) |
| T1156-99ef8ada | docs/dev/roadmap/v0.2-overview.md | 1153 | - [ ] T0521-4fed T0203-495f T0256-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.2-overview.md:199) (docs/dev/roadmap/v0.2-overview.md:517) |
| T1157-8c2fa606 | docs/dev/roadmap/v0.2-overview.md | 1154 | - [ ] T0522-e4a1 T0204-be79 T0257-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.2-overview.md:200) (docs/dev/roadmap/v0.2-overview.md:518) |
| T1158-440c5e71 | docs/dev/roadmap/v0.2-overview.md | 1155 | - [ ] T0523-e070 T0205-75ce T0258-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.2-overview.md:201) (docs/dev/roadmap/v0.2-overview.md:519) |
| T1159-cbcaaede | docs/dev/roadmap/v0.2-overview.md | 1156 | - [ ] T0524-ffc4 T0206-0fa4 T0259-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.2-overview.md:202) (docs/dev/roadmap/v0.2-overview.md:520) |
| T1160-35cf5927 | docs/dev/roadmap/v0.2-overview.md | 1157 | - [ ] T0525-b394 T0207-45f9 T0260-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.2-overview.md:203) (docs/dev/roadmap/v0.2-overview.md:521) |
| T1161-6123c9f4 | docs/dev/roadmap/v0.2-overview.md | 1158 | - [ ] T0526-d609 T0208-604a T0261-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.2-overview.md:204) (docs/dev/roadmap/v0.2-overview.md:522) |
| T1162-452adfdc | docs/dev/roadmap/v0.2-overview.md | 1159 | - [ ] T0527-b1cc T0209-8385 T0262-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.2-overview.md:205) (docs/dev/roadmap/v0.2-overview.md:523) |
| T1163-93619445 | docs/dev/roadmap/v0.2-overview.md | 1160 | - [ ] T0528-4e8c T0210-83e9 T0263-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.2-overview.md:206) (docs/dev/roadmap/v0.2-overview.md:524) |
| T1164-0c134a07 | docs/dev/roadmap/v0.2-overview.md | 1161 | - [ ] T0529-912f T0211-c2da T0264-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.2-overview.md:207) (docs/dev/roadmap/v0.2-overview.md:525) |
| T1165-f2cfc7c9 | docs/dev/roadmap/v0.2-overview.md | 1162 | - [ ] T0530-2530 T0212-e321 T0265-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.2-overview.md:208) (docs/dev/roadmap/v0.2-overview.md:526) |
| T1166-b0495b35 | docs/dev/roadmap/v0.2-overview.md | 1163 | - [ ] T0531-f9f3 T0213-90c2 T0266-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.2-overview.md:209) (docs/dev/roadmap/v0.2-overview.md:527) |
| T1167-da27294a | docs/dev/roadmap/v0.2-overview.md | 1164 | - [ ] T0532-2054 T0214-dbb7 T0267-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.2-overview.md:210) (docs/dev/roadmap/v0.2-overview.md:528) |
| T1168-d501e0a0 | docs/dev/roadmap/v0.2-overview.md | 1165 | - [ ] T0533-ba4d T0215-45f9 T0268-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.2-overview.md:211) (docs/dev/roadmap/v0.2-overview.md:529) |
| T1169-6d5ec7ef | docs/dev/roadmap/v0.2-overview.md | 1166 | - [ ] T0534-ef90 T0216-c57b T0269-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.2-overview.md:212) (docs/dev/roadmap/v0.2-overview.md:530) |
| T1170-c287c3f5 | docs/dev/roadmap/v0.2-overview.md | 1167 | - [ ] T0535-0cda T0217-24e1 T0270-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.2-overview.md:213) (docs/dev/roadmap/v0.2-overview.md:531) |
| T1171-f5cdb989 | docs/dev/roadmap/v0.2-overview.md | 1168 | - [ ] T0536-0157 T0218-68cf T0271-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.2-overview.md:214) (docs/dev/roadmap/v0.2-overview.md:532) |
| T1172-01b00d87 | docs/dev/roadmap/v0.2-overview.md | 1169 | - [ ] T0537-f8e7 T0219-45ed T0272-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.2-overview.md:215) (docs/dev/roadmap/v0.2-overview.md:533) |
| T1173-152ed8e7 | docs/dev/roadmap/v0.2-overview.md | 1170 | - [ ] T0538-4ce2 T0220-6c4d T0273-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.2-overview.md:216) (docs/dev/roadmap/v0.2-overview.md:534) |
| T1174-739671fa | docs/dev/roadmap/v0.2-overview.md | 1171 | - [ ] T0539-0d80 T0221-d81b T0274-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.2-overview.md:217) (docs/dev/roadmap/v0.2-overview.md:535) |
| T1175-b4dfbcfe | docs/dev/roadmap/v0.2-overview.md | 1172 | - [ ] T0540-9b29 T0222-1afc T0275-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.2-overview.md:218) (docs/dev/roadmap/v0.2-overview.md:536) |
| T1176-6694e34f | docs/dev/roadmap/v0.2-overview.md | 1173 | - [ ] T0541-cff0 T0223-cc17 T0276-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.2-overview.md:219) (docs/dev/roadmap/v0.2-overview.md:537) |
| T1177-54a724f9 | docs/dev/roadmap/v0.2-overview.md | 1174 | - [ ] T0542-0d28 T0224-ffd8 T0277-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.2-overview.md:220) (docs/dev/roadmap/v0.2-overview.md:538) |
| T1178-125d54fc | docs/dev/roadmap/v0.2-overview.md | 1175 | - [ ] T0543-a8f5 T0225-1977 T0278-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.2-overview.md:221) (docs/dev/roadmap/v0.2-overview.md:539) |
| T1179-09f7c248 | docs/dev/roadmap/v0.2-overview.md | 1176 | - [ ] T0544-3636 T0226-8f55 T0279-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.2-overview.md:222) (docs/dev/roadmap/v0.2-overview.md:540) |
| T1180-8902bc4b | docs/dev/roadmap/v0.2-overview.md | 1177 | - [ ] T0545-9c68 T0227-1fb4 T0280-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.2-overview.md:223) (docs/dev/roadmap/v0.2-overview.md:541) |
| T1181-208fb805 | docs/dev/roadmap/v0.2-overview.md | 1178 | - [ ] T0546-53fd T0228-f631 T0281-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.2-overview.md:224) (docs/dev/roadmap/v0.2-overview.md:542) |
| T1182-a08821b0 | docs/dev/roadmap/v0.2-overview.md | 1179 | - [ ] T0547-3ada T0229-5b09 T0282-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.2-overview.md:225) (docs/dev/roadmap/v0.2-overview.md:543) |
| T1183-682a8b49 | docs/dev/roadmap/v0.2-overview.md | 1180 | - [ ] T0548-3cdd T0230-0992 T0283-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.2-overview.md:226) (docs/dev/roadmap/v0.2-overview.md:544) |
| T1184-97f0475e | docs/dev/roadmap/v0.2-overview.md | 1181 | - [ ] T0549-add0 T0231-2147 T0284-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.2-overview.md:227) (docs/dev/roadmap/v0.2-overview.md:545) |
| T1185-b3ad1d8d | docs/dev/roadmap/v0.2-overview.md | 1182 | - [ ] T0550-428b T0232-2c69 T0285-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.2-overview.md:228) (docs/dev/roadmap/v0.2-overview.md:546) |
| T1186-acdc0ae9 | docs/dev/roadmap/v0.2-overview.md | 1183 | - [ ] T0551-7b12 T0233-f8fe T0286-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.2-overview.md:229) (docs/dev/roadmap/v0.2-overview.md:547) |
| T1187-a1cd86ea | docs/dev/roadmap/v0.2-overview.md | 1184 | - [ ] T0552-a1d1 T0234-c938 T0287-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.2-overview.md:230) (docs/dev/roadmap/v0.2-overview.md:548) |
| T1188-d3e02344 | docs/dev/roadmap/v0.2-overview.md | 1185 | - [ ] T0553-7697 T0235-6a56 T0288-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.2-overview.md:231) (docs/dev/roadmap/v0.2-overview.md:549) |
| T1189-e7912a98 | docs/dev/roadmap/v0.2-overview.md | 1186 | - [ ] T0554-4333 T0236-b0d4 T0289-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.2-overview.md:232) (docs/dev/roadmap/v0.2-overview.md:550) |
| T1190-0c9c3078 | docs/dev/roadmap/v0.2-overview.md | 1187 | - [ ] T0555-aef3 T0237-7052 T0290-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.2-overview.md:233) (docs/dev/roadmap/v0.2-overview.md:551) |
| T1191-1b61697b | docs/dev/roadmap/v0.2-overview.md | 1188 | - [ ] T0556-39b5 T0238-fa2f T0291-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.2-overview.md:234) (docs/dev/roadmap/v0.2-overview.md:552) |
| T1192-adeacfe7 | docs/dev/roadmap/v0.2-overview.md | 1189 | - [ ] T0557-ebd7 T0239-3b7d T0292-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.2-overview.md:235) (docs/dev/roadmap/v0.2-overview.md:553) |
| T1193-1d690f91 | docs/dev/roadmap/v0.2-overview.md | 1190 | - [ ] T0558-f101 T0240-d830 T0294-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.2-overview.md:236) (docs/dev/roadmap/v0.2-overview.md:554) |
| T1194-fe62aee2 | docs/dev/roadmap/v0.2-overview.md | 1191 | - [ ] T0559-e4da T0241-c27f T0295-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.2-overview.md:237) (docs/dev/roadmap/v0.2-overview.md:555) |
| T1195-682746c2 | docs/dev/roadmap/v0.2-overview.md | 1192 | - [ ] T0560-6aea T0242-9665 T0296-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.2-overview.md:238) (docs/dev/roadmap/v0.2-overview.md:556) |
| T1196-4d6539e2 | docs/dev/roadmap/v0.2-overview.md | 1193 | - [ ] T0561-26ea T0243-9fbd T0297-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.2-overview.md:239) (docs/dev/roadmap/v0.2-overview.md:557) |
| T1197-f8b4809a | docs/dev/roadmap/v0.2-overview.md | 1194 | - [ ] T0562-02fa T0244-40aa T0298-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.2-overview.md:240) (docs/dev/roadmap/v0.2-overview.md:558) |
| T1198-379b4cac | docs/dev/roadmap/v0.2-overview.md | 1195 | - [ ] T0563-7eec T0245-6f20 T0299-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.2-overview.md:241) (docs/dev/roadmap/v0.2-overview.md:559) |
| T1199-56d00aa8 | docs/dev/roadmap/v0.2-overview.md | 1196 | - [ ] T0564-3b0e T0246-a197 T0300-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.2-overview.md:242) (docs/dev/roadmap/v0.2-overview.md:560) |
| T1200-bfd22476 | docs/dev/roadmap/v0.2-overview.md | 1197 | - [ ] T0565-f1c0 T0247-096c T0301-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.2-overview.md:243) (docs/dev/roadmap/v0.2-overview.md:561) |
| T1201-979da547 | docs/dev/roadmap/v0.2-overview.md | 1198 | - [ ] T0566-f2f8 T0248-fd6c T0302-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:244) (docs/dev/roadmap/v0.2-overview.md:562) |
| T1202-8177cd6d | docs/dev/roadmap/v0.2-overview.md | 1199 | - [ ] T0567-0f91 T0249-6364 T0303-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:245) (docs/dev/roadmap/v0.2-overview.md:563) |
| T1203-89174987 | docs/dev/roadmap/v0.2-overview.md | 1200 | - [ ] T0568-7b04 T0250-07e7 T0304-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:246) (docs/dev/roadmap/v0.2-overview.md:564) |
| T1204-e4d91124 | docs/dev/roadmap/v0.2-overview.md | 1201 | - [ ] T0569-5aa8 T0251-6d34 T0305-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:247) (docs/dev/roadmap/v0.2-overview.md:565) |
| T1205-be7ebf25 | docs/dev/roadmap/v0.2-overview.md | 1202 | - [ ] T0570-77c2 T0252-df35 T0306-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:248) (docs/dev/roadmap/v0.2-overview.md:566) |
| T1206-3dead931 | docs/dev/roadmap/v0.2-overview.md | 1203 | - [ ] T0571-cb78 T0253-d812 T0307-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:249) (docs/dev/roadmap/v0.2-overview.md:567) |
| T1207-ca42eaf4 | docs/dev/roadmap/v0.2-overview.md | 1204 | - [ ] T0572-05ac T0254-6215 T0308-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:250) (docs/dev/roadmap/v0.2-overview.md:568) |
| T1208-e85d9f96 | docs/dev/roadmap/v0.2-overview.md | 1205 | - [ ] T0573-13a7 T0255-38eb T0309-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:251) (docs/dev/roadmap/v0.2-overview.md:569) |
| T1209-e18fca2d | docs/dev/roadmap/v0.2-overview.md | 1206 | - [ ] T0574-5038 T0256-7713 T0310-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:252) (docs/dev/roadmap/v0.2-overview.md:570) |
| T1210-0bef0cdd | docs/dev/roadmap/v0.2-overview.md | 1207 | - [ ] T0575-8178 T0257-698e T0311-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:253) (docs/dev/roadmap/v0.2-overview.md:571) |
| T1211-c0a81041 | docs/dev/roadmap/v0.2-overview.md | 1208 | - [ ] T0576-1f21 T0258-6de5 T0312-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:254) (docs/dev/roadmap/v0.2-overview.md:572) |
| T1212-2613a002 | docs/dev/roadmap/v0.2-overview.md | 1209 | - [ ] T0577-1df0 T0259-8bd2 T0313-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:255) (docs/dev/roadmap/v0.2-overview.md:573) |
| T1213-2610a655 | docs/dev/roadmap/v0.2-overview.md | 1210 | - [ ] T0578-d48c T0260-111d T0314-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:256) (docs/dev/roadmap/v0.2-overview.md:574) |
| T1214-44400e7e | docs/dev/roadmap/v0.2-overview.md | 1211 | - [ ] T0579-2a0d T0261-bb0f T0315-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:257) (docs/dev/roadmap/v0.2-overview.md:575) |
| T1215-fa7513fa | docs/dev/roadmap/v0.2-overview.md | 1212 | - [ ] T0580-2df3 T0262-a94d T0316-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:258) (docs/dev/roadmap/v0.2-overview.md:576) |
| T1216-c7df0eca | docs/dev/roadmap/v0.2-overview.md | 1213 | - [ ] T0581-b2bb T0263-2ede T0317-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:259) (docs/dev/roadmap/v0.2-overview.md:577) |
| T1217-74d54e0e | docs/dev/roadmap/v0.2-overview.md | 1214 | - [ ] T0582-0a0f T0264-d22a T0318-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:260) (docs/dev/roadmap/v0.2-overview.md:578) |
| T1218-9bdd1ccd | docs/dev/roadmap/v0.2-overview.md | 1215 | - [ ] T0583-2340 T0265-7d1a T0319-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:261) (docs/dev/roadmap/v0.2-overview.md:579) |
| T1219-0e0b9555 | docs/dev/roadmap/v0.2-overview.md | 1216 | - [ ] T0584-4cad T0266-c7ab T0320-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:262) (docs/dev/roadmap/v0.2-overview.md:580) |
| T1220-5733d4aa | docs/dev/roadmap/v0.2-overview.md | 1217 | - [ ] T0585-45cb T0267-0cf5 T0321-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:263) (docs/dev/roadmap/v0.2-overview.md:581) |
| T1221-b39d1135 | docs/dev/roadmap/v0.2-overview.md | 1218 | - [ ] T0586-0a76 T0268-8bdd T0322-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:264) (docs/dev/roadmap/v0.2-overview.md:582) |
| T1222-78e1f581 | docs/dev/roadmap/v0.2-overview.md | 1219 | - [ ] T0587-9e75 T0269-09d0 T0323-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:265) (docs/dev/roadmap/v0.2-overview.md:583) |
| T1223-dc9e298c | docs/dev/roadmap/v0.2-overview.md | 1220 | - [ ] T0588-c0bf T0270-0a32 T0324-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:266) (docs/dev/roadmap/v0.2-overview.md:584) |
| T1224-d2728e89 | docs/dev/roadmap/v0.2-overview.md | 1221 | - [ ] T0589-e9ba T0271-4601 T0325-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:267) (docs/dev/roadmap/v0.2-overview.md:585) |
| T1225-01c872e1 | docs/dev/roadmap/v0.2-overview.md | 1222 | - [ ] T0590-495d T0272-547e T0326-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:268) (docs/dev/roadmap/v0.2-overview.md:586) |
| T1226-a91bb784 | docs/dev/roadmap/v0.2-overview.md | 1223 | - [ ] T0591-b336 T0273-4c9f T0327-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:269) (docs/dev/roadmap/v0.2-overview.md:587) |
| T1227-39bcf9b6 | docs/dev/roadmap/v0.2-overview.md | 1224 | - [ ] T0592-bdcc T0274-2185 T0328-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:270) (docs/dev/roadmap/v0.2-overview.md:588) |
| T1228-9f782ebe | docs/dev/roadmap/v0.2-overview.md | 1225 | - [ ] T0593-a8fc T0275-8ba6 T0329-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:271) (docs/dev/roadmap/v0.2-overview.md:589) |
| T1229-0c8c244e | docs/dev/roadmap/v0.2-overview.md | 1226 | - [ ] T0594-c96b T0276-0886 T0330-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:272) (docs/dev/roadmap/v0.2-overview.md:590) |
| T1230-13fc27a7 | docs/dev/roadmap/v0.2-overview.md | 1227 | - [ ] T0595-5d58 T0277-9b3c T0331-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:273) (docs/dev/roadmap/v0.2-overview.md:591) |
| T1231-5c6098a0 | docs/dev/roadmap/v0.2-overview.md | 1228 | - [ ] T0596-a282 T0278-8770 T0332-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:274) (docs/dev/roadmap/v0.2-overview.md:592) |
| T1232-cec87f77 | docs/dev/roadmap/v0.2-overview.md | 1229 | - [ ] T0597-d285 T0279-65a3 T0333-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:275) (docs/dev/roadmap/v0.2-overview.md:593) |
| T1233-25b2fd1f | docs/dev/roadmap/v0.2-overview.md | 1230 | - [ ] T0598-5354 T0280-59b1 T0334-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:276) (docs/dev/roadmap/v0.2-overview.md:594) |
| T1234-fb81a0cc | docs/dev/roadmap/v0.2-overview.md | 1231 | - [ ] T0599-37c2 T0281-404e T0335-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:277) (docs/dev/roadmap/v0.2-overview.md:595) |
| T1235-3d63839c | docs/dev/roadmap/v0.2-overview.md | 1232 | - [ ] T0600-e3cf T0282-faf0 T0336-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:278) (docs/dev/roadmap/v0.2-overview.md:596) |
| T1236-25660920 | docs/dev/roadmap/v0.2-overview.md | 1233 | - [ ] T0601-95b0 T0283-87f9 T0337-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:279) (docs/dev/roadmap/v0.2-overview.md:597) |
| T1237-8a0206a4 | docs/dev/roadmap/v0.2-overview.md | 1234 | - [ ] T0602-d274 T0284-1140 T0338-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:280) (docs/dev/roadmap/v0.2-overview.md:598) |
| T1238-eafe99a4 | docs/dev/roadmap/v0.2-overview.md | 1235 | - [ ] T0603-3dea T0285-d98b T0339-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:281) (docs/dev/roadmap/v0.2-overview.md:599) |
| T1239-63701fad | docs/dev/roadmap/v0.2-overview.md | 1236 | - [ ] T0604-696d T0286-016a T0340-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:282) (docs/dev/roadmap/v0.2-overview.md:600) |
| T1240-ec768145 | docs/dev/roadmap/v0.2-overview.md | 1237 | - [ ] T0605-2e3f T0287-db81 T0341-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:283) (docs/dev/roadmap/v0.2-overview.md:601) |
| T1241-9c8be3c6 | docs/dev/roadmap/v0.2-overview.md | 1238 | - [ ] T0606-4e7b T0288-2f06 T0342-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:284) (docs/dev/roadmap/v0.2-overview.md:602) |
| T1242-351a7704 | docs/dev/roadmap/v0.2-overview.md | 1239 | - [ ] T0607-1c9e T0289-665f T0343-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:285) (docs/dev/roadmap/v0.2-overview.md:603) |
| T1243-3cba92bf | docs/dev/roadmap/v0.2-overview.md | 1240 | - [ ] T0608-629c T0290-cae7 T0344-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:286) (docs/dev/roadmap/v0.2-overview.md:604) |
| T1244-cdef26c5 | docs/dev/roadmap/v0.2-overview.md | 1241 | - [ ] T0609-05f7 T0291-77df T0345-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:287) (docs/dev/roadmap/v0.2-overview.md:605) |
| T1245-15289ac5 | docs/dev/roadmap/v0.2-overview.md | 1242 | - [ ] T0610-879a T0292-effb T0346-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:288) (docs/dev/roadmap/v0.2-overview.md:606) |
| T1246-bce29542 | docs/dev/roadmap/v0.2-overview.md | 1243 | - [ ] T0611-25f7 T0293-5185 T0347-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:289) (docs/dev/roadmap/v0.2-overview.md:607) |
| T1247-63e560fb | docs/dev/roadmap/v0.2-overview.md | 1244 | - [ ] T0612-6112 T0294-db1c T0348-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:290) (docs/dev/roadmap/v0.2-overview.md:608) |
| T1248-98e30808 | docs/dev/roadmap/v0.2-overview.md | 1245 | - [ ] T0613-b6fd T0295-a73a T0349-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:291) (docs/dev/roadmap/v0.2-overview.md:609) |
| T1249-635359e2 | docs/dev/roadmap/v0.2-overview.md | 1246 | - [ ] T0614-e2cf T0296-6ded T0350-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:292) (docs/dev/roadmap/v0.2-overview.md:610) |
| T1250-618948fb | docs/dev/roadmap/v0.2-overview.md | 1247 | - [ ] T0615-41c4 T0297-c86b T0352-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:293) (docs/dev/roadmap/v0.2-overview.md:611) |
| T1251-49a24861 | docs/dev/roadmap/v0.2-overview.md | 1248 | - [ ] T0616-5759 T0298-5be9 T0353-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:294) (docs/dev/roadmap/v0.2-overview.md:612) |
| T1252-eb45b531 | docs/dev/roadmap/v0.2-overview.md | 1249 | - [ ] T0617-391e T0299-5adc T0354-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:295) (docs/dev/roadmap/v0.2-overview.md:613) |
| T1253-7f218f78 | docs/dev/roadmap/v0.2-overview.md | 1250 | - [ ] T0618-8620 T0300-ceff T0355-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:296) (docs/dev/roadmap/v0.2-overview.md:614) |
| T1254-c06c50e6 | docs/dev/roadmap/v0.2-overview.md | 1251 | - [ ] T0619-ed18 T0301-0486 T0356-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:297) (docs/dev/roadmap/v0.2-overview.md:615) |
| T1255-c89d8de6 | docs/dev/roadmap/v0.2-overview.md | 1252 | - [ ] T0620-5360 T0302-ea26 T0357-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:298) (docs/dev/roadmap/v0.2-overview.md:616) |
| T1256-c76ad943 | docs/dev/roadmap/v0.2-overview.md | 1253 | - [ ] T0621-1a4d T0303-004d T0358-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:299) (docs/dev/roadmap/v0.2-overview.md:617) |
| T1257-6c5cff2f | docs/dev/roadmap/v0.2-overview.md | 1254 | - [ ] T0622-dcef T0304-0dc1 T0359-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:300) (docs/dev/roadmap/v0.2-overview.md:618) |
| T1258-7a512641 | docs/dev/roadmap/v0.2-overview.md | 1255 | - [ ] T0623-2a43 T0305-adc8 T0360-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:301) (docs/dev/roadmap/v0.2-overview.md:619) |
| T1259-814596ae | docs/dev/roadmap/v0.2-overview.md | 1256 | - [ ] T0624-71fc T0306-48eb T0361-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:302) (docs/dev/roadmap/v0.2-overview.md:620) |
| T1260-9d29d66e | docs/dev/roadmap/v0.2-overview.md | 1257 | - [ ] T0625-0cd0 T0307-5ed6 T0362-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:303) (docs/dev/roadmap/v0.2-overview.md:621) |
| T1261-206ec70d | docs/dev/roadmap/v0.2-overview.md | 1258 | - [ ] T0626-fb6c T0308-d86f T0363-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:304) (docs/dev/roadmap/v0.2-overview.md:622) |
| T1262-0a56cdb3 | docs/dev/roadmap/v0.2-overview.md | 1259 | - [ ] T0627-f25c T0309-8393 T0364-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:305) (docs/dev/roadmap/v0.2-overview.md:623) |
| T1263-a006c5ee | docs/dev/roadmap/v0.2-overview.md | 1260 | - [ ] T0628-2f6a T0310-8d04 T0365-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:306) (docs/dev/roadmap/v0.2-overview.md:624) |
| T1264-6a0807c9 | docs/dev/roadmap/v0.2-overview.md | 1261 | - [ ] T0629-e4bd T0311-a424 T0366-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:307) (docs/dev/roadmap/v0.2-overview.md:625) |
| T1265-cbbdd4f7 | docs/dev/roadmap/v0.2-overview.md | 1262 | - [ ] T0630-3a38 T0312-9cfd T0367-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:308) (docs/dev/roadmap/v0.2-overview.md:626) |
| T1266-a1ccf1bc | docs/dev/roadmap/v0.2-overview.md | 1263 | - [ ] T0631-7afe T0313-41b0 T0368-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:309) (docs/dev/roadmap/v0.2-overview.md:627) |
| T1267-309fd61d | docs/dev/roadmap/v0.2-overview.md | 1264 | - [ ] T0632-95d6 T0314-0b12 T0369-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:310) (docs/dev/roadmap/v0.2-overview.md:628) |
| T1268-6baef585 | docs/dev/roadmap/v0.2-overview.md | 1265 | - [ ] T0633-0504 T0315-640a T0370-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:311) (docs/dev/roadmap/v0.2-overview.md:629) |
| T1269-8f92155e | docs/dev/roadmap/v0.2-overview.md | 1266 | - [ ] T0634-4c2e T0316-1516 T0371-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:312) (docs/dev/roadmap/v0.2-overview.md:630) |
| T1270-fd6a379b | docs/dev/roadmap/v0.2-overview.md | 1267 | - [ ] T0635-8571 T0317-9ec6 T0372-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:313) (docs/dev/roadmap/v0.2-overview.md:631) |
| T1271-b7dd15a3 | docs/dev/roadmap/v0.2-overview.md | 1268 | - [ ] T0636-50a5 T0318-a391 T0373-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:314) (docs/dev/roadmap/v0.2-overview.md:632) |
| T1272-eeaf3b80 | docs/dev/roadmap/v0.2-overview.md | 1269 | - [ ] T0637-f3b3 T0319-991c T0374-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:315) (docs/dev/roadmap/v0.2-overview.md:633) |
| T1273-f8228c12 | docs/dev/roadmap/v0.2-overview.md | 1270 | - [ ] T0638-852b T0320-5b39 T0375-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.2-overview.md:316) (docs/dev/roadmap/v0.2-overview.md:634) |
| T1274-cf808178 | docs/dev/roadmap/v0.2-overview.md | 1271 | - [ ] T0639-c457 T0321-4526 T0376-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.2-overview.md:317) (docs/dev/roadmap/v0.2-overview.md:635) |
| T1275-a1e05c3f | docs/dev/roadmap/v0.2-overview.md | 1272 | - [ ] T0640-04a6 T0322-39ab T0377-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:318) (docs/dev/roadmap/v0.2-overview.md:636) |
| T1276-331ddc27 | docs/dev/roadmap/v0.2-overview.md | 1273 | - [ ] T0641-39e8 T0323-0b47 T0378-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:319) (docs/dev/roadmap/v0.2-overview.md:637) |
| T1277-343ff72b | docs/dev/roadmap/v0.2-overview.md | 1274 | - [ ] T0642-06e0 T0324-4cb0 T0379-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:320) (docs/dev/roadmap/v0.2-overview.md:638) |
| T1278-62024e55 | docs/dev/roadmap/v0.2-overview.md | 1275 | - [ ] T0643-7a79 T0325-9818 T0380-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:321) (docs/dev/roadmap/v0.2-overview.md:639) |
| T1279-983c5afb | docs/dev/roadmap/v0.2-overview.md | 1276 | - [ ] T0644-92c0 T0326-e1ad T0381-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:322) (docs/dev/roadmap/v0.2-overview.md:640) |
| T1280-29a40709 | docs/dev/roadmap/v0.2-overview.md | 1277 | - [ ] T0645-12e9 T0327-9936 T0382-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:323) (docs/dev/roadmap/v0.2-overview.md:641) |
| T1281-66c5b8af | docs/dev/roadmap/v0.2-overview.md | 1278 | - [ ] T0646-f373 T0328-e569 T0383-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:324) (docs/dev/roadmap/v0.2-overview.md:642) |
| T1282-9f6f17b6 | docs/dev/roadmap/v0.2-overview.md | 1279 | - [ ] T0647-0fc0 T0329-58a8 T0384-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:325) (docs/dev/roadmap/v0.2-overview.md:643) |
| T1283-5db756b0 | docs/dev/roadmap/v0.2-overview.md | 1280 | - [ ] T0648-3520 T0330-dfa0 T0385-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:326) (docs/dev/roadmap/v0.2-overview.md:644) |
| T1284-46240246 | docs/dev/roadmap/v0.2-overview.md | 1281 | - [ ] T0649-d70a T0331-5799 T0386-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.2-overview.md:327) (docs/dev/roadmap/v0.2-overview.md:645) |
| T1285-e4fcc65f | docs/dev/roadmap/v0.2-overview.md | 1282 | - [ ] T0650-7cc0 T0332-4485 T0387-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.2-overview.md:328) (docs/dev/roadmap/v0.2-overview.md:646) |
| T1286-11069512 | docs/dev/roadmap/v0.2-overview.md | 1283 | - [ ] T0651-f63c T0333-d0f6 T0388-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.2-overview.md:329) (docs/dev/roadmap/v0.2-overview.md:647) |
| T1287-046692e0 | docs/dev/roadmap/v0.2-overview.md | 1284 | - [ ] T0652-6ab8 T0334-ff96 T0389-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.2-overview.md:330) (docs/dev/roadmap/v0.2-overview.md:648) |
| T1288-0edaa2d7 | docs/dev/roadmap/v0.2-overview.md | 1285 | - [ ] T0653-3826 T0335-9703 T0390-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.2-overview.md:331) (docs/dev/roadmap/v0.2-overview.md:649) |
| T1289-59d5e203 | docs/dev/roadmap/v0.2-overview.md | 1286 | - [ ] T0654-ff35 T0336-209c T0391-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.2-overview.md:332) (docs/dev/roadmap/v0.2-overview.md:650) |
| T1290-dd9c4363 | docs/dev/roadmap/v0.2-overview.md | 1287 | - [ ] T0655-b47f T0337-31ca T0392-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.2-overview.md:333) (docs/dev/roadmap/v0.2-overview.md:651) |
| T1291-92f8d147 | docs/dev/roadmap/v0.2-overview.md | 1288 | - [ ] T0656-a285 T0338-abf1 T0393-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.2-overview.md:334) (docs/dev/roadmap/v0.2-overview.md:652) |
| T1292-a2b97d60 | docs/dev/roadmap/v0.2-overview.md | 1289 | - [ ] T0657-e8ad T0339-a36a T0394-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.2-overview.md:335) (docs/dev/roadmap/v0.2-overview.md:653) |
| T1293-43359558 | docs/dev/roadmap/v0.2-overview.md | 1290 | - [ ] T0658-c734 T0340-bb3f T0395-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.2-overview.md:336) (docs/dev/roadmap/v0.2-overview.md:654) |
| T1294-244dfdb5 | docs/dev/roadmap/v0.2-overview.md | 1291 | - [ ] T0659-3286 T0341-708f T0396-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.2-overview.md:337) (docs/dev/roadmap/v0.2-overview.md:655) |
| T1295-d316c8e4 | docs/dev/roadmap/v0.2-overview.md | 1292 | - [ ] T0660-0afb T0342-2e90 T0397-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.2-overview.md:338) (docs/dev/roadmap/v0.2-overview.md:656) |
| T1296-68ff4a7f | docs/dev/roadmap/v0.2-overview.md | 1293 | - [ ] T0661-68b3 T0343-83f7 T0398-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.2-overview.md:339) (docs/dev/roadmap/v0.2-overview.md:657) |
| T1297-0cb11e01 | docs/dev/roadmap/v0.2-overview.md | 1294 | - [ ] T0662-aa6d T0344-0793 T0399-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.2-overview.md:340) (docs/dev/roadmap/v0.2-overview.md:658) |
| T1298-2c2233df | docs/dev/roadmap/v0.2-overview.md | 1295 | - [ ] T0663-2657 T0345-5dd2 T0400-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.2-overview.md:341) (docs/dev/roadmap/v0.2-overview.md:659) |
| T1299-7e3a5665 | docs/dev/roadmap/v0.2-overview.md | 1296 | - [ ] T0664-2496 T0346-9ce8 T0401-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.2-overview.md:342) (docs/dev/roadmap/v0.2-overview.md:660) |
| T1300-6a5d5451 | docs/dev/roadmap/v0.2-overview.md | 1297 | - [ ] T0665-acb7 T0347-957c T0402-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.2-overview.md:343) (docs/dev/roadmap/v0.2-overview.md:661) |
| T1301-e27ff68e | docs/dev/roadmap/v0.2-overview.md | 1298 | - [ ] T0666-bd15 T0348-d289 T0403-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.2-overview.md:344) (docs/dev/roadmap/v0.2-overview.md:662) |
| T1302-5aec82fc | docs/dev/roadmap/v0.2-overview.md | 1299 | - [ ] T0667-8d32 T0349-36b6 T0404-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.2-overview.md:345) (docs/dev/roadmap/v0.2-overview.md:663) |
| T1303-7d7d223a | docs/dev/roadmap/v0.2-overview.md | 1300 | - [ ] T0668-d3cd T0350-2797 T0405-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.2-overview.md:346) (docs/dev/roadmap/v0.2-overview.md:664) |
| T1304-6cf50ca5 | docs/dev/roadmap/v0.2-overview.md | 1301 | - [ ] T0669-9765 T0351-00bb T0406-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.2-overview.md:347) (docs/dev/roadmap/v0.2-overview.md:665) |
| T1305-bb36d1e5 | docs/dev/roadmap/v0.2-overview.md | 1302 | - [ ] T0670-8df3 T0352-f33d T0407-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.2-overview.md:348) (docs/dev/roadmap/v0.2-overview.md:666) |
| T1306-48a8d054 | docs/dev/roadmap/v0.2-overview.md | 1303 | - [ ] T0671-6099 T0353-fa4f T0408-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.2-overview.md:349) (docs/dev/roadmap/v0.2-overview.md:667) |
| T1307-cad00cb6 | docs/dev/roadmap/v0.2-overview.md | 1304 | - [ ] T0672-8bb9 T0354-eb32 T0409-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.2-overview.md:350) (docs/dev/roadmap/v0.2-overview.md:668) |
| T1308-78438fe6 | docs/dev/roadmap/v0.2-overview.md | 1305 | - [ ] T0673-ac5a T0355-df06 T0410-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.2-overview.md:351) (docs/dev/roadmap/v0.2-overview.md:669) |
| T1309-de0a3a5d | docs/dev/roadmap/v0.2-overview.md | 1306 | - [ ] T0674-84eb T0356-e364 T0411-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.2-overview.md:352) (docs/dev/roadmap/v0.2-overview.md:670) |
| T1310-3face1b8 | docs/dev/roadmap/v0.2-overview.md | 1307 | - [ ] T0675-ca90 T0357-d372 T0412-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.2-overview.md:353) (docs/dev/roadmap/v0.2-overview.md:671) |
| T1311-f4cfacd9 | docs/dev/roadmap/v0.2-overview.md | 1308 | - [ ] T0676-ab0e T0358-411f T0413-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.2-overview.md:354) (docs/dev/roadmap/v0.2-overview.md:672) |
| T1312-bd31be88 | docs/dev/roadmap/v0.2-overview.md | 1309 | - [ ] T0677-6047 T0359-609d T0414-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.2-overview.md:355) (docs/dev/roadmap/v0.2-overview.md:673) |
| T1313-f9d08111 | docs/dev/roadmap/v0.2-overview.md | 1310 | - [ ] T0678-0d98 T0360-a163 T0415-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.2-overview.md:356) (docs/dev/roadmap/v0.2-overview.md:674) |
| T1314-77969b0a | docs/dev/roadmap/v0.2-overview.md | 1311 | - [ ] T0679-9a3a T0361-e3f7 T0416-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.2-overview.md:357) (docs/dev/roadmap/v0.2-overview.md:675) |
| T1315-0f361cfa | docs/dev/roadmap/v0.2-overview.md | 1312 | - [ ] T0680-8bb5 T0362-0fc9 T0417-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.2-overview.md:358) (docs/dev/roadmap/v0.2-overview.md:676) |
| T1316-fdbcf49f | docs/dev/roadmap/v0.2-overview.md | 1313 | - [ ] T0681-c099 T0363-7e62 T0418-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.2-overview.md:359) (docs/dev/roadmap/v0.2-overview.md:677) |
| T1317-a777fbd9 | docs/dev/roadmap/v0.2-overview.md | 1314 | - [ ] T0682-36b8 T0364-c662 T0419-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.2-overview.md:360) (docs/dev/roadmap/v0.2-overview.md:678) |
| T1318-d4eac08f | docs/dev/roadmap/v0.2-overview.md | 1315 | - [ ] T0683-9db6 T0365-c8a1 T0420-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.2-overview.md:361) (docs/dev/roadmap/v0.2-overview.md:679) |
| T1319-9970a1db | docs/dev/roadmap/v0.2-overview.md | 1316 | - [ ] T0684-0f1e T0366-fb89 T0421-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.2-overview.md:362) (docs/dev/roadmap/v0.2-overview.md:680) |
| T1320-a01d5745 | docs/dev/roadmap/v0.2-overview.md | 1317 | - [ ] T0685-03d0 T0367-f414 T0422-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.2-overview.md:363) (docs/dev/roadmap/v0.2-overview.md:681) |
| T1321-0b044a6b | docs/dev/roadmap/v0.2-overview.md | 1318 | - [ ] T0686-3297 T0368-c9f9 T0423-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.2-overview.md:364) (docs/dev/roadmap/v0.2-overview.md:682) |
| T1322-ba3ca378 | docs/dev/roadmap/v0.2-overview.md | 1319 | - [ ] T0687-fa42 T0369-b47d T0424-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.2-overview.md:365) (docs/dev/roadmap/v0.2-overview.md:683) |
| T1323-f81487f1 | docs/dev/roadmap/v0.2-overview.md | 1320 | - [ ] T0688-fddd T0370-8b59 T0425-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.2-overview.md:366) (docs/dev/roadmap/v0.2-overview.md:684) |
| T1324-59c29dfb | docs/dev/roadmap/v0.2-overview.md | 1321 | - [ ] T0689-fa1d T0371-c576 T0426-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.2-overview.md:367) (docs/dev/roadmap/v0.2-overview.md:685) |
| T1325-f80eb9d9 | docs/dev/roadmap/v0.2-overview.md | 1322 | - [ ] T0690-32f5 T0372-25d0 T0427-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.2-overview.md:368) (docs/dev/roadmap/v0.2-overview.md:686) |
| T1326-faca350c | docs/dev/roadmap/v0.2-overview.md | 1323 | - [ ] T0691-b18d T0373-ee91 T0428-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.2-overview.md:369) (docs/dev/roadmap/v0.2-overview.md:687) |
| T1327-1df22600 | docs/dev/roadmap/v0.2-overview.md | 1324 | - [ ] T0692-d763 T0374-48e9 T0429-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.2-overview.md:370) (docs/dev/roadmap/v0.2-overview.md:688) |
| T1328-f0345cbc | docs/dev/roadmap/v0.2-overview.md | 1325 | - [ ] T0693-73bb T0375-bc2b T0430-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.2-overview.md:371) (docs/dev/roadmap/v0.2-overview.md:689) |
| T1329-831bb9cb | docs/dev/roadmap/v0.2-overview.md | 1326 | - [ ] T0694-17d2 T0376-1026 T0431-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.2-overview.md:372) (docs/dev/roadmap/v0.2-overview.md:690) |
| T1330-6a256bc4 | docs/dev/roadmap/v0.2-overview.md | 1327 | - [ ] T0695-4e98 T0377-6445 T0432-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.2-overview.md:373) (docs/dev/roadmap/v0.2-overview.md:691) |
| T1331-67a0f91f | docs/dev/roadmap/v0.2-overview.md | 1328 | - [ ] T0696-6510 T0378-9d1f T0433-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.2-overview.md:374) (docs/dev/roadmap/v0.2-overview.md:692) |
| T1332-13a17851 | docs/dev/roadmap/v0.2-overview.md | 1329 | - [ ] T0697-4641 T0379-8488 T0434-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.2-overview.md:375) (docs/dev/roadmap/v0.2-overview.md:693) |
| T1333-edf4e717 | docs/dev/roadmap/v0.2-overview.md | 1330 | - [ ] T0698-5cae T0380-bb04 T0435-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.2-overview.md:376) (docs/dev/roadmap/v0.2-overview.md:694) |
| T1334-dc87c627 | docs/dev/roadmap/v0.2-overview.md | 1331 | - [ ] T0699-9fce T0381-9815 T0436-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.2-overview.md:377) (docs/dev/roadmap/v0.2-overview.md:695) |
| T1335-c747fcf9 | docs/dev/roadmap/v0.2-overview.md | 1332 | - [ ] T0700-e220 T0382-36f3 T0437-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.2-overview.md:378) (docs/dev/roadmap/v0.2-overview.md:696) |
| T1336-56289ac9 | docs/dev/roadmap/v0.2-overview.md | 1333 | - [ ] T0701-414e T0383-dbc9 T0438-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.2-overview.md:379) (docs/dev/roadmap/v0.2-overview.md:697) |
| T1337-62eefdd4 | docs/dev/roadmap/v0.2-overview.md | 1334 | - [ ] T0702-76cc T0384-eb3f T0439-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.2-overview.md:380) (docs/dev/roadmap/v0.2-overview.md:698) |
| T1338-81e39609 | docs/dev/roadmap/v0.2-overview.md | 1335 | - [ ] T0703-de7d T0385-ec08 T0440-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.2-overview.md:381) (docs/dev/roadmap/v0.2-overview.md:699) |
| T1339-f97b2902 | docs/dev/roadmap/v0.2-overview.md | 1336 | - [ ] T0704-44d2 T0386-5337 T0441-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.2-overview.md:382) (docs/dev/roadmap/v0.2-overview.md:700) |
| T1340-1aac5053 | docs/dev/roadmap/v0.2-overview.md | 1337 | - [ ] T0705-0f18 T0387-294c T0442-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.2-overview.md:383) (docs/dev/roadmap/v0.2-overview.md:701) |
| T1341-0c324cae | docs/dev/roadmap/v0.2-overview.md | 1338 | - [ ] T0706-269b T0388-ac9f T0443-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.2-overview.md:384) (docs/dev/roadmap/v0.2-overview.md:702) |
| T1342-c82d043c | docs/dev/roadmap/v0.2-overview.md | 1339 | - [ ] T0707-48cb T0389-87f9 T0444-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.2-overview.md:385) (docs/dev/roadmap/v0.2-overview.md:703) |
| T1343-df862d43 | docs/dev/roadmap/v0.2-overview.md | 1340 | - [ ] T0708-7f09 T0390-b2f6 T0445-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.2-overview.md:386) (docs/dev/roadmap/v0.2-overview.md:704) |
| T1344-f5e3f9b3 | docs/dev/roadmap/v0.2-overview.md | 1341 | - [ ] T0709-7388 T0391-5af2 T0446-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.2-overview.md:387) (docs/dev/roadmap/v0.2-overview.md:705) |
| T1345-822b0875 | docs/dev/roadmap/v0.2-overview.md | 1342 | - [ ] T0710-4323 T0392-b5f9 T0447-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.2-overview.md:388) (docs/dev/roadmap/v0.2-overview.md:706) |
| T1346-bae4de4f | docs/dev/roadmap/v0.2-overview.md | 1343 | - [ ] T0711-e944 T0393-f9f9 T0448-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.2-overview.md:389) (docs/dev/roadmap/v0.2-overview.md:707) |
| T1347-7238369f | docs/dev/roadmap/v0.2-overview.md | 1344 | - [ ] T0712-8335 T0394-5750 T0449-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.2-overview.md:390) (docs/dev/roadmap/v0.2-overview.md:708) |
| T1348-402e0f2d | docs/dev/roadmap/v0.2-overview.md | 1345 | - [ ] T0713-1449 T0395-617a T0450-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.2-overview.md:391) (docs/dev/roadmap/v0.2-overview.md:709) |
| T1349-3b6e070e | docs/dev/roadmap/v0.2-overview.md | 1346 | - [ ] T0714-2ed4 T0396-1b6b T0451-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.2-overview.md:392) (docs/dev/roadmap/v0.2-overview.md:710) |
| T1350-7f90df52 | docs/dev/roadmap/v0.2-overview.md | 1347 | - [ ] T0715-d889 T0397-42f6 T0452-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.2-overview.md:393) (docs/dev/roadmap/v0.2-overview.md:711) |
| T1351-b298cd5a | docs/dev/roadmap/v0.2-overview.md | 1348 | - [ ] T0716-55d2 T0398-c5e5 T0453-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.2-overview.md:394) (docs/dev/roadmap/v0.2-overview.md:712) |
| T1352-22975c22 | docs/dev/roadmap/v0.2-overview.md | 1349 | - [ ] T0717-5484 T0399-8f5a T0454-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.2-overview.md:395) (docs/dev/roadmap/v0.2-overview.md:713) |
| T1353-5827bdd0 | docs/dev/roadmap/v0.2-overview.md | 1350 | - [ ] T0718-29cf T0400-9dd2 T0455-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.2-overview.md:396) (docs/dev/roadmap/v0.2-overview.md:714) |
| T1354-3ccfb5f4 | docs/dev/roadmap/v0.2-overview.md | 1351 | - [ ] T0719-fd01 T0401-3c46 T0456-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.2-overview.md:397) (docs/dev/roadmap/v0.2-overview.md:715) |
| T1355-5153e0a7 | docs/dev/roadmap/v0.2-overview.md | 1352 | - [ ] T0720-81fa T0402-4454 T0457-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.2-overview.md:398) (docs/dev/roadmap/v0.2-overview.md:716) |
| T1356-02a15389 | docs/dev/roadmap/v0.2-overview.md | 1353 | - [ ] T0721-a971 T0403-147a T0458-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.2-overview.md:399) (docs/dev/roadmap/v0.2-overview.md:717) |
| T1357-d8899ba9 | docs/dev/roadmap/v0.2-overview.md | 1354 | - [ ] T0722-6259 T0404-9c10 T0459-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.2-overview.md:400) (docs/dev/roadmap/v0.2-overview.md:718) |
| T1358-8946af60 | docs/dev/roadmap/v0.2-overview.md | 1355 | - [ ] T0723-2e9e T0405-2e18 T0460-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.2-overview.md:401) (docs/dev/roadmap/v0.2-overview.md:719) |
| T1359-220eabff | docs/dev/roadmap/v0.2-overview.md | 1356 | - [ ] T0724-8c3e T0406-3617 T0461-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.2-overview.md:402) (docs/dev/roadmap/v0.2-overview.md:720) |
| T1360-c126339a | docs/dev/roadmap/v0.2-overview.md | 1357 | - [ ] T0725-35b4 T0407-10b9 T0462-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.2-overview.md:403) (docs/dev/roadmap/v0.2-overview.md:721) |
| T1361-5f367edd | docs/dev/roadmap/v0.2-overview.md | 1358 | - [ ] T0726-85d8 T0408-00c0 T0463-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.2-overview.md:404) (docs/dev/roadmap/v0.2-overview.md:722) |
| T1362-997aa700 | docs/dev/roadmap/v0.2-overview.md | 1359 | - [ ] T0727-98fd T0409-13fe T0464-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.2-overview.md:405) (docs/dev/roadmap/v0.2-overview.md:723) |
| T1363-18935614 | docs/dev/roadmap/v0.2-overview.md | 1360 | - [ ] T0728-b8c7 T0410-8137 T0465-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.2-overview.md:406) (docs/dev/roadmap/v0.2-overview.md:724) |
| T1364-61e780a3 | docs/dev/roadmap/v0.2-overview.md | 1361 | - [ ] T0729-0115 T0411-9f65 T0466-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.2-overview.md:407) (docs/dev/roadmap/v0.2-overview.md:725) |
| T1365-3e8e4431 | docs/dev/roadmap/v0.2-overview.md | 1362 | - [ ] T0730-21a0 T0412-285e T0467-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.2-overview.md:408) (docs/dev/roadmap/v0.2-overview.md:726) |
| T1366-8e9b0bfb | docs/dev/roadmap/v0.2-overview.md | 1363 | - [ ] T0731-c433 T0413-50d0 T0468-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.2-overview.md:409) (docs/dev/roadmap/v0.2-overview.md:727) |
| T1367-fa1150fc | docs/dev/roadmap/v0.2-overview.md | 1364 | - [ ] T0732-216c T0414-a18e T0469-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.2-overview.md:410) (docs/dev/roadmap/v0.2-overview.md:728) |
| T1368-5c64e028 | docs/dev/roadmap/v0.2-overview.md | 1365 | - [ ] T0733-5687 T0415-8a8a T0470-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.2-overview.md:411) (docs/dev/roadmap/v0.2-overview.md:729) |
| T1369-2fcdc3b2 | docs/dev/roadmap/v0.2-overview.md | 1366 | - [ ] T0734-fe81 T0416-45d6 T0471-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.2-overview.md:412) (docs/dev/roadmap/v0.2-overview.md:730) |
| T1370-32931cfa | docs/dev/roadmap/v0.2-overview.md | 1367 | - [ ] T0735-a5f8 T0417-2e67 T0472-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.2-overview.md:413) (docs/dev/roadmap/v0.2-overview.md:731) |
| T1371-79b2d394 | docs/dev/roadmap/v0.2-overview.md | 1368 | - [ ] T0736-b3d2 T0418-7a82 T0473-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.2-overview.md:414) (docs/dev/roadmap/v0.2-overview.md:732) |
| T1372-dbea95ab | docs/dev/roadmap/v0.2-overview.md | 1369 | - [ ] T0737-11d6 T0419-8a3a T0474-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.2-overview.md:415) (docs/dev/roadmap/v0.2-overview.md:733) |
| T1373-4e47f7de | docs/dev/roadmap/v0.2-overview.md | 1370 | - [ ] T0738-71c2 T0420-9453 T0475-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.2-overview.md:416) (docs/dev/roadmap/v0.2-overview.md:734) |
| T1374-7b0fe6a7 | docs/dev/roadmap/v0.2-overview.md | 1371 | - [ ] T0739-bcdc T0421-32d2 T0476-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.2-overview.md:417) (docs/dev/roadmap/v0.2-overview.md:735) |
| T1375-b03cf95f | docs/dev/roadmap/v0.2-overview.md | 1372 | - [ ] T0740-9a33 T0422-fd2c T0477-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.2-overview.md:418) (docs/dev/roadmap/v0.2-overview.md:736) |
| T1376-d59b4481 | docs/dev/roadmap/v0.2-overview.md | 1373 | - [ ] T0741-b140 T0423-6119 T0478-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.2-overview.md:419) (docs/dev/roadmap/v0.2-overview.md:737) |
| T1377-458d9fc1 | docs/dev/roadmap/v0.2-overview.md | 1374 | - [ ] T0742-a269 T0424-851a T0479-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.2-overview.md:420) (docs/dev/roadmap/v0.2-overview.md:738) |
| T1378-9f75ed35 | docs/dev/roadmap/v0.2-overview.md | 1375 | - [ ] T0743-8949 T0842-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) (docs/dev/roadmap/v0.2-overview.md:739) |
| T1379-fc9aea22 | docs/dev/roadmap/v0.2-overview.md | 1376 | - [ ] T0744-2c39 T0843-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) (docs/dev/roadmap/v0.2-overview.md:740) |
| T1380-8f16727a | docs/dev/roadmap/v0.2-overview.md | 1377 | - [ ] T0745-f706 T0844-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) (docs/dev/roadmap/v0.2-overview.md:741) |
| T1381-872f6738 | docs/dev/roadmap/v0.2-overview.md | 1378 | - [ ] T0746-ed76 T0845-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) (docs/dev/roadmap/v0.2-overview.md:742) |
| T1382-dac73a90 | docs/dev/roadmap/v0.2-overview.md | 1379 | - [ ] T0747-b343 T0846-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) (docs/dev/roadmap/v0.2-overview.md:743) |
| T1383-93aac416 | docs/dev/roadmap/v0.2-overview.md | 1380 | - [ ] T0748-192d T0847-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) (docs/dev/roadmap/v0.2-overview.md:744) |
| T1384-ab34c7ab | docs/dev/roadmap/v0.2-overview.md | 1381 | - [ ] T0749-a813 T0848-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:745) |
| T1385-7faebf95 | docs/dev/roadmap/v0.2-overview.md | 1382 | - [ ] T0750-83e3 T0849-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:746) |
| T1386-28ceffe3 | docs/dev/roadmap/v0.2-overview.md | 1383 | - [ ] T0751-cfee T0850-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:747) |
| T1387-a211b4b0 | docs/dev/roadmap/v0.2-overview.md | 1384 | - [ ] T0752-71ac T0851-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:748) |
| T1388-737c99e7 | docs/dev/roadmap/v0.2-overview.md | 1385 | - [ ] T0753-edb6 T0852-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:749) |
| T1389-1985770f | docs/dev/roadmap/v0.2-overview.md | 1386 | - [ ] T0754-7f5e T0853-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:750) |
| T1390-4096c688 | docs/dev/roadmap/v0.2-overview.md | 1387 | - [ ] T0755-795c T0854-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:751) |
| T1391-66f50e30 | docs/dev/roadmap/v0.2-overview.md | 1388 | - [ ] T0756-eff7 T0855-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:752) |
| T1392-c5d300db | docs/dev/roadmap/v0.2-overview.md | 1389 | - [ ] T0757-fa0a T0856-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:753) |
| T1393-a1ecf8cf | docs/dev/roadmap/v0.2-overview.md | 1390 | - [ ] T0758-433d T0857-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:754) |
| T1394-a4d55956 | docs/dev/roadmap/v0.2-overview.md | 1391 | - [ ] T0759-32cf T0858-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:755) |
| T1395-2be4c94e | docs/dev/roadmap/v0.2-overview.md | 1392 | - [ ] T0760-7ca6 T0859-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:756) |
| T1396-9167a6fb | docs/dev/roadmap/v0.2-overview.md | 1393 | - [ ] T0761-ea46 T0860-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:757) |
| T1397-cf97ac3f | docs/dev/roadmap/v0.2-overview.md | 1394 | - [ ] T0762-fbcd T0861-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:758) |
| T1398-67883846 | docs/dev/roadmap/v0.2-overview.md | 1395 | - [ ] T0763-94e0 T0862-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:759) |
| T1399-de3a06c3 | docs/dev/roadmap/v0.2-overview.md | 1396 | - [ ] T0764-6d72 T0863-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:760) |
| T1400-af4edec9 | docs/dev/roadmap/v0.2-overview.md | 1397 | - [ ] T0765-4d33 T0864-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:761) |
| T1401-016da209 | docs/dev/roadmap/v0.2-overview.md | 1398 | - [ ] T0766-2f2f T0865-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:762) |
| T1402-759d9253 | docs/dev/roadmap/v0.2-overview.md | 1399 | - [ ] T0767-add9 T0866-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:763) |
| T1403-658205f6 | docs/dev/roadmap/v0.2-overview.md | 1400 | - [ ] T0768-c70d T0867-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:764) |
| T1404-739c044e | docs/dev/roadmap/v0.2-overview.md | 1401 | - [ ] T0769-401c T0868-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:765) |
| T1405-853f0dbe | docs/dev/roadmap/v0.2-overview.md | 1402 | - [ ] T0770-5eff T0869-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:766) |
| T1406-ef5fb383 | docs/dev/roadmap/v0.2-overview.md | 1403 | - [ ] T0771-9bec T0870-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:767) |
| T1407-2d29bbea | docs/dev/roadmap/v0.2-overview.md | 1404 | - [ ] T0772-e847 T0871-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:768) |
| T1408-586946f1 | docs/dev/roadmap/v0.2-overview.md | 1405 | - [ ] T0773-99a0 T0872-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:769) |
| T1409-b323dd09 | docs/dev/roadmap/v0.2-overview.md | 1406 | - [ ] T0774-7600 T0873-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:770) |
| T1410-930fd406 | docs/dev/roadmap/v0.2-overview.md | 1407 | - [ ] T0775-77f0 T0874-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:771) |
| T1411-82ccb8e1 | docs/dev/roadmap/v0.2-overview.md | 1408 | - [ ] T0776-e32b T0875-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:772) |
| T1412-37b0fb01 | docs/dev/roadmap/v0.2-overview.md | 1409 | - [ ] T0777-aec5 T0876-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:773) |
| T1413-0bed289a | docs/dev/roadmap/v0.2-overview.md | 1410 | - [ ] T0778-303a T0877-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:774) |
| T1414-f47582b6 | docs/dev/roadmap/v0.2-overview.md | 1411 | - [ ] T0779-b81c T0878-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:775) |
| T1415-2795039e | docs/dev/roadmap/v0.2-overview.md | 1412 | - [ ] T0780-53af T0879-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:776) |
| T1416-53d1e11e | docs/dev/roadmap/v0.2-overview.md | 1413 | - [ ] T0781-f044 T0880-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:777) |
| T1417-48fb60d4 | docs/dev/roadmap/v0.2-overview.md | 1414 | - [ ] T0782-67e2 T0881-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:778) |
| T1418-ab45e454 | docs/dev/roadmap/v0.2-overview.md | 1415 | - [ ] T0783-b62a T0882-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:779) |
| T1419-d5c935b4 | docs/dev/roadmap/v0.2-overview.md | 1416 | - [ ] T0784-72e5 T0883-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:780) |
| T1420-2983aee3 | docs/dev/roadmap/v0.2-overview.md | 1417 | - [ ] T0785-d364 T0884-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:781) |
| T1421-5c88f1c1 | docs/dev/roadmap/v0.2-overview.md | 1418 | - [ ] T0786-94b0 T0885-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:782) |
| T1422-b3deb490 | docs/dev/roadmap/v0.2-overview.md | 1419 | - [ ] T0787-0b29 T0886-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:783) |
| T1423-48be9a60 | docs/dev/roadmap/v0.2-overview.md | 1420 | - [ ] T0788-bbe3 T0887-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:784) |
| T1424-8e326f2a | docs/dev/roadmap/v0.2-overview.md | 1421 | - [ ] T0789-8248 T0888-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:785) |
| T1425-1023e39a | docs/dev/roadmap/v0.2-overview.md | 1422 | - [ ] T0790-ec7f T0889-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:786) |
| T1426-6b797644 | docs/dev/roadmap/v0.2-overview.md | 1423 | - [ ] T0791-62af T0890-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:787) |
| T1427-470dc335 | docs/dev/roadmap/v0.2-overview.md | 1424 | - [ ] T0792-5044 T0891-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:788) |
| T1428-03d6b9fd | docs/dev/roadmap/v0.2-overview.md | 1425 | - [ ] T0793-144d T0892-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:789) |
| T1429-ca5be8af | docs/dev/roadmap/v0.2-overview.md | 1426 | - [ ] T0794-2421 T0893-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:790) |
| T1430-4b16b418 | docs/dev/roadmap/v0.2-overview.md | 1427 | - [ ] T0795-f476 T0894-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:791) |
| T1431-8b0fcba3 | docs/dev/roadmap/v0.2-overview.md | 1428 | - [ ] T0796-6ba3 T0895-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:792) |
| T1432-ae26268b | docs/dev/roadmap/v0.2-overview.md | 1429 | - [ ] T0797-2092 T0896-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:793) |
| T1433-3570e4a1 | docs/dev/roadmap/v0.2-overview.md | 1430 | - [ ] T0798-5c56 T0898-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:794) |
| T1434-7e20e2dd | docs/dev/roadmap/v0.2-overview.md | 1431 | - [ ] T0799-ae77 T0899-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:795) |
| T1435-227ec5ba | docs/dev/roadmap/v0.2-overview.md | 1432 | - [ ] T0800-9eba T0900-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:796) |
| T1436-060715f5 | docs/dev/roadmap/v0.2-overview.md | 1433 | - [ ] T0801-6187 T0901-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:797) |
| T1437-739cb30c | docs/dev/roadmap/v0.2-overview.md | 1434 | - [ ] T0802-475d T0902-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:798) |
| T1438-5cdf2846 | docs/dev/roadmap/v0.2-overview.md | 1435 | - [ ] T0803-8d1a T0903-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:799) |
| T1439-cca7fc83 | docs/dev/roadmap/v0.2-overview.md | 1436 | - [ ] T0804-7a7c T0904-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:800) |
| T1440-6ec32175 | docs/dev/roadmap/v0.2-overview.md | 1437 | - [ ] T0805-be30 T0905-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:801) |
| T1441-4c70cb07 | docs/dev/roadmap/v0.2-overview.md | 1438 | - [ ] T0806-fb9d T0906-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:802) |
| T1442-ce9f0d63 | docs/dev/roadmap/v0.2-overview.md | 1439 | - [ ] T0807-042a T0907-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:803) |
| T1443-4dbbaaf8 | docs/dev/roadmap/v0.2-overview.md | 1440 | - [ ] T0808-73a6 T0908-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:804) |
| T1444-d63afa61 | docs/dev/roadmap/v0.2-overview.md | 1441 | - [ ] T0809-9fff T0909-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:805) |
| T1445-501c8e74 | docs/dev/roadmap/v0.2-overview.md | 1442 | - [ ] T0810-7aae T0910-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:806) |
| T1446-7f79c2f6 | docs/dev/roadmap/v0.2-overview.md | 1443 | - [ ] T0811-d5e3 T0911-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:807) |
| T1447-0dc7a69f | docs/dev/roadmap/v0.2-overview.md | 1444 | - [ ] T0812-0fd8 T0912-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:808) |
| T1448-db2914d3 | docs/dev/roadmap/v0.2-overview.md | 1445 | - [ ] T0813-ce85 T0913-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:809) |
| T1449-00df118c | docs/dev/roadmap/v0.2-overview.md | 1446 | - [ ] T0814-90e0 T0914-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:810) |
| T1450-03191f23 | docs/dev/roadmap/v0.2-overview.md | 1447 | - [ ] T0815-9cac T0915-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:811) |
| T1451-562edb08 | docs/dev/roadmap/v0.2-overview.md | 1448 | - [ ] T0816-2ac0 T0916-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:812) |
| T1452-c82666de | docs/dev/roadmap/v0.2-overview.md | 1449 | - [ ] T0817-08c6 T0917-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:813) |
| T1453-9fe047ff | docs/dev/roadmap/v0.2-overview.md | 1450 | - [ ] T0818-8471 T0918-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:814) |
| T1454-c1d18c16 | docs/dev/roadmap/v0.2-overview.md | 1451 | - [ ] T0819-8e4d T0919-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:815) |
| T1455-be537bce | docs/dev/roadmap/v0.2-overview.md | 1452 | - [ ] T0820-fff5 T0920-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:816) |
| T1456-059af833 | docs/dev/roadmap/v0.2-overview.md | 1453 | - [ ] T0821-f6a7 T0921-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:817) |
| T1457-65346119 | docs/dev/roadmap/v0.2-overview.md | 1454 | - [ ] T0822-69e0 T0922-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:818) |
| T1458-44a9f587 | docs/dev/roadmap/v0.2-overview.md | 1455 | - [ ] T0823-1598 T0923-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:819) |
| T1459-9a443888 | docs/dev/roadmap/v0.2-overview.md | 1456 | - [ ] T0824-cfea T0924-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:820) |
| T1460-eadd1dca | docs/dev/roadmap/v0.2-overview.md | 1457 | - [ ] T0825-b281 T0925-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:821) |
| T1461-6dafe3dc | docs/dev/roadmap/v0.2-overview.md | 1458 | - [ ] T0826-664e T0926-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:822) |
| T1462-cbc064fd | docs/dev/roadmap/v0.2-overview.md | 1459 | - [ ] T0827-23bb T0927-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:823) |
| T1463-7f13b0e9 | docs/dev/roadmap/v0.2-overview.md | 1460 | - [ ] T0828-788f T0928-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:824) |
| T1464-411d1592 | docs/dev/roadmap/v0.2-overview.md | 1461 | - [ ] T0829-ffda T0929-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:825) |
| T1465-fe93a06b | docs/dev/roadmap/v0.2-overview.md | 1462 | - [ ] T0830-04c8 T0930-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) (docs/dev/roadmap/v0.2-overview.md:826) |
| T1466-425e61e1 | docs/dev/roadmap/v0.2-overview.md | 1463 | - [ ] T0831-5586 T0931-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) (docs/dev/roadmap/v0.2-overview.md:827) |
| T1467-ab89722a | docs/dev/roadmap/v0.2-overview.md | 1464 | - [ ] T0832-2426 T0932-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) (docs/dev/roadmap/v0.2-overview.md:828) |
| T1468-c799f597 | docs/dev/roadmap/v0.2-overview.md | 1465 | - [ ] T0833-7a8a T0933-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) (docs/dev/roadmap/v0.2-overview.md:829) |
| T1469-e4368541 | docs/dev/roadmap/v0.2-overview.md | 1466 | - [ ] T0834-318d T0934-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) (docs/dev/roadmap/v0.2-overview.md:830) |
| T1470-338d4f3a | docs/dev/roadmap/v0.2-overview.md | 1467 | - [ ] T0835-8f20 T0935-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) (docs/dev/roadmap/v0.2-overview.md:831) |
| T1471-6d6ad3f9 | docs/dev/roadmap/v0.2-overview.md | 1468 | - [ ] T0836-e854 T0936-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) (docs/dev/roadmap/v0.2-overview.md:832) |
| T1472-6818d022 | docs/dev/roadmap/v0.2-overview.md | 1469 | - [ ] T0837-35f9 T0937-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) (docs/dev/roadmap/v0.2-overview.md:833) |
| T1473-e38593cc | docs/dev/roadmap/v0.2-overview.md | 1470 | - [ ] T0838-3b5f T0938-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) (docs/dev/roadmap/v0.2-overview.md:834) |
| T1474-e77d199c | docs/dev/roadmap/v0.2-overview.md | 1471 | - [ ] T0839-b52a T0939-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) (docs/dev/roadmap/v0.2-overview.md:835) |
| T1475-6c1b1534 | docs/dev/roadmap/v0.2-overview.md | 1472 | - [ ] T0840-70e3 T0940-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) (docs/dev/roadmap/v0.2-overview.md:836) |
| T1476-edc6638e | docs/dev/roadmap/v0.2-overview.md | 1473 | - [ ] T0841-6143 T0941-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) (docs/dev/roadmap/v0.2-overview.md:837) |
| T1477-cb0e78f7 | docs/dev/roadmap/v0.2-overview.md | 1474 | - [ ] T0842-5f58 T0942-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) (docs/dev/roadmap/v0.2-overview.md:838) |
| T1478-3cad413c | docs/dev/roadmap/v0.2-overview.md | 1475 | - [ ] T0843-dc98 T0943-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) (docs/dev/roadmap/v0.2-overview.md:839) |
| T1479-8f17869a | docs/dev/roadmap/v0.2-overview.md | 1476 | - [ ] T0844-97d0 T0944-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) (docs/dev/roadmap/v0.2-overview.md:840) |
| T1480-c2a72ed1 | docs/dev/roadmap/v0.2-overview.md | 1477 | - [ ] T0845-7152 T0945-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) (docs/dev/roadmap/v0.2-overview.md:841) |
| T1481-288543d5 | docs/dev/roadmap/v0.2-overview.md | 1478 | - [ ] T0846-cd20 T0946-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) (docs/dev/roadmap/v0.2-overview.md:842) |
| T1482-c6cef5f9 | docs/dev/roadmap/v0.2-overview.md | 1479 | - [ ] T0847-36b3 T0947-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) (docs/dev/roadmap/v0.2-overview.md:843) |
| T1483-0388e95b | docs/dev/roadmap/v0.2-overview.md | 1480 | - [ ] T0848-f5e5 T0948-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) (docs/dev/roadmap/v0.2-overview.md:844) |
| T1484-72fc0652 | docs/dev/roadmap/v0.2-overview.md | 1481 | - [ ] T0849-9e53 T0949-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) (docs/dev/roadmap/v0.2-overview.md:845) |
| T1485-4941f300 | docs/dev/roadmap/v0.2-overview.md | 1482 | - [ ] T0850-c4a9 T0950-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) (docs/dev/roadmap/v0.2-overview.md:846) |
| T1486-97a85315 | docs/dev/roadmap/v0.2-overview.md | 1483 | - [ ] T0851-0f43 T0951-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) (docs/dev/roadmap/v0.2-overview.md:847) |
| T1487-59879a3c | docs/dev/roadmap/v0.2-overview.md | 1484 | - [ ] T0852-9835 T0952-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) (docs/dev/roadmap/v0.2-overview.md:848) |
| T1488-1a672edf | docs/dev/roadmap/v0.2-overview.md | 1485 | - [ ] T0853-a338 T0953-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) (docs/dev/roadmap/v0.2-overview.md:849) |
| T1489-b49569b0 | docs/dev/roadmap/v0.2-overview.md | 1486 | - [ ] T0854-f1ee T0954-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) (docs/dev/roadmap/v0.2-overview.md:850) |
| T1490-c928f875 | docs/dev/roadmap/v0.2-overview.md | 1487 | - [ ] T0855-8dfc T0955-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) (docs/dev/roadmap/v0.2-overview.md:851) |
| T1491-0764490c | docs/dev/roadmap/v0.2-overview.md | 1488 | - [ ] T0856-e9f7 T0956-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) (docs/dev/roadmap/v0.2-overview.md:852) |
| T1492-df952f9d | docs/dev/roadmap/v0.2-overview.md | 1489 | - [ ] T0857-42d3 T0957-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) (docs/dev/roadmap/v0.2-overview.md:853) |
| T1493-676a833d | docs/dev/roadmap/v0.2-overview.md | 1490 | - [ ] T0858-4f5b T0958-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) (docs/dev/roadmap/v0.2-overview.md:854) |
| T1494-7972a71b | docs/dev/roadmap/v0.2-overview.md | 1491 | - [ ] T0859-c844 T0959-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) (docs/dev/roadmap/v0.2-overview.md:855) |
| T1495-b6d680c0 | docs/dev/roadmap/v0.2-overview.md | 1492 | - [ ] T0860-b7d2 T0960-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) (docs/dev/roadmap/v0.2-overview.md:856) |
| T1496-f960e763 | docs/dev/roadmap/v0.2-overview.md | 1493 | - [ ] T0861-8744 T0961-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) (docs/dev/roadmap/v0.2-overview.md:857) |
| T1497-803b33a3 | docs/dev/roadmap/v0.2-overview.md | 1494 | - [ ] T0862-e2d7 T0962-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) (docs/dev/roadmap/v0.2-overview.md:858) |
| T1498-b8b348c2 | docs/dev/roadmap/v0.2-overview.md | 1495 | - [ ] T0863-5fec T0963-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) (docs/dev/roadmap/v0.2-overview.md:859) |
| T1499-5ba488e8 | docs/dev/roadmap/v0.2-overview.md | 1496 | - [ ] T0864-99bf T0964-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) (docs/dev/roadmap/v0.2-overview.md:860) |
| T1500-927a9629 | docs/dev/roadmap/v0.2-overview.md | 1497 | - [ ] T0865-7336 T0965-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) (docs/dev/roadmap/v0.2-overview.md:861) |
| T1501-a596d798 | docs/dev/roadmap/v0.2-overview.md | 1498 | - [ ] T0866-18f0 T0966-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) (docs/dev/roadmap/v0.2-overview.md:862) |
| T1502-6df4b30f | docs/dev/roadmap/v0.2-overview.md | 1499 | - [ ] T0867-be43 T0967-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) (docs/dev/roadmap/v0.2-overview.md:863) |
| T1503-929460c5 | docs/dev/roadmap/v0.2-overview.md | 1500 | - [ ] T0868-54bc T0968-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) (docs/dev/roadmap/v0.2-overview.md:864) |
| T1504-ac333cba | docs/dev/roadmap/v0.2-overview.md | 1501 | - [ ] T0869-280d T0969-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) (docs/dev/roadmap/v0.2-overview.md:865) |
| T1505-77f731ef | docs/dev/roadmap/v0.2-overview.md | 1502 | - [ ] T0870-882b T0970-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) (docs/dev/roadmap/v0.2-overview.md:866) |
| T1506-8dcdafab | docs/dev/roadmap/v0.2-overview.md | 1503 | - [ ] T0871-0e2c T0971-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) (docs/dev/roadmap/v0.2-overview.md:867) |
| T1507-13c1d182 | docs/dev/roadmap/v0.2-overview.md | 1504 | - [ ] T0872-39c0 T0972-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) (docs/dev/roadmap/v0.2-overview.md:868) |
| T1508-205d28e7 | docs/dev/roadmap/v0.2-overview.md | 1505 | - [ ] T0873-2ef0 T0973-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) (docs/dev/roadmap/v0.2-overview.md:869) |
| T1509-6ccb5c1d | docs/dev/roadmap/v0.2-overview.md | 1506 | - [ ] T0874-3a4e T0974-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) (docs/dev/roadmap/v0.2-overview.md:870) |
| T1510-28898cfb | docs/dev/roadmap/v0.2-overview.md | 1507 | - [ ] T0875-ee62 T0975-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) (docs/dev/roadmap/v0.2-overview.md:871) |
| T1511-edd6286a | docs/dev/roadmap/v0.2-overview.md | 1508 | - [ ] T0876-96ce T0977-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) (docs/dev/roadmap/v0.2-overview.md:872) |
| T1512-174e730a | docs/dev/roadmap/v0.2-overview.md | 1509 | - [ ] T0877-5c15 T0978-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) (docs/dev/roadmap/v0.2-overview.md:873) |
| T1513-85c8779e | docs/dev/roadmap/v0.2-overview.md | 1510 | - [ ] T0878-beda T0979-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) (docs/dev/roadmap/v0.2-overview.md:874) |
| T1514-ac4d418b | docs/dev/roadmap/v0.2-overview.md | 1511 | - [ ] T0879-0763 T0980-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) (docs/dev/roadmap/v0.2-overview.md:875) |
| T1515-22e5b981 | docs/dev/roadmap/v0.2-overview.md | 1512 | - [ ] T0880-b325 T0981-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) (docs/dev/roadmap/v0.2-overview.md:876) |
| T1516-d70dbd8f | docs/dev/roadmap/v0.2-overview.md | 1513 | - [ ] T0881-04d3 T0982-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) (docs/dev/roadmap/v0.2-overview.md:877) |
| T1517-a054a581 | docs/dev/roadmap/v0.2-overview.md | 1514 | - [ ] T0882-f598 T0983-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) (docs/dev/roadmap/v0.2-overview.md:878) |
| T1518-83d47756 | docs/dev/roadmap/v0.2-overview.md | 1515 | - [ ] T0883-7cac T0984-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) (docs/dev/roadmap/v0.2-overview.md:879) |
| T1519-d27e1c5c | docs/dev/roadmap/v0.2-overview.md | 1516 | - [ ] T0884-ec85 T0985-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) (docs/dev/roadmap/v0.2-overview.md:880) |
| T1520-1bbab763 | docs/dev/roadmap/v0.2-overview.md | 1517 | - [ ] T0885-1200 T0986-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) (docs/dev/roadmap/v0.2-overview.md:881) |
| T1521-baf8abae | docs/dev/roadmap/v0.2-overview.md | 1518 | - [ ] T0886-e840 T0987-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) (docs/dev/roadmap/v0.2-overview.md:882) |
| T1522-0d16017a | docs/dev/roadmap/v0.2-overview.md | 1519 | - [ ] T0887-fcd2 T0988-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) (docs/dev/roadmap/v0.2-overview.md:883) |
| T1523-5c28da31 | docs/dev/roadmap/v0.2-overview.md | 1520 | - [ ] T0888-5364 T0989-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) (docs/dev/roadmap/v0.2-overview.md:884) |
| T1524-c3230754 | docs/dev/roadmap/v0.2-overview.md | 1521 | - [ ] T0889-2d04 T0990-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) (docs/dev/roadmap/v0.2-overview.md:885) |
| T1525-9bc26d69 | docs/dev/roadmap/v0.2-overview.md | 1522 | - [ ] T0890-03c2 T0991-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) (docs/dev/roadmap/v0.2-overview.md:886) |
| T1526-27746a21 | docs/dev/roadmap/v0.2-overview.md | 1523 | - [ ] T0891-2f35 T0992-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) (docs/dev/roadmap/v0.2-overview.md:887) |
| T1527-159db9e6 | docs/dev/roadmap/v0.2-overview.md | 1524 | - [ ] T0892-3625 T0993-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) (docs/dev/roadmap/v0.2-overview.md:888) |
| T1528-47b03cf6 | docs/dev/roadmap/v0.2-overview.md | 1525 | - [ ] T0893-dd15 T0994-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) (docs/dev/roadmap/v0.2-overview.md:889) |
| T1529-7c01fed0 | docs/dev/roadmap/v0.2-overview.md | 1526 | - [ ] T0894-1be9 T0995-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) (docs/dev/roadmap/v0.2-overview.md:890) |
| T1530-d754a426 | docs/dev/roadmap/v0.2-overview.md | 1527 | - [ ] T0895-75e1 T0996-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) (docs/dev/roadmap/v0.2-overview.md:891) |
| T1531-7f231246 | docs/dev/roadmap/v0.2-overview.md | 1528 | - [ ] T0896-fe80 T0997-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) (docs/dev/roadmap/v0.2-overview.md:892) |
| T1532-1d21a1a9 | docs/dev/roadmap/v0.2-overview.md | 1529 | - [ ] T0897-c848 T0998-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) (docs/dev/roadmap/v0.2-overview.md:893) |
| T1533-5b1e6e73 | docs/dev/roadmap/v0.2-overview.md | 1530 | - [ ] T0898-b033 T0999-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) (docs/dev/roadmap/v0.2-overview.md:894) |
| T1534-20911cf6 | docs/dev/roadmap/v0.2-overview.md | 1531 | - [ ] T0899-232d T1000-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) (docs/dev/roadmap/v0.2-overview.md:895) |
| T1535-2f587517 | docs/dev/roadmap/v0.2-overview.md | 1532 | - [ ] T0900-c180 T1001-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) (docs/dev/roadmap/v0.2-overview.md:896) |
| T1536-80c1b74b | docs/dev/roadmap/v0.2-overview.md | 1533 | - [ ] T0901-3402 T1002-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) (docs/dev/roadmap/v0.2-overview.md:897) |
| T1537-c21d850d | docs/dev/roadmap/v0.2-overview.md | 1534 | - [ ] T0902-b2df T1003-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) (docs/dev/roadmap/v0.2-overview.md:898) |
| T1538-f5465e6e | docs/dev/roadmap/v0.2-overview.md | 1535 | - [ ] T0903-b5a7 T1004-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) (docs/dev/roadmap/v0.2-overview.md:899) |
| T1539-6e115fbe | docs/dev/roadmap/v0.2-overview.md | 1536 | - [ ] T0904-a9df T1005-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) (docs/dev/roadmap/v0.2-overview.md:900) |
| T1540-b6a677a7 | docs/dev/roadmap/v0.2-overview.md | 1537 | - [ ] T0905-184a T1006-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) (docs/dev/roadmap/v0.2-overview.md:901) |
| T1541-9329f71a | docs/dev/roadmap/v0.2-overview.md | 1538 | - [ ] T0906-4678 T1007-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) (docs/dev/roadmap/v0.2-overview.md:902) |
| T1542-c6055750 | docs/dev/roadmap/v0.2-overview.md | 1539 | - [ ] T0907-981f T1008-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) (docs/dev/roadmap/v0.2-overview.md:903) |
| T1543-9279ed48 | docs/dev/roadmap/v0.2-overview.md | 1540 | - [ ] T0908-1ff5 T1009-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) (docs/dev/roadmap/v0.2-overview.md:904) |
| T1544-d15b0668 | docs/dev/roadmap/v0.2-overview.md | 1541 | - [ ] T0909-77f0 T1010-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) (docs/dev/roadmap/v0.2-overview.md:905) |
| T1545-cecd02e0 | docs/dev/roadmap/v0.2-overview.md | 1542 | - [ ] T0910-4a05 T1011-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) (docs/dev/roadmap/v0.2-overview.md:906) |
| T1546-ad1843ea | docs/dev/roadmap/v0.2-overview.md | 1543 | - [ ] T0911-5bb7 T1012-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) (docs/dev/roadmap/v0.2-overview.md:907) |
| T1547-5cd18794 | docs/dev/roadmap/v0.2-overview.md | 1544 | - [ ] T0912-db32 T1013-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) (docs/dev/roadmap/v0.2-overview.md:908) |
| T1548-c8b5bd3e | docs/dev/roadmap/v0.2-overview.md | 1545 | - [ ] T0913-b5e9 T1014-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) (docs/dev/roadmap/v0.2-overview.md:909) |
| T1549-e886daf7 | docs/dev/roadmap/v0.2-overview.md | 1546 | - [ ] T0914-7d15 T1015-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) (docs/dev/roadmap/v0.2-overview.md:910) |
| T1550-961b331c | docs/dev/roadmap/v0.2-overview.md | 1547 | - [ ] T0915-0a4f T1016-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) (docs/dev/roadmap/v0.2-overview.md:911) |
| T1551-7971966c | docs/dev/roadmap/v0.2-overview.md | 1548 | - [ ] T0916-f9f1 T1017-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) (docs/dev/roadmap/v0.2-overview.md:912) |
| T1552-0aa77650 | docs/dev/roadmap/v0.2-overview.md | 1549 | - [ ] T0917-cb6b T1018-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) (docs/dev/roadmap/v0.2-overview.md:913) |
| T1553-37177dce | docs/dev/roadmap/v0.2-overview.md | 1550 | - [ ] T0918-a142 T1019-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) (docs/dev/roadmap/v0.2-overview.md:914) |
| T1554-9a5b68f6 | docs/dev/roadmap/v0.2-overview.md | 1551 | - [ ] T0919-ffbc T1020-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) (docs/dev/roadmap/v0.2-overview.md:915) |
| T1555-ac1e4e89 | docs/dev/roadmap/v0.2-overview.md | 1552 | - [ ] T0920-e3d9 T1021-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) (docs/dev/roadmap/v0.2-overview.md:916) |
| T1556-d302e3fc | docs/dev/roadmap/v0.2-overview.md | 1553 | - [ ] T0921-39ef T1022-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) (docs/dev/roadmap/v0.2-overview.md:917) |
| T1557-80b396bc | docs/dev/roadmap/v0.2-overview.md | 1554 | - [ ] T0922-1305 T1023-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) (docs/dev/roadmap/v0.2-overview.md:918) |
| T1558-ab36d475 | docs/dev/roadmap/v0.2-overview.md | 1555 | - [ ] T0923-3683 T1024-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) (docs/dev/roadmap/v0.2-overview.md:919) |
| T1559-e6999be7 | docs/dev/roadmap/v0.2-overview.md | 1556 | - [ ] T0924-4070 T1025-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) (docs/dev/roadmap/v0.2-overview.md:920) |
| T1560-defff534 | docs/dev/roadmap/v0.2-overview.md | 1557 | - [ ] T0925-2b5a T1026-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) (docs/dev/roadmap/v0.2-overview.md:921) |
| T1561-c9bd4058 | docs/dev/roadmap/v0.2-overview.md | 1558 | - [ ] T0926-9573 T1027-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) (docs/dev/roadmap/v0.2-overview.md:922) |
| T1562-fea155c6 | docs/dev/roadmap/v0.2-overview.md | 1559 | - [ ] T0927-76cb T1028-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) (docs/dev/roadmap/v0.2-overview.md:923) |
| T1563-f1e3084e | docs/dev/roadmap/v0.2-overview.md | 1560 | - [ ] T0928-b052 T1029-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) (docs/dev/roadmap/v0.2-overview.md:924) |
| T1564-160683fc | docs/dev/roadmap/v0.2-overview.md | 1561 | - [ ] T0929-87f2 T1030-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) (docs/dev/roadmap/v0.2-overview.md:925) |
| T1565-d7c90bee | docs/dev/roadmap/v0.2-overview.md | 1562 | - [ ] T0930-608a T1031-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) (docs/dev/roadmap/v0.2-overview.md:926) |
| T1566-fb8d87f0 | docs/dev/roadmap/v0.2-overview.md | 1563 | - [ ] T0931-8bda T1032-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) (docs/dev/roadmap/v0.2-overview.md:927) |
| T1567-0100ccf8 | docs/dev/roadmap/v0.2-overview.md | 1564 | - [ ] T0932-2431 T1033-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) (docs/dev/roadmap/v0.2-overview.md:928) |
| T1568-0b6c7c83 | docs/dev/roadmap/v0.2-overview.md | 1565 | - [ ] T0933-6d77 T1035-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) (docs/dev/roadmap/v0.2-overview.md:929) |
| T1569-8a7f4031 | docs/dev/roadmap/v0.2-overview.md | 1566 | - [ ] T0934-717d T1036-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) (docs/dev/roadmap/v0.2-overview.md:930) |
| T1570-a301aaea | docs/dev/roadmap/v0.2-overview.md | 1567 | - [ ] T0935-984e T1037-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) (docs/dev/roadmap/v0.2-overview.md:931) |
| T1571-8500bc05 | docs/dev/roadmap/v0.2-overview.md | 1568 | - [ ] T0936-4a59 T1038-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) (docs/dev/roadmap/v0.2-overview.md:932) |
| T1572-8b35be9c | docs/dev/roadmap/v0.2-overview.md | 1569 | - [ ] T0937-8bfd T1039-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) (docs/dev/roadmap/v0.2-overview.md:933) |
| T1573-5d419f87 | docs/dev/roadmap/v0.2-overview.md | 1570 | - [ ] T0938-70a5 T1040-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) (docs/dev/roadmap/v0.2-overview.md:934) |
| T1574-3003ebf0 | docs/dev/roadmap/v0.2-overview.md | 1571 | - [ ] T0939-df18 T1041-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) (docs/dev/roadmap/v0.2-overview.md:935) |
| T1575-36344cd6 | docs/dev/roadmap/v0.2-overview.md | 1572 | - [ ] T0940-f918 T1042-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) (docs/dev/roadmap/v0.2-overview.md:936) |
| T1576-9c246221 | docs/dev/roadmap/v0.2-overview.md | 1573 | - [ ] T0941-0cea T1043-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) (docs/dev/roadmap/v0.2-overview.md:937) |
| T1577-a9178429 | docs/dev/roadmap/v0.2-overview.md | 1574 | - [ ] T0942-ddc2 T1044-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) (docs/dev/roadmap/v0.2-overview.md:938) |
| T1578-444ebcdc | docs/dev/roadmap/v0.2-overview.md | 1575 | - [ ] T0943-81c0 T1045-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) (docs/dev/roadmap/v0.2-overview.md:939) |
| T1579-a7ffe6a3 | docs/dev/roadmap/v0.2-overview.md | 1576 | - [ ] T0944-ee3f T1046-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) (docs/dev/roadmap/v0.2-overview.md:940) |
| T1580-bdf949ae | docs/dev/roadmap/v0.2-overview.md | 1577 | - [ ] T0945-735b T1047-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) (docs/dev/roadmap/v0.2-overview.md:941) |
| T1581-9c6a0f42 | docs/dev/roadmap/v0.2-overview.md | 1578 | - [ ] T0946-c695 T1048-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) (docs/dev/roadmap/v0.2-overview.md:942) |
| T1582-0d6d32f8 | docs/dev/roadmap/v0.2-overview.md | 1579 | - [ ] T0947-ffaa T1049-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) (docs/dev/roadmap/v0.2-overview.md:943) |
| T1583-2f234915 | docs/dev/roadmap/v0.2-overview.md | 1580 | - [ ] T0948-3e68 T1050-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) (docs/dev/roadmap/v0.2-overview.md:944) |
| T1584-9040ea11 | docs/dev/roadmap/v0.2-overview.md | 1581 | - [ ] T0949-e008 T1051-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) (docs/dev/roadmap/v0.2-overview.md:945) |
| T1585-a86e6235 | docs/dev/roadmap/v0.2-overview.md | 1582 | - [ ] T0950-196b T1052-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) (docs/dev/roadmap/v0.2-overview.md:946) |
| T1586-d81bd0a4 | docs/dev/roadmap/v0.2-overview.md | 1583 | - [ ] T0951-f6f5 T1053-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) (docs/dev/roadmap/v0.2-overview.md:947) |
| T1587-1ec22f3b | docs/dev/roadmap/v0.2-overview.md | 1584 | - [ ] T0952-ebec T1054-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) (docs/dev/roadmap/v0.2-overview.md:948) |
| T1588-58c06cd8 | docs/dev/roadmap/v0.2-overview.md | 1585 | - [ ] T0953-2164 T1055-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) (docs/dev/roadmap/v0.2-overview.md:949) |
| T1589-68c8c661 | docs/dev/roadmap/v0.2-overview.md | 1586 | - [ ] T0954-18ff T1056-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) (docs/dev/roadmap/v0.2-overview.md:950) |
| T1590-09682fdf | docs/dev/roadmap/v0.2-overview.md | 1587 | - [ ] T0955-47f5 T1057-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) (docs/dev/roadmap/v0.2-overview.md:951) |
| T1591-55ddf6b6 | docs/dev/roadmap/v0.2-overview.md | 1588 | - [ ] T0956-9e1f T1058-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) (docs/dev/roadmap/v0.2-overview.md:952) |
| T1592-e1c503b1 | docs/dev/roadmap/v0.2-overview.md | 1589 | - [ ] T0957-9d67 T1059-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) (docs/dev/roadmap/v0.2-overview.md:953) |
| T1593-90344a13 | docs/dev/roadmap/v0.2-overview.md | 1590 | - [ ] T0958-8a98 T1060-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) (docs/dev/roadmap/v0.2-overview.md:954) |
| T1594-33fee7bb | docs/dev/roadmap/v0.2-overview.md | 1591 | - [ ] T0959-b2c7 T1061-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) (docs/dev/roadmap/v0.2-overview.md:955) |
| T1595-e6cf6366 | docs/dev/roadmap/v0.2-overview.md | 1592 | - [ ] T0960-684c T1062-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) (docs/dev/roadmap/v0.2-overview.md:956) |
| T1596-86b07440 | docs/dev/roadmap/v0.2-overview.md | 1593 | - [ ] T0961-e6ed T1063-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) (docs/dev/roadmap/v0.2-overview.md:957) |
| T1597-2d6609a2 | docs/dev/roadmap/v0.2-overview.md | 1594 | - [ ] T0962-99c7 T1064-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) (docs/dev/roadmap/v0.2-overview.md:958) |
| T1598-8f3cd2ad | docs/dev/roadmap/v0.2-overview.md | 1595 | - [ ] T0963-de25 T1065-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) (docs/dev/roadmap/v0.2-overview.md:959) |
| T1599-e5ef17e3 | docs/dev/roadmap/v0.2-overview.md | 1596 | - [ ] T0964-481a T1066-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) (docs/dev/roadmap/v0.2-overview.md:960) |
| T1600-cd5ae939 | docs/dev/roadmap/v0.2-overview.md | 1597 | - [ ] T0965-b9b1 T1067-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) (docs/dev/roadmap/v0.2-overview.md:961) |
| T1601-34f6210a | docs/dev/roadmap/v0.2-overview.md | 1598 | - [ ] T0966-6717 T1068-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) (docs/dev/roadmap/v0.2-overview.md:962) |
| T1602-08a4a81d | docs/dev/roadmap/v0.2-overview.md | 1599 | - [ ] T0967-02c4 T1069-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) (docs/dev/roadmap/v0.2-overview.md:963) |
| T1603-5acc3ae2 | docs/dev/roadmap/v0.2-overview.md | 1600 | - [ ] T0968-802f T1070-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) (docs/dev/roadmap/v0.2-overview.md:964) |
| T1604-92fc322b | docs/dev/roadmap/v0.2-overview.md | 1601 | - [ ] T0969-d305 T1071-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) (docs/dev/roadmap/v0.2-overview.md:965) |
| T1605-bff3081f | docs/dev/roadmap/v0.2-overview.md | 1602 | - [ ] T0970-efd0 T1072-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) (docs/dev/roadmap/v0.2-overview.md:966) |
| T1606-1fa1429b | docs/dev/roadmap/v0.2-overview.md | 1603 | - [ ] T0971-988c T1073-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) (docs/dev/roadmap/v0.2-overview.md:967) |
| T1607-58f8fa3f | docs/dev/roadmap/v0.2-overview.md | 1604 | - [ ] T0972-cc59 T1074-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) (docs/dev/roadmap/v0.2-overview.md:968) |
| T1608-723c4768 | docs/dev/roadmap/v0.2-overview.md | 1605 | - [ ] T0973-b971 T1075-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) (docs/dev/roadmap/v0.2-overview.md:969) |
| T1609-07cf382e | docs/dev/roadmap/v0.2-overview.md | 1606 | - [ ] T0974-59c8 T1076-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) (docs/dev/roadmap/v0.2-overview.md:970) |
| T1610-ed942c14 | docs/dev/roadmap/v0.2-overview.md | 1607 | - [ ] T0975-5bf4 T1077-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) (docs/dev/roadmap/v0.2-overview.md:971) |
| T1611-c5dcf313 | docs/dev/roadmap/v0.2-overview.md | 1608 | - [ ] T0976-6f2e T1078-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) (docs/dev/roadmap/v0.2-overview.md:972) |
| T1612-32cdac46 | docs/dev/roadmap/v0.2-overview.md | 1609 | - [ ] T0977-787f T1079-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) (docs/dev/roadmap/v0.2-overview.md:973) |
| T1613-bb50047c | docs/dev/roadmap/v0.2-overview.md | 1610 | - [ ] T0978-b7ae T1080-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) (docs/dev/roadmap/v0.2-overview.md:974) |
| T1614-f951643b | docs/dev/roadmap/v0.2-overview.md | 1611 | - [ ] T0979-b206 T1081-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) (docs/dev/roadmap/v0.2-overview.md:975) |
| T1615-5165f06d | docs/dev/roadmap/v0.2-overview.md | 1612 | - [ ] T0980-5d0d T1082-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) (docs/dev/roadmap/v0.2-overview.md:976) |
| T1616-84f9def8 | docs/dev/roadmap/v0.2-overview.md | 1613 | - [ ] T0981-cdb8 T1083-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) (docs/dev/roadmap/v0.2-overview.md:977) |
| T1617-22bddeb0 | docs/dev/roadmap/v0.2-overview.md | 1614 | - [ ] T0982-4943 T1084-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) (docs/dev/roadmap/v0.2-overview.md:978) |
| T1618-6b814bab | docs/dev/roadmap/v0.2-overview.md | 1615 | - [ ] T0983-d166 T1085-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) (docs/dev/roadmap/v0.2-overview.md:979) |
| T1619-731e59b5 | docs/dev/roadmap/v0.2-overview.md | 1616 | - [ ] T0984-00b6 T1086-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) (docs/dev/roadmap/v0.2-overview.md:980) |
| T1620-03ecf663 | docs/dev/roadmap/v0.2-overview.md | 1617 | - [ ] T0985-2c05 T1087-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) (docs/dev/roadmap/v0.2-overview.md:981) |
| T1621-f2bb8dfe | docs/dev/roadmap/v0.2-overview.md | 1618 | - [ ] T0986-55f7 T1088-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) (docs/dev/roadmap/v0.2-overview.md:982) |
| T1622-5e9345f3 | docs/dev/roadmap/v0.2-overview.md | 1619 | - [ ] T0987-6800 T1089-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) (docs/dev/roadmap/v0.2-overview.md:983) |
| T1623-cf6a01da | docs/dev/roadmap/v0.2-overview.md | 1620 | - [ ] T0988-4ff2 T1090-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) (docs/dev/roadmap/v0.2-overview.md:984) |
| T1624-d70c7864 | docs/dev/roadmap/v0.2-overview.md | 1621 | - [ ] T0989-4419 T1091-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) (docs/dev/roadmap/v0.2-overview.md:985) |
| T1625-af8363aa | docs/dev/roadmap/v0.2-overview.md | 1622 | - [ ] T0990-6396 T1092-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) (docs/dev/roadmap/v0.2-overview.md:986) |
| T1626-a9fa77bc | docs/dev/roadmap/v0.2-overview.md | 1623 | - [ ] T0991-0a22 T1093-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) (docs/dev/roadmap/v0.2-overview.md:987) |
| T1627-693e2d0d | docs/dev/roadmap/v0.2-overview.md | 1624 | - [ ] T0992-085f T1094-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) (docs/dev/roadmap/v0.2-overview.md:988) |
| T1628-39a49f37 | docs/dev/roadmap/v0.2-overview.md | 1625 | - [ ] T0993-cc1e T1095-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) (docs/dev/roadmap/v0.2-overview.md:989) |
| T1629-d0f5ddce | docs/dev/roadmap/v0.2-overview.md | 1626 | - [ ] T0994-fddc T1096-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) (docs/dev/roadmap/v0.2-overview.md:990) |
| T1630-9f0af918 | docs/dev/roadmap/v0.2-overview.md | 1627 | - [ ] T0995-8d91 T1097-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) (docs/dev/roadmap/v0.2-overview.md:991) |
| T1631-51901fc0 | docs/dev/roadmap/v0.2-overview.md | 1628 | - [ ] T0996-5d8e T1098-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) (docs/dev/roadmap/v0.2-overview.md:992) |
| T1632-6439f80d | docs/dev/roadmap/v0.2-overview.md | 1629 | - [ ] T0997-66f8 T1099-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) (docs/dev/roadmap/v0.2-overview.md:993) |
| T1633-3e85df98 | docs/dev/roadmap/v0.2-overview.md | 1630 | - [ ] T0998-4773 T1100-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) (docs/dev/roadmap/v0.2-overview.md:994) |
| T1634-b4b38e0c | docs/dev/roadmap/v0.2-overview.md | 1631 | - [ ] T0999-666c T1101-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) (docs/dev/roadmap/v0.2-overview.md:995) |
| T1635-7448e1c2 | docs/dev/roadmap/v0.2-overview.md | 1632 | - [ ] T1000-2001 T1102-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) (docs/dev/roadmap/v0.2-overview.md:996) |
| T1636-f1cc8bf0 | docs/dev/roadmap/v0.2-overview.md | 1633 | - [ ] T1001-f436 T1103-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) (docs/dev/roadmap/v0.2-overview.md:997) |
| T1637-26f55e8d | docs/dev/roadmap/v0.2-overview.md | 1634 | - [ ] T1002-656a T1104-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) (docs/dev/roadmap/v0.2-overview.md:998) |
| T1638-784728fd | docs/dev/roadmap/v0.2-overview.md | 1635 | - [ ] T1003-dd59 T1105-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) (docs/dev/roadmap/v0.2-overview.md:999) |
| T1639-d00d65f0 | docs/dev/roadmap/v0.2-overview.md | 1636 | - [ ] T1004-4ba4 T1106-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) (docs/dev/roadmap/v0.2-overview.md:1000) |
| T1640-6686e87c | docs/dev/roadmap/v0.2-overview.md | 1637 | - [ ] T1005-66e5 T1107-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) (docs/dev/roadmap/v0.2-overview.md:1001) |
| T1641-f24b8980 | docs/dev/roadmap/v0.2-overview.md | 1638 | - [ ] T1006-4b31 T1108-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) (docs/dev/roadmap/v0.2-overview.md:1002) |
| T1642-61c7551b | docs/dev/roadmap/v0.2-overview.md | 1639 | - [ ] T1007-8f97 T1109-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) (docs/dev/roadmap/v0.2-overview.md:1003) |
| T1643-afedca1a | docs/dev/roadmap/v0.2-overview.md | 1640 | - [ ] T1008-d36f T1110-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) (docs/dev/roadmap/v0.2-overview.md:1004) |
| T1644-9604b630 | docs/dev/roadmap/v0.2-overview.md | 1641 | - [ ] T1009-6c28 T1111-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) (docs/dev/roadmap/v0.2-overview.md:1005) |
| T1645-e109cca9 | docs/dev/roadmap/v0.2-overview.md | 1642 | - [ ] T1010-383c T1112-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) (docs/dev/roadmap/v0.2-overview.md:1006) |
| T1646-b2adb144 | docs/dev/roadmap/v0.2-overview.md | 1643 | - [ ] T1011-3925 T1113-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) (docs/dev/roadmap/v0.2-overview.md:1007) |
| T1647-cfb6345d | docs/dev/roadmap/v0.2-overview.md | 1644 | - [ ] T1012-fa1a T1114-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) (docs/dev/roadmap/v0.2-overview.md:1008) |
| T1648-fad68033 | docs/dev/roadmap/v0.2-overview.md | 1645 | - [ ] T1013-d659 T1115-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) (docs/dev/roadmap/v0.2-overview.md:1009) |
| T1649-533d6515 | docs/dev/roadmap/v0.2-overview.md | 1646 | - [ ] T1014-cf0f T1116-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) (docs/dev/roadmap/v0.2-overview.md:1010) |
| T1650-bb524380 | docs/dev/roadmap/v0.2-overview.md | 1647 | - [ ] T1015-f041 T1117-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) (docs/dev/roadmap/v0.2-overview.md:1011) |
| T1651-a1c8cb4c | docs/dev/roadmap/v0.2-overview.md | 1648 | - [ ] T1016-f6c2 T1118-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) (docs/dev/roadmap/v0.2-overview.md:1012) |
| T1652-552c239a | docs/dev/roadmap/v0.2-overview.md | 1649 | - [ ] T1017-4635 T1119-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) (docs/dev/roadmap/v0.2-overview.md:1013) |
| T1653-09d2f72f | docs/dev/roadmap/v0.2-overview.md | 1650 | - [ ] T1018-f664 T1120-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) (docs/dev/roadmap/v0.2-overview.md:1014) |
| T1654-0e33ee5d | docs/dev/roadmap/v0.2-overview.md | 1651 | - [ ] T1019-d796 T1121-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) (docs/dev/roadmap/v0.2-overview.md:1015) |
| T1655-ab6f7691 | docs/dev/roadmap/v0.2-overview.md | 1652 | - [ ] T1020-c8cf T1122-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) (docs/dev/roadmap/v0.2-overview.md:1016) |
| T1656-40a78821 | docs/dev/roadmap/v0.2-overview.md | 1653 | - [ ] T1021-0da4 T1123-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) (docs/dev/roadmap/v0.2-overview.md:1017) |
| T1657-d3150d0f | docs/dev/roadmap/v0.2-overview.md | 1654 | - [ ] T1022-8313 T1124-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) (docs/dev/roadmap/v0.2-overview.md:1018) |
| T1658-4345ea85 | docs/dev/roadmap/v0.2-overview.md | 1655 | - [ ] T1023-08c4 T1125-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) (docs/dev/roadmap/v0.2-overview.md:1019) |
| T1659-78e49d07 | docs/dev/roadmap/v0.2-overview.md | 1656 | - [ ] T1024-64e5 T1126-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) (docs/dev/roadmap/v0.2-overview.md:1020) |
| T1660-98ae4417 | docs/dev/roadmap/v0.2-overview.md | 1657 | - [ ] T1025-fbb4 T1127-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) (docs/dev/roadmap/v0.2-overview.md:1021) |
| T1661-0da7ac0f | docs/dev/roadmap/v0.2-overview.md | 1658 | - [ ] T1026-610d T1128-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) (docs/dev/roadmap/v0.2-overview.md:1022) |
| T1662-ac8e463c | docs/dev/roadmap/v0.2-overview.md | 1659 | - [ ] T1027-329b T1129-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) (docs/dev/roadmap/v0.2-overview.md:1023) |
| T1663-0e393be2 | docs/dev/roadmap/v0.2-overview.md | 1660 | - [ ] T1028-15cf T1130-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) (docs/dev/roadmap/v0.2-overview.md:1024) |
| T1664-d525fcff | docs/dev/roadmap/v0.2-overview.md | 1661 | - [ ] T1029-4491 T1131-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) (docs/dev/roadmap/v0.2-overview.md:1025) |
| T1665-9e3de542 | docs/dev/roadmap/v0.2-overview.md | 1662 | - [ ] T1030-789b T1132-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) (docs/dev/roadmap/v0.2-overview.md:1026) |
| T1666-d60f27a8 | docs/dev/roadmap/v0.2-overview.md | 1663 | - [ ] T1031-87ff T1133-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) (docs/dev/roadmap/v0.2-overview.md:1027) |
| T1667-7e2d3a1d | docs/dev/roadmap/v0.2-overview.md | 1664 | - [ ] T1032-2426 T1134-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) (docs/dev/roadmap/v0.2-overview.md:1028) |
| T1668-22bf97fd | docs/dev/roadmap/v0.2-overview.md | 1665 | - [ ] T1033-7f02 T1135-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) (docs/dev/roadmap/v0.2-overview.md:1029) |
| T1669-3b8071da | docs/dev/roadmap/v0.2-overview.md | 1666 | - [ ] T1034-7f41 T1136-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) (docs/dev/roadmap/v0.2-overview.md:1030) |
| T1670-bf60c6e1 | docs/dev/roadmap/v0.2-overview.md | 1667 | - [ ] T1035-fc8b T1137-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) (docs/dev/roadmap/v0.2-overview.md:1031) |
| T1671-057c518e | docs/dev/roadmap/v0.2-overview.md | 1668 | - [ ] T1036-3a27 T1138-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) (docs/dev/roadmap/v0.2-overview.md:1032) |
| T1672-b43a8162 | docs/dev/roadmap/v0.2-overview.md | 1669 | - [ ] T1037-8d53 T1139-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) (docs/dev/roadmap/v0.2-overview.md:1033) |
| T1673-9f72133c | docs/dev/roadmap/v0.2-overview.md | 1670 | - [ ] T1038-2833 T1140-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) (docs/dev/roadmap/v0.2-overview.md:1034) |
| T1674-ed1096a9 | docs/dev/roadmap/v0.2-overview.md | 1671 | - [ ] T1039-304b T1141-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) (docs/dev/roadmap/v0.2-overview.md:1035) |
| T1675-7e74be9f | docs/dev/roadmap/v0.2-overview.md | 1672 | - [ ] T1040-930c T1142-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) (docs/dev/roadmap/v0.2-overview.md:1036) |
| T1676-5be00928 | docs/dev/roadmap/v0.2-overview.md | 1673 | - [ ] T1041-ea84 T1143-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) (docs/dev/roadmap/v0.2-overview.md:1037) |
| T1677-576bbea8 | docs/dev/roadmap/v0.2-overview.md | 1674 | - [ ] T1042-0a0e T1144-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) (docs/dev/roadmap/v0.2-overview.md:1038) |
| T1678-4606c294 | docs/dev/roadmap/v0.2-overview.md | 1675 | - [ ] T1043-f3d9 T1145-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) (docs/dev/roadmap/v0.2-overview.md:1039) |
| T1679-41cfc398 | docs/dev/roadmap/v0.2-overview.md | 1676 | - [ ] T1044-d61b T1146-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) (docs/dev/roadmap/v0.2-overview.md:1040) |
| T1680-a53aacfb | docs/dev/roadmap/v0.2-overview.md | 1677 | - [ ] T1045-1432 T1147-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) (docs/dev/roadmap/v0.2-overview.md:1041) |
| T1681-184f8c57 | docs/dev/roadmap/v0.2-overview.md | 1678 | - [ ] T1046-ba47 T1148-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) (docs/dev/roadmap/v0.2-overview.md:1042) |
| T1682-d3c3fa94 | docs/dev/roadmap/v0.2-overview.md | 1679 | - [ ] T1047-5f35 T1149-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) (docs/dev/roadmap/v0.2-overview.md:1043) |
| T1683-83b10a09 | docs/dev/roadmap/v0.2-overview.md | 1680 | - [ ] T1048-db90 T1150-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) (docs/dev/roadmap/v0.2-overview.md:1044) |
| T1684-cf25411b | docs/dev/roadmap/v0.2-overview.md | 1681 | - [ ] T1049-3fd3 T1151-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) (docs/dev/roadmap/v0.2-overview.md:1045) |
| T1685-4dac7e30 | docs/dev/roadmap/v0.2-overview.md | 1682 | - [ ] T1050-ff08 T1152-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) (docs/dev/roadmap/v0.2-overview.md:1046) |
| T1686-f3aabb02 | docs/dev/roadmap/v0.2-overview.md | 1683 | - [ ] T1051-20cb T1153-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) (docs/dev/roadmap/v0.2-overview.md:1047) |
| T1687-0336c3db | docs/dev/roadmap/v0.2-overview.md | 1684 | - [ ] T1052-af9b T1154-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) (docs/dev/roadmap/v0.2-overview.md:1048) |
| T1688-3a5ce292 | docs/dev/roadmap/v0.2-overview.md | 1685 | - [ ] T1053-e604 T1155-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) (docs/dev/roadmap/v0.2-overview.md:1049) |
| T1689-0def8626 | docs/dev/roadmap/v0.2-overview.md | 1686 | - [ ] T1054-6800 T1156-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) (docs/dev/roadmap/v0.2-overview.md:1050) |
| T1690-e717d0d4 | docs/dev/roadmap/v0.2-overview.md | 1687 | - [ ] T1055-3263 T1157-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) (docs/dev/roadmap/v0.2-overview.md:1051) |
| T1691-9968e85f | docs/dev/roadmap/v0.2-overview.md | 1688 | - [ ] T1056-56e6 T1158-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) (docs/dev/roadmap/v0.2-overview.md:1052) |
| T1692-f43e16e2 | docs/dev/roadmap/v0.2-overview.md | 1689 | - [ ] T1057-7567 T1159-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) (docs/dev/roadmap/v0.2-overview.md:1053) |
| T1693-5593c8ff | docs/dev/roadmap/v0.2-overview.md | 1690 | - [ ] T1058-4194 T1160-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) (docs/dev/roadmap/v0.2-overview.md:1054) |
| T1694-4d037ee0 | docs/dev/roadmap/v0.2-overview.md | 1691 | - [ ] T1059-b186 T1161-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) (docs/dev/roadmap/v0.2-overview.md:1055) |
| T1695-f8c6978c | docs/dev/roadmap/v0.2-overview.md | 1692 | - [ ] T1060-8db7 T1162-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) (docs/dev/roadmap/v0.2-overview.md:1056) |
| T1696-5f8b7824 | docs/dev/roadmap/v0.2-overview.md | 1693 | - [ ] T2479-49f1 TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T1697-aacbcd04 | docs/dev/roadmap/v0.2-overview.md | 1694 | - [ ] T2480-32c8 ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:186) |
| T1698-2b0ac285 | docs/dev/roadmap/v0.2-overview.md | 1695 | - [ ] T2481-b2f3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:233) |
| T1699-152e8caa | docs/dev/roadmap/v0.2-overview.md | 1696 | - [ ] T2482-ba97 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:236) |
| T1700-75941445 | docs/dev/roadmap/v0.2-overview.md | 1697 | - [ ] T2483-f6a2 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:276) |
| T1701-62b2f835 | docs/dev/roadmap/v0.2-overview.md | 1698 | - [ ] T2484-7bc9 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:288) |
| T1702-7bcad4e8 | docs/dev/roadmap/v0.2-overview.md | 1699 | - [ ] T2485-7fda # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T1703-a854341a | docs/dev/roadmap/v0.2-overview.md | 1700 | - [ ] T2486-96c6 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T1704-5db1c509 | docs/dev/roadmap/v0.2-overview.md | 1701 | - [ ] T2487-6b53 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T1705-ea5a0593 | docs/dev/roadmap/v0.2-overview.md | 1702 | - [ ] T2488-daa2 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T1706-34753aa9 | docs/dev/roadmap/v0.2-overview.md | 1703 | - [ ] T2489-f9c4 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T1707-a3ba3b57 | docs/dev/roadmap/v0.2-overview.md | 1704 | - [ ] T2490-4020 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T1708-69ba942a | docs/dev/roadmap/v0.2-overview.md | 1705 | - [ ] T2491-6751 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T1709-6d9201df | docs/dev/roadmap/v0.2-overview.md | 1706 | - [ ] T2492-af05 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T1710-7e9f4d2a | docs/dev/roadmap/v0.2-overview.md | 1707 | - [ ] T2493-59b8 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T1711-19fef475 | docs/dev/roadmap/v0.2-overview.md | 1708 | - [ ] T2494-67ad **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T1712-5d3061d2 | docs/dev/roadmap/v0.2-overview.md | 1709 | - [ ] T2495-b2f1 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T1713-7cbb0705 | docs/dev/roadmap/v0.2-overview.md | 1710 | - [ ] T2496-5835 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T1714-304b1ec9 | docs/dev/roadmap/v0.2-overview.md | 1711 | - [ ] T2497-d447 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T1715-2706e01f | docs/dev/roadmap/v0.2-overview.md | 1712 | - [ ] T2498-b65a **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T1716-5eeb41e2 | docs/dev/roadmap/v0.2-overview.md | 1713 | - [ ] T2499-55a9 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T1717-7196c1db | docs/dev/roadmap/v0.2-overview.md | 1714 | - [ ] T2500-691f **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T1718-434cfece | docs/dev/roadmap/v0.2-overview.md | 1715 | - [ ] T2501-820c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T1719-1a690a8c | docs/dev/roadmap/v0.2-overview.md | 1716 | - [ ] T2502-712e **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T1720-423fd789 | docs/dev/roadmap/v0.2-overview.md | 1717 | - [ ] T2503-2b97 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T1721-35f732a0 | docs/dev/roadmap/v0.2-overview.md | 1718 | - [ ] T2504-cb63 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T1722-1469b8db | docs/dev/roadmap/v0.2-overview.md | 1719 | - [ ] T2505-3943 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T1723-f8b9b774 | docs/dev/roadmap/v0.2-overview.md | 1720 | - [ ] T2506-2398 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T1724-54a00ffc | docs/dev/roadmap/v0.2-overview.md | 1721 | - [ ] T2507-1740 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T1725-8a5dd63f | docs/dev/roadmap/v0.2-overview.md | 1722 | - [ ] T2508-9abc **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T1726-0dcf91af | docs/dev/roadmap/v0.2-overview.md | 1723 | - [ ] T2509-23ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T1727-5a2af85e | docs/dev/roadmap/v0.2-overview.md | 1724 | - [ ] T2510-c222 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T1728-a88759ee | docs/dev/roadmap/v0.2-overview.md | 1725 | - [ ] T2511-937e **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T1729-9df1b6d9 | docs/dev/roadmap/v0.2-overview.md | 1726 | - [ ] T2512-bb52 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T1730-f76f51a3 | docs/dev/roadmap/v0.2-overview.md | 1727 | - [ ] T2513-8977 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T1731-5eb08bcd | docs/dev/roadmap/v0.2-overview.md | 1728 | - [ ] T2514-fcc1 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T1732-62dc6541 | docs/dev/roadmap/v0.2-overview.md | 1729 | - [ ] T2515-6700 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T1733-7023a8b1 | docs/dev/roadmap/v0.2-overview.md | 1730 | - [ ] T2516-7bb0 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T1734-6f8cfaec | docs/dev/roadmap/v0.2-overview.md | 1731 | - [ ] T2517-aa57 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T1735-30b1f10a | docs/dev/roadmap/v0.2-overview.md | 1732 | - [ ] T2518-2d51 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T1736-5da749cd | docs/dev/roadmap/v0.2-overview.md | 1733 | - [ ] T2519-41cc **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T1737-41a864e6 | docs/dev/roadmap/v0.2-overview.md | 1734 | - [ ] T2520-b872 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T1738-333434dc | docs/dev/roadmap/v0.2-overview.md | 1735 | - [ ] T2521-d2c7 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T1739-59a5b597 | docs/dev/roadmap/v0.2-overview.md | 1736 | - [ ] T2522-2f80 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T1740-42c52e25 | docs/dev/roadmap/v0.2-overview.md | 1737 | - [ ] T2523-538c **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T1741-83b33626 | docs/dev/roadmap/v0.2-overview.md | 1738 | - [ ] T2524-4cbb **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T1742-a43e4f40 | docs/dev/roadmap/v0.2-overview.md | 1739 | - [ ] T2525-a931 **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T1743-5bb38d4c | docs/dev/roadmap/v0.2-overview.md | 1740 | - [ ] T2526-f81c **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T1744-42c4e102 | docs/dev/roadmap/v0.2-overview.md | 1741 | - [ ] T2527-a2ff **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T1745-52d51243 | docs/dev/roadmap/v0.2-overview.md | 1742 | - [ ] T2528-edef **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T1746-1bf7aab3 | docs/dev/roadmap/v0.2-overview.md | 1743 | - [ ] T2529-0551 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T1747-b9ac9c8a | docs/dev/roadmap/v0.2-overview.md | 1744 | - [ ] T2530-2792 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T1748-9f20cc26 | docs/dev/roadmap/v0.2-overview.md | 1745 | - [ ] T2531-6703 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T1749-17a2266c | docs/dev/roadmap/v0.2-overview.md | 1746 | - [ ] T2532-83fe **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T1750-f1ece045 | docs/dev/roadmap/v0.2-overview.md | 1747 | - [ ] T2533-2296 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T1751-18b5960d | docs/dev/roadmap/v0.2-overview.md | 1748 | - [ ] T2535-bb75 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T1752-ff44f219 | docs/dev/roadmap/v0.2-overview.md | 1749 | - [ ] T2536-b21c **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T1753-ab10f5a9 | docs/dev/roadmap/v0.2-overview.md | 1750 | - [ ] T2537-858d **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T1754-86acbcb6 | docs/dev/roadmap/v0.2-overview.md | 1751 | - [ ] T2538-fa9a **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T1755-6c150004 | docs/dev/roadmap/v0.2-overview.md | 1752 | - [ ] T2539-e9a6 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T1756-f7e5d171 | docs/dev/roadmap/v0.2-overview.md | 1753 | - [ ] T2540-12a4 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T1757-6edd6d0a | docs/dev/roadmap/v0.2-overview.md | 1754 | - [ ] T2541-6a23 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T1758-a886c1ba | docs/dev/roadmap/v0.2-overview.md | 1755 | - [ ] T2542-50df **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T1759-a4b5a198 | docs/dev/roadmap/v0.2-overview.md | 1756 | - [ ] T2543-e417 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T1760-103c8712 | docs/dev/roadmap/v0.2-overview.md | 1757 | - [ ] T2544-7686 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T1761-703b9314 | docs/dev/roadmap/v0.2-overview.md | 1758 | - [ ] T2545-0902 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T1762-f0b90601 | docs/dev/roadmap/v0.2-overview.md | 1759 | - [ ] T2546-312b **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T1763-d24dfa35 | docs/dev/roadmap/v0.2-overview.md | 1760 | - [ ] T2547-486e **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T1764-72ac5f97 | docs/dev/roadmap/v0.2-overview.md | 1761 | - [ ] T2548-1fb0 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T1765-287d9249 | docs/dev/roadmap/v0.2-overview.md | 1762 | - [ ] T2549-e046 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T1766-fc964b6f | docs/dev/roadmap/v0.2-overview.md | 1763 | - [ ] T2550-16c0 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T1767-5314ff61 | docs/dev/roadmap/v0.2-overview.md | 1764 | - [ ] T2551-07d9 **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T1768-f80a8be7 | docs/dev/roadmap/v0.2-overview.md | 1765 | - [ ] T2552-120d **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T1769-b28c5c36 | docs/dev/roadmap/v0.2-overview.md | 1766 | - [ ] T2553-37a4 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T1770-e3353927 | docs/dev/roadmap/v0.2-overview.md | 1767 | - [ ] T2554-f6f0 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T1771-88120835 | docs/dev/roadmap/v0.2-overview.md | 1768 | - [ ] T2555-f47e **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T1772-cc02a2ae | docs/dev/roadmap/v0.2-overview.md | 1769 | - [ ] T2556-1e77 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T1773-b5dc36ab | docs/dev/roadmap/v0.2-overview.md | 1770 | - [ ] T2557-7fb2 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T1774-6f11aa05 | docs/dev/roadmap/v0.2-overview.md | 1771 | - [ ] T2558-1c9c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T1775-ab32f84d | docs/dev/roadmap/v0.2-overview.md | 1772 | - [ ] T2559-2fc5 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T1776-b66d5ce5 | docs/dev/roadmap/v0.2-overview.md | 1773 | - [ ] T2560-5950 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T1777-34d7a34e | docs/dev/roadmap/v0.2-overview.md | 1774 | - [ ] T2561-1e61 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T1778-c7405579 | docs/dev/roadmap/v0.2-overview.md | 1775 | - [ ] T2562-3e09 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T1779-60705b12 | docs/dev/roadmap/v0.2-overview.md | 1776 | - [ ] T2563-df0f **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T1780-767d7d2d | docs/dev/roadmap/v0.2-overview.md | 1777 | - [ ] T2564-f079 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T1781-2941c11a | docs/dev/roadmap/v0.2-overview.md | 1778 | - [ ] T2565-5ad2 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T1782-21cf9aa2 | docs/dev/roadmap/v0.2-overview.md | 1779 | - [ ] T2566-0c05 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T1783-8ade4011 | docs/dev/roadmap/v0.2-overview.md | 1780 | - [ ] T2567-6a13 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T1784-559911bb | docs/dev/roadmap/v0.2-overview.md | 1781 | - [ ] T2568-2a9e **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T1785-07409c29 | docs/dev/roadmap/v0.2-overview.md | 1782 | - [ ] T2569-c3e7 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T1786-1a58e095 | docs/dev/roadmap/v0.2-overview.md | 1783 | - [ ] T2570-3c74 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T1787-6c0df2bc | docs/dev/roadmap/v0.2-overview.md | 1784 | - [ ] T2571-8638 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T1788-4c05a929 | docs/dev/roadmap/v0.2-overview.md | 1785 | - [ ] T2572-f1eb **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T1789-d34e26ea | docs/dev/roadmap/v0.2-overview.md | 1786 | - [ ] T2573-ef38 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T1790-98dad676 | docs/dev/roadmap/v0.2-overview.md | 1787 | - [ ] T2574-2c4e **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T1791-d802f686 | docs/dev/roadmap/v0.2-overview.md | 1788 | - [ ] T2575-260e **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T1792-8246edd5 | docs/dev/roadmap/v0.2-overview.md | 1789 | - [ ] T2576-cf39 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T1793-c54a59c4 | docs/dev/roadmap/v0.2-overview.md | 1790 | - [ ] T2577-c292 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T1794-44dc0373 | docs/dev/roadmap/v0.2-overview.md | 1791 | - [ ] T2578-99a5 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T1795-a549bf22 | docs/dev/roadmap/v0.2-overview.md | 1792 | - [ ] T2579-bd7b **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T1796-06d099c5 | docs/dev/roadmap/v0.2-overview.md | 1793 | - [ ] T2580-fd8d **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T1797-446162b3 | docs/dev/roadmap/v0.2-overview.md | 1794 | - [ ] T2581-fe9c **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T1798-d26d8d3c | docs/dev/roadmap/v0.2-overview.md | 1795 | - [ ] T2582-fb88 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T1799-6e568a7f | docs/dev/roadmap/v0.2-overview.md | 1796 | - [ ] T2583-930a **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T1800-dc818199 | docs/dev/roadmap/v0.2-overview.md | 1797 | - [ ] T2584-4371 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T1801-fb07331d | docs/dev/roadmap/v0.2-overview.md | 1798 | - [ ] T2585-a124 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T1802-c93d29e9 | docs/dev/roadmap/v0.2-overview.md | 1799 | - [ ] T2586-8031 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T1803-25829e0b | docs/dev/roadmap/v0.2-overview.md | 1800 | - [ ] T2587-4e3a **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T1804-c6d4cb2e | docs/dev/roadmap/v0.2-overview.md | 1801 | - [ ] T2588-2ecc **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T1805-74f567ba | docs/dev/roadmap/v0.2-overview.md | 1802 | - [ ] T2589-2e7e **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T1806-539567c4 | docs/dev/roadmap/v0.2-overview.md | 1803 | - [ ] T2590-f5ef **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T1807-2b5f3d77 | docs/dev/roadmap/v0.2-overview.md | 1804 | - [ ] T2591-8249 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T1808-1805b747 | docs/dev/roadmap/v0.2-overview.md | 1805 | - [ ] T2592-5343 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T1809-17d8c378 | docs/dev/roadmap/v0.2-overview.md | 1806 | - [ ] T2593-f471 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T1810-c23f60fb | docs/dev/roadmap/v0.2-overview.md | 1807 | - [ ] T2594-2e62 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T1811-c5973a4e | docs/dev/roadmap/v0.2-overview.md | 1808 | - [ ] T2595-7965 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T1812-cf615c7a | docs/dev/roadmap/v0.2-overview.md | 1809 | - [ ] T2596-361b **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T1813-48100655 | docs/dev/roadmap/v0.2-overview.md | 1810 | - [ ] T2597-5733 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T1814-fc8c2ff0 | docs/dev/roadmap/v0.2-overview.md | 1811 | - [ ] T2598-3f9b **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T1815-d6a82dfb | docs/dev/roadmap/v0.2-overview.md | 1812 | - [ ] T2599-b3a4 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T1816-d61c020d | docs/dev/roadmap/v0.2-overview.md | 1813 | - [ ] T2600-3d06 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T1817-8b27f654 | docs/dev/roadmap/v0.2-overview.md | 1814 | - [ ] T2601-9f55 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T1818-8c9d3180 | docs/dev/roadmap/v0.2-overview.md | 1815 | - [ ] T2602-5754 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T1819-ebf88aa5 | docs/dev/roadmap/v0.2-overview.md | 1816 | - [ ] T2603-5b96 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T1820-49a6d197 | docs/dev/roadmap/v0.2-overview.md | 1817 | - [ ] T2604-33e5 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T1821-c35d1407 | docs/dev/roadmap/v0.2-overview.md | 1818 | - [ ] T2605-a3e0 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T1822-aaaeb79e | docs/dev/roadmap/v0.2-overview.md | 1819 | - [ ] T2606-61ea **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T1823-56313a99 | docs/dev/roadmap/v0.2-overview.md | 1820 | - [ ] T2607-916b **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T1824-e5db3355 | docs/dev/roadmap/v0.2-overview.md | 1821 | - [ ] T2608-4960 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T1825-9690d788 | docs/dev/roadmap/v0.2-overview.md | 1822 | - [ ] T2609-8ca4 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T1826-059b2c4f | docs/dev/roadmap/v0.2-overview.md | 1823 | - [ ] T2610-7ca5 **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T1827-da7d8e51 | docs/dev/roadmap/v0.2-overview.md | 1824 | - [ ] T2611-0356 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T1828-edbcfcca | docs/dev/roadmap/v0.2-overview.md | 1825 | - [ ] T2612-212d **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T1829-3f6133fd | docs/dev/roadmap/v0.2-overview.md | 1826 | - [ ] T2614-4657 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T1830-c9e056ff | docs/dev/roadmap/v0.2-overview.md | 1827 | - [ ] T2615-cddb **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T1831-e68aece8 | docs/dev/roadmap/v0.2-overview.md | 1828 | - [ ] T2616-f7bd **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T1832-32a55c39 | docs/dev/roadmap/v0.2-overview.md | 1829 | - [ ] T2617-5a2d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T1833-10e682c1 | docs/dev/roadmap/v0.2-overview.md | 1830 | - [ ] T2618-d15b **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T1834-437ce1bd | docs/dev/roadmap/v0.2-overview.md | 1831 | - [ ] T2619-0844 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T1835-c64729b2 | docs/dev/roadmap/v0.2-overview.md | 1832 | - [ ] T2620-d223 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T1836-a6a5c109 | docs/dev/roadmap/v0.2-overview.md | 1833 | - [ ] T2621-9bd6 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T1837-9756e848 | docs/dev/roadmap/v0.2-overview.md | 1834 | - [ ] T2622-9b01 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T1838-65a97b64 | docs/dev/roadmap/v0.2-overview.md | 1835 | - [ ] T2623-98e9 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T1839-c887da2c | docs/dev/roadmap/v0.2-overview.md | 1836 | - [ ] T2624-65a0 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T1840-8f574626 | docs/dev/roadmap/v0.2-overview.md | 1837 | - [ ] T2625-bf0a **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T1841-ea3f4424 | docs/dev/roadmap/v0.2-overview.md | 1838 | - [ ] T2626-c7b2 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T1842-316b65e2 | docs/dev/roadmap/v0.2-overview.md | 1839 | - [ ] T2627-a895 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T1843-69aa6d07 | docs/dev/roadmap/v0.2-overview.md | 1840 | - [ ] T2628-80a2 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T1844-e0bcc559 | docs/dev/roadmap/v0.2-overview.md | 1841 | - [ ] T2629-2c6a **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T1845-937424b1 | docs/dev/roadmap/v0.2-overview.md | 1842 | - [ ] T2630-1030 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T1846-8210047b | docs/dev/roadmap/v0.2-overview.md | 1843 | - [ ] T2631-3c05 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T1847-17b07ed0 | docs/dev/roadmap/v0.2-overview.md | 1844 | - [ ] T2632-7e80 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T1848-e50e8566 | docs/dev/roadmap/v0.2-overview.md | 1845 | - [ ] T2633-d255 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T1849-2b6b7496 | docs/dev/roadmap/v0.2-overview.md | 1846 | - [ ] T2634-041e **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T1850-91dc365c | docs/dev/roadmap/v0.2-overview.md | 1847 | - [ ] T2635-fd93 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T1851-9b7cb715 | docs/dev/roadmap/v0.2-overview.md | 1848 | - [ ] T2636-3c21 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T1852-eb3c6fbd | docs/dev/roadmap/v0.2-overview.md | 1849 | - [ ] T2637-41fe **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T1853-6d958cae | docs/dev/roadmap/v0.2-overview.md | 1850 | - [ ] T2638-9e56 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T1854-c9f2a87f | docs/dev/roadmap/v0.2-overview.md | 1851 | - [ ] T2639-3721 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T1855-22c05f59 | docs/dev/roadmap/v0.2-overview.md | 1852 | - [ ] T2640-66bd **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T1856-a3da325f | docs/dev/roadmap/v0.2-overview.md | 1853 | - [ ] T2641-6e54 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T1857-0800dc8f | docs/dev/roadmap/v0.2-overview.md | 1854 | - [ ] T2642-c05d **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T1858-6097aa5b | docs/dev/roadmap/v0.2-overview.md | 1855 | - [ ] T2643-0998 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T1859-a56883e3 | docs/dev/roadmap/v0.2-overview.md | 1856 | - [ ] T2644-7ca3 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T1860-064c2185 | docs/dev/roadmap/v0.2-overview.md | 1857 | - [ ] T2645-bfd4 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T1861-9a3e225b | docs/dev/roadmap/v0.2-overview.md | 1858 | - [ ] T2646-6ecc **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T1862-b76eb1b2 | docs/dev/roadmap/v0.2-overview.md | 1859 | - [ ] T2647-7ca7 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T1863-d96faac0 | docs/dev/roadmap/v0.2-overview.md | 1860 | - [ ] T2648-1b1d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T1864-3082459a | docs/dev/roadmap/v0.2-overview.md | 1861 | - [ ] T2649-e05d **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T1865-6b16f78a | docs/dev/roadmap/v0.2-overview.md | 1862 | - [ ] T2650-2ffc **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T1866-9a79a25c | docs/dev/roadmap/v0.2-overview.md | 1863 | - [ ] T2651-45fd **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T1867-98e9b37a | docs/dev/roadmap/v0.2-overview.md | 1864 | - [ ] T2652-0b8d **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T1868-0fdcd816 | docs/dev/roadmap/v0.2-overview.md | 1865 | - [ ] T2653-a0c3 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T1869-ce7a7e32 | docs/dev/roadmap/v0.2-overview.md | 1866 | - [ ] T2654-3f86 **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T1870-40e39946 | docs/dev/roadmap/v0.2-overview.md | 1867 | - [ ] T2655-6b86 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T1871-f900deab | docs/dev/roadmap/v0.2-overview.md | 1868 | - [ ] T2656-1d77 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T1872-5a2facea | docs/dev/roadmap/v0.2-overview.md | 1869 | - [ ] T2657-0c39 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T1873-7a2b52ae | docs/dev/roadmap/v0.2-overview.md | 1870 | - [ ] T2658-2ef3 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T1874-c30147b8 | docs/dev/roadmap/v0.2-overview.md | 1871 | - [ ] T2659-fc5e **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T1875-df4a52e2 | docs/dev/roadmap/v0.2-overview.md | 1872 | - [ ] T2660-51d4 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T1876-096a4973 | docs/dev/roadmap/v0.2-overview.md | 1873 | - [ ] T2661-153d **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T1877-20cc84c8 | docs/dev/roadmap/v0.2-overview.md | 1874 | - [ ] T2662-ddc6 **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T1878-61d0dee8 | docs/dev/roadmap/v0.2-overview.md | 1875 | - [ ] T2663-ac36 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T1879-083d64cd | docs/dev/roadmap/v0.2-overview.md | 1876 | - [ ] T2664-a931 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T1880-2ebdde25 | docs/dev/roadmap/v0.2-overview.md | 1877 | - [ ] T2665-372c **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T1881-919bb680 | docs/dev/roadmap/v0.2-overview.md | 1878 | - [ ] T2666-fd4e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T1882-5ba28c73 | docs/dev/roadmap/v0.2-overview.md | 1879 | - [ ] T2667-8215 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T1883-57eeb716 | docs/dev/roadmap/v0.2-overview.md | 1880 | - [ ] T2668-7ca1 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T1884-4801bf0d | docs/dev/roadmap/v0.2-overview.md | 1881 | - [ ] T2669-1981 **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T1885-378d0b0a | docs/dev/roadmap/v0.2-overview.md | 1882 | - [ ] T2670-1576 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T1886-39c2ea1f | docs/dev/roadmap/v0.2-overview.md | 1883 | - [ ] T2672-8604 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T1887-70420d95 | docs/dev/roadmap/v0.2-overview.md | 1884 | - [ ] T2673-c399 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T1888-e0125a01 | docs/dev/roadmap/v0.2-overview.md | 1885 | - [ ] T2674-106b **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T1889-b0103cef | docs/dev/roadmap/v0.2-overview.md | 1886 | - [ ] T2675-d37d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T1890-fdcc4230 | docs/dev/roadmap/v0.2-overview.md | 1887 | - [ ] T2676-9334 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T1891-97cbf6d5 | docs/dev/roadmap/v0.2-overview.md | 1888 | - [ ] T2677-0715 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T1892-f3950c7c | docs/dev/roadmap/v0.2-overview.md | 1889 | - [ ] T2678-c658 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T1893-3aa34bf9 | docs/dev/roadmap/v0.2-overview.md | 1890 | - [ ] T2679-8b2d **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T1894-6a1d8005 | docs/dev/roadmap/v0.2-overview.md | 1891 | - [ ] T2680-7db0 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T1895-a231c8d5 | docs/dev/roadmap/v0.2-overview.md | 1892 | - [ ] T2681-16e2 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T1896-4f19420f | docs/dev/roadmap/v0.2-overview.md | 1893 | - [ ] T2682-92b0 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T1897-de248626 | docs/dev/roadmap/v0.2-overview.md | 1894 | - [ ] T2683-4020 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T1898-2e0e8212 | docs/dev/roadmap/v0.2-overview.md | 1895 | - [ ] T2684-d4f1 **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T1899-790a1a17 | docs/dev/roadmap/v0.2-overview.md | 1896 | - [ ] T2685-f488 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T1900-086e3b39 | docs/dev/roadmap/v0.2-overview.md | 1897 | - [ ] T2686-446f **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T1901-9cdfaee7 | docs/dev/roadmap/v0.2-overview.md | 1898 | - [ ] T2687-31b9 **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T1902-43aaea78 | docs/dev/roadmap/v0.2-overview.md | 1899 | - [ ] T2688-dbcf **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T1903-c6f061c7 | docs/dev/roadmap/v0.2-overview.md | 1900 | - [ ] T2689-8ce4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T1904-d386a007 | docs/dev/roadmap/v0.2-overview.md | 1901 | - [ ] T2690-99a1 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T1905-9b6aed55 | docs/dev/roadmap/v0.2-overview.md | 1902 | - [ ] T2691-a791 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T1906-ad3466e1 | docs/dev/roadmap/v0.2-overview.md | 1903 | - [ ] T2692-7d18 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T1907-2172c1c8 | docs/dev/roadmap/v0.2-overview.md | 1904 | - [ ] T2693-d21d **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T1908-67805af9 | docs/dev/roadmap/v0.2-overview.md | 1905 | - [ ] T2694-2238 **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T1909-e8972b80 | docs/dev/roadmap/v0.2-overview.md | 1906 | - [ ] T2695-6bc3 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T1910-45deb6a0 | docs/dev/roadmap/v0.2-overview.md | 1907 | - [ ] T2696-a4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T1911-7620a184 | docs/dev/roadmap/v0.2-overview.md | 1908 | - [ ] T2697-1c33 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T1912-c933ee62 | docs/dev/roadmap/v0.2-overview.md | 1909 | - [ ] T2698-a6b4 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T1913-90a5fc4b | docs/dev/roadmap/v0.2-overview.md | 1910 | - [ ] T2699-8b5f **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T1914-0b316300 | docs/dev/roadmap/v0.2-overview.md | 1911 | - [ ] T2700-180b **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T1915-7926d635 | docs/dev/roadmap/v0.2-overview.md | 1912 | - [ ] T2701-c4b9 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T1916-ff97b44e | docs/dev/roadmap/v0.2-overview.md | 1913 | - [ ] T2702-77fd **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T1917-9f25ed17 | docs/dev/roadmap/v0.2-overview.md | 1914 | - [ ] T2703-ce13 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T1918-bb526915 | docs/dev/roadmap/v0.2-overview.md | 1915 | - [ ] T2704-69fa **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T1919-be6a24d8 | docs/dev/roadmap/v0.2-overview.md | 1916 | - [ ] T2705-f3ee **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T1920-32755cfc | docs/dev/roadmap/v0.2-overview.md | 1917 | - [ ] T2706-14e5 **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T1921-ed5c208e | docs/dev/roadmap/v0.2-overview.md | 1918 | - [ ] T2707-4ead **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T1922-e620b7a9 | docs/dev/roadmap/v0.2-overview.md | 1919 | - [ ] T2708-2047 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T1923-76cc4308 | docs/dev/roadmap/v0.2-overview.md | 1920 | - [ ] T2709-6762 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T1924-5711c56b | docs/dev/roadmap/v0.2-overview.md | 1921 | - [ ] T2710-2e6c **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T1925-95be524e | docs/dev/roadmap/v0.2-overview.md | 1922 | - [ ] T2711-f1e0 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T1926-a9ed5d70 | docs/dev/roadmap/v0.2-overview.md | 1923 | - [ ] T2712-4708 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T1927-181afbe6 | docs/dev/roadmap/v0.2-overview.md | 1924 | - [ ] T2713-31fc **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T1928-3aa44f1d | docs/dev/roadmap/v0.2-overview.md | 1925 | - [ ] T2714-4f04 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T1929-65165402 | docs/dev/roadmap/v0.2-overview.md | 1926 | - [ ] T2715-9568 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T1930-bc271d6a | docs/dev/roadmap/v0.2-overview.md | 1927 | - [ ] T2716-b1c0 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T1931-58b421b7 | docs/dev/roadmap/v0.2-overview.md | 1928 | - [ ] T2717-1dcd **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T1932-dd342e0a | docs/dev/roadmap/v0.2-overview.md | 1929 | - [ ] T2718-46c1 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T1933-e58af03b | docs/dev/roadmap/v0.2-overview.md | 1930 | - [ ] T2719-a533 **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T1934-294fa5be | docs/dev/roadmap/v0.2-overview.md | 1931 | - [ ] T2720-bb7e **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T1935-d8d32d65 | docs/dev/roadmap/v0.2-overview.md | 1932 | - [ ] T2721-50dc **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T1936-69ddac15 | docs/dev/roadmap/v0.2-overview.md | 1933 | - [ ] T2722-2a9c **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T1937-22cbe7fa | docs/dev/roadmap/v0.2-overview.md | 1934 | - [ ] T2723-08f6 **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T1938-58ba188a | docs/dev/roadmap/v0.2-overview.md | 1935 | - [ ] T2724-1d1b **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T1939-04e86720 | docs/dev/roadmap/v0.2-overview.md | 1936 | - [ ] T2725-a3cc **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T1940-11be022e | docs/dev/roadmap/v0.2-overview.md | 1937 | - [ ] T2726-fd36 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T1941-df403d47 | docs/dev/roadmap/v0.2-overview.md | 1938 | - [ ] T2727-3327 **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T1942-11708066 | docs/dev/roadmap/v0.2-overview.md | 1939 | - [ ] T2728-2069 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T1943-c1592654 | docs/dev/roadmap/v0.2-overview.md | 1940 | - [ ] T2729-c621 **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T1944-abe9ccea | docs/dev/roadmap/v0.2-overview.md | 1941 | - [ ] T2730-6ff2 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T1945-141f3115 | docs/dev/roadmap/v0.2-overview.md | 1942 | - [ ] T2731-67f7 **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T1946-c527f233 | docs/dev/roadmap/v0.2-overview.md | 1943 | - [ ] T2732-bf12 **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T1947-a41d490f | docs/dev/roadmap/v0.2-overview.md | 1944 | - [ ] T2733-aea2 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T1948-c2a1f4a9 | docs/dev/roadmap/v0.2-overview.md | 1945 | - [ ] T2734-1a1a **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T1949-a628e358 | docs/dev/roadmap/v0.2-overview.md | 1946 | - [ ] T2735-19f9 **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T1950-dd432de7 | docs/dev/roadmap/v0.2-overview.md | 1947 | - [ ] T2736-2ee2 **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T1951-f7a6fd1d | docs/dev/roadmap/v0.2-overview.md | 1948 | - [ ] T2737-2f84 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T1952-4135561b | docs/dev/roadmap/v0.2-overview.md | 1949 | - [ ] T2738-e37f **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T1953-468c8056 | docs/dev/roadmap/v0.2-overview.md | 1950 | - [ ] T2739-506b **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T1954-0f84f8cd | docs/dev/roadmap/v0.2-overview.md | 1951 | - [ ] T2740-2b4c **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T1955-3c9cde93 | docs/dev/roadmap/v0.2-overview.md | 1952 | - [ ] T2741-4c5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T1956-b0c8b014 | docs/dev/roadmap/v0.2-overview.md | 1953 | - [ ] T2742-592b **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T1957-18710f9b | docs/dev/roadmap/v0.2-overview.md | 1954 | - [ ] T2743-e6a5 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T1958-e8de37c2 | docs/dev/roadmap/v0.2-overview.md | 1955 | - [ ] T2744-dae0 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T1959-d1fbc9d3 | docs/dev/roadmap/v0.2-overview.md | 1956 | - [ ] T2745-d4b8 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T1960-f4de8bd5 | docs/dev/roadmap/v0.2-overview.md | 1957 | - [ ] T2746-1637 **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T1961-236253ea | docs/dev/roadmap/v0.2-overview.md | 1958 | - [ ] T2747-c7e3 **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T1962-39d25706 | docs/dev/roadmap/v0.2-overview.md | 1959 | - [ ] T2748-e2e1 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T1963-11affd38 | docs/dev/roadmap/v0.2-overview.md | 1960 | - [ ] T2749-ee18 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T1964-c28106a4 | docs/dev/roadmap/v0.2-overview.md | 1961 | - [ ] T2750-3fb5 **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T1965-ce8cc255 | docs/dev/roadmap/v0.2-overview.md | 1962 | - [ ] T2751-3a76 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T1966-d29c9cfe | docs/dev/roadmap/v0.2-overview.md | 1963 | - [ ] T2752-79ca **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T1967-012f6854 | docs/dev/roadmap/v0.2-overview.md | 1964 | - [ ] T2753-e066 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T1968-f7cad36b | docs/dev/roadmap/v0.2-overview.md | 1965 | - [ ] T2754-2bc7 **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T1969-56e27209 | docs/dev/roadmap/v0.2-overview.md | 1966 | - [ ] T2755-9331 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T1970-238476c2 | docs/dev/roadmap/v0.2-overview.md | 1967 | - [ ] T2756-1a7d **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T1971-c839006c | docs/dev/roadmap/v0.2-overview.md | 1968 | - [ ] T2757-b3f1 **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T1972-918aca7e | docs/dev/roadmap/v0.2-overview.md | 1969 | - [ ] T2758-27a1 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T1973-eb70d730 | docs/dev/roadmap/v0.2-overview.md | 1970 | - [ ] T2759-2298 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T1974-eff64882 | docs/dev/roadmap/v0.2-overview.md | 1971 | - [ ] T2760-a992 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T1975-35ee2863 | docs/dev/roadmap/v0.2-overview.md | 1972 | - [ ] T2761-556f **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T1976-654f9104 | docs/dev/roadmap/v0.2-overview.md | 1973 | - [ ] T2762-33d4 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T1977-9ddb61c1 | docs/dev/roadmap/v0.2-overview.md | 1974 | - [ ] T2763-28b2 **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T1978-ff186969 | docs/dev/roadmap/v0.2-overview.md | 1975 | - [ ] T2764-285e **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T1979-5abf0e41 | docs/dev/roadmap/v0.2-overview.md | 1976 | - [ ] T2765-e099 **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T1980-b2e8d5d3 | docs/dev/roadmap/v0.2-overview.md | 1977 | - [ ] T2766-7e5b **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T1981-131bcb96 | docs/dev/roadmap/v0.2-overview.md | 1978 | - [ ] T2767-9566 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T1982-6cd35dae | docs/dev/roadmap/v0.2-overview.md | 1979 | - [ ] T2768-9be3 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T1983-3502df0f | docs/dev/roadmap/v0.2-overview.md | 1980 | - [ ] T2769-0224 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T1984-46c2bdb7 | docs/dev/roadmap/v0.2-overview.md | 1981 | - [ ] T2770-72d2 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T1985-c67a343f | docs/dev/roadmap/v0.2-overview.md | 1982 | - [ ] T2771-b207 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T1986-87c081c0 | docs/dev/roadmap/v0.2-overview.md | 1983 | - [ ] T2772-2b54 **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T1987-2bbe620f | docs/dev/roadmap/v0.2-overview.md | 1984 | - [ ] T2773-626b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T1988-571c043b | docs/dev/roadmap/v0.2-overview.md | 1985 | - [ ] T2774-2501 **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T1989-24e3d872 | docs/dev/roadmap/v0.2-overview.md | 1986 | - [ ] T2775-589c **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T1990-9bda3afb | docs/dev/roadmap/v0.2-overview.md | 1987 | - [ ] T2776-695a **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T1991-3e3af23a | docs/dev/roadmap/v0.2-overview.md | 1988 | - [ ] T2777-376a **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T1992-3c9531d7 | docs/dev/roadmap/v0.2-overview.md | 1989 | - [ ] T2778-0a9f **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T1993-80dffc49 | docs/dev/roadmap/v0.2-overview.md | 1990 | - [ ] T2779-ba2e **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T1994-a0ff8ed6 | docs/dev/roadmap/v0.2-overview.md | 1991 | - [ ] T2780-4d93 **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T1995-8325e524 | docs/dev/roadmap/v0.2-overview.md | 1992 | - [ ] T2781-14dc **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T1996-37de9555 | docs/dev/roadmap/v0.2-overview.md | 1993 | - [ ] T2782-f3ec **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T1997-e5a6140f | docs/dev/roadmap/v0.2-overview.md | 1994 | - [ ] T2783-0cd0 **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T1998-4b1a8357 | docs/dev/roadmap/v0.2-overview.md | 1995 | - [ ] T2784-0bf6 **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T1999-2540ec29 | docs/dev/roadmap/v0.2-overview.md | 1996 | - [ ] T2785-df2a **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T2000-836e6530 | docs/dev/roadmap/v0.2-overview.md | 1997 | - [ ] T2786-6a5b **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T2001-62023f7c | docs/dev/roadmap/v0.2-overview.md | 1998 | - [ ] T2787-8739 **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T2002-b017cf6d | docs/dev/roadmap/v0.2-overview.md | 1999 | - [ ] T2788-0478 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T2003-9ea467d2 | docs/dev/roadmap/v0.2-overview.md | 2000 | - [ ] T2789-6ff5 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T2004-7d55c180 | docs/dev/roadmap/v0.2-overview.md | 2001 | - [ ] T2790-227c **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T2005-a802af2f | docs/dev/roadmap/v0.2-overview.md | 2002 | - [ ] T2791-d40a **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T2006-c5694f48 | docs/dev/roadmap/v0.2-overview.md | 2003 | - [ ] T2792-04f8 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T2007-51f261a4 | docs/dev/roadmap/v0.2-overview.md | 2004 | - [ ] T2793-72f7 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T2008-5b0b7c2c | docs/dev/roadmap/v0.2-overview.md | 2005 | - [ ] T2794-5a1c **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T2009-86292dba | docs/dev/roadmap/v0.2-overview.md | 2006 | - [ ] T2795-da3e **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T2010-0bbd8f9c | docs/dev/roadmap/v0.2-overview.md | 2007 | - [ ] T2796-4a5c **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T2011-d48eea45 | docs/dev/roadmap/v0.2-overview.md | 2008 | - [ ] T2797-abac **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T2012-dcd5e77c | docs/dev/roadmap/v0.2-overview.md | 2009 | - [ ] T2798-b3ad **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T2013-18761f0a | docs/dev/roadmap/v0.2-overview.md | 2010 | - [ ] T2799-829b **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T2014-a0eeef82 | docs/dev/roadmap/v0.2-overview.md | 2011 | - [ ] T0107-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T2015-0c4bda7f | docs/dev/roadmap/v0.2-overview.md | 2012 | - [ ] T0108-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T2016-6a8f2159 | docs/dev/roadmap/v0.2-overview.md | 2013 | - [ ] T0109-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T2017-da248ae4 | docs/dev/roadmap/v0.2-overview.md | 2014 | - [ ] T0110-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T2018-1a6949f2 | docs/dev/roadmap/v0.2-overview.md | 2015 | - [ ] T0111-94a1e0fc # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:185) |
| T2019-0041ac84 | docs/dev/roadmap/v0.2-overview.md | 2016 | - [ ] T0112-fcff12e0 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:192) |
| T2020-d5fc35ee | docs/dev/roadmap/v0.2-overview.md | 2017 | - [ ] T0113-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T2021-98b38817 | docs/dev/roadmap/v0.2-overview.md | 2018 | - [ ] T0114-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T2022-df0bd3b6 | docs/dev/roadmap/v0.2-overview.md | 2019 | - [ ] T0115-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T2023-74763886 | docs/dev/roadmap/v0.2-overview.md | 2020 | - [ ] T0116-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T2024-75b815c8 | docs/dev/roadmap/v0.2-overview.md | 2021 | - [ ] T0117-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T2025-23ec0db2 | docs/dev/roadmap/v0.2-overview.md | 2022 | - [ ] T0118-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T2026-f64ac7c0 | docs/dev/roadmap/v0.2-overview.md | 2023 | - [ ] T0119-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T2027-c073e28f | docs/dev/roadmap/v0.2-overview.md | 2024 | - [ ] T0120-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T2028-c459bd8c | docs/dev/roadmap/v0.2-overview.md | 2025 | - [ ] T0121-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T2029-48baf843 | docs/dev/roadmap/v0.2-overview.md | 2026 | - [ ] T0122-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T2030-8333f6c1 | docs/dev/roadmap/v0.2-overview.md | 2027 | - [ ] T0123-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T2031-5f6cc183 | docs/dev/roadmap/v0.2-overview.md | 2028 | - [ ] T0124-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T2032-651b9541 | docs/dev/roadmap/v0.2-overview.md | 2029 | - [ ] T0125-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T2033-d7780c9e | docs/dev/roadmap/v0.2-overview.md | 2030 | - [ ] T0126-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T2034-0cc4ff9c | docs/dev/roadmap/v0.2-overview.md | 2031 | - [ ] T0127-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T2035-547ba862 | docs/dev/roadmap/v0.2-overview.md | 2032 | - [ ] T0128-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T2036-20060473 | docs/dev/roadmap/v0.2-overview.md | 2033 | - [ ] T0129-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T2037-44fc770c | docs/dev/roadmap/v0.2-overview.md | 2034 | - [ ] T0130-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T2038-117958d5 | docs/dev/roadmap/v0.2-overview.md | 2035 | - [ ] T0131-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T2039-877c2169 | docs/dev/roadmap/v0.2-overview.md | 2036 | - [ ] T0132-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T2040-3b399507 | docs/dev/roadmap/v0.2-overview.md | 2037 | - [ ] T0133-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T2041-9c8ab5f1 | docs/dev/roadmap/v0.2-overview.md | 2038 | - [ ] T0134-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T2042-b485e0ba | docs/dev/roadmap/v0.2-overview.md | 2039 | - [ ] T0135-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T2043-76acad3f | docs/dev/roadmap/v0.2-overview.md | 2040 | - [ ] T0136-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T2044-9c92e305 | docs/dev/roadmap/v0.2-overview.md | 2041 | - [ ] T0137-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T2045-24b1a80d | docs/dev/roadmap/v0.2-overview.md | 2042 | - [ ] T0138-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T2046-d289d5ca | docs/dev/roadmap/v0.2-overview.md | 2043 | - [ ] T0139-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T2047-12da5bb2 | docs/dev/roadmap/v0.2-overview.md | 2044 | - [ ] T0140-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T2048-408c5948 | docs/dev/roadmap/v0.2-overview.md | 2045 | - [ ] T0141-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T2049-959d85a6 | docs/dev/roadmap/v0.2-overview.md | 2046 | - [ ] T0142-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T2050-eeb48d7b | docs/dev/roadmap/v0.2-overview.md | 2047 | - [ ] T0143-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T2051-d09eb708 | docs/dev/roadmap/v0.2-overview.md | 2048 | - [ ] T0144-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T2052-219c4241 | docs/dev/roadmap/v0.2-overview.md | 2049 | - [ ] T0145-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T2053-23af62cf | docs/dev/roadmap/v0.2-overview.md | 2050 | - [ ] T0146-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T2054-92f55135 | docs/dev/roadmap/v0.2-overview.md | 2051 | - [ ] T0147-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T2055-c88b825d | docs/dev/roadmap/v0.2-overview.md | 2052 | - [ ] T0148-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T2056-b8bbb269 | docs/dev/roadmap/v0.2-overview.md | 2053 | - [ ] T0149-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T2057-f453f21d | docs/dev/roadmap/v0.2-overview.md | 2054 | - [ ] T0150-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T2058-1fc22b03 | docs/dev/roadmap/v0.2-overview.md | 2055 | - [ ] T0151-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T2059-f80b95bd | docs/dev/roadmap/v0.2-overview.md | 2056 | - [ ] T0152-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T2060-f531b3ee | docs/dev/roadmap/v0.2-overview.md | 2057 | - [ ] T0153-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T2061-3e16e0de | docs/dev/roadmap/v0.2-overview.md | 2058 | - [ ] T0154-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T2062-4b4b5035 | docs/dev/roadmap/v0.2-overview.md | 2059 | - [ ] T0155-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T2063-43ed1b05 | docs/dev/roadmap/v0.2-overview.md | 2060 | - [ ] T0156-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T2064-b49f6ac3 | docs/dev/roadmap/v0.2-overview.md | 2061 | - [ ] T0157-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T2065-38ed7bef | docs/dev/roadmap/v0.2-overview.md | 2062 | - [ ] T0158-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T2066-795aa492 | docs/dev/roadmap/v0.2-overview.md | 2063 | - [ ] T0159-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T2067-51a48687 | docs/dev/roadmap/v0.2-overview.md | 2064 | - [ ] T0160-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T2068-081c9b02 | docs/dev/roadmap/v0.2-overview.md | 2065 | - [ ] T0161-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T2069-f8c44d3a | docs/dev/roadmap/v0.2-overview.md | 2066 | - [ ] T0163-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T2070-aa151f90 | docs/dev/roadmap/v0.2-overview.md | 2067 | - [ ] T0164-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T2071-4c5de1ef | docs/dev/roadmap/v0.2-overview.md | 2068 | - [ ] T0165-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T2072-5f861e05 | docs/dev/roadmap/v0.2-overview.md | 2069 | - [ ] T0166-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T2073-5c5c5677 | docs/dev/roadmap/v0.2-overview.md | 2070 | - [ ] T0167-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T2074-20958e71 | docs/dev/roadmap/v0.2-overview.md | 2071 | - [ ] T0168-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T2075-7a592488 | docs/dev/roadmap/v0.2-overview.md | 2072 | - [ ] T0169-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T2076-e51ef9e4 | docs/dev/roadmap/v0.2-overview.md | 2073 | - [ ] T0170-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T2077-907f87cf | docs/dev/roadmap/v0.2-overview.md | 2074 | - [ ] T0171-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T2078-24501ec8 | docs/dev/roadmap/v0.2-overview.md | 2075 | - [ ] T0172-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T2079-ae440a9a | docs/dev/roadmap/v0.2-overview.md | 2076 | - [ ] T0173-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T2080-c5105fe0 | docs/dev/roadmap/v0.2-overview.md | 2077 | - [ ] T0174-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T2081-087b934e | docs/dev/roadmap/v0.2-overview.md | 2078 | - [ ] T0175-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T2082-86db825d | docs/dev/roadmap/v0.2-overview.md | 2079 | - [ ] T0176-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T2083-5ae28f40 | docs/dev/roadmap/v0.2-overview.md | 2080 | - [ ] T0177-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T2084-dd64b6f0 | docs/dev/roadmap/v0.2-overview.md | 2081 | - [ ] T0178-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T2085-843fd13f | docs/dev/roadmap/v0.2-overview.md | 2082 | - [ ] T0179-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T2086-4522a6cf | docs/dev/roadmap/v0.2-overview.md | 2083 | - [ ] T0180-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T2087-f1e0eebd | docs/dev/roadmap/v0.2-overview.md | 2084 | - [ ] T0181-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T2088-6602e987 | docs/dev/roadmap/v0.2-overview.md | 2085 | - [ ] T0182-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T2089-eb1166a9 | docs/dev/roadmap/v0.2-overview.md | 2086 | - [ ] T0183-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T2090-328dd8b0 | docs/dev/roadmap/v0.2-overview.md | 2087 | - [ ] T0184-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T2091-fe2eb0d3 | docs/dev/roadmap/v0.2-overview.md | 2088 | - [ ] T0185-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T2092-df0cbd2a | docs/dev/roadmap/v0.2-overview.md | 2089 | - [ ] T0186-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T2093-89999bb0 | docs/dev/roadmap/v0.2-overview.md | 2090 | - [ ] T0187-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T2094-1301aea8 | docs/dev/roadmap/v0.2-overview.md | 2091 | - [ ] T0188-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T2095-5847a284 | docs/dev/roadmap/v0.2-overview.md | 2092 | - [ ] T0189-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T2096-cfb4512f | docs/dev/roadmap/v0.2-overview.md | 2093 | - [ ] T0190-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T2097-2911d8ca | docs/dev/roadmap/v0.2-overview.md | 2094 | - [ ] T0191-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T2098-7fc04707 | docs/dev/roadmap/v0.2-overview.md | 2095 | - [ ] T0192-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T2099-722b4a9b | docs/dev/roadmap/v0.2-overview.md | 2096 | - [ ] T0193-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T2100-788e7db6 | docs/dev/roadmap/v0.2-overview.md | 2097 | - [ ] T0194-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T2101-c3ae10c4 | docs/dev/roadmap/v0.2-overview.md | 2098 | - [ ] T0195-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T2102-40c37563 | docs/dev/roadmap/v0.2-overview.md | 2099 | - [ ] T0196-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T2103-46a51828 | docs/dev/roadmap/v0.2-overview.md | 2100 | - [ ] T0197-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T2104-a33fc663 | docs/dev/roadmap/v0.2-overview.md | 2101 | - [ ] T0198-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T2105-62f3100f | docs/dev/roadmap/v0.2-overview.md | 2102 | - [ ] T0199-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T2106-9ac30ff0 | docs/dev/roadmap/v0.2-overview.md | 2103 | - [ ] T0200-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T2107-170fecb7 | docs/dev/roadmap/v0.2-overview.md | 2104 | - [ ] T0201-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T2108-cdff119e | docs/dev/roadmap/v0.2-overview.md | 2105 | - [ ] T0202-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T2109-3165637a | docs/dev/roadmap/v0.2-overview.md | 2106 | - [ ] T0203-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T2110-c36cb0bd | docs/dev/roadmap/v0.2-overview.md | 2107 | - [ ] T0204-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T2111-2d041d8d | docs/dev/roadmap/v0.2-overview.md | 2108 | - [ ] T0205-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T2112-0f962d14 | docs/dev/roadmap/v0.2-overview.md | 2109 | - [ ] T0206-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T2113-435a9318 | docs/dev/roadmap/v0.2-overview.md | 2110 | - [ ] T0207-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T2114-9405ac6f | docs/dev/roadmap/v0.2-overview.md | 2111 | - [ ] T0208-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T2115-498c9875 | docs/dev/roadmap/v0.2-overview.md | 2112 | - [ ] T0209-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T2116-d299507d | docs/dev/roadmap/v0.2-overview.md | 2113 | - [ ] T0210-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T2117-3bd509e1 | docs/dev/roadmap/v0.2-overview.md | 2114 | - [ ] T0211-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T2118-ede5b76c | docs/dev/roadmap/v0.2-overview.md | 2115 | - [ ] T0212-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T2119-7d952656 | docs/dev/roadmap/v0.2-overview.md | 2116 | - [ ] T0213-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T2120-d9295ff5 | docs/dev/roadmap/v0.2-overview.md | 2117 | - [ ] T0214-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T2121-30d092bd | docs/dev/roadmap/v0.2-overview.md | 2118 | - [ ] T0215-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T2122-35c027ad | docs/dev/roadmap/v0.2-overview.md | 2119 | - [ ] T0216-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T2123-9bdd8b34 | docs/dev/roadmap/v0.2-overview.md | 2120 | - [ ] T0217-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T2124-e344a44e | docs/dev/roadmap/v0.2-overview.md | 2121 | - [ ] T0218-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T2125-657d255c | docs/dev/roadmap/v0.2-overview.md | 2122 | - [ ] T0219-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T2126-4837c37d | docs/dev/roadmap/v0.2-overview.md | 2123 | - [ ] T0220-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T2127-65f95bef | docs/dev/roadmap/v0.2-overview.md | 2124 | - [ ] T0221-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T2128-1dba8216 | docs/dev/roadmap/v0.2-overview.md | 2125 | - [ ] T0222-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T2129-4f68bf52 | docs/dev/roadmap/v0.2-overview.md | 2126 | - [ ] T0223-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T2130-6a9b4130 | docs/dev/roadmap/v0.2-overview.md | 2127 | - [ ] T0224-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T2131-579ada9f | docs/dev/roadmap/v0.2-overview.md | 2128 | - [ ] T0225-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T2132-b027f5ec | docs/dev/roadmap/v0.2-overview.md | 2129 | - [ ] T0226-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T2133-8583326c | docs/dev/roadmap/v0.2-overview.md | 2130 | - [ ] T0227-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T2134-0a6aef63 | docs/dev/roadmap/v0.2-overview.md | 2131 | - [ ] T0228-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T2135-ee5b015e | docs/dev/roadmap/v0.2-overview.md | 2132 | - [ ] T0229-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T2136-002ab23e | docs/dev/roadmap/v0.2-overview.md | 2133 | - [ ] T0230-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T2137-7676ffdc | docs/dev/roadmap/v0.2-overview.md | 2134 | - [ ] T0231-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T2138-95be0c61 | docs/dev/roadmap/v0.2-overview.md | 2135 | - [ ] T0232-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T2139-617b469e | docs/dev/roadmap/v0.2-overview.md | 2136 | - [ ] T0233-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T2140-ca542f18 | docs/dev/roadmap/v0.2-overview.md | 2137 | - [ ] T0234-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T2141-93ec4b0e | docs/dev/roadmap/v0.2-overview.md | 2138 | - [ ] T0235-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T2142-1ae19699 | docs/dev/roadmap/v0.2-overview.md | 2139 | - [ ] T0236-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T2143-a063883b | docs/dev/roadmap/v0.2-overview.md | 2140 | - [ ] T0237-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T2144-d4a68975 | docs/dev/roadmap/v0.2-overview.md | 2141 | - [ ] T0238-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T2145-18354b19 | docs/dev/roadmap/v0.2-overview.md | 2142 | - [ ] T0239-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T2146-90f974d2 | docs/dev/roadmap/v0.2-overview.md | 2143 | - [ ] T0240-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T2147-be8b94c7 | docs/dev/roadmap/v0.2-overview.md | 2144 | - [ ] T0242-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T2148-3dd16c79 | docs/dev/roadmap/v0.2-overview.md | 2145 | - [ ] T0243-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T2149-1c56fecc | docs/dev/roadmap/v0.2-overview.md | 2146 | - [ ] T0244-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T2150-d59fcca7 | docs/dev/roadmap/v0.2-overview.md | 2147 | - [ ] T0245-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T2151-accb9797 | docs/dev/roadmap/v0.2-overview.md | 2148 | - [ ] T0246-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T2152-b7fca439 | docs/dev/roadmap/v0.2-overview.md | 2149 | - [ ] T0247-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T2153-f5c1fe2b | docs/dev/roadmap/v0.2-overview.md | 2150 | - [ ] T0248-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T2154-9b9fbea5 | docs/dev/roadmap/v0.2-overview.md | 2151 | - [ ] T0249-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T2155-8b0b14b9 | docs/dev/roadmap/v0.2-overview.md | 2152 | - [ ] T0250-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T2156-6c85ae77 | docs/dev/roadmap/v0.2-overview.md | 2153 | - [ ] T0251-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T2157-da6eff36 | docs/dev/roadmap/v0.2-overview.md | 2154 | - [ ] T0252-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T2158-f3b26ae1 | docs/dev/roadmap/v0.2-overview.md | 2155 | - [ ] T0253-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T2159-5009b7e9 | docs/dev/roadmap/v0.2-overview.md | 2156 | - [ ] T0254-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T2160-5c784430 | docs/dev/roadmap/v0.2-overview.md | 2157 | - [ ] T0255-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T2161-cfae685c | docs/dev/roadmap/v0.2-overview.md | 2158 | - [ ] T0256-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T2162-8988a053 | docs/dev/roadmap/v0.2-overview.md | 2159 | - [ ] T0257-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T2163-08a83dbf | docs/dev/roadmap/v0.2-overview.md | 2160 | - [ ] T0258-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T2164-1c1927ba | docs/dev/roadmap/v0.2-overview.md | 2161 | - [ ] T0259-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T2165-3899e57f | docs/dev/roadmap/v0.2-overview.md | 2162 | - [ ] T0260-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T2166-4ef4d0a8 | docs/dev/roadmap/v0.2-overview.md | 2163 | - [ ] T0261-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T2167-b746fae0 | docs/dev/roadmap/v0.2-overview.md | 2164 | - [ ] T0262-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T2168-c0031c79 | docs/dev/roadmap/v0.2-overview.md | 2165 | - [ ] T0263-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T2169-badc546e | docs/dev/roadmap/v0.2-overview.md | 2166 | - [ ] T0264-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T2170-6f692880 | docs/dev/roadmap/v0.2-overview.md | 2167 | - [ ] T0265-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T2171-1ad66b65 | docs/dev/roadmap/v0.2-overview.md | 2168 | - [ ] T0266-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T2172-fd4c732a | docs/dev/roadmap/v0.2-overview.md | 2169 | - [ ] T0267-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T2173-83efc423 | docs/dev/roadmap/v0.2-overview.md | 2170 | - [ ] T0268-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T2174-a2029173 | docs/dev/roadmap/v0.2-overview.md | 2171 | - [ ] T0269-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T2175-114aad43 | docs/dev/roadmap/v0.2-overview.md | 2172 | - [ ] T0270-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T2176-1b320aac | docs/dev/roadmap/v0.2-overview.md | 2173 | - [ ] T0271-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T2177-0324e23b | docs/dev/roadmap/v0.2-overview.md | 2174 | - [ ] T0272-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T2178-775d9b83 | docs/dev/roadmap/v0.2-overview.md | 2175 | - [ ] T0273-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T2179-9d1e224b | docs/dev/roadmap/v0.2-overview.md | 2176 | - [ ] T0274-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T2180-8afbfe1b | docs/dev/roadmap/v0.2-overview.md | 2177 | - [ ] T0275-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T2181-dbfae59b | docs/dev/roadmap/v0.2-overview.md | 2178 | - [ ] T0276-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T2182-f448ba9b | docs/dev/roadmap/v0.2-overview.md | 2179 | - [ ] T0277-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T2183-5479c4a5 | docs/dev/roadmap/v0.2-overview.md | 2180 | - [ ] T0278-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T2184-e50f6b14 | docs/dev/roadmap/v0.2-overview.md | 2181 | - [ ] T0279-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T2185-dabb0c57 | docs/dev/roadmap/v0.2-overview.md | 2182 | - [ ] T0280-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T2186-e8030f58 | docs/dev/roadmap/v0.2-overview.md | 2183 | - [ ] T0281-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T2187-2bfbb4f3 | docs/dev/roadmap/v0.2-overview.md | 2184 | - [ ] T0282-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T2188-36bf0728 | docs/dev/roadmap/v0.2-overview.md | 2185 | - [ ] T0283-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T2189-f7d5fa5b | docs/dev/roadmap/v0.2-overview.md | 2186 | - [ ] T0284-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T2190-9d278440 | docs/dev/roadmap/v0.2-overview.md | 2187 | - [ ] T0285-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T2191-0cee0d08 | docs/dev/roadmap/v0.2-overview.md | 2188 | - [ ] T0286-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T2192-aa3916c1 | docs/dev/roadmap/v0.2-overview.md | 2189 | - [ ] T0287-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T2193-373a29ef | docs/dev/roadmap/v0.2-overview.md | 2190 | - [ ] T0288-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T2194-d0d89fd2 | docs/dev/roadmap/v0.2-overview.md | 2191 | - [ ] T0289-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T2195-de3649da | docs/dev/roadmap/v0.2-overview.md | 2192 | - [ ] T0290-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T2196-fa1f20fc | docs/dev/roadmap/v0.2-overview.md | 2193 | - [ ] T0291-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T2197-b88cfd6e | docs/dev/roadmap/v0.2-overview.md | 2194 | - [ ] T0292-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T2198-d5139494 | docs/dev/roadmap/v0.2-overview.md | 2195 | - [ ] T0293-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T2199-4f0dd4a2 | docs/dev/roadmap/v0.2-overview.md | 2196 | - [ ] T0294-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T2200-6e883e14 | docs/dev/roadmap/v0.2-overview.md | 2197 | - [ ] T0295-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T2201-0f88bc59 | docs/dev/roadmap/v0.2-overview.md | 2198 | - [ ] T0296-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T2202-f54259d7 | docs/dev/roadmap/v0.2-overview.md | 2199 | - [ ] T0297-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T2203-1db01b91 | docs/dev/roadmap/v0.2-overview.md | 2200 | - [ ] T0298-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T2204-f4649b88 | docs/dev/roadmap/v0.2-overview.md | 2201 | - [ ] T0300-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T2205-0c682b3c | docs/dev/roadmap/v0.2-overview.md | 2202 | - [ ] T0301-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T2206-66c39c1a | docs/dev/roadmap/v0.2-overview.md | 2203 | - [ ] T0302-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T2207-39c46134 | docs/dev/roadmap/v0.2-overview.md | 2204 | - [ ] T0303-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T2208-4da10bef | docs/dev/roadmap/v0.2-overview.md | 2205 | - [ ] T0304-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T2209-d53c82e5 | docs/dev/roadmap/v0.2-overview.md | 2206 | - [ ] T0305-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T2210-0bb78761 | docs/dev/roadmap/v0.2-overview.md | 2207 | - [ ] T0306-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T2211-253d4a6e | docs/dev/roadmap/v0.2-overview.md | 2208 | - [ ] T0307-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T2212-2aab196a | docs/dev/roadmap/v0.2-overview.md | 2209 | - [ ] T0308-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T2213-30547d7e | docs/dev/roadmap/v0.2-overview.md | 2210 | - [ ] T0309-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T2214-f10d728d | docs/dev/roadmap/v0.2-overview.md | 2211 | - [ ] T0310-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T2215-db81d782 | docs/dev/roadmap/v0.2-overview.md | 2212 | - [ ] T0311-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T2216-2a246e29 | docs/dev/roadmap/v0.2-overview.md | 2213 | - [ ] T0312-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T2217-d17c69ef | docs/dev/roadmap/v0.2-overview.md | 2214 | - [ ] T0313-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T2218-c7d7fc0c | docs/dev/roadmap/v0.2-overview.md | 2215 | - [ ] T0314-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T2219-6c2c8ca3 | docs/dev/roadmap/v0.2-overview.md | 2216 | - [ ] T0315-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T2220-0b3ef593 | docs/dev/roadmap/v0.2-overview.md | 2217 | - [ ] T0316-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T2221-3c53f264 | docs/dev/roadmap/v0.2-overview.md | 2218 | - [ ] T0317-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T2222-de765aca | docs/dev/roadmap/v0.2-overview.md | 2219 | - [ ] T0318-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T2223-12085bca | docs/dev/roadmap/v0.2-overview.md | 2220 | - [ ] T0319-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T2224-9a557558 | docs/dev/roadmap/v0.2-overview.md | 2221 | - [ ] T0320-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T2225-91cdfe74 | docs/dev/roadmap/v0.2-overview.md | 2222 | - [ ] T0321-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T2226-b82e3442 | docs/dev/roadmap/v0.2-overview.md | 2223 | - [ ] T0322-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T2227-fcffb0d3 | docs/dev/roadmap/v0.2-overview.md | 2224 | - [ ] T0323-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T2228-bdee76f3 | docs/dev/roadmap/v0.2-overview.md | 2225 | - [ ] T0324-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T2229-293b2f02 | docs/dev/roadmap/v0.2-overview.md | 2226 | - [ ] T0325-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T2230-8c2db115 | docs/dev/roadmap/v0.2-overview.md | 2227 | - [ ] T0326-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T2231-99b582f9 | docs/dev/roadmap/v0.2-overview.md | 2228 | - [ ] T0327-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T2232-6cb44cce | docs/dev/roadmap/v0.2-overview.md | 2229 | - [ ] T0328-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T2233-ceca8816 | docs/dev/roadmap/v0.2-overview.md | 2230 | - [ ] T0329-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T2234-ecbc31c1 | docs/dev/roadmap/v0.2-overview.md | 2231 | - [ ] T0330-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T2235-bcf73ea6 | docs/dev/roadmap/v0.2-overview.md | 2232 | - [ ] T0331-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T2236-c4c1807b | docs/dev/roadmap/v0.2-overview.md | 2233 | - [ ] T0332-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T2237-564fba0e | docs/dev/roadmap/v0.2-overview.md | 2234 | - [ ] T0333-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T2238-4a050890 | docs/dev/roadmap/v0.2-overview.md | 2235 | - [ ] T0334-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T2239-e14f4de0 | docs/dev/roadmap/v0.2-overview.md | 2236 | - [ ] T0335-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T2240-f2a2f15c | docs/dev/roadmap/v0.2-overview.md | 2237 | - [ ] T0336-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T2241-29245340 | docs/dev/roadmap/v0.2-overview.md | 2238 | - [ ] T0337-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T2242-f3fcc954 | docs/dev/roadmap/v0.2-overview.md | 2239 | - [ ] T0338-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T2243-af782c26 | docs/dev/roadmap/v0.2-overview.md | 2240 | - [ ] T0339-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T2244-f8bdc6a3 | docs/dev/roadmap/v0.2-overview.md | 2241 | - [ ] T0340-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T2245-4d8a472c | docs/dev/roadmap/v0.2-overview.md | 2242 | - [ ] T0341-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T2246-5a80584c | docs/dev/roadmap/v0.2-overview.md | 2243 | - [ ] T0342-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T2247-e929ac1a | docs/dev/roadmap/v0.2-overview.md | 2244 | - [ ] T0343-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T2248-a92f23da | docs/dev/roadmap/v0.2-overview.md | 2245 | - [ ] T0344-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T2249-38386ed6 | docs/dev/roadmap/v0.2-overview.md | 2246 | - [ ] T0345-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T2250-005aace2 | docs/dev/roadmap/v0.2-overview.md | 2247 | - [ ] T0346-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T2251-4c748754 | docs/dev/roadmap/v0.2-overview.md | 2248 | - [ ] T0347-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T2252-f5d0baa7 | docs/dev/roadmap/v0.2-overview.md | 2249 | - [ ] T0348-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T2253-58f7b27f | docs/dev/roadmap/v0.2-overview.md | 2250 | - [ ] T0349-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T2254-a5a7da78 | docs/dev/roadmap/v0.2-overview.md | 2251 | - [ ] T0350-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T2255-0df38125 | docs/dev/roadmap/v0.2-overview.md | 2252 | - [ ] T0351-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T2256-76f62e90 | docs/dev/roadmap/v0.2-overview.md | 2253 | - [ ] T0352-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T2257-e7a5c64b | docs/dev/roadmap/v0.2-overview.md | 2254 | - [ ] T0353-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T2258-58694887 | docs/dev/roadmap/v0.2-overview.md | 2255 | - [ ] T0354-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T2259-0f6dcf13 | docs/dev/roadmap/v0.2-overview.md | 2256 | - [ ] T0355-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T2260-f2d36ed4 | docs/dev/roadmap/v0.2-overview.md | 2257 | - [ ] T0356-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T2261-6ab00347 | docs/dev/roadmap/v0.2-overview.md | 2258 | - [ ] T0357-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T2262-282dca8c | docs/dev/roadmap/v0.2-overview.md | 2259 | - [ ] T0358-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T2263-db4034eb | docs/dev/roadmap/v0.2-overview.md | 2260 | - [ ] T0359-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T2264-f14fee67 | docs/dev/roadmap/v0.2-overview.md | 2261 | - [ ] T0360-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T2265-68de116f | docs/dev/roadmap/v0.2-overview.md | 2262 | - [ ] T0361-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T2266-03e72e5e | docs/dev/roadmap/v0.2-overview.md | 2263 | - [ ] T0362-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T2267-05fca6e5 | docs/dev/roadmap/v0.2-overview.md | 2264 | - [ ] T0363-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T2268-d376ab5b | docs/dev/roadmap/v0.2-overview.md | 2265 | - [ ] T0364-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T2269-84cb2744 | docs/dev/roadmap/v0.2-overview.md | 2266 | - [ ] T0365-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T2270-48d31cce | docs/dev/roadmap/v0.2-overview.md | 2267 | - [ ] T0366-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T2271-65b11f96 | docs/dev/roadmap/v0.2-overview.md | 2268 | - [ ] T0367-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T2272-5c5c00bf | docs/dev/roadmap/v0.2-overview.md | 2269 | - [ ] T0368-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T2273-a8a355c6 | docs/dev/roadmap/v0.2-overview.md | 2270 | - [ ] T0369-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T2274-fca20be3 | docs/dev/roadmap/v0.2-overview.md | 2271 | - [ ] T0370-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T2275-437c64a8 | docs/dev/roadmap/v0.2-overview.md | 2272 | - [ ] T0371-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T2276-036d2334 | docs/dev/roadmap/v0.2-overview.md | 2273 | - [ ] T0372-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T2277-c422abfd | docs/dev/roadmap/v0.2-overview.md | 2274 | - [ ] T0373-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T2278-170d6883 | docs/dev/roadmap/v0.2-overview.md | 2275 | - [ ] T0374-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T2279-f258a51d | docs/dev/roadmap/v0.2-overview.md | 2276 | - [ ] T0375-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T2280-6dd0a719 | docs/dev/roadmap/v0.2-overview.md | 2277 | - [ ] T0376-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T2281-e56b221d | docs/dev/roadmap/v0.2-overview.md | 2278 | - [ ] T0377-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T2282-ccefa4b7 | docs/dev/roadmap/v0.2-overview.md | 2279 | - [ ] T0378-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T2283-be3dac11 | docs/dev/roadmap/v0.2-overview.md | 2280 | - [ ] T0379-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T2284-58c3d89c | docs/dev/roadmap/v0.2-overview.md | 2281 | - [ ] T0380-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T2285-9487bffa | docs/dev/roadmap/v0.2-overview.md | 2282 | - [ ] T0381-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T2286-fc5bd6a6 | docs/dev/roadmap/v0.2-overview.md | 2283 | - [ ] T0382-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T2287-c76e2477 | docs/dev/roadmap/v0.2-overview.md | 2284 | - [ ] T0383-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T2288-e76b1d9b | docs/dev/roadmap/v0.2-overview.md | 2285 | - [ ] T0384-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T2289-ad099014 | docs/dev/roadmap/v0.2-overview.md | 2286 | - [ ] T0385-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T2290-63c47fd6 | docs/dev/roadmap/v0.2-overview.md | 2287 | - [ ] T0386-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T2291-202526ed | docs/dev/roadmap/v0.2-overview.md | 2288 | - [ ] T0387-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T2292-068d2067 | docs/dev/roadmap/v0.2-overview.md | 2289 | - [ ] T0388-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T2293-8502d40b | docs/dev/roadmap/v0.2-overview.md | 2290 | - [ ] T0389-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T2294-0d21768e | docs/dev/roadmap/v0.2-overview.md | 2291 | - [ ] T0390-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T2295-82abff57 | docs/dev/roadmap/v0.2-overview.md | 2292 | - [ ] T0391-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T2296-2c33a080 | docs/dev/roadmap/v0.2-overview.md | 2293 | - [ ] T0392-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T2297-22a740f4 | docs/dev/roadmap/v0.2-overview.md | 2294 | - [ ] T0393-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T2298-0583059c | docs/dev/roadmap/v0.2-overview.md | 2295 | - [ ] T0394-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T2299-d987bce4 | docs/dev/roadmap/v0.2-overview.md | 2296 | - [ ] T0395-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T2300-fac78d7d | docs/dev/roadmap/v0.2-overview.md | 2297 | - [ ] T0396-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T2301-a4f15f97 | docs/dev/roadmap/v0.2-overview.md | 2298 | - [ ] T0397-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T2302-d95fd77c | docs/dev/roadmap/v0.2-overview.md | 2299 | - [ ] T0398-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T2303-8bb4bdd2 | docs/dev/roadmap/v0.2-overview.md | 2300 | - [ ] T0399-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T2304-6f2d03d3 | docs/dev/roadmap/v0.2-overview.md | 2301 | - [ ] T0400-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T2305-e32f72bc | docs/dev/roadmap/v0.2-overview.md | 2302 | - [ ] T0401-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T2306-1ce516a5 | docs/dev/roadmap/v0.2-overview.md | 2303 | - [ ] T0402-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T2307-98066cec | docs/dev/roadmap/v0.2-overview.md | 2304 | - [ ] T0403-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T2308-28ff5d48 | docs/dev/roadmap/v0.2-overview.md | 2305 | - [ ] T0404-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T2309-18f0d825 | docs/dev/roadmap/v0.2-overview.md | 2306 | - [ ] T0405-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T2310-1fc2a951 | docs/dev/roadmap/v0.2-overview.md | 2307 | - [ ] T0406-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T2311-0abcb030 | docs/dev/roadmap/v0.2-overview.md | 2308 | - [ ] T0407-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T2312-98704e85 | docs/dev/roadmap/v0.2-overview.md | 2309 | - [ ] T0408-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T2313-14d90cf5 | docs/dev/roadmap/v0.2-overview.md | 2310 | - [ ] T0409-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T2314-b2ac13b0 | docs/dev/roadmap/v0.2-overview.md | 2311 | - [ ] T0410-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T2315-715bbd0d | docs/dev/roadmap/v0.2-overview.md | 2312 | - [ ] T0411-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T2316-aeeb4491 | docs/dev/roadmap/v0.2-overview.md | 2313 | - [ ] T0412-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T2317-6d712bf8 | docs/dev/roadmap/v0.2-overview.md | 2314 | - [ ] T0413-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T2318-40c32f60 | docs/dev/roadmap/v0.2-overview.md | 2315 | - [ ] T0414-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T2319-e43eb1c3 | docs/dev/roadmap/v0.2-overview.md | 2316 | - [ ] T0415-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T2320-101a1747 | docs/dev/roadmap/v0.2-overview.md | 2317 | - [ ] T0416-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T2321-53723e71 | docs/dev/roadmap/v0.2-overview.md | 2318 | - [ ] T0417-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T2322-67b53233 | docs/dev/roadmap/v0.2-overview.md | 2319 | - [ ] T0418-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T2323-f1f17dde | docs/dev/roadmap/v0.2-overview.md | 2320 | - [ ] T0419-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T2324-85a32c6c | docs/dev/roadmap/v0.2-overview.md | 2321 | - [ ] T0420-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T2325-10ad0343 | docs/dev/roadmap/v0.2-overview.md | 2322 | - [ ] T0421-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T2326-04e2cb71 | docs/dev/roadmap/v0.2-overview.md | 2323 | - [ ] T0422-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T2327-ca181087 | docs/dev/roadmap/v0.2-overview.md | 2324 | - [ ] T0423-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T2328-61b2be5a | docs/dev/roadmap/v0.2-overview.md | 2325 | - [ ] T0424-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T2329-dba10c3a | docs/dev/roadmap/v0.2-overview.md | 2326 | - [ ] T0425-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T2330-ae3f97e4 | docs/dev/roadmap/v0.2-overview.md | 2327 | - [ ] T0426-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T2331-047fc0f1 | docs/dev/roadmap/v0.2-overview.md | 2328 | - [ ] T0427-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T2332-cbd6ad77 | docs/dev/roadmap/v0.2-overview.md | 2329 | - [ ] T6453-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T2333-0f26f53a | docs/dev/roadmap/v0.2-overview.md | 2330 | - [ ] T6454-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T2334-3e14b96f | docs/dev/roadmap/v0.2-overview.md | 2331 | - [ ] T6455-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T2335-0184c6bf | docs/dev/roadmap/v0.2-overview.md | 2332 | - [ ] T6456-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T2336-22f039f5 | docs/dev/roadmap/v0.2-overview.md | 2333 | - [ ] T6457-be759d82 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:167) |
| T2337-f3d3e2cd | docs/dev/roadmap/v0.2-overview.md | 2334 | - [ ] T6458-6f9a8901 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:174) |
| T2338-e5543c38 | docs/dev/roadmap/v0.2-overview.md | 2335 | - [ ] T6459-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T2339-0184c8da | docs/dev/roadmap/v0.2-overview.md | 2336 | - [ ] T6460-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T2340-36dbce97 | docs/dev/roadmap/v0.2-overview.md | 2337 | - [ ] T6461-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T2341-d56f327c | docs/dev/roadmap/v0.2-overview.md | 2338 | - [ ] T6462-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T2342-9fb671cf | docs/dev/roadmap/v0.2-overview.md | 2339 | - [ ] T6463-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T2343-7526570a | docs/dev/roadmap/v0.2-overview.md | 2340 | - [ ] T6464-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T2344-252711d1 | docs/dev/roadmap/v0.2-overview.md | 2341 | - [ ] T6465-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T2345-b09fdee2 | docs/dev/roadmap/v0.2-overview.md | 2342 | - [ ] T6466-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T2346-eafc8285 | docs/dev/roadmap/v0.2-overview.md | 2343 | - [ ] T6467-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T2347-5b17c878 | docs/dev/roadmap/v0.2-overview.md | 2344 | - [ ] T6468-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T2348-0819e27f | docs/dev/roadmap/v0.2-overview.md | 2345 | - [ ] T6469-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T2349-fd1c4916 | docs/dev/roadmap/v0.2-overview.md | 2346 | - [ ] T6470-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T2350-671e1966 | docs/dev/roadmap/v0.2-overview.md | 2347 | - [ ] T6471-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T2351-60e71451 | docs/dev/roadmap/v0.2-overview.md | 2348 | - [ ] T6472-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T2352-54260b70 | docs/dev/roadmap/v0.2-overview.md | 2349 | - [ ] T6473-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T2353-2682e569 | docs/dev/roadmap/v0.2-overview.md | 2350 | - [ ] T6474-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T2354-5d954a8f | docs/dev/roadmap/v0.2-overview.md | 2351 | - [ ] T6475-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T2355-be146593 | docs/dev/roadmap/v0.2-overview.md | 2352 | - [ ] T6476-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T2356-2d5d4689 | docs/dev/roadmap/v0.2-overview.md | 2353 | - [ ] T6477-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T2357-e828dee8 | docs/dev/roadmap/v0.2-overview.md | 2354 | - [ ] T6478-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T2358-a0ffaea6 | docs/dev/roadmap/v0.2-overview.md | 2355 | - [ ] T6479-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T2359-96c77c79 | docs/dev/roadmap/v0.2-overview.md | 2356 | - [ ] T6480-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T2360-78c6c0fc | docs/dev/roadmap/v0.2-overview.md | 2357 | - [ ] T6481-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T2361-046e111b | docs/dev/roadmap/v0.2-overview.md | 2358 | - [ ] T6482-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T2362-b6454399 | docs/dev/roadmap/v0.2-overview.md | 2359 | - [ ] T6483-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T2363-fffe49d2 | docs/dev/roadmap/v0.2-overview.md | 2360 | - [ ] T6484-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T2364-af2037a9 | docs/dev/roadmap/v0.2-overview.md | 2361 | - [ ] T6485-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T2365-a8a9f70b | docs/dev/roadmap/v0.2-overview.md | 2362 | - [ ] T6486-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T2366-427732af | docs/dev/roadmap/v0.2-overview.md | 2363 | - [ ] T6487-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T2367-7d91999e | docs/dev/roadmap/v0.2-overview.md | 2364 | - [ ] T6488-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T2368-080f82cd | docs/dev/roadmap/v0.2-overview.md | 2365 | - [ ] T6489-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T2369-ba05d4c5 | docs/dev/roadmap/v0.2-overview.md | 2366 | - [ ] T6490-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T2370-d54a9e9e | docs/dev/roadmap/v0.2-overview.md | 2367 | - [ ] T6491-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T2371-48c0c089 | docs/dev/roadmap/v0.2-overview.md | 2368 | - [ ] T6492-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T2372-f25e49d3 | docs/dev/roadmap/v0.2-overview.md | 2369 | - [ ] T6493-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T2373-c4f3f5b9 | docs/dev/roadmap/v0.2-overview.md | 2370 | - [ ] T6494-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T2374-dc4f83c6 | docs/dev/roadmap/v0.2-overview.md | 2371 | - [ ] T6495-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T2375-48b53980 | docs/dev/roadmap/v0.2-overview.md | 2372 | - [ ] T6496-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T2376-e1151923 | docs/dev/roadmap/v0.2-overview.md | 2373 | - [ ] T6497-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T2377-10e9af6f | docs/dev/roadmap/v0.2-overview.md | 2374 | - [ ] T6498-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T2378-464403c4 | docs/dev/roadmap/v0.2-overview.md | 2375 | - [ ] T6499-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T2379-bd705a07 | docs/dev/roadmap/v0.2-overview.md | 2376 | - [ ] T6500-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T2380-67b4721b | docs/dev/roadmap/v0.2-overview.md | 2377 | - [ ] T6501-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T2381-22b08d22 | docs/dev/roadmap/v0.2-overview.md | 2378 | - [ ] T6502-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T2382-64f44e09 | docs/dev/roadmap/v0.2-overview.md | 2379 | - [ ] T6503-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T2383-14941970 | docs/dev/roadmap/v0.2-overview.md | 2380 | - [ ] T6504-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T2384-52ed2da7 | docs/dev/roadmap/v0.2-overview.md | 2381 | - [ ] T6505-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T2385-ff6a0d88 | docs/dev/roadmap/v0.2-overview.md | 2382 | - [ ] T6506-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T2386-1834b005 | docs/dev/roadmap/v0.2-overview.md | 2383 | - [ ] T6507-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T2387-6058bff9 | docs/dev/roadmap/v0.2-overview.md | 2384 | - [ ] T6509-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T2388-1be7b22d | docs/dev/roadmap/v0.2-overview.md | 2385 | - [ ] T6510-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T2389-4d2f367a | docs/dev/roadmap/v0.2-overview.md | 2386 | - [ ] T6511-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T2390-04451e52 | docs/dev/roadmap/v0.2-overview.md | 2387 | - [ ] T6512-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T2391-5d487b9c | docs/dev/roadmap/v0.2-overview.md | 2388 | - [ ] T6513-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T2392-6e2d50c6 | docs/dev/roadmap/v0.2-overview.md | 2389 | - [ ] T6514-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T2393-60b68319 | docs/dev/roadmap/v0.2-overview.md | 2390 | - [ ] T6515-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T2394-7915cfa3 | docs/dev/roadmap/v0.2-overview.md | 2391 | - [ ] T6516-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T2395-eac09ece | docs/dev/roadmap/v0.2-overview.md | 2392 | - [ ] T6517-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T2396-34713550 | docs/dev/roadmap/v0.2-overview.md | 2393 | - [ ] T6518-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T2397-bee6ac3f | docs/dev/roadmap/v0.2-overview.md | 2394 | - [ ] T6519-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T2398-4dfdd935 | docs/dev/roadmap/v0.2-overview.md | 2395 | - [ ] T6520-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T2399-9413c410 | docs/dev/roadmap/v0.2-overview.md | 2396 | - [ ] T6521-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T2400-99504e10 | docs/dev/roadmap/v0.2-overview.md | 2397 | - [ ] T6522-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T2401-779ddaa9 | docs/dev/roadmap/v0.2-overview.md | 2398 | - [ ] T6523-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T2402-1cb25b92 | docs/dev/roadmap/v0.2-overview.md | 2399 | - [ ] T6524-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T2403-a6d0b16e | docs/dev/roadmap/v0.2-overview.md | 2400 | - [ ] T6525-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T2404-a1b35486 | docs/dev/roadmap/v0.2-overview.md | 2401 | - [ ] T6526-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T2405-af14e6eb | docs/dev/roadmap/v0.2-overview.md | 2402 | - [ ] T6527-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T2406-cee48a3c | docs/dev/roadmap/v0.2-overview.md | 2403 | - [ ] T6528-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T2407-f3a468f2 | docs/dev/roadmap/v0.2-overview.md | 2404 | - [ ] T6529-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T2408-160cb585 | docs/dev/roadmap/v0.2-overview.md | 2405 | - [ ] T6530-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T2409-17ec2959 | docs/dev/roadmap/v0.2-overview.md | 2406 | - [ ] T6531-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T2410-c780770e | docs/dev/roadmap/v0.2-overview.md | 2407 | - [ ] T6532-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T2411-3911fd47 | docs/dev/roadmap/v0.2-overview.md | 2408 | - [ ] T6533-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T2412-a8b7d004 | docs/dev/roadmap/v0.2-overview.md | 2409 | - [ ] T6534-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T2413-907262c8 | docs/dev/roadmap/v0.2-overview.md | 2410 | - [ ] T6535-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T2414-830dec0d | docs/dev/roadmap/v0.2-overview.md | 2411 | - [ ] T6536-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T2415-456f9e55 | docs/dev/roadmap/v0.2-overview.md | 2412 | - [ ] T6537-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T2416-c9dd2118 | docs/dev/roadmap/v0.2-overview.md | 2413 | - [ ] T6538-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T2417-dca0145b | docs/dev/roadmap/v0.2-overview.md | 2414 | - [ ] T6539-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T2418-e45752eb | docs/dev/roadmap/v0.2-overview.md | 2415 | - [ ] T6540-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T2419-1c166816 | docs/dev/roadmap/v0.2-overview.md | 2416 | - [ ] T6541-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T2420-36380a2d | docs/dev/roadmap/v0.2-overview.md | 2417 | - [ ] T6542-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T2421-da86147f | docs/dev/roadmap/v0.2-overview.md | 2418 | - [ ] T6543-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T2422-670f43e1 | docs/dev/roadmap/v0.2-overview.md | 2419 | - [ ] T6544-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T2423-6ec79056 | docs/dev/roadmap/v0.2-overview.md | 2420 | - [ ] T6545-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T2424-22f97ea7 | docs/dev/roadmap/v0.2-overview.md | 2421 | - [ ] T6546-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T2425-b55cfb32 | docs/dev/roadmap/v0.2-overview.md | 2422 | - [ ] T6547-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T2426-cc0a8671 | docs/dev/roadmap/v0.2-overview.md | 2423 | - [ ] T6548-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T2427-19c2ee92 | docs/dev/roadmap/v0.2-overview.md | 2424 | - [ ] T6549-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T2428-620dd7a5 | docs/dev/roadmap/v0.2-overview.md | 2425 | - [ ] T6550-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T2429-9e703072 | docs/dev/roadmap/v0.2-overview.md | 2426 | - [ ] T6551-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T2430-593d8109 | docs/dev/roadmap/v0.2-overview.md | 2427 | - [ ] T6552-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T2431-1994aace | docs/dev/roadmap/v0.2-overview.md | 2428 | - [ ] T6553-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T2432-4d69d207 | docs/dev/roadmap/v0.2-overview.md | 2429 | - [ ] T6554-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T2433-1d8a3674 | docs/dev/roadmap/v0.2-overview.md | 2430 | - [ ] T6555-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T2434-8fdc1f6f | docs/dev/roadmap/v0.2-overview.md | 2431 | - [ ] T6556-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T2435-9acf3d96 | docs/dev/roadmap/v0.2-overview.md | 2432 | - [ ] T6557-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T2436-e857a9e4 | docs/dev/roadmap/v0.2-overview.md | 2433 | - [ ] T6558-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T2437-cdd6eb40 | docs/dev/roadmap/v0.2-overview.md | 2434 | - [ ] T6559-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T2438-20f19af9 | docs/dev/roadmap/v0.2-overview.md | 2435 | - [ ] T6560-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T2439-ab524889 | docs/dev/roadmap/v0.2-overview.md | 2436 | - [ ] T6561-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T2440-cd341abb | docs/dev/roadmap/v0.2-overview.md | 2437 | - [ ] T6562-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T2441-a58b2b5c | docs/dev/roadmap/v0.2-overview.md | 2438 | - [ ] T6563-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T2442-99b8d808 | docs/dev/roadmap/v0.2-overview.md | 2439 | - [ ] T6564-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T2443-9923765e | docs/dev/roadmap/v0.2-overview.md | 2440 | - [ ] T6565-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T2444-d0e6fbd1 | docs/dev/roadmap/v0.2-overview.md | 2441 | - [ ] T6566-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T2445-46b61a7f | docs/dev/roadmap/v0.2-overview.md | 2442 | - [ ] T6567-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T2446-bebbdae5 | docs/dev/roadmap/v0.2-overview.md | 2443 | - [ ] T6568-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T2447-b76e226c | docs/dev/roadmap/v0.2-overview.md | 2444 | - [ ] T6569-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T2448-fc6889a8 | docs/dev/roadmap/v0.2-overview.md | 2445 | - [ ] T6570-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T2449-bf6a16d0 | docs/dev/roadmap/v0.2-overview.md | 2446 | - [ ] T6571-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T2450-fcaaa220 | docs/dev/roadmap/v0.2-overview.md | 2447 | - [ ] T6572-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T2451-bca65176 | docs/dev/roadmap/v0.2-overview.md | 2448 | - [ ] T6573-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T2452-3373bfa5 | docs/dev/roadmap/v0.2-overview.md | 2449 | - [ ] T6574-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T2453-a6226ae1 | docs/dev/roadmap/v0.2-overview.md | 2450 | - [ ] T6575-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T2454-a345ccfb | docs/dev/roadmap/v0.2-overview.md | 2451 | - [ ] T6576-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T2455-f647572d | docs/dev/roadmap/v0.2-overview.md | 2452 | - [ ] T6577-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T2456-38c40fb7 | docs/dev/roadmap/v0.2-overview.md | 2453 | - [ ] T6578-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T2457-363778a3 | docs/dev/roadmap/v0.2-overview.md | 2454 | - [ ] T6579-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T2458-5fcb3991 | docs/dev/roadmap/v0.2-overview.md | 2455 | - [ ] T6580-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T2459-81c4890d | docs/dev/roadmap/v0.2-overview.md | 2456 | - [ ] T6581-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T2460-275adc3c | docs/dev/roadmap/v0.2-overview.md | 2457 | - [ ] T6582-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T2461-776b6c9d | docs/dev/roadmap/v0.2-overview.md | 2458 | - [ ] T6583-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T2462-e46d65f4 | docs/dev/roadmap/v0.2-overview.md | 2459 | - [ ] T6584-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T2463-039adabc | docs/dev/roadmap/v0.2-overview.md | 2460 | - [ ] T6585-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T2464-121b0777 | docs/dev/roadmap/v0.2-overview.md | 2461 | - [ ] T6586-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T2465-06e33557 | docs/dev/roadmap/v0.2-overview.md | 2462 | - [ ] T6588-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T2466-560e3e2c | docs/dev/roadmap/v0.2-overview.md | 2463 | - [ ] T6589-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T2467-eec80bb2 | docs/dev/roadmap/v0.2-overview.md | 2464 | - [ ] T6590-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T2468-133f9b10 | docs/dev/roadmap/v0.2-overview.md | 2465 | - [ ] T6591-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T2469-d059963e | docs/dev/roadmap/v0.2-overview.md | 2466 | - [ ] T6592-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T2470-888afe86 | docs/dev/roadmap/v0.2-overview.md | 2467 | - [ ] T6593-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T2471-340556c2 | docs/dev/roadmap/v0.2-overview.md | 2468 | - [ ] T6594-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T2472-b2dd873a | docs/dev/roadmap/v0.2-overview.md | 2469 | - [ ] T6595-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T2473-270b5a5e | docs/dev/roadmap/v0.2-overview.md | 2470 | - [ ] T6596-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T2474-28d3de29 | docs/dev/roadmap/v0.2-overview.md | 2471 | - [ ] T6597-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T2475-1cd72b00 | docs/dev/roadmap/v0.2-overview.md | 2472 | - [ ] T6598-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T2476-14803829 | docs/dev/roadmap/v0.2-overview.md | 2473 | - [ ] T6599-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T2477-ef782d72 | docs/dev/roadmap/v0.2-overview.md | 2474 | - [ ] T6600-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T2478-5bf2cd0c | docs/dev/roadmap/v0.2-overview.md | 2475 | - [ ] T6601-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T2479-16492545 | docs/dev/roadmap/v0.2-overview.md | 2476 | - [ ] T6602-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T2480-dda2a02a | docs/dev/roadmap/v0.2-overview.md | 2477 | - [ ] T6603-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T2481-74188e11 | docs/dev/roadmap/v0.2-overview.md | 2478 | - [ ] T6604-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T2482-64cd559c | docs/dev/roadmap/v0.2-overview.md | 2479 | - [ ] T6605-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T2483-65977565 | docs/dev/roadmap/v0.2-overview.md | 2480 | - [ ] T6606-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T2484-d8fd34d9 | docs/dev/roadmap/v0.2-overview.md | 2481 | - [ ] T6607-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T2485-0c0b2ecb | docs/dev/roadmap/v0.2-overview.md | 2482 | - [ ] T6608-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T2486-e87c8948 | docs/dev/roadmap/v0.2-overview.md | 2483 | - [ ] T6609-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T2487-56187551 | docs/dev/roadmap/v0.2-overview.md | 2484 | - [ ] T6610-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T2488-b87075fc | docs/dev/roadmap/v0.2-overview.md | 2485 | - [ ] T6611-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T2489-e8b6b921 | docs/dev/roadmap/v0.2-overview.md | 2486 | - [ ] T6612-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T2490-fce9d097 | docs/dev/roadmap/v0.2-overview.md | 2487 | - [ ] T6613-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T2491-af3e9c72 | docs/dev/roadmap/v0.2-overview.md | 2488 | - [ ] T6614-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T2492-ab2d8244 | docs/dev/roadmap/v0.2-overview.md | 2489 | - [ ] T6615-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T2493-ef4e3de9 | docs/dev/roadmap/v0.2-overview.md | 2490 | - [ ] T6616-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T2494-89e1b433 | docs/dev/roadmap/v0.2-overview.md | 2491 | - [ ] T6617-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T2495-7dc46416 | docs/dev/roadmap/v0.2-overview.md | 2492 | - [ ] T6618-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T2496-3daf3a83 | docs/dev/roadmap/v0.2-overview.md | 2493 | - [ ] T6619-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T2497-2995c247 | docs/dev/roadmap/v0.2-overview.md | 2494 | - [ ] T6620-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T2498-073e5cd2 | docs/dev/roadmap/v0.2-overview.md | 2495 | - [ ] T6621-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T2499-01727b34 | docs/dev/roadmap/v0.2-overview.md | 2496 | - [ ] T6622-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T2500-ea159434 | docs/dev/roadmap/v0.2-overview.md | 2497 | - [ ] T6623-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T2501-852fe721 | docs/dev/roadmap/v0.2-overview.md | 2498 | - [ ] T6624-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T2502-987c5851 | docs/dev/roadmap/v0.2-overview.md | 2499 | - [ ] T6625-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T2503-1ee7bddc | docs/dev/roadmap/v0.2-overview.md | 2500 | - [ ] T6626-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T2504-22a9f24b | docs/dev/roadmap/v0.2-overview.md | 2501 | - [ ] T6627-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T2505-1d781330 | docs/dev/roadmap/v0.2-overview.md | 2502 | - [ ] T6628-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T2506-291eb42f | docs/dev/roadmap/v0.2-overview.md | 2503 | - [ ] T6629-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T2507-cd4bd9e1 | docs/dev/roadmap/v0.2-overview.md | 2504 | - [ ] T6630-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T2508-527a88ed | docs/dev/roadmap/v0.2-overview.md | 2505 | - [ ] T6631-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T2509-5109806c | docs/dev/roadmap/v0.2-overview.md | 2506 | - [ ] T6632-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T2510-2c052b8a | docs/dev/roadmap/v0.2-overview.md | 2507 | - [ ] T6633-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T2511-2ee52f51 | docs/dev/roadmap/v0.2-overview.md | 2508 | - [ ] T6634-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T2512-622ce11f | docs/dev/roadmap/v0.2-overview.md | 2509 | - [ ] T6635-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T2513-ebfb3d76 | docs/dev/roadmap/v0.2-overview.md | 2510 | - [ ] T6636-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T2514-12809d48 | docs/dev/roadmap/v0.2-overview.md | 2511 | - [ ] T6637-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T2515-25f9440f | docs/dev/roadmap/v0.2-overview.md | 2512 | - [ ] T6638-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T2516-e0f955f3 | docs/dev/roadmap/v0.2-overview.md | 2513 | - [ ] T6639-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T2517-dc3febd3 | docs/dev/roadmap/v0.2-overview.md | 2514 | - [ ] T6640-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T2518-dcc5576a | docs/dev/roadmap/v0.2-overview.md | 2515 | - [ ] T6641-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T2519-49d9fab0 | docs/dev/roadmap/v0.2-overview.md | 2516 | - [ ] T6642-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T2520-4a567f83 | docs/dev/roadmap/v0.2-overview.md | 2517 | - [ ] T6643-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T2521-20649688 | docs/dev/roadmap/v0.2-overview.md | 2518 | - [ ] T6644-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T2522-10614a6f | docs/dev/roadmap/v0.2-overview.md | 2519 | - [ ] T6646-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T2523-aae85510 | docs/dev/roadmap/v0.2-overview.md | 2520 | - [ ] T6647-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T2524-5f140167 | docs/dev/roadmap/v0.2-overview.md | 2521 | - [ ] T6648-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T2525-ae9c8f45 | docs/dev/roadmap/v0.2-overview.md | 2522 | - [ ] T6649-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T2526-7aa5f70d | docs/dev/roadmap/v0.2-overview.md | 2523 | - [ ] T6650-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T2527-9a05c587 | docs/dev/roadmap/v0.2-overview.md | 2524 | - [ ] T6651-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T2528-972fe181 | docs/dev/roadmap/v0.2-overview.md | 2525 | - [ ] T6652-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T2529-46915ff7 | docs/dev/roadmap/v0.2-overview.md | 2526 | - [ ] T6653-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T2530-712f3324 | docs/dev/roadmap/v0.2-overview.md | 2527 | - [ ] T6654-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T2531-32dd4af8 | docs/dev/roadmap/v0.2-overview.md | 2528 | - [ ] T6655-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T2532-dbd34e5e | docs/dev/roadmap/v0.2-overview.md | 2529 | - [ ] T6656-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T2533-cb80f66e | docs/dev/roadmap/v0.2-overview.md | 2530 | - [ ] T6657-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T2534-69ade574 | docs/dev/roadmap/v0.2-overview.md | 2531 | - [ ] T6658-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T2535-02a55a6e | docs/dev/roadmap/v0.2-overview.md | 2532 | - [ ] T6659-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T2536-61e46d17 | docs/dev/roadmap/v0.2-overview.md | 2533 | - [ ] T6660-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T2537-0ba40d60 | docs/dev/roadmap/v0.2-overview.md | 2534 | - [ ] T6661-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T2538-6b768c7e | docs/dev/roadmap/v0.2-overview.md | 2535 | - [ ] T6662-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T2539-d702bda8 | docs/dev/roadmap/v0.2-overview.md | 2536 | - [ ] T6663-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T2540-433a8e02 | docs/dev/roadmap/v0.2-overview.md | 2537 | - [ ] T6664-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T2541-63d97731 | docs/dev/roadmap/v0.2-overview.md | 2538 | - [ ] T6665-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T2542-6589b802 | docs/dev/roadmap/v0.2-overview.md | 2539 | - [ ] T6666-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T2543-242253bb | docs/dev/roadmap/v0.2-overview.md | 2540 | - [ ] T6667-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T2544-a9956717 | docs/dev/roadmap/v0.2-overview.md | 2541 | - [ ] T6668-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T2545-96b5ea37 | docs/dev/roadmap/v0.2-overview.md | 2542 | - [ ] T6669-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T2546-d158c64f | docs/dev/roadmap/v0.2-overview.md | 2543 | - [ ] T6670-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T2547-683fbf80 | docs/dev/roadmap/v0.2-overview.md | 2544 | - [ ] T6671-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T2548-a3a3d12d | docs/dev/roadmap/v0.2-overview.md | 2545 | - [ ] T6672-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T2549-e91a57f3 | docs/dev/roadmap/v0.2-overview.md | 2546 | - [ ] T6673-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T2550-214a0792 | docs/dev/roadmap/v0.2-overview.md | 2547 | - [ ] T6674-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T2551-92e035d7 | docs/dev/roadmap/v0.2-overview.md | 2548 | - [ ] T6675-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T2552-5cb36e25 | docs/dev/roadmap/v0.2-overview.md | 2549 | - [ ] T6676-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T2553-67fab030 | docs/dev/roadmap/v0.2-overview.md | 2550 | - [ ] T6677-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T2554-262cf949 | docs/dev/roadmap/v0.2-overview.md | 2551 | - [ ] T6678-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T2555-f95c2e71 | docs/dev/roadmap/v0.2-overview.md | 2552 | - [ ] T6679-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T2556-7d226057 | docs/dev/roadmap/v0.2-overview.md | 2553 | - [ ] T6680-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T2557-22bfcf30 | docs/dev/roadmap/v0.2-overview.md | 2554 | - [ ] T6681-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T2558-12b4d6ad | docs/dev/roadmap/v0.2-overview.md | 2555 | - [ ] T6682-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T2559-e116a38e | docs/dev/roadmap/v0.2-overview.md | 2556 | - [ ] T6683-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T2560-5a808868 | docs/dev/roadmap/v0.2-overview.md | 2557 | - [ ] T6684-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T2561-6d7e4b7f | docs/dev/roadmap/v0.2-overview.md | 2558 | - [ ] T6685-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T2562-4571e73c | docs/dev/roadmap/v0.2-overview.md | 2559 | - [ ] T6686-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T2563-f304da2b | docs/dev/roadmap/v0.2-overview.md | 2560 | - [ ] T6687-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T2564-bc502c43 | docs/dev/roadmap/v0.2-overview.md | 2561 | - [ ] T6688-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T2565-0b1a78e2 | docs/dev/roadmap/v0.2-overview.md | 2562 | - [ ] T6689-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T2566-37654f9c | docs/dev/roadmap/v0.2-overview.md | 2563 | - [ ] T6690-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T2567-6de221bd | docs/dev/roadmap/v0.2-overview.md | 2564 | - [ ] T6691-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T2568-94f54bbf | docs/dev/roadmap/v0.2-overview.md | 2565 | - [ ] T6692-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T2569-bbfff97b | docs/dev/roadmap/v0.2-overview.md | 2566 | - [ ] T6693-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T2570-25467d3c | docs/dev/roadmap/v0.2-overview.md | 2567 | - [ ] T6694-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T2571-4364b0f3 | docs/dev/roadmap/v0.2-overview.md | 2568 | - [ ] T6695-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T2572-fea22970 | docs/dev/roadmap/v0.2-overview.md | 2569 | - [ ] T6696-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T2573-139d44ac | docs/dev/roadmap/v0.2-overview.md | 2570 | - [ ] T6697-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T2574-d0796b41 | docs/dev/roadmap/v0.2-overview.md | 2571 | - [ ] T6698-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T2575-eae29055 | docs/dev/roadmap/v0.2-overview.md | 2572 | - [ ] T6699-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T2576-b6802e4a | docs/dev/roadmap/v0.2-overview.md | 2573 | - [ ] T6700-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T2577-5907c3e3 | docs/dev/roadmap/v0.2-overview.md | 2574 | - [ ] T6701-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T2578-c44490b3 | docs/dev/roadmap/v0.2-overview.md | 2575 | - [ ] T6702-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T2579-c7f5fc03 | docs/dev/roadmap/v0.2-overview.md | 2576 | - [ ] T6703-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T2580-39f11b2d | docs/dev/roadmap/v0.2-overview.md | 2577 | - [ ] T6704-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T2581-84d9121b | docs/dev/roadmap/v0.2-overview.md | 2578 | - [ ] T6705-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T2582-6308656a | docs/dev/roadmap/v0.2-overview.md | 2579 | - [ ] T6706-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T2583-c4543451 | docs/dev/roadmap/v0.2-overview.md | 2580 | - [ ] T6707-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T2584-9c9a9951 | docs/dev/roadmap/v0.2-overview.md | 2581 | - [ ] T6708-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T2585-9dc86d3d | docs/dev/roadmap/v0.2-overview.md | 2582 | - [ ] T6709-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T2586-15e932b7 | docs/dev/roadmap/v0.2-overview.md | 2583 | - [ ] T6710-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T2587-32c5030d | docs/dev/roadmap/v0.2-overview.md | 2584 | - [ ] T6711-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T2588-965b52b1 | docs/dev/roadmap/v0.2-overview.md | 2585 | - [ ] T6712-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T2589-35ecfd47 | docs/dev/roadmap/v0.2-overview.md | 2586 | - [ ] T6713-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T2590-7ac0415f | docs/dev/roadmap/v0.2-overview.md | 2587 | - [ ] T6714-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T2591-0556f9df | docs/dev/roadmap/v0.2-overview.md | 2588 | - [ ] T6715-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T2592-89a779ee | docs/dev/roadmap/v0.2-overview.md | 2589 | - [ ] T6716-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T2593-1aaf5c57 | docs/dev/roadmap/v0.2-overview.md | 2590 | - [ ] T6717-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T2594-816e54a7 | docs/dev/roadmap/v0.2-overview.md | 2591 | - [ ] T6718-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T2595-7a20697f | docs/dev/roadmap/v0.2-overview.md | 2592 | - [ ] T6719-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T2596-beefa6cd | docs/dev/roadmap/v0.2-overview.md | 2593 | - [ ] T6720-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T2597-06146902 | docs/dev/roadmap/v0.2-overview.md | 2594 | - [ ] T6721-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T2598-04f648b2 | docs/dev/roadmap/v0.2-overview.md | 2595 | - [ ] T6722-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T2599-775f812b | docs/dev/roadmap/v0.2-overview.md | 2596 | - [ ] T6723-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T2600-67d2f9d5 | docs/dev/roadmap/v0.2-overview.md | 2597 | - [ ] T6724-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T2601-8a3527da | docs/dev/roadmap/v0.2-overview.md | 2598 | - [ ] T6725-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T2602-a2d37e3b | docs/dev/roadmap/v0.2-overview.md | 2599 | - [ ] T6726-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T2603-af7af13d | docs/dev/roadmap/v0.2-overview.md | 2600 | - [ ] T6727-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T2604-616776ed | docs/dev/roadmap/v0.2-overview.md | 2601 | - [ ] T6728-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T2605-23d69974 | docs/dev/roadmap/v0.2-overview.md | 2602 | - [ ] T6729-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T2606-020b381a | docs/dev/roadmap/v0.2-overview.md | 2603 | - [ ] T6730-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T2607-bc671377 | docs/dev/roadmap/v0.2-overview.md | 2604 | - [ ] T6731-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T2608-970fb7fa | docs/dev/roadmap/v0.2-overview.md | 2605 | - [ ] T6732-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T2609-60395e6b | docs/dev/roadmap/v0.2-overview.md | 2606 | - [ ] T6733-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T2610-7751c222 | docs/dev/roadmap/v0.2-overview.md | 2607 | - [ ] T6734-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T2611-6130de47 | docs/dev/roadmap/v0.2-overview.md | 2608 | - [ ] T6735-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T2612-2e64d287 | docs/dev/roadmap/v0.2-overview.md | 2609 | - [ ] T6736-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T2613-0e2228d3 | docs/dev/roadmap/v0.2-overview.md | 2610 | - [ ] T6737-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T2614-76974290 | docs/dev/roadmap/v0.2-overview.md | 2611 | - [ ] T6738-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T2615-638180b7 | docs/dev/roadmap/v0.2-overview.md | 2612 | - [ ] T6739-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T2616-5c8936fd | docs/dev/roadmap/v0.2-overview.md | 2613 | - [ ] T6740-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T2617-49a6cfdc | docs/dev/roadmap/v0.2-overview.md | 2614 | - [ ] T6741-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T2618-c1c7c6c9 | docs/dev/roadmap/v0.2-overview.md | 2615 | - [ ] T6742-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T2619-5ad44509 | docs/dev/roadmap/v0.2-overview.md | 2616 | - [ ] T6743-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T2620-fe9ffd7b | docs/dev/roadmap/v0.2-overview.md | 2617 | - [ ] T6744-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T2621-eea57652 | docs/dev/roadmap/v0.2-overview.md | 2618 | - [ ] T6745-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T2622-d1f4ff52 | docs/dev/roadmap/v0.2-overview.md | 2619 | - [ ] T6746-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T2623-709a90a7 | docs/dev/roadmap/v0.2-overview.md | 2620 | - [ ] T6747-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T2624-e3940d8e | docs/dev/roadmap/v0.2-overview.md | 2621 | - [ ] T6748-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T2625-3489f57b | docs/dev/roadmap/v0.2-overview.md | 2622 | - [ ] T6749-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T2626-36680211 | docs/dev/roadmap/v0.2-overview.md | 2623 | - [ ] T6750-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T2627-32f91c62 | docs/dev/roadmap/v0.2-overview.md | 2624 | - [ ] T6751-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T2628-28e300cd | docs/dev/roadmap/v0.2-overview.md | 2625 | - [ ] T6752-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T2629-8e450525 | docs/dev/roadmap/v0.2-overview.md | 2626 | - [ ] T6753-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T2630-ff1b8e07 | docs/dev/roadmap/v0.2-overview.md | 2627 | - [ ] T6754-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T2631-57484580 | docs/dev/roadmap/v0.2-overview.md | 2628 | - [ ] T6755-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T2632-813d5115 | docs/dev/roadmap/v0.2-overview.md | 2629 | - [ ] T6756-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T2633-339a0f57 | docs/dev/roadmap/v0.2-overview.md | 2630 | - [ ] T6757-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T2634-61113218 | docs/dev/roadmap/v0.2-overview.md | 2631 | - [ ] T6758-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T2635-0353f16b | docs/dev/roadmap/v0.2-overview.md | 2632 | - [ ] T6759-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T2636-0b20b36c | docs/dev/roadmap/v0.2-overview.md | 2633 | - [ ] T6760-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T2637-8278bc31 | docs/dev/roadmap/v0.2-overview.md | 2634 | - [ ] T6761-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T2638-01dd171f | docs/dev/roadmap/v0.2-overview.md | 2635 | - [ ] T6762-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T2639-85ed00c0 | docs/dev/roadmap/v0.2-overview.md | 2636 | - [ ] T6763-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T2640-0a489f9b | docs/dev/roadmap/v0.2-overview.md | 2637 | - [ ] T6764-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T2641-b6ea1cb2 | docs/dev/roadmap/v0.2-overview.md | 2638 | - [ ] T6765-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T2642-41ad84bd | docs/dev/roadmap/v0.2-overview.md | 2639 | - [ ] T6766-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T2643-38bce1cc | docs/dev/roadmap/v0.2-overview.md | 2640 | - [ ] T6767-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T2644-27ea126b | docs/dev/roadmap/v0.2-overview.md | 2641 | - [ ] T6768-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T2645-a0a3ffac | docs/dev/roadmap/v0.2-overview.md | 2642 | - [ ] T6769-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T2646-6d186e21 | docs/dev/roadmap/v0.2-overview.md | 2643 | - [ ] T6770-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T2647-af35b2da | docs/dev/roadmap/v0.2-overview.md | 2644 | - [ ] T6771-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T2648-7d26c7b8 | docs/dev/roadmap/v0.2-overview.md | 2645 | - [ ] T6772-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T2649-6909f79a | docs/dev/roadmap/v0.2-overview.md | 2646 | - [ ] T6773-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T2650-092703ef | docs/dev/roadmap/v0.2-overview.md | 2647 | - [ ] T7089-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T2651-493c1c6c | docs/dev/roadmap/v0.2-overview.md | 2648 | - [ ] T7090-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T2652-9647c8fa | docs/dev/roadmap/v0.2-overview.md | 2649 | - [ ] T7091-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T2653-183cea5f | docs/dev/roadmap/v0.2-overview.md | 2650 | - [ ] T7092-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T2654-c1463bdf | docs/dev/roadmap/v0.2-overview.md | 2651 | - [ ] T7093-4c66e9b1 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:155) |
| T2655-35f80dff | docs/dev/roadmap/v0.2-overview.md | 2652 | - [ ] T7094-813e30e1 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:162) |
| T2656-de426b28 | docs/dev/roadmap/v0.2-overview.md | 2653 | - [ ] T7095-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T2657-2eb82a85 | docs/dev/roadmap/v0.2-overview.md | 2654 | - [ ] T7096-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T2658-65126386 | docs/dev/roadmap/v0.2-overview.md | 2655 | - [ ] T7097-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T2659-5da4d4ea | docs/dev/roadmap/v0.2-overview.md | 2656 | - [ ] T7098-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T2660-5f2b53e8 | docs/dev/roadmap/v0.2-overview.md | 2657 | - [ ] T7099-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T2661-94259a6b | docs/dev/roadmap/v0.2-overview.md | 2658 | - [ ] T7100-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T2662-d6533f69 | docs/dev/roadmap/v0.2-overview.md | 2659 | - [ ] T7101-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T2663-be5e392e | docs/dev/roadmap/v0.2-overview.md | 2660 | - [ ] T7102-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T2664-c759ae76 | docs/dev/roadmap/v0.2-overview.md | 2661 | - [ ] T7103-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T2665-961374c9 | docs/dev/roadmap/v0.2-overview.md | 2662 | - [ ] T7104-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T2666-8631c575 | docs/dev/roadmap/v0.2-overview.md | 2663 | - [ ] T7105-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T2667-5c68241a | docs/dev/roadmap/v0.2-overview.md | 2664 | - [ ] T7106-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T2668-b33ce970 | docs/dev/roadmap/v0.2-overview.md | 2665 | - [ ] T7107-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T2669-6b3032e1 | docs/dev/roadmap/v0.2-overview.md | 2666 | - [ ] T7108-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T2670-0966f919 | docs/dev/roadmap/v0.2-overview.md | 2667 | - [ ] T7109-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T2671-19db95d3 | docs/dev/roadmap/v0.2-overview.md | 2668 | - [ ] T7110-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T2672-ef34d90a | docs/dev/roadmap/v0.2-overview.md | 2669 | - [ ] T7111-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T2673-bc173bef | docs/dev/roadmap/v0.2-overview.md | 2670 | - [ ] T7112-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T2674-03d1ad0b | docs/dev/roadmap/v0.2-overview.md | 2671 | - [ ] T7113-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T2675-b635029e | docs/dev/roadmap/v0.2-overview.md | 2672 | - [ ] T7114-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T2676-58d88748 | docs/dev/roadmap/v0.2-overview.md | 2673 | - [ ] T7115-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T2677-30ac839a | docs/dev/roadmap/v0.2-overview.md | 2674 | - [ ] T7116-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T2678-541da3ad | docs/dev/roadmap/v0.2-overview.md | 2675 | - [ ] T7117-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T2679-720a2397 | docs/dev/roadmap/v0.2-overview.md | 2676 | - [ ] T7118-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T2680-be070889 | docs/dev/roadmap/v0.2-overview.md | 2677 | - [ ] T7119-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T2681-1d2899a1 | docs/dev/roadmap/v0.2-overview.md | 2678 | - [ ] T7120-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T2682-2e6ae6d0 | docs/dev/roadmap/v0.2-overview.md | 2679 | - [ ] T7121-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T2683-05b87c32 | docs/dev/roadmap/v0.2-overview.md | 2680 | - [ ] T7122-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T2684-e753fd9b | docs/dev/roadmap/v0.2-overview.md | 2681 | - [ ] T7123-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T2685-35ff47ee | docs/dev/roadmap/v0.2-overview.md | 2682 | - [ ] T7124-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T2686-3300e43d | docs/dev/roadmap/v0.2-overview.md | 2683 | - [ ] T7125-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T2687-0979d49a | docs/dev/roadmap/v0.2-overview.md | 2684 | - [ ] T7126-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T2688-775b641b | docs/dev/roadmap/v0.2-overview.md | 2685 | - [ ] T7127-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T2689-77097d38 | docs/dev/roadmap/v0.2-overview.md | 2686 | - [ ] T7128-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T2690-3033cb5c | docs/dev/roadmap/v0.2-overview.md | 2687 | - [ ] T7129-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T2691-b62c5079 | docs/dev/roadmap/v0.2-overview.md | 2688 | - [ ] T7130-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T2692-3c20cfe9 | docs/dev/roadmap/v0.2-overview.md | 2689 | - [ ] T7131-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T2693-009d55a8 | docs/dev/roadmap/v0.2-overview.md | 2690 | - [ ] T7132-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T2694-09504289 | docs/dev/roadmap/v0.2-overview.md | 2691 | - [ ] T7133-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T2695-2ec7da6a | docs/dev/roadmap/v0.2-overview.md | 2692 | - [ ] T7134-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T2696-571b7d5b | docs/dev/roadmap/v0.2-overview.md | 2693 | - [ ] T7135-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T2697-963787ec | docs/dev/roadmap/v0.2-overview.md | 2694 | - [ ] T7136-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T2698-fab95ccc | docs/dev/roadmap/v0.2-overview.md | 2695 | - [ ] T7137-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T2699-e765a58f | docs/dev/roadmap/v0.2-overview.md | 2696 | - [ ] T7138-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T2700-0bcd7209 | docs/dev/roadmap/v0.2-overview.md | 2697 | - [ ] T7139-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T2701-a874ce8b | docs/dev/roadmap/v0.2-overview.md | 2698 | - [ ] T7140-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T2702-ba9f865b | docs/dev/roadmap/v0.2-overview.md | 2699 | - [ ] T7141-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T2703-2ba59b06 | docs/dev/roadmap/v0.2-overview.md | 2700 | - [ ] T7142-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T2704-5a9eb908 | docs/dev/roadmap/v0.2-overview.md | 2701 | - [ ] T7143-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T2705-d9d66d7f | docs/dev/roadmap/v0.2-overview.md | 2702 | - [ ] T7145-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T2706-c4263aa6 | docs/dev/roadmap/v0.2-overview.md | 2703 | - [ ] T7146-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T2707-1b9edaf7 | docs/dev/roadmap/v0.2-overview.md | 2704 | - [ ] T7147-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T2708-7dcff6aa | docs/dev/roadmap/v0.2-overview.md | 2705 | - [ ] T7148-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T2709-9dcdf2a8 | docs/dev/roadmap/v0.2-overview.md | 2706 | - [ ] T7149-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T2710-d41f2c1d | docs/dev/roadmap/v0.2-overview.md | 2707 | - [ ] T7150-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T2711-12857a2e | docs/dev/roadmap/v0.2-overview.md | 2708 | - [ ] T7151-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T2712-b70ce6b6 | docs/dev/roadmap/v0.2-overview.md | 2709 | - [ ] T7152-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T2713-c4a49267 | docs/dev/roadmap/v0.2-overview.md | 2710 | - [ ] T7153-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T2714-8e3530b9 | docs/dev/roadmap/v0.2-overview.md | 2711 | - [ ] T7154-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T2715-3468de8b | docs/dev/roadmap/v0.2-overview.md | 2712 | - [ ] T7155-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T2716-060f6dcb | docs/dev/roadmap/v0.2-overview.md | 2713 | - [ ] T7156-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T2717-9034d9ca | docs/dev/roadmap/v0.2-overview.md | 2714 | - [ ] T7157-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T2718-7edbad2a | docs/dev/roadmap/v0.2-overview.md | 2715 | - [ ] T7158-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T2719-3cf3aeb1 | docs/dev/roadmap/v0.2-overview.md | 2716 | - [ ] T7159-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T2720-c378c03c | docs/dev/roadmap/v0.2-overview.md | 2717 | - [ ] T7160-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T2721-e4e0ca4a | docs/dev/roadmap/v0.2-overview.md | 2718 | - [ ] T7161-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T2722-1b737740 | docs/dev/roadmap/v0.2-overview.md | 2719 | - [ ] T7162-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T2723-3be9ab2f | docs/dev/roadmap/v0.2-overview.md | 2720 | - [ ] T7163-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T2724-46e53cd1 | docs/dev/roadmap/v0.2-overview.md | 2721 | - [ ] T7164-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T2725-f0ecd21d | docs/dev/roadmap/v0.2-overview.md | 2722 | - [ ] T7165-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T2726-d854c9fb | docs/dev/roadmap/v0.2-overview.md | 2723 | - [ ] T7166-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T2727-bd3f3fa0 | docs/dev/roadmap/v0.2-overview.md | 2724 | - [ ] T7167-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T2728-18da3c12 | docs/dev/roadmap/v0.2-overview.md | 2725 | - [ ] T7168-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T2729-f57ad5cd | docs/dev/roadmap/v0.2-overview.md | 2726 | - [ ] T7169-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T2730-e3010b43 | docs/dev/roadmap/v0.2-overview.md | 2727 | - [ ] T7170-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T2731-538a7725 | docs/dev/roadmap/v0.2-overview.md | 2728 | - [ ] T7171-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T2732-74785276 | docs/dev/roadmap/v0.2-overview.md | 2729 | - [ ] T7172-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T2733-f76e8d03 | docs/dev/roadmap/v0.2-overview.md | 2730 | - [ ] T7173-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T2734-af376513 | docs/dev/roadmap/v0.2-overview.md | 2731 | - [ ] T7174-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T2735-5dd603c2 | docs/dev/roadmap/v0.2-overview.md | 2732 | - [ ] T7175-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T2736-0119e7f7 | docs/dev/roadmap/v0.2-overview.md | 2733 | - [ ] T7176-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T2737-ff3b206c | docs/dev/roadmap/v0.2-overview.md | 2734 | - [ ] T7177-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T2738-26f722df | docs/dev/roadmap/v0.2-overview.md | 2735 | - [ ] T7178-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T2739-7cc82d40 | docs/dev/roadmap/v0.2-overview.md | 2736 | - [ ] T7179-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T2740-4018bf54 | docs/dev/roadmap/v0.2-overview.md | 2737 | - [ ] T7180-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T2741-4b44d2f1 | docs/dev/roadmap/v0.2-overview.md | 2738 | - [ ] T7181-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T2742-2a3b4bb2 | docs/dev/roadmap/v0.2-overview.md | 2739 | - [ ] T7182-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T2743-2203ee9d | docs/dev/roadmap/v0.2-overview.md | 2740 | - [ ] T7183-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T2744-9621601f | docs/dev/roadmap/v0.2-overview.md | 2741 | - [ ] T7184-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T2745-f32ece46 | docs/dev/roadmap/v0.2-overview.md | 2742 | - [ ] T7185-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T2746-61f6c0c9 | docs/dev/roadmap/v0.2-overview.md | 2743 | - [ ] T7186-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T2747-dbc84576 | docs/dev/roadmap/v0.2-overview.md | 2744 | - [ ] T7187-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T2748-fbb349e6 | docs/dev/roadmap/v0.2-overview.md | 2745 | - [ ] T7188-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T2749-8a0dfbf3 | docs/dev/roadmap/v0.2-overview.md | 2746 | - [ ] T7189-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T2750-8a95c09d | docs/dev/roadmap/v0.2-overview.md | 2747 | - [ ] T7190-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T2751-d93e8694 | docs/dev/roadmap/v0.2-overview.md | 2748 | - [ ] T7191-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T2752-9759a15b | docs/dev/roadmap/v0.2-overview.md | 2749 | - [ ] T7192-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T2753-07052cc0 | docs/dev/roadmap/v0.2-overview.md | 2750 | - [ ] T7193-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T2754-cf41cc50 | docs/dev/roadmap/v0.2-overview.md | 2751 | - [ ] T7194-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T2755-235559ca | docs/dev/roadmap/v0.2-overview.md | 2752 | - [ ] T7195-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T2756-0397a882 | docs/dev/roadmap/v0.2-overview.md | 2753 | - [ ] T7196-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T2757-07180d4a | docs/dev/roadmap/v0.2-overview.md | 2754 | - [ ] T7197-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T2758-a6a92932 | docs/dev/roadmap/v0.2-overview.md | 2755 | - [ ] T7198-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T2759-cb2c1cf8 | docs/dev/roadmap/v0.2-overview.md | 2756 | - [ ] T7199-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T2760-babd60eb | docs/dev/roadmap/v0.2-overview.md | 2757 | - [ ] T7200-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T2761-95c843d5 | docs/dev/roadmap/v0.2-overview.md | 2758 | - [ ] T7201-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T2762-3eef1c30 | docs/dev/roadmap/v0.2-overview.md | 2759 | - [ ] T7202-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T2763-ec82bbb3 | docs/dev/roadmap/v0.2-overview.md | 2760 | - [ ] T7203-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T2764-ed4a83ba | docs/dev/roadmap/v0.2-overview.md | 2761 | - [ ] T7204-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T2765-456801e0 | docs/dev/roadmap/v0.2-overview.md | 2762 | - [ ] T7205-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T2766-58349e7c | docs/dev/roadmap/v0.2-overview.md | 2763 | - [ ] T7206-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T2767-4ae11eac | docs/dev/roadmap/v0.2-overview.md | 2764 | - [ ] T7207-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T2768-b34363ea | docs/dev/roadmap/v0.2-overview.md | 2765 | - [ ] T7208-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T2769-743a6279 | docs/dev/roadmap/v0.2-overview.md | 2766 | - [ ] T7209-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T2770-eb11a2b3 | docs/dev/roadmap/v0.2-overview.md | 2767 | - [ ] T7210-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T2771-d7a19d72 | docs/dev/roadmap/v0.2-overview.md | 2768 | - [ ] T7211-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T2772-4307b0ba | docs/dev/roadmap/v0.2-overview.md | 2769 | - [ ] T7212-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T2773-7ae280a3 | docs/dev/roadmap/v0.2-overview.md | 2770 | - [ ] T7213-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T2774-2dcdb97e | docs/dev/roadmap/v0.2-overview.md | 2771 | - [ ] T7214-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T2775-fe358fba | docs/dev/roadmap/v0.2-overview.md | 2772 | - [ ] T7215-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T2776-9a40ce3e | docs/dev/roadmap/v0.2-overview.md | 2773 | - [ ] T7216-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T2777-80da2be3 | docs/dev/roadmap/v0.2-overview.md | 2774 | - [ ] T7217-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T2778-b85c12c5 | docs/dev/roadmap/v0.2-overview.md | 2775 | - [ ] T7218-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T2779-ab89c41f | docs/dev/roadmap/v0.2-overview.md | 2776 | - [ ] T7219-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T2780-9d196da7 | docs/dev/roadmap/v0.2-overview.md | 2777 | - [ ] T7220-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T2781-81e9524e | docs/dev/roadmap/v0.2-overview.md | 2778 | - [ ] T7221-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T2782-d65b270d | docs/dev/roadmap/v0.2-overview.md | 2779 | - [ ] T7222-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T2783-6d61213c | docs/dev/roadmap/v0.2-overview.md | 2780 | - [ ] T7224-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T2784-8da2c061 | docs/dev/roadmap/v0.2-overview.md | 2781 | - [ ] T7225-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T2785-ed038f5a | docs/dev/roadmap/v0.2-overview.md | 2782 | - [ ] T7226-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T2786-27fc16f2 | docs/dev/roadmap/v0.2-overview.md | 2783 | - [ ] T7227-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T2787-7e62ceb2 | docs/dev/roadmap/v0.2-overview.md | 2784 | - [ ] T7228-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T2788-13fe0138 | docs/dev/roadmap/v0.2-overview.md | 2785 | - [ ] T7229-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T2789-e30ca8f1 | docs/dev/roadmap/v0.2-overview.md | 2786 | - [ ] T7230-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T2790-53b3dff3 | docs/dev/roadmap/v0.2-overview.md | 2787 | - [ ] T7231-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T2791-a7091840 | docs/dev/roadmap/v0.2-overview.md | 2788 | - [ ] T7232-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T2792-9ffdf264 | docs/dev/roadmap/v0.2-overview.md | 2789 | - [ ] T7233-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T2793-e1b4b101 | docs/dev/roadmap/v0.2-overview.md | 2790 | - [ ] T7234-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T2794-0fac360b | docs/dev/roadmap/v0.2-overview.md | 2791 | - [ ] T7235-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T2795-e1139e74 | docs/dev/roadmap/v0.2-overview.md | 2792 | - [ ] T7236-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T2796-f6057d54 | docs/dev/roadmap/v0.2-overview.md | 2793 | - [ ] T7237-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T2797-9919e5e7 | docs/dev/roadmap/v0.2-overview.md | 2794 | - [ ] T7238-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T2798-561f1a68 | docs/dev/roadmap/v0.2-overview.md | 2795 | - [ ] T7239-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T2799-cf41f8c6 | docs/dev/roadmap/v0.2-overview.md | 2796 | - [ ] T7240-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T2800-b25cb767 | docs/dev/roadmap/v0.2-overview.md | 2797 | - [ ] T7241-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T2801-890a17ae | docs/dev/roadmap/v0.2-overview.md | 2798 | - [ ] T7242-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T2802-1a91480b | docs/dev/roadmap/v0.2-overview.md | 2799 | - [ ] T7243-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T2803-3b20e711 | docs/dev/roadmap/v0.2-overview.md | 2800 | - [ ] T7244-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T2804-065113a8 | docs/dev/roadmap/v0.2-overview.md | 2801 | - [ ] T7245-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T2805-cafbfce1 | docs/dev/roadmap/v0.2-overview.md | 2802 | - [ ] T7246-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T2806-df4fc1c9 | docs/dev/roadmap/v0.2-overview.md | 2803 | - [ ] T7247-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T2807-59360afa | docs/dev/roadmap/v0.2-overview.md | 2804 | - [ ] T7248-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T2808-a75ef23b | docs/dev/roadmap/v0.2-overview.md | 2805 | - [ ] T7249-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T2809-b7ce3400 | docs/dev/roadmap/v0.2-overview.md | 2806 | - [ ] T7250-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T2810-5609eeb3 | docs/dev/roadmap/v0.2-overview.md | 2807 | - [ ] T7251-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T2811-5cdc74f0 | docs/dev/roadmap/v0.2-overview.md | 2808 | - [ ] T7252-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T2812-4eba88c0 | docs/dev/roadmap/v0.2-overview.md | 2809 | - [ ] T7253-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T2813-25f500f9 | docs/dev/roadmap/v0.2-overview.md | 2810 | - [ ] T7254-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T2814-9f4e2c2c | docs/dev/roadmap/v0.2-overview.md | 2811 | - [ ] T7255-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T2815-7d6865d1 | docs/dev/roadmap/v0.2-overview.md | 2812 | - [ ] T7256-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T2816-91159c3b | docs/dev/roadmap/v0.2-overview.md | 2813 | - [ ] T7257-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T2817-3f53c1a2 | docs/dev/roadmap/v0.2-overview.md | 2814 | - [ ] T7258-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T2818-af3de176 | docs/dev/roadmap/v0.2-overview.md | 2815 | - [ ] T7259-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T2819-032b1371 | docs/dev/roadmap/v0.2-overview.md | 2816 | - [ ] T7260-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T2820-765ab243 | docs/dev/roadmap/v0.2-overview.md | 2817 | - [ ] T7261-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T2821-0f4b3414 | docs/dev/roadmap/v0.2-overview.md | 2818 | - [ ] T7262-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T2822-b284f32b | docs/dev/roadmap/v0.2-overview.md | 2819 | - [ ] T7263-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T2823-95f50023 | docs/dev/roadmap/v0.2-overview.md | 2820 | - [ ] T7264-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T2824-fcde5cd9 | docs/dev/roadmap/v0.2-overview.md | 2821 | - [ ] T7265-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T2825-5feed10f | docs/dev/roadmap/v0.2-overview.md | 2822 | - [ ] T7266-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T2826-3e57d092 | docs/dev/roadmap/v0.2-overview.md | 2823 | - [ ] T7267-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T2827-87a92109 | docs/dev/roadmap/v0.2-overview.md | 2824 | - [ ] T7268-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T2828-b30c1a39 | docs/dev/roadmap/v0.2-overview.md | 2825 | - [ ] T7269-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T2829-20b67ea2 | docs/dev/roadmap/v0.2-overview.md | 2826 | - [ ] T7270-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T2830-30beb88f | docs/dev/roadmap/v0.2-overview.md | 2827 | - [ ] T7271-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T2831-66abeeaa | docs/dev/roadmap/v0.2-overview.md | 2828 | - [ ] T7272-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T2832-d65b74bf | docs/dev/roadmap/v0.2-overview.md | 2829 | - [ ] T7273-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T2833-ba97b0c8 | docs/dev/roadmap/v0.2-overview.md | 2830 | - [ ] T7274-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T2834-8b3caba6 | docs/dev/roadmap/v0.2-overview.md | 2831 | - [ ] T7275-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T2835-e1fd8fe4 | docs/dev/roadmap/v0.2-overview.md | 2832 | - [ ] T7276-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T2836-190f882b | docs/dev/roadmap/v0.2-overview.md | 2833 | - [ ] T7277-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T2837-170eff0f | docs/dev/roadmap/v0.2-overview.md | 2834 | - [ ] T7278-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T2838-2cb4bc36 | docs/dev/roadmap/v0.2-overview.md | 2835 | - [ ] T7279-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T2839-5101f69c | docs/dev/roadmap/v0.2-overview.md | 2836 | - [ ] T7280-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T2840-0970499e | docs/dev/roadmap/v0.2-overview.md | 2837 | - [ ] T7282-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T2841-eda7e9ff | docs/dev/roadmap/v0.2-overview.md | 2838 | - [ ] T7283-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T2842-181d8220 | docs/dev/roadmap/v0.2-overview.md | 2839 | - [ ] T7284-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T2843-29e2c845 | docs/dev/roadmap/v0.2-overview.md | 2840 | - [ ] T7285-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T2844-341ec0d3 | docs/dev/roadmap/v0.2-overview.md | 2841 | - [ ] T7286-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T2845-a9e7745f | docs/dev/roadmap/v0.2-overview.md | 2842 | - [ ] T7287-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T2846-affb1b38 | docs/dev/roadmap/v0.2-overview.md | 2843 | - [ ] T7288-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T2847-2af28ba4 | docs/dev/roadmap/v0.2-overview.md | 2844 | - [ ] T7289-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T2848-81f0c141 | docs/dev/roadmap/v0.2-overview.md | 2845 | - [ ] T7290-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T2849-26a7bc68 | docs/dev/roadmap/v0.2-overview.md | 2846 | - [ ] T7291-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T2850-3a5438ec | docs/dev/roadmap/v0.2-overview.md | 2847 | - [ ] T7292-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T2851-be68b0b5 | docs/dev/roadmap/v0.2-overview.md | 2848 | - [ ] T7293-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T2852-8b8f0041 | docs/dev/roadmap/v0.2-overview.md | 2849 | - [ ] T7294-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T2853-7e04aa44 | docs/dev/roadmap/v0.2-overview.md | 2850 | - [ ] T7295-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T2854-c998c4ce | docs/dev/roadmap/v0.2-overview.md | 2851 | - [ ] T7296-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T2855-65ecc15a | docs/dev/roadmap/v0.2-overview.md | 2852 | - [ ] T7297-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T2856-8ea1e727 | docs/dev/roadmap/v0.2-overview.md | 2853 | - [ ] T7298-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T2857-24e5673d | docs/dev/roadmap/v0.2-overview.md | 2854 | - [ ] T7299-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T2858-bfc40962 | docs/dev/roadmap/v0.2-overview.md | 2855 | - [ ] T7300-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T2859-f3aa4218 | docs/dev/roadmap/v0.2-overview.md | 2856 | - [ ] T7301-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T2860-a5f4ebfd | docs/dev/roadmap/v0.2-overview.md | 2857 | - [ ] T7302-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T2861-37904741 | docs/dev/roadmap/v0.2-overview.md | 2858 | - [ ] T7303-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T2862-bf623f69 | docs/dev/roadmap/v0.2-overview.md | 2859 | - [ ] T7304-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T2863-cfda39b5 | docs/dev/roadmap/v0.2-overview.md | 2860 | - [ ] T7305-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T2864-4fbc513f | docs/dev/roadmap/v0.2-overview.md | 2861 | - [ ] T7306-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T2865-1c127227 | docs/dev/roadmap/v0.2-overview.md | 2862 | - [ ] T7307-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T2866-3ea69dee | docs/dev/roadmap/v0.2-overview.md | 2863 | - [ ] T7308-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T2867-3df56da9 | docs/dev/roadmap/v0.2-overview.md | 2864 | - [ ] T7309-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T2868-ee97745b | docs/dev/roadmap/v0.2-overview.md | 2865 | - [ ] T7310-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T2869-32c1cb80 | docs/dev/roadmap/v0.2-overview.md | 2866 | - [ ] T7311-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T2870-ef718559 | docs/dev/roadmap/v0.2-overview.md | 2867 | - [ ] T7312-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T2871-02ec83f7 | docs/dev/roadmap/v0.2-overview.md | 2868 | - [ ] T7313-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T2872-5061b534 | docs/dev/roadmap/v0.2-overview.md | 2869 | - [ ] T7314-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T2873-50bda611 | docs/dev/roadmap/v0.2-overview.md | 2870 | - [ ] T7315-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T2874-69e6ec15 | docs/dev/roadmap/v0.2-overview.md | 2871 | - [ ] T7316-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T2875-547a0c52 | docs/dev/roadmap/v0.2-overview.md | 2872 | - [ ] T7317-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T2876-67894d85 | docs/dev/roadmap/v0.2-overview.md | 2873 | - [ ] T7318-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T2877-d65e8235 | docs/dev/roadmap/v0.2-overview.md | 2874 | - [ ] T7319-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T2878-4abc8cff | docs/dev/roadmap/v0.2-overview.md | 2875 | - [ ] T7320-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T2879-eba6edf1 | docs/dev/roadmap/v0.2-overview.md | 2876 | - [ ] T7321-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T2880-ba044e2d | docs/dev/roadmap/v0.2-overview.md | 2877 | - [ ] T7322-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T2881-192d0909 | docs/dev/roadmap/v0.2-overview.md | 2878 | - [ ] T7323-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T2882-c2582d82 | docs/dev/roadmap/v0.2-overview.md | 2879 | - [ ] T7324-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T2883-41f23f0c | docs/dev/roadmap/v0.2-overview.md | 2880 | - [ ] T7325-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T2884-8f084b0e | docs/dev/roadmap/v0.2-overview.md | 2881 | - [ ] T7326-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T2885-ef5293d9 | docs/dev/roadmap/v0.2-overview.md | 2882 | - [ ] T7327-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T2886-ac8ffff8 | docs/dev/roadmap/v0.2-overview.md | 2883 | - [ ] T7328-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T2887-8016db2a | docs/dev/roadmap/v0.2-overview.md | 2884 | - [ ] T7329-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T2888-ca288261 | docs/dev/roadmap/v0.2-overview.md | 2885 | - [ ] T7330-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T2889-780fda7a | docs/dev/roadmap/v0.2-overview.md | 2886 | - [ ] T7331-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T2890-4c8b915c | docs/dev/roadmap/v0.2-overview.md | 2887 | - [ ] T7332-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T2891-4a80c68e | docs/dev/roadmap/v0.2-overview.md | 2888 | - [ ] T7333-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T2892-54a2a520 | docs/dev/roadmap/v0.2-overview.md | 2889 | - [ ] T7334-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T2893-6b398572 | docs/dev/roadmap/v0.2-overview.md | 2890 | - [ ] T7335-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T2894-6c477558 | docs/dev/roadmap/v0.2-overview.md | 2891 | - [ ] T7336-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T2895-54c6b1bb | docs/dev/roadmap/v0.2-overview.md | 2892 | - [ ] T7337-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T2896-675ad590 | docs/dev/roadmap/v0.2-overview.md | 2893 | - [ ] T7338-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T2897-1fdab6ce | docs/dev/roadmap/v0.2-overview.md | 2894 | - [ ] T7339-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T2898-34169c5d | docs/dev/roadmap/v0.2-overview.md | 2895 | - [ ] T7340-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T2899-b3cdabda | docs/dev/roadmap/v0.2-overview.md | 2896 | - [ ] T7341-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T2900-9c486153 | docs/dev/roadmap/v0.2-overview.md | 2897 | - [ ] T7342-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T2901-99116ef8 | docs/dev/roadmap/v0.2-overview.md | 2898 | - [ ] T7343-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T2902-ea2f1d70 | docs/dev/roadmap/v0.2-overview.md | 2899 | - [ ] T7344-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T2903-dcfc9722 | docs/dev/roadmap/v0.2-overview.md | 2900 | - [ ] T7345-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T2904-ac8a6600 | docs/dev/roadmap/v0.2-overview.md | 2901 | - [ ] T7346-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T2905-b49a9f86 | docs/dev/roadmap/v0.2-overview.md | 2902 | - [ ] T7347-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T2906-0ad97ec4 | docs/dev/roadmap/v0.2-overview.md | 2903 | - [ ] T7348-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T2907-8b5454ff | docs/dev/roadmap/v0.2-overview.md | 2904 | - [ ] T7349-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T2908-2d827607 | docs/dev/roadmap/v0.2-overview.md | 2905 | - [ ] T7350-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T2909-57aa5e8e | docs/dev/roadmap/v0.2-overview.md | 2906 | - [ ] T7351-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T2910-ea440f44 | docs/dev/roadmap/v0.2-overview.md | 2907 | - [ ] T7352-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T2911-28a37518 | docs/dev/roadmap/v0.2-overview.md | 2908 | - [ ] T7353-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T2912-e4db2ae7 | docs/dev/roadmap/v0.2-overview.md | 2909 | - [ ] T7354-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T2913-3e0efad9 | docs/dev/roadmap/v0.2-overview.md | 2910 | - [ ] T7355-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T2914-847d6274 | docs/dev/roadmap/v0.2-overview.md | 2911 | - [ ] T7356-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T2915-05125872 | docs/dev/roadmap/v0.2-overview.md | 2912 | - [ ] T7357-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T2916-e5798967 | docs/dev/roadmap/v0.2-overview.md | 2913 | - [ ] T7358-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T2917-ae8433ad | docs/dev/roadmap/v0.2-overview.md | 2914 | - [ ] T7359-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T2918-eb70312c | docs/dev/roadmap/v0.2-overview.md | 2915 | - [ ] T7360-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T2919-3f213c58 | docs/dev/roadmap/v0.2-overview.md | 2916 | - [ ] T7361-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T2920-d9de1495 | docs/dev/roadmap/v0.2-overview.md | 2917 | - [ ] T7362-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T2921-d1a0bfe6 | docs/dev/roadmap/v0.2-overview.md | 2918 | - [ ] T7363-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T2922-eeb67bef | docs/dev/roadmap/v0.2-overview.md | 2919 | - [ ] T7364-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T2923-723553b2 | docs/dev/roadmap/v0.2-overview.md | 2920 | - [ ] T7365-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T2924-ac46f050 | docs/dev/roadmap/v0.2-overview.md | 2921 | - [ ] T7366-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T2925-69a663cb | docs/dev/roadmap/v0.2-overview.md | 2922 | - [ ] T7367-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T2926-3ac21272 | docs/dev/roadmap/v0.2-overview.md | 2923 | - [ ] T7368-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T2927-85c9d72d | docs/dev/roadmap/v0.2-overview.md | 2924 | - [ ] T7369-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T2928-c197acb4 | docs/dev/roadmap/v0.2-overview.md | 2925 | - [ ] T7370-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T2929-4bf01b93 | docs/dev/roadmap/v0.2-overview.md | 2926 | - [ ] T7371-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T2930-68069bd6 | docs/dev/roadmap/v0.2-overview.md | 2927 | - [ ] T7372-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T2931-a650c58b | docs/dev/roadmap/v0.2-overview.md | 2928 | - [ ] T7373-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T2932-94d6834b | docs/dev/roadmap/v0.2-overview.md | 2929 | - [ ] T7374-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T2933-692ca644 | docs/dev/roadmap/v0.2-overview.md | 2930 | - [ ] T7375-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T2934-e657d6aa | docs/dev/roadmap/v0.2-overview.md | 2931 | - [ ] T7376-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T2935-6f5e50d4 | docs/dev/roadmap/v0.2-overview.md | 2932 | - [ ] T7377-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T2936-d4d575be | docs/dev/roadmap/v0.2-overview.md | 2933 | - [ ] T7378-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T2937-c1fedcdb | docs/dev/roadmap/v0.2-overview.md | 2934 | - [ ] T7379-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T2938-e556d988 | docs/dev/roadmap/v0.2-overview.md | 2935 | - [ ] T7380-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T2939-7687a914 | docs/dev/roadmap/v0.2-overview.md | 2936 | - [ ] T7381-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T2940-4d69c001 | docs/dev/roadmap/v0.2-overview.md | 2937 | - [ ] T7382-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T2941-d464375f | docs/dev/roadmap/v0.2-overview.md | 2938 | - [ ] T7383-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T2942-d2bf71e3 | docs/dev/roadmap/v0.2-overview.md | 2939 | - [ ] T7384-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T2943-1fc6ff24 | docs/dev/roadmap/v0.2-overview.md | 2940 | - [ ] T7385-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T2944-faa3f6ac | docs/dev/roadmap/v0.2-overview.md | 2941 | - [ ] T7386-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T2945-a4268763 | docs/dev/roadmap/v0.2-overview.md | 2942 | - [ ] T7387-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T2946-d3b196ed | docs/dev/roadmap/v0.2-overview.md | 2943 | - [ ] T7388-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T2947-181bb6f4 | docs/dev/roadmap/v0.2-overview.md | 2944 | - [ ] T7389-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T2948-94cb5cce | docs/dev/roadmap/v0.2-overview.md | 2945 | - [ ] T7390-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T2949-8abb6ef8 | docs/dev/roadmap/v0.2-overview.md | 2946 | - [ ] T7391-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T2950-7bb9c85a | docs/dev/roadmap/v0.2-overview.md | 2947 | - [ ] T7392-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T2951-39306e56 | docs/dev/roadmap/v0.2-overview.md | 2948 | - [ ] T7393-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T2952-b200a180 | docs/dev/roadmap/v0.2-overview.md | 2949 | - [ ] T7394-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T2953-d76cfa31 | docs/dev/roadmap/v0.2-overview.md | 2950 | - [ ] T7395-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T2954-94eaee31 | docs/dev/roadmap/v0.2-overview.md | 2951 | - [ ] T7396-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T2955-f4fde81a | docs/dev/roadmap/v0.2-overview.md | 2952 | - [ ] T7397-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T2956-ab8397ad | docs/dev/roadmap/v0.2-overview.md | 2953 | - [ ] T7398-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T2957-2c8c9b03 | docs/dev/roadmap/v0.2-overview.md | 2954 | - [ ] T7399-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T2958-33416583 | docs/dev/roadmap/v0.2-overview.md | 2955 | - [ ] T7400-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T2959-a8bc7ce9 | docs/dev/roadmap/v0.2-overview.md | 2956 | - [ ] T7401-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T2960-0e5304ab | docs/dev/roadmap/v0.2-overview.md | 2957 | - [ ] T7402-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T2961-b4239a43 | docs/dev/roadmap/v0.2-overview.md | 2958 | - [ ] T7403-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T2962-914303fe | docs/dev/roadmap/v0.2-overview.md | 2959 | - [ ] T7404-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T2963-f5943149 | docs/dev/roadmap/v0.2-overview.md | 2960 | - [ ] T7405-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T2964-0b5fd4a5 | docs/dev/roadmap/v0.2-overview.md | 2961 | - [ ] T7406-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T2965-fa406fa9 | docs/dev/roadmap/v0.2-overview.md | 2962 | - [ ] T7407-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T2966-5802f048 | docs/dev/roadmap/v0.2-overview.md | 2963 | - [ ] T7408-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T2967-895b0a71 | docs/dev/roadmap/v0.2-overview.md | 2964 | - [ ] T7409-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T2968-daf944bf | docs/dev/roadmap/v0.2-overview.md | 2965 | - [ ] T7725-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T2969-e4bd1288 | docs/dev/roadmap/v0.2-overview.md | 2966 | - [ ] T7726-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T2970-5e72a5df | docs/dev/roadmap/v0.2-overview.md | 2967 | - [ ] T7727-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T2971-2822bdc6 | docs/dev/roadmap/v0.2-overview.md | 2968 | - [ ] T7728-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T2972-75edefa1 | docs/dev/roadmap/v0.2-overview.md | 2969 | - [ ] T7729-4c66e9b1 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:155) |
| T2973-f30c0ef2 | docs/dev/roadmap/v0.2-overview.md | 2970 | - [ ] T7730-813e30e1 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:162) |
| T2974-2dd8a7d2 | docs/dev/roadmap/v0.2-overview.md | 2971 | - [ ] T7731-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T2975-f269c4d4 | docs/dev/roadmap/v0.2-overview.md | 2972 | - [ ] T7732-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T2976-004bd1ed | docs/dev/roadmap/v0.2-overview.md | 2973 | - [ ] T7733-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T2977-1c3d7578 | docs/dev/roadmap/v0.2-overview.md | 2974 | - [ ] T7734-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T2978-776f856b | docs/dev/roadmap/v0.2-overview.md | 2975 | - [ ] T7735-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T2979-6d1d6c0b | docs/dev/roadmap/v0.2-overview.md | 2976 | - [ ] T7736-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T2980-4f7556e4 | docs/dev/roadmap/v0.2-overview.md | 2977 | - [ ] T7737-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T2981-2c21adb2 | docs/dev/roadmap/v0.2-overview.md | 2978 | - [ ] T7738-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T2982-a84f146b | docs/dev/roadmap/v0.2-overview.md | 2979 | - [ ] T7739-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T2983-c246adf2 | docs/dev/roadmap/v0.2-overview.md | 2980 | - [ ] T7740-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T2984-ac6508fe | docs/dev/roadmap/v0.2-overview.md | 2981 | - [ ] T7741-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T2985-b1664698 | docs/dev/roadmap/v0.2-overview.md | 2982 | - [ ] T7742-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T2986-c72d0729 | docs/dev/roadmap/v0.2-overview.md | 2983 | - [ ] T7743-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T2987-300a4d68 | docs/dev/roadmap/v0.2-overview.md | 2984 | - [ ] T7744-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T2988-1341b12a | docs/dev/roadmap/v0.2-overview.md | 2985 | - [ ] T7745-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T2989-2310201f | docs/dev/roadmap/v0.2-overview.md | 2986 | - [ ] T7746-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T2990-8dfe12d3 | docs/dev/roadmap/v0.2-overview.md | 2987 | - [ ] T7747-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T2991-485f9c01 | docs/dev/roadmap/v0.2-overview.md | 2988 | - [ ] T7748-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T2992-019a3415 | docs/dev/roadmap/v0.2-overview.md | 2989 | - [ ] T7749-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T2993-af250b12 | docs/dev/roadmap/v0.2-overview.md | 2990 | - [ ] T7750-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T2994-485bd3e8 | docs/dev/roadmap/v0.2-overview.md | 2991 | - [ ] T7751-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T2995-848e6825 | docs/dev/roadmap/v0.2-overview.md | 2992 | - [ ] T7752-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T2996-9c6b9110 | docs/dev/roadmap/v0.2-overview.md | 2993 | - [ ] T7753-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T2997-b1aaf9f3 | docs/dev/roadmap/v0.2-overview.md | 2994 | - [ ] T7754-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T2998-8e8ef661 | docs/dev/roadmap/v0.2-overview.md | 2995 | - [ ] T7755-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T2999-abdcf749 | docs/dev/roadmap/v0.2-overview.md | 2996 | - [ ] T7756-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T3000-2ec37ec3 | docs/dev/roadmap/v0.2-overview.md | 2997 | - [ ] T7757-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T3001-fd4ddc00 | docs/dev/roadmap/v0.2-overview.md | 2998 | - [ ] T7758-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T3002-ff567610 | docs/dev/roadmap/v0.2-overview.md | 2999 | - [ ] T7759-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T3003-7bb1fb65 | docs/dev/roadmap/v0.2-overview.md | 3000 | - [ ] T7760-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T3004-55f60eac | docs/dev/roadmap/v0.2-overview.md | 3001 | - [ ] T7761-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T3005-1deee9dd | docs/dev/roadmap/v0.2-overview.md | 3002 | - [ ] T7762-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T3006-0f9e779d | docs/dev/roadmap/v0.2-overview.md | 3003 | - [ ] T7763-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T3007-ea122fd4 | docs/dev/roadmap/v0.2-overview.md | 3004 | - [ ] T7764-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T3008-2231f2e8 | docs/dev/roadmap/v0.2-overview.md | 3005 | - [ ] T7765-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T3009-87f842c3 | docs/dev/roadmap/v0.2-overview.md | 3006 | - [ ] T7766-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T3010-6f1c9b43 | docs/dev/roadmap/v0.2-overview.md | 3007 | - [ ] T7767-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T3011-2091af9c | docs/dev/roadmap/v0.2-overview.md | 3008 | - [ ] T7768-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T3012-1c64c7fc | docs/dev/roadmap/v0.2-overview.md | 3009 | - [ ] T7769-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T3013-c3fd7b61 | docs/dev/roadmap/v0.2-overview.md | 3010 | - [ ] T7770-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T3014-f9afb142 | docs/dev/roadmap/v0.2-overview.md | 3011 | - [ ] T7771-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T3015-c4186edc | docs/dev/roadmap/v0.2-overview.md | 3012 | - [ ] T7772-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T3016-116ec394 | docs/dev/roadmap/v0.2-overview.md | 3013 | - [ ] T7773-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T3017-1263cac4 | docs/dev/roadmap/v0.2-overview.md | 3014 | - [ ] T7774-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T3018-0795d85e | docs/dev/roadmap/v0.2-overview.md | 3015 | - [ ] T7775-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T3019-65cad74f | docs/dev/roadmap/v0.2-overview.md | 3016 | - [ ] T7776-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T3020-506b00a8 | docs/dev/roadmap/v0.2-overview.md | 3017 | - [ ] T7777-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T3021-1059dd3c | docs/dev/roadmap/v0.2-overview.md | 3018 | - [ ] T7778-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T3022-7c81af74 | docs/dev/roadmap/v0.2-overview.md | 3019 | - [ ] T7779-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T3023-f2d91565 | docs/dev/roadmap/v0.2-overview.md | 3020 | - [ ] T7781-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T3024-279a1aa0 | docs/dev/roadmap/v0.2-overview.md | 3021 | - [ ] T7782-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T3025-63731ba3 | docs/dev/roadmap/v0.2-overview.md | 3022 | - [ ] T7783-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T3026-e57d9243 | docs/dev/roadmap/v0.2-overview.md | 3023 | - [ ] T7784-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T3027-b4c00a81 | docs/dev/roadmap/v0.2-overview.md | 3024 | - [ ] T7785-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T3028-c041cbf3 | docs/dev/roadmap/v0.2-overview.md | 3025 | - [ ] T7786-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T3029-eceb6962 | docs/dev/roadmap/v0.2-overview.md | 3026 | - [ ] T7787-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T3030-aba1a7f7 | docs/dev/roadmap/v0.2-overview.md | 3027 | - [ ] T7788-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T3031-1b5a8ef6 | docs/dev/roadmap/v0.2-overview.md | 3028 | - [ ] T7789-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T3032-0f6990aa | docs/dev/roadmap/v0.2-overview.md | 3029 | - [ ] T7790-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T3033-23c512d1 | docs/dev/roadmap/v0.2-overview.md | 3030 | - [ ] T7791-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T3034-217b7bb3 | docs/dev/roadmap/v0.2-overview.md | 3031 | - [ ] T7792-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T3035-115171b7 | docs/dev/roadmap/v0.2-overview.md | 3032 | - [ ] T7793-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T3036-70c59b23 | docs/dev/roadmap/v0.2-overview.md | 3033 | - [ ] T7794-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T3037-737c545d | docs/dev/roadmap/v0.2-overview.md | 3034 | - [ ] T7795-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T3038-2348a0bb | docs/dev/roadmap/v0.2-overview.md | 3035 | - [ ] T7796-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T3039-e836c958 | docs/dev/roadmap/v0.2-overview.md | 3036 | - [ ] T7797-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T3040-20971692 | docs/dev/roadmap/v0.2-overview.md | 3037 | - [ ] T7798-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T3041-e7fda541 | docs/dev/roadmap/v0.2-overview.md | 3038 | - [ ] T7799-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T3042-9607cb25 | docs/dev/roadmap/v0.2-overview.md | 3039 | - [ ] T7800-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T3043-d452f002 | docs/dev/roadmap/v0.2-overview.md | 3040 | - [ ] T7801-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T3044-1bb31c03 | docs/dev/roadmap/v0.2-overview.md | 3041 | - [ ] T7802-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T3045-710519ee | docs/dev/roadmap/v0.2-overview.md | 3042 | - [ ] T7803-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T3046-409f8486 | docs/dev/roadmap/v0.2-overview.md | 3043 | - [ ] T7804-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T3047-65bde894 | docs/dev/roadmap/v0.2-overview.md | 3044 | - [ ] T7805-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T3048-898ffd48 | docs/dev/roadmap/v0.2-overview.md | 3045 | - [ ] T7806-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T3049-5fd0510b | docs/dev/roadmap/v0.2-overview.md | 3046 | - [ ] T7807-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T3050-4758981a | docs/dev/roadmap/v0.2-overview.md | 3047 | - [ ] T7808-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T3051-78d21fce | docs/dev/roadmap/v0.2-overview.md | 3048 | - [ ] T7809-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T3052-bb897702 | docs/dev/roadmap/v0.2-overview.md | 3049 | - [ ] T7810-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T3053-ff86b80e | docs/dev/roadmap/v0.2-overview.md | 3050 | - [ ] T7811-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T3054-9d4bbc42 | docs/dev/roadmap/v0.2-overview.md | 3051 | - [ ] T7812-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T3055-fa6cb2b1 | docs/dev/roadmap/v0.2-overview.md | 3052 | - [ ] T7813-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T3056-fb83c789 | docs/dev/roadmap/v0.2-overview.md | 3053 | - [ ] T7814-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T3057-13025cc0 | docs/dev/roadmap/v0.2-overview.md | 3054 | - [ ] T7815-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T3058-51ebb7af | docs/dev/roadmap/v0.2-overview.md | 3055 | - [ ] T7816-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T3059-0d665796 | docs/dev/roadmap/v0.2-overview.md | 3056 | - [ ] T7817-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T3060-265265fe | docs/dev/roadmap/v0.2-overview.md | 3057 | - [ ] T7818-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T3061-59f29f34 | docs/dev/roadmap/v0.2-overview.md | 3058 | - [ ] T7819-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T3062-2cbad61c | docs/dev/roadmap/v0.2-overview.md | 3059 | - [ ] T7820-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T3063-fa653658 | docs/dev/roadmap/v0.2-overview.md | 3060 | - [ ] T7821-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T3064-ef413f53 | docs/dev/roadmap/v0.2-overview.md | 3061 | - [ ] T7822-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T3065-acf4204f | docs/dev/roadmap/v0.2-overview.md | 3062 | - [ ] T7823-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T3066-e85d4d0d | docs/dev/roadmap/v0.2-overview.md | 3063 | - [ ] T7824-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T3067-acf13475 | docs/dev/roadmap/v0.2-overview.md | 3064 | - [ ] T7825-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T3068-0b24e7e4 | docs/dev/roadmap/v0.2-overview.md | 3065 | - [ ] T7826-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T3069-54fedcc7 | docs/dev/roadmap/v0.2-overview.md | 3066 | - [ ] T7827-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T3070-b31724fe | docs/dev/roadmap/v0.2-overview.md | 3067 | - [ ] T7828-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T3071-915dd8d3 | docs/dev/roadmap/v0.2-overview.md | 3068 | - [ ] T7829-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T3072-2e1afb9f | docs/dev/roadmap/v0.2-overview.md | 3069 | - [ ] T7830-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T3073-94d88593 | docs/dev/roadmap/v0.2-overview.md | 3070 | - [ ] T7831-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T3074-ca9c2b58 | docs/dev/roadmap/v0.2-overview.md | 3071 | - [ ] T7832-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T3075-8e929af4 | docs/dev/roadmap/v0.2-overview.md | 3072 | - [ ] T7833-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T3076-e11105c0 | docs/dev/roadmap/v0.2-overview.md | 3073 | - [ ] T7834-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T3077-7547237f | docs/dev/roadmap/v0.2-overview.md | 3074 | - [ ] T7835-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T3078-164fc12e | docs/dev/roadmap/v0.2-overview.md | 3075 | - [ ] T7836-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T3079-eb92ca7c | docs/dev/roadmap/v0.2-overview.md | 3076 | - [ ] T7837-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T3080-baf3bdc6 | docs/dev/roadmap/v0.2-overview.md | 3077 | - [ ] T7838-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T3081-9c12113f | docs/dev/roadmap/v0.2-overview.md | 3078 | - [ ] T7839-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T3082-2f376867 | docs/dev/roadmap/v0.2-overview.md | 3079 | - [ ] T7840-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T3083-9c6a2ba7 | docs/dev/roadmap/v0.2-overview.md | 3080 | - [ ] T7841-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T3084-88df6824 | docs/dev/roadmap/v0.2-overview.md | 3081 | - [ ] T7842-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T3085-aa077513 | docs/dev/roadmap/v0.2-overview.md | 3082 | - [ ] T7843-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T3086-5f88dc87 | docs/dev/roadmap/v0.2-overview.md | 3083 | - [ ] T7844-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T3087-3dbecacb | docs/dev/roadmap/v0.2-overview.md | 3084 | - [ ] T7845-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T3088-131fa5eb | docs/dev/roadmap/v0.2-overview.md | 3085 | - [ ] T7846-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T3089-f81cf149 | docs/dev/roadmap/v0.2-overview.md | 3086 | - [ ] T7847-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T3090-46ba9fb8 | docs/dev/roadmap/v0.2-overview.md | 3087 | - [ ] T7848-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T3091-09aaa599 | docs/dev/roadmap/v0.2-overview.md | 3088 | - [ ] T7849-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T3092-43773f5c | docs/dev/roadmap/v0.2-overview.md | 3089 | - [ ] T7850-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T3093-1888e53f | docs/dev/roadmap/v0.2-overview.md | 3090 | - [ ] T7851-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T3094-f43156d6 | docs/dev/roadmap/v0.2-overview.md | 3091 | - [ ] T7852-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T3095-8195c3ef | docs/dev/roadmap/v0.2-overview.md | 3092 | - [ ] T7853-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T3096-282e1c44 | docs/dev/roadmap/v0.2-overview.md | 3093 | - [ ] T7854-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T3097-80dbdf8e | docs/dev/roadmap/v0.2-overview.md | 3094 | - [ ] T7855-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T3098-53a0f90a | docs/dev/roadmap/v0.2-overview.md | 3095 | - [ ] T7856-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T3099-3bd51254 | docs/dev/roadmap/v0.2-overview.md | 3096 | - [ ] T7857-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T3100-bf4f7de0 | docs/dev/roadmap/v0.2-overview.md | 3097 | - [ ] T7858-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T3101-c2e210f0 | docs/dev/roadmap/v0.2-overview.md | 3098 | - [ ] T7860-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T3102-e9cf5117 | docs/dev/roadmap/v0.2-overview.md | 3099 | - [ ] T7861-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T3103-612d9cf8 | docs/dev/roadmap/v0.2-overview.md | 3100 | - [ ] T7862-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T3104-d5b63037 | docs/dev/roadmap/v0.2-overview.md | 3101 | - [ ] T7863-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T3105-03f0c7c3 | docs/dev/roadmap/v0.2-overview.md | 3102 | - [ ] T7864-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T3106-8c1c4846 | docs/dev/roadmap/v0.2-overview.md | 3103 | - [ ] T7865-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T3107-47245ce5 | docs/dev/roadmap/v0.2-overview.md | 3104 | - [ ] T7866-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T3108-05c0c37f | docs/dev/roadmap/v0.2-overview.md | 3105 | - [ ] T7867-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T3109-2edf2eb1 | docs/dev/roadmap/v0.2-overview.md | 3106 | - [ ] T7868-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T3110-eb422667 | docs/dev/roadmap/v0.2-overview.md | 3107 | - [ ] T7869-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T3111-dc10787f | docs/dev/roadmap/v0.2-overview.md | 3108 | - [ ] T7870-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T3112-e9cdb92b | docs/dev/roadmap/v0.2-overview.md | 3109 | - [ ] T7871-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T3113-acee6181 | docs/dev/roadmap/v0.2-overview.md | 3110 | - [ ] T7872-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T3114-ea2b3d65 | docs/dev/roadmap/v0.2-overview.md | 3111 | - [ ] T7873-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T3115-037dfee5 | docs/dev/roadmap/v0.2-overview.md | 3112 | - [ ] T7874-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T3116-d4284963 | docs/dev/roadmap/v0.2-overview.md | 3113 | - [ ] T7875-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T3117-7f16a70e | docs/dev/roadmap/v0.2-overview.md | 3114 | - [ ] T7876-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T3118-188a34c4 | docs/dev/roadmap/v0.2-overview.md | 3115 | - [ ] T7877-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T3119-7d483ad2 | docs/dev/roadmap/v0.2-overview.md | 3116 | - [ ] T7878-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T3120-647fcba1 | docs/dev/roadmap/v0.2-overview.md | 3117 | - [ ] T7879-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T3121-d503ac0b | docs/dev/roadmap/v0.2-overview.md | 3118 | - [ ] T7880-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T3122-b4dbec6c | docs/dev/roadmap/v0.2-overview.md | 3119 | - [ ] T7881-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T3123-da53f85f | docs/dev/roadmap/v0.2-overview.md | 3120 | - [ ] T7882-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T3124-caf3caa7 | docs/dev/roadmap/v0.2-overview.md | 3121 | - [ ] T7883-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T3125-530fd13e | docs/dev/roadmap/v0.2-overview.md | 3122 | - [ ] T7884-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T3126-8358b09d | docs/dev/roadmap/v0.2-overview.md | 3123 | - [ ] T7885-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T3127-e77769f4 | docs/dev/roadmap/v0.2-overview.md | 3124 | - [ ] T7886-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T3128-c1d9a043 | docs/dev/roadmap/v0.2-overview.md | 3125 | - [ ] T7887-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T3129-56da6440 | docs/dev/roadmap/v0.2-overview.md | 3126 | - [ ] T7888-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T3130-44d98a2c | docs/dev/roadmap/v0.2-overview.md | 3127 | - [ ] T7889-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T3131-5b759368 | docs/dev/roadmap/v0.2-overview.md | 3128 | - [ ] T7890-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T3132-92de7c33 | docs/dev/roadmap/v0.2-overview.md | 3129 | - [ ] T7891-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T3133-85b3a1d8 | docs/dev/roadmap/v0.2-overview.md | 3130 | - [ ] T7892-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T3134-7608accc | docs/dev/roadmap/v0.2-overview.md | 3131 | - [ ] T7893-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T3135-e7991323 | docs/dev/roadmap/v0.2-overview.md | 3132 | - [ ] T7894-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T3136-ee55fd8d | docs/dev/roadmap/v0.2-overview.md | 3133 | - [ ] T7895-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T3137-a4d8114f | docs/dev/roadmap/v0.2-overview.md | 3134 | - [ ] T7896-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T3138-2993803a | docs/dev/roadmap/v0.2-overview.md | 3135 | - [ ] T7897-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T3139-7adfd861 | docs/dev/roadmap/v0.2-overview.md | 3136 | - [ ] T7898-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T3140-8e384539 | docs/dev/roadmap/v0.2-overview.md | 3137 | - [ ] T7899-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T3141-60a1e386 | docs/dev/roadmap/v0.2-overview.md | 3138 | - [ ] T7900-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T3142-dee6c6e8 | docs/dev/roadmap/v0.2-overview.md | 3139 | - [ ] T7901-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T3143-f748f657 | docs/dev/roadmap/v0.2-overview.md | 3140 | - [ ] T7902-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T3144-3cb4375f | docs/dev/roadmap/v0.2-overview.md | 3141 | - [ ] T7903-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T3145-7dbc1973 | docs/dev/roadmap/v0.2-overview.md | 3142 | - [ ] T7904-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T3146-c4029da2 | docs/dev/roadmap/v0.2-overview.md | 3143 | - [ ] T7905-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T3147-f53c01e6 | docs/dev/roadmap/v0.2-overview.md | 3144 | - [ ] T7906-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T3148-e73e1700 | docs/dev/roadmap/v0.2-overview.md | 3145 | - [ ] T7907-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T3149-b6c0dc57 | docs/dev/roadmap/v0.2-overview.md | 3146 | - [ ] T7908-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T3150-7f8118bf | docs/dev/roadmap/v0.2-overview.md | 3147 | - [ ] T7909-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T3151-d32815d6 | docs/dev/roadmap/v0.2-overview.md | 3148 | - [ ] T7910-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T3152-88b0ff04 | docs/dev/roadmap/v0.2-overview.md | 3149 | - [ ] T7911-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T3153-d32e73d4 | docs/dev/roadmap/v0.2-overview.md | 3150 | - [ ] T7912-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T3154-ae5cd0c8 | docs/dev/roadmap/v0.2-overview.md | 3151 | - [ ] T7913-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T3155-323efee6 | docs/dev/roadmap/v0.2-overview.md | 3152 | - [ ] T7914-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T3156-e9527e5a | docs/dev/roadmap/v0.2-overview.md | 3153 | - [ ] T7915-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T3157-d267efeb | docs/dev/roadmap/v0.2-overview.md | 3154 | - [ ] T7916-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T3158-960ccc57 | docs/dev/roadmap/v0.2-overview.md | 3155 | - [ ] T7918-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T3159-9b80bc16 | docs/dev/roadmap/v0.2-overview.md | 3156 | - [ ] T7919-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T3160-36d66534 | docs/dev/roadmap/v0.2-overview.md | 3157 | - [ ] T7920-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T3161-337fb4ff | docs/dev/roadmap/v0.2-overview.md | 3158 | - [ ] T7921-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T3162-7653cf21 | docs/dev/roadmap/v0.2-overview.md | 3159 | - [ ] T7922-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T3163-a475b53c | docs/dev/roadmap/v0.2-overview.md | 3160 | - [ ] T7923-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T3164-c760b04f | docs/dev/roadmap/v0.2-overview.md | 3161 | - [ ] T7924-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T3165-ed6fc196 | docs/dev/roadmap/v0.2-overview.md | 3162 | - [ ] T7925-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T3166-b0c75f97 | docs/dev/roadmap/v0.2-overview.md | 3163 | - [ ] T7926-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T3167-a1a11d4d | docs/dev/roadmap/v0.2-overview.md | 3164 | - [ ] T7927-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T3168-91fb9936 | docs/dev/roadmap/v0.2-overview.md | 3165 | - [ ] T7928-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T3169-ecb66a9c | docs/dev/roadmap/v0.2-overview.md | 3166 | - [ ] T7929-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T3170-8103655e | docs/dev/roadmap/v0.2-overview.md | 3167 | - [ ] T7930-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T3171-4594991f | docs/dev/roadmap/v0.2-overview.md | 3168 | - [ ] T7931-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T3172-526e681e | docs/dev/roadmap/v0.2-overview.md | 3169 | - [ ] T7932-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T3173-0df60460 | docs/dev/roadmap/v0.2-overview.md | 3170 | - [ ] T7933-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T3174-33cbeea3 | docs/dev/roadmap/v0.2-overview.md | 3171 | - [ ] T7934-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T3175-c73e5628 | docs/dev/roadmap/v0.2-overview.md | 3172 | - [ ] T7935-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T3176-8fe53766 | docs/dev/roadmap/v0.2-overview.md | 3173 | - [ ] T7936-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T3177-ac262855 | docs/dev/roadmap/v0.2-overview.md | 3174 | - [ ] T7937-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T3178-d1f48563 | docs/dev/roadmap/v0.2-overview.md | 3175 | - [ ] T7938-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T3179-4e67548e | docs/dev/roadmap/v0.2-overview.md | 3176 | - [ ] T7939-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T3180-892713cd | docs/dev/roadmap/v0.2-overview.md | 3177 | - [ ] T7940-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T3181-c54821df | docs/dev/roadmap/v0.2-overview.md | 3178 | - [ ] T7941-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T3182-99617c03 | docs/dev/roadmap/v0.2-overview.md | 3179 | - [ ] T7942-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T3183-31c9202e | docs/dev/roadmap/v0.2-overview.md | 3180 | - [ ] T7943-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T3184-5e0d83b5 | docs/dev/roadmap/v0.2-overview.md | 3181 | - [ ] T7944-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T3185-e01a6365 | docs/dev/roadmap/v0.2-overview.md | 3182 | - [ ] T7945-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T3186-cc6dec41 | docs/dev/roadmap/v0.2-overview.md | 3183 | - [ ] T7946-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T3187-22b624cf | docs/dev/roadmap/v0.2-overview.md | 3184 | - [ ] T7947-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T3188-c4cba2ca | docs/dev/roadmap/v0.2-overview.md | 3185 | - [ ] T7948-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T3189-ee0284b7 | docs/dev/roadmap/v0.2-overview.md | 3186 | - [ ] T7949-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T3190-b1a82dc5 | docs/dev/roadmap/v0.2-overview.md | 3187 | - [ ] T7950-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T3191-e70d2c79 | docs/dev/roadmap/v0.2-overview.md | 3188 | - [ ] T7951-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T3192-921e2542 | docs/dev/roadmap/v0.2-overview.md | 3189 | - [ ] T7952-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T3193-f7c1afe3 | docs/dev/roadmap/v0.2-overview.md | 3190 | - [ ] T7953-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T3194-97e475f8 | docs/dev/roadmap/v0.2-overview.md | 3191 | - [ ] T7954-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T3195-461d32d1 | docs/dev/roadmap/v0.2-overview.md | 3192 | - [ ] T7955-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T3196-0f2f5111 | docs/dev/roadmap/v0.2-overview.md | 3193 | - [ ] T7956-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T3197-1acb825d | docs/dev/roadmap/v0.2-overview.md | 3194 | - [ ] T7957-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T3198-dbe4ca00 | docs/dev/roadmap/v0.2-overview.md | 3195 | - [ ] T7958-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T3199-045661f9 | docs/dev/roadmap/v0.2-overview.md | 3196 | - [ ] T7959-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T3200-7bec35ca | docs/dev/roadmap/v0.2-overview.md | 3197 | - [ ] T7960-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T3201-fff65e19 | docs/dev/roadmap/v0.2-overview.md | 3198 | - [ ] T7961-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T3202-f1f20fe9 | docs/dev/roadmap/v0.2-overview.md | 3199 | - [ ] T7962-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T3203-1abf76d9 | docs/dev/roadmap/v0.2-overview.md | 3200 | - [ ] T7963-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T3204-7b915dd6 | docs/dev/roadmap/v0.2-overview.md | 3201 | - [ ] T7964-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T3205-fd5bd168 | docs/dev/roadmap/v0.2-overview.md | 3202 | - [ ] T7965-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T3206-ed68b812 | docs/dev/roadmap/v0.2-overview.md | 3203 | - [ ] T7966-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T3207-4924ec28 | docs/dev/roadmap/v0.2-overview.md | 3204 | - [ ] T7967-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T3208-c3a8c4ec | docs/dev/roadmap/v0.2-overview.md | 3205 | - [ ] T7968-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T3209-6a3898e4 | docs/dev/roadmap/v0.2-overview.md | 3206 | - [ ] T7969-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T3210-5841a5ed | docs/dev/roadmap/v0.2-overview.md | 3207 | - [ ] T7970-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T3211-ef75a6ad | docs/dev/roadmap/v0.2-overview.md | 3208 | - [ ] T7971-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T3212-65988d57 | docs/dev/roadmap/v0.2-overview.md | 3209 | - [ ] T7972-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T3213-dc46fc49 | docs/dev/roadmap/v0.2-overview.md | 3210 | - [ ] T7973-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T3214-6554bf84 | docs/dev/roadmap/v0.2-overview.md | 3211 | - [ ] T7974-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T3215-3ac9ca74 | docs/dev/roadmap/v0.2-overview.md | 3212 | - [ ] T7975-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T3216-3eef6033 | docs/dev/roadmap/v0.2-overview.md | 3213 | - [ ] T7976-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T3217-7c10d231 | docs/dev/roadmap/v0.2-overview.md | 3214 | - [ ] T7977-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T3218-58af153a | docs/dev/roadmap/v0.2-overview.md | 3215 | - [ ] T7978-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T3219-ef33c029 | docs/dev/roadmap/v0.2-overview.md | 3216 | - [ ] T7979-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T3220-904fd4ca | docs/dev/roadmap/v0.2-overview.md | 3217 | - [ ] T7980-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T3221-54bd23f8 | docs/dev/roadmap/v0.2-overview.md | 3218 | - [ ] T7981-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T3222-280e399a | docs/dev/roadmap/v0.2-overview.md | 3219 | - [ ] T7982-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T3223-6b02fe96 | docs/dev/roadmap/v0.2-overview.md | 3220 | - [ ] T7983-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T3224-713e5ec9 | docs/dev/roadmap/v0.2-overview.md | 3221 | - [ ] T7984-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T3225-57448b63 | docs/dev/roadmap/v0.2-overview.md | 3222 | - [ ] T7985-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T3226-ff60a3ae | docs/dev/roadmap/v0.2-overview.md | 3223 | - [ ] T7986-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T3227-7ee05fc4 | docs/dev/roadmap/v0.2-overview.md | 3224 | - [ ] T7987-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T3228-c1f40905 | docs/dev/roadmap/v0.2-overview.md | 3225 | - [ ] T7988-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T3229-5c357641 | docs/dev/roadmap/v0.2-overview.md | 3226 | - [ ] T7989-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T3230-82aa514e | docs/dev/roadmap/v0.2-overview.md | 3227 | - [ ] T7990-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T3231-fe1299fb | docs/dev/roadmap/v0.2-overview.md | 3228 | - [ ] T7991-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T3232-579297be | docs/dev/roadmap/v0.2-overview.md | 3229 | - [ ] T7992-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T3233-640fa897 | docs/dev/roadmap/v0.2-overview.md | 3230 | - [ ] T7993-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T3234-499f595d | docs/dev/roadmap/v0.2-overview.md | 3231 | - [ ] T7994-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T3235-409af115 | docs/dev/roadmap/v0.2-overview.md | 3232 | - [ ] T7995-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T3236-703e2e00 | docs/dev/roadmap/v0.2-overview.md | 3233 | - [ ] T7996-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T3237-3e49b7cb | docs/dev/roadmap/v0.2-overview.md | 3234 | - [ ] T7997-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T3238-8b3a8dd3 | docs/dev/roadmap/v0.2-overview.md | 3235 | - [ ] T7998-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T3239-5875c4e7 | docs/dev/roadmap/v0.2-overview.md | 3236 | - [ ] T7999-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T3240-fa6e6d39 | docs/dev/roadmap/v0.2-overview.md | 3237 | - [ ] T8000-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T3241-982adbff | docs/dev/roadmap/v0.2-overview.md | 3238 | - [ ] T8001-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T3242-f0fa5660 | docs/dev/roadmap/v0.2-overview.md | 3239 | - [ ] T8002-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T3243-1ce2693b | docs/dev/roadmap/v0.2-overview.md | 3240 | - [ ] T8003-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T3244-92f53169 | docs/dev/roadmap/v0.2-overview.md | 3241 | - [ ] T8004-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T3245-89ae73b6 | docs/dev/roadmap/v0.2-overview.md | 3242 | - [ ] T8005-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T3246-e35f46dc | docs/dev/roadmap/v0.2-overview.md | 3243 | - [ ] T8006-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T3247-416fb08e | docs/dev/roadmap/v0.2-overview.md | 3244 | - [ ] T8007-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T3248-963b3612 | docs/dev/roadmap/v0.2-overview.md | 3245 | - [ ] T8008-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T3249-92c849e2 | docs/dev/roadmap/v0.2-overview.md | 3246 | - [ ] T8009-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T3250-74a59af8 | docs/dev/roadmap/v0.2-overview.md | 3247 | - [ ] T8010-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T3251-73116d7f | docs/dev/roadmap/v0.2-overview.md | 3248 | - [ ] T8011-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T3252-7970f08b | docs/dev/roadmap/v0.2-overview.md | 3249 | - [ ] T8012-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T3253-57db0b52 | docs/dev/roadmap/v0.2-overview.md | 3250 | - [ ] T8013-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T3254-2fab9c5a | docs/dev/roadmap/v0.2-overview.md | 3251 | - [ ] T8014-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T3255-9d7207d9 | docs/dev/roadmap/v0.2-overview.md | 3252 | - [ ] T8015-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T3256-1510a0cb | docs/dev/roadmap/v0.2-overview.md | 3253 | - [ ] T8016-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T3257-82d5f0b7 | docs/dev/roadmap/v0.2-overview.md | 3254 | - [ ] T8017-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T3258-a2b4086d | docs/dev/roadmap/v0.2-overview.md | 3255 | - [ ] T8018-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T3259-ddd76167 | docs/dev/roadmap/v0.2-overview.md | 3256 | - [ ] T8019-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T3260-4c687dba | docs/dev/roadmap/v0.2-overview.md | 3257 | - [ ] T8020-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T3261-9b1e6253 | docs/dev/roadmap/v0.2-overview.md | 3258 | - [ ] T8021-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T3262-b04c43a9 | docs/dev/roadmap/v0.2-overview.md | 3259 | - [ ] T8022-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T3263-acde92dc | docs/dev/roadmap/v0.2-overview.md | 3260 | - [ ] T8023-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T3264-725895e8 | docs/dev/roadmap/v0.2-overview.md | 3261 | - [ ] T8024-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T3265-420114fd | docs/dev/roadmap/v0.2-overview.md | 3262 | - [ ] T8025-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T3266-111853cb | docs/dev/roadmap/v0.2-overview.md | 3263 | - [ ] T8026-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T3267-9d5b1844 | docs/dev/roadmap/v0.2-overview.md | 3264 | - [ ] T8027-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T3268-447713d0 | docs/dev/roadmap/v0.2-overview.md | 3265 | - [ ] T8028-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T3269-fd7a9a83 | docs/dev/roadmap/v0.2-overview.md | 3266 | - [ ] T8029-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T3270-a20c9ebe | docs/dev/roadmap/v0.2-overview.md | 3267 | - [ ] T8030-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T3271-26c4b1ea | docs/dev/roadmap/v0.2-overview.md | 3268 | - [ ] T8031-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T3272-332d781a | docs/dev/roadmap/v0.2-overview.md | 3269 | - [ ] T8032-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T3273-92cc6665 | docs/dev/roadmap/v0.2-overview.md | 3270 | - [ ] T8033-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T3274-d5b80ea5 | docs/dev/roadmap/v0.2-overview.md | 3271 | - [ ] T8034-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T3275-25e7c272 | docs/dev/roadmap/v0.2-overview.md | 3272 | - [ ] T8035-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T3276-3a46eead | docs/dev/roadmap/v0.2-overview.md | 3273 | - [ ] T8036-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T3277-d1b874db | docs/dev/roadmap/v0.2-overview.md | 3274 | - [ ] T8037-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T3278-ab83c45b | docs/dev/roadmap/v0.2-overview.md | 3275 | - [ ] T8038-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T3279-5366ed2e | docs/dev/roadmap/v0.2-overview.md | 3276 | - [ ] T8039-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T3280-6926ce4c | docs/dev/roadmap/v0.2-overview.md | 3277 | - [ ] T8040-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T3281-beffc886 | docs/dev/roadmap/v0.2-overview.md | 3278 | - [ ] T8041-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T3282-d35a21a5 | docs/dev/roadmap/v0.2-overview.md | 3279 | - [ ] T8042-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T3283-37944db1 | docs/dev/roadmap/v0.2-overview.md | 3280 | - [ ] T8043-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T3284-341bd275 | docs/dev/roadmap/v0.2-overview.md | 3281 | - [ ] T8044-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T3285-a90ffa62 | docs/dev/roadmap/v0.2-overview.md | 3282 | - [ ] T8045-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T3286-ff99d95b | docs/dev/roadmap/v0.2-overview.md | 3283 | - [ ] T8290-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T3287-8485af75 | docs/dev/roadmap/v0.2-overview.md | 3284 | - [ ] T8291-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T3288-9d41edc0 | docs/dev/roadmap/v0.2-overview.md | 3285 | - [ ] T8292-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T3289-603728db | docs/dev/roadmap/v0.2-overview.md | 3286 | - [ ] T8293-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T3290-53312a21 | docs/dev/roadmap/v0.2-overview.md | 3287 | - [ ] T8294-4c66e9b1 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:155) |
| T3291-b808f297 | docs/dev/roadmap/v0.2-overview.md | 3288 | - [ ] T8295-813e30e1 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:162) |
| T3292-7f589937 | docs/dev/roadmap/v0.2-overview.md | 3289 | - [ ] T8296-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T3293-476ff199 | docs/dev/roadmap/v0.2-overview.md | 3290 | - [ ] T8297-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T3294-19127714 | docs/dev/roadmap/v0.2-overview.md | 3291 | - [ ] T8298-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T3295-723f67a2 | docs/dev/roadmap/v0.2-overview.md | 3292 | - [ ] T8299-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T3296-b1082de6 | docs/dev/roadmap/v0.2-overview.md | 3293 | - [ ] T8300-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T3297-d465c1c0 | docs/dev/roadmap/v0.2-overview.md | 3294 | - [ ] T8301-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T3298-33c5cce2 | docs/dev/roadmap/v0.2-overview.md | 3295 | - [ ] T8302-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T3299-75871133 | docs/dev/roadmap/v0.2-overview.md | 3296 | - [ ] T8303-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T3300-e4b11713 | docs/dev/roadmap/v0.2-overview.md | 3297 | - [ ] T8304-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T3301-d327ec29 | docs/dev/roadmap/v0.2-overview.md | 3298 | - [ ] T8305-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T3302-0406f15f | docs/dev/roadmap/v0.2-overview.md | 3299 | - [ ] T8306-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T3303-47caf032 | docs/dev/roadmap/v0.2-overview.md | 3300 | - [ ] T8307-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T3304-4e87d690 | docs/dev/roadmap/v0.2-overview.md | 3301 | - [ ] T8308-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T3305-c713610f | docs/dev/roadmap/v0.2-overview.md | 3302 | - [ ] T8309-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T3306-cec4841b | docs/dev/roadmap/v0.2-overview.md | 3303 | - [ ] T8310-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T3307-fe998c5a | docs/dev/roadmap/v0.2-overview.md | 3304 | - [ ] T8311-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T3308-3ae230ba | docs/dev/roadmap/v0.2-overview.md | 3305 | - [ ] T8312-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T3309-23d7e18e | docs/dev/roadmap/v0.2-overview.md | 3306 | - [ ] T8313-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T3310-7f3b0d1d | docs/dev/roadmap/v0.2-overview.md | 3307 | - [ ] T8314-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T3311-45f60589 | docs/dev/roadmap/v0.2-overview.md | 3308 | - [ ] T8315-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T3312-c32418e0 | docs/dev/roadmap/v0.2-overview.md | 3309 | - [ ] T8316-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T3313-3b1a384d | docs/dev/roadmap/v0.2-overview.md | 3310 | - [ ] T8317-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T3314-cadd38ff | docs/dev/roadmap/v0.2-overview.md | 3311 | - [ ] T8318-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T3315-b8a0dda2 | docs/dev/roadmap/v0.2-overview.md | 3312 | - [ ] T8319-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T3316-1e9f4c99 | docs/dev/roadmap/v0.2-overview.md | 3313 | - [ ] T8320-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T3317-d2d2e9b4 | docs/dev/roadmap/v0.2-overview.md | 3314 | - [ ] T8321-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T3318-b1d803b6 | docs/dev/roadmap/v0.2-overview.md | 3315 | - [ ] T8322-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T3319-296a9e89 | docs/dev/roadmap/v0.2-overview.md | 3316 | - [ ] T8323-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T3320-54b3f965 | docs/dev/roadmap/v0.2-overview.md | 3317 | - [ ] T8324-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T3321-5b4bb744 | docs/dev/roadmap/v0.2-overview.md | 3318 | - [ ] T8325-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T3322-fd9558a8 | docs/dev/roadmap/v0.2-overview.md | 3319 | - [ ] T8326-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T3323-f3143f38 | docs/dev/roadmap/v0.2-overview.md | 3320 | - [ ] T8327-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T3324-cc48f366 | docs/dev/roadmap/v0.2-overview.md | 3321 | - [ ] T8328-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T3325-5e82e105 | docs/dev/roadmap/v0.2-overview.md | 3322 | - [ ] T8329-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T3326-3354c102 | docs/dev/roadmap/v0.2-overview.md | 3323 | - [ ] T8330-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T3327-eeb9ffdf | docs/dev/roadmap/v0.2-overview.md | 3324 | - [ ] T8331-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T3328-99098d1d | docs/dev/roadmap/v0.2-overview.md | 3325 | - [ ] T8332-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T3329-8a2aabd6 | docs/dev/roadmap/v0.2-overview.md | 3326 | - [ ] T8333-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T3330-f2a39ef2 | docs/dev/roadmap/v0.2-overview.md | 3327 | - [ ] T8334-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T3331-e582b218 | docs/dev/roadmap/v0.2-overview.md | 3328 | - [ ] T8335-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T3332-7ba9b7e8 | docs/dev/roadmap/v0.2-overview.md | 3329 | - [ ] T8336-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T3333-86999d12 | docs/dev/roadmap/v0.2-overview.md | 3330 | - [ ] T8337-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T3334-1f9d0390 | docs/dev/roadmap/v0.2-overview.md | 3331 | - [ ] T8338-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T3335-1090ffd6 | docs/dev/roadmap/v0.2-overview.md | 3332 | - [ ] T8339-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T3336-b3fbd070 | docs/dev/roadmap/v0.2-overview.md | 3333 | - [ ] T8340-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T3337-bc48711c | docs/dev/roadmap/v0.2-overview.md | 3334 | - [ ] T8341-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T3338-b50358d5 | docs/dev/roadmap/v0.2-overview.md | 3335 | - [ ] T8342-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T3339-f94d9ff5 | docs/dev/roadmap/v0.2-overview.md | 3336 | - [ ] T8343-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T3340-7ddd8a4d | docs/dev/roadmap/v0.2-overview.md | 3337 | - [ ] T8344-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T3341-d74c08c3 | docs/dev/roadmap/v0.2-overview.md | 3338 | - [ ] T8346-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T3342-fe9e6f65 | docs/dev/roadmap/v0.2-overview.md | 3339 | - [ ] T8347-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T3343-b5c54e74 | docs/dev/roadmap/v0.2-overview.md | 3340 | - [ ] T8348-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T3344-7739b01a | docs/dev/roadmap/v0.2-overview.md | 3341 | - [ ] T8349-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T3345-c23d2b5e | docs/dev/roadmap/v0.2-overview.md | 3342 | - [ ] T8350-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T3346-34095536 | docs/dev/roadmap/v0.2-overview.md | 3343 | - [ ] T8351-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T3347-3e02f394 | docs/dev/roadmap/v0.2-overview.md | 3344 | - [ ] T8352-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T3348-d4f6ee07 | docs/dev/roadmap/v0.2-overview.md | 3345 | - [ ] T8353-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T3349-a7b16378 | docs/dev/roadmap/v0.2-overview.md | 3346 | - [ ] T8354-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T3350-9c683735 | docs/dev/roadmap/v0.2-overview.md | 3347 | - [ ] T8355-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T3351-fd9420b2 | docs/dev/roadmap/v0.2-overview.md | 3348 | - [ ] T8356-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T3352-fd7216b4 | docs/dev/roadmap/v0.2-overview.md | 3349 | - [ ] T8357-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T3353-9e0ec73a | docs/dev/roadmap/v0.2-overview.md | 3350 | - [ ] T8358-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T3354-4cb783e3 | docs/dev/roadmap/v0.2-overview.md | 3351 | - [ ] T8359-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T3355-4d931f2b | docs/dev/roadmap/v0.2-overview.md | 3352 | - [ ] T8360-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T3356-a49631e5 | docs/dev/roadmap/v0.2-overview.md | 3353 | - [ ] T8361-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T3357-816e337e | docs/dev/roadmap/v0.2-overview.md | 3354 | - [ ] T8362-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T3358-b4865379 | docs/dev/roadmap/v0.2-overview.md | 3355 | - [ ] T8363-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T3359-5144e16a | docs/dev/roadmap/v0.2-overview.md | 3356 | - [ ] T8364-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T3360-a6791066 | docs/dev/roadmap/v0.2-overview.md | 3357 | - [ ] T8365-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T3361-9b092dd2 | docs/dev/roadmap/v0.2-overview.md | 3358 | - [ ] T8366-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T3362-6ad4c468 | docs/dev/roadmap/v0.2-overview.md | 3359 | - [ ] T8367-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T3363-4ec72eb1 | docs/dev/roadmap/v0.2-overview.md | 3360 | - [ ] T8368-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T3364-300e785d | docs/dev/roadmap/v0.2-overview.md | 3361 | - [ ] T8369-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T3365-635e8b96 | docs/dev/roadmap/v0.2-overview.md | 3362 | - [ ] T8370-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T3366-c314d8b4 | docs/dev/roadmap/v0.2-overview.md | 3363 | - [ ] T8371-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T3367-513e47ca | docs/dev/roadmap/v0.2-overview.md | 3364 | - [ ] T8372-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T3368-9bb7d618 | docs/dev/roadmap/v0.2-overview.md | 3365 | - [ ] T8373-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T3369-ef51d752 | docs/dev/roadmap/v0.2-overview.md | 3366 | - [ ] T8374-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T3370-72e7379d | docs/dev/roadmap/v0.2-overview.md | 3367 | - [ ] T8375-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T3371-72533739 | docs/dev/roadmap/v0.2-overview.md | 3368 | - [ ] T8376-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T3372-c356a391 | docs/dev/roadmap/v0.2-overview.md | 3369 | - [ ] T8377-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T3373-06a3fe7e | docs/dev/roadmap/v0.2-overview.md | 3370 | - [ ] T8378-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T3374-d1d46eee | docs/dev/roadmap/v0.2-overview.md | 3371 | - [ ] T8379-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T3375-a702bcd3 | docs/dev/roadmap/v0.2-overview.md | 3372 | - [ ] T8380-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T3376-96372c87 | docs/dev/roadmap/v0.2-overview.md | 3373 | - [ ] T8381-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T3377-847e63d5 | docs/dev/roadmap/v0.2-overview.md | 3374 | - [ ] T8382-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T3378-414a378e | docs/dev/roadmap/v0.2-overview.md | 3375 | - [ ] T8383-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T3379-2f99906d | docs/dev/roadmap/v0.2-overview.md | 3376 | - [ ] T8384-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T3380-9462f100 | docs/dev/roadmap/v0.2-overview.md | 3377 | - [ ] T8385-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T3381-5c7a795b | docs/dev/roadmap/v0.2-overview.md | 3378 | - [ ] T8386-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T3382-6a95a5b3 | docs/dev/roadmap/v0.2-overview.md | 3379 | - [ ] T8387-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T3383-77afb479 | docs/dev/roadmap/v0.2-overview.md | 3380 | - [ ] T8388-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T3384-c3d19320 | docs/dev/roadmap/v0.2-overview.md | 3381 | - [ ] T8389-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T3385-4827e2d5 | docs/dev/roadmap/v0.2-overview.md | 3382 | - [ ] T8390-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T3386-9ae71094 | docs/dev/roadmap/v0.2-overview.md | 3383 | - [ ] T8391-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T3387-8b9e0795 | docs/dev/roadmap/v0.2-overview.md | 3384 | - [ ] T8392-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T3388-8a106618 | docs/dev/roadmap/v0.2-overview.md | 3385 | - [ ] T8393-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T3389-797ccfb4 | docs/dev/roadmap/v0.2-overview.md | 3386 | - [ ] T8394-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T3390-e8272565 | docs/dev/roadmap/v0.2-overview.md | 3387 | - [ ] T8395-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T3391-439c5362 | docs/dev/roadmap/v0.2-overview.md | 3388 | - [ ] T8396-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T3392-2b66a696 | docs/dev/roadmap/v0.2-overview.md | 3389 | - [ ] T8397-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T3393-4fa39848 | docs/dev/roadmap/v0.2-overview.md | 3390 | - [ ] T8398-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T3394-728f2af8 | docs/dev/roadmap/v0.2-overview.md | 3391 | - [ ] T8399-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T3395-25a6ef62 | docs/dev/roadmap/v0.2-overview.md | 3392 | - [ ] T8400-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T3396-0ea9848e | docs/dev/roadmap/v0.2-overview.md | 3393 | - [ ] T8401-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T3397-99062073 | docs/dev/roadmap/v0.2-overview.md | 3394 | - [ ] T8402-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T3398-3fdcd1e6 | docs/dev/roadmap/v0.2-overview.md | 3395 | - [ ] T8403-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T3399-f6337cb4 | docs/dev/roadmap/v0.2-overview.md | 3396 | - [ ] T8404-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T3400-12ea02f7 | docs/dev/roadmap/v0.2-overview.md | 3397 | - [ ] T8405-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T3401-df2dd167 | docs/dev/roadmap/v0.2-overview.md | 3398 | - [ ] T8406-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T3402-5189225a | docs/dev/roadmap/v0.2-overview.md | 3399 | - [ ] T8407-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T3403-78059d3d | docs/dev/roadmap/v0.2-overview.md | 3400 | - [ ] T8408-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T3404-89641b45 | docs/dev/roadmap/v0.2-overview.md | 3401 | - [ ] T8409-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T3405-bd684c86 | docs/dev/roadmap/v0.2-overview.md | 3402 | - [ ] T8410-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T3406-99348ea4 | docs/dev/roadmap/v0.2-overview.md | 3403 | - [ ] T8411-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T3407-d351ee7d | docs/dev/roadmap/v0.2-overview.md | 3404 | - [ ] T8412-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T3408-cba177ad | docs/dev/roadmap/v0.2-overview.md | 3405 | - [ ] T8413-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T3409-04526031 | docs/dev/roadmap/v0.2-overview.md | 3406 | - [ ] T8414-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T3410-bf070efa | docs/dev/roadmap/v0.2-overview.md | 3407 | - [ ] T8415-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T3411-21cff8a7 | docs/dev/roadmap/v0.2-overview.md | 3408 | - [ ] T8416-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T3412-dda85a99 | docs/dev/roadmap/v0.2-overview.md | 3409 | - [ ] T8417-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T3413-0dc7d9ea | docs/dev/roadmap/v0.2-overview.md | 3410 | - [ ] T8418-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T3414-6c136036 | docs/dev/roadmap/v0.2-overview.md | 3411 | - [ ] T8419-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T3415-6da303b9 | docs/dev/roadmap/v0.2-overview.md | 3412 | - [ ] T8420-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T3416-d8ea56d8 | docs/dev/roadmap/v0.2-overview.md | 3413 | - [ ] T8421-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T3417-af437bff | docs/dev/roadmap/v0.2-overview.md | 3414 | - [ ] T8422-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T3418-bb5e282e | docs/dev/roadmap/v0.2-overview.md | 3415 | - [ ] T8423-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T3419-ab06d9fd | docs/dev/roadmap/v0.2-overview.md | 3416 | - [ ] T8425-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T3420-80dd7998 | docs/dev/roadmap/v0.2-overview.md | 3417 | - [ ] T8426-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T3421-95baff5a | docs/dev/roadmap/v0.2-overview.md | 3418 | - [ ] T8427-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T3422-4ed0663e | docs/dev/roadmap/v0.2-overview.md | 3419 | - [ ] T8428-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T3423-3456feaf | docs/dev/roadmap/v0.2-overview.md | 3420 | - [ ] T8429-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T3424-4e44eb3a | docs/dev/roadmap/v0.2-overview.md | 3421 | - [ ] T8430-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T3425-35d542b0 | docs/dev/roadmap/v0.2-overview.md | 3422 | - [ ] T8431-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T3426-9fae0775 | docs/dev/roadmap/v0.2-overview.md | 3423 | - [ ] T8432-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T3427-53da2c26 | docs/dev/roadmap/v0.2-overview.md | 3424 | - [ ] T8433-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T3428-a94b5fb3 | docs/dev/roadmap/v0.2-overview.md | 3425 | - [ ] T8434-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T3429-64cdcc00 | docs/dev/roadmap/v0.2-overview.md | 3426 | - [ ] T8435-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T3430-ed650f72 | docs/dev/roadmap/v0.2-overview.md | 3427 | - [ ] T8436-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T3431-ea191e85 | docs/dev/roadmap/v0.2-overview.md | 3428 | - [ ] T8437-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T3432-517215b4 | docs/dev/roadmap/v0.2-overview.md | 3429 | - [ ] T8438-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T3433-38ec9e46 | docs/dev/roadmap/v0.2-overview.md | 3430 | - [ ] T8439-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T3434-c9fd2552 | docs/dev/roadmap/v0.2-overview.md | 3431 | - [ ] T8440-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T3435-df396cb0 | docs/dev/roadmap/v0.2-overview.md | 3432 | - [ ] T8441-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T3436-bd7ea555 | docs/dev/roadmap/v0.2-overview.md | 3433 | - [ ] T8442-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T3437-9aaa8d87 | docs/dev/roadmap/v0.2-overview.md | 3434 | - [ ] T8443-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T3438-39342736 | docs/dev/roadmap/v0.2-overview.md | 3435 | - [ ] T8444-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T3439-9fa6161a | docs/dev/roadmap/v0.2-overview.md | 3436 | - [ ] T8445-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T3440-3f2cf1dc | docs/dev/roadmap/v0.2-overview.md | 3437 | - [ ] T8446-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T3441-842f6d4e | docs/dev/roadmap/v0.2-overview.md | 3438 | - [ ] T8447-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T3442-2412ef4b | docs/dev/roadmap/v0.2-overview.md | 3439 | - [ ] T8448-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T3443-632553e6 | docs/dev/roadmap/v0.2-overview.md | 3440 | - [ ] T8449-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T3444-91f88b60 | docs/dev/roadmap/v0.2-overview.md | 3441 | - [ ] T8450-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T3445-365558c1 | docs/dev/roadmap/v0.2-overview.md | 3442 | - [ ] T8451-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T3446-ab082e8e | docs/dev/roadmap/v0.2-overview.md | 3443 | - [ ] T8452-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T3447-96732d10 | docs/dev/roadmap/v0.2-overview.md | 3444 | - [ ] T8453-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T3448-27b830f1 | docs/dev/roadmap/v0.2-overview.md | 3445 | - [ ] T8454-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T3449-4737446e | docs/dev/roadmap/v0.2-overview.md | 3446 | - [ ] T8455-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T3450-1cc62b47 | docs/dev/roadmap/v0.2-overview.md | 3447 | - [ ] T8456-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T3451-888c6c19 | docs/dev/roadmap/v0.2-overview.md | 3448 | - [ ] T8457-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T3452-60feb070 | docs/dev/roadmap/v0.2-overview.md | 3449 | - [ ] T8458-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T3453-0135517d | docs/dev/roadmap/v0.2-overview.md | 3450 | - [ ] T8459-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T3454-921719f7 | docs/dev/roadmap/v0.2-overview.md | 3451 | - [ ] T8460-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T3455-c229b0aa | docs/dev/roadmap/v0.2-overview.md | 3452 | - [ ] T8461-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T3456-c46b0bb6 | docs/dev/roadmap/v0.2-overview.md | 3453 | - [ ] T8462-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T3457-14bb1590 | docs/dev/roadmap/v0.2-overview.md | 3454 | - [ ] T8463-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T3458-e4e2670a | docs/dev/roadmap/v0.2-overview.md | 3455 | - [ ] T8464-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T3459-f4ef9a35 | docs/dev/roadmap/v0.2-overview.md | 3456 | - [ ] T8465-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T3460-e8e3e00b | docs/dev/roadmap/v0.2-overview.md | 3457 | - [ ] T8466-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T3461-6bc034c7 | docs/dev/roadmap/v0.2-overview.md | 3458 | - [ ] T8467-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T3462-1db69f20 | docs/dev/roadmap/v0.2-overview.md | 3459 | - [ ] T8468-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T3463-e48ee70e | docs/dev/roadmap/v0.2-overview.md | 3460 | - [ ] T8469-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T3464-34b1c601 | docs/dev/roadmap/v0.2-overview.md | 3461 | - [ ] T8470-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T3465-e3ccadfe | docs/dev/roadmap/v0.2-overview.md | 3462 | - [ ] T8471-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T3466-9cc00a49 | docs/dev/roadmap/v0.2-overview.md | 3463 | - [ ] T8472-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T3467-1c3303a6 | docs/dev/roadmap/v0.2-overview.md | 3464 | - [ ] T8473-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T3468-c84e6f01 | docs/dev/roadmap/v0.2-overview.md | 3465 | - [ ] T8474-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T3469-182ef47e | docs/dev/roadmap/v0.2-overview.md | 3466 | - [ ] T8475-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T3470-541a9bdb | docs/dev/roadmap/v0.2-overview.md | 3467 | - [ ] T8476-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T3471-b9962523 | docs/dev/roadmap/v0.2-overview.md | 3468 | - [ ] T8477-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T3472-2f81fdc5 | docs/dev/roadmap/v0.2-overview.md | 3469 | - [ ] T8478-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T3473-68aea03a | docs/dev/roadmap/v0.2-overview.md | 3470 | - [ ] T8479-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T3474-b1f27a6d | docs/dev/roadmap/v0.2-overview.md | 3471 | - [ ] T8480-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T3475-3995cc95 | docs/dev/roadmap/v0.2-overview.md | 3472 | - [ ] T8481-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T3476-c9de7fc8 | docs/dev/roadmap/v0.2-overview.md | 3473 | - [ ] T8483-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T3477-e9293827 | docs/dev/roadmap/v0.2-overview.md | 3474 | - [ ] T8484-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T3478-11bd218d | docs/dev/roadmap/v0.2-overview.md | 3475 | - [ ] T8485-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T3479-d24ba45b | docs/dev/roadmap/v0.2-overview.md | 3476 | - [ ] T8486-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T3480-653ca49f | docs/dev/roadmap/v0.2-overview.md | 3477 | - [ ] T8487-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T3481-faa76fa9 | docs/dev/roadmap/v0.2-overview.md | 3478 | - [ ] T8488-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T3482-a204cc3b | docs/dev/roadmap/v0.2-overview.md | 3479 | - [ ] T8489-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T3483-6e19fc90 | docs/dev/roadmap/v0.2-overview.md | 3480 | - [ ] T8490-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T3484-e7441c03 | docs/dev/roadmap/v0.2-overview.md | 3481 | - [ ] T8491-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T3485-27252c54 | docs/dev/roadmap/v0.2-overview.md | 3482 | - [ ] T8492-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T3486-44900473 | docs/dev/roadmap/v0.2-overview.md | 3483 | - [ ] T8493-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T3487-1f509006 | docs/dev/roadmap/v0.2-overview.md | 3484 | - [ ] T8494-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T3488-a374c0d7 | docs/dev/roadmap/v0.2-overview.md | 3485 | - [ ] T8495-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T3489-ec92d349 | docs/dev/roadmap/v0.2-overview.md | 3486 | - [ ] T8496-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T3490-70bdd3df | docs/dev/roadmap/v0.2-overview.md | 3487 | - [ ] T8497-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T3491-5be5bb68 | docs/dev/roadmap/v0.2-overview.md | 3488 | - [ ] T8498-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T3492-0accca9c | docs/dev/roadmap/v0.2-overview.md | 3489 | - [ ] T8499-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T3493-1ce1f263 | docs/dev/roadmap/v0.2-overview.md | 3490 | - [ ] T8500-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T3494-b04d1dc6 | docs/dev/roadmap/v0.2-overview.md | 3491 | - [ ] T8501-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T3495-c3fcf4ca | docs/dev/roadmap/v0.2-overview.md | 3492 | - [ ] T8502-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T3496-15cf07bc | docs/dev/roadmap/v0.2-overview.md | 3493 | - [ ] T8503-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T3497-53fbc458 | docs/dev/roadmap/v0.2-overview.md | 3494 | - [ ] T8504-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T3498-358007e7 | docs/dev/roadmap/v0.2-overview.md | 3495 | - [ ] T8505-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T3499-cc03a849 | docs/dev/roadmap/v0.2-overview.md | 3496 | - [ ] T8506-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T3500-1040e26f | docs/dev/roadmap/v0.2-overview.md | 3497 | - [ ] T8507-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T3501-6682be9d | docs/dev/roadmap/v0.2-overview.md | 3498 | - [ ] T8508-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T3502-62f00f63 | docs/dev/roadmap/v0.2-overview.md | 3499 | - [ ] T8509-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T3503-9c08767a | docs/dev/roadmap/v0.2-overview.md | 3500 | - [ ] T8510-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T3504-93550acb | docs/dev/roadmap/v0.2-overview.md | 3501 | - [ ] T8511-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T3505-63092b04 | docs/dev/roadmap/v0.2-overview.md | 3502 | - [ ] T8512-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T3506-821139d5 | docs/dev/roadmap/v0.2-overview.md | 3503 | - [ ] T8513-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T3507-33caf148 | docs/dev/roadmap/v0.2-overview.md | 3504 | - [ ] T8514-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T3508-f3139a75 | docs/dev/roadmap/v0.2-overview.md | 3505 | - [ ] T8515-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T3509-80167a40 | docs/dev/roadmap/v0.2-overview.md | 3506 | - [ ] T8516-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T3510-e6d2f976 | docs/dev/roadmap/v0.2-overview.md | 3507 | - [ ] T8517-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T3511-ef952662 | docs/dev/roadmap/v0.2-overview.md | 3508 | - [ ] T8518-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T3512-708abcc5 | docs/dev/roadmap/v0.2-overview.md | 3509 | - [ ] T8519-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T3513-676ae886 | docs/dev/roadmap/v0.2-overview.md | 3510 | - [ ] T8520-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T3514-3edcd8b8 | docs/dev/roadmap/v0.2-overview.md | 3511 | - [ ] T8521-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T3515-94b4cd13 | docs/dev/roadmap/v0.2-overview.md | 3512 | - [ ] T8522-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T3516-a313fa97 | docs/dev/roadmap/v0.2-overview.md | 3513 | - [ ] T8523-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T3517-907cf7d2 | docs/dev/roadmap/v0.2-overview.md | 3514 | - [ ] T8524-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T3518-b4ab7a49 | docs/dev/roadmap/v0.2-overview.md | 3515 | - [ ] T8525-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T3519-15812411 | docs/dev/roadmap/v0.2-overview.md | 3516 | - [ ] T8526-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T3520-d2d17a93 | docs/dev/roadmap/v0.2-overview.md | 3517 | - [ ] T8527-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T3521-aa68f9c5 | docs/dev/roadmap/v0.2-overview.md | 3518 | - [ ] T8528-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T3522-b9bf5f26 | docs/dev/roadmap/v0.2-overview.md | 3519 | - [ ] T8529-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T3523-516d110f | docs/dev/roadmap/v0.2-overview.md | 3520 | - [ ] T8530-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T3524-d1cace1f | docs/dev/roadmap/v0.2-overview.md | 3521 | - [ ] T8531-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T3525-9b8e3a79 | docs/dev/roadmap/v0.2-overview.md | 3522 | - [ ] T8532-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T3526-10cd0bd4 | docs/dev/roadmap/v0.2-overview.md | 3523 | - [ ] T8533-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T3527-97d26ea3 | docs/dev/roadmap/v0.2-overview.md | 3524 | - [ ] T8534-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T3528-3261f150 | docs/dev/roadmap/v0.2-overview.md | 3525 | - [ ] T8535-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T3529-50f807ab | docs/dev/roadmap/v0.2-overview.md | 3526 | - [ ] T8536-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T3530-4195ffac | docs/dev/roadmap/v0.2-overview.md | 3527 | - [ ] T8537-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T3531-847da09e | docs/dev/roadmap/v0.2-overview.md | 3528 | - [ ] T8538-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T3532-a7f1b2c2 | docs/dev/roadmap/v0.2-overview.md | 3529 | - [ ] T8539-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T3533-9db61f24 | docs/dev/roadmap/v0.2-overview.md | 3530 | - [ ] T8540-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T3534-dfd8057e | docs/dev/roadmap/v0.2-overview.md | 3531 | - [ ] T8541-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T3535-bd35d786 | docs/dev/roadmap/v0.2-overview.md | 3532 | - [ ] T8542-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T3536-85f34a32 | docs/dev/roadmap/v0.2-overview.md | 3533 | - [ ] T8543-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T3537-80672fea | docs/dev/roadmap/v0.2-overview.md | 3534 | - [ ] T8544-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T3538-f6f1db1a | docs/dev/roadmap/v0.2-overview.md | 3535 | - [ ] T8545-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T3539-4c849c15 | docs/dev/roadmap/v0.2-overview.md | 3536 | - [ ] T8546-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T3540-c785920b | docs/dev/roadmap/v0.2-overview.md | 3537 | - [ ] T8547-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T3541-feee4e02 | docs/dev/roadmap/v0.2-overview.md | 3538 | - [ ] T8548-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T3542-0b385d92 | docs/dev/roadmap/v0.2-overview.md | 3539 | - [ ] T8549-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T3543-dd3864da | docs/dev/roadmap/v0.2-overview.md | 3540 | - [ ] T8550-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T3544-c699f54e | docs/dev/roadmap/v0.2-overview.md | 3541 | - [ ] T8551-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T3545-98f90d49 | docs/dev/roadmap/v0.2-overview.md | 3542 | - [ ] T8552-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T3546-6298eb55 | docs/dev/roadmap/v0.2-overview.md | 3543 | - [ ] T8553-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T3547-b73b382c | docs/dev/roadmap/v0.2-overview.md | 3544 | - [ ] T8554-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T3548-bb4373e7 | docs/dev/roadmap/v0.2-overview.md | 3545 | - [ ] T8555-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T3549-759174d9 | docs/dev/roadmap/v0.2-overview.md | 3546 | - [ ] T8556-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T3550-60677cec | docs/dev/roadmap/v0.2-overview.md | 3547 | - [ ] T8557-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T3551-7c238bfa | docs/dev/roadmap/v0.2-overview.md | 3548 | - [ ] T8558-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T3552-9b5e6f9d | docs/dev/roadmap/v0.2-overview.md | 3549 | - [ ] T8559-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T3553-a332e80e | docs/dev/roadmap/v0.2-overview.md | 3550 | - [ ] T8560-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T3554-499246e0 | docs/dev/roadmap/v0.2-overview.md | 3551 | - [ ] T8561-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T3555-3d98d492 | docs/dev/roadmap/v0.2-overview.md | 3552 | - [ ] T8562-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T3556-1dcf6170 | docs/dev/roadmap/v0.2-overview.md | 3553 | - [ ] T8563-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T3557-979fba2e | docs/dev/roadmap/v0.2-overview.md | 3554 | - [ ] T8564-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T3558-75abc88d | docs/dev/roadmap/v0.2-overview.md | 3555 | - [ ] T8565-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T3559-5a7df166 | docs/dev/roadmap/v0.2-overview.md | 3556 | - [ ] T8566-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T3560-52eabd0e | docs/dev/roadmap/v0.2-overview.md | 3557 | - [ ] T8567-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T3561-47c41194 | docs/dev/roadmap/v0.2-overview.md | 3558 | - [ ] T8568-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T3562-ac162c15 | docs/dev/roadmap/v0.2-overview.md | 3559 | - [ ] T8569-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T3563-bb5e5a0f | docs/dev/roadmap/v0.2-overview.md | 3560 | - [ ] T8570-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T3564-744b3fee | docs/dev/roadmap/v0.2-overview.md | 3561 | - [ ] T8571-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T3565-b5ffa5fd | docs/dev/roadmap/v0.2-overview.md | 3562 | - [ ] T8572-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T3566-5fb93974 | docs/dev/roadmap/v0.2-overview.md | 3563 | - [ ] T8573-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T3567-00f6a126 | docs/dev/roadmap/v0.2-overview.md | 3564 | - [ ] T8574-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T3568-fd06f0a3 | docs/dev/roadmap/v0.2-overview.md | 3565 | - [ ] T8575-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T3569-51eef6a4 | docs/dev/roadmap/v0.2-overview.md | 3566 | - [ ] T8576-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T3570-fc5a2715 | docs/dev/roadmap/v0.2-overview.md | 3567 | - [ ] T8577-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T3571-50b4f23d | docs/dev/roadmap/v0.2-overview.md | 3568 | - [ ] T8578-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T3572-75e6d33e | docs/dev/roadmap/v0.2-overview.md | 3569 | - [ ] T8579-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T3573-847aeef1 | docs/dev/roadmap/v0.2-overview.md | 3570 | - [ ] T8580-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T3574-d22f255b | docs/dev/roadmap/v0.2-overview.md | 3571 | - [ ] T8581-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T3575-ed0c99e3 | docs/dev/roadmap/v0.2-overview.md | 3572 | - [ ] T8582-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T3576-effb4138 | docs/dev/roadmap/v0.2-overview.md | 3573 | - [ ] T8583-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T3577-5301c7c3 | docs/dev/roadmap/v0.2-overview.md | 3574 | - [ ] T8584-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T3578-96a4b993 | docs/dev/roadmap/v0.2-overview.md | 3575 | - [ ] T8585-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T3579-b3e6ec3c | docs/dev/roadmap/v0.2-overview.md | 3576 | - [ ] T8586-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T3580-c4db4c15 | docs/dev/roadmap/v0.2-overview.md | 3577 | - [ ] T8587-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T3581-1e45143c | docs/dev/roadmap/v0.2-overview.md | 3578 | - [ ] T8588-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T3582-54829cf8 | docs/dev/roadmap/v0.2-overview.md | 3579 | - [ ] T8589-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T3583-629fad63 | docs/dev/roadmap/v0.2-overview.md | 3580 | - [ ] T8590-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T3584-75562549 | docs/dev/roadmap/v0.2-overview.md | 3581 | - [ ] T8591-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T3585-94e60dc8 | docs/dev/roadmap/v0.2-overview.md | 3582 | - [ ] T8592-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T3586-ba763c1a | docs/dev/roadmap/v0.2-overview.md | 3583 | - [ ] T8593-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T3587-9bd96978 | docs/dev/roadmap/v0.2-overview.md | 3584 | - [ ] T8594-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T3588-4bed47b3 | docs/dev/roadmap/v0.2-overview.md | 3585 | - [ ] T8595-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T3589-55b42715 | docs/dev/roadmap/v0.2-overview.md | 3586 | - [ ] T8596-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T3590-288d394c | docs/dev/roadmap/v0.2-overview.md | 3587 | - [ ] T8597-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T3591-ed4728db | docs/dev/roadmap/v0.2-overview.md | 3588 | - [ ] T8598-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T3592-e9554d35 | docs/dev/roadmap/v0.2-overview.md | 3589 | - [ ] T8599-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T3593-d3eddc3f | docs/dev/roadmap/v0.2-overview.md | 3590 | - [ ] T8600-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T3594-6197a9d7 | docs/dev/roadmap/v0.2-overview.md | 3591 | - [ ] T8601-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T3595-6ae857ba | docs/dev/roadmap/v0.2-overview.md | 3592 | - [ ] T8602-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T3596-c9c37640 | docs/dev/roadmap/v0.2-overview.md | 3593 | - [ ] T8603-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T3597-541879ae | docs/dev/roadmap/v0.2-overview.md | 3594 | - [ ] T8604-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T3598-6cf2d4c0 | docs/dev/roadmap/v0.2-overview.md | 3595 | - [ ] T8605-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T3599-ff060d49 | docs/dev/roadmap/v0.2-overview.md | 3596 | - [ ] T8606-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T3600-e2d6ca4d | docs/dev/roadmap/v0.2-overview.md | 3597 | - [ ] T8607-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T3601-49c5768c | docs/dev/roadmap/v0.2-overview.md | 3598 | - [ ] T8608-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T3602-b5438ad8 | docs/dev/roadmap/v0.2-overview.md | 3599 | - [ ] T8609-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T3603-f56f9db5 | docs/dev/roadmap/v0.2-overview.md | 3600 | - [ ] T8610-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T3604-ce7e661d | docs/dev/roadmap/v0.2-overview.md | 3601 | - [ ] T3604-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T3605-5405e65c | docs/dev/roadmap/v0.2-overview.md | 3602 | - [ ] T3605-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T3606-574fefc7 | docs/dev/roadmap/v0.2-overview.md | 3603 | - [ ] T3606-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T3607-6d22cd25 | docs/dev/roadmap/v0.2-overview.md | 3604 | - [ ] T3607-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T3608-9c97106e | docs/dev/roadmap/v0.2-overview.md | 3605 | - [ ] T3608-4c66e9b1 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:155) |
| T3609-2ca44749 | docs/dev/roadmap/v0.2-overview.md | 3606 | - [ ] T3609-813e30e1 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:162) |
| T3610-6a51b945 | docs/dev/roadmap/v0.2-overview.md | 3607 | - [ ] T3610-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T3611-5cd0708c | docs/dev/roadmap/v0.2-overview.md | 3608 | - [ ] T3611-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T3612-2af4ef81 | docs/dev/roadmap/v0.2-overview.md | 3609 | - [ ] T3612-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T3613-b1fdbdb0 | docs/dev/roadmap/v0.2-overview.md | 3610 | - [ ] T3613-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T3614-d85a1f63 | docs/dev/roadmap/v0.2-overview.md | 3611 | - [ ] T3614-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T3615-905c84b2 | docs/dev/roadmap/v0.2-overview.md | 3612 | - [ ] T3615-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T3616-13e12de0 | docs/dev/roadmap/v0.2-overview.md | 3613 | - [ ] T3616-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T3617-b1ff3c8c | docs/dev/roadmap/v0.2-overview.md | 3614 | - [ ] T3617-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T3618-d232b1cc | docs/dev/roadmap/v0.2-overview.md | 3615 | - [ ] T3618-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T3619-85c27860 | docs/dev/roadmap/v0.2-overview.md | 3616 | - [ ] T3619-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T3620-88231de4 | docs/dev/roadmap/v0.2-overview.md | 3617 | - [ ] T3620-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T3621-091089d6 | docs/dev/roadmap/v0.2-overview.md | 3618 | - [ ] T3621-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T3622-7ff433bb | docs/dev/roadmap/v0.2-overview.md | 3619 | - [ ] T3622-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T3623-6909e447 | docs/dev/roadmap/v0.2-overview.md | 3620 | - [ ] T3623-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T3624-521fd725 | docs/dev/roadmap/v0.2-overview.md | 3621 | - [ ] T3624-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T3625-3fb04501 | docs/dev/roadmap/v0.2-overview.md | 3622 | - [ ] T3625-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T3626-54610215 | docs/dev/roadmap/v0.2-overview.md | 3623 | - [ ] T3626-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T3627-806a1e4f | docs/dev/roadmap/v0.2-overview.md | 3624 | - [ ] T3627-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T3628-e7c0ce00 | docs/dev/roadmap/v0.2-overview.md | 3625 | - [ ] T3628-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T3629-0375836a | docs/dev/roadmap/v0.2-overview.md | 3626 | - [ ] T3629-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T3630-419a9780 | docs/dev/roadmap/v0.2-overview.md | 3627 | - [ ] T3630-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T3631-ffed66f8 | docs/dev/roadmap/v0.2-overview.md | 3628 | - [ ] T3631-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T3632-efb5f57e | docs/dev/roadmap/v0.2-overview.md | 3629 | - [ ] T3632-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T3633-efb7e131 | docs/dev/roadmap/v0.2-overview.md | 3630 | - [ ] T3633-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T3634-407a338a | docs/dev/roadmap/v0.2-overview.md | 3631 | - [ ] T3634-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T3635-6177396a | docs/dev/roadmap/v0.2-overview.md | 3632 | - [ ] T3635-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T3636-3f048200 | docs/dev/roadmap/v0.2-overview.md | 3633 | - [ ] T3636-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T3637-cd1af290 | docs/dev/roadmap/v0.2-overview.md | 3634 | - [ ] T3637-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T3638-559114e4 | docs/dev/roadmap/v0.2-overview.md | 3635 | - [ ] T3638-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T3639-a6fe2402 | docs/dev/roadmap/v0.2-overview.md | 3636 | - [ ] T3639-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T3640-74a2939b | docs/dev/roadmap/v0.2-overview.md | 3637 | - [ ] T3640-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T3641-b30c31fb | docs/dev/roadmap/v0.2-overview.md | 3638 | - [ ] T3641-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T3642-b7963159 | docs/dev/roadmap/v0.2-overview.md | 3639 | - [ ] T3642-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T3643-f24737c6 | docs/dev/roadmap/v0.2-overview.md | 3640 | - [ ] T3643-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T3644-2c06ef26 | docs/dev/roadmap/v0.2-overview.md | 3641 | - [ ] T3644-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T3645-4952f303 | docs/dev/roadmap/v0.2-overview.md | 3642 | - [ ] T3645-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T3646-fea2f6b3 | docs/dev/roadmap/v0.2-overview.md | 3643 | - [ ] T3646-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T3647-5363570f | docs/dev/roadmap/v0.2-overview.md | 3644 | - [ ] T3647-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T3648-199d6baf | docs/dev/roadmap/v0.2-overview.md | 3645 | - [ ] T3648-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T3649-a6b144bd | docs/dev/roadmap/v0.2-overview.md | 3646 | - [ ] T3649-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T3650-f483e61b | docs/dev/roadmap/v0.2-overview.md | 3647 | - [ ] T3650-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T3651-376bf8e1 | docs/dev/roadmap/v0.2-overview.md | 3648 | - [ ] T3651-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T3652-ba29f4e2 | docs/dev/roadmap/v0.2-overview.md | 3649 | - [ ] T3652-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T3653-38d05e9e | docs/dev/roadmap/v0.2-overview.md | 3650 | - [ ] T3653-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T3654-06abf2a2 | docs/dev/roadmap/v0.2-overview.md | 3651 | - [ ] T3654-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T3655-8ae6c0eb | docs/dev/roadmap/v0.2-overview.md | 3652 | - [ ] T3655-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T3656-4b39bd53 | docs/dev/roadmap/v0.2-overview.md | 3653 | - [ ] T3656-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T3657-7ae4cb6b | docs/dev/roadmap/v0.2-overview.md | 3654 | - [ ] T3657-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T3658-8a000a78 | docs/dev/roadmap/v0.2-overview.md | 3655 | - [ ] T3658-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T3659-1dfec36c | docs/dev/roadmap/v0.2-overview.md | 3656 | - [ ] T3660-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T3660-f2276dcf | docs/dev/roadmap/v0.2-overview.md | 3657 | - [ ] T3661-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T3661-6da34bce | docs/dev/roadmap/v0.2-overview.md | 3658 | - [ ] T3662-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T3662-c3903c35 | docs/dev/roadmap/v0.2-overview.md | 3659 | - [ ] T3663-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T3663-1c9ba123 | docs/dev/roadmap/v0.2-overview.md | 3660 | - [ ] T3664-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T3664-a51f5bd6 | docs/dev/roadmap/v0.2-overview.md | 3661 | - [ ] T3665-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T3665-1122ca78 | docs/dev/roadmap/v0.2-overview.md | 3662 | - [ ] T3666-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T3666-a91d8155 | docs/dev/roadmap/v0.2-overview.md | 3663 | - [ ] T3667-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T3667-8320a3fd | docs/dev/roadmap/v0.2-overview.md | 3664 | - [ ] T3668-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T3668-052abad3 | docs/dev/roadmap/v0.2-overview.md | 3665 | - [ ] T3669-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T3669-03012eab | docs/dev/roadmap/v0.2-overview.md | 3666 | - [ ] T3670-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T3670-c01bd299 | docs/dev/roadmap/v0.2-overview.md | 3667 | - [ ] T3671-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T3671-73609f38 | docs/dev/roadmap/v0.2-overview.md | 3668 | - [ ] T3672-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T3672-c4ffa4bf | docs/dev/roadmap/v0.2-overview.md | 3669 | - [ ] T3673-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T3673-391f1694 | docs/dev/roadmap/v0.2-overview.md | 3670 | - [ ] T3674-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T3674-ab52fae8 | docs/dev/roadmap/v0.2-overview.md | 3671 | - [ ] T3675-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T3675-edf0520c | docs/dev/roadmap/v0.2-overview.md | 3672 | - [ ] T3676-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T3676-efb8d5af | docs/dev/roadmap/v0.2-overview.md | 3673 | - [ ] T3677-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T3677-7e31d3c6 | docs/dev/roadmap/v0.2-overview.md | 3674 | - [ ] T3678-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T3678-2a046697 | docs/dev/roadmap/v0.2-overview.md | 3675 | - [ ] T3679-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T3679-ae54f9ae | docs/dev/roadmap/v0.2-overview.md | 3676 | - [ ] T3680-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T3680-823e982a | docs/dev/roadmap/v0.2-overview.md | 3677 | - [ ] T3681-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T3681-0e5a093b | docs/dev/roadmap/v0.2-overview.md | 3678 | - [ ] T3682-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T3682-6859cf38 | docs/dev/roadmap/v0.2-overview.md | 3679 | - [ ] T3683-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T3683-3896fbe7 | docs/dev/roadmap/v0.2-overview.md | 3680 | - [ ] T3684-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T3684-fec8da2d | docs/dev/roadmap/v0.2-overview.md | 3681 | - [ ] T3685-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T3685-94ea7085 | docs/dev/roadmap/v0.2-overview.md | 3682 | - [ ] T3686-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T3686-7b915942 | docs/dev/roadmap/v0.2-overview.md | 3683 | - [ ] T3687-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T3687-fbdd536d | docs/dev/roadmap/v0.2-overview.md | 3684 | - [ ] T3688-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T3688-db5f69f3 | docs/dev/roadmap/v0.2-overview.md | 3685 | - [ ] T3689-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T3689-f6d105ed | docs/dev/roadmap/v0.2-overview.md | 3686 | - [ ] T3690-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T3690-d4e6ac73 | docs/dev/roadmap/v0.2-overview.md | 3687 | - [ ] T3691-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T3691-bdd71f1e | docs/dev/roadmap/v0.2-overview.md | 3688 | - [ ] T3692-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T3692-e17ab8fa | docs/dev/roadmap/v0.2-overview.md | 3689 | - [ ] T3693-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T3693-3795bc85 | docs/dev/roadmap/v0.2-overview.md | 3690 | - [ ] T3694-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T3694-4e23ae72 | docs/dev/roadmap/v0.2-overview.md | 3691 | - [ ] T3695-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T3695-4965d480 | docs/dev/roadmap/v0.2-overview.md | 3692 | - [ ] T3696-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T3696-fac72dd5 | docs/dev/roadmap/v0.2-overview.md | 3693 | - [ ] T3697-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T3697-005a75ad | docs/dev/roadmap/v0.2-overview.md | 3694 | - [ ] T3698-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T3698-c6dfdfe1 | docs/dev/roadmap/v0.2-overview.md | 3695 | - [ ] T3699-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T3699-fe7d0d44 | docs/dev/roadmap/v0.2-overview.md | 3696 | - [ ] T3700-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T3700-b7b390c2 | docs/dev/roadmap/v0.2-overview.md | 3697 | - [ ] T3701-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T3701-adee4885 | docs/dev/roadmap/v0.2-overview.md | 3698 | - [ ] T3702-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T3702-7f23b43b | docs/dev/roadmap/v0.2-overview.md | 3699 | - [ ] T3703-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T3703-ec1d1d17 | docs/dev/roadmap/v0.2-overview.md | 3700 | - [ ] T3704-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T3704-6549df6d | docs/dev/roadmap/v0.2-overview.md | 3701 | - [ ] T3705-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T3705-1f66bf3b | docs/dev/roadmap/v0.2-overview.md | 3702 | - [ ] T3706-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T3706-144571fb | docs/dev/roadmap/v0.2-overview.md | 3703 | - [ ] T3707-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T3707-d3a8acd0 | docs/dev/roadmap/v0.2-overview.md | 3704 | - [ ] T3708-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T3708-62ae5840 | docs/dev/roadmap/v0.2-overview.md | 3705 | - [ ] T3709-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T3709-41484ea7 | docs/dev/roadmap/v0.2-overview.md | 3706 | - [ ] T3710-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T3710-f514a771 | docs/dev/roadmap/v0.2-overview.md | 3707 | - [ ] T3711-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T3711-40636548 | docs/dev/roadmap/v0.2-overview.md | 3708 | - [ ] T3712-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T3712-c97482a0 | docs/dev/roadmap/v0.2-overview.md | 3709 | - [ ] T3713-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T3713-21fe49f4 | docs/dev/roadmap/v0.2-overview.md | 3710 | - [ ] T3714-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T3714-53917c7c | docs/dev/roadmap/v0.2-overview.md | 3711 | - [ ] T3715-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T3715-b3d72ed1 | docs/dev/roadmap/v0.2-overview.md | 3712 | - [ ] T3716-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T3716-aa5dec51 | docs/dev/roadmap/v0.2-overview.md | 3713 | - [ ] T3717-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T3717-6c0effcf | docs/dev/roadmap/v0.2-overview.md | 3714 | - [ ] T3718-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T3718-7bda5a02 | docs/dev/roadmap/v0.2-overview.md | 3715 | - [ ] T3719-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T3719-6a288f8c | docs/dev/roadmap/v0.2-overview.md | 3716 | - [ ] T3720-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T3720-b8acf2e8 | docs/dev/roadmap/v0.2-overview.md | 3717 | - [ ] T3721-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T3721-04260b75 | docs/dev/roadmap/v0.2-overview.md | 3718 | - [ ] T3722-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T3722-916a70ac | docs/dev/roadmap/v0.2-overview.md | 3719 | - [ ] T3723-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T3723-b3ec0b97 | docs/dev/roadmap/v0.2-overview.md | 3720 | - [ ] T3724-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T3724-071472d7 | docs/dev/roadmap/v0.2-overview.md | 3721 | - [ ] T3725-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T3725-11b7155f | docs/dev/roadmap/v0.2-overview.md | 3722 | - [ ] T3726-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T3726-b0151caa | docs/dev/roadmap/v0.2-overview.md | 3723 | - [ ] T3727-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T3727-962e187e | docs/dev/roadmap/v0.2-overview.md | 3724 | - [ ] T3728-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T3728-feb90a3a | docs/dev/roadmap/v0.2-overview.md | 3725 | - [ ] T3729-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T3729-06f446f4 | docs/dev/roadmap/v0.2-overview.md | 3726 | - [ ] T3730-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T3730-e60fdb05 | docs/dev/roadmap/v0.2-overview.md | 3727 | - [ ] T3731-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T3731-00c53cd9 | docs/dev/roadmap/v0.2-overview.md | 3728 | - [ ] T3732-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T3732-3ad3e278 | docs/dev/roadmap/v0.2-overview.md | 3729 | - [ ] T3733-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T3733-a5d80fe1 | docs/dev/roadmap/v0.2-overview.md | 3730 | - [ ] T3734-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T3734-b15129de | docs/dev/roadmap/v0.2-overview.md | 3731 | - [ ] T3735-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T3735-bc9b397f | docs/dev/roadmap/v0.2-overview.md | 3732 | - [ ] T3736-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T3736-390f804b | docs/dev/roadmap/v0.2-overview.md | 3733 | - [ ] T3737-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T3737-a378d06f | docs/dev/roadmap/v0.2-overview.md | 3734 | - [ ] T3739-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T3738-e429130a | docs/dev/roadmap/v0.2-overview.md | 3735 | - [ ] T3740-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T3739-65e9b77b | docs/dev/roadmap/v0.2-overview.md | 3736 | - [ ] T3741-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T3740-d73b7470 | docs/dev/roadmap/v0.2-overview.md | 3737 | - [ ] T3742-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T3741-79952c08 | docs/dev/roadmap/v0.2-overview.md | 3738 | - [ ] T3743-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T3742-b7eb13c3 | docs/dev/roadmap/v0.2-overview.md | 3739 | - [ ] T3744-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T3743-1abd799b | docs/dev/roadmap/v0.2-overview.md | 3740 | - [ ] T3745-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T3744-6891046d | docs/dev/roadmap/v0.2-overview.md | 3741 | - [ ] T3746-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T3745-79b9b762 | docs/dev/roadmap/v0.2-overview.md | 3742 | - [ ] T3747-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T3746-ef153934 | docs/dev/roadmap/v0.2-overview.md | 3743 | - [ ] T3748-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T3747-e879268f | docs/dev/roadmap/v0.2-overview.md | 3744 | - [ ] T3749-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T3748-88fed867 | docs/dev/roadmap/v0.2-overview.md | 3745 | - [ ] T3750-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T3749-a0d9fd02 | docs/dev/roadmap/v0.2-overview.md | 3746 | - [ ] T3751-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T3750-b3247558 | docs/dev/roadmap/v0.2-overview.md | 3747 | - [ ] T3752-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T3751-5c501c1f | docs/dev/roadmap/v0.2-overview.md | 3748 | - [ ] T3753-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T3752-e5f9221a | docs/dev/roadmap/v0.2-overview.md | 3749 | - [ ] T3754-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T3753-fddb8d56 | docs/dev/roadmap/v0.2-overview.md | 3750 | - [ ] T3755-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T3754-c9d3c77f | docs/dev/roadmap/v0.2-overview.md | 3751 | - [ ] T3756-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T3755-943dd9f0 | docs/dev/roadmap/v0.2-overview.md | 3752 | - [ ] T3757-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T3756-83c3be6e | docs/dev/roadmap/v0.2-overview.md | 3753 | - [ ] T3758-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T3757-c5debac1 | docs/dev/roadmap/v0.2-overview.md | 3754 | - [ ] T3759-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T3758-6753ea0c | docs/dev/roadmap/v0.2-overview.md | 3755 | - [ ] T3760-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T3759-33f52e19 | docs/dev/roadmap/v0.2-overview.md | 3756 | - [ ] T3761-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T3760-866851b2 | docs/dev/roadmap/v0.2-overview.md | 3757 | - [ ] T3762-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T3761-58f5c89a | docs/dev/roadmap/v0.2-overview.md | 3758 | - [ ] T3763-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T3762-fb4ffe1c | docs/dev/roadmap/v0.2-overview.md | 3759 | - [ ] T3764-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T3763-3322cbf0 | docs/dev/roadmap/v0.2-overview.md | 3760 | - [ ] T3765-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T3764-625b2484 | docs/dev/roadmap/v0.2-overview.md | 3761 | - [ ] T3766-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T3765-b728e0a2 | docs/dev/roadmap/v0.2-overview.md | 3762 | - [ ] T3767-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T3766-e24ce044 | docs/dev/roadmap/v0.2-overview.md | 3763 | - [ ] T3768-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T3767-b91a5bcd | docs/dev/roadmap/v0.2-overview.md | 3764 | - [ ] T3769-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T3768-beaf9dcf | docs/dev/roadmap/v0.2-overview.md | 3765 | - [ ] T3770-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T3769-b1335ac2 | docs/dev/roadmap/v0.2-overview.md | 3766 | - [ ] T3771-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T3770-a006906b | docs/dev/roadmap/v0.2-overview.md | 3767 | - [ ] T3772-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T3771-fa4f70c8 | docs/dev/roadmap/v0.2-overview.md | 3768 | - [ ] T3773-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T3772-9bc40f20 | docs/dev/roadmap/v0.2-overview.md | 3769 | - [ ] T3774-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T3773-eaf271a3 | docs/dev/roadmap/v0.2-overview.md | 3770 | - [ ] T3775-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T3774-bf50c538 | docs/dev/roadmap/v0.2-overview.md | 3771 | - [ ] T3776-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T3775-3f7e5d2e | docs/dev/roadmap/v0.2-overview.md | 3772 | - [ ] T3777-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T3776-5531dc97 | docs/dev/roadmap/v0.2-overview.md | 3773 | - [ ] T3778-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T3777-fb47124f | docs/dev/roadmap/v0.2-overview.md | 3774 | - [ ] T3779-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T3778-f524fd49 | docs/dev/roadmap/v0.2-overview.md | 3775 | - [ ] T3780-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T3779-93f5b382 | docs/dev/roadmap/v0.2-overview.md | 3776 | - [ ] T3781-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T3780-82cba8f6 | docs/dev/roadmap/v0.2-overview.md | 3777 | - [ ] T3782-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T3781-4879f626 | docs/dev/roadmap/v0.2-overview.md | 3778 | - [ ] T3783-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T3782-9790f78f | docs/dev/roadmap/v0.2-overview.md | 3779 | - [ ] T3784-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T3783-c6cba963 | docs/dev/roadmap/v0.2-overview.md | 3780 | - [ ] T3785-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T3784-b67699b3 | docs/dev/roadmap/v0.2-overview.md | 3781 | - [ ] T3786-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T3785-484d6c82 | docs/dev/roadmap/v0.2-overview.md | 3782 | - [ ] T3787-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T3786-00b72fd2 | docs/dev/roadmap/v0.2-overview.md | 3783 | - [ ] T3788-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T3787-910cab82 | docs/dev/roadmap/v0.2-overview.md | 3784 | - [ ] T3789-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T3788-96ff5075 | docs/dev/roadmap/v0.2-overview.md | 3785 | - [ ] T3790-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T3789-af293196 | docs/dev/roadmap/v0.2-overview.md | 3786 | - [ ] T3791-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T3790-e70b9532 | docs/dev/roadmap/v0.2-overview.md | 3787 | - [ ] T3792-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T3791-8ee85997 | docs/dev/roadmap/v0.2-overview.md | 3788 | - [ ] T3793-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T3792-c8ac33d9 | docs/dev/roadmap/v0.2-overview.md | 3789 | - [ ] T3794-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T3793-21898bb3 | docs/dev/roadmap/v0.2-overview.md | 3790 | - [ ] T3795-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T3794-e42eab91 | docs/dev/roadmap/v0.2-overview.md | 3791 | - [ ] T3797-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T3795-cced891f | docs/dev/roadmap/v0.2-overview.md | 3792 | - [ ] T3798-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T3796-c1b58ea1 | docs/dev/roadmap/v0.2-overview.md | 3793 | - [ ] T3799-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T3797-84c532c2 | docs/dev/roadmap/v0.2-overview.md | 3794 | - [ ] T3800-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T3798-75e12056 | docs/dev/roadmap/v0.2-overview.md | 3795 | - [ ] T3801-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T3799-cd17c0f5 | docs/dev/roadmap/v0.2-overview.md | 3796 | - [ ] T3802-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T3800-336e2683 | docs/dev/roadmap/v0.2-overview.md | 3797 | - [ ] T3803-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T3801-d5e5cd25 | docs/dev/roadmap/v0.2-overview.md | 3798 | - [ ] T3804-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T3802-0d5af9eb | docs/dev/roadmap/v0.2-overview.md | 3799 | - [ ] T3805-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T3803-ba802841 | docs/dev/roadmap/v0.2-overview.md | 3800 | - [ ] T3806-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T3804-d0c92ed9 | docs/dev/roadmap/v0.2-overview.md | 3801 | - [ ] T3807-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T3805-4e065790 | docs/dev/roadmap/v0.2-overview.md | 3802 | - [ ] T3808-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T3806-797a13ab | docs/dev/roadmap/v0.2-overview.md | 3803 | - [ ] T3809-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T3807-9d119f36 | docs/dev/roadmap/v0.2-overview.md | 3804 | - [ ] T3810-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T3808-6b2243ab | docs/dev/roadmap/v0.2-overview.md | 3805 | - [ ] T3811-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T3809-f0481c1d | docs/dev/roadmap/v0.2-overview.md | 3806 | - [ ] T3812-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T3810-ed7f8138 | docs/dev/roadmap/v0.2-overview.md | 3807 | - [ ] T3813-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T3811-1784429e | docs/dev/roadmap/v0.2-overview.md | 3808 | - [ ] T3814-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T3812-44b7e417 | docs/dev/roadmap/v0.2-overview.md | 3809 | - [ ] T3815-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T3813-bb481270 | docs/dev/roadmap/v0.2-overview.md | 3810 | - [ ] T3816-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T3814-b22cae7a | docs/dev/roadmap/v0.2-overview.md | 3811 | - [ ] T3817-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T3815-febfb239 | docs/dev/roadmap/v0.2-overview.md | 3812 | - [ ] T3818-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T3816-9cfd8cfa | docs/dev/roadmap/v0.2-overview.md | 3813 | - [ ] T3819-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T3817-cd1ec478 | docs/dev/roadmap/v0.2-overview.md | 3814 | - [ ] T3820-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T3818-f7f6bdb5 | docs/dev/roadmap/v0.2-overview.md | 3815 | - [ ] T3821-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T3819-13510c43 | docs/dev/roadmap/v0.2-overview.md | 3816 | - [ ] T3822-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T3820-ee15bb84 | docs/dev/roadmap/v0.2-overview.md | 3817 | - [ ] T3823-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T3821-e0ddcc17 | docs/dev/roadmap/v0.2-overview.md | 3818 | - [ ] T3824-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T3822-e6e40d30 | docs/dev/roadmap/v0.2-overview.md | 3819 | - [ ] T3825-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T3823-1dcee9ce | docs/dev/roadmap/v0.2-overview.md | 3820 | - [ ] T3826-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T3824-69feec37 | docs/dev/roadmap/v0.2-overview.md | 3821 | - [ ] T3827-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T3825-c69ea1d3 | docs/dev/roadmap/v0.2-overview.md | 3822 | - [ ] T3828-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T3826-d47bdb6a | docs/dev/roadmap/v0.2-overview.md | 3823 | - [ ] T3829-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T3827-c6b753f9 | docs/dev/roadmap/v0.2-overview.md | 3824 | - [ ] T3830-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T3828-c23a0536 | docs/dev/roadmap/v0.2-overview.md | 3825 | - [ ] T3831-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T3829-34096618 | docs/dev/roadmap/v0.2-overview.md | 3826 | - [ ] T3832-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T3830-20dd0db7 | docs/dev/roadmap/v0.2-overview.md | 3827 | - [ ] T3833-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T3831-11874b07 | docs/dev/roadmap/v0.2-overview.md | 3828 | - [ ] T3834-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T3832-9c1bdc2c | docs/dev/roadmap/v0.2-overview.md | 3829 | - [ ] T3835-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T3833-d148c896 | docs/dev/roadmap/v0.2-overview.md | 3830 | - [ ] T3836-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T3834-b1101cad | docs/dev/roadmap/v0.2-overview.md | 3831 | - [ ] T3837-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T3835-5180bf6e | docs/dev/roadmap/v0.2-overview.md | 3832 | - [ ] T3838-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T3836-d05cd882 | docs/dev/roadmap/v0.2-overview.md | 3833 | - [ ] T3839-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T3837-e5d72a12 | docs/dev/roadmap/v0.2-overview.md | 3834 | - [ ] T3840-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T3838-9ce34fae | docs/dev/roadmap/v0.2-overview.md | 3835 | - [ ] T3841-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T3839-6d7bbe49 | docs/dev/roadmap/v0.2-overview.md | 3836 | - [ ] T3842-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T3840-bab30e87 | docs/dev/roadmap/v0.2-overview.md | 3837 | - [ ] T3843-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T3841-63217be1 | docs/dev/roadmap/v0.2-overview.md | 3838 | - [ ] T3844-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T3842-b8490cff | docs/dev/roadmap/v0.2-overview.md | 3839 | - [ ] T3845-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T3843-d82a93df | docs/dev/roadmap/v0.2-overview.md | 3840 | - [ ] T3846-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T3844-b504d90b | docs/dev/roadmap/v0.2-overview.md | 3841 | - [ ] T3847-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T3845-382eff3e | docs/dev/roadmap/v0.2-overview.md | 3842 | - [ ] T3848-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T3846-36b5eb45 | docs/dev/roadmap/v0.2-overview.md | 3843 | - [ ] T3849-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T3847-d05aec48 | docs/dev/roadmap/v0.2-overview.md | 3844 | - [ ] T3850-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T3848-a3079da3 | docs/dev/roadmap/v0.2-overview.md | 3845 | - [ ] T3851-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T3849-8c8609ca | docs/dev/roadmap/v0.2-overview.md | 3846 | - [ ] T3852-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T3850-cfae8a12 | docs/dev/roadmap/v0.2-overview.md | 3847 | - [ ] T3853-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T3851-31f8bc88 | docs/dev/roadmap/v0.2-overview.md | 3848 | - [ ] T3854-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T3852-d1c0617e | docs/dev/roadmap/v0.2-overview.md | 3849 | - [ ] T3855-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T3853-eab25f64 | docs/dev/roadmap/v0.2-overview.md | 3850 | - [ ] T3856-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T3854-7777a9f9 | docs/dev/roadmap/v0.2-overview.md | 3851 | - [ ] T3857-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T3855-424dffc6 | docs/dev/roadmap/v0.2-overview.md | 3852 | - [ ] T3858-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T3856-63999c07 | docs/dev/roadmap/v0.2-overview.md | 3853 | - [ ] T3859-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T3857-31d123fc | docs/dev/roadmap/v0.2-overview.md | 3854 | - [ ] T3860-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T3858-727e9c4f | docs/dev/roadmap/v0.2-overview.md | 3855 | - [ ] T3861-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T3859-7dc1870f | docs/dev/roadmap/v0.2-overview.md | 3856 | - [ ] T3862-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T3860-56c2b8e2 | docs/dev/roadmap/v0.2-overview.md | 3857 | - [ ] T3863-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T3861-4c764d8d | docs/dev/roadmap/v0.2-overview.md | 3858 | - [ ] T3864-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T3862-080d8316 | docs/dev/roadmap/v0.2-overview.md | 3859 | - [ ] T3865-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T3863-7b25ef7a | docs/dev/roadmap/v0.2-overview.md | 3860 | - [ ] T3866-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T3864-3bf988e2 | docs/dev/roadmap/v0.2-overview.md | 3861 | - [ ] T3867-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T3865-08c511ba | docs/dev/roadmap/v0.2-overview.md | 3862 | - [ ] T3868-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T3866-010ca29a | docs/dev/roadmap/v0.2-overview.md | 3863 | - [ ] T3869-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T3867-b2bac7ca | docs/dev/roadmap/v0.2-overview.md | 3864 | - [ ] T3870-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T3868-f15c8bd3 | docs/dev/roadmap/v0.2-overview.md | 3865 | - [ ] T3871-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T3869-45b15174 | docs/dev/roadmap/v0.2-overview.md | 3866 | - [ ] T3872-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T3870-c03db632 | docs/dev/roadmap/v0.2-overview.md | 3867 | - [ ] T3873-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T3871-1e112e03 | docs/dev/roadmap/v0.2-overview.md | 3868 | - [ ] T3874-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T3872-cb3369be | docs/dev/roadmap/v0.2-overview.md | 3869 | - [ ] T3875-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T3873-29091dc1 | docs/dev/roadmap/v0.2-overview.md | 3870 | - [ ] T3876-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T3874-cc53606c | docs/dev/roadmap/v0.2-overview.md | 3871 | - [ ] T3877-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T3875-47992027 | docs/dev/roadmap/v0.2-overview.md | 3872 | - [ ] T3878-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T3876-5b470d40 | docs/dev/roadmap/v0.2-overview.md | 3873 | - [ ] T3879-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T3877-97e01dca | docs/dev/roadmap/v0.2-overview.md | 3874 | - [ ] T3880-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T3878-dd802148 | docs/dev/roadmap/v0.2-overview.md | 3875 | - [ ] T3881-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T3879-0eff6d60 | docs/dev/roadmap/v0.2-overview.md | 3876 | - [ ] T3882-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T3880-57377174 | docs/dev/roadmap/v0.2-overview.md | 3877 | - [ ] T3883-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T3881-08c21c71 | docs/dev/roadmap/v0.2-overview.md | 3878 | - [ ] T3884-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T3882-9f5ef143 | docs/dev/roadmap/v0.2-overview.md | 3879 | - [ ] T3885-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T3883-e3bee53a | docs/dev/roadmap/v0.2-overview.md | 3880 | - [ ] T3886-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T3884-0ccace48 | docs/dev/roadmap/v0.2-overview.md | 3881 | - [ ] T3887-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T3885-992a35a5 | docs/dev/roadmap/v0.2-overview.md | 3882 | - [ ] T3888-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T3886-33dcb8e6 | docs/dev/roadmap/v0.2-overview.md | 3883 | - [ ] T3889-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T3887-ade3be7f | docs/dev/roadmap/v0.2-overview.md | 3884 | - [ ] T3890-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T3888-984c4f83 | docs/dev/roadmap/v0.2-overview.md | 3885 | - [ ] T3891-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T3889-010f1c28 | docs/dev/roadmap/v0.2-overview.md | 3886 | - [ ] T3892-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T3890-b1721b6e | docs/dev/roadmap/v0.2-overview.md | 3887 | - [ ] T3893-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T3891-2c33b9f3 | docs/dev/roadmap/v0.2-overview.md | 3888 | - [ ] T3894-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T3892-f0946ea1 | docs/dev/roadmap/v0.2-overview.md | 3889 | - [ ] T3895-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T3893-b64fca43 | docs/dev/roadmap/v0.2-overview.md | 3890 | - [ ] T3896-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T3894-1d8f801b | docs/dev/roadmap/v0.2-overview.md | 3891 | - [ ] T3897-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T3895-b5fd1fb4 | docs/dev/roadmap/v0.2-overview.md | 3892 | - [ ] T3898-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T3896-ff2ac410 | docs/dev/roadmap/v0.2-overview.md | 3893 | - [ ] T3899-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T3897-ad0c8ee8 | docs/dev/roadmap/v0.2-overview.md | 3894 | - [ ] T3900-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T3898-e5496a4b | docs/dev/roadmap/v0.2-overview.md | 3895 | - [ ] T3901-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T3899-6d8a847e | docs/dev/roadmap/v0.2-overview.md | 3896 | - [ ] T3902-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T3900-a01fe418 | docs/dev/roadmap/v0.2-overview.md | 3897 | - [ ] T3903-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T3901-fcab4ea5 | docs/dev/roadmap/v0.2-overview.md | 3898 | - [ ] T3904-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T3902-cea3d3d3 | docs/dev/roadmap/v0.2-overview.md | 3899 | - [ ] T3905-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T3903-d302515f | docs/dev/roadmap/v0.2-overview.md | 3900 | - [ ] T3906-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T3904-e4fe4e67 | docs/dev/roadmap/v0.2-overview.md | 3901 | - [ ] T3907-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T3905-3eab66e7 | docs/dev/roadmap/v0.2-overview.md | 3902 | - [ ] T3908-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T3906-d615231f | docs/dev/roadmap/v0.2-overview.md | 3903 | - [ ] T3909-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T3907-608114b2 | docs/dev/roadmap/v0.2-overview.md | 3904 | - [ ] T3910-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T3908-1c4e84e0 | docs/dev/roadmap/v0.2-overview.md | 3905 | - [ ] T3911-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T3909-44930cbe | docs/dev/roadmap/v0.2-overview.md | 3906 | - [ ] T3912-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T3910-cda4a99b | docs/dev/roadmap/v0.2-overview.md | 3907 | - [ ] T3913-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T3911-4dab8af0 | docs/dev/roadmap/v0.2-overview.md | 3908 | - [ ] T3914-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T3912-d1d69906 | docs/dev/roadmap/v0.2-overview.md | 3909 | - [ ] T3915-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T3913-d51f29fa | docs/dev/roadmap/v0.2-overview.md | 3910 | - [ ] T3916-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T3914-499832c9 | docs/dev/roadmap/v0.2-overview.md | 3911 | - [ ] T3917-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T3915-be2075f0 | docs/dev/roadmap/v0.2-overview.md | 3912 | - [ ] T3918-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T3916-8ffbbc02 | docs/dev/roadmap/v0.2-overview.md | 3913 | - [ ] T3919-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T3917-234cc806 | docs/dev/roadmap/v0.2-overview.md | 3914 | - [ ] T3920-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T3918-8360e408 | docs/dev/roadmap/v0.2-overview.md | 3915 | - [ ] T3921-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T3919-40707fe1 | docs/dev/roadmap/v0.2-overview.md | 3916 | - [ ] T3922-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T3920-c72b6f75 | docs/dev/roadmap/v0.2-overview.md | 3917 | - [ ] T3923-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T3921-fb62fdad | docs/dev/roadmap/v0.2-overview.md | 3918 | - [ ] T3924-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T3922-64017797 | docs/dev/roadmap/v0.3-plus/master-todo.md | 4 | ## Master TODO |
| T3923-d829486b | docs/dev/roadmap/v0.3-plus/master-todo.md | 6 | - [ ] T0005-eebdb0bc Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). (docs/release-checklist-v0.1.md:10) |
| T3924-878ffb5e | docs/dev/roadmap/v0.3-plus/master-todo.md | 7 | - [ ] T0006-6c054b93 **Conftest/OPA Policies** laufen sauber (`make ci-policy`). (docs/release-checklist-v0.1.md:11) |
| T3925-5ac5c2af | docs/dev/roadmap/v0.3-plus/master-todo.md | 8 | - [ ] T0008-105487d6 **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy. (docs/release-checklist-v0.1.md:13) |
| T3926-16f80f62 | docs/dev/roadmap/v0.3-plus/master-todo.md | 9 | - [ ] T0009-eca070fc **Ingress TLS** aktiv (cert-manager, staging Issuer OK). (docs/release-checklist-v0.1.md:14) |
| T3927-5df4e5b5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 10 | - [ ] T0010-32fc4428 Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv). (docs/release-checklist-v0.1.md:15) |
| T3928-7a8dc8b3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 11 | - [ ] T0011-4f3a4fbb **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report). (docs/release-checklist-v0.1.md:21) |
| T3929-83501199 | docs/dev/roadmap/v0.3-plus/master-todo.md | 12 | - [ ] T0012-d26eb117 **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page). (docs/release-checklist-v0.1.md:22) |
| T3930-77df7dc8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 13 | - [ ] T0013-d31f6320 **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert. (docs/release-checklist-v0.1.md:23) |
| T3931-3e9991b6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 14 | - [ ] T0014-685a9f1c **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün. (docs/release-checklist-v0.1.md:24) |
| T3932-47cf7162 | docs/dev/roadmap/v0.3-plus/master-todo.md | 15 | - [ ] T0015-ab336203 **Dependabot** aktiviert (pip, npm, GitHub Actions). (docs/release-checklist-v0.1.md:25) |
| T3933-d67084c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 16 | - [ ] T0016-8f6509a4 **Trivy Scan** ohne kritische Findings. (docs/release-checklist-v0.1.md:26) |
| T3934-200764c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 17 | - [ ] T0017-34585d61 **dbt build/test** grün (Seeds, Models, Tests). (docs/release-checklist-v0.1.md:32) |
| T3935-e3eb86f3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 18 | - [ ] T0018-2acaec2b **dbt docs generate** erzeugt Artefakt (Docs erreichbar). (docs/release-checklist-v0.1.md:33) |
| T3936-d6f01b8f | docs/dev/roadmap/v0.3-plus/master-todo.md | 19 | - [ ] T0019-8c283abc **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`). (docs/release-checklist-v0.1.md:34) |
| T3937-7c3eeba8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 20 | - [ ] T0020-3e64a531 **Exposures** definiert (Superset Dashboards verlinkt). (docs/release-checklist-v0.1.md:35) |
| T3938-45f3d671 | docs/dev/roadmap/v0.3-plus/master-todo.md | 21 | - [ ] T0021-5a64e8a4 **Freshness Checks** für Sources ohne Errors. (docs/release-checklist-v0.1.md:36) |
| T3939-a2b6e081 | docs/dev/roadmap/v0.3-plus/master-todo.md | 22 | - [ ] T0022-d46f9a42 **Superset Dashboard** „analytics_prices“ importiert: (docs/release-checklist-v0.1.md:42) |
| T3940-2b0fe2c6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 23 | - [ ] T0023-887e2ee6 **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert. (docs/release-checklist-v0.1.md:45) |
| T3941-c1de04e1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 24 | - [ ] T0024-7e0be2e1 Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News). (docs/release-checklist-v0.1.md:46) |
| T3942-770fa966 | docs/dev/roadmap/v0.3-plus/master-todo.md | 25 | - [ ] T0025-b8e15dc1 **Vitest/Playwright Tests** decken Detailseiten ab. (docs/release-checklist-v0.1.md:47) |
| T3943-8d93d202 | docs/dev/roadmap/v0.3-plus/master-todo.md | 26 | - [ ] T0026-852109aa **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar. (docs/release-checklist-v0.1.md:53) |
| T3944-ba375f18 | docs/dev/roadmap/v0.3-plus/master-todo.md | 27 | - [ ] T0027-6e44531b **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh. (docs/release-checklist-v0.1.md:54) |
| T3945-f6409a12 | docs/dev/roadmap/v0.3-plus/master-todo.md | 28 | - [ ] T0028-d0e1d9c3 **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j). (docs/release-checklist-v0.1.md:55) |
| T3946-f79ac11a | docs/dev/roadmap/v0.3-plus/master-todo.md | 29 | - [ ] T0029-574bfa1d Restore-Runbook einmal **trocken getestet**. (docs/release-checklist-v0.1.md:56) |
| T3947-064f902d | docs/dev/roadmap/v0.3-plus/master-todo.md | 30 | - [ ] T0030-a42b9b1e **OTel Collector** deployed (4317/4318/9464 erreichbar). (docs/release-checklist-v0.1.md:62) |
| T3948-8ddd28df | docs/dev/roadmap/v0.3-plus/master-todo.md | 31 | - [ ] T0031-3686a8ea **Python Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:63) |
| T3949-a543498b | docs/dev/roadmap/v0.3-plus/master-todo.md | 32 | - [ ] T0032-50c95364 **Node Services** exportieren Traces + `/metrics`. (docs/release-checklist-v0.1.md:64) |
| T3950-820ab0dc | docs/dev/roadmap/v0.3-plus/master-todo.md | 33 | - [ ] T0033-fd890733 **Prometheus** scrapt Services; Grafana Panels gefüllt. (docs/release-checklist-v0.1.md:65) |
| T3951-b6b4e00f | docs/dev/roadmap/v0.3-plus/master-todo.md | 34 | - [ ] T0034-81973fbd **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB). (docs/release-checklist-v0.1.md:66) |
| T3952-9d2abe4d | docs/dev/roadmap/v0.3-plus/master-todo.md | 35 | - [ ] T0035-b3e96bed **Loki** enthält Logs aller Services (Promtail shipping OK). (docs/release-checklist-v0.1.md:67) |
| T3953-56b582df | docs/dev/roadmap/v0.3-plus/master-todo.md | 36 | - [ ] T0036-206b6181 **Grafana Dashboards**: (docs/release-checklist-v0.1.md:68) |
| T3954-1467a171 | docs/dev/roadmap/v0.3-plus/master-todo.md | 37 | - [ ] T0037-f9ff8ace **README** Quickstart aktualisiert (Makefile Targets, Health-Checks). (docs/release-checklist-v0.1.md:76) |
| T3955-1c138272 | docs/dev/roadmap/v0.3-plus/master-todo.md | 38 | - [ ] T0038-f0bed26f **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo. (docs/release-checklist-v0.1.md:77) |
| T3956-abd4e2f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 39 | - [ ] T0039-e2d936fa **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin. (docs/release-checklist-v0.1.md:78) |
| T3957-4eee7b9c | docs/dev/roadmap/v0.3-plus/master-todo.md | 40 | - [ ] T0040-8dc3e1de **Language Policy**: Docs in EN, DE als Appendix. (docs/release-checklist-v0.1.md:79) |
| T3958-0d1b0571 | docs/dev/roadmap/v0.3-plus/master-todo.md | 41 | - [ ] T0041-72f3bcfb **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo. (docs/release-checklist-v0.1.md:80) |
| T3959-87471c36 | docs/dev/roadmap/v0.3-plus/master-todo.md | 42 | - [ ] T0042-ffe9d529 **CI Docs-Checks** grün (markdownlint, link check, doctoc). (docs/release-checklist-v0.1.md:81) |
| T3960-e301b8da | docs/dev/roadmap/v0.3-plus/master-todo.md | 43 | - [ ] T0043-60e9ff73 **Secrets** in Staging (Vault/ExternalSecrets) gesetzt. (docs/release-checklist-v0.1.md:87) |
| T3961-5c6dd53f | docs/dev/roadmap/v0.3-plus/master-todo.md | 44 | - [ ] T0044-c0036628 **Ingress Hosts** & TLS validiert. (docs/release-checklist-v0.1.md:88) |
| T3962-c5070420 | docs/dev/roadmap/v0.3-plus/master-todo.md | 45 | - [ ] T0045-c622e84c **Demo-Data Seed** erfolgreich (`make seed-demo`). (docs/release-checklist-v0.1.md:89) |
| T3963-fa3c8255 | docs/dev/roadmap/v0.3-plus/master-todo.md | 46 | - [ ] T0046-1aba4558 **Smoke-Test** im Staging: (docs/release-checklist-v0.1.md:90) |
| T3964-47203e64 | docs/dev/roadmap/v0.3-plus/master-todo.md | 47 | - [ ] T0047-63c7922a `main` eingefroren, `release/v0.1` Branch erstellt. (docs/release-checklist-v0.1.md:103) |
| T3965-f3c48a61 | docs/dev/roadmap/v0.3-plus/master-todo.md | 48 | - [ ] T0048-0400782a **Changelog** generiert (`git log --oneline v0.0.0..HEAD`). (docs/release-checklist-v0.1.md:104) |
| T3966-50c29e23 | docs/dev/roadmap/v0.3-plus/master-todo.md | 49 | - [ ] T0049-b6c0d1dc **Release Notes** erstellt (Features, Breaking Changes, Known Issues). (docs/release-checklist-v0.1.md:105) |
| T3967-fbcbfa99 | docs/dev/roadmap/v0.3-plus/master-todo.md | 50 | - [ ] T0050-bac8349c **Tag v0.1.0** gesetzt und Release publiziert. (docs/release-checklist-v0.1.md:106) |
| T3968-9e3d34a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 51 | - [ ] T0051-34456b6a Dokumentation zur Installation/Exploration angehängt. (docs/release-checklist-v0.1.md:107) |
| T3969-8a089808 | docs/dev/roadmap/v0.3-plus/master-todo.md | 52 | - [ ] T3604-49f1ca8b TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! (docs/dev/v0.2/Datenquellen-Cluster.md:89) |
| T3970-a731fbe7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 53 | - [ ] T3605-c53b285c ## 📋 Tickets (zum TODO-Index hinzufügen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:170) |
| T3971-d48e33ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 54 | - [ ] T3606-640680d3 ## TODO: (docs/dev/v0.2/FlowiseAI-Agents-integration.md:217) |
| T3972-e62264b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 55 | - [ ] T3607-30cd45d8 * `TODO-Index.md` (FLOWISE-Tickets anhängen) (docs/dev/v0.2/FlowiseAI-Agents-integration.md:220) |
| T3973-a81f4f30 | docs/dev/roadmap/v0.3-plus/master-todo.md | 56 | - [ ] T3608-4c66e9b1 # Umsetzung: Tickets (zum Master TODO-Index ergänzen) (docs/dev/v0.2/Preset-Profile.md:155) |
| T3974-67ed4571 | docs/dev/roadmap/v0.3-plus/master-todo.md | 57 | - [ ] T3609-813e30e1 TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. (docs/dev/v0.2/Preset-Profile.md:162) |
| T3975-c201e358 | docs/dev/roadmap/v0.3-plus/master-todo.md | 58 | - [ ] T3610-7fda6ac5 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/TODO-Index.md:1) |
| T3976-729324ac | docs/dev/roadmap/v0.3-plus/master-todo.md | 59 | - [ ] T3611-96c614d5 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/TODO-Index.md:9) |
| T3977-348ecb8e | docs/dev/roadmap/v0.3-plus/master-todo.md | 60 | - [ ] T3612-6b53c8a4 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/TODO-Index.md:10) |
| T3978-c9aa7eee | docs/dev/roadmap/v0.3-plus/master-todo.md | 61 | - [ ] T3613-daa23089 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/TODO-Index.md:11) |
| T3979-11fc2eb5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 62 | - [ ] T3614-f9c44215 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/TODO-Index.md:12) |
| T3980-cd2a53cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 63 | - [ ] T3615-40201c9c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/TODO-Index.md:13) |
| T3981-574d10df | docs/dev/roadmap/v0.3-plus/master-todo.md | 64 | - [ ] T3616-6751fa30 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/TODO-Index.md:16) |
| T3982-e4fa93cf | docs/dev/roadmap/v0.3-plus/master-todo.md | 65 | - [ ] T3617-af050ca3 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/TODO-Index.md:17) |
| T3983-3f7c18d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 66 | - [ ] T3618-59b8bd9a **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/TODO-Index.md:18) |
| T3984-823d15ef | docs/dev/roadmap/v0.3-plus/master-todo.md | 67 | - [ ] T3619-67ada37b **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/TODO-Index.md:19) |
| T3985-612e1f57 | docs/dev/roadmap/v0.3-plus/master-todo.md | 68 | - [ ] T3620-b2f142a9 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/TODO-Index.md:20) |
| T3986-4cd0609f | docs/dev/roadmap/v0.3-plus/master-todo.md | 69 | - [ ] T3621-583511c7 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/TODO-Index.md:23) |
| T3987-28819faf | docs/dev/roadmap/v0.3-plus/master-todo.md | 70 | - [ ] T3622-d447eff2 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/TODO-Index.md:24) |
| T3988-20e2994f | docs/dev/roadmap/v0.3-plus/master-todo.md | 71 | - [ ] T3623-b65ad138 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/TODO-Index.md:25) |
| T3989-dc9a02b9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 72 | - [ ] T3624-55a9d5ec **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/TODO-Index.md:26) |
| T3990-dab27d31 | docs/dev/roadmap/v0.3-plus/master-todo.md | 73 | - [ ] T3625-691f4516 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/TODO-Index.md:27) |
| T3991-8d5fc614 | docs/dev/roadmap/v0.3-plus/master-todo.md | 74 | - [ ] T3626-820ca449 **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/TODO-Index.md:30) |
| T3992-6ce6a6bb | docs/dev/roadmap/v0.3-plus/master-todo.md | 75 | - [ ] T3627-712e08d4 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/TODO-Index.md:31) |
| T3993-516d03ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 76 | - [ ] T3628-2b976b3e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/TODO-Index.md:32) |
| T3994-a48b0b29 | docs/dev/roadmap/v0.3-plus/master-todo.md | 77 | - [ ] T3629-cb6348b8 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/TODO-Index.md:33) |
| T3995-124231ca | docs/dev/roadmap/v0.3-plus/master-todo.md | 78 | - [ ] T3630-3943b83a **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/TODO-Index.md:36) |
| T3996-7b425150 | docs/dev/roadmap/v0.3-plus/master-todo.md | 79 | - [ ] T3631-239835d3 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/TODO-Index.md:37) |
| T3997-fe67017f | docs/dev/roadmap/v0.3-plus/master-todo.md | 80 | - [ ] T3632-1740a146 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/TODO-Index.md:38) |
| T3998-4f99ca90 | docs/dev/roadmap/v0.3-plus/master-todo.md | 81 | - [ ] T3633-9abc3901 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/TODO-Index.md:39) |
| T3999-1f1ef716 | docs/dev/roadmap/v0.3-plus/master-todo.md | 82 | - [ ] T3634-23ac25a1 **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/TODO-Index.md:40) |
| T4000-52d7d998 | docs/dev/roadmap/v0.3-plus/master-todo.md | 83 | - [ ] T3635-c22256e6 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/TODO-Index.md:41) |
| T4001-0fdf5959 | docs/dev/roadmap/v0.3-plus/master-todo.md | 84 | - [ ] T3636-937e2f61 **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/TODO-Index.md:42) |
| T4002-aad84e25 | docs/dev/roadmap/v0.3-plus/master-todo.md | 85 | - [ ] T3637-bb528afa **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/TODO-Index.md:43) |
| T4003-4928580b | docs/dev/roadmap/v0.3-plus/master-todo.md | 86 | - [ ] T3638-8977f932 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/TODO-Index.md:44) |
| T4004-97a6917b | docs/dev/roadmap/v0.3-plus/master-todo.md | 87 | - [ ] T3639-fcc18c85 **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/TODO-Index.md:45) |
| T4005-3eb973ef | docs/dev/roadmap/v0.3-plus/master-todo.md | 88 | - [ ] T3640-6700f0dc **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/TODO-Index.md:48) |
| T4006-a5b09680 | docs/dev/roadmap/v0.3-plus/master-todo.md | 89 | - [ ] T3641-7bb02d96 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/TODO-Index.md:49) |
| T4007-9bff53f6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 90 | - [ ] T3642-aa570ddf **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/TODO-Index.md:50) |
| T4008-9553260a | docs/dev/roadmap/v0.3-plus/master-todo.md | 91 | - [ ] T3643-2d5151d5 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/TODO-Index.md:51) |
| T4009-e2db8d48 | docs/dev/roadmap/v0.3-plus/master-todo.md | 92 | - [ ] T3644-41cc3d9c **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/TODO-Index.md:54) |
| T4010-178b406a | docs/dev/roadmap/v0.3-plus/master-todo.md | 93 | - [ ] T3645-b872722a **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/TODO-Index.md:55) |
| T4011-3bfaa37a | docs/dev/roadmap/v0.3-plus/master-todo.md | 94 | - [ ] T3646-d2c73ca4 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/TODO-Index.md:56) |
| T4012-d594b8ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 95 | - [ ] T3647-2f805132 **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/TODO-Index.md:57) |
| T4013-2f9c32e2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 96 | - [ ] T3648-538cc227 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/TODO-Index.md:58) |
| T4014-64ac7f70 | docs/dev/roadmap/v0.3-plus/master-todo.md | 97 | - [ ] T3649-4cbbedec **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/TODO-Index.md:59) |
| T4015-53e7879a | docs/dev/roadmap/v0.3-plus/master-todo.md | 98 | - [ ] T3650-a9315cdf **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation (docs/dev/v0.2/TODO-Index.md:60) |
| T4016-01a537ba | docs/dev/roadmap/v0.3-plus/master-todo.md | 99 | - [ ] T3651-f81ce959 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/TODO-Index.md:63) |
| T4017-236dab9a | docs/dev/roadmap/v0.3-plus/master-todo.md | 100 | - [ ] T3652-a2ff9eaa **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/TODO-Index.md:64) |
| T4018-d07a171b | docs/dev/roadmap/v0.3-plus/master-todo.md | 101 | - [ ] T3653-edefb47a **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/TODO-Index.md:65) |
| T4019-5344ad65 | docs/dev/roadmap/v0.3-plus/master-todo.md | 102 | - [ ] T3654-05512e8e **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/TODO-Index.md:66) |
| T4020-688bf39f | docs/dev/roadmap/v0.3-plus/master-todo.md | 103 | - [ ] T3655-27928674 **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/TODO-Index.md:67) |
| T4021-be2bc467 | docs/dev/roadmap/v0.3-plus/master-todo.md | 104 | - [ ] T3656-670382ca **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/TODO-Index.md:68) |
| T4022-a0c6312a | docs/dev/roadmap/v0.3-plus/master-todo.md | 105 | - [ ] T3657-83fe939a **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/TODO-Index.md:69) |
| T4023-22a94ecf | docs/dev/roadmap/v0.3-plus/master-todo.md | 106 | - [ ] T3658-2296ac84 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/TODO-Index.md:72) |
| T4024-09ae17f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 107 | - [ ] T3660-bb757a60 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/TODO-Index.md:74) |
| T4025-4765f3d3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 108 | - [ ] T3661-b21c66b1 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/TODO-Index.md:75) |
| T4026-b811b9a5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 109 | - [ ] T3662-858d65b1 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/TODO-Index.md:76) |
| T4027-7efbabbe | docs/dev/roadmap/v0.3-plus/master-todo.md | 110 | - [ ] T3663-fa9a75ec **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/TODO-Index.md:79) |
| T4028-635a1179 | docs/dev/roadmap/v0.3-plus/master-todo.md | 111 | - [ ] T3664-e9a60584 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/TODO-Index.md:80) |
| T4029-454a94d6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 112 | - [ ] T3665-12a45cbe **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/TODO-Index.md:81) |
| T4030-3177c056 | docs/dev/roadmap/v0.3-plus/master-todo.md | 113 | - [ ] T3666-6a239443 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/TODO-Index.md:82) |
| T4031-b0bf64ea | docs/dev/roadmap/v0.3-plus/master-todo.md | 114 | - [ ] T3667-50dfc868 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/TODO-Index.md:83) |
| T4032-1d6397a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 115 | - [ ] T3668-e4176dd4 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/TODO-Index.md:88) |
| T4033-1a26558b | docs/dev/roadmap/v0.3-plus/master-todo.md | 116 | - [ ] T3669-76860348 **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/TODO-Index.md:89) |
| T4034-7ee36378 | docs/dev/roadmap/v0.3-plus/master-todo.md | 117 | - [ ] T3670-09020bc9 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/TODO-Index.md:90) |
| T4035-2d85e80c | docs/dev/roadmap/v0.3-plus/master-todo.md | 118 | - [ ] T3671-312b93e0 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/TODO-Index.md:91) |
| T4036-afed4795 | docs/dev/roadmap/v0.3-plus/master-todo.md | 119 | - [ ] T3672-486ef2ed **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/TODO-Index.md:92) |
| T4037-f9a127e0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 120 | - [ ] T3673-1fb00e36 **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/TODO-Index.md:93) |
| T4038-0b2489e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 121 | - [ ] T3674-e046d4d0 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/TODO-Index.md:94) |
| T4039-c06e8a51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 122 | - [ ] T3675-16c0defd **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/TODO-Index.md:95) |
| T4040-e0dc3140 | docs/dev/roadmap/v0.3-plus/master-todo.md | 123 | - [ ] T3676-07d9b72a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/TODO-Index.md:96) |
| T4041-42b461f0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 124 | - [ ] T3677-120d3b48 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/TODO-Index.md:97) |
| T4042-431999b3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 125 | - [ ] T3678-37a44314 **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/TODO-Index.md:98) |
| T4043-6df6091e | docs/dev/roadmap/v0.3-plus/master-todo.md | 126 | - [ ] T3679-f6f0ac08 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/TODO-Index.md:99) |
| T4044-cb67faab | docs/dev/roadmap/v0.3-plus/master-todo.md | 127 | - [ ] T3680-f47ef523 **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/TODO-Index.md:100) |
| T4045-459a09e3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 128 | - [ ] T3681-1e77dce9 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/TODO-Index.md:101) |
| T4046-5cdbcb65 | docs/dev/roadmap/v0.3-plus/master-todo.md | 129 | - [ ] T3682-7fb20f8d **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/TODO-Index.md:102) |
| T4047-f5640b60 | docs/dev/roadmap/v0.3-plus/master-todo.md | 130 | - [ ] T3683-1c9c78b6 **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/TODO-Index.md:107) |
| T4048-2002c94b | docs/dev/roadmap/v0.3-plus/master-todo.md | 131 | - [ ] T3684-2fc57e38 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/TODO-Index.md:108) |
| T4049-b5d1af3b | docs/dev/roadmap/v0.3-plus/master-todo.md | 132 | - [ ] T3685-5950a90f **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/TODO-Index.md:109) |
| T4050-af746ab5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 133 | - [ ] T3686-1e613ad0 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/TODO-Index.md:110) |
| T4051-ad4d4916 | docs/dev/roadmap/v0.3-plus/master-todo.md | 134 | - [ ] T3687-3e09c258 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/TODO-Index.md:111) |
| T4052-846b3089 | docs/dev/roadmap/v0.3-plus/master-todo.md | 135 | - [ ] T3688-df0fea1d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/TODO-Index.md:112) |
| T4053-1bf6a490 | docs/dev/roadmap/v0.3-plus/master-todo.md | 136 | - [ ] T3689-f0796a6f **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/TODO-Index.md:113) |
| T4054-497c864f | docs/dev/roadmap/v0.3-plus/master-todo.md | 137 | - [ ] T3690-5ad28f17 **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/TODO-Index.md:114) |
| T4055-939c24ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 138 | - [ ] T3691-0c056d58 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/TODO-Index.md:115) |
| T4056-9ab90955 | docs/dev/roadmap/v0.3-plus/master-todo.md | 139 | - [ ] T3692-6a135243 **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/TODO-Index.md:116) |
| T4057-e4e01076 | docs/dev/roadmap/v0.3-plus/master-todo.md | 140 | - [ ] T3693-2a9efbbd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/TODO-Index.md:117) |
| T4058-16451feb | docs/dev/roadmap/v0.3-plus/master-todo.md | 141 | - [ ] T3694-c3e76b03 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) (docs/dev/v0.2/Ticket-Checkliste.md:1) |
| T4059-d8df5b08 | docs/dev/roadmap/v0.3-plus/master-todo.md | 142 | - [ ] T3695-3c74f562 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/Ticket-Checkliste.md:9) |
| T4060-0195196d | docs/dev/roadmap/v0.3-plus/master-todo.md | 143 | - [ ] T3696-86384cee **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/Ticket-Checkliste.md:10) |
| T4061-311fccdf | docs/dev/roadmap/v0.3-plus/master-todo.md | 144 | - [ ] T3697-f1ebad68 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/Ticket-Checkliste.md:11) |
| T4062-15099383 | docs/dev/roadmap/v0.3-plus/master-todo.md | 145 | - [ ] T3698-ef38943a **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/Ticket-Checkliste.md:12) |
| T4063-ced19959 | docs/dev/roadmap/v0.3-plus/master-todo.md | 146 | - [ ] T3699-2c4e0e55 **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:13) |
| T4064-556d1043 | docs/dev/roadmap/v0.3-plus/master-todo.md | 147 | - [ ] T3700-260ec1ba **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/Ticket-Checkliste.md:16) |
| T4065-322b7277 | docs/dev/roadmap/v0.3-plus/master-todo.md | 148 | - [ ] T3701-cf392a31 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/Ticket-Checkliste.md:17) |
| T4066-db6d0e1e | docs/dev/roadmap/v0.3-plus/master-todo.md | 149 | - [ ] T3702-c2929de2 **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/Ticket-Checkliste.md:18) |
| T4067-4707a736 | docs/dev/roadmap/v0.3-plus/master-todo.md | 150 | - [ ] T3703-99a53243 **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/Ticket-Checkliste.md:19) |
| T4068-eee93766 | docs/dev/roadmap/v0.3-plus/master-todo.md | 151 | - [ ] T3704-bd7b9b38 **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/Ticket-Checkliste.md:20) |
| T4069-bf1bf0dc | docs/dev/roadmap/v0.3-plus/master-todo.md | 152 | - [ ] T3705-fd8d5463 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/Ticket-Checkliste.md:23) |
| T4070-2567624d | docs/dev/roadmap/v0.3-plus/master-todo.md | 153 | - [ ] T3706-fe9c9b01 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/Ticket-Checkliste.md:24) |
| T4071-8a513958 | docs/dev/roadmap/v0.3-plus/master-todo.md | 154 | - [ ] T3707-fb88ffb0 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/Ticket-Checkliste.md:25) |
| T4072-4b56f8fc | docs/dev/roadmap/v0.3-plus/master-todo.md | 155 | - [ ] T3708-930adfd5 **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/Ticket-Checkliste.md:26) |
| T4073-fd27985c | docs/dev/roadmap/v0.3-plus/master-todo.md | 156 | - [ ] T3709-4371a444 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/Ticket-Checkliste.md:27) |
| T4074-ab3cd3f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 157 | - [ ] T3710-a1249e1c **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/Ticket-Checkliste.md:30) |
| T4075-d56d3257 | docs/dev/roadmap/v0.3-plus/master-todo.md | 158 | - [ ] T3711-8031896a **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/Ticket-Checkliste.md:31) |
| T4076-b3dec37f | docs/dev/roadmap/v0.3-plus/master-todo.md | 159 | - [ ] T3712-4e3ab17e **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/Ticket-Checkliste.md:32) |
| T4077-390ca027 | docs/dev/roadmap/v0.3-plus/master-todo.md | 160 | - [ ] T3713-2ecc8c30 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/Ticket-Checkliste.md:33) |
| T4078-5b7645ff | docs/dev/roadmap/v0.3-plus/master-todo.md | 161 | - [ ] T3714-2e7ef320 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/Ticket-Checkliste.md:36) |
| T4079-057b06f8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 162 | - [ ] T3715-f5ef504e **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/Ticket-Checkliste.md:37) |
| T4080-910552dc | docs/dev/roadmap/v0.3-plus/master-todo.md | 163 | - [ ] T3716-8249b090 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/Ticket-Checkliste.md:38) |
| T4081-644ab7c1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 164 | - [ ] T3717-53434e25 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/Ticket-Checkliste.md:39) |
| T4082-670dfd7a | docs/dev/roadmap/v0.3-plus/master-todo.md | 165 | - [ ] T3718-f4718a0d **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/Ticket-Checkliste.md:40) |
| T4083-438fdf8d | docs/dev/roadmap/v0.3-plus/master-todo.md | 166 | - [ ] T3719-2e62061b **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/Ticket-Checkliste.md:41) |
| T4084-03882a11 | docs/dev/roadmap/v0.3-plus/master-todo.md | 167 | - [ ] T3720-7965089b **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/Ticket-Checkliste.md:42) |
| T4085-61a29ff3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 168 | - [ ] T3721-361b2744 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/Ticket-Checkliste.md:43) |
| T4086-d7383c93 | docs/dev/roadmap/v0.3-plus/master-todo.md | 169 | - [ ] T3722-57338d8b **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/Ticket-Checkliste.md:46) |
| T4087-269fc4ef | docs/dev/roadmap/v0.3-plus/master-todo.md | 170 | - [ ] T3723-3f9b35c6 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/Ticket-Checkliste.md:47) |
| T4088-f4a0275f | docs/dev/roadmap/v0.3-plus/master-todo.md | 171 | - [ ] T3724-b3a4b50c **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/Ticket-Checkliste.md:48) |
| T4089-0f64d66b | docs/dev/roadmap/v0.3-plus/master-todo.md | 172 | - [ ] T3725-3d064402 **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/Ticket-Checkliste.md:49) |
| T4090-a301efbf | docs/dev/roadmap/v0.3-plus/master-todo.md | 173 | - [ ] T3726-9f55a7e3 **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:52) |
| T4091-7f84cf73 | docs/dev/roadmap/v0.3-plus/master-todo.md | 174 | - [ ] T3727-57541fe4 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/Ticket-Checkliste.md:53) |
| T4092-ae8258c4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 175 | - [ ] T3728-5b962c45 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/Ticket-Checkliste.md:54) |
| T4093-43f4ec07 | docs/dev/roadmap/v0.3-plus/master-todo.md | 176 | - [ ] T3729-33e5f56d **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/Ticket-Checkliste.md:55) |
| T4094-f89d8f79 | docs/dev/roadmap/v0.3-plus/master-todo.md | 177 | - [ ] T3730-a3e06510 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/Ticket-Checkliste.md:56) |
| T4095-59c1ee65 | docs/dev/roadmap/v0.3-plus/master-todo.md | 178 | - [ ] T3731-61eaba80 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/Ticket-Checkliste.md:57) |
| T4096-d2862e44 | docs/dev/roadmap/v0.3-plus/master-todo.md | 179 | - [ ] T3732-916bb7e9 **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/Ticket-Checkliste.md:60) |
| T4097-09102357 | docs/dev/roadmap/v0.3-plus/master-todo.md | 180 | - [ ] T3733-49602af1 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/Ticket-Checkliste.md:61) |
| T4098-738ccf39 | docs/dev/roadmap/v0.3-plus/master-todo.md | 181 | - [ ] T3734-8ca4f49d **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/Ticket-Checkliste.md:62) |
| T4099-43be0d55 | docs/dev/roadmap/v0.3-plus/master-todo.md | 182 | - [ ] T3735-7ca5c4fb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/Ticket-Checkliste.md:63) |
| T4100-b2674a51 | docs/dev/roadmap/v0.3-plus/master-todo.md | 183 | - [ ] T3736-03560a6d **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/Ticket-Checkliste.md:64) |
| T4101-34e0f0a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 184 | - [ ] T3737-212d7d93 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/Ticket-Checkliste.md:67) |
| T4102-d5a9159c | docs/dev/roadmap/v0.3-plus/master-todo.md | 185 | - [ ] T3739-46578c8e **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/Ticket-Checkliste.md:69) |
| T4103-9f7c0947 | docs/dev/roadmap/v0.3-plus/master-todo.md | 186 | - [ ] T3740-cddb81e2 **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/Ticket-Checkliste.md:70) |
| T4104-91db2f28 | docs/dev/roadmap/v0.3-plus/master-todo.md | 187 | - [ ] T3741-f7bd1421 **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/Ticket-Checkliste.md:71) |
| T4105-e1b56349 | docs/dev/roadmap/v0.3-plus/master-todo.md | 188 | - [ ] T3742-5a2d6148 **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/Ticket-Checkliste.md:74) |
| T4106-46839915 | docs/dev/roadmap/v0.3-plus/master-todo.md | 189 | - [ ] T3743-d15bbcb1 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/Ticket-Checkliste.md:75) |
| T4107-3f74ba5e | docs/dev/roadmap/v0.3-plus/master-todo.md | 190 | - [ ] T3744-08448e85 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/Ticket-Checkliste.md:76) |
| T4108-410051e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 191 | - [ ] T3745-d2236406 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/Ticket-Checkliste.md:77) |
| T4109-68c9fbb7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 192 | - [ ] T3746-9bd657cd **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/Ticket-Checkliste.md:78) |
| T4110-1f6c03e6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 193 | - [ ] T3747-9b019ff4 # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:1) |
| T4111-56181779 | docs/dev/roadmap/v0.3-plus/master-todo.md | 194 | - [ ] T3748-98e90d90 **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:9) |
| T4112-0ab98c44 | docs/dev/roadmap/v0.3-plus/master-todo.md | 195 | - [ ] T3749-65a07da1 **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:10) |
| T4113-098a7aa1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 196 | - [ ] T3750-bf0ac642 **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:11) |
| T4114-83f1c87d | docs/dev/roadmap/v0.3-plus/master-todo.md | 197 | - [ ] T3751-c7b2ea55 **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:12) |
| T4115-f18aad80 | docs/dev/roadmap/v0.3-plus/master-todo.md | 198 | - [ ] T3752-a895be4c **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:13) |
| T4116-b24a2cfa | docs/dev/roadmap/v0.3-plus/master-todo.md | 199 | - [ ] T3753-80a2e913 **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:16) |
| T4117-fbe2d3ca | docs/dev/roadmap/v0.3-plus/master-todo.md | 200 | - [ ] T3754-2c6aa5b0 **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:17) |
| T4118-1d6890e2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 201 | - [ ] T3755-1030e0fd **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:18) |
| T4119-528e2892 | docs/dev/roadmap/v0.3-plus/master-todo.md | 202 | - [ ] T3756-3c059eea **[GRAPH-4]** Graph-Export (GraphML, JSON) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:19) |
| T4120-8fe42280 | docs/dev/roadmap/v0.3-plus/master-todo.md | 203 | - [ ] T3757-7e80880f **[GRAPH-5]** Audit: Query-Logs + Query-Metrics (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:20) |
| T4121-e8505b70 | docs/dev/roadmap/v0.3-plus/master-todo.md | 204 | - [ ] T3758-d25582d3 **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:23) |
| T4122-7719a8cd | docs/dev/roadmap/v0.3-plus/master-todo.md | 205 | - [ ] T3759-041e81a9 **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:24) |
| T4123-90ba0450 | docs/dev/roadmap/v0.3-plus/master-todo.md | 206 | - [ ] T3760-fd930023 **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:25) |
| T4124-23fbb6be | docs/dev/roadmap/v0.3-plus/master-todo.md | 207 | - [ ] T3761-3c21423e **[SEARCH-4]** Export: JSON/CSV Dumps pro Index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:26) |
| T4125-5a7670bb | docs/dev/roadmap/v0.3-plus/master-todo.md | 208 | - [ ] T3762-41fef9d2 **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:27) |
| T4126-a56660fc | docs/dev/roadmap/v0.3-plus/master-todo.md | 209 | - [ ] T3763-9e560efe **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:30) |
| T4127-b16caae9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 210 | - [ ] T3764-37219dc9 **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:31) |
| T4128-98e862fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 211 | - [ ] T3765-66bd4524 **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:32) |
| T4129-08b9a72b | docs/dev/roadmap/v0.3-plus/master-todo.md | 212 | - [ ] T3766-6e54ac16 **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:33) |
| T4130-d8bb59b1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 213 | - [ ] T3767-c05d7b58 **[FE-1]** Einheitliches Theme (globals.css konsolidieren) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:36) |
| T4131-63351570 | docs/dev/roadmap/v0.3-plus/master-todo.md | 214 | - [ ] T3768-09986fb5 **[FE-2]** /search: Facettenfilter + Ranking-Regler (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:37) |
| T4132-8485a938 | docs/dev/roadmap/v0.3-plus/master-todo.md | 215 | - [ ] T3769-7ca3edc4 **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:38) |
| T4133-55793ff1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 216 | - [ ] T3770-bfd46364 **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:39) |
| T4134-b6823e7f | docs/dev/roadmap/v0.3-plus/master-todo.md | 217 | - [ ] T3771-6ecc94ac **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:40) |
| T4135-e4c53fdb | docs/dev/roadmap/v0.3-plus/master-todo.md | 218 | - [ ] T3772-7ca78b51 **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:41) |
| T4136-9a46b36d | docs/dev/roadmap/v0.3-plus/master-todo.md | 219 | - [ ] T3773-1b1da82d **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:42) |
| T4137-847abca4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 220 | - [ ] T3774-e05ddd88 **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:43) |
| T4138-f59a767e | docs/dev/roadmap/v0.3-plus/master-todo.md | 221 | - [ ] T3775-2ffc74f0 **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:44) |
| T4139-bf5013a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 222 | - [ ] T3776-45fd5c7b **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:45) |
| T4140-b9e75ec7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 223 | - [ ] T3777-0b8d92a4 **[GATE-1]** OAuth2/OIDC Support (JWT Validation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:48) |
| T4141-d71114a8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 224 | - [ ] T3778-a0c3bfe4 **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:49) |
| T4142-444cfa67 | docs/dev/roadmap/v0.3-plus/master-todo.md | 225 | - [ ] T3779-3f86dd6a **[GATE-3]** Attribute-Level Security vorbereiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:50) |
| T4143-7186f54d | docs/dev/roadmap/v0.3-plus/master-todo.md | 226 | - [ ] T3780-6b86dd7e **[GATE-4]** Audit-Logs in Loki weiterleiten (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:51) |
| T4144-be3a7ec9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 227 | - [ ] T3781-1d7717fb **[NIFI-1]** RSS/Atom Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:54) |
| T4145-e6d371a4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 228 | - [ ] T3782-0c39b3a6 **[NIFI-2]** API Ingest Flow (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:55) |
| T4146-c696b0d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 229 | - [ ] T3783-2ef30966 **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:56) |
| T4147-7a022a3b | docs/dev/roadmap/v0.3-plus/master-todo.md | 230 | - [ ] T3784-fc5ed44a **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:57) |
| T4148-ee082d32 | docs/dev/roadmap/v0.3-plus/master-todo.md | 231 | - [ ] T3785-51d406f2 **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:58) |
| T4149-b658845c | docs/dev/roadmap/v0.3-plus/master-todo.md | 232 | - [ ] T3786-153dda62 **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:59) |
| T4150-a0946be4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 233 | - [ ] T3787-ddc6f2da **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:60) |
| T4151-f2429f4e | docs/dev/roadmap/v0.3-plus/master-todo.md | 234 | - [ ] T3788-ac36672e **[N8N-1]** Investigation Assistant Flow (search+graph queries) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:63) |
| T4152-c5a86c9b | docs/dev/roadmap/v0.3-plus/master-todo.md | 235 | - [ ] T3789-a9312730 **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:64) |
| T4153-545fcc88 | docs/dev/roadmap/v0.3-plus/master-todo.md | 236 | - [ ] T3790-372c0169 **[N8N-3]** Cross-Source Correlation (news+social+plugins) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:65) |
| T4154-8fb62568 | docs/dev/roadmap/v0.3-plus/master-todo.md | 237 | - [ ] T3791-fd4e6beb **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:66) |
| T4155-148ba69f | docs/dev/roadmap/v0.3-plus/master-todo.md | 238 | - [ ] T3792-8215cd0e **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:67) |
| T4156-482785c8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 239 | - [ ] T3793-7ca16b98 **[N8N-6]** Veracity Alerts (false/manipulative → escalate) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:68) |
| T4157-8e9c630e | docs/dev/roadmap/v0.3-plus/master-todo.md | 240 | - [ ] T3794-1981f93b **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:69) |
| T4158-7fdaf36d | docs/dev/roadmap/v0.3-plus/master-todo.md | 241 | - [ ] T3795-15767370 **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:72) |
| T4159-5e760252 | docs/dev/roadmap/v0.3-plus/master-todo.md | 242 | - [ ] T3797-8604ab72 **[CLI-3]** Plugin Command (`it plugin run <tool>`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:74) |
| T4160-738cfb43 | docs/dev/roadmap/v0.3-plus/master-todo.md | 243 | - [ ] T3798-c399e39a **[CLI-4]** Auth Command (`it login --oidc`) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:75) |
| T4161-72e7e037 | docs/dev/roadmap/v0.3-plus/master-todo.md | 244 | - [ ] T3799-106b7d7f **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:76) |
| T4162-d98a82a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 245 | - [ ] T3800-d37df55d **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:79) |
| T4163-fca7c7a6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 246 | - [ ] T3801-933459f0 **[OBS-2]** Structured JSON Logs (X-Request-ID) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:80) |
| T4164-5194dd0f | docs/dev/roadmap/v0.3-plus/master-todo.md | 247 | - [ ] T3802-071543a2 **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:81) |
| T4165-75a6dc1f | docs/dev/roadmap/v0.3-plus/master-todo.md | 248 | - [ ] T3803-c6581fd9 **[OBS-4]** Coverage Gate fixen + CI stabilisieren (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:82) |
| T4166-63bc6f22 | docs/dev/roadmap/v0.3-plus/master-todo.md | 249 | - [ ] T3804-8b2d5322 **[OBS-5]** Frontend Build Konflikt (settings page) lösen (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:83) |
| T4167-67d70d15 | docs/dev/roadmap/v0.3-plus/master-todo.md | 250 | - [ ] T3805-7db02ef5 **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:88) |
| T4168-f322ae04 | docs/dev/roadmap/v0.3-plus/master-todo.md | 251 | - [ ] T3806-16e2dcde **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:89) |
| T4169-5cf2a35d | docs/dev/roadmap/v0.3-plus/master-todo.md | 252 | - [ ] T3807-92b03197 **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:90) |
| T4170-a99b6615 | docs/dev/roadmap/v0.3-plus/master-todo.md | 253 | - [ ] T3808-4020de87 **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:91) |
| T4171-4c55c460 | docs/dev/roadmap/v0.3-plus/master-todo.md | 254 | - [ ] T3809-d4f1efbf **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:92) |
| T4172-406e4d69 | docs/dev/roadmap/v0.3-plus/master-todo.md | 255 | - [ ] T3810-f488f7cd **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:93) |
| T4173-5aaf266f | docs/dev/roadmap/v0.3-plus/master-todo.md | 256 | - [ ] T3811-446f8627 **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:94) |
| T4174-9ff5ba76 | docs/dev/roadmap/v0.3-plus/master-todo.md | 257 | - [ ] T3812-31b9b5ab **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:95) |
| T4175-3a197d6a | docs/dev/roadmap/v0.3-plus/master-todo.md | 258 | - [ ] T3813-dbcf673a **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:96) |
| T4176-1c5f0f88 | docs/dev/roadmap/v0.3-plus/master-todo.md | 259 | - [ ] T3814-8ce46fb4 **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:97) |
| T4177-e85d5ad4 | docs/dev/roadmap/v0.3-plus/master-todo.md | 260 | - [ ] T3815-99a18dbb **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:98) |
| T4178-e91532aa | docs/dev/roadmap/v0.3-plus/master-todo.md | 261 | - [ ] T3816-a7915861 **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:99) |
| T4179-738fbadc | docs/dev/roadmap/v0.3-plus/master-todo.md | 262 | - [ ] T3817-7d18c1ee **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:100) |
| T4180-6f29fc19 | docs/dev/roadmap/v0.3-plus/master-todo.md | 263 | - [ ] T3818-d21d0237 **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:101) |
| T4181-034f036d | docs/dev/roadmap/v0.3-plus/master-todo.md | 264 | - [ ] T3819-2238d26f **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:102) |
| T4182-7d2a9762 | docs/dev/roadmap/v0.3-plus/master-todo.md | 265 | - [ ] T3820-6bc3091c **[VERIF-1]** Source Reputation & Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:105) |
| T4183-972eb0d6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 266 | - [ ] T3821-a4e8d4e8 **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:106) |
| T4184-2673bfc0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 267 | - [ ] T3822-1c331227 **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:107) |
| T4185-23e3befc | docs/dev/roadmap/v0.3-plus/master-todo.md | 268 | - [ ] T3823-a6b4b836 **[VERIF-4]** RTE/Stance Classifier + Aggregation (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:108) |
| T4186-1413cadb | docs/dev/roadmap/v0.3-plus/master-todo.md | 269 | - [ ] T3824-8b5fd368 **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:109) |
| T4187-6655c8d9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 270 | - [ ] T3825-180ba18d **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:110) |
| T4188-7bd036b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 271 | - [ ] T3826-c4b93c16 **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:111) |
| T4189-5aa3d821 | docs/dev/roadmap/v0.3-plus/master-todo.md | 272 | - [ ] T3827-77fde1ec **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:112) |
| T4190-bd4d29aa | docs/dev/roadmap/v0.3-plus/master-todo.md | 273 | - [ ] T3828-ce13cf19 **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:113) |
| T4191-f7ba3c53 | docs/dev/roadmap/v0.3-plus/master-todo.md | 274 | - [ ] T3829-69fa6b9e **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:114) |
| T4192-3a8f5735 | docs/dev/roadmap/v0.3-plus/master-todo.md | 275 | - [ ] T3830-f3ee4ebd **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:115) |
| T4193-608bdcfe | docs/dev/roadmap/v0.3-plus/master-todo.md | 276 | - [ ] T3831-14e59e2f **[LEGAL-1]** RAG-Service für Gesetzestexte (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:120) |
| T4194-ce335f52 | docs/dev/roadmap/v0.3-plus/master-todo.md | 277 | - [ ] T3832-4ead3226 **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:121) |
| T4195-6db4859e | docs/dev/roadmap/v0.3-plus/master-todo.md | 278 | - [ ] T3833-2047a757 **[LEGAL-3]** NiFi ingest_laws + rag_index (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:122) |
| T4196-229053dd | docs/dev/roadmap/v0.3-plus/master-todo.md | 279 | - [ ] T3834-6762a565 **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:123) |
| T4197-2f62eee0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 280 | - [ ] T3835-2e6ce046 **[LEGAL-5]** Frontend Tab „Legal/Compliance“ (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:124) |
| T4198-8630f4bc | docs/dev/roadmap/v0.3-plus/master-todo.md | 281 | - [ ] T3836-f1e02267 **[LEGAL-6]** Dossier-Vorlage Compliance Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:125) |
| T4199-ef121101 | docs/dev/roadmap/v0.3-plus/master-todo.md | 282 | - [ ] T3837-4708d8c6 **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:128) |
| T4200-dc432c56 | docs/dev/roadmap/v0.3-plus/master-todo.md | 283 | - [ ] T3838-31fc216d **[DISINFO-2]** Bot-Likelihood Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:129) |
| T4201-c4f3d7c3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 284 | - [ ] T3839-4f04dea7 **[DISINFO-3]** Temporal Pattern Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:130) |
| T4202-16727148 | docs/dev/roadmap/v0.3-plus/master-todo.md | 285 | - [ ] T3840-9568b165 **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:131) |
| T4203-e4e5967b | docs/dev/roadmap/v0.3-plus/master-todo.md | 286 | - [ ] T3841-b1c070e9 **[DISINFO-5]** Frontend Dashboard Top Narratives (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:132) |
| T4204-6cba8312 | docs/dev/roadmap/v0.3-plus/master-todo.md | 287 | - [ ] T3842-1dcdd73a **[DISINFO-6]** Fact-Check API Integration (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:133) |
| T4205-50b47f14 | docs/dev/roadmap/v0.3-plus/master-todo.md | 288 | - [ ] T3843-46c16667 **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:136) |
| T4206-c320ef2b | docs/dev/roadmap/v0.3-plus/master-todo.md | 289 | - [ ] T3844-a53352bf **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:137) |
| T4207-40e53568 | docs/dev/roadmap/v0.3-plus/master-todo.md | 290 | - [ ] T3845-bb7eb051 **[SUPPLY-3]** Simulation Engine (Event → Impact) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:138) |
| T4208-ce961a20 | docs/dev/roadmap/v0.3-plus/master-todo.md | 291 | - [ ] T3846-50dca75f **[SUPPLY-4]** n8n Risk Alerts + Impact Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:139) |
| T4209-5d187afa | docs/dev/roadmap/v0.3-plus/master-todo.md | 292 | - [ ] T3847-2a9c25be **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:140) |
| T4210-e9799f70 | docs/dev/roadmap/v0.3-plus/master-todo.md | 293 | - [ ] T3848-08f61ccc **[SUPPLY-6]** Dossier Supply Chain Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:141) |
| T4211-069c02b0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 294 | - [ ] T3849-1d1b7443 **[FIN-1]** Graph-Schema Accounts/Transfers (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:144) |
| T4212-8295dc46 | docs/dev/roadmap/v0.3-plus/master-todo.md | 295 | - [ ] T3850-a3cced00 **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:145) |
| T4213-0a3630e8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 296 | - [ ] T3851-fd362fb6 **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:146) |
| T4214-4c1428fe | docs/dev/roadmap/v0.3-plus/master-todo.md | 297 | - [ ] T3852-332741ce **[FIN-4]** Anomaly Detection Module (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:147) |
| T4215-01253ead | docs/dev/roadmap/v0.3-plus/master-todo.md | 298 | - [ ] T3853-20697a13 **[FIN-5]** n8n Red Flag Alerts + Escalations (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:148) |
| T4216-0c0f79f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 299 | - [ ] T3854-c62121ce **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:149) |
| T4217-e1fe26d2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 300 | - [ ] T3855-6ff24c71 **[FIN-7]** Dossier Financial Red Flags (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:150) |
| T4218-b4ee0ed8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 301 | - [ ] T3856-67f7dcdf **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:153) |
| T4219-0fa8542b | docs/dev/roadmap/v0.3-plus/master-todo.md | 302 | - [ ] T3857-bf12851c **[GEO-2]** Graph-Schema Events/Assets/Conflicts (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:154) |
| T4220-d3c643bd | docs/dev/roadmap/v0.3-plus/master-todo.md | 303 | - [ ] T3858-aea22c53 **[GEO-3]** Geo-Time Anomaly Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:155) |
| T4221-1c48ed6f | docs/dev/roadmap/v0.3-plus/master-todo.md | 304 | - [ ] T3859-1a1a1d42 **[GEO-4]** n8n Alerts + Conflict Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:156) |
| T4222-156f5267 | docs/dev/roadmap/v0.3-plus/master-todo.md | 305 | - [ ] T3860-19f9a63c **[GEO-5]** Frontend Map Dashboard + Timeline (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:157) |
| T4223-f7c0ac7c | docs/dev/roadmap/v0.3-plus/master-todo.md | 306 | - [ ] T3861-2ee21faf **[GEO-6]** Simulation Engine (Eskalations-Szenarien) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:158) |
| T4224-8fe878f1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 307 | - [ ] T3862-2f844223 **[GEO-7]** Dossier Geopolitical Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:159) |
| T4225-8ccf1a7d | docs/dev/roadmap/v0.3-plus/master-todo.md | 308 | - [ ] T3863-e37ffd8d **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:162) |
| T4226-b64f5a1d | docs/dev/roadmap/v0.3-plus/master-todo.md | 309 | - [ ] T3864-506b4526 **[HUM-2]** Graph-Schema Crisis/Indicators/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:163) |
| T4227-45bddb85 | docs/dev/roadmap/v0.3-plus/master-todo.md | 310 | - [ ] T3865-2b4c1a56 **[HUM-3]** Risk Assessment Modul (ML) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:164) |
| T4228-0c93aa95 | docs/dev/roadmap/v0.3-plus/master-todo.md | 311 | - [ ] T3866-4c5e0b5e **[HUM-4]** n8n Crisis Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:165) |
| T4229-f7dfd7d7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 312 | - [ ] T3867-592bf836 **[HUM-5]** Frontend Crisis Dashboard + Forecast (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:166) |
| T4230-0f27dbdd | docs/dev/roadmap/v0.3-plus/master-todo.md | 313 | - [ ] T3868-e6a53430 **[HUM-6]** Dossier Humanitarian Crisis Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:167) |
| T4231-4ad7af03 | docs/dev/roadmap/v0.3-plus/master-todo.md | 314 | - [ ] T3869-dae0d505 **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:172) |
| T4232-dafc35a2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 315 | - [ ] T3870-d4b84698 **[CLIMATE-2]** Graph-Schema ClimateIndicators (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:173) |
| T4233-6481c644 | docs/dev/roadmap/v0.3-plus/master-todo.md | 316 | - [ ] T3871-1637519f **[CLIMATE-3]** CO₂/Emission Scoring Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:174) |
| T4234-b4e91a08 | docs/dev/roadmap/v0.3-plus/master-todo.md | 317 | - [ ] T3872-c7e3d37c **[CLIMATE-4]** n8n Alerts (Emission Targets) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:175) |
| T4235-e486bac5 | docs/dev/roadmap/v0.3-plus/master-todo.md | 318 | - [ ] T3873-e2e1cc02 **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:176) |
| T4236-c50c53f1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 319 | - [ ] T3874-ee182a19 **[CLIMATE-6]** Dossier Climate Risk Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:177) |
| T4237-dfaf2dc0 | docs/dev/roadmap/v0.3-plus/master-todo.md | 320 | - [ ] T3875-3fb5ce0e **[TECH-1]** NiFi ingest_patents + research_data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:180) |
| T4238-7dbd35f1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 321 | - [ ] T3876-3a765387 **[TECH-2]** Graph-Schema Patents/TechTrends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:181) |
| T4239-3c725c83 | docs/dev/roadmap/v0.3-plus/master-todo.md | 322 | - [ ] T3877-79ca9f99 **[TECH-3]** Innovation Hotspot Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:182) |
| T4240-7fc5d7de | docs/dev/roadmap/v0.3-plus/master-todo.md | 323 | - [ ] T3878-e06695d0 **[TECH-4]** n8n Tech Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:183) |
| T4241-1a924d33 | docs/dev/roadmap/v0.3-plus/master-todo.md | 324 | - [ ] T3879-2bc7ebba **[TECH-5]** Frontend Patent/Innovation Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:184) |
| T4242-814772b6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 325 | - [ ] T3880-9331c680 **[TECH-6]** Dossier Technology Trends (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:185) |
| T4243-2c8b1dda | docs/dev/roadmap/v0.3-plus/master-todo.md | 326 | - [ ] T3881-1a7dbb11 **[TERROR-1]** Ingest Propaganda Sources (Social, Web) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:188) |
| T4244-1a6a5736 | docs/dev/roadmap/v0.3-plus/master-todo.md | 327 | - [ ] T3882-b3f1c1fd **[TERROR-2]** Graph-Schema TerrorNetworks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:189) |
| T4245-23e601bc | docs/dev/roadmap/v0.3-plus/master-todo.md | 328 | - [ ] T3883-27a1b4f7 **[TERROR-3]** Finance Flow Analysis (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:190) |
| T4246-6e8ca4a3 | docs/dev/roadmap/v0.3-plus/master-todo.md | 329 | - [ ] T3884-22987a00 **[TERROR-4]** n8n Alerts Suspicious Networks (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:191) |
| T4247-dc3d6bd2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 330 | - [ ] T3885-a9924200 **[TERROR-5]** Frontend Terror Network Graph (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:192) |
| T4248-30a6d813 | docs/dev/roadmap/v0.3-plus/master-todo.md | 331 | - [ ] T3886-556f4de8 **[TERROR-6]** Dossier Terrorism Threat Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:193) |
| T4249-fd7f5bfa | docs/dev/roadmap/v0.3-plus/master-todo.md | 332 | - [ ] T3887-33d49c77 **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:196) |
| T4250-4d8b7eef | docs/dev/roadmap/v0.3-plus/master-todo.md | 333 | - [ ] T3888-28b2871d **[HEALTH-2]** Graph-Schema HealthEvents/Regions (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:197) |
| T4251-26479376 | docs/dev/roadmap/v0.3-plus/master-todo.md | 334 | - [ ] T3889-285ec35b **[HEALTH-3]** Epidemic Outbreak Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:198) |
| T4252-23843329 | docs/dev/roadmap/v0.3-plus/master-todo.md | 335 | - [ ] T3890-e099d4ed **[HEALTH-4]** n8n Health Alerts + Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:199) |
| T4253-ab20fd6c | docs/dev/roadmap/v0.3-plus/master-todo.md | 336 | - [ ] T3891-7e5bd677 **[HEALTH-5]** Frontend Health Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:200) |
| T4254-10f1bdf7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 337 | - [ ] T3892-9566bac6 **[HEALTH-6]** Dossier Health/Epidemic Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:201) |
| T4255-c1f49e5f | docs/dev/roadmap/v0.3-plus/master-todo.md | 338 | - [ ] T3893-9be3e880 **[ETHICS-1]** Ingest Model Cards + AI Incident Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:204) |
| T4256-76f97cdc | docs/dev/roadmap/v0.3-plus/master-todo.md | 339 | - [ ] T3894-0224fbb9 **[ETHICS-2]** Graph-Schema Bias/Models/Orgs (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:205) |
| T4257-12d5cc7d | docs/dev/roadmap/v0.3-plus/master-todo.md | 340 | - [ ] T3895-72d2ee22 **[ETHICS-3]** Bias Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:206) |
| T4258-bff5cd6a | docs/dev/roadmap/v0.3-plus/master-todo.md | 341 | - [ ] T3896-b20776b0 **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:207) |
| T4259-072587a1 | docs/dev/roadmap/v0.3-plus/master-todo.md | 342 | - [ ] T3897-2b54964d **[ETHICS-5]** Frontend AI Ethics Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:208) |
| T4260-0fb0b0e7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 343 | - [ ] T3898-626b3a4b **[ETHICS-6]** Dossier AI Ethics Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:209) |
| T4261-0d8fbeef | docs/dev/roadmap/v0.3-plus/master-todo.md | 344 | - [ ] T3899-2501c79d **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:212) |
| T4262-e9f4c05f | docs/dev/roadmap/v0.3-plus/master-todo.md | 345 | - [ ] T3900-589c55f2 **[MEDIA-2]** Deepfake Detection Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:213) |
| T4263-edc6efbd | docs/dev/roadmap/v0.3-plus/master-todo.md | 346 | - [ ] T3901-695af690 **[MEDIA-3]** Graph-Schema MediaAuthenticity (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:214) |
| T4264-c6afba4b | docs/dev/roadmap/v0.3-plus/master-todo.md | 347 | - [ ] T3902-376abb53 **[MEDIA-4]** n8n Alerts Fake Media (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:215) |
| T4265-3fd1cde6 | docs/dev/roadmap/v0.3-plus/master-todo.md | 348 | - [ ] T3903-0a9f1830 **[MEDIA-5]** Frontend Media Forensics Panel (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:216) |
| T4266-1a104df9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 349 | - [ ] T3904-ba2ed8c8 **[MEDIA-6]** Dossier Media Authenticity Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:217) |
| T4267-4dd22b93 | docs/dev/roadmap/v0.3-plus/master-todo.md | 350 | - [ ] T3905-4d93d5ad **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:220) |
| T4268-8dfd4480 | docs/dev/roadmap/v0.3-plus/master-todo.md | 351 | - [ ] T3906-14dc9ba1 **[ECON-2]** Graph-Schema EconomicIndicators/Trades (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:221) |
| T4269-f5657280 | docs/dev/roadmap/v0.3-plus/master-todo.md | 352 | - [ ] T3907-f3ec442c **[ECON-3]** Market Risk Analysis Modul (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:222) |
| T4270-c30c3fc8 | docs/dev/roadmap/v0.3-plus/master-todo.md | 353 | - [ ] T3908-0cd07ccc **[ECON-4]** n8n Economic Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:223) |
| T4271-cea31532 | docs/dev/roadmap/v0.3-plus/master-todo.md | 354 | - [ ] T3909-0bf6341c **[ECON-5]** Frontend Economic Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:224) |
| T4272-7273a357 | docs/dev/roadmap/v0.3-plus/master-todo.md | 355 | - [ ] T3910-df2aaf71 **[ECON-6]** Dossier Economic Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:225) |
| T4273-17093d6b | docs/dev/roadmap/v0.3-plus/master-todo.md | 356 | - [ ] T3911-6a5b522a **[CULTURE-1]** Ingest Social/News/Blog Data (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:228) |
| T4274-48aa0bd7 | docs/dev/roadmap/v0.3-plus/master-todo.md | 357 | - [ ] T3912-8739e6bd **[CULTURE-2]** Graph-Schema Narratives/Discourse (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:229) |
| T4275-076f6bcc | docs/dev/roadmap/v0.3-plus/master-todo.md | 358 | - [ ] T3913-047831b1 **[CULTURE-3]** Meme/Hashtag Cluster Detection (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:230) |
| T4276-f343736a | docs/dev/roadmap/v0.3-plus/master-todo.md | 359 | - [ ] T3914-6ff50254 **[CULTURE-4]** n8n Cultural Trend Reports (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:231) |
| T4277-44d82707 | docs/dev/roadmap/v0.3-plus/master-todo.md | 360 | - [ ] T3915-227c1d1f **[CULTURE-5]** Frontend Cultural Trends Dashboard (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:232) |
| T4278-7d5f4fc9 | docs/dev/roadmap/v0.3-plus/master-todo.md | 361 | - [ ] T3916-d40aa618 **[CULTURE-6]** Dossier Cultural Intelligence Report (docs/dev/v0.2/v0.3+/Master-TODO-Index.md:233) |
| T4279-19c1378e | docs/dev/roadmap/v0.3-plus/master-todo.md | 362 | - [ ] T3917-04f85588 # 📌 Tickets (zum TODO-Index ergänzen) (docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md:103) |
| T4280-97900feb | docs/dev/roadmap/v0.3-plus/master-todo.md | 363 | - [ ] T3918-72f781f0 **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:3) |
| T4281-7bf3a4f2 | docs/dev/roadmap/v0.3-plus/master-todo.md | 364 | - [ ] T3919-5a1c6d78 **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:4) |
| T4282-8a672d6f | docs/dev/roadmap/v0.3-plus/master-todo.md | 365 | - [ ] T3920-da3e0788 **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:5) |
| T4283-791f8394 | docs/dev/roadmap/v0.3-plus/master-todo.md | 366 | - [ ] T3921-4a5c5818 **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:6) |
| T4284-2b165322 | docs/dev/roadmap/v0.3-plus/master-todo.md | 367 | - [ ] T3922-abac2b40 **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:7) |
| T4285-4754f346 | docs/dev/roadmap/v0.3-plus/master-todo.md | 368 | - [ ] T3923-b3adb79e **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:8) |
| T4286-94d66576 | docs/dev/roadmap/v0.3-plus/master-todo.md | 369 | - [ ] T3924-829b8481 **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) (docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md:9) |
| T4287-49f1ca8b | docs/dev/v0.2/Datenquellen-Cluster.md | 89 | TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! |
| T4288-c53b285c | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 170 | ## 📋 Tickets (zum TODO-Index hinzufügen) |
| T4289-640680d3 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 217 | ## TODO: |
| T4290-30cd45d8 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 220 | * `TODO-Index.md` (FLOWISE-Tickets anhängen) |
| T4291-4c66e9b1 | docs/dev/v0.2/Preset-Profile.md | 155 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
| T4292-813e30e1 | docs/dev/v0.2/Preset-Profile.md | 162 | TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. |
| T4293-7fda6ac5 | docs/dev/v0.2/TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T4294-96c614d5 | docs/dev/v0.2/TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T4295-6b53c8a4 | docs/dev/v0.2/TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T4296-daa23089 | docs/dev/v0.2/TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T4297-f9c44215 | docs/dev/v0.2/TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T4298-40201c9c | docs/dev/v0.2/TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T4299-6751fa30 | docs/dev/v0.2/TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T4300-af050ca3 | docs/dev/v0.2/TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T4301-59b8bd9a | docs/dev/v0.2/TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T4302-67ada37b | docs/dev/v0.2/TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T4303-b2f142a9 | docs/dev/v0.2/TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T4304-583511c7 | docs/dev/v0.2/TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T4305-d447eff2 | docs/dev/v0.2/TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T4306-b65ad138 | docs/dev/v0.2/TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T4307-55a9d5ec | docs/dev/v0.2/TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T4308-691f4516 | docs/dev/v0.2/TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T4309-820ca449 | docs/dev/v0.2/TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T4310-712e08d4 | docs/dev/v0.2/TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T4311-2b976b3e | docs/dev/v0.2/TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T4312-cb6348b8 | docs/dev/v0.2/TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T4313-3943b83a | docs/dev/v0.2/TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T4314-239835d3 | docs/dev/v0.2/TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T4315-1740a146 | docs/dev/v0.2/TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T4316-9abc3901 | docs/dev/v0.2/TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T4317-23ac25a1 | docs/dev/v0.2/TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T4318-c22256e6 | docs/dev/v0.2/TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T4319-937e2f61 | docs/dev/v0.2/TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T4320-bb528afa | docs/dev/v0.2/TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T4321-8977f932 | docs/dev/v0.2/TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T4322-fcc18c85 | docs/dev/v0.2/TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T4323-6700f0dc | docs/dev/v0.2/TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T4324-7bb02d96 | docs/dev/v0.2/TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T4325-aa570ddf | docs/dev/v0.2/TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T4326-2d5151d5 | docs/dev/v0.2/TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T4327-41cc3d9c | docs/dev/v0.2/TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T4328-b872722a | docs/dev/v0.2/TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T4329-d2c73ca4 | docs/dev/v0.2/TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T4330-2f805132 | docs/dev/v0.2/TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T4331-538cc227 | docs/dev/v0.2/TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T4332-4cbbedec | docs/dev/v0.2/TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T4333-a9315cdf | docs/dev/v0.2/TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation |
| T4334-f81ce959 | docs/dev/v0.2/TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T4335-a2ff9eaa | docs/dev/v0.2/TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T4336-edefb47a | docs/dev/v0.2/TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T4337-05512e8e | docs/dev/v0.2/TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T4338-27928674 | docs/dev/v0.2/TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T4339-670382ca | docs/dev/v0.2/TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T4340-83fe939a | docs/dev/v0.2/TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T4341-2296ac84 | docs/dev/v0.2/TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T4342-071175b0 | docs/dev/v0.2/TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T4343-bb757a60 | docs/dev/v0.2/TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T4344-b21c66b1 | docs/dev/v0.2/TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T4345-858d65b1 | docs/dev/v0.2/TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T4346-fa9a75ec | docs/dev/v0.2/TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T4347-e9a60584 | docs/dev/v0.2/TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T4348-12a45cbe | docs/dev/v0.2/TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T4349-6a239443 | docs/dev/v0.2/TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T4350-50dfc868 | docs/dev/v0.2/TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T4351-e4176dd4 | docs/dev/v0.2/TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T4352-76860348 | docs/dev/v0.2/TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T4353-09020bc9 | docs/dev/v0.2/TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T4354-312b93e0 | docs/dev/v0.2/TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T4355-486ef2ed | docs/dev/v0.2/TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T4356-1fb00e36 | docs/dev/v0.2/TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T4357-e046d4d0 | docs/dev/v0.2/TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T4358-16c0defd | docs/dev/v0.2/TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T4359-07d9b72a | docs/dev/v0.2/TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T4360-120d3b48 | docs/dev/v0.2/TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T4361-37a44314 | docs/dev/v0.2/TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T4362-f6f0ac08 | docs/dev/v0.2/TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T4363-f47ef523 | docs/dev/v0.2/TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T4364-1e77dce9 | docs/dev/v0.2/TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T4365-7fb20f8d | docs/dev/v0.2/TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T4366-1c9c78b6 | docs/dev/v0.2/TODO-Index.md | 107 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T4367-2fc57e38 | docs/dev/v0.2/TODO-Index.md | 108 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T4368-5950a90f | docs/dev/v0.2/TODO-Index.md | 109 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T4369-1e613ad0 | docs/dev/v0.2/TODO-Index.md | 110 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T4370-3e09c258 | docs/dev/v0.2/TODO-Index.md | 111 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T4371-df0fea1d | docs/dev/v0.2/TODO-Index.md | 112 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T4372-f0796a6f | docs/dev/v0.2/TODO-Index.md | 113 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T4373-5ad28f17 | docs/dev/v0.2/TODO-Index.md | 114 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T4374-0c056d58 | docs/dev/v0.2/TODO-Index.md | 115 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T4375-6a135243 | docs/dev/v0.2/TODO-Index.md | 116 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T4376-2a9efbbd | docs/dev/v0.2/TODO-Index.md | 117 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T4377-c3e76b03 | docs/dev/v0.2/Ticket-Checkliste.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T4378-3c74f562 | docs/dev/v0.2/Ticket-Checkliste.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T4379-86384cee | docs/dev/v0.2/Ticket-Checkliste.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T4380-f1ebad68 | docs/dev/v0.2/Ticket-Checkliste.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T4381-ef38943a | docs/dev/v0.2/Ticket-Checkliste.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T4382-2c4e0e55 | docs/dev/v0.2/Ticket-Checkliste.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T4383-260ec1ba | docs/dev/v0.2/Ticket-Checkliste.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T4384-cf392a31 | docs/dev/v0.2/Ticket-Checkliste.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T4385-c2929de2 | docs/dev/v0.2/Ticket-Checkliste.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T4386-99a53243 | docs/dev/v0.2/Ticket-Checkliste.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T4387-bd7b9b38 | docs/dev/v0.2/Ticket-Checkliste.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T4388-fd8d5463 | docs/dev/v0.2/Ticket-Checkliste.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T4389-fe9c9b01 | docs/dev/v0.2/Ticket-Checkliste.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T4390-fb88ffb0 | docs/dev/v0.2/Ticket-Checkliste.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T4391-930adfd5 | docs/dev/v0.2/Ticket-Checkliste.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T4392-4371a444 | docs/dev/v0.2/Ticket-Checkliste.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T4393-a1249e1c | docs/dev/v0.2/Ticket-Checkliste.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T4394-8031896a | docs/dev/v0.2/Ticket-Checkliste.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T4395-4e3ab17e | docs/dev/v0.2/Ticket-Checkliste.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T4396-2ecc8c30 | docs/dev/v0.2/Ticket-Checkliste.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T4397-2e7ef320 | docs/dev/v0.2/Ticket-Checkliste.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T4398-f5ef504e | docs/dev/v0.2/Ticket-Checkliste.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T4399-8249b090 | docs/dev/v0.2/Ticket-Checkliste.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T4400-53434e25 | docs/dev/v0.2/Ticket-Checkliste.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T4401-f4718a0d | docs/dev/v0.2/Ticket-Checkliste.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T4402-2e62061b | docs/dev/v0.2/Ticket-Checkliste.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T4403-7965089b | docs/dev/v0.2/Ticket-Checkliste.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T4404-361b2744 | docs/dev/v0.2/Ticket-Checkliste.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T4405-57338d8b | docs/dev/v0.2/Ticket-Checkliste.md | 46 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T4406-3f9b35c6 | docs/dev/v0.2/Ticket-Checkliste.md | 47 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T4407-b3a4b50c | docs/dev/v0.2/Ticket-Checkliste.md | 48 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T4408-3d064402 | docs/dev/v0.2/Ticket-Checkliste.md | 49 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T4409-9f55a7e3 | docs/dev/v0.2/Ticket-Checkliste.md | 52 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T4410-57541fe4 | docs/dev/v0.2/Ticket-Checkliste.md | 53 | - [ ] **[NIFI-2]** API Ingest Flow |
| T4411-5b962c45 | docs/dev/v0.2/Ticket-Checkliste.md | 54 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T4412-33e5f56d | docs/dev/v0.2/Ticket-Checkliste.md | 55 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T4413-a3e06510 | docs/dev/v0.2/Ticket-Checkliste.md | 56 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T4414-61eaba80 | docs/dev/v0.2/Ticket-Checkliste.md | 57 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T4415-916bb7e9 | docs/dev/v0.2/Ticket-Checkliste.md | 60 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T4416-49602af1 | docs/dev/v0.2/Ticket-Checkliste.md | 61 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T4417-8ca4f49d | docs/dev/v0.2/Ticket-Checkliste.md | 62 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T4418-7ca5c4fb | docs/dev/v0.2/Ticket-Checkliste.md | 63 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T4419-03560a6d | docs/dev/v0.2/Ticket-Checkliste.md | 64 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T4420-212d7d93 | docs/dev/v0.2/Ticket-Checkliste.md | 67 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T4421-31f1363d | docs/dev/v0.2/Ticket-Checkliste.md | 68 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T4422-46578c8e | docs/dev/v0.2/Ticket-Checkliste.md | 69 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T4423-cddb81e2 | docs/dev/v0.2/Ticket-Checkliste.md | 70 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T4424-f7bd1421 | docs/dev/v0.2/Ticket-Checkliste.md | 71 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T4425-5a2d6148 | docs/dev/v0.2/Ticket-Checkliste.md | 74 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T4426-d15bbcb1 | docs/dev/v0.2/Ticket-Checkliste.md | 75 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T4427-08448e85 | docs/dev/v0.2/Ticket-Checkliste.md | 76 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T4428-d2236406 | docs/dev/v0.2/Ticket-Checkliste.md | 77 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T4429-9bd657cd | docs/dev/v0.2/Ticket-Checkliste.md | 78 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T4430-9b019ff4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) |
| T4431-98e90d90 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T4432-65a07da1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T4433-bf0ac642 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T4434-c7b2ea55 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T4435-a895be4c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T4436-80a2e913 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T4437-2c6aa5b0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T4438-1030e0fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T4439-3c059eea | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T4440-7e80880f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T4441-d25582d3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T4442-041e81a9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T4443-fd930023 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T4444-3c21423e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T4445-41fef9d2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T4446-9e560efe | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T4447-37219dc9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T4448-66bd4524 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T4449-6e54ac16 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T4450-c05d7b58 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T4451-09986fb5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T4452-7ca3edc4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T4453-bfd46364 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T4454-6ecc94ac | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T4455-7ca78b51 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T4456-1b1da82d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T4457-e05ddd88 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T4458-2ffc74f0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T4459-45fd5c7b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T4460-0b8d92a4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T4461-a0c3bfe4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T4462-3f86dd6a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T4463-6b86dd7e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T4464-1d7717fb | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T4465-0c39b3a6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T4466-2ef30966 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T4467-fc5ed44a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T4468-51d406f2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T4469-153dda62 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T4470-ddc6f2da | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) |
| T4471-ac36672e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T4472-a9312730 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T4473-372c0169 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T4474-fd4e6beb | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T4475-8215cd0e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T4476-7ca16b98 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T4477-1981f93b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T4478-15767370 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T4479-68c472d8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\\|search\\|dossier]`) |
| T4480-8604ab72 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T4481-c399e39a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T4482-106b7d7f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T4483-d37df55d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T4484-933459f0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T4485-071543a2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T4486-c6581fd9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T4487-8b2d5322 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T4488-7db02ef5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T4489-16e2dcde | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T4490-92b03197 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T4491-4020de87 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T4492-d4f1efbf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T4493-f488f7cd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T4494-446f8627 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T4495-31b9b5ab | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T4496-dbcf673a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T4497-8ce46fb4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T4498-99a18dbb | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T4499-a7915861 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T4500-7d18c1ee | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T4501-d21d0237 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T4502-2238d26f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T4503-6bc3091c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 105 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T4504-a4e8d4e8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 106 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T4505-1c331227 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 107 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T4506-a6b4b836 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 108 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T4507-8b5fd368 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 109 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T4508-180ba18d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 110 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T4509-c4b93c16 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 111 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T4510-77fde1ec | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 112 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T4511-ce13cf19 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 113 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T4512-69fa6b9e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 114 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T4513-f3ee4ebd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 115 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T4514-14e59e2f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 120 | - [ ] **[LEGAL-1]** RAG-Service für Gesetzestexte |
| T4515-4ead3226 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 121 | - [ ] **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) |
| T4516-2047a757 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 122 | - [ ] **[LEGAL-3]** NiFi ingest_laws + rag_index |
| T4517-6762a565 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 123 | - [ ] **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports |
| T4518-2e6ce046 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 124 | - [ ] **[LEGAL-5]** Frontend Tab „Legal/Compliance“ |
| T4519-f1e02267 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 125 | - [ ] **[LEGAL-6]** Dossier-Vorlage Compliance Report |
| T4520-4708d8c6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 128 | - [ ] **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) |
| T4521-31fc216d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 129 | - [ ] **[DISINFO-2]** Bot-Likelihood Modul |
| T4522-4f04dea7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 130 | - [ ] **[DISINFO-3]** Temporal Pattern Detection |
| T4523-9568b165 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 131 | - [ ] **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier |
| T4524-b1c070e9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 132 | - [ ] **[DISINFO-5]** Frontend Dashboard Top Narratives |
| T4525-1dcdd73a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 133 | - [ ] **[DISINFO-6]** Fact-Check API Integration |
| T4526-46c16667 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 136 | - [ ] **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions |
| T4527-a53352bf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 137 | - [ ] **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions |
| T4528-bb7eb051 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 138 | - [ ] **[SUPPLY-3]** Simulation Engine (Event → Impact) |
| T4529-50dca75f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 139 | - [ ] **[SUPPLY-4]** n8n Risk Alerts + Impact Reports |
| T4530-2a9c25be | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 140 | - [ ] **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool |
| T4531-08f61ccc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 141 | - [ ] **[SUPPLY-6]** Dossier Supply Chain Risk Report |
| T4532-1d1b7443 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 144 | - [ ] **[FIN-1]** Graph-Schema Accounts/Transfers |
| T4533-a3cced00 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 145 | - [ ] **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions |
| T4534-fd362fb6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 146 | - [ ] **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) |
| T4535-332741ce | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 147 | - [ ] **[FIN-4]** Anomaly Detection Module |
| T4536-20697a13 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 148 | - [ ] **[FIN-5]** n8n Red Flag Alerts + Escalations |
| T4537-c62121ce | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 149 | - [ ] **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard |
| T4538-6ff24c71 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 150 | - [ ] **[FIN-7]** Dossier Financial Red Flags |
| T4539-67f7dcdf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 153 | - [ ] **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social |
| T4540-bf12851c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 154 | - [ ] **[GEO-2]** Graph-Schema Events/Assets/Conflicts |
| T4541-aea22c53 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 155 | - [ ] **[GEO-3]** Geo-Time Anomaly Detection |
| T4542-1a1a1d42 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 156 | - [ ] **[GEO-4]** n8n Alerts + Conflict Reports |
| T4543-19f9a63c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 157 | - [ ] **[GEO-5]** Frontend Map Dashboard + Timeline |
| T4544-2ee21faf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 158 | - [ ] **[GEO-6]** Simulation Engine (Eskalations-Szenarien) |
| T4545-2f844223 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 159 | - [ ] **[GEO-7]** Dossier Geopolitical Report |
| T4546-e37ffd8d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 162 | - [ ] **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators |
| T4547-506b4526 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 163 | - [ ] **[HUM-2]** Graph-Schema Crisis/Indicators/Regions |
| T4548-2b4c1a56 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 164 | - [ ] **[HUM-3]** Risk Assessment Modul (ML) |
| T4549-4c5e0b5e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 165 | - [ ] **[HUM-4]** n8n Crisis Alerts + Reports |
| T4550-592bf836 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 166 | - [ ] **[HUM-5]** Frontend Crisis Dashboard + Forecast |
| T4551-e6a53430 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 167 | - [ ] **[HUM-6]** Dossier Humanitarian Crisis Report |
| T4552-dae0d505 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 172 | - [ ] **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) |
| T4553-d4b84698 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 173 | - [ ] **[CLIMATE-2]** Graph-Schema ClimateIndicators |
| T4554-1637519f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 174 | - [ ] **[CLIMATE-3]** CO₂/Emission Scoring Modul |
| T4555-c7e3d37c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 175 | - [ ] **[CLIMATE-4]** n8n Alerts (Emission Targets) |
| T4556-e2e1cc02 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 176 | - [ ] **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap |
| T4557-ee182a19 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 177 | - [ ] **[CLIMATE-6]** Dossier Climate Risk Report |
| T4558-3fb5ce0e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 180 | - [ ] **[TECH-1]** NiFi ingest_patents + research_data |
| T4559-3a765387 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 181 | - [ ] **[TECH-2]** Graph-Schema Patents/TechTrends |
| T4560-79ca9f99 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 182 | - [ ] **[TECH-3]** Innovation Hotspot Detection |
| T4561-e06695d0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 183 | - [ ] **[TECH-4]** n8n Tech Trend Reports |
| T4562-2bc7ebba | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 184 | - [ ] **[TECH-5]** Frontend Patent/Innovation Graph |
| T4563-9331c680 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 185 | - [ ] **[TECH-6]** Dossier Technology Trends |
| T4564-1a7dbb11 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 188 | - [ ] **[TERROR-1]** Ingest Propaganda Sources (Social, Web) |
| T4565-b3f1c1fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 189 | - [ ] **[TERROR-2]** Graph-Schema TerrorNetworks |
| T4566-27a1b4f7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 190 | - [ ] **[TERROR-3]** Finance Flow Analysis |
| T4567-22987a00 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 191 | - [ ] **[TERROR-4]** n8n Alerts Suspicious Networks |
| T4568-a9924200 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 192 | - [ ] **[TERROR-5]** Frontend Terror Network Graph |
| T4569-556f4de8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 193 | - [ ] **[TERROR-6]** Dossier Terrorism Threat Report |
| T4570-33d49c77 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 196 | - [ ] **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) |
| T4571-28b2871d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 197 | - [ ] **[HEALTH-2]** Graph-Schema HealthEvents/Regions |
| T4572-285ec35b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 198 | - [ ] **[HEALTH-3]** Epidemic Outbreak Detection |
| T4573-e099d4ed | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 199 | - [ ] **[HEALTH-4]** n8n Health Alerts + Reports |
| T4574-7e5bd677 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 200 | - [ ] **[HEALTH-5]** Frontend Health Dashboard |
| T4575-9566bac6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 201 | - [ ] **[HEALTH-6]** Dossier Health/Epidemic Report |
| T4576-9be3e880 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 204 | - [ ] **[ETHICS-1]** Ingest Model Cards + AI Incident Data |
| T4577-0224fbb9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 205 | - [ ] **[ETHICS-2]** Graph-Schema Bias/Models/Orgs |
| T4578-72d2ee22 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 206 | - [ ] **[ETHICS-3]** Bias Detection Modul |
| T4579-b20776b0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 207 | - [ ] **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) |
| T4580-2b54964d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 208 | - [ ] **[ETHICS-5]** Frontend AI Ethics Dashboard |
| T4581-626b3a4b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 209 | - [ ] **[ETHICS-6]** Dossier AI Ethics Report |
| T4582-2501c79d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 212 | - [ ] **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) |
| T4583-589c55f2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 213 | - [ ] **[MEDIA-2]** Deepfake Detection Modul |
| T4584-695af690 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 214 | - [ ] **[MEDIA-3]** Graph-Schema MediaAuthenticity |
| T4585-376abb53 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 215 | - [ ] **[MEDIA-4]** n8n Alerts Fake Media |
| T4586-0a9f1830 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 216 | - [ ] **[MEDIA-5]** Frontend Media Forensics Panel |
| T4587-ba2ed8c8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 217 | - [ ] **[MEDIA-6]** Dossier Media Authenticity Report |
| T4588-4d93d5ad | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 220 | - [ ] **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) |
| T4589-14dc9ba1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 221 | - [ ] **[ECON-2]** Graph-Schema EconomicIndicators/Trades |
| T4590-f3ec442c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 222 | - [ ] **[ECON-3]** Market Risk Analysis Modul |
| T4591-0cd07ccc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 223 | - [ ] **[ECON-4]** n8n Economic Reports |
| T4592-0bf6341c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 224 | - [ ] **[ECON-5]** Frontend Economic Dashboard |
| T4593-df2aaf71 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 225 | - [ ] **[ECON-6]** Dossier Economic Intelligence Report |
| T4594-6a5b522a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 228 | - [ ] **[CULTURE-1]** Ingest Social/News/Blog Data |
| T4595-8739e6bd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 229 | - [ ] **[CULTURE-2]** Graph-Schema Narratives/Discourse |
| T4596-047831b1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 230 | - [ ] **[CULTURE-3]** Meme/Hashtag Cluster Detection |
| T4597-6ff50254 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 231 | - [ ] **[CULTURE-4]** n8n Cultural Trend Reports |
| T4598-227c1d1f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 232 | - [ ] **[CULTURE-5]** Frontend Cultural Trends Dashboard |
| T4599-d40aa618 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 233 | - [ ] **[CULTURE-6]** Dossier Cultural Intelligence Report |
| T4600-04f85588 | docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md | 103 | # 📌 Tickets (zum TODO-Index ergänzen) |
| T4601-72f781f0 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 3 | - [ ] **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) |
| T4602-5a1c6d78 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 4 | - [ ] **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden |
| T4603-da3e0788 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 5 | - [ ] **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen |
| T4604-4a5c5818 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 6 | - [ ] **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix |
| T4605-abac2b40 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 7 | - [ ] **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos |
| T4606-b3adb79e | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 8 | - [ ] **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle |
| T4607-829b8481 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 9 | - [ ] **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) |
| T4608-e320e5f8 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG-2.md | 27 | - [ ] T0123-abcd1234 Implement NER API in `services/nlp` (docs/dev/roadmap/v0.2-to-build.md:14) |
| T4609-8db7577c | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG-2.md | 89 | * `docs: integrate TODO index into roadmap files (idempotent)` |
| T4610-65885270 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 73 | * `WORK-ON-new_docs/out/todo_index.md` (alle Checkboxen `- [ ]`/`- [x]`/nummerierte, plus `TODO:`/`FIXME:`/`NOTE:`; **mit IDs T####-hash, Datei, Zeile, Text**) |
| T4611-e28e7e42 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 256 | * **Alle** TODOs (Checkboxen + TODO/FIXME/NOTE) in `todo_index.md` mit **IDs + Quelle+Zeile**. |
| T4612-b668572d | docs/dev/guides/frontend-modernization-setup-guide.md | 150 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T4613-17fd826e | docs/dev/guides/frontend-modernization-setup-guide.md | 151 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T4614-2e5432e9 | docs/dev/guides/frontend-modernization-setup-guide.md | 152 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T4615-14f16534 | docs/dev/guides/frontend-modernization-setup-guide.md | 153 | - [ ] **Search Functionality** - Faceted Search + Results |
| T4616-979ccb63 | docs/dev/guides/frontend-modernization-setup-guide.md | 154 | - [ ] **Form Validation** - Error States + Success |
| T4617-6ce52c31 | docs/dev/guides/frontend-modernization-setup-guide.md | 155 | - [ ] **Real-time Updates** - WebSocket Connection |
| T4618-e7127849 | docs/dev/guides/frontend-modernization-setup-guide.md | 168 | - [ ] **Bundle Size** < 500KB gzipped |
| T4619-19f6b15e | docs/dev/guides/frontend-modernization-setup-guide.md | 169 | - [ ] **First Contentful Paint** < 1.8s |
| T4620-9bee0b15 | docs/dev/guides/frontend-modernization-setup-guide.md | 170 | - [ ] **Largest Contentful Paint** < 2.5s |
| T4621-fe80e46c | docs/dev/guides/frontend-modernization-setup-guide.md | 171 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T4622-34ea233c | docs/dev/guides/frontend-modernization-setup-guide.md | 214 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T4623-b1e49fce | docs/dev/guides/frontend-modernization-setup-guide.md | 215 | - [ ] **User Acceptance Testing** abgeschlossen |
| T4624-a0ceea27 | docs/dev/guides/frontend-modernization-setup-guide.md | 216 | - [ ] **Documentation aktualisiert** |
| T4625-f5827cb9 | docs/dev/guides/frontend-modernization-setup-guide.md | 217 | - [ ] **Deployment Pipeline getestet** |
| T4626-326f4150 | docs/dev/guides/frontend-modernization-setup-guide.md | 218 | - [ ] **Monitoring Setup** aktiv |
| T4627-a439ad8b | docs/dev/guides/frontend-modernization-setup-guide.md | 219 | - [ ] **Rollback Plan** definiert |
| T4628-077a9deb | docs/dev/guides/frontend-modernization.md | 293 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T4629-efe0ce23 | docs/dev/guides/frontend-modernization.md | 294 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T4630-062cf84e | docs/dev/guides/frontend-modernization.md | 295 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T4631-6d5fbd33 | docs/dev/guides/frontend-modernization.md | 296 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T4632-7013d1ed | docs/dev/guides/frontend-modernization.md | 297 | - [ ] **Search Functionality** - Faceted Search + Results |
| T4633-d006d53b | docs/dev/guides/frontend-modernization.md | 298 | - [ ] **Form Validation** - Error States + Success |
| T4634-4533677e | docs/dev/guides/frontend-modernization.md | 299 | - [ ] **Real-time Updates** - WebSocket Connection |
| T4635-fc4b4f27 | docs/dev/guides/frontend-modernization.md | 300 | - [ ] **Notifications** - Toast Messages |
| T4636-799ee059 | docs/dev/guides/frontend-modernization.md | 301 | - [ ] **Charts** - Interactive Visualizations |
| T4637-2225a132 | docs/dev/guides/frontend-modernization.md | 302 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T4638-56b49316 | docs/dev/guides/frontend-modernization.md | 303 | - [ ] **Authentication** - Login/Logout Flow |
| T4639-8bcb6cdb | docs/dev/guides/frontend-modernization.md | 327 | - [ ] **Bundle Size** < 500KB gzipped |
| T4640-78a4720b | docs/dev/guides/frontend-modernization.md | 328 | - [ ] **First Contentful Paint** < 1.8s |
| T4641-5b5be07c | docs/dev/guides/frontend-modernization.md | 329 | - [ ] **Largest Contentful Paint** < 2.5s |
| T4642-aa016152 | docs/dev/guides/frontend-modernization.md | 330 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T4643-dddb196b | docs/dev/guides/frontend-modernization.md | 331 | - [ ] **First Input Delay** < 100ms |
| T4644-5ceae1bf | docs/dev/guides/frontend-modernization.md | 461 | - [ ] **Alle Tests bestanden** |
| T4645-ddcddc42 | docs/dev/guides/frontend-modernization.md | 462 | - [ ] **Performance Benchmarks erreicht** |
| T4646-9ff666f6 | docs/dev/guides/frontend-modernization.md | 463 | - [ ] **Mobile Testing abgeschlossen** |
| T4647-98f37747 | docs/dev/guides/frontend-modernization.md | 464 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T4648-7f72bc57 | docs/dev/guides/frontend-modernization.md | 465 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T4649-019ffbda | docs/dev/guides/frontend-modernization.md | 466 | - [ ] **User Acceptance Testing** abgeschlossen |
| T4650-62f04e67 | docs/dev/guides/frontend-modernization.md | 467 | - [ ] **Documentation aktualisiert** |
| T4651-34a380d6 | docs/dev/guides/frontend-modernization.md | 468 | - [ ] **Deployment Pipeline getestet** |
| T4652-591eb056 | docs/dev/guides/frontend-modernization.md | 469 | - [ ] **Monitoring Setup** aktiv |
| T4653-4872d65e | docs/dev/guides/frontend-modernization.md | 470 | - [ ] **Rollback Plan** definiert |
| T4654-f3bf1785 | docs/dev/guides/frontend-modernization.md | 925 | - [ ] **Alle Tests bestanden** |
| T4655-fe1b1ed3 | docs/dev/guides/frontend-modernization.md | 926 | - [ ] **Performance Benchmarks erreicht** |
| T4656-8395733e | docs/dev/guides/frontend-modernization.md | 927 | - [ ] **Mobile Testing abgeschlossen** |
| T4657-a92e84b3 | docs/dev/guides/frontend-modernization.md | 928 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T4658-156d6269 | docs/dev/guides/frontend-modernization.md | 1017 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T4659-c3a14895 | docs/dev/guides/frontend-modernization.md | 1024 | - [ ] **Notifications** - Toast Messages |
| T4660-1e2428e2 | docs/dev/guides/frontend-modernization.md | 1025 | - [ ] **Charts** - Interactive Visualizations |
| T4661-63cae15e | docs/dev/guides/frontend-modernization.md | 1026 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T4662-14f85e51 | docs/dev/guides/frontend-modernization.md | 1027 | - [ ] **Authentication** - Login/Logout Flow |
| T4663-0c484ef7 | docs/dev/guides/frontend-modernization.md | 1046 | - [ ] **First Input Delay** < 100ms |
| T4664-7aa40bc3 | docs/presets/Presets(Profile).md | 177 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
| T4665-d5d2c97b | docs/waveterm/README.md | 388 | ### **TODO-Index – Ergänzung** |
| T4666-47044964 | docs/waveterm/README.md | 390 | > Hänge an `docs/TODO-Index.md` an: |
| T4667-5f70b37c | docs/waveterm/README.md | 394 | - [ ] **[WT-EMBED-1]** Webview Tab `/terminal` + SSO (OIDC) |
| T4668-97595967 | docs/waveterm/README.md | 395 | - [ ] **[WT-EMBED-2]** Profiles Loader (journalism/compliance/crisis/…) |
| T4669-929c8a6b | docs/waveterm/README.md | 396 | - [ ] **[WT-EMBED-3]** “Send to WaveTerm” Actions (+context payload) |
| T4670-b9f3e5a3 | docs/waveterm/README.md | 397 | - [ ] **[WT-EMBED-4]** Session Recording → Dossier Appendix |
| T4671-67309ce5 | docs/waveterm/README.md | 398 | - [ ] **[WT-PLUGIN-1]** WaveTerm Plugin Manifest (`it` commands, panels) |
| T4672-4a48ca51 | docs/waveterm/README.md | 399 | - [ ] **[WT-PLUGIN-2]** Dossier/Graph Previews (MD/SVG) |
| T4673-e18e3065 | docs/waveterm/README.md | 400 | - [ ] **[WT-PLUGIN-3]** Command Palettes & Snippets |
| T4674-6f2a48f3 | docs/waveterm/README.md | 401 | - [ ] **[WT-JOBS-1]** `/api/jobs` (queue, artifacts) |
| T4675-37580cf6 | docs/waveterm/README.md | 402 | - [ ] **[WT-JOBS-2]** n8n Node `waveterm.run` |
| T4676-62463ab4 | docs/waveterm/README.md | 403 | - [ ] **[WT-JOBS-3]** NiFi Processor `WaveTermInvoker` |
| T4677-179ca16b | docs/waveterm/README.md | 404 | - [ ] **[WT-SEC-1]** gVisor/Kata runtime + default no-net |
| T4678-b2c802d2 | docs/waveterm/README.md | 405 | - [ ] **[WT-SEC-2]** OPA policies (tool allowlist, export gates) |
| T4679-f4c50303 | docs/waveterm/README.md | 406 | - [ ] **[WT-SEC-3]** Vault tokens (short-lived) for CLI/API |
| T4680-bbf5f486 | docs/waveterm/README.md | 407 | - [ ] **[WT-DOC-1]** `docs/waveterm/README.md` (Setup, Profiles, Safety) |
| T4681-b6f6d90d | docs/waveterm/README.md | 408 | - [ ] **[WT-DOC-2]** `docs/waveterm/presets/*.yaml` Beispiele |
| T4682-34306263 | docs/waveterm/README.md | 409 | - [ ] **[WT-DOC-3]** `docs/api/jobs.md` Spezifikation |
