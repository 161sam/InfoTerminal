## 🔍 Dependency Vulnerability Scan (SCA)
_Generated: 2025-09-24 14:24:20 UTC_

| Severity | Count |
| --- | --- |
| Critical | 5 |
| High | 25 |
| Medium | 32 |
| Low | 6 |
| Info | 0 |
| Unknown | 24 |

❌ **Policy**: 30 vulnerabilities at or above High (fail threshold)

**Top 5 CVEs / Advisories**
1. **CVE-2024-35195** (Medium, python) – Packages: requests, requests@2.31.0; Fix: 2.32.0 – [Advisory](https://github.com/psf/requests)
2. **CVE-2024-47081** (Medium, python) – Packages: requests, requests@2.31.0; Fix: 2.32.4 – [Advisory](http://seclists.org/fulldisclosure/2025/Jun/2)
3. **CVE-2024-5206** (Medium, python) – Packages: scikit-learn, scikit-learn@1.3.2; Fix: 1.5.0, 70ca21f106b603b611da73012c9ade7cd8e438b8 – [Advisory](https://github.com/pypa/advisory-database/tree/main/vulns/scikit-learn/PYSEC-2024-110.yaml)
4. **CVE-2025-2099** (Medium, python) – Packages: transformers, transformers@4.35.2; Fix: 4.49.0, 4.50.0, 8cb522b4190bd556ce51be04942720650b1a3e57 – [Advisory](https://github.com/huggingface/transformers)
5. **CVE-2025-3730** (Medium, python) – Packages: torch, torch@2.1.1, torch@2.3.1; Fix: 2.8.0 – [Advisory](https://github.com/pytorch/pytorch)

_Reports: `artifacts/security/sca/` (JSON & HTML)_

_Skipped 51 unpinned Python requirements (see summary for details)._
