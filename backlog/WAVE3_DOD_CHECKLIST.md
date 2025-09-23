# Phase 2 – Wave 3 DoD Checklist

_Idempotente Übersicht für Wave 3 (Pakete G & E). Update die Häkchen sobald Inkremente landen; erneutes Ausführen bleibt stabil._

> 📋 **Wave source of truth:** [`PACKAGE_SEQUENCE.yaml`](phase2/PACKAGE_SEQUENCE.yaml) definiert aktive Pakete/Gates.

## Increment Tracking (Wave 3)

| Increment | Package | Status | Owner / Notes |
| --- | --- | --- | --- |
| G-1 | Plugins & Sandbox | ☑ done | Runner lädt YAML-Registry, validiert Parameter, erzwingt Timeouts & Metriken (`plugin_run_total`). |
| G-2 | Plugins & Sandbox | ☑ done | Async Graph/Search Ingest + Quickstart-Doku + offline Mock (`PLUGIN_TEST_MODE`). |
| E-1 | Video Pipeline | ☑ done | OpenCV-Extraktion mit `video_frames_processed_total`, Tests erzeugen Dummy-Video. |
| E-2 | Video Pipeline | ☑ done | `/v1/videos/analyze` + Graph-Ingest + Quickstart dokumentiert Feature-Flags & Demo. |

## Package G – Plugin Runner MVP

### Increment G-1 – Metrics & Registry Hardening
- [x] Plugin registry validates commands, enforces timeouts/memory/CPU per `plugin.yaml`. 【F:services/plugin-runner/registry.py†L1-L520】
- [x] Prometheus Counter/Histogramme (`plugin_run_total`, `plugin_run_failures_total`, `plugin_run_duration_seconds`) registriert und über `/metrics` exponiert. 【F:services/plugin-runner/metrics.py†L1-L27】【F:services/plugin-runner/app_v1.py†L1-L260】
- [x] Grafana Panel „Plugin Execution Rate“ aktualisiert auf neuen Counter. 【F:monitoring/grafana-dashboards/infoterminal-overview.json†L560-L620】

### Increment G-2 – Graph/Search Ingest & Docs
- [x] `_shared.clients.graph_ingest.GraphIngestClient` speichert Fallback-JSON oder postet `/v1/ingest/plugin-run`. 【F:services/_shared/clients/graph_ingest.py†L1-L120】【F:services/graph-api/app/routes/ingest.py†L1-L120】
- [x] Mockbarer nmap-Test erzeugt Graph-Artefakte (`plugin_run_*.json`). 【F:services/plugin-runner/tests/test_nmap_ingest.py†L1-L60】【F:plugins/nmap/mock_output.xml†L1-L25】
- [x] Quickstart beschreibt Registry, Feature-Flags, Metrics & Demo-Fluss. 【F:docs/plugins/quickstart.md†L1-L200】

## Package E – Video Pipeline MVP

### Increment E-1 – Frame Extraction & Metrics
- [x] `VideoPipeline` extrahiert Frames, erkennt Objekte, setzt Bounding-Boxes & Graph-Entities. 【F:services/media-forensics/video_pipeline.py†L1-L200】
- [x] `video_frames_processed_total` Counter + Grafana Panel instrumentiert. 【F:services/media-forensics/metrics.py†L1-L11】【F:monitoring/grafana-dashboards/infoterminal-overview.json†L600-L660】
- [x] Unit-Test erzeugt Dummy-Video und prüft Summary/Graph-Payload. 【F:services/media-forensics/tests/test_video_pipeline.py†L1-L60】

### Increment E-2 – API, Ingest & Docs
- [x] `/v1/videos/analyze` Feature-Flag `VIDEO_PIPELINE_ENABLED`, Upload-Validierung & Graph-Ingest. 【F:services/media-forensics/routers/media_forensics_v1.py†L1-L420】
- [x] Graph-API `/v1/ingest/video` persistiert Szenen/Objekte & toggelt `video_pipeline_enabled`. 【F:services/graph-api/app/routes/ingest.py†L1-L120】
- [x] Quickstart führt End-to-End-Demo inkl. Curl-Beispiel & Observability auf. 【F:docs/media/video_pipeline.md†L1-L160】

## Gates Verification

- [ ] Inventory aktualisiert (`scripts/generate_inventory.py`) nach Merge.
- [x] README 5-Minuten-Demo erweitert um Plugin- und Video-Fluss. 【F:README.md†L48-L120】
- [x] Wave 3 Quickstarts & STATUS/ROADMAP-Deltas gepflegt (`STATUS.md`, `ROADMAP_STATUS.md`, `DOCS_DIFF.md`). 【F:STATUS.md†L10-L80】【F:ROADMAP_STATUS.md†L71-L120】【F:DOCS_DIFF.md†L7-L16】
- [x] Tests: `pytest services/plugin-runner/tests/test_nmap_ingest.py`, `pytest services/media-forensics/tests/test_video_pipeline.py`, `pytest services/graph-api/tests/test_ingest.py` grün.
- [ ] Security Review offen (Docker Sandbox + OPA Policies folgen in Wave 4).
