#!/usr/bin/env python3
"""Benchmark runner for the Agent Connector service."""

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

DEFAULT_URL = os.getenv("AGENT_CONNECTOR_URL", "http://localhost:8633/v1/plugins/registry")


def main() -> None:
    parser = build_arg_parser(
        "agent-connector",
        default_url=DEFAULT_URL,
        default_method="GET",
        description="Benchmark the agent connector plugin registry endpoint for discovery latency.",
        default_payload=None,
        default_concurrency=4,
        default_requests=36,
        default_latency_slo_ms=400.0,
        default_throughput_slo_rps=12.0,
    )
    args = parser.parse_args()

    payload = load_payload(args)
    headers = parse_headers(args.headers)

    config = BenchmarkConfig(
        service_name="agent-connector",
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
