| ID | File | Line | Text |
|---|---|---|---|
| T0001-123e | docs/SECURITY_SWEEP.md | 3 | - TODO: Secrets rotieren (Keycloak admin, oauth2-proxy cookie, DB-Passwörter). |
| T0002-9f6d | docs/SECURITY_SWEEP.md | 4 | - TODO: TLS/Ingress für Prod (Cert-Manager). |
| T0003-95be | docs/SECURITY_SWEEP.md | 5 | - TODO: Backups für PG/OpenSearch/Neo4j. |
| T0004-0877 | docs/TODO-Index.md | 1 | # TODO-Index |
| T0005-eebd | docs/release-checklist-v0.1.md | 10 | - [ ] Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs). |
| T0006-6c05 | docs/release-checklist-v0.1.md | 11 | - [ ] **Conftest/OPA Policies** laufen sauber (`make ci-policy`). |
| T0007-7b3c | docs/release-checklist-v0.1.md | 12 | - [ ] **Secrets entfernt** aus Manifests/Code (`grep -R "password" infra/ services/ \| grep -v example` → leer). |
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
| T0089-65cf | docs/export/AFFINE.md | 189 | ### **TODO-Index – Ergänzungen** |
| T0090-23b5 | docs/export/AFFINE.md | 191 | > Hänge diesen Block an `docs/TODO-Index.md` an. |
| T0091-d4c0 | docs/export/AFFINE.md | 195 | - [ ] **[EXPORT-1]** Bundle-Builder (md + assets + meta/export.json) |
| T0092-1551 | docs/export/AFFINE.md | 196 | - [ ] **[EXPORT-2]** Graph-Exporter (mermaid.mmd, dot, svg) |
| T0093-66f7 | docs/export/AFFINE.md | 197 | - [ ] **[EXPORT-3]** Canvas-Exporter (excalidraw.json) |
| T0094-35bc | docs/export/AFFINE.md | 198 | - [ ] **[EXPORT-4]** Geo-Exporter (geojson + map.png/svg) |
| T0095-f628 | docs/export/AFFINE.md | 199 | - [ ] **[APPFLOWY-1]** AppFlowy Adapter – Watched Folder |
| T0096-dafa | docs/export/AFFINE.md | 200 | - [ ] **[APPFLOWY-2]** AppFlowy Adapter – API Mode (optional) |
| T0097-52af | docs/export/AFFINE.md | 201 | - [ ] **[AFFINE-1]** AFFiNE Adapter – Watched Folder + Edgeless Import |
| T0098-33b2 | docs/export/AFFINE.md | 202 | - [ ] **[AFFINE-2]** AFFiNE Adapter – API Mode (optional) |
| T0099-5e0d | docs/export/AFFINE.md | 203 | - [ ] **[FE-EXPORT-1]** Frontend Export-Dialog (Targets + Formate) |
| T0100-bb2c | docs/export/AFFINE.md | 204 | - [ ] **[CLI-EXP-1]** CLI `it export dossier/graph/canvas` |
| T0101-678e | docs/export/AFFINE.md | 205 | - [ ] **[N8N-EXP-1]** n8n Nodes `export_to_appflowy` / `export_to_affine` |
| T0102-414d | docs/export/AFFINE.md | 206 | - [ ] **[POLICY-EXP-1]** OPA-Regeln (classification gates) |
| T0103-6936 | docs/export/AFFINE.md | 207 | - [ ] **[VAULT-EXP-1]** Secrets Handling für Adapter-APIs |
| T0104-f262 | docs/export/AFFINE.md | 208 | - [ ] **[QA-EXP-1]** Golden Bundle Tests |
| T0105-63db | docs/export/AFFINE.md | 209 | - [ ] **[QA-EXP-2]** Roundtrip Import Tests |
| T0106-9923 | docs/dev/Checkliste.md | 10 | Weitere Details siehe `TODO-Index.md`. |
| T0107-3313 | docs/dev/Frontend-Modernisierung.md | 288 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T0108-e928 | docs/dev/Frontend-Modernisierung.md | 289 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T0109-8ef8 | docs/dev/Frontend-Modernisierung.md | 290 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T0110-2374 | docs/dev/Frontend-Modernisierung.md | 291 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T0111-2c90 | docs/dev/Frontend-Modernisierung.md | 292 | - [ ] **Search Functionality** - Faceted Search + Results |
| T0112-2ba5 | docs/dev/Frontend-Modernisierung.md | 293 | - [ ] **Form Validation** - Error States + Success |
| T0113-0a72 | docs/dev/Frontend-Modernisierung.md | 294 | - [ ] **Real-time Updates** - WebSocket Connection |
| T0114-6e99 | docs/dev/Frontend-Modernisierung.md | 295 | - [ ] **Notifications** - Toast Messages |
| T0115-2956 | docs/dev/Frontend-Modernisierung.md | 296 | - [ ] **Charts** - Interactive Visualizations |
| T0116-5dc8 | docs/dev/Frontend-Modernisierung.md | 297 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T0117-e8f6 | docs/dev/Frontend-Modernisierung.md | 298 | - [ ] **Authentication** - Login/Logout Flow |
| T0118-adfc | docs/dev/Frontend-Modernisierung.md | 322 | - [ ] **Bundle Size** < 500KB gzipped |
| T0119-42cc | docs/dev/Frontend-Modernisierung.md | 323 | - [ ] **First Contentful Paint** < 1.8s |
| T0120-8d45 | docs/dev/Frontend-Modernisierung.md | 324 | - [ ] **Largest Contentful Paint** < 2.5s |
| T0121-a457 | docs/dev/Frontend-Modernisierung.md | 325 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T0122-1d5d | docs/dev/Frontend-Modernisierung.md | 326 | - [ ] **First Input Delay** < 100ms |
| T0123-96da | docs/dev/Frontend-Modernisierung.md | 456 | - [ ] **Alle Tests bestanden** |
| T0124-335f | docs/dev/Frontend-Modernisierung.md | 457 | - [ ] **Performance Benchmarks erreicht** |
| T0125-a0ad | docs/dev/Frontend-Modernisierung.md | 458 | - [ ] **Mobile Testing abgeschlossen** |
| T0126-f52c | docs/dev/Frontend-Modernisierung.md | 459 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T0127-1e6e | docs/dev/Frontend-Modernisierung.md | 460 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T0128-e08b | docs/dev/Frontend-Modernisierung.md | 461 | - [ ] **User Acceptance Testing** abgeschlossen |
| T0129-6dd5 | docs/dev/Frontend-Modernisierung.md | 462 | - [ ] **Documentation aktualisiert** |
| T0130-316c | docs/dev/Frontend-Modernisierung.md | 463 | - [ ] **Deployment Pipeline getestet** |
| T0131-1b8f | docs/dev/Frontend-Modernisierung.md | 464 | - [ ] **Monitoring Setup** aktiv |
| T0132-3f17 | docs/dev/Frontend-Modernisierung.md | 465 | - [ ] **Rollback Plan** definiert |
| T0133-d4ce | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 277 | - [ ] **Desktop Navigation** - Sidebar funktioniert |
| T0134-aa90 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 278 | - [ ] **Mobile Navigation** - Hamburger Menu + Bottom Tabs |
| T0135-04b4 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 279 | - [ ] **Dark/Light Mode** - Toggle funktioniert |
| T0136-e4ea | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 280 | - [ ] **Command Palette** - Cmd+K öffnet Palette |
| T0137-539a | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 281 | - [ ] **Search Functionality** - Faceted Search + Results |
| T0138-21a9 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 282 | - [ ] **Form Validation** - Error States + Success |
| T0139-f9f1 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 283 | - [ ] **Real-time Updates** - WebSocket Connection |
| T0140-f1b4 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 284 | - [ ] **Notifications** - Toast Messages |
| T0141-2c63 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 285 | - [ ] **Charts** - Interactive Visualizations |
| T0142-0fcc | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 286 | - [ ] **Data Tables** - Sorting + Filtering + Pagination |
| T0143-f77b | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 287 | - [ ] **Authentication** - Login/Logout Flow |
| T0144-c1e0 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 311 | - [ ] **Bundle Size** < 500KB gzipped |
| T0145-1d8e | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 312 | - [ ] **First Contentful Paint** < 1.8s |
| T0146-e242 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 313 | - [ ] **Largest Contentful Paint** < 2.5s |
| T0147-9e8c | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 314 | - [ ] **Cumulative Layout Shift** < 0.1 |
| T0148-353d | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 315 | - [ ] **First Input Delay** < 100ms |
| T0149-19d6 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 445 | - [ ] **Alle Tests bestanden** |
| T0150-62c1 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 446 | - [ ] **Performance Benchmarks erreicht** |
| T0151-5f09 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 447 | - [ ] **Mobile Testing abgeschlossen** |
| T0152-15c6 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 448 | - [ ] **Accessibility validiert** (WCAG 2.1) |
| T0153-49bb | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 449 | - [ ] **Cross-Browser getestet** (Chrome, Firefox, Safari, Edge) |
| T0154-aef7 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 450 | - [ ] **User Acceptance Testing** abgeschlossen |
| T0155-09ea | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 451 | - [ ] **Documentation aktualisiert** |
| T0156-b662 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 452 | - [ ] **Deployment Pipeline getestet** |
| T0157-8574 | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 453 | - [ ] **Monitoring Setup** aktiv |
| T0158-540a | docs/dev/Frontend-Modernisierung_Setup-Guide.md | 454 | - [ ] **Rollback Plan** definiert |
| T0159-a178 | docs/dev/README.md | 429 | # TODO: filter by OPA decision (resource tags vs user attributes) |
| T0160-9add | docs/dev/SECURITY-BLUEPRINT.md | 120 | ## ✅ Tickets (Erweiterung zum TODO-Index) |
| T0161-a02a | docs/dev/VERIFICATION-BLUEPRINT.md | 360 | ## ✅ Tickets (zum TODO-Index ergänzen) |
| T0162-38a5 | docs/dev/frontend_modernization_guide.md | 205 | - [ ] Design System implementiert |
| T0163-8f4a | docs/dev/frontend_modernization_guide.md | 206 | - [ ] Layout System eingerichtet |
| T0164-064f | docs/dev/frontend_modernization_guide.md | 207 | - [ ] Komponenten modernisiert |
| T0165-f94f | docs/dev/frontend_modernization_guide.md | 208 | - [ ] Responsive Design getestet |
| T0166-0d03 | docs/dev/frontend_modernization_guide.md | 209 | - [ ] Performance optimiert |
| T0167-599d | docs/dev/frontend_modernization_guide.md | 210 | - [ ] Tests aktualisiert |
| T0168-df6d | docs/dev/frontend_modernization_guide.md | 211 | - [ ] Accessibility geprüft |
| T0169-e4bc | docs/dev/frontend_modernization_guide.md | 212 | - [ ] Cross-Browser Tests |
| T0170-eb76 | docs/dev/frontend_modernization_guide.md | 213 | - [ ] Mobile Experience validiert |
| T0171-8937 | docs/dev/frontend_modernization_guide.md | 214 | - [ ] Documentation aktualisiert |
| T0172-f92e | docs/dev/superset-nifi-flowise.md | 184 | - [ ] **Superset-Composer**: JS/Python Helper eingebaut → Link öffnet Dashboard mit Filtern |
| T0173-bf72 | docs/dev/superset-nifi-flowise.md | 185 | - [ ] **NiFi→Aleph**: InvokeHTTP Multipart konfiguriert, 200/202 Rückgabe sichtbar |
| T0174-0b79 | docs/dev/superset-nifi-flowise.md | 186 | - [ ] **Flowise Agent**: Tools/Schemas registriert, Guardrail-Prompt gesetzt, Tool-Limit aktiv |
| T0175-c015 | docs/dev/superset-nifi-flowise.md | 187 | - [ ] **Smoke Tests**: |
| T0176-6588 | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 73 | * `WORK-ON-new_docs/out/todo_index.md` (alle Checkboxen `- [ ]`/`- [x]`/nummerierte, plus `TODO:`/`FIXME:`/`NOTE:`; **mit IDs T####-hash, Datei, Zeile, Text**) |
| T0177-e28e | docs/dev/dev-prompts/DOCS-CONSOLIDIERUNG.md | 256 | * **Alle** TODOs (Checkboxen + TODO/FIXME/NOTE) in `todo_index.md` mit **IDs + Quelle+Zeile**. |
| T0178-49f1 | docs/dev/v0.2/Datenquellen-Cluster.md | 89 | TODO: **Feature-Pakete** schnüren (z. B. „Media Sources Pack“, „Threat Intel Pack“), die direkt in die Roadmap (0.3/0.5) integriert werden können! |
| T0179-32c8 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 186 | ## 📋 Tickets (zum TODO-Index hinzufügen) |
| T0180-b2f3 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 233 | ## TODO: |
| T0181-ba97 | docs/dev/v0.2/FlowiseAI-Agents-integration.md | 236 | * `TODO-Index.md` (FLOWISE-Tickets anhängen) |
| T0182-f6a2 | docs/dev/v0.2/Preset-Profile.md | 276 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
| T0183-7bc9 | docs/dev/v0.2/Preset-Profile.md | 288 | TODO: packe das als `docs/presets/` (je ein YAML + README) ins Repo und ergänze `PRESET-*.md` mit konkreten NiFi Template-Exports und n8n JSONs für die drei Profile. |
| T0184-7fda | docs/dev/v0.2/TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T0185-96c6 | docs/dev/v0.2/TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T0186-6b53 | docs/dev/v0.2/TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T0187-daa2 | docs/dev/v0.2/TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T0188-f9c4 | docs/dev/v0.2/TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T0189-4020 | docs/dev/v0.2/TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T0190-6751 | docs/dev/v0.2/TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T0191-af05 | docs/dev/v0.2/TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T0192-59b8 | docs/dev/v0.2/TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T0193-67ad | docs/dev/v0.2/TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T0194-b2f1 | docs/dev/v0.2/TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T0195-5835 | docs/dev/v0.2/TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T0196-d447 | docs/dev/v0.2/TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T0197-b65a | docs/dev/v0.2/TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T0198-55a9 | docs/dev/v0.2/TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T0199-691f | docs/dev/v0.2/TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T0200-820c | docs/dev/v0.2/TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T0201-712e | docs/dev/v0.2/TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T0202-2b97 | docs/dev/v0.2/TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T0203-cb63 | docs/dev/v0.2/TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T0204-3943 | docs/dev/v0.2/TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T0205-2398 | docs/dev/v0.2/TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T0206-1740 | docs/dev/v0.2/TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T0207-9abc | docs/dev/v0.2/TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T0208-23ac | docs/dev/v0.2/TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T0209-c222 | docs/dev/v0.2/TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T0210-937e | docs/dev/v0.2/TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T0211-bb52 | docs/dev/v0.2/TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T0212-8977 | docs/dev/v0.2/TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T0213-fcc1 | docs/dev/v0.2/TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T0214-6700 | docs/dev/v0.2/TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T0215-7bb0 | docs/dev/v0.2/TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T0216-aa57 | docs/dev/v0.2/TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T0217-2d51 | docs/dev/v0.2/TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T0218-41cc | docs/dev/v0.2/TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T0219-b872 | docs/dev/v0.2/TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T0220-d2c7 | docs/dev/v0.2/TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T0221-2f80 | docs/dev/v0.2/TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T0222-538c | docs/dev/v0.2/TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T0223-4cbb | docs/dev/v0.2/TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T0224-a931 | docs/dev/v0.2/TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline: Claim Extract, Retrieval, RTE, Geo/Time/Media Checks, Aggregation |
| T0225-f81c | docs/dev/v0.2/TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T0226-a2ff | docs/dev/v0.2/TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T0227-edef | docs/dev/v0.2/TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T0228-0551 | docs/dev/v0.2/TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T0229-2792 | docs/dev/v0.2/TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T0230-6703 | docs/dev/v0.2/TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T0231-83fe | docs/dev/v0.2/TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T0232-2296 | docs/dev/v0.2/TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T0233-0711 | docs/dev/v0.2/TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) |
| T0234-bb75 | docs/dev/v0.2/TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T0235-b21c | docs/dev/v0.2/TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T0236-858d | docs/dev/v0.2/TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T0237-fa9a | docs/dev/v0.2/TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T0238-e9a6 | docs/dev/v0.2/TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T0239-12a4 | docs/dev/v0.2/TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T0240-6a23 | docs/dev/v0.2/TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T0241-50df | docs/dev/v0.2/TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T0242-e417 | docs/dev/v0.2/TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T0243-7686 | docs/dev/v0.2/TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T0244-0902 | docs/dev/v0.2/TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T0245-312b | docs/dev/v0.2/TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T0246-486e | docs/dev/v0.2/TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T0247-1fb0 | docs/dev/v0.2/TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T0248-e046 | docs/dev/v0.2/TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T0249-16c0 | docs/dev/v0.2/TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T0250-07d9 | docs/dev/v0.2/TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T0251-120d | docs/dev/v0.2/TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T0252-37a4 | docs/dev/v0.2/TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T0253-f6f0 | docs/dev/v0.2/TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T0254-f47e | docs/dev/v0.2/TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T0255-1e77 | docs/dev/v0.2/TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T0256-7fb2 | docs/dev/v0.2/TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T0257-1c9c | docs/dev/v0.2/TODO-Index.md | 107 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T0258-2fc5 | docs/dev/v0.2/TODO-Index.md | 108 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T0259-5950 | docs/dev/v0.2/TODO-Index.md | 109 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T0260-1e61 | docs/dev/v0.2/TODO-Index.md | 110 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T0261-3e09 | docs/dev/v0.2/TODO-Index.md | 111 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T0262-df0f | docs/dev/v0.2/TODO-Index.md | 112 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T0263-f079 | docs/dev/v0.2/TODO-Index.md | 113 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T0264-5ad2 | docs/dev/v0.2/TODO-Index.md | 114 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T0265-0c05 | docs/dev/v0.2/TODO-Index.md | 115 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T0266-6a13 | docs/dev/v0.2/TODO-Index.md | 116 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T0267-2a9e | docs/dev/v0.2/TODO-Index.md | 117 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T0268-c3e7 | docs/dev/v0.2/Ticket-Checkliste.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v0.2) |
| T0269-3c74 | docs/dev/v0.2/Ticket-Checkliste.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T0270-8638 | docs/dev/v0.2/Ticket-Checkliste.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T0271-f1eb | docs/dev/v0.2/Ticket-Checkliste.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T0272-ef38 | docs/dev/v0.2/Ticket-Checkliste.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T0273-2c4e | docs/dev/v0.2/Ticket-Checkliste.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T0274-260e | docs/dev/v0.2/Ticket-Checkliste.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T0275-cf39 | docs/dev/v0.2/Ticket-Checkliste.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T0276-c292 | docs/dev/v0.2/Ticket-Checkliste.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T0277-99a5 | docs/dev/v0.2/Ticket-Checkliste.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T0278-bd7b | docs/dev/v0.2/Ticket-Checkliste.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T0279-fd8d | docs/dev/v0.2/Ticket-Checkliste.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T0280-fe9c | docs/dev/v0.2/Ticket-Checkliste.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T0281-fb88 | docs/dev/v0.2/Ticket-Checkliste.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T0282-930a | docs/dev/v0.2/Ticket-Checkliste.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T0283-4371 | docs/dev/v0.2/Ticket-Checkliste.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T0284-a124 | docs/dev/v0.2/Ticket-Checkliste.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T0285-8031 | docs/dev/v0.2/Ticket-Checkliste.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T0286-4e3a | docs/dev/v0.2/Ticket-Checkliste.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T0287-2ecc | docs/dev/v0.2/Ticket-Checkliste.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T0288-2e7e | docs/dev/v0.2/Ticket-Checkliste.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T0289-f5ef | docs/dev/v0.2/Ticket-Checkliste.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T0290-8249 | docs/dev/v0.2/Ticket-Checkliste.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T0291-5343 | docs/dev/v0.2/Ticket-Checkliste.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T0292-f471 | docs/dev/v0.2/Ticket-Checkliste.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T0293-2e62 | docs/dev/v0.2/Ticket-Checkliste.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T0294-7965 | docs/dev/v0.2/Ticket-Checkliste.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T0295-361b | docs/dev/v0.2/Ticket-Checkliste.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T0296-5733 | docs/dev/v0.2/Ticket-Checkliste.md | 46 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T0297-3f9b | docs/dev/v0.2/Ticket-Checkliste.md | 47 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T0298-b3a4 | docs/dev/v0.2/Ticket-Checkliste.md | 48 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T0299-3d06 | docs/dev/v0.2/Ticket-Checkliste.md | 49 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T0300-9f55 | docs/dev/v0.2/Ticket-Checkliste.md | 52 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T0301-5754 | docs/dev/v0.2/Ticket-Checkliste.md | 53 | - [ ] **[NIFI-2]** API Ingest Flow |
| T0302-5b96 | docs/dev/v0.2/Ticket-Checkliste.md | 54 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T0303-33e5 | docs/dev/v0.2/Ticket-Checkliste.md | 55 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T0304-a3e0 | docs/dev/v0.2/Ticket-Checkliste.md | 56 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T0305-61ea | docs/dev/v0.2/Ticket-Checkliste.md | 57 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T0306-916b | docs/dev/v0.2/Ticket-Checkliste.md | 60 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T0307-4960 | docs/dev/v0.2/Ticket-Checkliste.md | 61 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T0308-8ca4 | docs/dev/v0.2/Ticket-Checkliste.md | 62 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T0309-7ca5 | docs/dev/v0.2/Ticket-Checkliste.md | 63 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T0310-0356 | docs/dev/v0.2/Ticket-Checkliste.md | 64 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T0311-212d | docs/dev/v0.2/Ticket-Checkliste.md | 67 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T0312-31f1 | docs/dev/v0.2/Ticket-Checkliste.md | 68 | - [ ] **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) |
| T0313-4657 | docs/dev/v0.2/Ticket-Checkliste.md | 69 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T0314-cddb | docs/dev/v0.2/Ticket-Checkliste.md | 70 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T0315-f7bd | docs/dev/v0.2/Ticket-Checkliste.md | 71 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T0316-5a2d | docs/dev/v0.2/Ticket-Checkliste.md | 74 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T0317-d15b | docs/dev/v0.2/Ticket-Checkliste.md | 75 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T0318-0844 | docs/dev/v0.2/Ticket-Checkliste.md | 76 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T0319-d223 | docs/dev/v0.2/Ticket-Checkliste.md | 77 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T0320-9bd6 | docs/dev/v0.2/Ticket-Checkliste.md | 78 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T0321-9b01 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 1 | # 📝 InfoTerminal TODO-Index (v0.1.9.1 → v1.0) |
| T0322-98e9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 9 | - [ ] **[CORE-API-1]** Vereinheitliche `/healthz` und `/readyz` Endpoints |
| T0323-65a0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 10 | - [ ] **[CORE-API-2]** Einheitliches Error-Schema (RFC 7807 JSON Problem Detail) |
| T0324-bf0a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 11 | - [ ] **[CORE-API-3]** Swagger/OpenAPI Doku für alle Services |
| T0325-c7b2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 12 | - [ ] **[CORE-API-4]** OAuth2 JWT Auth im Gateway + OIDC Integration |
| T0326-a895 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 13 | - [ ] **[CORE-API-5]** Audit-Logging Middleware (structured JSON mit X-Request-ID) |
| T0327-80a2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 16 | - [ ] **[GRAPH-1]** Ontologie-Layer (Entities, Events, Relations, Properties) |
| T0328-2c6a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 17 | - [ ] **[GRAPH-2]** Graph-Algorithmen v1 (Degree Centrality, Betweenness, Louvain, Dijkstra) |
| T0329-1030 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 18 | - [ ] **[GRAPH-3]** Robustere Cypher-Queries (Retry/Backoff) |
| T0330-3c05 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 19 | - [ ] **[GRAPH-4]** Graph-Export (GraphML, JSON) |
| T0331-7e80 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 20 | - [ ] **[GRAPH-5]** Audit: Query-Logs + Query-Metrics |
| T0332-d255 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 23 | - [ ] **[SEARCH-1]** NLP v1 Integration (NER, RE, Summarization) |
| T0333-041e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 24 | - [ ] **[SEARCH-2]** Embedding Reranking Pipeline (Flag-gesteuert) |
| T0334-fd93 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 25 | - [ ] **[SEARCH-3]** Index-Policy für „news“, „docs“ und „plugins“ |
| T0335-3c21 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 26 | - [ ] **[SEARCH-4]** Export: JSON/CSV Dumps pro Index |
| T0336-41fe | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 27 | - [ ] **[SEARCH-5]** Observability: Search-Latency + Query Errors in Prometheus |
| T0337-9e56 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 30 | - [ ] **[VIEWS-1]** Healthcheck (SELECT 1 + DB latency) |
| T0338-3721 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 31 | - [ ] **[VIEWS-2]** Views für Ontologie-Entities (JOIN Neo4j + Postgres) |
| T0339-66bd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 32 | - [ ] **[VIEWS-3]** Integration mit Superset (Cross-Filter Views) |
| T0340-6e54 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 33 | - [ ] **[VIEWS-4]** Ready-Metrics (Connections, Idle, Errors) |
| T0341-c05d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 36 | - [ ] **[FE-1]** Einheitliches Theme (globals.css konsolidieren) |
| T0342-0998 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 37 | - [ ] **[FE-2]** /search: Facettenfilter + Ranking-Regler |
| T0343-7ca3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 38 | - [ ] **[FE-3]** /graphx: Ontologie-Visualisierung + Algorithmen-Ergebnisse |
| T0344-bfd4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 39 | - [ ] **[FE-4]** /graphx: Geospatial Layer (Leaflet/MapLibre) |
| T0345-6ecc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 40 | - [ ] **[FE-5]** /settings: Endpoints + OAuth2/OIDC Config sichtbar |
| T0346-7ca7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 41 | - [ ] **[FE-6]** Dossier-Lite: Report-Builder (Export PDF/MD) |
| T0347-1b1d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 42 | - [ ] **[FE-7]** Collaboration: Notes/Comments (Yjs CRDT) |
| T0348-e05d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 43 | - [ ] **[FE-8]** Audit-Overlay (zeige Logs/Aktionen pro User) |
| T0349-2ffc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 44 | - [ ] **[FE-9]** Verification-Badges & Evidence-Panel (Veracity Scores) |
| T0350-45fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 45 | - [ ] **[FE-10]** Review-UI für Claims/Evidence (Overrides, History) |
| T0351-0b8d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 48 | - [ ] **[GATE-1]** OAuth2/OIDC Support (JWT Validation) |
| T0352-a0c3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 49 | - [ ] **[GATE-2]** Policy-Dateien für Role-Based-Access erweitern |
| T0353-3f86 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 50 | - [ ] **[GATE-3]** Attribute-Level Security vorbereiten |
| T0354-6b86 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 51 | - [ ] **[GATE-4]** Audit-Logs in Loki weiterleiten |
| T0355-1d77 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 54 | - [ ] **[NIFI-1]** RSS/Atom Ingest Flow |
| T0356-0c39 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 55 | - [ ] **[NIFI-2]** API Ingest Flow |
| T0357-2ef3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 56 | - [ ] **[NIFI-3]** File Watch/Upload Flow (OCR + NLP) |
| T0358-fc5e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 57 | - [ ] **[NIFI-4]** Streaming/Kafka Pipeline (Sensor/CDR) |
| T0359-51d4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 58 | - [ ] **[NIFI-5]** Video-Pipeline (NiFi → FFmpeg → ML inference) |
| T0360-153d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 59 | - [ ] **[NIFI-6]** Geospatial Enrichment (Geocoding via Nominatim/Photon) |
| T0361-ddc6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 60 | - [ ] **[NIFI-7]** Verification-Pipeline (Claims, Retrieval, RTE, Geo/Media, Aggregation) |
| T0362-ac36 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 63 | - [ ] **[N8N-1]** Investigation Assistant Flow (search+graph queries) |
| T0363-a931 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 64 | - [ ] **[N8N-2]** Alerts Flow (keyword watchlists → Slack/Email) |
| T0364-372c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 65 | - [ ] **[N8N-3]** Cross-Source Correlation (news+social+plugins) |
| T0365-fd4e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 66 | - [ ] **[N8N-4]** Case Dossier Creation (auto-PDF + Graph snapshot) |
| T0366-8215 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 67 | - [ ] **[N8N-5]** Plugin Integration Flows (z. B. nmap → Graph) |
| T0367-7ca1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 68 | - [ ] **[N8N-6]** Veracity Alerts (false/manipulative → escalate) |
| T0368-1981 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 69 | - [ ] **[N8N-7]** Escalation Flow (hoher Widerspruchsgrad → Senior Review) |
| T0369-1576 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 72 | - [ ] **[CLI-1]** Lifecycle Commands (up/down/start/stop/restart/status/logs) |
| T0370-68c4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 73 | - [ ] **[CLI-2]** Export Command (`it export [graph\|search\|dossier]`) |
| T0371-8604 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 74 | - [ ] **[CLI-3]** Plugin Command (`it plugin run <tool>`) |
| T0372-c399 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 75 | - [ ] **[CLI-4]** Auth Command (`it login --oidc`) |
| T0373-106b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 76 | - [ ] **[CLI-5]** Format-Optionen für Status/Logs (json/yaml/table) |
| T0374-d37d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 79 | - [ ] **[OBS-1]** Observability Profile (Prometheus, Grafana, Loki, Tempo, Alertmanager) |
| T0375-9334 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 80 | - [ ] **[OBS-2]** Structured JSON Logs (X-Request-ID) |
| T0376-0715 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 81 | - [ ] **[OBS-3]** Backup-Scripts (Neo4j, Postgres, OpenSearch) |
| T0377-c658 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 82 | - [ ] **[OBS-4]** Coverage Gate fixen + CI stabilisieren |
| T0378-8b2d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 83 | - [ ] **[OBS-5]** Frontend Build Konflikt (settings page) lösen |
| T0379-7db0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 88 | - [ ] **[SEC-EGRESS-1]** Egress-Gateway (Tor+VPN+Proxy-Chain, Kill-Switch, DNS-Sinkhole) |
| T0380-16e2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 89 | - [ ] **[SEC-EGRESS-2]** NetworkPolicy: Services nur via Egress-Gateway |
| T0381-92b0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 90 | - [ ] **[SEC-EGRESS-3]** UI-Schalter `IT_MODE/IT_EGRESS`, Proxy-Injektion |
| T0382-4020 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 91 | - [ ] **[SEC-EGRESS-4]** DNS-Hardening: DoH/Tor-DNS, blockiere Port 53 |
| T0383-d4f1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 92 | - [ ] **[SEC-STORE-1]** Ephemeral FS (Incognito Sessions, Auto-Wipe) |
| T0384-f488 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 93 | - [ ] **[SEC-STORE-2]** Vault-Integration + per-Tenant Keys |
| T0385-446f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 94 | - [ ] **[SEC-STORE-3]** Hash+Sign-Pipeline für Forensics-Exporte |
| T0386-31b9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 95 | - [ ] **[SEC-BROWSER-1]** Remote Browser Pool (Profile, WebRTC-Off, Cookie-Jar per Case) |
| T0387-dbcf | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 96 | - [ ] **[SEC-BROWSER-2]** Identity Profiles (UA/Locale/Timezone) |
| T0388-8ce4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 97 | - [ ] **[SEC-BROWSER-3]** robots.txt-Enforcer + Quell-Whitelist |
| T0389-99a1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 98 | - [ ] **[SEC-AUDIT-1]** Dual-Plane Logging (persistent vs. in-memory) |
| T0390-a791 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 99 | - [ ] **[SEC-AUDIT-2]** UI-Warnungen (Export enthält Metadaten) |
| T0391-7d18 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 100 | - [ ] **[SEC-SBX-1]** Plugin-Sandbox (gVisor/Kata/Firecracker, default no-net) |
| T0392-d21d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 101 | - [ ] **[SEC-SBX-2]** OPA-Validierung `plugin.yaml` (CAPs/Secrets) |
| T0393-2238 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 102 | - [ ] **[SEC-SBX-3]** SBOM/Cosign/Trivy-Scans in CI |
| T0394-6bc3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 105 | - [ ] **[VERIF-1]** Source Reputation & Bot-Likelihood Modul |
| T0395-a4e8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 106 | - [ ] **[VERIF-2]** Claim-Extractor + MinHash Cluster + Claim IDs |
| T0396-1c33 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 107 | - [ ] **[VERIF-3]** Evidence Retrieval (Hybrid BM25+Dense) |
| T0397-a6b4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 108 | - [ ] **[VERIF-4]** RTE/Stance Classifier + Aggregation |
| T0398-8b5f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 109 | - [ ] **[VERIF-5]** Temporal/Geo Checks (Mordecai + Heuristiken) |
| T0399-180b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 110 | - [ ] **[VERIF-6]** Media Forensics (pHash, EXIF, Reverse Search, ELA) |
| T0400-c4b9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 111 | - [ ] **[VERIF-7]** Schema/Mappings/Constraints für Verification (OpenSearch + Neo4j) |
| T0401-77fd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 112 | - [ ] **[VERIF-8]** Review-UI (Evidence Panel, Overrides, History) |
| T0402-ce13 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 113 | - [ ] **[VERIF-9]** Active Learning Loop (Label-Store, Re-Training) |
| T0403-69fa | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 114 | - [ ] **[VERIF-10]** n8n Alerts/Escalations (Watchlists, kontrovers) |
| T0404-f3ee | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 115 | - [ ] **[VERIF-11]** Dossier-Integration (Claim-basierte Reports mit Evidenz-Anhang) |
| T0405-14e5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 120 | - [ ] **[LEGAL-1]** RAG-Service für Gesetzestexte |
| T0406-4ead | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 121 | - [ ] **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange) |
| T0407-2047 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 122 | - [ ] **[LEGAL-3]** NiFi ingest_laws + rag_index |
| T0408-6762 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 123 | - [ ] **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports |
| T0409-2e6c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 124 | - [ ] **[LEGAL-5]** Frontend Tab „Legal/Compliance“ |
| T0410-f1e0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 125 | - [ ] **[LEGAL-6]** Dossier-Vorlage Compliance Report |
| T0411-4708 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 128 | - [ ] **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash) |
| T0412-31fc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 129 | - [ ] **[DISINFO-2]** Bot-Likelihood Modul |
| T0413-4f04 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 130 | - [ ] **[DISINFO-3]** Temporal Pattern Detection |
| T0414-9568 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 131 | - [ ] **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier |
| T0415-b1c0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 132 | - [ ] **[DISINFO-5]** Frontend Dashboard Top Narratives |
| T0416-1dcd | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 133 | - [ ] **[DISINFO-6]** Fact-Check API Integration |
| T0417-46c1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 136 | - [ ] **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions |
| T0418-a533 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 137 | - [ ] **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions |
| T0419-bb7e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 138 | - [ ] **[SUPPLY-3]** Simulation Engine (Event → Impact) |
| T0420-50dc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 139 | - [ ] **[SUPPLY-4]** n8n Risk Alerts + Impact Reports |
| T0421-2a9c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 140 | - [ ] **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool |
| T0422-08f6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 141 | - [ ] **[SUPPLY-6]** Dossier Supply Chain Risk Report |
| T0423-1d1b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 144 | - [ ] **[FIN-1]** Graph-Schema Accounts/Transfers |
| T0424-a3cc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 145 | - [ ] **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions |
| T0425-fd36 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 146 | - [ ] **[FIN-3]** Leak-Integration (ICIJ Leaks → Graph) |
| T0426-3327 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 147 | - [ ] **[FIN-4]** Anomaly Detection Module |
| T0427-2069 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 148 | - [ ] **[FIN-5]** n8n Red Flag Alerts + Escalations |
| T0428-c621 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 149 | - [ ] **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard |
| T0429-6ff2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 150 | - [ ] **[FIN-7]** Dossier Financial Red Flags |
| T0430-67f7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 153 | - [ ] **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social |
| T0431-bf12 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 154 | - [ ] **[GEO-2]** Graph-Schema Events/Assets/Conflicts |
| T0432-aea2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 155 | - [ ] **[GEO-3]** Geo-Time Anomaly Detection |
| T0433-1a1a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 156 | - [ ] **[GEO-4]** n8n Alerts + Conflict Reports |
| T0434-19f9 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 157 | - [ ] **[GEO-5]** Frontend Map Dashboard + Timeline |
| T0435-2ee2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 158 | - [ ] **[GEO-6]** Simulation Engine (Eskalations-Szenarien) |
| T0436-2f84 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 159 | - [ ] **[GEO-7]** Dossier Geopolitical Report |
| T0437-e37f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 162 | - [ ] **[HUM-1]** NiFi ingest_health_weather_data + merge_indicators |
| T0438-506b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 163 | - [ ] **[HUM-2]** Graph-Schema Crisis/Indicators/Regions |
| T0439-2b4c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 164 | - [ ] **[HUM-3]** Risk Assessment Modul (ML) |
| T0440-4c5e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 165 | - [ ] **[HUM-4]** n8n Crisis Alerts + Reports |
| T0441-592b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 166 | - [ ] **[HUM-5]** Frontend Crisis Dashboard + Forecast |
| T0442-e6a5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 167 | - [ ] **[HUM-6]** Dossier Humanitarian Crisis Report |
| T0443-dae0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 172 | - [ ] **[CLIMATE-1]** NiFi ingest_climate_data (NASA/ESA/Copernicus) |
| T0444-d4b8 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 173 | - [ ] **[CLIMATE-2]** Graph-Schema ClimateIndicators |
| T0445-1637 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 174 | - [ ] **[CLIMATE-3]** CO₂/Emission Scoring Modul |
| T0446-c7e3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 175 | - [ ] **[CLIMATE-4]** n8n Alerts (Emission Targets) |
| T0447-e2e1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 176 | - [ ] **[CLIMATE-5]** Frontend Climate Dashboard + Heatmap |
| T0448-ee18 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 177 | - [ ] **[CLIMATE-6]** Dossier Climate Risk Report |
| T0449-3fb5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 180 | - [ ] **[TECH-1]** NiFi ingest_patents + research_data |
| T0450-3a76 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 181 | - [ ] **[TECH-2]** Graph-Schema Patents/TechTrends |
| T0451-79ca | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 182 | - [ ] **[TECH-3]** Innovation Hotspot Detection |
| T0452-e066 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 183 | - [ ] **[TECH-4]** n8n Tech Trend Reports |
| T0453-2bc7 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 184 | - [ ] **[TECH-5]** Frontend Patent/Innovation Graph |
| T0454-9331 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 185 | - [ ] **[TECH-6]** Dossier Technology Trends |
| T0455-1a7d | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 188 | - [ ] **[TERROR-1]** Ingest Propaganda Sources (Social, Web) |
| T0456-b3f1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 189 | - [ ] **[TERROR-2]** Graph-Schema TerrorNetworks |
| T0457-27a1 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 190 | - [ ] **[TERROR-3]** Finance Flow Analysis |
| T0458-2298 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 191 | - [ ] **[TERROR-4]** n8n Alerts Suspicious Networks |
| T0459-a992 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 192 | - [ ] **[TERROR-5]** Frontend Terror Network Graph |
| T0460-556f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 193 | - [ ] **[TERROR-6]** Dossier Terrorism Threat Report |
| T0461-33d4 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 196 | - [ ] **[HEALTH-1]** NiFi ingest_health_data (WHO, RKI, Social) |
| T0462-28b2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 197 | - [ ] **[HEALTH-2]** Graph-Schema HealthEvents/Regions |
| T0463-285e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 198 | - [ ] **[HEALTH-3]** Epidemic Outbreak Detection |
| T0464-e099 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 199 | - [ ] **[HEALTH-4]** n8n Health Alerts + Reports |
| T0465-7e5b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 200 | - [ ] **[HEALTH-5]** Frontend Health Dashboard |
| T0466-9566 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 201 | - [ ] **[HEALTH-6]** Dossier Health/Epidemic Report |
| T0467-9be3 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 204 | - [ ] **[ETHICS-1]** Ingest Model Cards + AI Incident Data |
| T0468-0224 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 205 | - [ ] **[ETHICS-2]** Graph-Schema Bias/Models/Orgs |
| T0469-72d2 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 206 | - [ ] **[ETHICS-3]** Bias Detection Modul |
| T0470-b207 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 207 | - [ ] **[ETHICS-4]** n8n Alerts (Bias, Ethics Violations) |
| T0471-2b54 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 208 | - [ ] **[ETHICS-5]** Frontend AI Ethics Dashboard |
| T0472-626b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 209 | - [ ] **[ETHICS-6]** Dossier AI Ethics Report |
| T0473-2501 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 212 | - [ ] **[MEDIA-1]** Ingest Images/Videos (EXIF, Hashing) |
| T0474-589c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 213 | - [ ] **[MEDIA-2]** Deepfake Detection Modul |
| T0475-695a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 214 | - [ ] **[MEDIA-3]** Graph-Schema MediaAuthenticity |
| T0476-376a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 215 | - [ ] **[MEDIA-4]** n8n Alerts Fake Media |
| T0477-0a9f | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 216 | - [ ] **[MEDIA-5]** Frontend Media Forensics Panel |
| T0478-ba2e | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 217 | - [ ] **[MEDIA-6]** Dossier Media Authenticity Report |
| T0479-4d93 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 220 | - [ ] **[ECON-1]** NiFi ingest_economic_data (IMF, OECD, World Bank) |
| T0480-14dc | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 221 | - [ ] **[ECON-2]** Graph-Schema EconomicIndicators/Trades |
| T0481-f3ec | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 222 | - [ ] **[ECON-3]** Market Risk Analysis Modul |
| T0482-0cd0 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 223 | - [ ] **[ECON-4]** n8n Economic Reports |
| T0483-0bf6 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 224 | - [ ] **[ECON-5]** Frontend Economic Dashboard |
| T0484-df2a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 225 | - [ ] **[ECON-6]** Dossier Economic Intelligence Report |
| T0485-6a5b | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 228 | - [ ] **[CULTURE-1]** Ingest Social/News/Blog Data |
| T0486-8739 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 229 | - [ ] **[CULTURE-2]** Graph-Schema Narratives/Discourse |
| T0487-0478 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 230 | - [ ] **[CULTURE-3]** Meme/Hashtag Cluster Detection |
| T0488-6ff5 | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 231 | - [ ] **[CULTURE-4]** n8n Cultural Trend Reports |
| T0489-227c | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 232 | - [ ] **[CULTURE-5]** Frontend Cultural Trends Dashboard |
| T0490-d40a | docs/dev/v0.2/v0.3+/Master-TODO-Index.md | 233 | - [ ] **[CULTURE-6]** Dossier Cultural Intelligence Report |
| T0491-04f8 | docs/dev/v0.2/v0.3+/Preset-Profile_ideen.md | 103 | # 📌 Tickets (zum TODO-Index ergänzen) |
| T0492-72f7 | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 3 | - [ ] **[CLI-WT-1]** `it waveterm open` – WaveTerm Instanz öffnen (Browser/Panel) |
| T0493-5a1c | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 4 | - [ ] **[CLI-WT-2]** `it waveterm send` – Kommando in aktiven Workspace senden |
| T0494-da3e | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 5 | - [ ] **[CLI-WT-3]** `it waveterm case` – Case-Verzeichnis mounten/attachen |
| T0495-4a5c | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 6 | - [ ] **[CLI-WT-4]** `it waveterm export` – Session/Artefakte → Dossier-Appendix |
| T0496-abac | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 7 | - [ ] **[CLI-WT-5]** Vault-/Token-Handling für WaveTerm-Kommandos |
| T0497-b3ad | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 8 | - [ ] **[CLI-WT-6]** OPA-Policies für WaveTerm-CLI-Befehle |
| T0498-829b | docs/dev/v0.2/v0.3+/TODO-Index-cli-ergänzung.md | 9 | - [ ] **[CLI-WT-7]** Roundtrip-Tests (CLI → WaveTerm → Artefakte → Dossier) |
| T0499-071f | docs/presets/Presets(Profile).md | 303 | # Umsetzung: Tickets (zum Master TODO-Index ergänzen) |
