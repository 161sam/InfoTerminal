#!/usr/bin/env python3
"""Validate the observability baseline across InfoTerminal services."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
OBSERVABILITY_PATH = REPO_ROOT / "inventory" / "observability.json"

REQUIRED_LABELS = {"service", "version", "env"}
SKIP_SERVICES = {"frontend", "cli"}


def load_inventory() -> Dict[str, Any]:
    if not OBSERVABILITY_PATH.exists():
        raise SystemExit(
            "Observability inventory missing. Run `python scripts/generate_inventory.py` first."
        )
    return json.loads(OBSERVABILITY_PATH.read_text(encoding="utf-8"))


def should_validate(service: Dict[str, Any]) -> bool:
    name = service.get("name") or ""
    if name.startswith("_"):
        return False
    if name in SKIP_SERVICES:
        return False
    frameworks = service.get("frameworks") or []
    language = (service.get("language") or "").lower()
    if "fastapi" in frameworks:
        return True
    return language in {"python", "javascript", "typescript"}


def validate_service(service: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    name = service.get("name", "unknown")
    if not should_validate(service):
        return errors

    if not service.get("healthz"):
        errors.append(f"{name}: missing /healthz endpoint")
    if not service.get("readyz"):
        errors.append(f"{name}: missing /readyz endpoint")

    metrics = service.get("metrics", {})
    metrics_path = metrics.get("path")
    labels = set(metrics.get("labels") or [])
    if not metrics_path:
        errors.append(f"{name}: missing /metrics endpoint")
    else:
        missing_labels = sorted(REQUIRED_LABELS - labels)
        if missing_labels:
            errors.append(
                f"{name}: metrics missing required labels ({', '.join(missing_labels)})"
            )

    return errors


def main() -> None:
    inventory = load_inventory()
    services = inventory.get("services", [])
    failures: List[str] = []
    for svc in services:
        failures.extend(validate_service(svc))

    if failures:
        print("Observability Baseline failed:")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)

    print("Observability Baseline passed for all services.")


if __name__ == "__main__":
    main()
