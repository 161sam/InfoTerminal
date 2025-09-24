# 🗺️ ROADMAP_STATUS – Phase 2 Kick-off (2025-09-24)

The Phase 2–4 roadmap is organized into subsystem packages A–L plus Hardening and Release. Each section summarises the target state, current implementation evidence, gaps, Definition of Done (DoD), and dependencies.

> 📌 **Wave ordering reference:** [`backlog/phase2/PACKAGE_SEQUENCE.yaml`](backlog/phase2/PACKAGE_SEQUENCE.yaml) feeds dashboards and checklists for the active wave limit (max two concurrent packages).

## A) Ontologie & Graph
- **Goal**: Complete ontology coverage, graph analytics APIs (degree, betweenness, communities, shortest paths), dossier export hooks, and geo-enabled subgraph views.
- **Current Evidence**:
  - FastAPI analytics router exposes degree, Louvain, shortest-path, and subgraph export endpoints with Prometheus counters. 【F:services/graph-api/app/routes/analytics.py†L1-L220】【F:services/graph-api/metrics.py†L1-L40】
  - Superset dashboard + Grafana panels checked in for graph analytics MVP. 【F:apps/superset/assets/dashboard/graph_analytics_mvp.json†L1-L200】【F:grafana/dashboards/graph-analytics-mvp.json†L1-L200】
  - README beschreibt 5-Minuten-Demo für Search → Graph → Dossier inklusive Subgraph-Export. 【F:README.md†L17-L94】
- **Gaps / Risks**:
  - Frontend graph explorer still targets hard-coded localhost endpoints, bypassing gateway routing. 【F:apps/frontend/src/components/graph/GraphExplorer.tsx†L1-L92】
  - Ontology validation + automated Superset import checks not yet part of CI.
- **DoD Checklist**:
  - [x] Observability: `/metrics`, `/healthz`, `/readyz` with graph-specific dashboards.
  - [ ] Tests: Integration tests covering analytics endpoints and ontology validators.
  - [x] Docs: Updated ontology reference + sample queries in `docs/`.
  - [ ] Security: Gateway + OPA policies guarding graph export endpoints.
- **Dependencies**: Package C (Geospatial map overlays), Package F (Dossier integration).

## B) NLP & KI-Layer
- **Goal**: Stable summarisation, relation extraction, entity linking with confidence reporting, and feedback loops for active learning.
- **Current Evidence**:
  - Doc-entities router provides NER, relations, fuzzy matching, graph write hooks und liefert Resolver-Metadaten + HTML Highlights. 【F:services/doc-entities/routers/doc_entities_v1.py†L1-L390】
  - Resolver aggregiert Alias/Fuzzy Kandidaten, exportiert Prometheus Counter & Histogramme inkl. `doc_entities_linking_status_total`. 【F:services/doc-entities/resolver.py†L1-L220】【F:services/doc-entities/metrics.py†L1-L68】
  - Frontend zeigt Linking-Badges & README dokumentiert Demo-Fluss (NER → Resolver → Geo). 【F:apps/frontend/src/components/docs/DocumentDetail.tsx†L1-L320】【F:README.md†L48-L96】
- **Gaps / Risks**:
  - Summaries und Feedback-Flows bleiben Mock; Active-Learning-Persistence & Resolver-Audit fehlen. 【F:apps/frontend/pages/dossier.tsx†L60-L120】
  - Evaluation-Datasets / Precision-Tracking für Linking fehlen weiterhin.
- **DoD Checklist**:
  - [x] Observability: Latency/error metrics for NER, summarisation, linking pipelines.
  - [x] Tests: Gold-sample regression tests for NER, relations, linking precision/recall.
  - [x] Docs: README demo + Wave 2 checklist dokumentieren Linking/Geo Flow. 【F:README.md†L48-L96】【F:backlog/phase2/WAVE2_DOD_CHECKLIST.md†L1-L80】
  - [ ] Security: Input size limits + audit logging for feedback endpoints.
- **Dependencies**: Package F (Dossier), Package H (Agents need NLP tooling).

## C) Geospatial-Layer
- **Goal**: Geo ingest (GeoJSON/OSM), bbox/nearby APIs, clustering/heatmaps, and frontend map overlays linked to the graph.
- **Current Evidence**:
  - `/geo/entities` + `/geo/entities/nearby` beantworten BBox/Radius Queries; Counters `graph_geo_queries_total`, `geo_query_count`, Fehlerzähler & Grafana-Panels aktiv. 【F:services/graph-api/app/routes/geospatial.py†L1-L220】【F:services/graph-api/metrics.py†L28-L40】【F:monitoring/grafana-dashboards/infoterminal-overview.json†L1-L400】
  - Frontend Map Panel & README Demo nutzen Graph-Geo API (Bounding Box, Nearby, Heatmap). 【F:apps/frontend/src/components/MapPanel.tsx†L1-L220】【F:README.md†L63-L96】
  - Graph-views exposes a dedicated geo router. 【F:services/graph-views/geo.py†L1-L120】
- **Gaps / Risks**:
  - Kein automatisiertes GeoJSON/OSM-Ingest; Geocoding Add-on default deaktiviert, Rate-Limits offen.
  - Karten rely on Demo-Daten; Caching/normalisation docs fehlen weiterhin.
- **DoD Checklist**:
  - [x] Observability: Geo ingest job metrics + map tile latency dashboards.
  - [x] Tests: API tests for bbox/nearby endpoints with sample fixtures.
  - [x] Docs: Geospatial ingest guide + map integration walkthrough.
  - [ ] Security: Rate limits for external geocode providers; location privacy review.
- **Dependencies**: Package A (graph data), Package D (ingest pipelines), Package K (frontend UX).

## D) Daten-Ingest & Workflows (NiFi/n8n)
- **Goal**: Standard flows for CSV/JSON/RSS/streaming, reusable playbooks chaining search → NLP → graph, plus idempotent retry/backoff paths.
- **Current Evidence**:
  - Compose overlays ship NiFi and n8n services with dedicated ports. 【F:inventory/services.json†L266-L289】
  - Sample n8n playbooks (`fact-checking-assistant-v2.json`, `investigation-assistant-v1.json`). 【F:apps/n8n/fact-checking-assistant-v2.json†L1-L80】
  - NiFi scripts for start/stop/import exist under `scripts/`. 【F:scripts/nifi_start.sh†L1-L40】
- **Gaps / Risks**:
  - No automated import/upgrade story for flows; retry/DLQ handling undocumented.
  - Observability and error channels missing from playbooks.
- **DoD Checklist**:
  - [ ] Observability: Flow success/error metrics exported to Prometheus.
  - [ ] Tests: Smoke tests for template instantiation and sample data ingestion.
  - [ ] Docs: Step-by-step import + troubleshooting guide.
  - [ ] Security: Credential management + rate-limit guardrails for external feeds.
- **Dependencies**: Packages B (NLP services), F (Dossier generation), I (external feeds).

## E) Video-Pipeline (MVP)
- **Goal**: NiFi → FFmpeg → ML pipeline generating scene/object metadata, graph integration, and correction UI.
- **Current Evidence**:
  - `/v1/videos/analyze` streams frames, detects objects, and guards upload size via feature flag `VIDEO_PIPELINE_ENABLED`. 【F:services/media-forensics/routers/media_forensics_v1.py†L1-L420】
  - OpenCV-based pipeline extracts scenes/objects, increments `video_frames_processed_total`, and prepares graph payloads. 【F:services/media-forensics/video_pipeline.py†L1-L200】
  - Quickstart documents demo workflow incl. Grafana panel for frames processed. 【F:docs/media/video_pipeline.md†L1-L160】【F:monitoring/grafana-dashboards/infoterminal-overview.json†L560-L660】
- **Gaps / Risks**:
  - Pipeline glue (NiFi → FFmpeg) absent; no storage schema for extracted metadata.
  - Frontend views still static; no correction workflow.
- **DoD Checklist**:
  - [x] Observability: Processing latency + queue depth metrics.
  - [x] Tests: Integration test from sample video to graph entries.
  - [x] Docs: Demo walkthrough + resource requirements.
  - [ ] Security: Sandbox FFmpeg execution, validate uploads.
- **Dependencies**: Packages D (workflows), F (dossier), G (plugin sandbox), H (agents for review).

## F) Dossier & Collaboration
- **Goal**: Export dossiers (PDF/MD) from search/graph context, shared notes/comments per case, audit logging.
- **Current Evidence**:
  - Collab-hub `/dossier/export` erzeugt Markdown/PDF inkl. Templates & Metrics, Tests decken Markdown/PDF + Notes Feature ab. 【F:services/collab-hub/app/main.py†L200-L360】【F:services/collab-hub/tests/test_dossier.py†L1-L60】
  - Feature-flagged Notizen mit Audit-Logging (`CH_AUDIT_PATH`) aktivierbar; README-Demo referenziert End-to-End-Fluss. 【F:services/collab-hub/app/main.py†L60-L220】【F:README.md†L51-L94】
  - Beispiel-Exports unter `examples/dossier/` dokumentiert. 【F:examples/dossier/README.md†L1-L80】
- **Gaps / Risks**:
  - Audit logging not yet shipped to Loki/Tempo; frontend dossier builder und notes UI weiterhin ohne Backend-Verbindung.
  - Case-basierte RBAC/Sharing-Regeln fehlen.
- **DoD Checklist**:
  - [x] Observability: Metrics for dossier exports and collaboration events.
  - [ ] Tests: E2E flow from search selection to dossier PDF.
  - [x] Docs: Collaboration how-to + template catalogue.
  - [ ] Security: Access controls per case + audit trail ingestion.
- **Dependencies**: Packages A/B (data sources), J (observability), Release.

## G) Plugin-Architektur (Kali-Tools)
- **Goal**: Plugin registry + sandbox runner (timeouts, resource controls), example plugins (nmap, whois) integrated with workflows and search ingest.
- **Current Evidence**:
  - Plugin-runner enforces per-plugin metrics/timeouts and forwards results to Graph/Search via async ingestor. 【F:services/plugin-runner/app_v1.py†L1-L260】【F:services/plugin-runner/metrics.py†L1-L27】
  - Mockable nmap workflow with tests + mock output ensures offline determinism. 【F:services/plugin-runner/tests/test_nmap_ingest.py†L1-L60】【F:plugins/nmap/mock_output.xml†L1-L25】
  - Plugin quickstart documents registry schema, execution API, and metrics endpoints. 【F:docs/plugins/quickstart.md†L1-L200】
- **Gaps / Risks**:
  - Sandbox isolation + resource caps not enforced; security review pending.
  - No automated ingest of plugin outputs into search/graph.
- **DoD Checklist**:
  - [x] Observability: Plugin execution metrics + audit logs.
  - [x] Tests: Smoke tests per plugin, failure-path coverage.
  - [x] Docs: Plugin authoring guide + registry schema.
  - [ ] Security: Timeouts, input validation, container isolation, OPA policies.
- **Dependencies**: Packages H (agents), D (workflows), Security hardening.

## H) AI-Agenten
- **Goal**: Flowise connector, multi-agent playbooks (researcher/verifier/dossier), Assistant UI with tool panels, policy enforcement.
- **Current Evidence**:
-  - Flowise connector MVP enforces an OPA-governed six-tool registry, `/chat` with mocked tool execution, and Prometheus counters plus UI surfacing policy errors. 【F:services/flowise-connector/app/main.py†L1-L520】【F:services/flowise-connector/tests/test_agents_mvp.py†L1-L140】【F:apps/frontend/pages/agent/mvp.tsx†L1-L280】
-  - Grafana dashboard extended with agent counters; quickstart documents setup and offline demo. 【F:grafana/dashboards/infra-overview.json†L7-L40】【F:docs/agents/quickstart.md†L1-L120】
-  - Frontend ships `/agent/mvp` single-turn chat with progress badges + API proxy. 【F:apps/frontend/pages/agent/mvp.tsx†L1-L265】【F:apps/frontend/pages/api/agent/mvp-chat.ts†L1-L80】
- **Gaps / Risks**:
-  - Flowise integration still mocked; OPA policies and multi-turn orchestration pending.
-  - Audit logging and tool telemetry need central sink; cancellation hook currently stub only.
- **DoD Checklist**:
  - [ ] Observability: Agent invocation metrics + failure alerts.
  - [ ] Tests: Scenario tests for tool chaining and fallback paths.
  - [ ] Docs: Agent playbook catalogue + policy requirements.
  - [ ] Security: OPA enforcement, rate limits, redact logs.
- **Dependencies**: Packages B (NLP), G (plugins), F (dossier), Security hardening.

## I) Externe Datenquellen & Cyber-Feeds
- **Goal**: Integrate news APIs, social streams, MISP/OTX/Shodan connectors with periodic jobs and dashboards.
- **Current Evidence**:
  - RSS connector service normalises entries (id/title/url/published_at) with dedup, dry-run flag, exponential backoff, and Prometheus counters. 【F:services/feed-ingestor/app/main.py†L118-L308】【F:services/feed-ingestor/tests/test_rss_connector.py†L1-L180】
  - Grafana dashboard includes feed metrics; quickstart documents offline demo and feature flags. 【F:grafana/dashboards/infra-overview.json†L7-L64】【F:docs/feeds/quickstart.md†L1-L120】
- **Gaps / Risks**:
  - Only RSS implemented; integration with real search/graph stores and credential management pending.
  - Compliance/privacy assessments absent; threat-intel connectors still missing.
- **DoD Checklist**:
  - [x] Observability: Feed freshness + error metrics. 【F:services/feed-ingestor/app/main.py†L118-L289】
  - [x] Tests: Connector smoke tests with mocked providers. 【F:services/feed-ingestor/tests/test_rss_connector.py†L1-L200】
  - [x] Docs: Source configuration guide + stability notes. 【F:docs/feeds/quickstart.md†L1-L120】
  - [ ] Security: Egress policy compliance, credential rotation.
- **Dependencies**: Packages D (workflows), J (observability), Security hardening.

## J) Performance & Infra
- **Goal**: Caching, async queues, scaling docs (gateway/load balancing), timeouts/retries everywhere, observability dashboards + alerts.
- **Current Evidence**:
  - Cache-manager + performance-monitor services exist. 【F:services/cache-manager/main.py†L670-L740】【F:services/performance-monitor/app_v1.py†L1-L120】
  - Gateway enforces rate limits and metrics. 【F:services/gateway/index.ts†L1-L120】
  - Observability compose includes Prometheus/Grafana/Loki/Tempo. 【F:inventory/services.json†L266-L289】
  - **J1 Baseline – done**: `inventory/observability.json` + `scripts/check_observability_baseline.py` sichern `/healthz`/`/readyz`/`/metrics` mit Standard-Labels über alle App-Services; CI-Job „Observability Baseline“ läuft in `ci.yml`. 【F:inventory/observability.json†L1-L240】【F:scripts/check_observability_baseline.py†L1-L85】【F:.github/workflows/ci.yml†L1-L160】
  - **J2 Trace & Log Correlation – done**: Gateway propagiert W3C-Trace-Header outbound, strukturiert Logs mit `trace_id`/`span_id`, stellt `/demo/trace` Smoke-Route bereit und die API-SLO-Dashboard ergänzt Tempo-Panels für Trace-Latenz & Top-Endpunkte. 【F:services/gateway/app/app.py†L1-L220】【F:grafana/dashboards/api-slo.json†L1-L80】【F:docs/dev/observability.md†L1-L220】
  - **J3 SLOs & Alerts – done**: Grafana visualisiert Availability/Latency/Error-SLIs je Kernservice; Prometheus-Alerts überwachen Burn-Rates (1h/6h) sowie P95-Latenzschwellen mit dokumentierten Pushgateway-Fake-Series. 【F:grafana/dashboards/api-slo.json†L1-L200】【F:monitoring/alerts/performance-alerts.yml†L1-L200】【F:docs/dev/slo.md†L1-L200】
- **Gaps / Risks**:
  - Metrics missing for 37 services; long-tail services lack SLO coverage beyond the four core APIs. 【F:inventory/findings.md†L1-L69】
  - Queue/backpressure not configured; scaling docs outdated.
- **DoD Checklist**:
  - [x] Observability: Unified dashboards + alert SLOs.
  - [ ] Tests: Load/latency benchmarks with documented results.
  - [ ] Docs: Scaling runbook + retry/timeout matrix.
  - [ ] Security: Pen-test checklists for infra components.
- **Dependencies**: Packages A–I (all rely on infra), Hardening, Release.

## K) Frontend & UX
- **Goal**: Settings (OIDC/OAuth2), live indicators via WebSockets, dossier template picker, responsiveness, performance (lazy load, PWA fallback).
- **Current Evidence**:
  - Frontend exposes settings pages and feature toggles. 【F:inventory/frontend.json†L150-L210】【F:apps/frontend/src/lib/config.ts†L1-L80】
  - Components for collaboration, maps, analytics present. 【F:apps/frontend/src/components/collaboration/CollaborationBoard.tsx†L1-L120】
- **Gaps / Risks**:
  - Live indicators rely on placeholders; login flow not connected to OIDC; PWA fallback absent.
  - Performance metrics not tracked (no LCP/TTI instrumentation).
- **DoD Checklist**:
  - [ ] Observability: Frontend performance metrics + error logging.
  - [ ] Tests: Playwright E2E for critical flows.
  - [ ] Docs: UX walkthrough with screenshots/GIFs.
  - [ ] Security: OIDC integration + CSRF hardening.
- **Dependencies**: Packages F, H, Auth package.

## L) Doku & Tests
- **Goal**: Synchronised docs (architecture, API inventory, ports policy, how-tos), E2E scenarios, CI gates (lint/type/test/e2e), changelog + migrations.
- **Current Evidence**:
  - Docs exist but outdated; new inventory artefacts generated. 【F:docs/API_INVENTORY.md†L1-L80】【F:inventory/services.json†L1-L392】
  - Test suites present across services (e.g. search-api tests). 【F:services/search-api/tests/test_metrics.py†L1-L120】
  - Release script scaffolding available. 【F:scripts/release.sh†L1-L80】
- **Gaps / Risks**:
  - Docs diverge from code; CI coverage unknown; migrations undocumented.
- **DoD Checklist**:
  - [ ] Observability: CI dashboards + test coverage reports.
  - [ ] Tests: Ensure all packages have unit/integration/E2E coverage.
  - [ ] Docs: Update core docs per DOCS_DIFF, maintain changelog.
  - [ ] Security: Document privacy/egress policies in docs.
- **Dependencies**: All packages; Release readiness.

## Hardening (Phase 3)
- **Goal**: Threat modelling, pen-test checklist, recovery/backups, egress/incognito compliance.
- **Evidence**:
  - OPA policies and tests exist under `policy/`. 【F:policy/README.md†L1-L80】【F:policy/tests/rbac_test.rego†L1-L80】
  - Egress gateway supports proxy rotation endpoints. 【F:services/egress-gateway/app.py†L120-L210】
- **Gaps**:
  - Threat model doc missing; no automated backup verification scripts.
- **DoD Checklist**:
  - [ ] Security reviews completed with tracked findings.
  - [ ] Recovery runbooks and tested backups.
  - [ ] Incognito/egress policies enforced across agents/plugins.
- **Dependencies**: Packages G, H, I, J.

## Release (Phase 4)
- **Goal**: Versioning, release notes, demo datasets/flows, install guides (dev/demo/prod), reproducible from-scratch instructions.
- **Evidence**:
  - `scripts/release.sh` scaffolds tagging + GitHub releases. 【F:scripts/release.sh†L1-L80】
  - `cli/it_cli/root.py` provides automation for compose lifecycle. 【F:cli/it_cli/root.py†L1-L80】
- **Gaps**:
  - Demo datasets + flow exports missing; install guides outdated; no verified from-scratch runbook.
- **DoD Checklist**:
  - [ ] Release notes referencing all packages and migration steps.
  - [ ] Demo assets (datasets, NiFi/n8n/Flowise templates) stored under version control.
  - [ ] Install guides for dev/demo/prod validated.
  - [ ] CI green for lint/type/test/e2e at release tag.
- **Dependencies**: Completion of packages A–L, Hardening tasks.

