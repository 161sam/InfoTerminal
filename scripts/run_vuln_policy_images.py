#!/usr/bin/env python3
"""Scan container images with Trivy and enforce the vuln_policy_images gate.

The script discovers container images referenced across docker-compose manifests and
Kubernetes production manifests (matching the SBOM tooling) and executes a Trivy
vulnerability scan for each image. It writes JSON reports to
``artifacts/security/images/reports`` together with a consolidated summary and a
PR-ready Markdown comment. Policy thresholds are defined in
``policy/vuln_policy_images.json`` and the allow-list (baseline) is managed via
``policy/vuln_baseline_images.json``.

Baseline entries require an explicit justification and expiry date. Accepted
vulnerabilities are excluded from policy enforcement until they expire.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = REPO_ROOT / "artifacts" / "security" / "images"
REPORTS_DIR = ARTIFACT_ROOT / "reports"
SUMMARY_JSON = ARTIFACT_ROOT / "scan_summary.json"
SUMMARY_HTML = ARTIFACT_ROOT / "scan_summary.html"
PR_COMMENT_PATH = ARTIFACT_ROOT / "pr_comment.md"
POLICY_PATH = REPO_ROOT / "policy" / "vuln_policy_images.json"
BASELINE_PATH = REPO_ROOT / "policy" / "vuln_baseline_images.json"
DEFAULT_POLICY = {"fail_threshold": "high", "warn_threshold": "medium"}
ENV_FAIL = "VULN_POLICY_IMAGES_FAIL_LEVEL"
ENV_WARN = "VULN_POLICY_IMAGES_WARN_LEVEL"
ENV_SKIP_UPDATE = "TRIVY_SKIP_UPDATE"
SEVERITY_ORDER = ["critical", "high", "medium", "low", "unknown"]
SEVERITY_WEIGHTS = {name: index for index, name in enumerate(SEVERITY_ORDER)}
EXPIRY_SOON_DAYS = 30

try:
    from generate_image_sboms import collect_images  # type: ignore
except ImportError as exc:  # pragma: no cover - defensive guard for path misconfiguration
    raise SystemExit(
        "Unable to import collect_images from scripts/generate_image_sboms.py. "
        "Run this script from the repository root."
    ) from exc


class ScanError(RuntimeError):
    """Raised when Trivy fails or invalid data is encountered."""


@dataclass
class BaselineAcceptance:
    """Represents an accepted vulnerability (baseline whitelist entry)."""

    identifier: str
    images: List[str]
    components: List[str]
    reason: str
    expires: datetime
    owner: Optional[str] = None
    notes: Optional[str] = None
    severity: Optional[str] = None
    reference: Optional[str] = None
    used: bool = field(default=False)

    def applies_to(self, image: str, component: Optional[str]) -> bool:
        if self.images and "*" not in self.images and image not in self.images:
            return False
        if self.components and component:
            return component in self.components
        if self.components and not component:
            # Entry expects a component/package, but the finding has none -> no match
            return False
        return True

    def is_expired(self, now: datetime) -> bool:
        return self.expires < now

    def is_expiring_soon(self, now: datetime) -> bool:
        return now <= self.expires <= now + timedelta(days=EXPIRY_SOON_DAYS)

    def to_dict(self) -> dict:
        data = {
            "id": self.identifier,
            "images": self.images,
            "components": self.components,
            "reason": self.reason,
            "expires": self.expires.isoformat(),
        }
        if self.owner:
            data["owner"] = self.owner
        if self.notes:
            data["notes"] = self.notes
        if self.severity:
            data["severity"] = self.severity
        if self.reference:
            data["reference"] = self.reference
        data["used"] = self.used
        return data


@dataclass
class Finding:
    """Represents a single vulnerability finding from Trivy."""

    key: str
    image: str
    target: str
    identifier: str
    severity: str
    package: Optional[str]
    installed_version: Optional[str]
    fixed_version: Optional[str]
    url: Optional[str]
    title: Optional[str]
    published: Optional[str]
    status: str  # "active" or "accepted"
    baseline: Optional[BaselineAcceptance] = None

    def to_dict(self) -> dict:
        data = {
            "key": self.key,
            "image": self.image,
            "target": self.target,
            "id": self.identifier,
            "severity": self.severity,
            "package": self.package,
            "installed_version": self.installed_version,
            "fixed_version": self.fixed_version,
            "url": self.url,
            "title": self.title,
            "published": self.published,
            "status": self.status,
        }
        if self.baseline:
            data["baseline"] = {
                "id": self.baseline.identifier,
                "reason": self.baseline.reason,
                "expires": self.baseline.expires.isoformat(),
                "owner": self.baseline.owner,
                "notes": self.baseline.notes,
            }
        return data


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan container images with Trivy and enforce vuln_policy_images gate.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the actions without executing Trivy or writing artefacts.",
    )
    parser.add_argument(
        "--images",
        nargs="*",
        help="Optional subset of images to scan (defaults to all discovered images).",
    )
    parser.add_argument(
        "--fail-threshold",
        choices=SEVERITY_ORDER,
        help="Override fail threshold (takes precedence over policy & env).",
    )
    parser.add_argument(
        "--warn-threshold",
        choices=SEVERITY_ORDER,
        help="Override warning threshold (takes precedence over policy & env).",
    )
    parser.add_argument(
        "--skip-clean",
        action="store_true",
        help="Skip pruning stale reports that are no longer referenced.",
    )
    return parser.parse_args(argv)


def load_policy(args: argparse.Namespace) -> Dict[str, str]:
    policy = DEFAULT_POLICY.copy()
    if POLICY_PATH.exists():
        try:
            data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:  # pragma: no cover - configuration error
            raise SystemExit(f"Invalid JSON in {POLICY_PATH}: {exc}") from exc
        if isinstance(data, dict):
            policy.update({k: str(v) for k, v in data.items() if v is not None})
    if os.getenv(ENV_FAIL):
        policy["fail_threshold"] = os.environ[ENV_FAIL]
    if os.getenv(ENV_WARN):
        policy["warn_threshold"] = os.environ[ENV_WARN]
    if args.fail_threshold:
        policy["fail_threshold"] = args.fail_threshold
    if args.warn_threshold:
        policy["warn_threshold"] = args.warn_threshold

    for key in ("fail_threshold", "warn_threshold"):
        value = policy.get(key)
        if not isinstance(value, str):
            raise SystemExit(f"Policy value for {key} must be a string, got {type(value)!r}")
        normalised = value.lower().strip()
        if normalised not in SEVERITY_ORDER:
            raise SystemExit(
                f"Unsupported severity '{value}' for {key}. Valid options: {', '.join(SEVERITY_ORDER)}"
            )
        policy[key] = normalised
    return policy


def normalise_severity(raw: Optional[str]) -> str:
    if not raw:
        return "unknown"
    value = raw.lower()
    if value not in SEVERITY_ORDER:
        return "unknown"
    return value


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ScanError(f"Failed to parse JSON report: {path}\n{exc}") from exc


def parse_timestamp(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def parse_baseline(now: datetime) -> List[BaselineAcceptance]:
    if not BASELINE_PATH.exists():
        return []
    try:
        data = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:  # pragma: no cover - configuration error
        raise SystemExit(f"Invalid JSON in {BASELINE_PATH}: {exc}") from exc

    acceptances_raw = data.get("acceptances") if isinstance(data, dict) else None
    if acceptances_raw is None:
        return []
    if not isinstance(acceptances_raw, list):
        raise SystemExit(
            f"Expected 'acceptances' to be a list in {BASELINE_PATH}, got {type(acceptances_raw)!r}"
        )

    acceptances: List[BaselineAcceptance] = []
    for index, item in enumerate(acceptances_raw):
        if not isinstance(item, dict):
            raise SystemExit(f"Baseline entry #{index} is not an object: {item!r}")
        identifier = str(item.get("id") or "").strip()
        if not identifier:
            raise SystemExit(f"Baseline entry #{index} is missing 'id'")
        reason = str(item.get("reason") or "").strip()
        if not reason:
            raise SystemExit(f"Baseline entry {identifier} is missing 'reason'")
        expires_raw = str(item.get("expires") or "").strip()
        if not expires_raw:
            raise SystemExit(f"Baseline entry {identifier} is missing 'expires'")
        try:
            expires = datetime.fromisoformat(expires_raw)
        except ValueError as exc:
            raise SystemExit(
                f"Baseline entry {identifier} has invalid expiry '{expires_raw}': {exc}"
            ) from exc
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        images_raw = item.get("images")
        components_raw = item.get("components")
        images: List[str] = []
        components: List[str] = []
        if images_raw is None:
            images = []
        elif isinstance(images_raw, list):
            images = [str(elem) for elem in images_raw if elem]
        elif isinstance(images_raw, str):
            images = [images_raw]
        else:
            raise SystemExit(f"Baseline entry {identifier}: 'images' must be list or string")
        if components_raw is None:
            components = []
        elif isinstance(components_raw, list):
            components = [str(elem) for elem in components_raw if elem]
        elif isinstance(components_raw, str):
            components = [components_raw]
        else:
            raise SystemExit(f"Baseline entry {identifier}: 'components' must be list or string")
        acceptance = BaselineAcceptance(
            identifier=identifier,
            images=images,
            components=components,
            reason=reason,
            expires=expires.astimezone(timezone.utc),
            owner=(str(item["owner"]).strip() if item.get("owner") else None),
            notes=(str(item["notes"]).strip() if item.get("notes") else None),
            severity=(str(item["severity"]).lower().strip() if item.get("severity") else None),
            reference=(str(item["reference"]).strip() if item.get("reference") else None),
        )
        acceptances.append(acceptance)
    # Sort for deterministic processing
    return sorted(acceptances, key=lambda acc: (acc.identifier, ",".join(acc.images)))


def resolve_trivy_command() -> List[str]:
    custom_cmd = os.environ.get("TRIVY_CMD")
    if custom_cmd:
        return custom_cmd.split()
    trivy_cmd = shutil.which("trivy")  # type: ignore[name-defined]
    if trivy_cmd:
        return [trivy_cmd]
    raise ScanError(
        "Trivy executable not found. Install 'trivy' or set TRIVY_CMD to the desired command."
    )


def sanitise_report_name(image_ref: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in image_ref)
    return f"{safe}.trivy.json"


def ensure_directories() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)


def run_trivy_scan(
    command: Sequence[str],
    image: str,
    output_path: Path,
    *,
    skip_update: bool,
    dry_run: bool,
) -> None:
    args = list(command) + [
        "image",
        "--quiet",
        "--format",
        "json",
        "--scanners",
        "vuln",
        "--severity",
        ",".join(level.upper() for level in SEVERITY_ORDER),
        "--output",
        str(output_path),
    ]
    if skip_update:
        args.append("--skip-db-update")
    args.append(image)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if dry_run:
        print(f"[dry-run] {' '.join(args)}")
        return

    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise ScanError(
            f"Trivy scan failed for {image} (exit code {result.returncode})\n{stderr}"
        )
    if not output_path.exists() or output_path.stat().st_size == 0:
        raise ScanError(f"Trivy did not produce an output file for {image}: {output_path}")


def finding_key(image: str, vulnerability_id: str, package: Optional[str], target: str) -> str:
    parts = [image, vulnerability_id]
    if package:
        parts.append(package)
    if target and target != image:
        parts.append(target)
    return "::".join(parts)


def load_reports(
    images: Iterable[str],
    baseline: List[BaselineAcceptance],
    now: datetime,
) -> Tuple[List[Finding], List[Finding], List[BaselineAcceptance], List[BaselineAcceptance]]:
    active: List[Finding] = []
    accepted: List[Finding] = []
    expired_acceptances: List[BaselineAcceptance] = []
    baseline_by_id: Dict[str, List[BaselineAcceptance]] = defaultdict(list)
    for entry in baseline:
        baseline_by_id[entry.identifier].append(entry)

    for image in images:
        report_path = REPORTS_DIR / sanitise_report_name(image)
        if not report_path.exists():
            raise ScanError(
                f"Missing report for image {image}: {report_path.relative_to(REPO_ROOT)}. "
                "Run the script without --dry-run to generate reports."
            )
        report = read_json(report_path)
        results = report.get("Results") or []
        if not isinstance(results, list):
            continue
        for result in results:
            if not isinstance(result, dict):
                continue
            target = str(result.get("Target") or image)
            vulnerabilities = result.get("Vulnerabilities") or []
            if not isinstance(vulnerabilities, list):
                continue
            for vuln in vulnerabilities:
                if not isinstance(vuln, dict):
                    continue
                identifier = str(vuln.get("VulnerabilityID") or vuln.get("ID") or "").strip()
                if not identifier:
                    continue
                severity = normalise_severity(str(vuln.get("Severity") or ""))
                package = str(vuln.get("PkgName") or "").strip() or None
                installed = str(vuln.get("InstalledVersion") or "").strip() or None
                fixed = str(vuln.get("FixedVersion") or "").strip() or None
                url = str(vuln.get("PrimaryURL") or "").strip() or None
                title = str(vuln.get("Title") or "").strip() or None
                published = None
                if vuln.get("PublishedDate"):
                    published_dt = parse_timestamp(str(vuln.get("PublishedDate")))
                    if published_dt:
                        published = published_dt.isoformat()
                key = finding_key(image, identifier, package, target)
                matching_acceptances = [
                    entry
                    for entry in baseline_by_id.get(identifier, [])
                    if entry.applies_to(image, package)
                ]
                chosen_acceptance: Optional[BaselineAcceptance] = None
                for entry in matching_acceptances:
                    if entry.is_expired(now):
                        if entry not in expired_acceptances:
                            expired_acceptances.append(entry)
                        continue
                    chosen_acceptance = entry
                    entry.used = True
                    break
                status = "accepted" if chosen_acceptance else "active"
                finding = Finding(
                    key=key,
                    image=image,
                    target=target,
                    identifier=identifier,
                    severity=severity,
                    package=package,
                    installed_version=installed,
                    fixed_version=fixed,
                    url=url,
                    title=title,
                    published=published,
                    status=status,
                    baseline=chosen_acceptance,
                )
                if chosen_acceptance:
                    accepted.append(finding)
                else:
                    active.append(finding)
    unused_acceptances = [entry for entry in baseline if not entry.used]
    return active, accepted, expired_acceptances, unused_acceptances


def severity_levels_at_or_above(threshold: str) -> Tuple[str, ...]:
    idx = SEVERITY_ORDER.index(threshold)
    return tuple(SEVERITY_ORDER[: idx + 1])


def summarise(
    images: List[str],
    active: List[Finding],
    accepted: List[Finding],
    expired: List[BaselineAcceptance],
    unused: List[BaselineAcceptance],
    policy: Dict[str, str],
    now: datetime,
    previous_summary: Optional[dict],
) -> Tuple[dict, dict]:
    totals = {severity: {"active": 0, "accepted": 0} for severity in SEVERITY_ORDER}
    for finding in active:
        totals.setdefault(finding.severity, {"active": 0, "accepted": 0})
        totals[finding.severity]["active"] += 1
    for finding in accepted:
        totals.setdefault(finding.severity, {"active": 0, "accepted": 0})
        totals[finding.severity]["accepted"] += 1

    fail_levels = severity_levels_at_or_above(policy["fail_threshold"])
    warn_levels = severity_levels_at_or_above(policy["warn_threshold"])
    active_fail = [f for f in active if f.severity in fail_levels]
    active_warn = [f for f in active if f.severity in warn_levels]
    fail = bool(active_fail)
    warn = bool(active_warn) and not fail
    expiring_map = {}
    for finding in accepted:
        base = finding.baseline
        if base and base.is_expiring_soon(now):
            key = (base.identifier, tuple(base.images), tuple(base.components))
            if key not in expiring_map:
                expiring_map[key] = base
    expiring_soon_entries = sorted(expiring_map.values(), key=lambda b: (b.expires, b.identifier))

    active_keys = [finding.key for finding in active]
    previous_keys = set(previous_summary.get("active_keys", [])) if previous_summary else set()
    current_keys = set(active_keys)
    new_keys = sorted(current_keys - previous_keys)
    resolved_keys = sorted(previous_keys - current_keys)

    key_to_finding = {finding.key: finding for finding in active}
    delta_new = [key_to_finding[key].to_dict() for key in new_keys if key in key_to_finding]
    delta_resolved = []
    if previous_summary:
        prev_findings = {
            item["key"]: item
            for item in previous_summary.get("active_findings", [])
            if isinstance(item, dict) and item.get("key")
        }
        for key in resolved_keys:
            if key in prev_findings:
                delta_resolved.append(prev_findings[key])

    summary = {
        "generated_at": now.isoformat(),
        "images": images,
        "totals": totals,
        "policy": policy,
        "status": {
            "fail": fail,
            "warn": warn,
            "fail_count": len(active_fail),
            "warn_count": len(active_warn),
        },
        "active_findings": [finding.to_dict() for finding in active],
        "accepted_findings": [finding.to_dict() for finding in accepted],
        "active_keys": active_keys,
        "baseline": {
            "path": str(BASELINE_PATH.relative_to(REPO_ROOT) if BASELINE_PATH.exists() else BASELINE_PATH),
            "expired": [entry.to_dict() for entry in expired],
            "unused": [entry.to_dict() for entry in unused],
            "expiring_soon": [entry.to_dict() for entry in expiring_soon_entries],
        },
        "delta": {
            "new": delta_new,
            "resolved": delta_resolved,
        },
    }
    return summary, {
        "fail": fail,
        "warn": warn,
        "fail_findings": active_fail,
        "warn_findings": active_warn,
        "delta_new": delta_new,
        "delta_resolved": delta_resolved,
    }



def write_summary_artifacts(summary: dict, status_data: dict, now: datetime, dry_run: bool) -> None:
    if dry_run:
        print(f"[dry-run] Would write {SUMMARY_JSON.relative_to(REPO_ROOT)}")
        print(f"[dry-run] Would write {PR_COMMENT_PATH.relative_to(REPO_ROOT)}")
        print(f"[dry-run] Would write {SUMMARY_HTML.relative_to(REPO_ROOT)}")
        return
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PR_COMMENT_PATH.write_text(build_pr_comment(summary, status_data, now), encoding="utf-8")
    SUMMARY_HTML.write_text(build_summary_html(summary), encoding="utf-8")


def build_pr_comment(summary: dict, status_data: dict, now: datetime) -> str:
    totals = summary.get("totals", {})
    status = summary.get("status", {})
    policy = summary.get("policy", {})
    lines = ["## 🚨 Container Vulnerability Scan (Images)"]
    lines.append(f"_Generated: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}_")
    lines.append("")
    lines.append("| Severity | Active | Accepted |")
    lines.append("| --- | --- | --- |")
    for severity in SEVERITY_ORDER:
        entry = totals.get(severity, {"active": 0, "accepted": 0})
        lines.append(
            f"| {severity.title()} | {entry.get('active', 0)} | {entry.get('accepted', 0)} |"
        )
    lines.append("")
    fail = status.get("fail")
    warn = status.get("warn") and not fail
    if fail:
        fail_level = policy.get("fail_threshold", "high").title()
        fail_count = status_data.get("fail_findings")
        count_display = len(fail_count) if isinstance(fail_count, list) else "N/A"
        lines.append(f"❌ **Policy**: {count_display} vulnerabilities ≥ {fail_level} (fail threshold)")
    elif warn:
        warn_level = policy.get("warn_threshold", "medium").title()
        warn_findings = status_data.get("warn_findings")
        count_display = len(warn_findings) if isinstance(warn_findings, list) else "N/A"
        lines.append(f"⚠️ **Policy**: {count_display} vulnerabilities ≥ {warn_level} (warn threshold)")
    else:
        warn_level = policy.get("warn_threshold", "medium").title()
        lines.append(f"✅ **Policy**: No vulnerabilities ≥ {warn_level}")
    lines.append("")

    delta = summary.get("delta", {})
    new_findings = delta.get("new") or []
    resolved_findings = delta.get("resolved") or []
    if new_findings or resolved_findings:
        lines.append("**Delta since previous scan**")
        if new_findings:
            for item in new_findings[:5]:
                lines.append(
                    f"- ➕ {item['id']} ({item['severity'].title()}, {item['image']}) – {item.get('package') or 'package n/a'}"
                )
            if len(new_findings) > 5:
                lines.append(f"- … {len(new_findings) - 5} additional new findings")
        if resolved_findings:
            for item in resolved_findings[:5]:
                lines.append(
                    f"- ➖ {item['id']} ({item['severity'].title()}, {item['image']})"
                )
            if len(resolved_findings) > 5:
                lines.append(f"- … {len(resolved_findings) - 5} additional resolved findings")
        lines.append("")

    active = summary.get("active_findings", [])
    if active:
        lines.append("**Top Active Findings**")
        sorted_active = sorted(
            active,
            key=lambda item: (SEVERITY_WEIGHTS.get(item.get("severity", "unknown"), 0), item.get("id"), item.get("image")),
        )
        for idx, item in enumerate(sorted_active[:5], start=1):
            fix = item.get("fixed_version") or "n/a"
            package = item.get("package") or "package n/a"
            url = item.get("url")
            link = f" – [Advisory]({url})" if url else ""
            lines.append(
                f"{idx}. **{item['id']}** ({item['severity'].title()}, {item['image']}) – {package} {item.get('installed_version') or 'n/a'}; Fix: {fix}{link}"
            )
        lines.append("")

    baseline = summary.get("baseline", {})
    expiring = baseline.get("expiring_soon") or []
    expired = baseline.get("expired") or []
    if expiring or expired:
        lines.append("**Baseline Review Needed**")
        for item in expiring[:5]:
            lines.append(
                f"- ⏳ {item['id']} for {', '.join(item.get('images') or ['*'])} expires {item['expires']} – {item.get('reason')}"
            )
        for item in expired[:5]:
            lines.append(
                f"- ❗️ {item['id']} expired {item['expires']} – {item.get('reason')}"
            )
        lines.append("")

    lines.append(
        f"_Reports: `{ARTIFACT_ROOT.relative_to(REPO_ROOT)}/` (JSON, HTML) – Baseline: `{baseline.get('path')}`_"
    )
    return "\n".join(lines).strip() + "\n"


def build_summary_html(summary: dict) -> str:
    head = """<html><head><meta charset=\"utf-8\"><title>Container Vulnerability Scan</title>
<style>
body { font-family: sans-serif; margin: 2rem; }
h1 { font-size: 1.5rem; }
table { border-collapse: collapse; margin-top: 1rem; }
th, td { border: 1px solid #ccc; padding: 0.4rem 0.6rem; text-align: left; }
.severity-critical { color: #b00020; font-weight: bold; }
.severity-high { color: #d32f2f; font-weight: bold; }
.severity-medium { color: #f57c00; }
.severity-low { color: #388e3c; }
.severity-unknown { color: #616161; }
section { margin-top: 1.5rem; }
</style></head><body>"""
    body = ["<h1>Container Vulnerability Scan (Images)</h1>"]
    body.append(f"<p>Generated: {summary['generated_at']}</p>")
    body.append("<section><h2>Totals</h2><table><thead><tr><th>Severity</th><th>Active</th><th>Accepted</th></tr></thead><tbody>")
    for severity in SEVERITY_ORDER:
        entry = summary["totals"].get(severity, {"active": 0, "accepted": 0})
        body.append(
            f"<tr><td class=\"severity-{severity}\">{severity.title()}</td><td>{entry['active']}</td><td>{entry['accepted']}</td></tr>"
        )
    body.append("</tbody></table></section>")

    def render_findings(title: str, findings: List[dict]) -> None:
        if not findings:
            return
        body.append(f"<section><h2>{title}</h2><table><thead><tr><th>Severity</th><th>ID</th><th>Image</th><th>Package</th><th>Installed</th><th>Fixed</th><th>Notes</th></tr></thead><tbody>")
        for item in findings:
            url = item.get("url")
            title_attr = item.get("title") or ""
            link = f'<a href="{url}">link</a>' if url else ""
            baseline_note = ""
            if item.get("baseline"):
                baseline_note = f"Accepted: {item['baseline'].get('reason')} (expires {item['baseline'].get('expires')})"
            body.append(
                "<tr>"
                f"<td class=\"severity-{item['severity']}\">{item['severity'].title()}</td>"
                f"<td>{item['id']}</td>"
                f"<td>{item['image']}</td>"
                f"<td>{item.get('package') or ''}</td>"
                f"<td>{item.get('installed_version') or ''}</td>"
                f"<td>{item.get('fixed_version') or ''}</td>"
                f"<td>{title_attr} {link} {baseline_note}</td>"
                "</tr>"
            )
        body.append("</tbody></table></section>")

    render_findings("Active Findings", summary.get("active_findings", []))
    render_findings("Accepted (Baseline) Findings", summary.get("accepted_findings", []))

    baseline = summary.get("baseline", {})
    expired = baseline.get("expired") or []
    unused = baseline.get("unused") or []
    if expired or unused:
        body.append("<section><h2>Baseline Review</h2>")
        if expired:
            body.append("<h3>Expired</h3><ul>")
            for item in expired:
                body.append(
                    f"<li>{item['id']} for {', '.join(item.get('images') or ['*'])} expired {item['expires']} – {item.get('reason')}</li>"
                )
            body.append("</ul>")
        if unused:
            body.append("<h3>Unused</h3><ul>")
            for item in unused:
                body.append(
                    f"<li>{item['id']} for {', '.join(item.get('images') or ['*'])} – {item.get('reason')}</li>"
                )
            body.append("</ul>")
        body.append("</section>")

    body.append("</body></html>")
    return head + "".join(body)


def prune_stale_reports(current_images: Iterable[str], dry_run: bool) -> None:
    expected = {sanitise_report_name(image) for image in current_images}
    for path in REPORTS_DIR.glob("*.trivy.json"):
        if path.name not in expected:
            rel = path.relative_to(REPO_ROOT)
            if dry_run:
                print(f"[dry-run] Would remove stale report {rel}")
            else:
                path.unlink()


def load_previous_summary() -> Optional[dict]:
    if not SUMMARY_JSON.exists():
        return None
    try:
        return json.loads(SUMMARY_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    dry_run_env = bool(int(os.environ.get("DRY_RUN", "0"))) if os.environ.get("DRY_RUN") else False
    dry_run = args.dry_run or dry_run_env
    now = datetime.now(timezone.utc)
    ensure_directories()
    policy = load_policy(args)
    baseline = parse_baseline(now)

    images_map = collect_images()
    images = sorted(images_map.keys())
    if args.images:
        selected = []
        missing = []
        for image in args.images:
            if image in images:
                selected.append(image)
            else:
                missing.append(image)
        if missing:
            raise SystemExit(f"Requested images not found in repository manifests: {', '.join(missing)}")
        images = sorted(selected)
    if not images:
        raise SystemExit("No container images detected in compose or manifest files")

    previous_summary = load_previous_summary()

    if dry_run:
        print("Running in dry-run mode. No reports will be generated.")
        for image in images:
            report_name = sanitise_report_name(image)
            print(f"[dry-run] trivy image --format json --output artifacts/security/images/reports/{report_name} {image}")
        return

    skip_update = os.environ.get(ENV_SKIP_UPDATE, "0") not in {"", "0", "false", "False"}

    try:
        trivy_cmd = resolve_trivy_command()
    except ScanError as exc:
        raise SystemExit(str(exc)) from exc

    for image in images:
        report_path = REPORTS_DIR / sanitise_report_name(image)
        run_trivy_scan(trivy_cmd, image, report_path, skip_update=skip_update, dry_run=dry_run)

    if not args.skip_clean:
        prune_stale_reports(images, dry_run=dry_run)

    active, accepted, expired, unused = load_reports(images, baseline, now)
    summary, status_data = summarise(images, active, accepted, expired, unused, policy, now, previous_summary)
    write_summary_artifacts(summary, status_data, now, dry_run=dry_run)
    print(
        f"Scanned {len(images)} image(s). Active findings: {len(active)} | Accepted: {len(accepted)}."
    )
    if status_data.get("fail"):
        raise SystemExit(1)
    if status_data.get("warn"):
        print("Warning: Vulnerabilities at or above warn threshold detected.")


if __name__ == "__main__":
    main()
