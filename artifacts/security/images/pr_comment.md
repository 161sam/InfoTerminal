## 🚨 Container Vulnerability Scan (Images)
_Generated: 2025-09-25 06:17:36 UTC_

| Severity | Active | Accepted |
| --- | --- | --- |
| Critical | 92 | 16 |
| High | 2045 | 0 |
| Medium | 6921 | 0 |
| Low | 3823 | 0 |
| Unknown | 73 | 0 |

❌ **Policy**: 2137 vulnerabilities ≥ High (fail threshold)

**Top Active Findings**
1. **CVE-2021-29921** (Critical, apache/nifi:2.0.0) – libpython3.9 3.9.2-1; Fix: 3.9.2-1+deb11u2 – [Advisory](https://avd.aquasec.com/nvd/cve-2021-29921)
2. **CVE-2021-29921** (Critical, apache/nifi:2.0.0) – libpython3.9-dev 3.9.2-1; Fix: 3.9.2-1+deb11u2 – [Advisory](https://avd.aquasec.com/nvd/cve-2021-29921)
3. **CVE-2021-29921** (Critical, apache/nifi:2.0.0) – libpython3.9-minimal 3.9.2-1; Fix: 3.9.2-1+deb11u2 – [Advisory](https://avd.aquasec.com/nvd/cve-2021-29921)
4. **CVE-2021-29921** (Critical, apache/nifi:2.0.0) – libpython3.9-stdlib 3.9.2-1; Fix: 3.9.2-1+deb11u2 – [Advisory](https://avd.aquasec.com/nvd/cve-2021-29921)
5. **CVE-2021-29921** (Critical, apache/nifi:2.0.0) – python3.9 3.9.2-1; Fix: 3.9.2-1+deb11u2 – [Advisory](https://avd.aquasec.com/nvd/cve-2021-29921)

**Baseline Review Needed**
- ⏳ CVE-2018-3739 for infoterminal/frontend:latest expires 2025-10-15T00:00:00+00:00 – Frontend will upgrade https-proxy-agent to >=2.2.4 together with pnpm audit run.
- ⏳ CVE-2018-3750 for infoterminal/frontend:latest expires 2025-10-15T00:00:00+00:00 – Frontend package deep-extend will be removed via pnpm audit fix patch; release scheduled in sprint FT-2025.10.
- ⏳ CVE-2021-44906 for infoterminal/frontend:latest expires 2025-10-15T00:00:00+00:00 – Legacy minimist dependency to be dropped when migrating Next.js configs; mitigation tracked for sprint FT-2025.10.
- ⏳ CVE-2021-3918 for infoterminal/frontend:latest expires 2025-10-22T00:00:00+00:00 – json-schema pinned by ajv v8 transitive; upgrade to ajv 8.17.x under review.
- ⏳ CVE-2025-7783 for infoterminal/frontend:latest expires 2025-10-22T00:00:00+00:00 – Form-data dependency bump blocked by fetch polyfill change; fix scheduled alongside Next.js upgrade.

_Reports: `artifacts/security/images/` (JSON, HTML) – Baseline: `policy/vuln_baseline_images.json`_
