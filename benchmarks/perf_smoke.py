#!/usr/bin/env python3
"""Run deterministic performance smoke benchmarks for core services."""

from __future__ import annotations

import argparse
import json
import os
from typing import Dict, List

from common import BenchmarkConfig, run_benchmark


def build_smoke_plan(simulate: bool) -> List[BenchmarkConfig]:
    """Return benchmark configs for the smoke run."""

    return [
        BenchmarkConfig(
            service_name="search-api",
            url=os.getenv("SEARCH_API_URL", "http://localhost:8611/v1/search"),
            method="POST",
            payload={
                "q": "osint",
                "filters": {},
                "facets": [],
                "highlight": False,
            },
            concurrency=2,
            total_requests=6,
            timeout=5.0,
            latency_slo_ms=400.0,
            throughput_slo_rps=8.0,
            output_prefix="search-api_smoke",
            simulate=simulate,
        ),
        BenchmarkConfig(
            service_name="graph-api",
            url=os.getenv("GRAPH_API_URL", "http://localhost:8612/v1/cypher"),
            method="POST",
            payload={
                "query": "MATCH (n) RETURN n LIMIT 3",
                "parameters": {},
                "read_only": True,
            },
            concurrency=2,
            total_requests=6,
            timeout=5.0,
            latency_slo_ms=550.0,
            throughput_slo_rps=6.0,
            output_prefix="graph-api_smoke",
            simulate=simulate,
        ),
        BenchmarkConfig(
            service_name="doc-entities",
            url=os.getenv("DOC_ENTITIES_URL", "http://localhost:8613/v1/extract/entities"),
            method="POST",
            payload={"text": "Open-source intelligence accelerates investigations.", "language": "en"},
            concurrency=2,
            total_requests=5,
            timeout=10.0,
            latency_slo_ms=1500.0,
            throughput_slo_rps=4.0,
            output_prefix="doc-entities_smoke",
            simulate=simulate,
        ),
        BenchmarkConfig(
            service_name="agent-connector",
            url=os.getenv("AGENT_CONNECTOR_URL", "http://localhost:8633/v1/plugins/registry"),
            method="GET",
            concurrency=2,
            total_requests=6,
            timeout=5.0,
            latency_slo_ms=450.0,
            throughput_slo_rps=7.0,
            output_prefix="agent-connector_smoke",
            simulate=simulate,
        ),
    ]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run performance smoke benchmarks (simulate by default for CI)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["simulate", "live"],
        default="simulate",
        help="Run in deterministic simulation mode or execute live HTTP calls",
    )
    args = parser.parse_args()

    simulate = args.mode == "simulate"
    results: Dict[str, Dict[str, str]] = {}
    for config in build_smoke_plan(simulate):
        summary = run_benchmark(config)
        results[config.service_name] = {
            "status": summary.status,
            "artifact_json": f"artifacts/perf/{config.output_prefix}.json",
            "artifact_csv": f"artifacts/perf/{config.output_prefix}.csv",
        }

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
