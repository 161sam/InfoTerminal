#!/usr/bin/env python3
"""Run dependency SCA (Python & Node) and enforce the vuln_policy_sca gate."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.error import HTTPError, URLError

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "security" / "sca"
PYTHON_DIR = ARTIFACT_ROOT / "python"
NODE_DIR = ARTIFACT_ROOT / "node"
SUMMARY_JSON = ARTIFACT_ROOT / "sca_summary.json"
SUMMARY_HTML = ARTIFACT_ROOT / "sca_summary.html"
PR_COMMENT_PATH = ARTIFACT_ROOT / "pr_comment.md"
POLICY_PATH = REPO_ROOT / "policy" / "vuln_policy_sca.json"
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"
PYTHON_REQ_PATTERN = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]+\])?==([A-Za-z0-9][A-Za-z0-9._+!\-]*)$")
OSV_VULN_URL = "https://api.osv.dev/v1/vulns/"
OSV_VULN_CACHE: Dict[str, dict] = {}

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info", "unknown"]
SEVERITY_WEIGHTS = {name: weight for weight, name in enumerate(reversed(SEVERITY_ORDER))}
SEVERITY_WEIGHTS.update({name: len(SEVERITY_ORDER) for name in ("moderate", "medium")})
DEFAULT_POLICY = {"fail_threshold": "high", "warn_threshold": "medium"}
ENV_FAIL = "VULN_POLICY_SCA_FAIL_LEVEL"
ENV_WARN = "VULN_POLICY_SCA_WARN_LEVEL"
EXCLUDED_DIRS = {"node_modules", ".git", "artifacts", ".venv", "__pycache__"}


class ScanError(RuntimeError):
    """Raised when an underlying SCA tool fails."""


def load_policy() -> Dict[str, str]:
    policy = DEFAULT_POLICY.copy()
    if POLICY_PATH.exists():
        try:
            loaded = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # pragma: no cover - configuration error
            raise SystemExit(f"Invalid JSON in {POLICY_PATH}: {exc}") from exc
        if isinstance(loaded, dict):
            policy.update({k: str(v) for k, v in loaded.items() if v is not None})
    if os.getenv(ENV_FAIL):
        policy["fail_threshold"] = os.environ[ENV_FAIL]
    if os.getenv(ENV_WARN):
        policy["warn_threshold"] = os.environ[ENV_WARN]
    for key in ("fail_threshold", "warn_threshold"):
        value = policy.get(key, "").lower()
        if value not in SEVERITY_ORDER:
            raise SystemExit(
                f"Unsupported severity '{policy.get(key)}' for {key}. "
                f"Valid options: {', '.join(SEVERITY_ORDER)}"
            )
        policy[key] = value
    return policy


def levels_at_or_above(threshold: str) -> Tuple[str, ...]:
    idx = SEVERITY_ORDER.index(threshold)
    return tuple(SEVERITY_ORDER[: idx + 1])


def find_python_manifests() -> List[Path]:
    patterns = ("requirements*.txt", "Pipfile.lock", "poetry.lock")
    manifests: List[Path] = []
    for pattern in patterns:
        for path in REPO_ROOT.rglob(pattern):
            if any(part in EXCLUDED_DIRS for part in path.parts):
                continue
            if path.is_file():
                manifests.append(path)
    return sorted({p for p in manifests})


def sanitize_name(path: Path) -> str:
    rel = path.relative_to(REPO_ROOT).as_posix()
    return rel.replace("/", "__")


def run_command(command: List[str]) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment error
        raise ScanError(f"Command not found: {command[0]}") from exc
    return result


def run_pip_audit(manifest: Path) -> dict:
    pinned, skipped = parse_python_requirements(manifest)
    dependencies: List[dict] = []
    if pinned:
        results = query_osv_batch(pinned)
        if len(results) != len(pinned):
            raise ScanError(
                f"OSV returned {len(results)} results for {len(pinned)} requirements in {manifest}"
            )
        for (name, version), result in zip(pinned, results):
            vulns = []
            for vuln_ref in result.get("vulns", []) or []:
                vuln_id = vuln_ref.get("id") if isinstance(vuln_ref, dict) else None
                vuln_data = fetch_osv_vuln(vuln_id) if vuln_id else vuln_ref
                if not isinstance(vuln_data, dict):
                    continue
                severity = severity_from_osv(vuln_data)
                fix_versions = fix_versions_from_osv(vuln_data)
                references = [ref.get("url") for ref in vuln_data.get("references", []) if ref.get("url")]
                vulns.append(
                    {
                        "id": vuln_data.get("id") or vuln_id,
                        "source_id": vuln_data.get("id") or vuln_id,
                        "package": name,
                        "version": version,
                        "ecosystem": "python",
                        "severity": severity,
                        "description": vuln_data.get("summary") or vuln_data.get("details", ""),
                        "aliases": vuln_data.get("aliases") or [],
                        "fix_versions": fix_versions,
                        "references": references,
                    }
                )
            dependencies.append({"name": name, "version": version, "vulns": vulns})
    return {"dependencies": dependencies, "skipped": skipped, "queries": pinned}


def parse_python_requirements(manifest: Path) -> Tuple[List[Tuple[str, str]], List[str]]:
    pinned: List[Tuple[str, str]] = []
    skipped: List[str] = []
    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        no_comment = line.split("#", 1)[0].strip()
        if not no_comment:
            continue
        if no_comment.startswith(("-r", "--", "git+", "http://", "https://")):
            skipped.append(raw_line)
            continue
        requirement = no_comment.split(";", 1)[0].strip()
        match = PYTHON_REQ_PATTERN.match(requirement)
        if match:
            pinned.append((match.group(1), match.group(2)))
        else:
            skipped.append(raw_line)
    return pinned, skipped


def query_osv_batch(packages: List[Tuple[str, str]]) -> List[dict]:
    results: List[dict] = []
    chunk_size = 100
    for start in range(0, len(packages), chunk_size):
        chunk = packages[start : start + chunk_size]
        body = {
            "queries": [
                {"package": {"name": name, "ecosystem": "PyPI"}, "version": version}
                for name, version in chunk
            ]
        }
        request = urllib.request.Request(
            OSV_BATCH_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                payload = json.load(response)
        except (HTTPError, URLError, TimeoutError) as exc:  # pragma: no cover - network error
            raise ScanError(f"OSV query failed: {exc}") from exc
        chunk_results = payload.get("results")
        if not isinstance(chunk_results, list):
            raise ScanError("OSV response missing 'results' list")
        results.extend(chunk_results)
    return results


def fetch_osv_vuln(vuln_id: str) -> dict:
    if vuln_id in OSV_VULN_CACHE:
        return OSV_VULN_CACHE[vuln_id]
    request = urllib.request.Request(OSV_VULN_URL + vuln_id, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError) as exc:  # pragma: no cover - network error
        raise ScanError(f"Failed to fetch OSV details for {vuln_id}: {exc}") from exc
    OSV_VULN_CACHE[vuln_id] = payload
    return payload


def severity_from_osv(vuln: dict) -> str:
    scores = []
    for entry in vuln.get("severity", []):
        score = entry.get("score")
        if not score:
            continue
        try:
            scores.append(float(score))
        except ValueError:  # pragma: no cover - upstream format change
            continue
    if scores:
        best = max(scores)
        if best >= 9.0:
            return "critical"
        if best >= 7.0:
            return "high"
        if best >= 4.0:
            return "medium"
        if best > 0:
            return "low"
    db_specific = vuln.get("database_specific", {})
    if isinstance(db_specific, dict) and db_specific.get("severity"):
        return normalise_severity(str(db_specific["severity"]))
    return "unknown"


def fix_versions_from_osv(vuln: dict) -> List[str]:
    fixes = set()
    for affected in vuln.get("affected", []):
        for rng in affected.get("ranges", []):
            for event in rng.get("events", []):
                fixed = event.get("fixed")
                if fixed:
                    fixes.add(str(fixed))
        database_specific = affected.get("database_specific")
        if isinstance(database_specific, dict):
            fixed = database_specific.get("fixed")
            if isinstance(fixed, (list, tuple)):
                fixes.update(str(item) for item in fixed)
            elif fixed:
                fixes.add(str(fixed))
    return sorted(fixes)


def _python_dependencies(data: dict | List[dict]) -> List[dict]:
    if isinstance(data, dict):
        deps = data.get("dependencies", [])
        if isinstance(deps, list):
            return deps
        raise ScanError("pip-audit JSON payload missing 'dependencies' list")
    if isinstance(data, list):
        return data
    raise ScanError("Unexpected pip-audit JSON structure")


def collect_python_vulns(manifest: Path, data: dict | List[dict]) -> Tuple[List[dict], Counter]:
    dependencies = _python_dependencies(data)
    vulns: List[dict] = []
    counts: Counter = Counter({key: 0 for key in SEVERITY_ORDER})
    for package in dependencies:
        pkg_name = package.get("name", "")
        pkg_version = package.get("version", "")
        for vuln in package.get("vulns", []):
            severity = normalise_severity(vuln.get("severity"))
            counts[severity] += 1
            aliases = vuln.get("aliases") or []
            cve = next((alias for alias in aliases if alias.startswith("CVE-")), None)
            identifier = cve or vuln.get("id") or f"{pkg_name}:{pkg_version}"
            references = vuln.get("references") or []
            vulns.append(
                {
                    "id": identifier,
                    "source_id": vuln.get("id"),
                    "package": pkg_name,
                    "version": pkg_version,
                    "ecosystem": "python",
                    "manifest": manifest.relative_to(REPO_ROOT).as_posix(),
                    "severity": severity,
                    "description": vuln.get("description", ""),
                    "fix_versions": vuln.get("fix_versions", []),
                    "aliases": aliases,
                    "references": references,
                }
            )
    return vulns, counts


def run_pnpm_audit() -> dict:
    cmd = ["pnpm", "audit", "--json"]
    result = run_command(cmd)
    if result.returncode not in (0, 1):
        raise ScanError(
            f"pnpm audit failed (exit {result.returncode}):\n{result.stderr.strip()}"
        )
    payload = result.stdout.strip() or "{}"
    try:
        return json.loads(payload)
    except json.JSONDecodeError as exc:  # pragma: no cover - tool output change
        raise ScanError(f"pnpm audit returned invalid JSON: {exc}") from exc


def collect_node_vulns(data: dict) -> Tuple[List[dict], Counter]:
    counts = Counter({key: 0 for key in SEVERITY_ORDER})
    vulnerabilities: List[dict] = []
    metadata = data.get("metadata", {})
    meta_counts = metadata.get("vulnerabilities", {})
    for severity, value in meta_counts.items():
        counts[normalise_severity(severity)] += int(value or 0)
    for advisory in (data.get("advisories") or {}).values():
        severity = normalise_severity(advisory.get("severity"))
        if severity not in SEVERITY_ORDER:
            continue
        module = advisory.get("module_name") or advisory.get("module", "")
        cves = advisory.get("cves") or []
        identifier = cves[0] if cves else advisory.get("github_advisory_id") or str(advisory.get("id"))
        findings = advisory.get("findings") or []
        versions = sorted({f"{module}@{finding.get('version','')}" for finding in findings if finding.get("version")})
        paths = sorted({path for finding in findings for path in finding.get("paths", [])})
        references = advisory.get("references") or ""
        reference_lines = [ref.strip("- ") for ref in references.splitlines() if ref.strip()]
        vulnerabilities.append(
            {
                "id": identifier,
                "source_id": advisory.get("github_advisory_id") or str(advisory.get("id")),
                "package": module,
                "version": ", ".join(versions) if versions else "",
                "ecosystem": "node",
                "severity": severity,
                "description": advisory.get("title") or advisory.get("overview", ""),
                "fix_versions": [advisory.get("patched_versions") or ""],
                "aliases": cves,
                "references": reference_lines or [advisory.get("url", "")],
                "paths": paths,
            }
        )
    return vulnerabilities, counts


def normalise_severity(value: str | None) -> str:
    if not value:
        return "unknown"
    lowered = value.lower()
    if lowered in ("moderate", "medium"):
        return "medium"
    if lowered not in SEVERITY_ORDER:
        return "unknown"
    return lowered


def write_json(path: Path, payload: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
        handle.write("\n")


def ensure_clean_dirs() -> None:
    for directory in (PYTHON_DIR, NODE_DIR):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)


def aggregate_vulnerabilities(vulns: Iterable[dict]) -> List[dict]:
    aggregated: Dict[str, dict] = {}
    for vuln in vulns:
        identifier = vuln["id"]
        entry = aggregated.setdefault(
            identifier,
            {
                "id": identifier,
                "severity": vuln["severity"],
                "ecosystems": set(),
                "packages": set(),
                "manifests": set(),
                "fix_versions": set(),
                "references": set(),
                "descriptions": set(),
                "aliases": set(),
                "occurrences": 0,
            },
        )
        entry["ecosystems"].add(vuln.get("ecosystem", "unknown"))
        if vuln.get("package"):
            entry["packages"].add(vuln["package"])
        if vuln.get("version"):
            entry["packages"].add(f"{vuln['package']}@{vuln['version']}")
        if vuln.get("manifest"):
            entry["manifests"].add(vuln["manifest"])
        for fix in vuln.get("fix_versions", []):
            if fix:
                entry["fix_versions"].add(str(fix))
        for ref in vuln.get("references", []):
            if ref:
                entry["references"].add(ref)
        if vuln.get("description"):
            entry["descriptions"].add(vuln["description"])
        for alias in vuln.get("aliases", []):
            if alias:
                entry["aliases"].add(alias)
        entry["occurrences"] += 1
        existing_weight = SEVERITY_WEIGHTS.get(entry["severity"], 0)
        new_weight = SEVERITY_WEIGHTS.get(vuln["severity"], 0)
        if new_weight > existing_weight:
            entry["severity"] = vuln["severity"]
    normalised: List[dict] = []
    for entry in aggregated.values():
        normalised.append(
            {
                "id": entry["id"],
                "severity": entry["severity"],
                "ecosystems": sorted(entry["ecosystems"]),
                "packages": sorted(entry["packages"]),
                "manifests": sorted(entry["manifests"]),
                "fix_versions": sorted(entry["fix_versions"]),
                "references": sorted(entry["references"]),
                "aliases": sorted(entry["aliases"]),
                "occurrences": entry["occurrences"],
                "description": next(iter(entry["descriptions"]), ""),
            }
        )
    return sorted(
        normalised,
        key=lambda item: (
            -SEVERITY_WEIGHTS.get(item["severity"], 0),
            -item["occurrences"],
            item["id"],
        ),
    )


def build_html(summary: dict, top_vulns: List[dict]) -> str:
    rows = "\n".join(
        f"<tr><td>{escape(sev.title())}</td><td>{summary['counts'].get(sev, 0)}</td></tr>"
        for sev in SEVERITY_ORDER
    )
    vuln_rows = "".join(
        f"<li><strong>{escape(vuln['id'])}</strong> "
        f"({escape(vuln['severity'].title())}, {escape(', '.join(vuln['ecosystems']))})"
        f" – Packages: {escape(', '.join(vuln['packages']) or 'n/a')}"
        f" – Fix: {escape(', '.join(vuln['fix_versions']) or 'n/a')}"
        f" – <a href='{escape(vuln['references'][0])}'>Advisory</a></li>"
        if vuln.get("references")
        else f"<li><strong>{escape(vuln['id'])}</strong> "
        f"({escape(vuln['severity'].title())}, {escape(', '.join(vuln['ecosystems']))})"
        f" – Packages: {escape(', '.join(vuln['packages']) or 'n/a')}"
        f" – Fix: {escape(', '.join(vuln['fix_versions']) or 'n/a')}</li>"
        for vuln in top_vulns
    )
    generated_at = escape(summary["generated_at"])
    status = escape(summary["policy"].get("status", ""))
    message = escape(summary["policy"].get("message", ""))
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<title>Dependency Vulnerability Scan</title>"
        "<style>body{font-family:Arial,Helvetica,sans-serif;margin:2rem;}"
        "table{border-collapse:collapse;}th,td{border:1px solid #ddd;padding:0.5rem;}"
        "th{background:#f5f5f5;}</style></head><body>"
        f"<h1>Dependency Vulnerability Scan</h1>"
        f"<p><strong>Status:</strong> {status} – {message}</p>"
        f"<p><strong>Generated:</strong> {generated_at}</p>"
        "<h2>Severity Totals</h2>"
        f"<table><thead><tr><th>Severity</th><th>Count</th></tr></thead><tbody>{rows}</tbody></table>"
        "<h2>Top Findings</h2>"
        f"<ol>{vuln_rows or '<li>No vulnerabilities detected.</li>'}</ol>"
        "</body></html>"
    )


def build_pr_comment(summary: dict, top_vulns: List[dict]) -> str:
    lines = ["## 🔍 Dependency Vulnerability Scan (SCA)"]
    lines.append(f"_Generated: {summary['generated_at']}_")
    lines.append("")
    lines.append("| Severity | Count |")
    lines.append("| --- | --- |")
    for severity in SEVERITY_ORDER:
        lines.append(f"| {severity.title()} | {summary['counts'].get(severity, 0)} |")
    lines.append("")
    policy = summary.get("policy", {})
    status = policy.get("status", "pass")
    message = policy.get("message", "")
    icon = {"fail": "❌", "warn": "⚠️"}.get(status, "✅")
    lines.append(f"{icon} **Policy**: {message}")
    if top_vulns:
        lines.append("")
        lines.append("**Top 5 CVEs / Advisories**")
        for idx, vuln in enumerate(top_vulns[:5], start=1):
            ref = vuln["references"][0] if vuln.get("references") else ""
            link = f" – [Advisory]({ref})" if ref else ""
            packages = ", ".join(vuln.get("packages") or []) or "n/a"
            fixes = ", ".join(vuln.get("fix_versions") or []) or "n/a"
            eco = ", ".join(vuln.get("ecosystems") or []) or "unknown"
            lines.append(
                f"{idx}. **{vuln['id']}** ({vuln['severity'].title()}, {eco}) – Packages: {packages}; Fix: {fixes}{link}"
            )
    else:
        lines.append("")
        lines.append("No known vulnerabilities were detected.")
    lines.append("")
    lines.append("_Reports: `artifacts/security/sca/` (JSON & HTML)_")
    python_meta = summary.get("ecosystems", {}).get("python", {})
    skipped_total = python_meta.get("skipped_total", 0)
    if skipped_total:
        lines.append("")
        lines.append(f"_Skipped {skipped_total} unpinned Python requirements (see summary for details)._")
    comment = "\n".join(lines)
    if not comment.endswith("\n"):
        comment += "\n"
    return comment


def evaluate_policy(counts: Counter, policy: Dict[str, str]) -> Tuple[str, str]:
    fail_levels = levels_at_or_above(policy["fail_threshold"])
    warn_levels = levels_at_or_above(policy["warn_threshold"])
    fail_count = sum(counts.get(level, 0) for level in fail_levels)
    warn_count = sum(counts.get(level, 0) for level in warn_levels)
    if fail_count:
        return (
            "fail",
            f"{fail_count} vulnerabilities at or above {policy['fail_threshold'].title()} (fail threshold)",
        )
    if warn_count:
        return (
            "warn",
            f"{warn_count} vulnerabilities at or above {policy['warn_threshold'].title()} (warn threshold)",
        )
    return (
        "pass",
        f"No vulnerabilities at or above {policy['warn_threshold'].title()} threshold",
    )


def main() -> None:
    policy = load_policy()
    ensure_clean_dirs()

    python_manifests = find_python_manifests()
    python_results: List[dict] = []
    python_counts = Counter({key: 0 for key in SEVERITY_ORDER})
    collected_vulns: List[dict] = []

    for manifest in python_manifests:
        data = run_pip_audit(manifest)
        manifest_vulns, manifest_counts = collect_python_vulns(manifest, data)
        dependencies = _python_dependencies(data)
        collected_vulns.extend(manifest_vulns)
        python_counts.update(manifest_counts)
        python_results.append(
            {
                "manifest": manifest.relative_to(REPO_ROOT).as_posix(),
                "tool": "osv.dev",
                "dependency_count": len(dependencies),
                "vulnerability_count": sum(manifest_counts.values()),
                "skipped": data.get("skipped", []) if isinstance(data, dict) else [],
            }
        )
        output_path = PYTHON_DIR / f"{sanitize_name(manifest)}.json"
        write_json(output_path, data)

    pnpm_data = run_pnpm_audit()
    node_vulns, node_counts = collect_node_vulns(pnpm_data)
    collected_vulns.extend(node_vulns)
    node_result = {
        "lockfile": "pnpm-lock.yaml",
        "tool": "pnpm audit",
        "vulnerability_count": sum(node_counts.values()),
    }
    write_json(NODE_DIR / "pnpm-audit.json", pnpm_data)

    total_counts = Counter({key: 0 for key in SEVERITY_ORDER})
    total_counts.update(python_counts)
    total_counts.update(node_counts)

    status, message = evaluate_policy(total_counts, policy)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

    top_vulns = aggregate_vulnerabilities(collected_vulns)

    skipped_total = sum(len(entry.get("skipped", [])) for entry in python_results)

    summary = {
        "generated_at": generated_at,
        "counts": dict(total_counts),
        "policy": {"status": status, "message": message, "fail_threshold": policy["fail_threshold"], "warn_threshold": policy["warn_threshold"]},
        "ecosystems": {
            "python": {
                "manifests": python_results,
                "counts": dict(python_counts),
                "skipped_total": skipped_total,
            },
            "node": {
                "lockfile": node_result,
                "counts": dict(node_counts),
            },
        },
        "top_vulnerabilities": top_vulns[:5],
    }

    write_json(SUMMARY_JSON, summary)
    SUMMARY_HTML.write_text(build_html(summary, top_vulns[:5]), encoding="utf-8")
    PR_COMMENT_PATH.write_text(build_pr_comment(summary, top_vulns[:5]), encoding="utf-8")

    print("Dependency SCA summary:")
    for severity in SEVERITY_ORDER:
        print(f"  {severity.title():<9}: {total_counts.get(severity, 0)}")
    print(f"Policy result: {status.upper()} – {message}")

    if status == "fail":
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except ScanError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
