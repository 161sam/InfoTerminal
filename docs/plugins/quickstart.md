# Plugin Runner Quickstart (Wave 3)

Wave 3 expands the sandbox runner with a registry-driven execution flow, deterministic test fixtures, and graph/search ingest. This guide walks through the nmap reference plugin, explains feature flags, metrics, and the offline-friendly workflow used in CI.

## 1. Prerequisites

1. Ensure the plugin runner service is up (Docker profile `plugin-runner` or `make services/plugin-runner`).
2. Set the following environment variables when running locally:
   ```bash
   export PLUGINS_DIR="$(pwd)/plugins"
   export RESULTS_DIR="$(pwd)/tmp/plugin-results"
   export PLUGIN_TEST_MODE=1            # use mock outputs for deterministic runs
   export IT_ENABLE_METRICS=1           # expose /metrics via Prometheus middleware
   export GRAPH_INGEST_FALLBACK_DIR="$(pwd)/tmp/graph-ingest"
   ```
3. Optional: point `GRAPH_API_URL` and `SEARCH_API_URL` to live services; otherwise results are written to `RESULTS_DIR/graph_ingest/`.

## 2. Registry Layout & Security Defaults

Each plugin lives under `plugins/<name>/plugin.yaml`. Important fields:

- `command_templates`: maps scan types to commands. The runner enforces timeouts, CPU and memory limits from the `security` block. If a requested template is missing, the first available template is used.
- `output_parsing`: defines how raw output is parsed (e.g. `nmap_xml_parser`).
- `integration.graph_entities` & `integration.search_indexing`: describe how results are turned into graph nodes/documents.
- `security.timeout`, `security.memory_limit`, `security.cpu_limit`: enforced for every run (high-risk plugins must use the Docker sandbox).

The runner validates incoming parameters (`type`, `choices`, regex patterns) before a job is queued. High-risk plugins cannot be executed locally and require Docker.

## 3. Executing the nmap Reference Plugin

1. Queue a job via HTTP:
   ```bash
   curl -X POST http://localhost:8621/v1/plugins/nmap/execute \
     -H 'Content-Type: application/json' \
     -d '{
       "parameters": {"target": "scan.example", "scan_type": "basic"},
       "output_format": "json"
     }'
   ```
   The response returns a `job_id` with status `queued`.
2. Poll job status (the background worker consumes the queue):
   ```bash
   curl http://localhost:8621/v1/jobs/<job_id>
   ```
   When `PLUGIN_TEST_MODE=1` the runner loads `plugins/nmap/mock_output.xml`, parses it, and marks the job `completed`.
3. Inspect persisted artefacts under `${RESULTS_DIR}`. Parsed graph/search payloads are embedded in the job response (`graph_entities`, `search_documents`) and mirrored as JSON in `results/<job_id>.json`.

## 4. Graph/Search Ingest

- Successful runs trigger an async ingest via `_shared.clients.graph_ingest.GraphIngestClient`.
- If `GRAPH_API_URL` is unset, payloads are saved locally (`plugin_run_<job>.json`) so demos/tests stay offline-friendly.
- Graph API exposes `/v1/ingest/plugin-run` which appends the artefacts to `app.state.plugin_runs` and toggles `video_pipeline_enabled` when video data arrives. 【F:services/graph-api/app/routes/ingest.py†L1-L120】

## 5. Observability

- `/metrics` now exposes:
  - `plugin_run_total{plugin="nmap"}` — total executions per plugin.
  - `plugin_run_failures_total{plugin="nmap"}` — failed runs.
  - `plugin_run_duration_seconds{plugin="nmap"}` — histogram of execution time.
- Grafana dashboard “Plugin Execution Rate” queries `rate(plugin_run_total[5m])` and `Video Frames Processed Rate` visualises the media pipeline. 【F:monitoring/grafana-dashboards/infoterminal-overview.json†L560-L660】

## 6. Testing & CI Hooks

- `services/plugin-runner/tests/test_nmap_ingest.py` runs the mock nmap flow end-to-end, asserting graph ingest artefacts are produced. 【F:services/plugin-runner/tests/test_nmap_ingest.py†L1-L60】
- Wave 3 ensures offline determinism: no Docker execution is required during tests because `PLUGIN_TEST_MODE` loads the bundled mock XML.

## 7. Next Steps

- Harden Docker sandboxing with OPA policies and extended audit logs.
- Add more Kali-style plugins following the same registry schema (whois, subfinder already ship similar manifests).
- Integrate CLI helpers (`it plugin run`) with the new `/v1/plugins/...` endpoints.
