#!/usr/bin/env python3
"""Deterministic synthetic smoke checks for core InfoTerminal services.

The script reuses the blackbox-exporter target list so that CI, Prometheus,

and manual invocations stay aligned. By default it performs a GET request for

all configured targets and fails fast when one of them is not reachable or

returns a non-2xx/3xx status code.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGET_FILE = REPO_ROOT / "observability" / "prometheus" / "synthetic-smoke-targets.json"
DEFAULT_TIMEOUT = 5.0


@dataclass
class SmokeTarget:
    service: str
    url: str
    module: str = "http_2xx"

    @classmethod
    def from_mapping(cls, mapping: dict) -> "SmokeTarget":
        labels = mapping.get("labels", {})
        targets = mapping.get("targets", [])
        if not targets:
            raise ValueError("Synthetic target entry must define at least one target")
        url = targets[0]
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"Invalid URL for synthetic target: {url!r}")
        service = labels.get("service") or parsed.netloc
        module = labels.get("module", "http_2xx")
        return cls(service=service, url=url, module=module)


@dataclass
class ProbeResult:
    target: SmokeTarget
    success: bool
    status: int | None
    latency_ms: float | None
    error: str | None = None

    def render(self) -> str:
        status_text = "n/a" if self.status is None else str(self.status)
        latency = "n/a" if self.latency_ms is None else f"{self.latency_ms:.1f} ms"
        marker = "OK" if self.success else "FAIL"
        reason = "" if self.error is None else f" ({self.error})"
        return f"[{marker}] {self.target.service}: {status_text} in {latency}{reason}"


def load_targets(path: Path) -> List[SmokeTarget]:
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError as exc:
        raise SystemExit(f"Target definition file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in target definition file {path}: {exc}") from exc

    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise SystemExit("Synthetic target file must contain a list of mappings")

    targets: List[SmokeTarget] = []
    for idx, raw in enumerate(data):
        if not isinstance(raw, dict):
            raise SystemExit(f"Entry {idx} in synthetic target file is not an object")
        try:
            targets.append(SmokeTarget.from_mapping(raw))
        except ValueError as exc:
            raise SystemExit(str(exc)) from exc
    if not targets:
        raise SystemExit("Synthetic smoke target file does not define any targets")
    return targets


def probe(target: SmokeTarget, timeout: float) -> ProbeResult:
    request = Request(target.url, method="GET", headers={"User-Agent": "InfoTerminal-Synthetic/CI"})
    start = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            # Read a small chunk to guarantee connection success without buffering entire body.
            response.read(64)
    except HTTPError as exc:
        latency_ms = (time.perf_counter() - start) * 1000.0
        return ProbeResult(target=target, success=False, status=exc.code, latency_ms=latency_ms, error=exc.reason)
    except URLError as exc:
        return ProbeResult(target=target, success=False, status=None, latency_ms=None, error=str(exc.reason))
    except Exception as exc:  # pragma: no cover - defensive guardrail
        return ProbeResult(target=target, success=False, status=None, latency_ms=None, error=str(exc))

    latency_ms = (time.perf_counter() - start) * 1000.0
    success = 200 <= status < 400
    error = None if success else "unexpected status"
    return ProbeResult(target=target, success=success, status=status, latency_ms=latency_ms, error=error)


def run_smoke(targets: Iterable[SmokeTarget], timeout: float, fail_fast: bool) -> List[ProbeResult]:
    results: List[ProbeResult] = []
    for target in targets:
        result = probe(target, timeout)
        results.append(result)
        print(result.render())
        if fail_fast and not result.success:
            break
    return results


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Synthetic smoke checks for InfoTerminal core services")
    parser.add_argument(
        "--targets-file",
        type=Path,
        default=DEFAULT_TARGET_FILE,
        help=f"Path to the synthetic target definition (default: {DEFAULT_TARGET_FILE})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Timeout in seconds per HTTP probe (default: %(default)s)",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Abort immediately after the first failure",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print discovered targets without executing probes",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate target definitions without executing HTTP probes",
    )
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    targets = load_targets(args.targets_file)

    if args.dry_run:
        for target in targets:
            print(f"- {target.service}: {target.url} ({target.module})")
        return 0

    if args.validate_only:
        valid = True
        for target in targets:
            parsed = urlparse(target.url)
            host = parsed.hostname or ""
            if parsed.scheme != "http":
                print(f"[INVALID] {target.service}: unsupported scheme {parsed.scheme}")
                valid = False
            if host and host != "localhost" and "." in host:
                print(f"[INVALID] {target.service}: host {host} must be internal-only")
                valid = False
        return 0 if valid else 1

    results = run_smoke(targets, timeout=args.timeout, fail_fast=args.fail_fast)
    success = all(result.success for result in results)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
