# 📌 Backlog – Phase 1 → v1.0

Baseline backlog derived from `STATUS.md`, `DOCS_DIFF.md`, and `ROADMAP_STATUS.md`. Epics map directly to roadmap packages A–L plus Hardening and Release. All issues target **milestone: v1.0** unless stated otherwise.

> **Phase 2 Kick-off:** The risk-reducing execution order for packages A–L and the Wave 1 (A & F) MVP checklist live in [`phase2/ITERATION-01_PLAN.md`](phase2/ITERATION-01_PLAN.md). Each wave limits concurrent work to two packages and keeps delivery gates green between increments.

## Epic Overview

| Package | Epic ID | Labels | Milestone |
| --- | --- | --- | --- |
| A) Ontologie & Graph | `pkg-A-graph` | `phase-2`, `pkg-A-graph` | `v1.0` |
| B) NLP & KI | `pkg-B-nlp` | `phase-2`, `pkg-B-nlp` | `v1.0` |
| C) Geospatial | `pkg-C-geo` | `phase-2`, `pkg-C-geo` | `v1.0` |
| D) Daten-Ingest & Workflows | `pkg-D-ingest` | `phase-2`, `pkg-D-ingest` | `v1.0` |
| E) Video-Pipeline | `pkg-E-video` | `phase-2`, `pkg-E-video` | `v1.0` |
| F) Dossier & Collaboration | `pkg-F-dossier` | `phase-2`, `pkg-F-dossier` | `v1.0` |
| G) Plugin-Architektur | `pkg-G-plugins` | `phase-2`, `pkg-G-plugins` | `v1.0` |
| H) AI-Agenten | `pkg-H-agents` | `phase-2`, `pkg-H-agents` | `v1.0` |
| I) Externe Feeds | `pkg-I-feeds` | `phase-2`, `pkg-I-feeds` | `v1.0` |
| J) Performance & Infra | `pkg-J-infra` | `phase-2`, `pkg-J-infra`, `observability` | `v1.0` |
| K) Frontend & UX | `pkg-K-ux` | `phase-2`, `pkg-K-ux` | `v1.0` |
| L) Doku & Tests | `pkg-L-docs` | `phase-2`, `pkg-L-docs` | `v1.0` |
| Hardening | `pkg-hardening` | `phase-3`, `security` | `v1.0` |
| Release | `pkg-release` | `phase-4`, `release` | `v1.0` |

---

### A) Ontologie & Graph — Epic `pkg-A-graph`
**Scope references**: `STATUS.md` (Graph & Ontologie row), `ROADMAP_STATUS.md` §A, `DOCS_DIFF.md` (ontology export gaps).

**Epic DoD**
- Graph export endpoints validated against ontology constraints.
- Geo overlays and dossier hooks powered by live graph data.
- Observability dashboards (metrics/latency) for analytics endpoints.
- Docs updated with sample Cypher + export instructions.

**Issues**
1. **A-01 Validate analytics endpoints** — Labels: `pkg-A-graph`, `service-graph-api`, `tests`, `observability`
   - Acceptance: Pytest suite covering degree/betweenness/community APIs; metrics scraped in Grafana dashboard.
   - Dependencies: Search for sample datasets (Issue L-02).
2. **A-02 Integrate graph exports with dossier** — Labels: `pkg-A-graph`, `pkg-F-dossier`, `frontend`
   - Acceptance: Dossier export uses `/export/*` endpoints; frontend GraphExplorer consumes gateway base URLs.
   - Dependencies: F-01 (dossier export pipeline).
3. **A-03 Ontology validation tooling** — Labels: `pkg-A-graph`, `docs`, `devx`
   - Acceptance: CLI command verifies ontology definitions; docs include regeneration steps.

---

### B) NLP & KI — Epic `pkg-B-nlp`
**Scope references**: `STATUS.md` (Doc-Entities row), `ROADMAP_STATUS.md` §B, `DOCS_DIFF.md` (API inventory gaps).

**Epic DoD**
- Stable summarisation + relation extraction APIs with regression tests.
- Entity linking results stored with confidence + feedback loop endpoints.
- Metrics emitted per model/task; docs include evaluation dataset references.

**Issues**
1. **B-01 Gold sample test suite** — Labels: `pkg-B-nlp`, `tests`, `service-doc-entities`
   - Acceptance: Regression tests for NER, relations, summarisation hitting `/v1/*`; coverage >80% on critical paths.
2. **B-02 Active learning feedback API** — Labels: `pkg-B-nlp`, `backend`, `observability`
   - Acceptance: Feedback endpoint persists to DB, exposes metrics, documented in API inventory.
3. **B-03 Frontend NLP integration** — Labels: `pkg-B-nlp`, `pkg-K-ux`, `frontend`
   - Acceptance: NLP page displays live outputs from doc-entities; no mock data remains.

---

### C) Geospatial — Epic `pkg-C-geo`
**Scope references**: `STATUS.md` (Graph & Ontologie row), `ROADMAP_STATUS.md` §C.

**Epic DoD**
- Geo ingest pipeline (GeoJSON/OSM) feeding graph.
- bbox/nearby/cluster APIs with pagination + timeouts.
- Map UI toggles tied to live APIs; documentation for coordinate normalisation.

**Issues**
1. **C-01 Geo ingest automation** — Labels: `pkg-C-geo`, `pkg-D-ingest`, `backend`
   - Acceptance: NiFi template imports GeoJSON into graph; retry/backoff configured.
2. **C-02 Geospatial API tests** — Labels: `pkg-C-geo`, `tests`
   - Acceptance: FastAPI tests cover bbox/nearby endpoints with fixtures; 95% path coverage.
3. **C-03 Map overlay wiring** — Labels: `pkg-C-geo`, `pkg-K-ux`, `frontend`
   - Acceptance: Frontend map components use gateway base URL; toggles documented in UX guide.

---

### D) Daten-Ingest & Workflows — Epic `pkg-D-ingest`
**Scope references**: `STATUS.md` (NiFi/n8n row), `ROADMAP_STATUS.md` §D, `DOCS_DIFF.md` (workflow docs missing).

**Epic DoD**
- Automated import/export of NiFi/n8n templates with versioning.
- Retry/backoff + DLQ for ingest failures; monitoring dashboards.
- Docs explain end-to-end pipeline configuration.

**Issues**
1. **D-01 Template automation CLI** — Labels: `pkg-D-ingest`, `cli`, `devx`
   - Acceptance: CLI command imports/updates NiFi/n8n flows idempotently; integration tests run in CI.
2. **D-02 Workflow observability** — Labels: `pkg-D-ingest`, `observability`
   - Acceptance: Prometheus exports success/failure counters for standard flows; alerts configured.
3. **D-03 Playbook runbooks** — Labels: `pkg-D-ingest`, `docs`
   - Acceptance: Markdown runbook with screenshots + troubleshooting; linked from DOCS_DIFF actions.

---

### E) Video-Pipeline — Epic `pkg-E-video`
**Scope references**: `STATUS.md` (Verification row), `ROADMAP_STATUS.md` §E.

**Epic DoD**
- NiFi → FFmpeg → ML pipeline producing metadata persisted to graph.
- Media correction UI with audit logs; performance notes documented.
- Smoke tests using demo video asset.

**Issues**
1. **E-01 Pipeline orchestration** — Labels: `pkg-E-video`, `pkg-D-ingest`, `backend`
   - Acceptance: NiFi flow executes FFmpeg task, persists metadata via API; metrics emitted.
2. **E-02 Correction UI & feedback** — Labels: `pkg-E-video`, `pkg-K-ux`, `frontend`
   - Acceptance: Verification UI allows approve/reject actions, persisting to media-forensics service.
3. **E-03 Demo dataset & docs** — Labels: `pkg-E-video`, `docs`, `release`
   - Acceptance: Demo video + walkthrough documented; linked in Release artefacts.

---

### F) Dossier & Collaboration — Epic `pkg-F-dossier`
**Scope references**: `STATUS.md` (Dossier row), `ROADMAP_STATUS.md` §F.

**Epic DoD**
- Dossier export (PDF/MD) referencing live data.
- Shared notes/comments persisted with audit trail to Loki/Tempo.
- Two dossier templates published with instructions.

**Issues**
1. **F-01 Export service implementation** — Labels: `pkg-F-dossier`, `backend`, `pkg-A-graph`
   - Acceptance: `/dossier/export` returns PDF/MD from live data; integration test verifies.
2. **F-02 Collaboration observability** — Labels: `pkg-F-dossier`, `observability`
   - Acceptance: Collab-hub exposes metrics + /readyz; dashboards for activity volume.
3. **F-03 Template documentation** — Labels: `pkg-F-dossier`, `docs`
   - Acceptance: Docs section with template descriptions, usage, and audit hooks.

---

### G) Plugin-Architektur — Epic `pkg-G-plugins`
**Scope references**: `STATUS.md` (Plugins row), `ROADMAP_STATUS.md` §G.

**Epic DoD**
- Plugin sandbox with resource/time limits, OPA checks, audit logs.
- Two production-ready plugins (nmap, whois) integrated into ingest/search.
- Docs + registry schema published.

**Issues**
1. **G-01 Sandbox hardening** — Labels: `pkg-G-plugins`, `security`
   - Acceptance: Runner enforces CPU/memory limits, timeouts, OPA validation; tests cover failure paths.
2. **G-02 Plugin ingest integration** — Labels: `pkg-G-plugins`, `pkg-D-ingest`
   - Acceptance: Plugin outputs ingested into search/graph with schema mapping.
3. **G-03 Authoring guide** — Labels: `pkg-G-plugins`, `docs`
   - Acceptance: Markdown guide with examples; referenced in DOCS_DIFF backlog.

---

### H) AI-Agenten — Epic `pkg-H-agents`
**Scope references**: `STATUS.md` (Flowise row), `ROADMAP_STATUS.md` §H.

**Epic DoD**
- Flowise connector hardened with policy enforcement + rate limits.
- Multi-agent playbooks (researcher/verifier/dossier) stored and reproducible.
- Assistant UI surfaces tool outputs with audit trail.

**Issues**
1. **H-01 Policy enforcement for agents** — Labels: `pkg-H-agents`, `security`, `policy`
   - Acceptance: OPA policies invoked per agent call; violations logged.
2. **H-02 Playbook persistence** — Labels: `pkg-H-agents`, `pkg-D-ingest`
   - Acceptance: Playbooks stored in versioned repo, CLI deploys them idempotently.
3. **H-03 Assistant UI telemetry** — Labels: `pkg-H-agents`, `pkg-K-ux`, `observability`
   - Acceptance: Frontend records agent response times/errors; dashboards created.

---

### I) Externe Feeds — Epic `pkg-I-feeds`
**Scope references**: `STATUS.md` (Ops/Egress, Plugins rows), `ROADMAP_STATUS.md` §I.

**Epic DoD**
- Integrate at least two external feeds (e.g. MISP, OTX) with rate-limit handling.
- Periodic jobs documented; dashboards for feed freshness.
- Stability notes + privacy constraints captured.

**Issues**
1. **I-01 Feed connectors** — Labels: `pkg-I-feeds`, `pkg-D-ingest`
   - Acceptance: Two connectors ingest data into OpenSearch/Neo4j with validation tests.
2. **I-02 Scheduling + monitoring** — Labels: `pkg-I-feeds`, `observability`
   - Acceptance: Scheduler metrics + alerts for stale feeds.
3. **I-03 Privacy & compliance doc** — Labels: `pkg-I-feeds`, `security`, `docs`
   - Acceptance: Documented egress/privacy review, linked to Hardening epic.

---

### J) Performance & Infra — Epic `pkg-J-infra`
**Scope references**: `STATUS.md` (Observability, Ops rows), `ROADMAP_STATUS.md` §J.

**Epic DoD**
- Metrics/health/ready coverage for all services; Grafana dashboards + alerts.
- Timeout/retry matrix documented; cache/queue strategy implemented.
- Load/perf benchmarks recorded.

**Issues**
1. **J-01 Probe coverage** — Labels: `pkg-J-infra`, `observability`
   - Acceptance: Inventory shrinks missing probes to zero; verify via script & CI.
2. **J-02 Retry/timeout matrix** — Labels: `pkg-J-infra`, `docs`, `backend`
   - Acceptance: Documentation + configuration for service timeouts/retries; tests for failure paths.
3. **J-03 Performance benchmark suite** — Labels: `pkg-J-infra`, `tests`
   - Acceptance: Repeatable load test results stored in reports with thresholds.

---

### K) Frontend & UX — Epic `pkg-K-ux`
**Scope references**: `STATUS.md` (Frontend row), `ROADMAP_STATUS.md` §K.

**Epic DoD**
- Settings page wired to OIDC/OAuth2; live indicators powered by WebSocket streams.
- Dossier template picker + responsive layouts; performance metrics tracked.
- PWA fallback documented.

**Issues**
1. **K-01 OIDC sign-in flow** — Labels: `pkg-K-ux`, `auth`, `frontend`
   - Acceptance: Frontend authenticates against auth-service/Keycloak; tests cover login/logout.
2. **K-02 Live indicators** — Labels: `pkg-K-ux`, `observability`
   - Acceptance: Graph/search status widgets consume `/healthz`; websockets tested.
3. **K-03 UX performance instrumentation** — Labels: `pkg-K-ux`, `analytics`
   - Acceptance: LCP/TTI metrics captured and surfaced; PWA manifest updated.

---

### L) Doku & Tests — Epic `pkg-L-docs`
**Scope references**: `STATUS.md` (Docs row), `DOCS_DIFF.md`, `ROADMAP_STATUS.md` §L.

**Epic DoD**
- Docs refreshed per DOCS_DIFF actions; CHANGELOG & migrations maintained.
- CI pipeline enforces lint/type/test/e2e; coverage thresholds documented.
- From-scratch runbook validated.

**Issues**
1. **L-01 Inventory-driven doc refresh** — Labels: `pkg-L-docs`, `docs`
   - Acceptance: `docs/API_INVENTORY.md`, `docs/PORTS_POLICY.md`, README, ROADMAP updated using inventory outputs.
2. **L-02 Coverage reporting** — Labels: `pkg-L-docs`, `tests`, `ci`
   - Acceptance: CI publishes coverage + lint/type reports; gating thresholds enforced.
3. **L-03 From-scratch runbook** — Labels: `pkg-L-docs`, `release`
   - Acceptance: Documented dev/demo/prod setup validated by dry run.

---

### Hardening — Epic `pkg-hardening`
**Scope references**: `STATUS.md` (Security notes), `ROADMAP_STATUS.md` Hardening section.

**Epic DoD**
- Updated threat model + pen-test checklist executed; findings tracked.
- Backup/recovery drills documented; incident response plan drafted.
- Egress/Incognito policies enforced across services & agents.

**Issues**
1. **HARD-01 Threat model update** — Labels: `pkg-hardening`, `security`
   - Acceptance: Threat model document referencing new services; reviewed with stakeholders.
2. **HARD-02 Backup & recovery drill** — Labels: `pkg-hardening`, `infra`
   - Acceptance: Automated backup verification for Postgres/Neo4j/OpenSearch; runbook updated.
3. **HARD-03 Egress policy validation** — Labels: `pkg-hardening`, `policy`
   - Acceptance: Tests ensure egress gateway/agents respect allowlists; audit logs stored.

---

### Release — Epic `pkg-release`
**Scope references**: `STATUS.md` (Release risk), `ROADMAP_STATUS.md` Release section.

**Epic DoD**
- Release notes + changelog finalised; version tags automated via `scripts/release.sh`.
- Demo datasets/flows packaged; install guides (dev/demo/prod) validated.
- CI green for lint/type/test/e2e at release tag.

**Issues**
1. **REL-01 Release playbook** — Labels: `pkg-release`, `release`
   - Acceptance: Step-by-step release checklist maintained; includes rollback plan.
2. **REL-02 Demo asset bundle** — Labels: `pkg-release`, `docs`, `pkg-D-ingest`
   - Acceptance: Demo datasets + flow exports stored and referenced in docs.
3. **REL-03 Install guides validation** — Labels: `pkg-release`, `devx`
   - Acceptance: Dev/demo/prod install docs tested; feedback captured in STATUS updates.

