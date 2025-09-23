# Phase 2 – Wave 1 DoD Checklist

_This checklist is idempotent: rerun after each merge to confirm gates remain green. Update issue references when tasks close._

> 📋 **Wave source of truth:** See [`PACKAGE_SEQUENCE.yaml`](PACKAGE_SEQUENCE.yaml) for the authoritative ordering,
> gates, and dependencies powering this checklist.

## Package A – Ontologie & Graph (MVP)

- [ ] `/graphs/analysis/degree` endpoint paginates + enforces timeout guardrails (pytest coverage `services/graph-api/tests/analysis/test_degree.py`).
- [ ] `/graphs/analysis/communities` exposes Louvain output with `community_id` column and Prometheus counters `graph_analysis_queries_total{algorithm="louvain"}`.
- [ ] `/graphs/analysis/shortest-path` returns deterministic fixture path ≤ configured hop limit and reports duration histogram (`graph_analysis_duration_seconds_bucket`).
- [ ] Subgraph export endpoint (`/graphs/analysis/subgraph-export`) streams JSON + Markdown payload, increments `graph_subgraph_exports_total`.
- [ ] Superset dashboard `graph_analytics_mvp` deployed via `apps/superset/assets/scripts/import.sh` and linked from README demo.
- [ ] Grafana dashboard `graph-analytics-mvp.json` imported to observability stack.
- [ ] Smoke E2E (`test_infoterminal_v030_features.sh --suite graph-dossier`) validates query → export flow.

## Package F – Dossier & Collaboration (MVP)

- [ ] `/dossier/export` generates Markdown and PDF artefacts using templates in `examples/dossier/` (checksum verified in smoke test).
- [ ] Feature-flagged notes endpoint persists case-based notes with audit entries routed to Loki (`logs/collab-notes.log`).
- [ ] Metrics exposed: `dossier_exports_total`, `dossier_export_duration_seconds_bucket`, `collab_notes_total`.
- [ ] Superset dataset `graph_analytics_mvp` provides dossier-ready analytics context (centrality histogram + community count).
- [ ] Grafana stat panel reflects dossier export counters on the `graph-analytics-mvp` dashboard.
- [ ] README demo script documents Search → Graph → Dossier export walkthrough.
- [ ] Architecture/Observability review notes captured in `reports/architecture/phase2-wave1.md` post-completion.

## Gates Verification

- [ ] `scripts/generate_inventory.py` run post-merge (Inventory/Policy gate).
- [ ] `/metrics`, `/healthz`, `/readyz` endpoints verified via `scripts/check_gates.sh` (Health gate).
- [ ] Docs regenerated where inventories changed (API/Docs gate).
- [ ] Smoke E2E suite green in CI (`test_infoterminal_v030_features.sh`).
