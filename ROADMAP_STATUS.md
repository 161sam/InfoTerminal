# 🗺️ ROADMAP_STATUS – Phase 2 Kick-off (2025-09-23)

The Phase 2–4 roadmap is organized into subsystem packages A–L plus Hardening and Release. Each section summarises the target state, current implementation evidence, gaps, Definition of Done (DoD), and dependencies.

> 📌 **Wave ordering reference:** [`backlog/phase2/PACKAGE_SEQUENCE.yaml`](backlog/phase2/PACKAGE_SEQUENCE.yaml) feeds dashboards and checklists for the active wave limit (max two concurrent packages).

## A) Ontologie & Graph
- **Goal**: Complete ontology coverage, graph analytics APIs (degree, betweenness, communities, shortest paths), dossier export hooks, and geo-enabled subgraph views.
- **Current Evidence**:
  - Graph algorithms implemented in `services/graph-api/analytics.py` (degree, betweenness, Louvain). 【F:services/graph-api/analytics.py†L1-L120】
  - Geospatial helpers and Nominatim integration in `services/graph-api/geospatial.py`. 【F:services/graph-api/geospatial.py†L1-L120】
  - Graph-views service exposes configurable metrics and feature flags. 【F:inventory/services.json†L227-L266】
- **Gaps / Risks**:
  - Frontend graph explorer still targets hard-coded localhost endpoints, bypassing gateway routing. 【F:apps/frontend/src/components/graph/GraphExplorer.tsx†L1-L92】
  - Dossier APIs not yet wired to graph exports; no automated validation of ontology constraints. 【F:services/graph-views/dossier/api.py†L1-L120】
- **DoD Checklist**:
  - [ ] Observability: `/metrics`, `/healthz`, `/readyz` with graph-specific dashboards.
  - [ ] Tests: Integration tests covering analytics endpoints and ontology validators.
  - [ ] Docs: Updated ontology reference + sample queries in `docs/`.
  - [ ] Security: Gateway + OPA policies guarding graph export endpoints.
- **Dependencies**: Package C (Geospatial map overlays), Package F (Dossier integration).

## B) NLP & KI-Layer
- **Goal**: Stable summarisation, relation extraction, entity linking with confidence reporting, and feedback loops for active learning.
- **Current Evidence**:
  - Doc-entities router provides NER, relations, fuzzy matching, and graph write hooks. 【F:services/doc-entities/routers/doc_entities_v1.py†L1-L120】
  - Verification service exposes standardized FastAPI v1 endpoints with Prometheus middleware. 【F:services/verification/app_v1.py†L1-L120】
  - Inventory lists supporting services (doc-entities, verification, rag-api) with health/ready endpoints. 【F:inventory/services.json†L161-L205】
- **Gaps / Risks**:
  - Summaries and dossier exports rely on synchronous mocks; no persistence for active-learning feedback. 【F:apps/frontend/pages/dossier.tsx†L60-L120】
  - Entity linking stats absent; evaluation datasets not tracked.
- **DoD Checklist**:
  - [ ] Observability: Latency/error metrics for NER, summarisation, linking pipelines.
  - [ ] Tests: Gold-sample regression tests for NER, relations, linking precision/recall.
  - [ ] Docs: API contracts + sample payloads in `docs/NLP/`.
  - [ ] Security: Input size limits + audit logging for feedback endpoints.
- **Dependencies**: Package F (Dossier), Package H (Agents need NLP tooling).

## C) Geospatial-Layer
- **Goal**: Geo ingest (GeoJSON/OSM), bbox/nearby APIs, clustering/heatmaps, and frontend map overlays linked to the graph.
- **Current Evidence**:
  - Geocode, bbox, and coordinate update routines already scaffolded in `geospatial.py`. 【F:services/graph-api/geospatial.py†L1-L120】
  - Frontend contains MapLibre panel components (heatmaps, geocode marker, bounding boxes). 【F:apps/frontend/src/components/map/panels/HeatmapVisualization.tsx†L1-L120】
  - Graph-views exposes a dedicated geo router. 【F:services/graph-views/geo.py†L1-L120】
- **Gaps / Risks**:
  - No ingest automation for GeoJSON/OSM; map components not yet wired to live APIs.
  - Missing documentation on coordinate normalisation and caching.
- **DoD Checklist**:
  - [ ] Observability: Geo ingest job metrics + map tile latency dashboards.
  - [ ] Tests: API tests for bbox/nearby endpoints with sample fixtures.
  - [ ] Docs: Geospatial ingest guide + map integration walkthrough.
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
  - Media-forensics service with core + media routers. 【F:services/media-forensics/routers/media_forensics_v1.py†L1-L120】
  - Forensics service scaffolding for object detection. 【F:services/forensics/app_v1.py†L1-L120】
  - Verification frontend pages for media forensics dashboards. 【F:apps/frontend/pages/verification/media-forensics.tsx†L1-L120】
- **Gaps / Risks**:
  - Pipeline glue (NiFi → FFmpeg) absent; no storage schema for extracted metadata.
  - Frontend views still static; no correction workflow.
- **DoD Checklist**:
  - [ ] Observability: Processing latency + queue depth metrics.
  - [ ] Tests: Integration test from sample video to graph entries.
  - [ ] Docs: Demo walkthrough + resource requirements.
  - [ ] Security: Sandbox FFmpeg execution, validate uploads.
- **Dependencies**: Packages D (workflows), F (dossier), G (plugin sandbox), H (agents for review).

## F) Dossier & Collaboration
- **Goal**: Export dossiers (PDF/MD) from search/graph context, shared notes/comments per case, audit logging.
- **Current Evidence**:
  - Graph-views dossier API stubs and templates. 【F:services/graph-views/dossier/api.py†L1-L120】
  - Frontend dossier builder with modular panels. 【F:apps/frontend/pages/dossier.tsx†L1-L160】
  - Collab-hub service managing tasks and websocket updates. 【F:services/collab-hub/app/main.py†L1-L120】
- **Gaps / Risks**:
  - Dossier exports mock data; collab-hub lacks metrics and audit persistence.
  - Audit logging not integrated with Loki/Tempo.
- **DoD Checklist**:
  - [ ] Observability: Metrics for dossier exports and collaboration events.
  - [ ] Tests: E2E flow from search selection to dossier PDF.
  - [ ] Docs: Collaboration how-to + template catalogue.
  - [ ] Security: Access controls per case + audit trail ingestion.
- **Dependencies**: Packages A/B (data sources), J (observability), Release.

## G) Plugin-Architektur (Kali-Tools)
- **Goal**: Plugin registry + sandbox runner (timeouts, resource controls), example plugins (nmap, whois) integrated with workflows and search ingest.
- **Current Evidence**:
  - Plugin-runner FastAPI service with registry loader. 【F:services/plugin-runner/app_v1.py†L1-L120】
  - Example plugin manifests (nmap, whois) in `plugins/`. 【F:plugins/nmap/manifest.yaml†L1-L80】
  - Agent-connector exposes plugin orchestration endpoints. 【F:inventory/apis.json†L1-L40】
- **Gaps / Risks**:
  - Sandbox isolation + resource caps not enforced; security review pending.
  - No automated ingest of plugin outputs into search/graph.
- **DoD Checklist**:
  - [ ] Observability: Plugin execution metrics + audit logs.
  - [ ] Tests: Smoke tests per plugin, failure-path coverage.
  - [ ] Docs: Plugin authoring guide + registry schema.
  - [ ] Security: Timeouts, input validation, container isolation, OPA policies.
- **Dependencies**: Packages H (agents), D (workflows), Security hardening.

## H) AI-Agenten
- **Goal**: Flowise connector, multi-agent playbooks (researcher/verifier/dossier), Assistant UI with tool panels, policy enforcement.
- **Current Evidence**:
  - Flowise connector service with agent routers and metrics. 【F:services/flowise-connector/routers/agents_v1.py†L1-L120】
  - Frontend Next.js API routes proxy agent chat/capabilities. 【F:apps/frontend/pages/api/agent/chat.ts†L1-L120】
  - Agent feature flags available via `config.ts`. 【F:apps/frontend/src/lib/config.ts†L1-L80】
- **Gaps / Risks**:
  - Multi-agent orchestration lacks persistence; policy checks not integrated with OPA.
  - No guardrails for rate limiting or audit logging.
- **DoD Checklist**:
  - [ ] Observability: Agent invocation metrics + failure alerts.
  - [ ] Tests: Scenario tests for tool chaining and fallback paths.
  - [ ] Docs: Agent playbook catalogue + policy requirements.
  - [ ] Security: OPA enforcement, rate limits, redact logs.
- **Dependencies**: Packages B (NLP), G (plugins), F (dossier), Security hardening.

## I) Externe Datenquellen & Cyber-Feeds
- **Goal**: Integrate news APIs, social streams, MISP/OTX/Shodan connectors with periodic jobs and dashboards.
- **Current Evidence**:
  - Federation proxy + open data connectors scaffolded. 【F:services/federation-proxy/app_v1.py†L1-L120】
  - Plugins directory includes external data tools (openbb, subfinder). 【F:plugins/openbb/manifest.yaml†L1-L80】
  - NiFi/n8n overlays provide ingest infrastructure. 【F:inventory/services.json†L266-L289】
- **Gaps / Risks**:
  - No active scheduling or rate-limit documentation; dashboards missing.
  - Compliance/privacy assessments absent.
- **DoD Checklist**:
  - [ ] Observability: Feed freshness + error metrics.
  - [ ] Tests: Connector smoke tests with mocked providers.
  - [ ] Docs: Source configuration guide + stability notes.
  - [ ] Security: Egress policy compliance, credential rotation.
- **Dependencies**: Packages D (workflows), J (observability), Security hardening.

## J) Performance & Infra
- **Goal**: Caching, async queues, scaling docs (gateway/load balancing), timeouts/retries everywhere, observability dashboards + alerts.
- **Current Evidence**:
  - Cache-manager + performance-monitor services exist. 【F:services/cache-manager/main.py†L670-L740】【F:services/performance-monitor/app_v1.py†L1-L120】
  - Gateway enforces rate limits and metrics. 【F:services/gateway/index.ts†L1-L120】
  - Observability compose includes Prometheus/Grafana/Loki/Tempo. 【F:inventory/services.json†L266-L289】
- **Gaps / Risks**:
  - Metrics missing for 37 services; alert definitions absent. 【F:inventory/findings.md†L1-L69】
  - Queue/backpressure not configured; scaling docs outdated.
- **DoD Checklist**:
  - [ ] Observability: Unified dashboards + alert SLOs.
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

