#!/usr/bin/env python3
"""Validate that image SBOM artefacts and license inventory are complete."""

from __future__ import annotations

import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.generate_image_sboms import (  # type: ignore[import-not-found]
    IMAGES_SBOM_DIR,
    LICENSE_OUTPUT,
    collect_images,
    sanitise_filename,
)


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - CLI validation guard
        raise SystemExit(f"{path} is not valid JSON: {exc}") from exc


def main() -> None:
    images = collect_images()
    if not images:
        raise SystemExit("No images discovered; ensure docker-compose*/production manifests exist")

    missing_sboms: list[str] = []
    empty_sboms: list[str] = []

    for image in sorted(images):
        sbom_path = IMAGES_SBOM_DIR / sanitise_filename(image)
        if not sbom_path.exists():
            missing_sboms.append(f"{image} -> {sbom_path.relative_to(REPO_ROOT)}")
            continue
        if sbom_path.stat().st_size == 0:
            empty_sboms.append(str(sbom_path.relative_to(REPO_ROOT)))
            continue
        data = _load_json(sbom_path)
        if not data.get("components"):
            raise SystemExit(f"SBOM for {image} has no components: {sbom_path}")

    if missing_sboms:
        raise SystemExit(
            "Missing SBOMs for referenced images: " + ", ".join(missing_sboms)
        )
    if empty_sboms:
        raise SystemExit("Empty SBOM files: " + ", ".join(empty_sboms))

    if not LICENSE_OUTPUT.exists():
        raise SystemExit(f"Missing license inventory JSON: {LICENSE_OUTPUT}")
    if LICENSE_OUTPUT.stat().st_size == 0:
        raise SystemExit(f"License inventory is empty: {LICENSE_OUTPUT}")

    license_payload = _load_json(LICENSE_OUTPUT)
    if not isinstance(license_payload.get("images"), list):
        raise SystemExit("License inventory does not contain an 'images' list")

    inventory_index = {
        entry.get("image"): entry for entry in license_payload["images"] if isinstance(entry, dict)
    }
    missing_in_inventory = sorted(image for image in images if image not in inventory_index)
    if missing_in_inventory:
        raise SystemExit(
            "License inventory missing images: " + ", ".join(missing_in_inventory)
        )

    for image, entry in inventory_index.items():
        sbom_ref = entry.get("sbom")
        if not sbom_ref:
            raise SystemExit(f"License inventory entry for {image} lacks 'sbom' reference")
        sbom_path = REPO_ROOT / sbom_ref
        if not sbom_path.exists():
            raise SystemExit(
                f"License inventory entry for {image} references missing SBOM: {sbom_ref}"
            )

    print("sbom_image_integrity: all required artefacts are present and non-empty")


if __name__ == "__main__":
    main()
