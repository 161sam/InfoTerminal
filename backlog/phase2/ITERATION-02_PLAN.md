# Iteration 02 – Wave 2 Plan

_Idempotent planning sheet for Phase 2 Iteration 02. Update the status column instead of duplicating entries._

| Package | Deliverable | Status | Notes |
| --- | --- | --- | --- |
| B (NLP & Resolver) | Alias-based entity linking with resolver metrics + gold sample tests | ✅ | `services/doc-entities/resolver.py`, `metrics.py` (`doc_entities_linking_status_total`), `tests/test_resolver_gold.py` |
| B (NLP & Resolver) | Frontend badges & metadata surfacing for resolved/unmatched entities | ✅ | `apps/frontend/src/components/docs/DocumentDetail.tsx`, `EntityBadge.tsx` |
| C (Geospatial Layer) | `/geo` bbox/nearby queries + Prometheus counters + unit tests | ✅ | `services/graph-api/app/routes/geospatial.py`, `tests/test_geospatial.py`, `metrics.py` (`geo_query_count`) |
| C (Geospatial Layer) | README demo & Grafana panels for geo query flow | ✅ | `README.md`, `monitoring/grafana-dashboards/infoterminal-overview.json` |
| Cross-cutting | Wave 2 DoD checklist, status artefacts, docs | ✅ | `backlog/phase2/WAVE2_DOD_CHECKLIST.md`, `STATUS.md`, `ROADMAP_STATUS.md` |

> Next steps: schedule Architecture/Observability review (per DoD), verify CI smoke gates remain green, then prepare Wave 3 kickoff once review findings are captured.
