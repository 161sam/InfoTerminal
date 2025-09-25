#!/usr/bin/env python3
"""Generate machine-readable inventory reports for InfoTerminal.

This utility collects information about backend services, API routes,
database artefacts, and the frontend surface area. The output is written to
``inventory/`` as JSON files (plus an optional findings report) so that Phase 1
audits can consume consistent, idempotent metadata.

Usage::

    python scripts/generate_inventory.py           # writes JSON files
    python scripts/generate_inventory.py --dry-run # preview without writing

The script is intentionally conservative – it relies purely on static
inspection and avoids executing arbitrary project code. Whenever something
cannot be inferred automatically it is marked as ``unknown`` so that manual
follow-up is straightforward.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

try:
    import yaml  # type: ignore
except Exception as exc:  # pragma: no cover - defensive import guard
    raise SystemExit(
        "PyYAML is required to generate the inventory. Install it via"
        " `pip install pyyaml` and retry."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SERVICES_DIR = REPO_ROOT / "services"
FRONTEND_DIR = REPO_ROOT / "apps" / "frontend"
INVENTORY_DIR = REPO_ROOT / "inventory"

# Allow re-use of the FastAPI AST walker from the parity report generator.
sys.path.insert(0, str(REPO_ROOT / "scripts"))
try:
    import generate_parity_reports as parity
except Exception as exc:  # pragma: no cover - static import guard
    raise SystemExit(
        "Unable to import generate_parity_reports – ensure the repository is"
        " intact before running the inventory script."
    ) from exc


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_compose_services() -> Dict[str, Dict[str, Any]]:
    """Parse docker-compose files and aggregate per-service metadata."""

    service_data: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "compose_files": set(),
            "profiles": set(),
            "ports": set(),
            "env": set(),
            "depends_on": set(),
        }
    )

    compose_globs = ["docker-compose*.yml", "docker-compose*.yaml", "auth-service-compose.yml"]
    for pattern in compose_globs:
        for path in REPO_ROOT.glob(pattern):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            services = data.get("services") or {}
            for svc_name, cfg in services.items():
                entry = service_data[svc_name]
                entry["compose_files"].add(str(path.relative_to(REPO_ROOT)))
                for profile in cfg.get("profiles", []) or []:
                    entry["profiles"].add(profile)
                for port in cfg.get("ports", []) or []:
                    if isinstance(port, str):
                        entry["ports"].add(port)
                    elif isinstance(port, dict):
                        host = port.get("published") or port.get("host")
                        container = port.get("target") or port.get("container")
                        if host and container:
                            entry["ports"].add(f"{host}:{container}")
                        elif container:
                            entry["ports"].add(str(container))
                environment = cfg.get("environment") or {}
                if isinstance(environment, dict):
                    for key in environment:
                        entry["env"].add(str(key))
                elif isinstance(environment, list):
                    for item in environment:
                        if isinstance(item, str) and "=" in item:
                            entry["env"].add(item.split("=", 1)[0])
                for dep in cfg.get("depends_on", []) or []:
                    if isinstance(dep, str):
                        entry["depends_on"].add(dep)
                    elif isinstance(dep, dict):
                        entry["depends_on"].add(dep.get("service"))
    # Convert sets to sorted lists for JSON serialisation.
    return {
        name: {
            "compose_files": sorted(value["compose_files"]),
            "profiles": sorted(filter(None, value["profiles"])),
            "ports": sorted(filter(None, value["ports"])),
            "env": sorted(filter(None, value["env"])),
            "depends_on": sorted(filter(None, value["depends_on"])),
        }
        for name, value in service_data.items()
    }


def detect_language_and_framework(service_dir: Path) -> Dict[str, Any]:
    language = "unknown"
    frameworks: Set[str] = set()
    if (service_dir / "package.json").exists():
        language = "javascript"
        package_json = json.loads((service_dir / "package.json").read_text(encoding="utf-8"))
        deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}
        for candidate in ("next", "express", "fastify"):
            if candidate in deps:
                frameworks.add(candidate)
    elif any((service_dir / candidate).exists() for candidate in ("pyproject.toml", "requirements.txt", "setup.cfg")):
        language = "python"
        # Heuristic: look for FastAPI, Typer, etc.
        for path in service_dir.glob("**/*.py"):
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if "FastAPI" in content:
                frameworks.add("fastapi")
            if "Typer" in content:
                frameworks.add("typer")
    return {"language": language, "frameworks": sorted(frameworks)}


def detect_health_endpoints(service_dir: Path) -> Dict[str, bool]:
    targets = {"healthz": False, "readyz": False, "metrics": False}
    if not service_dir.exists():
        return targets
    for path in service_dir.rglob("*.py"):
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name in targets:
            if name == "metrics":
                if (
                    f"/{name}" in content
                    or "enable_prometheus_metrics" in content
                    or "setup_standard_middleware" in content
                ):
                    targets[name] = True
            elif f"/{name}" in content:
                targets[name] = True
    return targets


def collect_feature_flags_from_env(env_vars: Iterable[str]) -> List[str]:
    flags = []
    for key in env_vars:
        if re.search(r"(FEATURE|FLAG|ENABLE|DISABLE)", key.upper()):
            flags.append(key)
    return sorted(set(flags))


@dataclass
class ServiceRecord:
    name: str
    path: Optional[str]
    language: str
    frameworks: List[str] = field(default_factory=list)
    compose_files: List[str] = field(default_factory=list)
    profiles: List[str] = field(default_factory=list)
    ports: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    env: List[str] = field(default_factory=list)
    feature_flags: List[str] = field(default_factory=list)
    healthz: bool = False
    readyz: bool = False
    metrics: bool = False


def collect_services() -> Dict[str, Any]:
    compose_data = load_compose_services()
    service_dirs = {}
    if SERVICES_DIR.exists():
        for path in SERVICES_DIR.iterdir():
            if path.is_dir() and not path.name.startswith("."):
                service_dirs[path.name] = path
    # Include selected app directories that behave like services.
    if FRONTEND_DIR.exists():
        service_dirs.setdefault("frontend", FRONTEND_DIR)
    for extra in ("apps/n8n", "apps/superset", "cli"):
        candidate = REPO_ROOT / extra
        if candidate.exists():
            service_dirs.setdefault(Path(extra).name, candidate)

    records: List[ServiceRecord] = []
    for name in sorted(set(list(compose_data.keys()) + list(service_dirs.keys()))):
        service_path = service_dirs.get(name)
        info = detect_language_and_framework(service_path) if service_path else {"language": "unknown", "frameworks": []}
        health_info = detect_health_endpoints(service_path) if service_path else {"healthz": False, "readyz": False, "metrics": False}
        compose_entry = compose_data.get(name, {})
        env_vars = compose_entry.get("env", [])
        record = ServiceRecord(
            name=name,
            path=str(service_path.relative_to(REPO_ROOT)) if service_path else None,
            language=info["language"],
            frameworks=info["frameworks"],
            compose_files=compose_entry.get("compose_files", []),
            profiles=compose_entry.get("profiles", []),
            ports=compose_entry.get("ports", []),
            depends_on=compose_entry.get("depends_on", []),
            env=env_vars,
            feature_flags=collect_feature_flags_from_env(env_vars),
            healthz=health_info.get("healthz", False),
            readyz=health_info.get("readyz", False),
            metrics=health_info.get("metrics", False),
        )
        records.append(record)

    return {
        "generated_at": iso_now(),
        "services": [asdict(record) for record in records],
    }


def _normalise_security_option(option: Any) -> str:
    if isinstance(option, str):
        return option.strip()
    return ""


def _ensure_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def collect_security_inventory() -> Dict[str, Any]:
    compose_globs = ["docker-compose*.yml", "docker-compose*.yaml", "auth-service-compose.yml"]
    compose_records: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {
            "compose_files": set(),
            "seccomp": set(),
            "apparmor": set(),
            "no_new_privileges": False,
            "cap_drop": set(),
            "cap_add": set(),
            "networks": set(),
            "internal_default": False,
            "unrestricted_network": False,
        }
    )

    for pattern in compose_globs:
        for path in REPO_ROOT.glob(pattern):
            try:
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                continue
            services = data.get("services") or {}
            networks = data.get("networks") or {}
            default_network = networks.get("default") if isinstance(networks, dict) else {}
            default_internal = bool(default_network.get("internal")) if isinstance(default_network, dict) else False
            internal_networks = {
                name
                for name, cfg in (networks.items() if isinstance(networks, dict) else [])
                if isinstance(cfg, dict) and cfg.get("internal")
            }
            for svc_name, cfg in services.items():
                record = compose_records[svc_name]
                record["compose_files"].add(str(path.relative_to(REPO_ROOT)))

                security_opts = [_normalise_security_option(opt) for opt in (cfg.get("security_opt") or [])]
                for opt in security_opts:
                    if opt.startswith("seccomp="):
                        record["seccomp"].add(opt.split("=", 1)[1])
                    elif opt.startswith("apparmor:"):
                        record["apparmor"].add(opt.split(":", 1)[1])
                    elif opt.startswith("no-new-privileges") and ("=true" in opt.lower() or ":true" in opt.lower()):
                        record["no_new_privileges"] = True

                for cap in _ensure_list(cfg.get("cap_drop")):
                    record["cap_drop"].add(cap)
                for cap in _ensure_list(cfg.get("cap_add")):
                    record["cap_add"].add(cap)

                raw_networks = cfg.get("networks")
                resolved_networks: Set[str] = set()
                if isinstance(raw_networks, list):
                    for item in raw_networks:
                        if isinstance(item, str):
                            resolved_networks.add(item)
                        elif isinstance(item, dict):
                            name = item.get("name")
                            if name:
                                resolved_networks.add(str(name))
                elif isinstance(raw_networks, dict):
                    for name in raw_networks.keys():
                        resolved_networks.add(str(name))
                else:
                    resolved_networks.add("default")

                for net in resolved_networks:
                    record["networks"].add(net)
                    if net == "egress":
                        record["unrestricted_network"] = True
                    elif net == "default":
                        if default_internal:
                            record["internal_default"] = True
                        else:
                            record["unrestricted_network"] = True
                    elif net in internal_networks:
                        record["internal_default"] = True
                    else:
                        record["unrestricted_network"] = True

    compose_summary = []
    for name, payload in sorted(compose_records.items()):
        cap_drop_list = sorted(payload["cap_drop"]) if payload["cap_drop"] else []
        cap_add_list = sorted(payload["cap_add"]) if payload["cap_add"] else []
        networks_list = sorted(payload["networks"]) if payload["networks"] else []
        if "egress" in networks_list:
            egress_policy = "egress-allowed"
        elif payload["internal_default"] and not payload["unrestricted_network"]:
            egress_policy = "internal-only"
        else:
            egress_policy = "unspecified"
        compose_summary.append(
            {
                "name": name,
                "compose_files": sorted(payload["compose_files"]),
                "seccomp": sorted(payload["seccomp"]),
                "apparmor": sorted(payload["apparmor"]),
                "no_new_privileges": payload["no_new_privileges"],
                "cap_drop": cap_drop_list,
                "cap_add": cap_add_list,
                "networks": networks_list,
                "egress_policy": egress_policy,
            }
        )

    k8s_path = REPO_ROOT / "deploy" / "kubernetes" / "production.yaml"
    kubernetes_summary: List[Dict[str, Any]] = []
    network_policies: List[Dict[str, Any]] = []
    if k8s_path.exists():
        try:
            docs = list(yaml.safe_load_all(k8s_path.read_text(encoding="utf-8")))
        except yaml.YAMLError:
            docs = []
        for doc in docs:
            if not isinstance(doc, dict):
                continue
            kind = doc.get("kind")
            metadata = doc.get("metadata", {})
            namespace = metadata.get("namespace", "infoterminal")
            if kind == "Deployment":
                template = doc.get("spec", {}).get("template", {})
                pod_meta = template.get("metadata", {})
                pod_spec = template.get("spec", {})
                annotations = pod_meta.get("annotations", {})
                pod_context = pod_spec.get("securityContext", {})
                containers_summary: List[Dict[str, Any]] = []
                for container in pod_spec.get("containers", []):
                    if not isinstance(container, dict):
                        continue
                    ctx = container.get("securityContext", {})
                    containers_summary.append(
                        {
                            "name": container.get("name"),
                            "allowPrivilegeEscalation": ctx.get("allowPrivilegeEscalation"),
                            "readOnlyRootFilesystem": ctx.get("readOnlyRootFilesystem"),
                            "runAsNonRoot": ctx.get("runAsNonRoot"),
                            "seccompProfile": ctx.get("seccompProfile"),
                            "capabilities": ctx.get("capabilities"),
                        }
                    )
                kubernetes_summary.append(
                    {
                        "name": metadata.get("name"),
                        "namespace": namespace,
                        "annotations": annotations,
                        "podSecurityContext": pod_context,
                        "containers": containers_summary,
                    }
                )
            elif kind == "NetworkPolicy":
                network_policies.append(
                    {
                        "name": metadata.get("name"),
                        "namespace": namespace,
                        "policyTypes": doc.get("policyTypes"),
                        "podSelector": doc.get("podSelector"),
                        "ingress": doc.get("ingress"),
                        "egress": doc.get("egress"),
                    }
                )

    return {
        "generated_at": iso_now(),
        "compose": compose_summary,
        "kubernetes": kubernetes_summary,
        "networkPolicies": network_policies,
    }


def build_observability_inventory(services_payload: Dict[str, Any]) -> Dict[str, Any]:
    required_labels = ["service", "version", "env"]
    optional_labels = ["tenant"]
    entries: List[Dict[str, Any]] = []

    for svc in services_payload.get("services", []):
        entries.append(
            {
                "name": svc.get("name"),
                "path": svc.get("path"),
                "language": svc.get("language"),
                "frameworks": svc.get("frameworks", []),
                "healthz": "/healthz" if svc.get("healthz") else None,
                "readyz": "/readyz" if svc.get("readyz") else None,
                "metrics": {
                    "path": "/metrics" if svc.get("metrics") else None,
                    "labels": required_labels if svc.get("metrics") else [],
                    "optional_labels": optional_labels,
                },
            }
        )

    return {
        "generated_at": iso_now(),
        "required_labels": required_labels,
        "optional_labels": optional_labels,
        "services": entries,
    }


def collect_api_inventory() -> Dict[str, Any]:
    services: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    if SERVICES_DIR.exists():
        for service_dir in sorted(p for p in SERVICES_DIR.iterdir() if p.is_dir() and not p.name.startswith(".")):
            endpoints = parity.collect_service_endpoints(service_dir)
            for endpoint in endpoints:
                services[endpoint.service].append(
                    {
                        "method": endpoint.method,
                        "path": endpoint.path,
                        "summary": endpoint.summary,
                        "status_codes": endpoint.status_codes,
                        "response_model": endpoint.response_model,
                        "source": endpoint.source,
                        "lineno": endpoint.lineno,
                    }
                )
    # Sort endpoints per service for deterministic output.
    for endpoint_list in services.values():
        endpoint_list.sort(key=lambda item: (item["path"], item["method"]))
    return {
        "generated_at": iso_now(),
        "services": dict(sorted(services.items())),
    }


def collect_db_inventory() -> Dict[str, Any]:
    postgres_items: List[Dict[str, Any]] = []
    neo4j_items: List[Dict[str, Any]] = []
    opensearch_items: List[Dict[str, Any]] = []

    migration_dirs = [
        path
        for path in REPO_ROOT.rglob("migrations")
        if path.is_dir() and "node_modules" not in path.parts and ".venv" not in path.parts
    ]
    for path in migration_dirs:
        owner: Optional[str] = None
        parts = list(path.relative_to(REPO_ROOT).parts)
        for idx, part in enumerate(parts):
            if part in {"services", "infra", "etl"} and idx + 1 < len(parts):
                owner = "/".join(parts[idx : idx + 2])
                break
        postgres_items.append(
            {
                "path": str(path.relative_to(REPO_ROOT)),
                "owner": owner,
                "files": sorted(
                    str(p.relative_to(REPO_ROOT))
                    for p in path.rglob("*")
                    if p.suffix in {".py", ".sql", ".sql.j2"}
                ),
            }
        )

    for ext in ("*.cql", "*.cypher", "*.cypherql"):
        for path in REPO_ROOT.rglob(ext):
            if any(part in {"node_modules", ".venv", "tests"} for part in path.parts):
                continue
            neo4j_items.append(
                {
                    "path": str(path.relative_to(REPO_ROOT)),
                    "size": path.stat().st_size,
                }
            )

    for ext in ("*index.json", "*mappings.json", "*opensearch.json"):
        for path in REPO_ROOT.rglob(ext):
            if any(part in {"node_modules", ".venv"} for part in path.parts):
                continue
            opensearch_items.append(
                {
                    "path": str(path.relative_to(REPO_ROOT)),
                    "size": path.stat().st_size,
                }
            )

    return {
        "generated_at": iso_now(),
        "postgres": sorted(postgres_items, key=lambda item: item["path"]),
        "neo4j": sorted(neo4j_items, key=lambda item: item["path"]),
        "opensearch": sorted(opensearch_items, key=lambda item: item["path"]),
    }


def derive_route_from_page(path: Path, base: Path) -> str:
    rel = path.relative_to(base)
    parts = list(rel.parts)
    if parts[-1].startswith("_"):
        return "#internal"
    stem = rel.with_suffix("")
    segments = []
    for part in stem.parts:
        if part == "index":
            continue
        segments.append(part)
    route = "/" + "/".join(segments)
    route = route.replace("//", "/")
    if route == "/":
        return route
    return route.rstrip("/") or "/"


def collect_frontend_inventory() -> Dict[str, Any]:
    pages: List[Dict[str, Any]] = []
    api_routes: List[Dict[str, Any]] = []
    feature_flags: Set[str] = set()

    pages_dir = FRONTEND_DIR / "pages"
    if pages_dir.exists():
        for path in sorted(pages_dir.rglob("*.tsx")):
            if "api" in path.relative_to(pages_dir).parts:
                continue
            route = derive_route_from_page(path, pages_dir)
            if route == "#internal":
                continue
            pages.append({
                "route": route,
                "file": str(path.relative_to(REPO_ROOT)),
            })

        api_dir = pages_dir / "api"
        if api_dir.exists():
            for path in sorted(api_dir.rglob("*.ts")):
                route = derive_route_from_page(path, api_dir)
                if route == "#internal":
                    continue
                api_routes.append(
                    {
                        "route": f"/api{'' if route == '/' else route}",
                        "file": str(path.relative_to(REPO_ROOT)),
                    }
                )

    # Feature toggles (NEXT_PUBLIC_*, FEATURE_*, ENABLE_* in frontend code).
    env_pattern = re.compile(r"process\.env\.([A-Z0-9_]+)")
    for path in FRONTEND_DIR.rglob("*"):
        if path.suffix not in {".ts", ".tsx"}:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in env_pattern.findall(content):
            if any(prefix in match for prefix in ("NEXT_PUBLIC", "FEATURE", "ENABLE", "FLAG")):
                feature_flags.add(match)

    return {
        "generated_at": iso_now(),
        "pages": pages,
        "api_routes": sorted(api_routes, key=lambda item: item["route"]),
        "feature_flags": sorted(feature_flags),
    }


def build_findings(services_payload: Dict[str, Any]) -> str:
    lines = ["# Inventory Findings", "", f"Generated: {iso_now()}", ""]
    missing_health: List[str] = []
    missing_ready: List[str] = []
    missing_metrics: List[str] = []
    for svc in services_payload.get("services", []):
        name = svc["name"]
        if not svc.get("healthz"):
            missing_health.append(name)
        if not svc.get("readyz"):
            missing_ready.append(name)
        if not svc.get("metrics"):
            missing_metrics.append(name)

    if missing_health:
        lines.append("## Services missing /healthz")
        lines.append("")
        for name in sorted(missing_health):
            lines.append(f"- {name}")
        lines.append("")

    if missing_ready:
        lines.append("## Services missing /readyz")
        lines.append("")
        for name in sorted(missing_ready):
            lines.append(f"- {name}")
        lines.append("")

    if missing_metrics:
        lines.append("## Services missing /metrics")
        lines.append("")
        for name in sorted(missing_metrics):
            lines.append(f"- {name}")
        lines.append("")

    if len(lines) <= 4:
        lines.append("No findings – all services expose healthz/readyz/metrics endpoints.")

    return "\n".join(lines).rstrip() + "\n"


def write_outputs(outputs: Dict[Path, str], dry_run: bool = False) -> None:
    for path, content in outputs.items():
        if dry_run:
            print(f"[dry-run] Would write {path.relative_to(REPO_ROOT)} ({len(content)} bytes)")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Preview generated files without writing to disk")
    args = parser.parse_args()

    services_payload = collect_services()
    apis_payload = collect_api_inventory()
    db_payload = collect_db_inventory()
    frontend_payload = collect_frontend_inventory()
    findings_report = build_findings(services_payload)
    observability_payload = build_observability_inventory(services_payload)
    security_payload = collect_security_inventory()

    outputs = {
        INVENTORY_DIR / "services.json": json.dumps(services_payload, indent=2, sort_keys=True) + "\n",
        INVENTORY_DIR / "apis.json": json.dumps(apis_payload, indent=2, sort_keys=True) + "\n",
        INVENTORY_DIR / "db.json": json.dumps(db_payload, indent=2, sort_keys=True) + "\n",
        INVENTORY_DIR / "frontend.json": json.dumps(frontend_payload, indent=2, sort_keys=True) + "\n",
        INVENTORY_DIR / "findings.md": findings_report,
        INVENTORY_DIR / "observability.json": json.dumps(observability_payload, indent=2, sort_keys=True) + "\n",
        INVENTORY_DIR / "security.json": json.dumps(security_payload, indent=2, sort_keys=True) + "\n",
    }

    write_outputs(outputs, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
