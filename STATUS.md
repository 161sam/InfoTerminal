# 📊 InfoTerminal Phase 2 Kick-off Status

_Last update: 2025-09-23 – generated after running `scripts/generate_inventory.py`._

> ℹ️ **Wave tracker:** `backlog/phase2/PACKAGE_SEQUENCE.yaml` lists the active packages and gates for Phase 2.

## Executive Summary (Ampel)
- **Implementierungsgrad – 🟡**: 52 runtime-relevant services detected; core APIs (search, graph, doc-entities, verification) expose v1 contracts, but frontend workflows, ingest orchestration, and collaboration stacks remain partially stubbed. 【F:inventory/services.json†L1-L266】
- **Docs-Konsistenz – 🔴**: Historic inventories and roadmap notes lag behind current service surface; key docs (API inventory, roadmap intelligence) omit newer connectors and overlays. See [DOCS_DIFF.md](DOCS_DIFF.md) for prioritized deltas.
- **Observability-Abdeckung – 🔴**: 29 services lack `/healthz`, 31 miss `/readyz`, and 37 have no `/metrics`, leaving alerting coverage incomplete. 【F:inventory/findings.md†L1-L69】
- **Security-Reife – 🟡**: Auth-service, gateway, and OPA scaffolding exist, yet proxy hardening, plugin isolation, and geospatial data egress reviews are pending consolidation (rows below).
- **Release-Risiko – 🔴**: Without synchronized docs, backlog issues, or verified ingest-to-dossier flows, v1.0 cannot be certified; alignment tracked in [ROADMAP_STATUS.md](ROADMAP_STATUS.md) and [backlog/README.md](backlog/README.md).
- **Phase 2 Aktivierung – 🟡**: Wave 1 (Packages A & F) running per [`PACKAGE_SEQUENCE.yaml`](backlog/phase2/PACKAGE_SEQUENCE.yaml); later waves remain queued until gates stay green across consecutive runs.

> Baseline artefacts: **STATUS.md**, **DOCS_DIFF.md**, **ROADMAP_STATUS.md**, and the structured epics in **backlog/README.md**.

## Subsystem Matrix

| Scope | Implementiert | Belege (Dateien/Endpunkte) | Lücken / Blocker | Nächste Schritte (Roadmap-Paket) |
| --- | --- | --- | --- | --- |
| **Frontend (Next.js)** | Teil | 30 pages, 59 API routes, 26 feature flags enumerated via `inventory/frontend.json`; Graph UI and Dossier panels present in `apps/frontend/src`. 【F:inventory/frontend.json†L1-L210】【F:apps/frontend/src/components/graph/GraphExplorer.tsx†L1-L92】【F:apps/frontend/pages/dossier.tsx†L1-L120】 | Graph explorer hard-codes localhost APIs (bypassing config), dossier builder mocks exports, and feature toggles lack runtime docs. | Align FE data access with gateway configs, wire dossier exports + agent hooks (Packages C, F, H). |
| **Search (search-api)** | Ja | FastAPI v1 app with health/ready/metrics and extensive tests. 【F:inventory/services.json†L205-L226】【F:services/search-api/src/search_api/app/main_v1.py†L1-L120】【F:services/search-api/tests/test_metrics.py†L1-L120】 | OPA rules exist but enforcement coverage across gateways/frontends not yet validated; search UI uses fallback endpoints. | Harden authz path & propagate observability dashboards (Packages B, J, L). |
| **Graph & Ontologie (graph-api, graph-views)** | Teil | Graph algorithms + geospatial helpers implemented; graph-views exposes metrics/feature flags. 【F:services/graph-api/analytics.py†L1-L120】【F:services/graph-api/geospatial.py†L1-L120】【F:inventory/services.json†L227-L266】 | Frontend graph explorer bypasses gateway, dossiers not yet consuming graph subviews, export endpoints untested. | Finish ontology validation, connect dossier hooks, geo map integration (Packages A, C, F). |
| **Doc-Entities / NLP** | Teil | Service handles NER, relations, fuzzy matching, DB persistence with optional graph writes. 【F:inventory/services.json†L161-L184】【F:services/doc-entities/routers/doc_entities_v1.py†L1-L120】 | Summaries and relation exports rely on synchronous mocks; active-learning feedback APIs missing storage. | Finalize relation graph syncing, add evaluation datasets + feedback endpoints (Package B). |
| **Verification & Media Forensics** | Teil | Verification FastAPI app with Prometheus middleware; media-forensics service exposing core + media routers. 【F:inventory/services.json†L289-L329】【F:services/verification/app_v1.py†L1-L120】【F:services/media-forensics/routers/media_forensics_v1.py†L1-L120】 | Legacy endpoints still active, media pipeline lacks NiFi/FFmpeg orchestration, FE verification views stub analytics. | Build end-to-end video ingest + verification dashboard (Packages E, B). |
| **Flowise Connector / Agent Hub** | Teil | Flowise connector service with agent routers and metrics, plus frontend API routes for agent chat. 【F:inventory/services.json†L330-L352】【F:services/flowise-connector/routers/agents_v1.py†L1-L120】【F:inventory/frontend.json†L1-L120】 | Tool registries not policy-bound; multi-agent orchestration lacks persistence and rate-limit governance. | Formalize agent policy contracts, add audit trails & Flowise playbooks (Package H). |
| **NiFi / n8n / Workflows** | Teil | Compose overlays for NiFi & n8n, sample playbooks (`apps/n8n/*.json`). 【F:inventory/services.json†L266-L289】【F:apps/n8n/fact-checking-assistant-v2.json†L1-L80】 | No reproducible import scripts, retry/backoff configs undocumented, observability of flows absent. | Automate template deployment, add DLQ/backoff handling, document runbooks (Package D). |
| **Dossier & Collaboration** | Teil | Graph-views exposes dossier API stubs; frontend dossier page modularized. 【F:services/graph-views/dossier/api.py†L1-L120】【F:apps/frontend/pages/dossier.tsx†L1-L160】 | Export endpoints mock responses; collab-hub lacks metrics/readyz and UI relies on placeholder data. | Implement export pipeline + shared notes persistence, connect audit logging (Package F). |
| **Plugins & Sandbox Runner** | Teil | Plugin-runner FastAPI app, plugin registry YAMLs under `/plugins`. 【F:inventory/services.json†L353-L392】【F:services/plugin-runner/app_v1.py†L1-L120】【F:plugins/nmap/manifest.yaml†L1-L80】 | Sandbox/resource controls unfinished; plugin security review + CLI integration pending. | Finalize plugin isolation, add OPA/timeout guards, publish orchestration docs (Package G). |
| **Ops & Egress Controls** | Teil | Egress gateway, ops-controller, and policy bundles present with compose wiring. 【F:inventory/services.json†L184-L205】【F:services/egress-gateway/app.py†L120-L210】【F:services/ops-controller/app/main.py†L1-L120】 | Health endpoints missing on infra services; proxy rotation logic lacks audit hooks; ops-controller ports duplicated in compose. | Harden egress auditing, unify observability, document rotation flows (Packages J, Security). |
| **Auth / RBAC / OPA** | Teil | Auth-service exposes full v1 scope, gateway proxies search/graph/views, policy bundles under `policy/`. 【F:inventory/services.json†L184-L205】【F:services/auth-service/src/auth_service/app_v1.py†L360-L760】【F:services/gateway/index.ts†L1-L120】 | Keycloak/SSO compose overlays exist but integration tests absent; FE login still stubbed in several pages. | Complete OIDC wiring in FE, add OPA regression tests, document RBAC roles (Packages J, K). |
| **Observability Stack** | Teil | Observability compose exposes Prometheus/Grafana/Loki/Tempo, but many services miss probes. 【F:inventory/services.json†L266-L289】【F:inventory/findings.md†L1-L69】 | Metrics absent for 37 services; alert thresholds undefined; logs/traces integration inconsistent. | Enforce observability DoD across services, ship Grafana dashboards + alert rules (Packages J, L). |
| **Infra / Compose / Envs** | Teil | 12 compose overlays + policy-specific files; CLI supports profile selection. 【F:inventory/services.json†L1-L392】【F:docker-compose.graph-views.yml†L1-L120】【F:cli/it_cli/root.py†L1-L80】 | Port policy drift (duplicates, host defaults exposed), `.env.example` coverage incomplete. | Normalize compose ports via inventory, document start/stop matrices (Packages J, Release). |
| **CLI & Tooling** | Teil | Typer-based CLI manages compose lifecycle, plugin scaffolding, and status reporting. 【F:cli/it_cli/root.py†L1-L120】【F:cli/it_cli/commands/status.py†L1-L160】 | CLI lacks inventory integration; tests not covering new commands; packaging instructions outdated. | Extend CLI to surface inventory and observability checks (Packages L, Release). |
| **Docs & Knowledge Base** | Nein | Legacy API inventory, empty roadmap intelligence, outdated port policy. 【F:docs/API_INVENTORY.md†L1-L80】【F:docs/ROADMAP-INTELLIGENCE.md†L1-L2】【F:docs/PORTS_POLICY.md†L1-L20】 | Docs diverge from code; no single baseline for backlog or release gating. | Execute DOCS_DIFF remediation, align docs with new inventory artefacts (Packages L, Release). |

## Observability Snapshot
- Missing health probes: 29 services; missing ready probes: 31; missing metrics: 37. 【F:inventory/findings.md†L1-L69】
- Compose overlays expose Prometheus/Grafana/Loki/Tempo on host ports 3412–3416. 【F:inventory/services.json†L266-L289】

## Inventory Highlights
- Services inventory stored in `inventory/services.json`; API discovery in `inventory/apis.json`; database artefacts aggregated in `inventory/db.json`; frontend surface captured in `inventory/frontend.json`. 【F:inventory/services.json†L1-L392】【F:inventory/apis.json†L1-L20】【F:inventory/db.json†L1-L40】【F:inventory/frontend.json†L1-L210】
- Findings summary for missing probes/metrics resides in `inventory/findings.md`. 【F:inventory/findings.md†L1-L69】

## Traceability
- Detailed roadmap/package mapping: [ROADMAP_STATUS.md](ROADMAP_STATUS.md)
- Prioritized documentation fixes: [DOCS_DIFF.md](DOCS_DIFF.md)
- Issue backlog (epics & sub-issues): [backlog/README.md](backlog/README.md)
