#!/usr/bin/env python3
"""Benchmark runner for the Doc-Entities service."""

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

DEFAULT_URL = os.getenv("DOC_ENTITIES_URL", "http://localhost:8613/v1/extract/entities")
DEFAULT_PAYLOAD = {
    "text": "InfoTerminal accelerates OSINT workflows by combining search, graph analytics, and NLP in a unified workspace.",
    "language": "en",
}


def main() -> None:
    parser = build_arg_parser(
        "doc-entities",
        default_url=DEFAULT_URL,
        default_method="POST",
        description="Benchmark the doc-entities /v1/extract/entities endpoint (spaCy pipeline).",
        default_payload=DEFAULT_PAYLOAD,
        default_concurrency=3,
        default_requests=24,
        default_latency_slo_ms=1200.0,
        default_throughput_slo_rps=8.0,
    )
    args = parser.parse_args()

    payload = load_payload(args)
    headers = parse_headers(args.headers)

    config = BenchmarkConfig(
        service_name="doc-entities",
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
