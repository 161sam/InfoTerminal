#!/usr/bin/env python3
"""Generate frozen OpenAPI artefacts for InfoTerminal services."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SERVICES_DIR = REPO_ROOT / "services"


def _load_fastapi_app(service: str, module_path: str) -> "FastAPI":
    """Import the FastAPI application for the given service."""

    service_src = SERVICES_DIR / f"{service}" / "src"
    if not service_src.exists():
        raise SystemExit(f"service '{service}' does not contain a src/ directory")

    # Ensure both the shared service helpers and the service package itself are importable.
    sys.path.insert(0, str(SERVICES_DIR))
    sys.path.insert(0, str(service_src))

    module: ModuleType = importlib.import_module(module_path)
    app = getattr(module, "app", None)
    if app is None:
        raise SystemExit(f"module '{module_path}' does not expose a FastAPI 'app'")
    return app


def generate_openapi(service: str, module_path: str) -> dict[str, Any]:
    """Return the OpenAPI schema for the specified FastAPI app."""

    app = _load_fastapi_app(service, module_path)
    schema = app.openapi()
    if not isinstance(schema, dict):
        raise SystemExit("FastAPI returned a non-dict OpenAPI schema")
    return schema


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OpenAPI artefact")
    parser.add_argument(
        "--service",
        default="search-api",
        help="Service name (folder under services/)"
    )
    parser.add_argument(
        "--module",
        default="search_api.app.main_v1",
        help="Python module containing the FastAPI app"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "artifacts" / "api" / "openapi-v1.0.json",
        help="Path to write the OpenAPI JSON artefact"
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="Indentation for the JSON output"
    )

    args = parser.parse_args()
    schema = generate_openapi(args.service, args.module)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(schema, indent=args.indent, sort_keys=True))


if __name__ == "__main__":
    main()
