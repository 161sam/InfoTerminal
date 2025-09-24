#!/usr/bin/env python3
"""Validate that source SBOM and license artefacts exist and are non-empty."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SBOM_DIR = REPO_ROOT / "artifacts" / "sbom" / "source"
LICENSE_DIR = REPO_ROOT / "artifacts" / "compliance" / "licenses"

REQUIRED_SBOMS = (
    SBOM_DIR / "backend-python.cdx.json",
    SBOM_DIR / "frontend-node.cdx.json",
)

REQUIRED_LICENSES = (
    LICENSE_DIR / "license_inventory.json",
    LICENSE_DIR / "license_inventory.csv",
)


def _assert_json(path: Path) -> None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - CLI validation
        raise SystemExit(f"{path} is not valid JSON: {exc}")
    if isinstance(data, dict) and not data.get("components") and "cdxTool" not in data:
        raise SystemExit(f"{path} does not contain any components")
    if isinstance(data, list) and not data:
        raise SystemExit(f"{path} JSON payload is empty")


def _assert_csv(path: Path) -> None:
    if not path.read_text(encoding="utf-8").strip():
        raise SystemExit(f"{path} is empty")


def main() -> None:
    missing = [str(path) for path in (*REQUIRED_SBOMS, *REQUIRED_LICENSES) if not path.exists()]
    if missing:
        raise SystemExit(f"Missing required artefacts: {', '.join(missing)}")
    for sbom_path in REQUIRED_SBOMS:
        if sbom_path.stat().st_size == 0:
            raise SystemExit(f"SBOM is empty: {sbom_path}")
        _assert_json(sbom_path)
    license_json, license_csv = REQUIRED_LICENSES
    if license_json.stat().st_size == 0:
        raise SystemExit(f"License inventory JSON is empty: {license_json}")
    _assert_json(license_json)
    if license_csv.stat().st_size == 0:
        raise SystemExit(f"License inventory CSV is empty: {license_csv}")
    _assert_csv(license_csv)
    print("sbom_source_integrity: all required artefacts are present and non-empty")


if __name__ == "__main__":
    main()
