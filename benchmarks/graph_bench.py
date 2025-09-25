#!/usr/bin/env python3
"""Benchmark runner for the Graph API service."""

from __future__ import annotations

import json
import os

from common import (
    BenchmarkConfig,
    build_arg_parser,
    load_payload,
    parse_headers,
    run_benchmark,
)

DEFAULT_URL = os.getenv("GRAPH_API_URL", "http://localhost:8612/v1/cypher")
DEFAULT_PAYLOAD = {
    "query": "MATCH (n) RETURN count(n) as total",
    "parameters": {},
    "read_only": True,
}


def main() -> None:
    parser = build_arg_parser(
        "graph-api",
        default_url=DEFAULT_URL,
        default_method="POST",
        description="Benchmark the Graph API Cypher endpoint for query latency and throughput.",
        default_payload=DEFAULT_PAYLOAD,
        default_concurrency=4,
        default_requests=32,
        default_latency_slo_ms=450.0,
        default_throughput_slo_rps=15.0,
    )
    args = parser.parse_args()

    payload = load_payload(args)
    headers = parse_headers(args.headers)

    config = BenchmarkConfig(
        service_name="graph-api",
        url=args.url,
        method=args.method,
        payload=payload,
        headers=headers,
        concurrency=args.concurrency,
        total_requests=args.requests,
        timeout=args.timeout,
        latency_slo_ms=args.latency_slo_ms,
        throughput_slo_rps=args.throughput_slo_rps,
        output_prefix=args.output_prefix,
        dry_run=args.dry_run,
        simulate=args.simulate,
        verify_tls=not args.insecure,
    )
    summary = run_benchmark(config)
    print(json.dumps(summary.to_dict(), indent=2))


if __name__ == "__main__":
    main()
