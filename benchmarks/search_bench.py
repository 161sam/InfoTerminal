#!/usr/bin/env python3
"""Benchmark runner for the Search API service."""

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

DEFAULT_URL = os.getenv("SEARCH_API_URL", "http://localhost:8611/v1/search")
DEFAULT_PAYLOAD = {
    "q": "infoterminal",
    "filters": {},
    "facets": ["source", "language"],
    "sort": {"field": "published_at", "order": "desc"},
    "highlight": True,
}


def main() -> None:
    parser = build_arg_parser(
        "search-api",
        default_url=DEFAULT_URL,
        default_method="POST",
        description="Execute latency/throughput benchmarks against the Search API /v1/search endpoint.",
        default_payload=DEFAULT_PAYLOAD,
        default_concurrency=5,
        default_requests=40,
        default_latency_slo_ms=350.0,
        default_throughput_slo_rps=20.0,
    )
    args = parser.parse_args()

    payload = load_payload(args)
    headers = parse_headers(args.headers)

    config = BenchmarkConfig(
        service_name="search-api",
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
