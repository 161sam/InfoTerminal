#!/usr/bin/env python3
"""Validate runtime-hardening policies for Compose and Kubernetes manifests."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
SECURITY_INVENTORY = REPO_ROOT / "inventory" / "security.json"
ALLOWED_EGRESS_SERVICES = {
    "egress-gateway",
    "feed-ingestor",
    "flowise-connector",
    "n8n",
    "nifi",
    "gateway",
    "opa",
}


def load_inventory() -> dict:
    if not SECURITY_INVENTORY.exists():
        raise SystemExit(
            "inventory/security.json is missing. Run `python scripts/generate_inventory.py` first."
        )
    return json.loads(SECURITY_INVENTORY.read_text(encoding="utf-8"))


def validate_compose(compose_entries: List[dict]) -> List[str]:
    errors: List[str] = []
    for entry in compose_entries:
        name = entry.get("name") or "<unknown>"
        seccomp = entry.get("seccomp") or []
        apparmor = entry.get("apparmor") or []
        caps_drop = entry.get("cap_drop") or []
        no_new_privs = bool(entry.get("no_new_privileges"))
        egress_policy = entry.get("egress_policy")

        if not seccomp:
            errors.append(f"compose:{name}: missing seccomp profile")
        if not apparmor:
            errors.append(f"compose:{name}: missing AppArmor profile reference")
        if "ALL" not in caps_drop:
            errors.append(f"compose:{name}: does not drop ALL capabilities")
        if not no_new_privs:
            errors.append(f"compose:{name}: no-new-privileges not enforced")
        if egress_policy == "egress-allowed" and name not in ALLOWED_EGRESS_SERVICES:
            errors.append(f"compose:{name}: unexpected egress allowance")
        if egress_policy in {None, "unspecified"}:
            errors.append(f"compose:{name}: egress policy not defined")
    return errors


def validate_kubernetes(k8s_entries: List[dict], policies: List[dict]) -> List[str]:
    errors: List[str] = []
    for entry in k8s_entries:
        name = entry.get("name") or "<unknown>"
        annotations = entry.get("annotations") or {}
        containers = entry.get("containers") or []
        if not any(value == "runtime/default" for value in annotations.values()):
            errors.append(f"k8s:{name}: missing AppArmor annotation for runtime/default")
        pod_seccomp = entry.get("podSecurityContext", {}).get("seccompProfile", {})
        if pod_seccomp.get("type") != "RuntimeDefault":
            errors.append(f"k8s:{name}: pod seccompProfile not RuntimeDefault")
        for container in containers:
            cname = container.get("name") or "<container>"
            if container.get("allowPrivilegeEscalation") is not False:
                errors.append(f"k8s:{name}/{cname}: allowPrivilegeEscalation must be false")
            capabilities = container.get("capabilities") or {}
            drops = capabilities.get("drop") or []
            if "ALL" not in drops:
                errors.append(f"k8s:{name}/{cname}: capabilities.drop must include ALL")
            seccomp_profile = container.get("seccompProfile") or {}
            if seccomp_profile.get("type") != "RuntimeDefault":
                errors.append(f"k8s:{name}/{cname}: seccompProfile not RuntimeDefault")
    if not policies:
        errors.append("k8s: missing NetworkPolicy definitions for egress restrictions")
    return errors


def main() -> None:
    inventory = load_inventory()
    errors: List[str] = []
    errors.extend(validate_compose(inventory.get("compose", [])))
    errors.extend(validate_kubernetes(inventory.get("kubernetes", []), inventory.get("networkPolicies", [])))

    if errors:
        for item in errors:
            print(f"ERROR: {item}")
        sys.exit(1)
    print("runtime hardening smoke: ok")


if __name__ == "__main__":
    main()
