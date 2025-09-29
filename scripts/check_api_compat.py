#!/usr/bin/env python3
"""Check OpenAPI compatibility against the frozen artefact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable

from generate_openapi_artifact import generate_openapi

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = REPO_ROOT / "artifacts" / "api" / "openapi-v1.0.json"


class CompatibilityError(Exception):
    """Raised when a breaking change is detected."""


def load_schema(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise CompatibilityError(f"baseline OpenAPI artefact missing: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:  # pragma: no cover - sanity
        raise CompatibilityError(f"failed to parse OpenAPI artefact {path}: {exc}") from exc


def _index_parameters(params: Iterable[Dict[str, Any]]) -> Dict[tuple[str, str], Dict[str, Any]]:
    indexed: Dict[tuple[str, str], Dict[str, Any]] = {}
    for param in params:
        key = (param.get("name"), param.get("in"))
        indexed[key] = param
    return indexed


def _normalise_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    """Return a subset of schema fields relevant for compatibility checks."""

    if not isinstance(schema, dict):
        return schema

    normalised = dict(schema)
    for key in ["description", "title", "example", "examples", "deprecated"]:
        normalised.pop(key, None)

    if "properties" in normalised:
        normalised["properties"] = {
            name: _normalise_schema(value)
            for name, value in normalised["properties"].items()
        }
    if "items" in normalised and isinstance(normalised["items"], dict):
        normalised["items"] = _normalise_schema(normalised["items"])

    return normalised


def _compare_parameters(old_params: Iterable[Dict[str, Any]], new_params: Iterable[Dict[str, Any]], path: str, method: str, problems: list[str]) -> None:
    old_index = _index_parameters(old_params)
    new_index = _index_parameters(new_params)

    for key, old_param in old_index.items():
        if key not in new_index:
            problems.append(f"{path} {method}: parameter {key} removed")
            continue

        new_param = new_index[key]
        for field in ["required", "schema", "content"]:
            if field not in old_param:
                continue
            if field not in new_param:
                problems.append(f"{path} {method}: parameter {key} missing field '{field}'")
                continue
            if field == "schema":
                if _normalise_schema(old_param[field]) != _normalise_schema(new_param[field]):
                    problems.append(f"{path} {method}: parameter {key} schema changed")
            else:
                if old_param[field] != new_param[field]:
                    problems.append(f"{path} {method}: parameter {key} field '{field}' changed")


def _compare_request_body(old_body: Dict[str, Any], new_body: Dict[str, Any], path: str, method: str, problems: list[str]) -> None:
    if not old_body:
        return
    if not new_body:
        problems.append(f"{path} {method}: request body removed")
        return

    if old_body.get("required") and not new_body.get("required"):
        problems.append(f"{path} {method}: request body no longer required")

    old_content = old_body.get("content", {})
    new_content = new_body.get("content", {})
    for media_type, old_media in old_content.items():
        if media_type not in new_content:
            problems.append(f"{path} {method}: request body media type {media_type} removed")
            continue
        old_schema = _normalise_schema(old_media.get("schema", {}))
        new_schema = _normalise_schema(new_content[media_type].get("schema", {}))
        if old_schema != new_schema:
            problems.append(f"{path} {method}: request body schema for {media_type} changed")


def _compare_responses(old_responses: Dict[str, Any], new_responses: Dict[str, Any], path: str, method: str, problems: list[str]) -> None:
    for status_code, old_response in old_responses.items():
        if status_code not in new_responses:
            problems.append(f"{path} {method}: response {status_code} removed")
            continue
        new_response = new_responses[status_code]
        old_content = old_response.get("content", {})
        new_content = new_response.get("content", {})
        for media_type, old_media in old_content.items():
            if media_type not in new_content:
                problems.append(f"{path} {method}: response {status_code} media {media_type} removed")
                continue
            old_schema = _normalise_schema(old_media.get("schema", {}))
            new_schema = _normalise_schema(new_content[media_type].get("schema", {}))
            if old_schema != new_schema:
                problems.append(f"{path} {method}: response {status_code} schema for {media_type} changed")


def _compare_components(old_components: Dict[str, Any], new_components: Dict[str, Any], problems: list[str]) -> None:
    old_schemas = old_components.get("schemas", {})
    new_schemas = new_components.get("schemas", {})
    for name, old_schema in old_schemas.items():
        if name not in new_schemas:
            problems.append(f"component schema {name} removed")
            continue
        if _normalise_schema(old_schema) != _normalise_schema(new_schemas[name]):
            problems.append(f"component schema {name} changed")


def check_backward_compatible(old_schema: Dict[str, Any], new_schema: Dict[str, Any]) -> list[str]:
    problems: list[str] = []

    old_paths = old_schema.get("paths", {})
    new_paths = new_schema.get("paths", {})
    for path, old_methods in old_paths.items():
        if path not in new_paths:
            problems.append(f"path {path} removed")
            continue
        new_methods = new_paths[path]
        for method, old_operation in old_methods.items():
            if method.startswith("x-"):
                continue
            new_operation = new_methods.get(method)
            if new_operation is None:
                problems.append(f"{path}: method {method} removed")
                continue
            _compare_parameters(
                old_operation.get("parameters", []),
                new_operation.get("parameters", []),
                path,
                method,
                problems,
            )
            _compare_request_body(
                old_operation.get("requestBody"),
                new_operation.get("requestBody"),
                path,
                method,
                problems,
            )
            _compare_responses(
                old_operation.get("responses", {}),
                new_operation.get("responses", {}),
                path,
                method,
                problems,
            )

    _compare_components(
        old_schema.get("components", {}),
        new_schema.get("components", {}),
        problems,
    )

    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="Check API compatibility")
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
        "--artefact",
        type=Path,
        default=ARTIFACT_PATH,
        help="Path to the frozen OpenAPI artefact"
    )

    args = parser.parse_args()

    baseline = load_schema(args.artefact)
    current = generate_openapi(args.service, args.module)

    problems = check_backward_compatible(baseline, current)
    if problems:
        details = "\n - ".join([""] + problems)
        raise SystemExit(f"Breaking API changes detected:{details}")

    print("API compatibility check passed: no breaking changes detected.")


if __name__ == "__main__":
    main()
