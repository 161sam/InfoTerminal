# Iteration 03 – Wave 3 Plan

_Idempotent planning sheet for Phase 2 Iteration 03. Update the status column instead of duplicating entries._

| Package | Deliverable | Status | Notes |
| --- | --- | --- | --- |
| G (Plugins & Sandbox) | Prometheus metrics (`plugin_run_*`), timeout enforcement, mockable nmap workflow with Graph ingest | ✅ | `services/plugin-runner/app_v1.py`, `metrics.py`, `_shared/clients/graph_ingest.py`, `tests/test_nmap_ingest.py` |
| G (Plugins & Sandbox) | Registry/Quickstart docs + README demo coverage | ✅ | `docs/plugins/quickstart.md`, `README.md` (Wave 3 section) |
| E (Video Pipeline) | OpenCV frame extraction, object detection, Prometheus counter | ✅ | `services/media-forensics/video_pipeline.py`, `metrics.py`, `tests/test_video_pipeline.py` |
| E (Video Pipeline) | `/v1/videos/analyze` endpoint, Graph ingest + Quickstart | ✅ | `services/media-forensics/routers/media_forensics_v1.py`, `services/graph-api/app/routes/ingest.py`, `docs/media/video_pipeline.md` |
| Cross-cutting | Wave 3 DoD checklist, STATUS/ROADMAP updates, Grafana panels | ✅ | `backlog/WAVE3_DOD_CHECKLIST.md`, `STATUS.md`, `ROADMAP_STATUS.md`, `monitoring/grafana-dashboards/infoterminal-overview.json` |

> Next steps: schedule targeted security review (Docker sandbox / FFmpeg) and prepare Wave 4 scope (Agents & External feeds) once observability smoke checks stay green.
