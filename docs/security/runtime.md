# Runtime Hardening

InfoTerminal containers now ship with enforced runtime controls across Docker
Compose and Kubernetes deployments. Each service runs with a deterministic
seccomp profile, AppArmor confinement, reduced Linux capabilities, and
`no-new-privileges` to prevent privilege escalation. Additionally, namespace
network policies restrict outbound traffic so only a few whitelisted services
may reach the public internet.

## Compose defaults

All Compose stacks include the shared extension
`x-runtime-defaults` which injects:

- `security_opt` → `no-new-privileges:true`, seccomp profile
  (`./security/runtime/seccomp/infoterminal-default.json`), and AppArmor
  (`docker-default`).
- `cap_drop: [ALL]` with a minimal `cap_add` set (`CHOWN`, `DAC_OVERRIDE`,
  `FOWNER`, `SETGID`, `SETUID`, `NET_BIND_SERVICE`).
- Internal-only networking by setting the default network to `internal: true`.
  Services that require internet access attach to the dedicated `egress`
  network.

Allowed egress services:

| Service | Compose file | Reason |
| --- | --- | --- |
| `egress-gateway` | `docker-compose.yml` | Break-glass proxy for curated outbound requests. |
| `flowise-connector` | `docker-compose.agents.yml` | Calls Flowise API + agent webhooks. |
| `nifi` | `docker-compose.verification.yml` | Retrieves external sources during ingest flows. |
| `n8n` | `docker-compose.verification.yml` | Executes automation playbooks with external plugins. |
| `gateway` | `docker-compose.gateway.yml` | Exposes public entrypoint and may call upstreams. |
| `opa` | `docker-compose.opa*.yml` | Posts audit events to optional external sinks. |

Every other service remains on the internal network only. The consolidated
output is tracked via `inventory/security.json`.

## Kubernetes hardening

Each Deployment/StatefulSet template now carries:

- Pod annotations `container.apparmor.security.beta.kubernetes.io/<container>`
  set to `runtime/default`.
- Pod `securityContext.seccompProfile.type: RuntimeDefault`.
- Container `securityContext` with `allowPrivilegeEscalation: false`,
  `capabilities.drop: ["ALL"]`, and `seccompProfile: {type: RuntimeDefault}`.
- Label `security.infoterminal.dev/egress` with value `internal` (default) or
  `allowed` for the gateway/editorial proxies.

Two namespace-wide `NetworkPolicy` resources enforce outbound rules:

1. `restrict-default-egress` – defaults all pods to internal-only traffic and
   DNS lookups to `kube-system`.
2. `allow-external-egress` – permits pods labelled
   `security.infoterminal.dev/egress=allowed` to reach arbitrary external
   addresses (ports 80/443/53).

## Seccomp profile

The Docker seccomp profile lives in
`security/runtime/seccomp/infoterminal-default.json`. It is based on the Docker
RuntimeDefault policy with tightened syscall allowances suitable for typical
userland services. Update the profile if a service requires additional syscalls;
changes will be picked up automatically by all Compose stacks via the shared
extension above.

## Validation

A new gate `runtime_hardening_smoke` runs in CI (`.github/workflows/ci.yml`). It
performs the following checks:

1. Generates `inventory/security.json` via
   `python scripts/generate_inventory.py`.
2. Executes `python scripts/runtime_hardening_smoke.py` to assert that every
   Compose service declares seccomp/AppArmor/no-new-privileges and that only the
   approved services attach to the `egress` network.
3. Confirms that Kubernetes manifests define the expected AppArmor annotations,
   seccomp profiles, container security contexts, and network policies.

Run the gate locally before pushing:

```bash
python3 scripts/generate_inventory.py
python3 scripts/runtime_hardening_smoke.py
```

If the smoke test fails, inspect the diagnostic messages—they point to the
service or manifest missing the hardening settings.

## Updating the allowlist

To grant external egress to an additional service, add `egress` to the service’s
Compose network list and label the corresponding Kubernetes workload with
`security.infoterminal.dev/egress: allowed`. Document the rationale inside this
file under “Allowed egress services” and ensure the change is approved by the
security lead before merging.
