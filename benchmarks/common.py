"""Utility functions for running HTTP benchmarks across InfoTerminal services."""
from __future__ import annotations

import argparse
import asyncio
import csv
import json
import math
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

try:  # Optional dependency – only required for live runs
    import httpx
except ImportError:  # pragma: no cover - httpx optional for simulation/dry-run
    httpx = None  # type: ignore

ARTIFACT_DIR = Path("artifacts/perf")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class BenchmarkConfig:
    """Configuration for a benchmark run."""

    service_name: str
    url: str
    method: str = "GET"
    payload: Optional[Any] = None
    headers: Dict[str, str] = field(default_factory=dict)
    concurrency: int = 5
    total_requests: int = 50
    timeout: float = 10.0
    latency_slo_ms: Optional[float] = None
    throughput_slo_rps: Optional[float] = None
    output_prefix: Optional[str] = None
    dry_run: bool = False
    simulate: bool = False
    verify_tls: bool = True

    def serialise(self) -> Dict[str, Any]:
        """Return a JSON serialisable representation of the config."""

        return {
            "service_name": self.service_name,
            "url": self.url,
            "method": self.method,
            "payload": self.payload,
            "headers": self.headers,
            "concurrency": self.concurrency,
            "total_requests": self.total_requests,
            "timeout": self.timeout,
            "latency_slo_ms": self.latency_slo_ms,
            "throughput_slo_rps": self.throughput_slo_rps,
            "dry_run": self.dry_run,
            "simulate": self.simulate,
            "verify_tls": self.verify_tls,
        }


@dataclass
class RequestResult:
    """Result for a single HTTP request."""

    success: bool
    status_code: Optional[int]
    latency_ms: float
    error: Optional[str] = None


@dataclass
class BenchmarkSummary:
    """Aggregated summary for a benchmark run."""

    service_name: str
    timestamp: str
    status: str
    config: Dict[str, Any]
    metrics: Dict[str, Any]
    slo: Dict[str, Any]
    errors: List[str]
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Return a serialisable dict."""

        return {
            "service_name": self.service_name,
            "timestamp": self.timestamp,
            "status": self.status,
            "config": self.config,
            "metrics": self.metrics,
            "slo": self.slo,
            "errors": self.errors,
            "notes": self.notes,
        }


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def _percentile(values: List[float], percentile: float) -> Optional[float]:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    values_sorted = sorted(values)
    k = (len(values_sorted) - 1) * percentile
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return values_sorted[int(k)]
    d0 = values_sorted[int(f)] * (c - k)
    d1 = values_sorted[int(c)] * (k - f)
    return d0 + d1


def _aggregate_results(results: List[RequestResult], duration: float) -> Dict[str, Any]:
    latencies = [r.latency_ms for r in results if r.latency_ms is not None]
    success_results = [r for r in results if r.success]
    total_requests = len(results)
    success_count = len(success_results)
    error_count = total_requests - success_count
    success_rate = (success_count / total_requests) if total_requests else 0.0
    throughput = (success_count / duration) if duration > 0 else 0.0

    latency_section = {
        "min_ms": min(latencies) if latencies else None,
        "max_ms": max(latencies) if latencies else None,
        "mean_ms": sum(latencies) / len(latencies) if latencies else None,
        "p50_ms": _percentile(latencies, 0.50),
        "p95_ms": _percentile(latencies, 0.95),
        "p99_ms": _percentile(latencies, 0.99),
    }

    return {
        "total_requests": total_requests,
        "success_count": success_count,
        "error_count": error_count,
        "success_rate": success_rate,
        "duration_seconds": duration,
        "throughput_rps": throughput,
        "latency_ms": latency_section,
    }


def _slo_status(metrics: Dict[str, Any], config: BenchmarkConfig) -> Tuple[Dict[str, Any], str]:
    slo_info: Dict[str, Any] = {}
    status = "ok"

    latency_p95 = metrics["latency_ms"].get("p95_ms")
    if config.latency_slo_ms is not None:
        latency_met = latency_p95 is not None and latency_p95 <= config.latency_slo_ms
        slo_info["latency_p95_ms"] = {
            "target": config.latency_slo_ms,
            "actual": latency_p95,
            "met": latency_met,
        }
        if not latency_met:
            status = "degraded"

    throughput = metrics.get("throughput_rps")
    if config.throughput_slo_rps is not None:
        throughput_met = throughput is not None and throughput >= config.throughput_slo_rps
        slo_info["throughput_rps"] = {
            "target": config.throughput_slo_rps,
            "actual": throughput,
            "met": throughput_met,
        }
        if not throughput_met:
            status = "degraded"

    if metrics["success_count"] == 0:
        status = "failed"

    if metrics["error_count"] > 0 and status == "ok":
        status = "degraded"

    return slo_info, status


def _ensure_httpx_available() -> None:
    if httpx is None:  # pragma: no cover - triggered when dependency missing
        raise RuntimeError(
            "httpx is required for live benchmark runs. Install it via 'pip install httpx'."
        )


async def _execute_request(
    client: "httpx.AsyncClient", config: BenchmarkConfig, request_id: int
) -> RequestResult:
    start = time.perf_counter()
    try:
        response = await client.request(
            config.method.upper(),
            config.url,
            json=config.payload if config.payload is not None else None,
            headers=config.headers or None,
        )
        latency_ms = (time.perf_counter() - start) * 1000.0
        return RequestResult(
            success=response.status_code < 500,
            status_code=response.status_code,
            latency_ms=latency_ms,
            error=None if response.status_code < 400 else response.text[:512],
        )
    except Exception as exc:  # pragma: no cover - network failures
        latency_ms = (time.perf_counter() - start) * 1000.0
        return RequestResult(success=False, status_code=None, latency_ms=latency_ms, error=str(exc))


async def _run_live_benchmark(config: BenchmarkConfig) -> Tuple[List[RequestResult], float]:
    _ensure_httpx_available()
    limits = httpx.Limits(max_keepalive_connections=config.concurrency, max_connections=config.concurrency)
    timeout = httpx.Timeout(config.timeout)
    results: List[RequestResult] = []
    start = time.perf_counter()
    async with httpx.AsyncClient(verify=config.verify_tls, limits=limits, timeout=timeout) as client:
        sem = asyncio.Semaphore(config.concurrency)

        async def runner(request_id: int) -> RequestResult:
            async with sem:
                return await _execute_request(client, config, request_id)

        tasks = [asyncio.create_task(runner(i)) for i in range(config.total_requests)]
        for coro in asyncio.as_completed(tasks):
            results.append(await coro)
    duration = time.perf_counter() - start
    return results, duration


def _simulate_results(config: BenchmarkConfig) -> Tuple[List[RequestResult], float, List[str]]:
    import random

    seed_basis = f"{config.service_name}:{config.total_requests}:{config.concurrency}:{config.method}:{config.url}"
    seed = abs(hash(seed_basis)) % (2**32)
    rng = random.Random(seed)
    base_latency = rng.uniform(60.0, 220.0)
    latencies: List[float] = []
    results: List[RequestResult] = []
    for _ in range(config.total_requests):
        jitter = rng.gauss(0, base_latency * 0.12)
        latency = max(5.0, base_latency + jitter)
        latencies.append(latency)
        results.append(RequestResult(success=True, status_code=200, latency_ms=latency))
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    # Approximate duration assuming concurrency reduces runtime
    duration = max(avg_latency / 1000.0 * (config.total_requests / max(config.concurrency, 1)), 0.001)
    notes = [
        "simulation_mode",  # marker for downstream tooling
        f"seed={seed}",
    ]
    return results, duration, notes


def write_artifacts(summary: BenchmarkSummary, output_prefix: str) -> None:
    json_path = ARTIFACT_DIR / f"{output_prefix}.json"
    csv_path = ARTIFACT_DIR / f"{output_prefix}.csv"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(summary.to_dict(), f, indent=2, sort_keys=True)

    csv_columns = [
        "service_name",
        "timestamp",
        "status",
        "total_requests",
        "success_count",
        "error_count",
        "success_rate",
        "duration_seconds",
        "throughput_rps",
        "latency_min_ms",
        "latency_mean_ms",
        "latency_p50_ms",
        "latency_p95_ms",
        "latency_p99_ms",
        "latency_max_ms",
        "latency_slo_target_ms",
        "latency_slo_met",
        "throughput_slo_target_rps",
        "throughput_slo_met",
    ]

    metrics = summary.metrics
    latency = metrics.get("latency_ms", {}) if isinstance(metrics, dict) else {}
    slo = summary.slo if isinstance(summary.slo, dict) else {}

    row = {
        "service_name": summary.service_name,
        "timestamp": summary.timestamp,
        "status": summary.status,
        "total_requests": metrics.get("total_requests"),
        "success_count": metrics.get("success_count"),
        "error_count": metrics.get("error_count"),
        "success_rate": metrics.get("success_rate"),
        "duration_seconds": metrics.get("duration_seconds"),
        "throughput_rps": metrics.get("throughput_rps"),
        "latency_min_ms": latency.get("min_ms"),
        "latency_mean_ms": latency.get("mean_ms"),
        "latency_p50_ms": latency.get("p50_ms"),
        "latency_p95_ms": latency.get("p95_ms"),
        "latency_p99_ms": latency.get("p99_ms"),
        "latency_max_ms": latency.get("max_ms"),
    }

    latency_slo = slo.get("latency_p95_ms") if slo else None
    throughput_slo = slo.get("throughput_rps") if slo else None
    if latency_slo:
        row["latency_slo_target_ms"] = latency_slo.get("target")
        row["latency_slo_met"] = latency_slo.get("met")
    if throughput_slo:
        row["throughput_slo_target_rps"] = throughput_slo.get("target")
        row["throughput_slo_met"] = throughput_slo.get("met")

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=csv_columns)
        writer.writeheader()
        writer.writerow(row)


def run_benchmark(config: BenchmarkConfig) -> BenchmarkSummary:
    """Execute a benchmark run (live, simulated, or dry-run)."""

    timestamp = datetime.now(timezone.utc).isoformat()

    if config.dry_run:
        metrics = {
            "total_requests": 0,
            "success_count": 0,
            "error_count": 0,
            "success_rate": 0.0,
            "duration_seconds": 0.0,
            "throughput_rps": 0.0,
            "latency_ms": {
                "min_ms": None,
                "max_ms": None,
                "mean_ms": None,
                "p50_ms": None,
                "p95_ms": None,
                "p99_ms": None,
            },
        }
        slo, status = _slo_status(metrics, config)
        summary = BenchmarkSummary(
            service_name=config.service_name,
            timestamp=timestamp,
            status="skipped",
            config=config.serialise(),
            metrics=metrics,
            slo=slo,
            errors=[],
            notes=["dry_run"],
        )
        write_artifacts(summary, config.output_prefix or config.service_name)
        return summary

    if config.simulate:
        results, duration, notes = _simulate_results(config)
    else:
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            results, duration = loop.run_until_complete(_run_live_benchmark(config))
            notes = []
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            asyncio.set_event_loop(None)

    metrics = _aggregate_results(results, duration)
    slo, status = _slo_status(metrics, config)
    errors = [r.error for r in results if r.error][:10]
    summary = BenchmarkSummary(
        service_name=config.service_name,
        timestamp=timestamp,
        status=status,
        config=config.serialise(),
        metrics=metrics,
        slo=slo,
        errors=[e for e in errors if e],
        notes=notes,
    )
    write_artifacts(summary, config.output_prefix or config.service_name)
    return summary


def build_arg_parser(
    service_name: str,
    *,
    default_url: str,
    default_method: str = "GET",
    description: Optional[str] = None,
    default_payload: Optional[Any] = None,
    default_concurrency: int = 5,
    default_requests: int = 50,
    default_latency_slo_ms: Optional[float] = None,
    default_throughput_slo_rps: Optional[float] = None,
) -> argparse.ArgumentParser:
    """Create a reusable CLI parser for service benchmark scripts."""

    parser = argparse.ArgumentParser(
        description=description or f"Benchmark runner for {service_name}",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--url", default=default_url, help="Target URL for the benchmark endpoint")
    parser.add_argument("--method", default=default_method, help="HTTP method to use")
    parser.add_argument(
        "--payload",
        help="Inline JSON payload (overrides default/sample payload)",
    )
    parser.add_argument(
        "--payload-file",
        dest="payload_file",
        help="Path to JSON file containing request payload",
    )
    parser.add_argument(
        "--header",
        dest="headers",
        action="append",
        default=[],
        help="Custom header in KEY:VALUE format (can be passed multiple times)",
    )
    parser.add_argument("--concurrency", type=int, default=default_concurrency, help="Number of concurrent workers")
    parser.add_argument("--requests", type=int, default=default_requests, help="Total number of requests to execute")
    parser.add_argument("--timeout", type=float, default=10.0, help="Per-request timeout in seconds")
    parser.add_argument(
        "--latency-slo-ms",
        type=float,
        default=default_latency_slo_ms,
        help="Target P95 latency in milliseconds",
    )
    parser.add_argument(
        "--throughput-slo-rps",
        type=float,
        default=default_throughput_slo_rps,
        help="Target throughput in requests per second",
    )
    parser.add_argument(
        "--output-prefix",
        default=service_name.replace("-", "_"),
        help="Filename prefix for generated artefacts",
    )
    parser.add_argument("--dry-run", action="store_true", help="Skip execution but still emit artefact skeleton")
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Generate deterministic synthetic metrics (useful for CI smoke tests)",
    )
    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable TLS verification (for local HTTPS development)",
    )
    parser.set_defaults(default_payload=default_payload)
    return parser


def parse_headers(raw_headers: Iterable[str]) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    for item in raw_headers:
        if not item:
            continue
        if ":" not in item:
            raise ValueError(f"Invalid header format: {item!r}. Expected KEY:VALUE")
        key, value = item.split(":", 1)
        headers[key.strip()] = value.strip()
    return headers


def load_payload(args: argparse.Namespace) -> Optional[Any]:
    if getattr(args, "payload_file", None):
        path = Path(args.payload_file)
        return json.loads(path.read_text(encoding="utf-8"))
    if getattr(args, "payload", None):
        return json.loads(args.payload)
    return getattr(args, "default_payload", None)


__all__ = [
    "BenchmarkConfig",
    "BenchmarkSummary",
    "build_arg_parser",
    "load_payload",
    "parse_headers",
    "run_benchmark",
]
