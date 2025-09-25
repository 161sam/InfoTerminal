# Container Vulnerability Remediation Tracker

_Last updated: 2025-09-25._

This tracker maps every open critical finding from the container scan to an owning squad, remediation approach, and deadline. It complements the generated scan artefacts under `artifacts/security/images/` and is intended for weekly review in the security guild sync.

## 1. Frontend dependency refresh (tickets `SEC-FE-127` – `SEC-FE-132`)

| Target | Findings | Owner | Approach | Deadline |
| --- | --- | --- | --- | --- |
| `infoterminal/frontend:latest` | CVE-2018-3739, CVE-2018-3750, CVE-2021-44906, CVE-2021-3918, CVE-2025-7783, CVE-2025-29927 | Frontend squad (lead: M. Reuter) | Bump transitive deps via coordinated `pnpm` upgrade (`next@14.2.7+`, `form-data@4.0.2`, `https-proxy-agent@7.0.6`, `deep-extend@0.6.1`, `json-schema@0.5.2`) and regenerate lockfile. Follow the runbook in `scripts/security/update_frontend_dependencies.sh` (supports `DRY_RUN`). | 2025-10-24 (one week before baseline expiry) |

**Runbook excerpt**

```bash
# Dry-run to see proposed edits
DRY_RUN=1 bash scripts/security/update_frontend_dependencies.sh
# Apply updates & reinstall
bash scripts/security/update_frontend_dependencies.sh
pnpm install --filter @infoterminal/frontend... --no-frozen-lockfile
pnpm --filter @infoterminal/frontend test && pnpm --filter @infoterminal/frontend run build
```

## 2. Platform base-image upgrades (libdb5.3)

| Images | Findings | Owner | Status | Deadline |
| --- | --- | --- | --- | --- |
| `apache/nifi:2.0.0` | CVE-2019-8457 (libdb5.3), CVE-2021-29921 (Python 3.9) | Platform squad (lead: M. Kaya) | Waiting on upstream NiFi 2.0.1 security refresh. Tracking Jira `SEC-PLAT-221`. | 2025-11-15 |
| `grafana/promtail:2.9.4` | CVE-2019-8457 (libdb5.3) | Platform squad | Move to `grafana/promtail:3.1.2` once released (removes libdb). Evaluate custom slim image if vendor date slips past 2025-10-31. | 2025-10-31 |
| `neo4j:5.x` (5, 5.15, 5.22, 5.24.2) | CVE-2019-8457 (libdb5.3) | Platform squad | Neo4j 5.25 security release ETA mid-October. Prepare compose override (`docker-compose.neo.yml`) to switch tags and smoke-test backup/restore. | 2025-11-15 |

## 3. Outstanding criticals without baseline

| CVE | Image | Component | Owner | Decision | Next checkpoint |
| --- | --- | --- | --- | --- | --- |
| CVE-2021-29921 | `apache/nifi:2.0.0` | Python 3.9 | Platform squad | Prefer image bump; fall back to custom rebuild with patched Debian package if upstream slips. | 2025-10-09 |
| CVE-2025-50213 | `apache/airflow:2.10.4` (`:2` tag) | `apache-airflow-providers-snowflake` | DataOps squad (lead: J. Schneider) | Evaluate upgrade to Airflow 2.10.5 or backport provider patch; baseline only if vendor SLA >30 days. | 2025-10-02 |
| CVE-2025-47917 | `apache/superset:latest` | `libmbedcrypto7` | DataOps squad | Switch to `apache/superset:4.0.x` once upstream publishes fix; coordinate with BI team for regression. | 2025-10-16 |
| CVE-2024-45337, CVE-2024-24790 | `grafana/*`, `prom/*`, `redis:*` | Go stdlib / `golang.org/x/crypto` | Observability squad (lead: L. Hartmann) | Upgrade to Grafana 11.2.x / Prometheus 2.55.x builds compiled with Go ≥1.23.1. Prepare Helm chart PRs and test in staging. | 2025-10-09 |

## 4. Reporting cadence

- Update this tracker immediately after running `scripts/run_vuln_policy_images.py`.
- During security sync, review approaching deadlines (≤14 days) and decide on baseline renewals vs. upgrades.
- Once remediation lands, remove the baseline entry from `policy/vuln_baseline_images.json` and document the fix in `DOCS_DIFF.md`.

## 5. References

- `artifacts/security/images/scan_summary.json` – machine-readable totals & delta.
- `policy/vuln_baseline_images.json` – accepted CVEs with expiries.
- `docs/security/vulnerability_scanning.md` – gate overview and remediation notes.
