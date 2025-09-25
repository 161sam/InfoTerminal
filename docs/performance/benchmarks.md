# Performance Benchmarks (Search, Graph, Doc-Entities, Agent)

This guide explains how to execute the new SLO-focused benchmarks that cover the four
core InfoTerminal services:

- `search-api` (`/v1/search`)
- `graph-api` (`/v1/cypher`)
- `doc-entities` (`/v1/extract/entities`)
- `agent-connector` (`/v1/plugins/registry`)

Each benchmark script provides configurable load (concurrency, number of requests),
calculates latency percentiles and throughput, and evaluates the results against
service-specific SLO targets. Artefacts are emitted as JSON and CSV under
`artifacts/perf/` and are overwritten deterministically on every run.

## Prerequisites

- Python 3.10+ (3.11 recommended)
- Optional dependency for live runs: [`httpx`](https://www.python-httpx.org/) – install
  via `pip install httpx`
- Services must be reachable on the expected ports (defaults follow the port policy:
  `8611` Search, `8612` Graph, `8613` Doc-Entities, `8633` Agent). Override the base
  URLs with the environment variables `SEARCH_API_URL`, `GRAPH_API_URL`,
  `DOC_ENTITIES_URL`, and `AGENT_CONNECTOR_URL` if you proxy through the gateway or a
different host.

> ℹ️ **Simulation & dry-run support**: Passing `--simulate` generates deterministic
> synthetic results without hitting the APIs. Passing `--dry-run` skips execution but
> still writes skeleton artefacts. Both modes are useful in CI or when developing
> locally without all services running.

## Running the benchmarks

All scripts live in `benchmarks/` and expose a `--help` flag with the available
options.

```bash
# Search API benchmark (POST /v1/search)
python benchmarks/search_bench.py --concurrency 8 --requests 120

# Graph API benchmark (POST /v1/cypher)
python benchmarks/graph_bench.py --payload-file samples/queries/cypher.json

# Doc-Entities benchmark (POST /v1/extract/entities)
python benchmarks/doc_entities_bench.py --simulate  # quick deterministic smoke run

# Agent connector benchmark (GET /v1/plugins/registry)
python benchmarks/agent_bench.py --header "Authorization: Bearer <token>"
```

Common flags:

| Flag | Description |
| --- | --- |
| `--concurrency` | Concurrent workers (default varies per service). |
| `--requests` | Total requests executed. |
| `--latency-slo-ms` | Target P95 latency in milliseconds (for SLO evaluation). |
| `--throughput-slo-rps` | Target minimum throughput (requests per second). |
| `--simulate` | Generate deterministic synthetic results (no network I/O). |
| `--dry-run` | Skip execution but emit zeroed artefacts. |
| `--output-prefix` | Filename prefix for artefacts (defaults to the service name). |

## Artefacts & interpretation

Every run produces two artefacts per service under `artifacts/perf/`:

- `<service>.json` – structured summary including configuration, metrics, SLO status,
  and (up to) the first 10 error messages.
- `<service>.csv` – single-row CSV for quick import into spreadsheets or Grafana CSV
  data sources.

Key metrics:

- `latency_ms.p95_ms` – compare to the latency SLO target.
- `throughput_rps` – compare to the throughput SLO target.
- `success_rate` – percentage of successful requests (4xx responses count as degraded,
  5xx responses as failures).

Status mapping:

- `ok` – All requests succeeded and all configured SLOs were met.
- `degraded` – Some errors occurred or one of the SLO targets was missed.
- `failed` – No successful requests were recorded.
- `skipped` – Dry run; no requests executed.

The artefacts are overwritten deterministically, which means re-running a benchmark
updates the same files instead of appending new ones. This makes it easy to version the
latest benchmark results in Git or share the folder as a short-lived snapshot.

## Automation & CI smoke

The helper script `benchmarks/perf_smoke.py` executes a reduced workload against all
four services. By default it runs in deterministic simulation mode and generates
artefacts with the suffix `_smoke`. Use `--mode live` to execute real HTTP calls once
all services are running:

```bash
python benchmarks/perf_smoke.py           # simulated smoke (default)
python benchmarks/perf_smoke.py --mode live  # live smoke benchmark
```

This script is wired into the optional CI job `perf-smoke`, providing fast regression
signals without requiring the entire stack to be online during pull requests.

## Grafana “Perf Trends” panels

The Grafana dashboard `grafana/dashboards/perf-trends.json` adds a dedicated “Perf
Trends” view. It focuses on P95 latency and throughput for the four core services and
supports a service dropdown to switch context quickly. Point the panels at Prometheus
metrics (`http_server_duration_seconds_bucket` and `http_requests_total`) and tag the
new JSON dashboard file in Git to keep observability assets in sync with the benchmark
scripts.
