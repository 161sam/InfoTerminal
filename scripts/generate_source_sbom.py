#!/usr/bin/env python3
"""Generate CycloneDX SBOMs for source dependencies and consolidate licenses.

The script refreshes Python SBOMs via ``cyclonedx-py`` and Node SBOMs via
``@appthreat/cdxgen`` before merging both into ``artifacts/compliance/licenses``.
Re-running is idempotent; existing artefakte werden deterministisch überschrieben.
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_SOURCES_DIR = REPO_ROOT / "artifacts" / "sbom" / "source"
LICENSE_DIR = REPO_ROOT / "artifacts" / "compliance" / "licenses"

@dataclass(frozen=True)
class PythonProject:
    name: str
    requirements_file: Path
    pyproject_file: Path
    output_name: str

@dataclass(frozen=True)
class NodeWorkspace:
    name: str
    manifest_dir: Path
    project_path: Path
    output_name: str


PYTHON_PROJECTS: Tuple[PythonProject, ...] = (
    PythonProject(
        name="graph-views-backend",
        requirements_file=REPO_ROOT / "services" / "graph-views" / "requirements-dev.txt",
        pyproject_file=REPO_ROOT / "services" / "graph-views" / "pyproject.toml",
        output_name="backend-python.cdx.json",
    ),
)

NODE_WORKSPACES: Tuple[NodeWorkspace, ...] = (
    NodeWorkspace(
        name="frontend-workspace",
        manifest_dir=REPO_ROOT,
        project_path=Path("apps/frontend"),
        output_name="frontend-node.cdx.json",
    ),
)


def _check_dependency(module: str, package: str) -> None:
    """Ensure a Python module is available, attempting to install if missing."""
    try:
        __import__(module)
    except ModuleNotFoundError:  # pragma: no cover - executed only on missing deps
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def _run(cmd: List[str], *, cwd: Path | None = None) -> None:
    subprocess.run(cmd, check=True, cwd=cwd)


def generate_python_sboms() -> List[Path]:
    _check_dependency("cyclonedx_py", "cyclonedx-bom>=7.1.0")
    outputs: List[Path] = []
    for project in PYTHON_PROJECTS:
        if not project.requirements_file.exists():
            raise FileNotFoundError(f"Missing requirements file: {project.requirements_file}")
        if not project.pyproject_file.exists():
            raise FileNotFoundError(f"Missing pyproject metadata: {project.pyproject_file}")
        output_path = ARTIFACT_SOURCES_DIR / project.output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            sys.executable,
            "-m",
            "cyclonedx_py",
            "requirements",
            str(project.requirements_file),
            "--pyproject",
            str(project.pyproject_file),
            "--output-reproducible",
            "--of",
            "JSON",
            "-o",
            str(output_path),
        ]
        _run(cmd, cwd=REPO_ROOT)
        if output_path.stat().st_size == 0:
            raise RuntimeError(f"Generated SBOM is empty: {output_path}")
        outputs.append(output_path)
    return outputs


def generate_node_sboms() -> List[Path]:
    outputs: List[Path] = []
    for workspace in NODE_WORKSPACES:
        project_dir = workspace.manifest_dir / workspace.project_path
        if not project_dir.exists():
            raise FileNotFoundError(f"Missing workspace directory: {project_dir}")
        lockfile = workspace.manifest_dir / "pnpm-lock.yaml"
        if not lockfile.exists():
            raise FileNotFoundError(f"Missing lockfile: {lockfile}")
        output_path = ARTIFACT_SOURCES_DIR / workspace.output_name
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cmd = [
            "npx",
            "--yes",
            "@appthreat/cdxgen@7.0.5",
            "-t",
            "npm",
            "-p",
            str(project_dir),
            "-o",
            str(output_path),
        ]
        _run(cmd, cwd=workspace.manifest_dir)
        xml_path = Path(str(output_path).replace(".cdx.json", ".cdx.xml"))
        if xml_path.exists():
            xml_path.unlink()
        if output_path.stat().st_size == 0:
            raise RuntimeError(f"Generated SBOM is empty: {output_path}")
        outputs.append(output_path)
    return outputs


def _normalise_license(component: Dict) -> str:
    licenses = []
    for license_entry in component.get("licenses", []) or []:
        lic = license_entry.get("license") or {}
        if isinstance(lic, dict):
            if lic.get("name"):
                licenses.append(str(lic["name"]))
            elif lic.get("id"):
                licenses.append(str(lic["id"]))
        elif isinstance(license_entry, dict) and license_entry.get("expression"):
            licenses.append(str(license_entry["expression"]))
    if not licenses:
        return "UNKNOWN"
    return "; ".join(dict.fromkeys(licenses))


def _extract_url(component: Dict) -> str:
    for ref in component.get("externalReferences", []) or []:
        if ref.get("url") and ref.get("type") in {"website", "vcs", "distribution"}:
            return str(ref["url"])
    if component.get("purl") and component.get("purl").startswith("pkg:npm/"):
        name = component.get("name", "")
        return f"https://www.npmjs.com/package/{name}"
    return ""


def _normalise_repo_url(raw_url: str | None) -> str | None:
    if not raw_url:
        return None
    url = raw_url.strip()
    if url.startswith("git+"):
        url = url[4:]
    return url or None


def _read_node_package_metadata(component: Dict) -> Tuple[str | None, str | None]:
    for prop in component.get("properties", []) or []:
        if prop.get("name") == "SrcFile":
            package_json_path = Path(prop.get("value", ""))
            if package_json_path.exists():
                try:
                    with package_json_path.open("r", encoding="utf-8") as handle:
                        data = json.load(handle)
                except (OSError, json.JSONDecodeError):
                    return None, None
                license_field = data.get("license")
                license_value: str | None = None
                if isinstance(license_field, str):
                    license_value = license_field
                elif isinstance(license_field, dict):
                    license_value = license_field.get("type") or license_field.get("name")
                elif isinstance(license_field, list):
                    collected: List[str] = []
                    for item in license_field:
                        if isinstance(item, dict):
                            value = item.get("type") or item.get("name")
                        else:
                            value = str(item)
                        if value:
                            collected.append(value)
                    if collected:
                        license_value = "; ".join(dict.fromkeys(collected))
                repo_url = data.get("repository")
                homepage = data.get("homepage")
                if isinstance(repo_url, dict):
                    repo_url = repo_url.get("url")
                repo_url = _normalise_repo_url(repo_url) or _normalise_repo_url(homepage)
                return (license_value.strip() if isinstance(license_value, str) else license_value), repo_url
    return None, None


@lru_cache(maxsize=64)
def _read_python_metadata(package: str, version: str) -> Tuple[str | None, str | None]:
    url = f"https://pypi.org/pypi/{package}/{version}/json"
    try:
        with urlopen(url, timeout=10) as response:  # type: ignore[arg-type]
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return None, None
    info = payload.get("info", {}) if isinstance(payload, dict) else {}
    license_value = info.get("license")
    if isinstance(license_value, str):
        license_value = license_value.strip()
    if not license_value or license_value.lower() == "unknown":
        classifiers = info.get("classifiers", []) or []
        license_entries = [
            classifier.split("::")[-1].strip()
            for classifier in classifiers
            if isinstance(classifier, str) and classifier.startswith("License ::")
        ]
        if license_entries:
            license_value = "; ".join(dict.fromkeys(license_entries))
    project_urls = info.get("project_urls", {}) or {}
    homepage = info.get("home_page") or info.get("project_url")
    repo_url = None
    for key in (
        "Homepage",
        "Repository",
        "Source",
        "Source Code",
        "Source code",
        "Source Repository",
    ):
        if project_urls.get(key):
            repo_url = project_urls[key]
            break
    if not repo_url:
        repo_url = homepage
    return (license_value if license_value else None), repo_url


def consolidate_licenses(sbom_paths: Iterable[Path]) -> None:
    inventory: Dict[Tuple[str, str, str], Dict[str, str]] = {}
    for sbom_path in sbom_paths:
        with sbom_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        ecosystem = "python" if "python" in sbom_path.name else "node"
        for component in data.get("components", []) or []:
            name = component.get("name")
            version = component.get("version", "")
            if not name or not version:
                continue
            key = (ecosystem, name, version)
            license_name = _normalise_license(component)
            url = _extract_url(component)
            if ecosystem == "node":
                extra_license, extra_url = _read_node_package_metadata(component)
            else:
                extra_license, extra_url = _read_python_metadata(name, version)
            if license_name == "UNKNOWN" and extra_license:
                license_name = extra_license
            if ecosystem == "node":
                fallback_url = "npmjs.com/package"
            else:
                fallback_url = "pypi.org/simple"
            if (not url or fallback_url in url) and extra_url:
                url = extra_url
            entry = inventory.get(key, {
                "ecosystem": ecosystem,
                "name": name,
                "version": version,
                "license": license_name,
                "url": url,
                "source_bom": sbom_path.name,
            })
            if not entry.get("license") or entry["license"] == "UNKNOWN":
                entry["license"] = license_name
            if not entry.get("url"):
                entry["url"] = url
            entry["source_bom"] = sbom_path.name
            inventory[key] = entry
    ordered_entries = sorted(inventory.values(), key=lambda item: (item["ecosystem"], item["name"].lower(), item["version"]))
    LICENSE_DIR.mkdir(parents=True, exist_ok=True)
    json_path = LICENSE_DIR / "license_inventory.json"
    csv_path = LICENSE_DIR / "license_inventory.csv"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(ordered_entries, handle, indent=2, sort_keys=False)
        handle.write("\n")
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ecosystem", "name", "version", "license", "url", "source_bom"])
        writer.writeheader()
        writer.writerows(ordered_entries)
    if json_path.stat().st_size == 0 or csv_path.stat().st_size == 0:
        raise RuntimeError("License inventory generation failed: empty file produced")


def main() -> None:
    ARTIFACT_SOURCES_DIR.mkdir(parents=True, exist_ok=True)
    generated_sboms: List[Path] = []
    generated_sboms.extend(generate_python_sboms())
    generated_sboms.extend(generate_node_sboms())
    consolidate_licenses(generated_sboms)
    print("Generated SBOMs:")
    for path in generated_sboms:
        print(f" - {path.relative_to(REPO_ROOT)}")
    print("License inventory:")
    for path in sorted(LICENSE_DIR.glob("license_inventory.*")):
        print(f" - {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
