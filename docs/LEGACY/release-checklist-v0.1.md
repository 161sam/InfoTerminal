

> **Legacy Notice (v0.1)**  
> This document describes pre-v0.2 behavior and is kept for historical reference.  
> See the updated docs in `docs/` and the v0.2 roadmap for current guidance.

# 🚀 Release-Checkliste v0.1 – InfoTerminal

Version: **v0.1.0**  
Ziel: Erste stabile Staging-Release mit allen Kernfunktionen (Security, CI, Data, Pipelines, Observability, Docs).

---

## 1. Code & Security

- [ ] Alle **PRs gemergt** (Security, Tests, dbt, Pipelines, Observability, Docs).
- [ ] **Conftest/OPA Policies** laufen sauber (`make ci-policy`).
- [ ] **Secrets entfernt** aus Manifests/Code (`grep -R "password" infra/ services/ | grep -v example` → leer).
- [ ] **ExternalSecrets** konfiguriert für DBs, Keycloak, OAuth-Proxy.
- [ ] **Ingress TLS** aktiv (cert-manager, staging Issuer OK).
- [ ] Optional: **mTLS Overlay** dokumentiert (falls Mesh aktiv).

---

## 2. Tests & CI/CD

- [ ] **Pytest** für Search-API & Graph-API grün (inkl. Coverage-Report).
- [ ] **Vitest** Frontend-Tests laufen (mind. SearchBox/Detail-Page).
- [ ] **Playwright E2E Smoke**: Dummy-Login → Suche → Graph → Asset-Detail funktioniert.
- [ ] **CI-Pipeline** (lint, typecheck, tests, e2e, security-scan, perf-smoke) grün.
- [ ] **Dependabot** aktiviert (pip, npm, GitHub Actions).
- [ ] **Trivy Scan** ohne kritische Findings.

---

## 3. Datenqualität & Warehouse

- [ ] **dbt build/test** grün (Seeds, Models, Tests).
- [ ] **dbt docs generate** erzeugt Artefakt (Docs erreichbar).
- [ ] **Snapshots** (dim_asset SCD2) laufen (`dbt snapshot`).
- [ ] **Exposures** definiert (Superset Dashboards verlinkt).
- [ ] **Freshness Checks** für Sources ohne Errors.

---

## 4. Analytics-Frontend

- [ ] **Superset Dashboard** „analytics_prices“ importiert:
  - Charts: Close, Volume, Volatility(7d/30d), OHLC
  - Native Filter + Cross-Filter aktiv
- [ ] **Deep-Link** von Superset zu Frontend `/asset/[id]` funktioniert.
- [ ] Frontend-Detailseiten für **Asset** & **Person** verfügbar (Charts, Graph-Snippet, News).
- [ ] **Vitest/Playwright Tests** decken Detailseiten ab.

---

## 5. Pipelines & Automation

- [ ] **NiFi Flow** aktiv: Watch-Folder → Aleph Upload → Erfolg/Fehlerpfade sichtbar.
- [ ] **Airflow DAG** `openbb_dbt_superset` läuft: OpenBB → dbt run/test → Superset Refresh.
- [ ] **CronJobs** für Backups aktiv (Postgres, OpenSearch, Neo4j).
- [ ] Restore-Runbook einmal **trocken getestet**.

---

## 6. Observability

- [ ] **OTel Collector** deployed (4317/4318/9464 erreichbar).
- [ ] **Python Services** exportieren Traces + `/metrics`.
- [ ] **Node Services** exportieren Traces + `/metrics`.
- [ ] **Prometheus** scrapt Services; Grafana Panels gefüllt.
- [ ] **Tempo** zeigt Traces End-to-End (Frontend → Gateway → APIs → DB).
- [ ] **Loki** enthält Logs aller Services (Promtail shipping OK).
- [ ] **Grafana Dashboards**:
  - API-SLO: p95 Latency, Throughput, Error-Rate
  - Infra Overview: CPU/Mem, DB Stats, Pod Restarts

---

## 7. Docs & Developer Experience

- [ ] **README** Quickstart aktualisiert (Makefile Targets, Health-Checks).
- [ ] **ADRs** (mind. OPA/ABAC, Multi-Storage, OIDC, Policy Gateway) im Repo.
- [ ] **Runbooks** vorhanden: Auth/Gateway, Neo4j Recovery, Search Reindex, Superset Admin.
- [ ] **Language Policy**: Docs in EN, DE als Appendix.
- [ ] **CONTRIBUTING.md**, **CODEOWNERS**, Issue/PR-Templates im Repo.
- [ ] **CI Docs-Checks** grün (markdownlint, link check, doctoc).

---

## 8. Staging-Rollout

- [ ] **Secrets** in Staging (Vault/ExternalSecrets) gesetzt.
- [ ] **Ingress Hosts** & TLS validiert.
- [ ] **Demo-Data Seed** erfolgreich (`make seed-demo`).
- [ ] **Smoke-Test** im Staging:
  - Frontend erreichbar
  - Suche liefert Treffer
  - Graph zeigt Knoten
  - Dashboard lädt
  - Trace erscheint in Tempo
  - Metrics sichtbar
  - Logs sichtbar

---

## 9. Release Management

- [ ] `main` eingefroren, `release/v0.1` Branch erstellt.
- [ ] **Changelog** generiert (`git log --oneline v0.0.0..HEAD`).
- [ ] **Release Notes** erstellt (Features, Breaking Changes, Known Issues).
- [ ] **Tag v0.1.0** gesetzt und Release publiziert.
- [ ] Dokumentation zur Installation/Exploration angehängt.

---

✅ Wenn alle Punkte erledigt → **Release v0.1 fertig!**
