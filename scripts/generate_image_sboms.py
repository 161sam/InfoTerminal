#!/usr/bin/env python3
"""Generate CycloneDX SBOMs for container images and consolidate license metadata.

The script inspects all ``docker-compose*.yml`` files and the production Kubernetes
profile (``deploy/kubernetes/production.yaml``) to discover referenced container
images. For every image it ensures an SBOM exists under ``artifacts/sbom/images``
and aggregates license information into ``artifacts/compliance/licenses/images.json``.

Re-running is idempotent: artefacts are overwritten deterministically. Pass
``--dry-run`` (or set ``DRY_RUN=1``) to inspect planned work without executing
Docker/SBOM commands.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from shutil import which
from typing import Dict, Iterable, List, Sequence

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_GLOB = "docker-compose*.yml"
PROD_MANIFEST = REPO_ROOT / "deploy" / "kubernetes" / "production.yaml"
IMAGES_SBOM_DIR = REPO_ROOT / "artifacts" / "sbom" / "images"
LICENSE_OUTPUT = REPO_ROOT / "artifacts" / "compliance" / "licenses" / "images.json"


@dataclass
class ImageUsage:
    compose_services: List[str] = field(default_factory=list)
    manifest_refs: List[str] = field(default_factory=list)
    build_targets: List[str] = field(default_factory=list)

    def add_compose(self, descriptor: str, has_build: bool) -> None:
        if descriptor not in self.compose_services:
            self.compose_services.append(descriptor)
        if has_build and descriptor not in self.build_targets:
            self.build_targets.append(descriptor)

    def add_manifest(self, descriptor: str) -> None:
        if descriptor not in self.manifest_refs:
            self.manifest_refs.append(descriptor)

    @property
    def requires_build(self) -> bool:
        return bool(self.build_targets)

    def sources(self) -> List[str]:
        return self.compose_services + self.manifest_refs


class MissingSbomTool(RuntimeError):
    pass


def load_documents(path: Path) -> Iterable[dict]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:  # pragma: no cover - defensive filesystem guard
        raise RuntimeError(f"Failed to read YAML file: {path}\n{exc}") from exc

    try:
        documents = list(yaml.safe_load_all(raw))
    except yaml.YAMLError:
        try:
            single = yaml.safe_load(raw)
        except yaml.YAMLError as exc:  # pragma: no cover - defensive parsing guard
            raise RuntimeError(f"Failed to parse YAML: {path}\n{exc}") from exc
        else:
            if isinstance(single, dict):
                yield single
            return

    for doc in documents:
        if isinstance(doc, dict):
            yield doc


def fallback_parse_compose(path: Path) -> List[tuple[str, str, bool]]:
    """Very small parser for indented docker-compose fragments."""
    entries: List[tuple[str, str, bool]] = []
    current_name: str | None = None
    current_image: str | None = None
    current_has_build = False

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.rstrip()
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            service_match = re.match(r"^(?P<indent>\s*)([\w.-]+):\s*$", line)
            if service_match:
                indent = len(service_match.group("indent"))
                name = service_match.group(2)
                if indent <= 2:
                    if current_name and current_image:
                        entries.append((current_name, current_image, current_has_build))
                    current_name = name
                    current_image = None
                    current_has_build = False
                continue
            if current_name is None:
                continue
            image_match = re.match(r"^\s*image:\s*(\S.*)$", line)
            if image_match:
                current_image = image_match.group(1).strip()
                continue
            build_match = re.match(r"^\s*build:.*$", line)
            if build_match:
                current_has_build = True
                continue
        if current_name and current_image:
            entries.append((current_name, current_image, current_has_build))
    return entries


def collect_images() -> Dict[str, ImageUsage]:
    images: Dict[str, ImageUsage] = {}

    for compose_path in sorted(REPO_ROOT.glob(COMPOSE_GLOB)):
        rel_path = compose_path.relative_to(REPO_ROOT)
        try:
            documents = list(load_documents(compose_path))
        except RuntimeError as exc:
            print(f"[warn] {exc}; falling back to heuristic parser")
            documents = []

        if documents:
            for doc in documents:
                services = doc.get("services")
                if not isinstance(services, dict):
                    continue
                for service_name, service in services.items():
                    if not isinstance(service, dict):
                        continue
                    image = service.get("image")
                    if not image:
                        continue
                    usage = images.setdefault(image, ImageUsage())
                    descriptor = f"{rel_path}::{service_name}"
                    usage.add_compose(descriptor, has_build=bool(service.get("build")))
        else:
            for service_name, image, has_build in fallback_parse_compose(compose_path):
                usage = images.setdefault(image, ImageUsage())
                descriptor = f"{rel_path}::{service_name}"
                usage.add_compose(descriptor, has_build=has_build)

    if PROD_MANIFEST.exists():
        rel_prod = PROD_MANIFEST.relative_to(REPO_ROOT)
        for doc in load_documents(PROD_MANIFEST):
            kind = doc.get("kind", "<unknown>")
            meta = doc.get("metadata") or {}
            meta_name = meta.get("name", "<unnamed>")
            spec = doc.get("spec") or {}
            template = spec.get("template") or {}
            pod_spec = template.get("spec") or {}
            containers = list(pod_spec.get("containers") or [])
            containers.extend(pod_spec.get("initContainers") or [])
            for container in containers:
                if not isinstance(container, dict):
                    continue
                image = container.get("image")
                if not image:
                    continue
                usage = images.setdefault(image, ImageUsage())
                container_name = container.get("name", "<container>")
                descriptor = f"{rel_prod}::{kind}/{meta_name}::{container_name}"
                usage.add_manifest(descriptor)

    return images


def ensure_image_available(image: str, usage: ImageUsage, *, dry_run: bool, auto_build: bool) -> None:
    inspect_cmd = ["docker", "image", "inspect", image]
    if dry_run:
        print(f"[dry-run] docker image inspect {image}")
        if usage.requires_build:
            build_hint = usage.build_targets[0]
            compose_file, service = build_hint.split("::", 1)
            if auto_build:
                print(
                    "[dry-run] docker compose -f"
                    f" {compose_file} build {service}"
                )
            else:
                print(
                    "[dry-run] missing image would require manual build: "
                    f"docker compose -f {compose_file} build {service}"
                )
        else:
            print(f"[dry-run] docker pull {image}")
        return
    inspect = subprocess.run(inspect_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if inspect.returncode == 0:
        return

    if usage.requires_build:
        build_hint = usage.build_targets[0]
        compose_file, service = build_hint.split("::", 1)
        if not auto_build:
            raise RuntimeError(
                "Container image not present locally. Build the service first: "
                f"docker compose -f {compose_file} build {service}"
            )
        build_cmd = [
            "docker",
            "compose",
            "-f",
            compose_file,
            "build",
            service,
        ]
        subprocess.run(build_cmd, check=True)
        inspect = subprocess.run(
            inspect_cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if inspect.returncode == 0:
            return
        raise RuntimeError(
            f"Image {image} still missing after auto build: docker compose -f {compose_file} build {service}"
        )

    pull_cmd = ["docker", "pull", image]
    subprocess.run(pull_cmd, check=True)


def detect_sbom_tool() -> Sequence[str]:
    env_tool = os.environ.get("SBOM_IMAGE_TOOL")
    if env_tool:
        return env_tool.split()

    if which("syft"):
        return ("syft",)

    docker_path = which("docker")
    if docker_path:
        probe = subprocess.run([
            docker_path,
            "sbom",
            "--help",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if probe.returncode == 0:
            return (docker_path, "sbom")

    raise MissingSbomTool(
        "No supported SBOM tool detected. Install `syft` (preferred) or Docker CLI >= 23 "
        "with the `docker sbom` plugin, or set SBOM_IMAGE_TOOL explicitly."
    )


def sanitise_filename(image: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", image)
    return f"{safe}.cdx.json"


def run_sbom_command(tool: Sequence[str], image: str, output_path: Path, *, dry_run: bool) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[dry-run] {' '.join(tool)} {image} -> {output_path.relative_to(REPO_ROOT)}")
        return

    if tool[0].endswith("syft") and len(tool) == 1:
        cmd = ["syft", image, "-o", "cyclonedx-json"]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_path.write_bytes(result.stdout)
    elif tool[0].endswith("docker") and len(tool) >= 2 and tool[1] == "sbom":
        cmd = list(tool) + ["--format", "cyclonedx-json", "--output", str(output_path), image]
        subprocess.run(cmd, check=True)
    else:
        raise MissingSbomTool(
            "Unsupported SBOM tool configuration. Use syft or docker sbom, or set SBOM_IMAGE_TOOL."
        )

    if output_path.stat().st_size == 0:
        raise RuntimeError(f"Generated SBOM is empty: {output_path}")


def normalize_license(component: dict) -> List[str]:
    licenses: List[str] = []
    for entry in component.get("licenses", []) or []:
        if isinstance(entry, dict) and "license" in entry:
            license_obj = entry.get("license")
            if isinstance(license_obj, dict):
                name = license_obj.get("name") or license_obj.get("id")
                if name:
                    value = str(name).strip()
                    if value and value not in licenses:
                        licenses.append(value)
        elif isinstance(entry, dict) and entry.get("expression"):
            value = str(entry["expression"]).strip()
            if value and value not in licenses:
                licenses.append(value)
    if not licenses:
        return ["UNKNOWN"]
    return licenses


def aggregate_licenses(sbom_map: Dict[str, Path], usages: Dict[str, ImageUsage]) -> Dict[str, dict]:
    results: Dict[str, dict] = {}
    for image, sbom_path in sbom_map.items():
        if not sbom_path.exists():
            continue
        with sbom_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        components = data.get("components", []) or []
        unique_licenses: List[str] = []
        unknown_components: List[str] = []
        for component in components:
            if not isinstance(component, dict):
                continue
            component_name = component.get("name")
            component_version = component.get("version")
            component_id = "::".join(
                str(part)
                for part in (component_name, component_version)
                if part
            )
            normalized = normalize_license(component)
            if normalized == ["UNKNOWN"]:
                if component_id and component_id not in unknown_components:
                    unknown_components.append(component_id)
            for lic in normalized:
                if lic != "UNKNOWN" and lic not in unique_licenses:
                    unique_licenses.append(lic)
        results[image] = {
            "sbom": str(sbom_path.relative_to(REPO_ROOT)),
            "licenses": sorted(unique_licenses),
            "unknown_components": sorted(unknown_components),
            "component_count": len(components),
            "sources": usages.get(image).sources() if image in usages else [],
            "requires_build": usages.get(image).requires_build if image in usages else False,
        }
    return results


def write_license_report(data: Dict[str, dict], *, dry_run: bool) -> None:
    LICENSE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "images": [
            {
                "image": image,
                **details,
            }
            for image, details in sorted(data.items())
        ],
    }
    if dry_run:
        print(f"[dry-run] write {LICENSE_OUTPUT.relative_to(REPO_ROOT)}")
        return
    with LICENSE_OUTPUT.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=False)
        handle.write("\n")
    if LICENSE_OUTPUT.stat().st_size == 0:
        raise RuntimeError(f"License inventory generation failed: {LICENSE_OUTPUT}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate container image SBOMs and license inventory")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned actions without generating SBOMs or writing artefacts",
    )
    parser.add_argument(
        "--auto-build",
        action="store_true",
        help="Attempt to docker compose build missing local images before generating SBOMs",
    )
    return parser.parse_args()


def resolve_dry_run_flag(args: argparse.Namespace) -> bool:
    if args.dry_run:
        return True
    env = os.environ.get("DRY_RUN", "0").lower()
    return env in {"1", "true", "yes", "on"}


def resolve_auto_build_flag(args: argparse.Namespace) -> bool:
    if args.auto_build:
        return True
    env = os.environ.get("AUTO_BUILD", "0").lower()
    return env in {"1", "true", "yes", "on"}


def main() -> None:
    args = parse_args()
    dry_run = resolve_dry_run_flag(args)
    auto_build = resolve_auto_build_flag(args)

    images = collect_images()
    if not images:
        raise SystemExit("No container images detected in compose/prod manifests")

    tool = ()
    if not dry_run:
        tool = detect_sbom_tool()
    else:
        print("Running in dry-run mode; no SBOM tool lookup performed")
    if auto_build:
        print("Auto-build enabled for missing local images")

    generated_sboms: Dict[str, Path] = {}
    for image, usage in sorted(images.items()):
        output_path = IMAGES_SBOM_DIR / sanitise_filename(image)
        generated_sboms[image] = output_path
        print(f"Processing image: {image}")
        print(f"  Sources: {', '.join(usage.sources())}")
        ensure_image_available(image, usage, dry_run=dry_run, auto_build=auto_build)
        if not dry_run:
            run_sbom_command(tool, image, output_path, dry_run=dry_run)

    license_data = aggregate_licenses(generated_sboms, images)
    write_license_report(license_data, dry_run=dry_run)

    print("Generated SBOMs:")
    for image, path in sorted(generated_sboms.items()):
        status = "(missing)"
        if path.exists():
            status = "(ok)"
        elif dry_run:
            status = "(skipped)"
        print(f" - {image}: {path.relative_to(REPO_ROOT)} {status}")
    print(f"License inventory: {LICENSE_OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
