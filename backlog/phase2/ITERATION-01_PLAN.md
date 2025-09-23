# Phase 2 – Iteration 01 Execution Plan

_Start date: 2025-09-23_

This document captures the risk-reducing kick-off for Phase 2. It is idempotent: rerunning the associated checklists regenerates
status dashboards and revalidates gates without duplicating artefacts.

## Objectives

1. Establish a **prioritised sequence for packages A–L** that respects dependencies, value, and risk mitigation.
2. Activate the first MVP wave (**Packages A & F**) with lightweight, verifiable increments.
3. Ensure all work preserves the four delivery gates (Inventory/Policy, Health-Ready-Metrics, API/Docs, Smoke-E2E) with
   progress tracked in [`WAVE1_DOD_CHECKLIST.md`](WAVE1_DOD_CHECKLIST.md).

## Prioritised Package Order (Phase 2 Waves)

> ℹ️ **Machine-readable source:** [`PACKAGE_SEQUENCE.yaml`](PACKAGE_SEQUENCE.yaml) captures the same wave ordering with
> value, risk, dependencies, and gate metadata. Regenerate dashboards/checklists from that file to keep reruns idempotent.

| Wave | Active Packages (max 2) | Value & Risk Rationale |
| --- | --- | --- |
| Wave 1 (current) | **A – Ontologie & Graph**, **F – Dossier & Collaboration** | Unlocks graph analytics + dossier exports to prove end-to-end value. F depends on A’s subgraph export hook. Enables demo flow (Search → Graph → Dossier). |
| Wave 2 | **B – NLP & Resolver**, **C – Geospatial** | Builds on graph hooks from Wave 1. Relation extraction + entity linking feeds dossier context, while geospatial overlays consume graph node metadata. Running together keeps review load manageable while covering complementary data enrichments. |
| Wave 3 | **G – Plugins**, **D – Daten-Ingest & Workflows** | With core analytics stable, harden plugin runner (nmap example) and integrate ingest automation. Plugin outputs feed ingest/search; NiFi/n8n automation depends on dossier + graph exports from earlier waves. |
| Wave 4 | **H – AI-Agenten**, **I – Externe Feeds** | Agent orchestration requires NLP + plugin results; feed connectors rely on ingest tooling. Sequencing limits blast radius by building atop established observability. |
| Wave 5 | **J – Performance & Infra**, **K – Frontend & UX** | Optimise infra and UX once functional features land, ensuring instrumentation and OIDC integration leverage earlier packages. |
| Wave 6 | **L – Doku & Tests**, **Hardening**, **Release** | Final consolidation after feature waves to update docs, execute hardening, and prepare release playbooks. |

> ✅ **Check**: After each wave completes, rerun `scripts/generate_inventory.py`, Grafana dashboard exports, and smoke E2E scripts to ensure gates stay green before starting the next wave.

## Wave 1 Detailed Plan (Packages A & F)

### Increment Breakdown (risk-reducing, idempotent)

| Increment | Package | Focus | Dependencies | Completion Evidence |
| --- | --- | --- | --- | --- |
| **A-1** | A | Harden `/graphs/analysis/*` endpoints (pagination, timeouts, metrics) + smoke tests | Seed graph fixtures | Pytest module `services/graph-api/tests/test_analysis_routes.py`, Prometheus counters exposed |
| **A-2** | A | Dossier subgraph export + CLI hook | Increment A-1 | Endpoint `/graphs/analysis/subgraph-export`, CLI snippet documented |
| **A-3** | A | Observability + dashboards (Superset + Grafana) | Increments A-1/A-2 | Dashboard artefacts (`apps/superset/assets/**/*graph_analytics_mvp*`, `grafana/dashboards/graph-analytics-mvp.json`) |
| **F-1** | F | `/dossier/export` Markdown/PDF service + templates | Subgraph export (A-2) | Integration test `services/collab-hub/tests/test_dossier.py`, sample exports in `examples/dossier/` |
| **F-2** | F | Notes/Comments MVP with audit logging + metrics | Feature flag scaffolding | Audit log config (`CH_AUDIT_PATH`), metrics counters, feature flag default off |
| **F-3** | F | README demo refresh, Superset/Grafana references, smoke E2E extension | Increments F-1/F-2 + A-3 | Updated README 5-minute demo, `scripts/smoke_graph_analysis.sh` and dossier smoke script |

> 🔁 **Idempotent**: Each increment regenerates artefacts in place (dashboards, exports, docs) so reruns update resources without duplicating them.

### Package A – Ontologie & Graph (MVP scope)

**Goal:** Deliver analytics endpoints (degree centrality, Louvain communities, shortest path) and expose dossier-ready subgraph exports with observability + docs updates.

#### Increment A-1 – Analytics Endpoint Hardening
- [x] Confirm `/graphs/analysis/degree`, `/graphs/analysis/communities`, `/graphs/analysis/shortest-path` enforce pagination, timeout guards, and increment Prometheus counters (`graph_analysis_queries_total`, `graph_analysis_duration_seconds`). 【F:services/graph-api/app/routes/analytics.py†L28-L216】【F:services/graph-api/metrics.py†L12-L26】
- [x] Add smoke coverage hitting each endpoint with fixture graph (`pytest -k analysis` in `services/graph-api`). 【F:services/graph-api/tests/test_analysis_routes.py†L12-L106】【F:scripts/smoke_graph_analysis.sh†L1-L76】

#### Increment A-2 – Dossier Hook Export
- [x] Implement `/graphs/analysis/subgraph-export` returning JSON + Markdown block. 【F:services/graph-api/app/routes/analytics.py†L218-L308】
- [x] Provide CLI snippet (`cli it graph export --case-id ...`) and document parameter expectations for dossier pipeline. 【F:docs/api/graph-analysis.md†L1-L60】【F:README.md†L63-L94】

#### Increment A-3 – Superset & Grafana Assets
- [x] Create Superset dataset + charts under `apps/superset/assets/graph_analytics_mvp/*` and dashboard export `apps/superset/assets/dashboard/graph_analytics_mvp.json` (imported via `apps/superset/assets/scripts/import.sh`). 【F:apps/superset/assets/datasets/graph_analytics_mvp.yaml†L1-L32】【F:apps/superset/assets/dashboard/graph_analytics_mvp.json†L1-L34】
- [x] Add Grafana dashboard JSON `grafana/dashboards/graph-analytics-mvp.json` with panels for centrality histogram & community count; link in README demo. 【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】【F:README.md†L63-L94】
- [x] Update API docs with curl examples, pagination hints, metrics references. 【F:docs/api/graph-analysis.md†L1-L60】

**Definition of Done (Package A, Wave 1)**
- [x] Analytics endpoints covered by unit/integration tests and smoke script. 【F:services/graph-api/tests/test_analysis_routes.py†L12-L106】【F:scripts/smoke_graph_analysis.sh†L1-L76】
- [x] `/metrics` exposes counters + histograms with labels (`algorithm`, `status`). 【F:services/graph-api/metrics.py†L12-L40】
- [x] Superset + Grafana artefacts stored in repo and referenced in README demo script. 【F:apps/superset/assets/dashboard/graph_analytics_mvp.json†L1-L34】【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】【F:README.md†L63-L94】
- [x] CLI + docs provide example queries and export instructions. 【F:docs/api/graph-analysis.md†L1-L60】【F:README.md†L63-L94】

### Package F – Dossier & Collaboration (MVP scope)

**Goal:** Ship Dossier-Lite exports (Markdown + PDF) from search/graph triggers and enable shared notes with audit logging.

#### Increment F-1 – Dossier Export Service
- [x] Implement `/dossier/export` generating MD/PDF via templating (support `source=search|graph`). 【F:services/collab-hub/app/main.py†L204-L312】【F:services/collab-hub/templates/dossier/brief.md.j2†L1-L20】
- [x] Add CLI command + integration test using fixture data; publish sample exports under `examples/dossier/`. 【F:services/collab-hub/tests/test_dossier.py†L1-L78】【F:examples/dossier/README.md†L1-L8】【F:README.md†L63-L94】

#### Increment F-2 – Notes & Metrics MVP
- [x] Enable feature-flagged notes endpoint for case-based notes with audit log emission (Loki-compatible JSON lines) and ensure feature flag defaults to `false`. 【F:services/collab-hub/app/main.py†L40-L118】【F:services/collab-hub/app/main.py†L362-L388】
- [x] Emit `dossier_exports_total`, `dossier_export_duration_seconds`, `collab_notes_total` metrics and surface via `/metrics`. 【F:services/collab-hub/app/main.py†L24-L49】【F:services/collab-hub/app/main.py†L204-L312】
- [x] Update Grafana dashboard `graph-analytics-mvp` with dossier counters. 【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】

#### Increment F-3 – Docs, Demo & Smoke Validation
- [x] Document export flow with Markdown/PDF samples, Superset context, and CLI examples. 【F:README.md†L63-L94】【F:docs/api/graph-analysis.md†L1-L60】【F:examples/dossier/README.md†L1-L8】
- [x] Update README demo script referencing CLI, Superset dashboard, Grafana board. 【F:README.md†L63-L94】
- [x] Extend smoke script (`scripts/smoke_graph_analysis.sh` + dossier smoke script) to cover Search → Graph → Dossier export with PDF checksum. 【F:scripts/smoke_graph_analysis.sh†L1-L76】【F:services/collab-hub/tests/test_dossier.py†L49-L78】

**Definition of Done (Package F, Wave 1)**
- [x] Export endpoint returns MD & PDF; templates stored + versioned. 【F:services/collab-hub/app/main.py†L204-L312】【F:services/collab-hub/templates/dossier/brief.md.j2†L1-L20】【F:examples/dossier/README.md†L1-L8】
- [x] Notes API persists data with audit events logged and feature flag documented. 【F:services/collab-hub/app/main.py†L40-L118】【F:services/collab-hub/app/main.py†L362-L388】
- [x] Metrics available and visualised (Grafana dashboard `graph-analytics-mvp`, Superset dataset `graph_analytics_mvp`). 【F:services/collab-hub/app/main.py†L24-L49】【F:grafana/dashboards/graph-analytics-mvp.json†L1-L44】【F:apps/superset/assets/datasets/graph_analytics_mvp.yaml†L1-L32】
- [x] Documentation updated (API, how-to, demo script) with screenshots/GIF placeholders. 【F:docs/api/graph-analysis.md†L1-L60】【F:README.md†L63-L94】
- [x] Smoke E2E demonstrates Search → Graph → Dossier path (`scripts/smoke_graph_analysis.sh`, `scripts/smoke_graph_views.sh`). 【F:scripts/smoke_graph_analysis.sh†L1-L76】【F:services/collab-hub/tests/test_dossier.py†L49-L78】

## Governance & Observability Checklist

- [ ] Feature flags default to **off**; toggles documented in `inventory/frontend.json` after deployment.
- [ ] `DOCS_DIFF.md` high-priority items linked to issues for packages A, F, L.
- [ ] `/metrics` additions include unit labels to support alerting.
- [ ] Update `ROADMAP_STATUS.md` and `STATUS.md` via generation scripts after each merge.
- [ ] Record findings in `reports/architecture/phase2-wave1.md` post-review (template TBD).

## Demo Script (Wave 1)

`README.md` enthält den 5-Minuten-Ablauf **Search → Graph → Dossier** (offline, idempotent):
1. `scripts/dev_up.sh graph dossier` – notwendige Services starten.
2. `scripts/fixtures/load_graph_mini.sh` – Demo-Graph laden.
3. `curl http://localhost:8612/graphs/analysis/degree?limit=10` – zentrale Metriken prüfen.
4. `curl http://localhost:8612/graphs/analysis/subgraph-export?...` – Markdown-Export erzeugen.
5. `curl http://localhost:8625/dossier/export ...` – PDF exportieren; anschließend Superset/Grafana Dashboards öffnen.

## Next Steps

- Track progress via GitHub issues labelled `pkg-A-graph` and `pkg-F-dossier`.
- Schedule 30-min Architecture/Observability review after Wave 1 DoD complete.
- Only after stable green gates → initiate Wave 2 (B + C) planning doc.

