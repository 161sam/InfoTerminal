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
- [ ] Confirm `/graphs/analysis/degree`, `/graphs/analysis/communities`, `/graphs/analysis/shortest-path` enforce pagination, timeout guards, and increment Prometheus counters (`graph_analysis_queries_total`, `graph_analysis_duration_seconds`).
- [ ] Add smoke coverage hitting each endpoint with fixture graph (`pytest -k analysis` in `services/graph-api`).

#### Increment A-2 – Dossier Hook Export
- [ ] Implement `/graphs/analysis/subgraph-export` returning JSON + Markdown block.
- [ ] Provide CLI snippet (`cli it graph export --case-id ...`) and document parameter expectations for dossier pipeline.

#### Increment A-3 – Superset & Grafana Assets
- [ ] Create Superset dataset + charts under `apps/superset/assets/graph_analytics_mvp/*` and dashboard export `apps/superset/assets/dashboard/graph_analytics_mvp.json` (imported via `apps/superset/assets/scripts/import.sh`).
- [ ] Add Grafana dashboard JSON `grafana/dashboards/graph-analytics-mvp.json` with panels for centrality histogram & community count; link in README demo.
- [ ] Update API docs with curl examples, pagination hints, metrics references.

**Definition of Done (Package A, Wave 1)**
- [ ] Analytics endpoints covered by unit/integration tests and smoke script.
- [ ] `/metrics` exposes counters + histograms with labels (`algorithm`, `status`).
- [ ] Superset + Grafana artefacts stored in repo and referenced in README demo script.
- [ ] CLI + docs provide example queries and export instructions.

### Package F – Dossier & Collaboration (MVP scope)

**Goal:** Ship Dossier-Lite exports (Markdown + PDF) from search/graph triggers and enable shared notes with audit logging.

#### Increment F-1 – Dossier Export Service
- [ ] Implement `/dossier/export` generating MD/PDF via templating (support `source=search|graph`).
- [ ] Add CLI command + integration test using fixture data; publish sample exports under `examples/dossier/`.

#### Increment F-2 – Notes & Metrics MVP
- [ ] Enable feature-flagged notes endpoint for case-based notes with audit log emission (Loki-compatible JSON lines) and ensure feature flag defaults to `false`.
- [ ] Emit `dossier_exports_total`, `dossier_export_duration_seconds`, `collab_notes_total` metrics and surface via `/metrics`.
- [ ] Update Grafana dashboard `graph-analytics-mvp` with dossier counters.

#### Increment F-3 – Docs, Demo & Smoke Validation
- [ ] Document export flow with Markdown/PDF samples, Superset context, and CLI examples.
- [ ] Update README demo script referencing CLI, Superset dashboard, Grafana board.
- [ ] Extend smoke script (`scripts/smoke_graph_analysis.sh` + dossier smoke script) to cover Search → Graph → Dossier export with PDF checksum.

**Definition of Done (Package F, Wave 1)**
- [ ] Export endpoint returns MD & PDF; templates stored + versioned.
- [ ] Notes API persists data with audit events logged and feature flag documented.
- [ ] Metrics available and visualised (Grafana dashboard `graph-analytics-mvp`, Superset dataset `graph_analytics_mvp`).
- [ ] Documentation updated (API, how-to, demo script) with screenshots/GIF placeholders.
- [ ] Smoke E2E demonstrates Search → Graph → Dossier path (`scripts/smoke_graph_analysis.sh`, `scripts/smoke_graph_views.sh`).

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

