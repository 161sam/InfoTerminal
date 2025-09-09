➡ Consolidated at: ../dev/guides/flowise-agents.md#docs-blueprints-flowise-agents-blueprint-md
# 🔌 FLOWISE-AGENTS-BLUEPRINT

## 🎯 Ziele
- Low-Code Orchestrierung von Research-/OSINT-Agents (Plan → Tools → Verifikation → Dossier).
- Sicherer Zugriff auf interne Daten & Module (Search, Graph, RAG, Verification, Forensics).
- Presets laden kuratierte Agent-Sets (z. B. Disinfo, Compliance, Crisis).
- Governance: Sandboxing, OPA-Policies, Audit, Rate/Cost-Limits, PII-Schutz.

## 🧭 Architektur
**Komponenten**
- **Flowise** (UI/Runtime): Agent-Flows, Node-Editor, Memory, Tracing.
- **Agent-Gateway (FastAPI)**: OIDC/JWT, RBAC, Rate-Limits, Audit, Secrets-Broker.
- **Tool-Adapter** (svc): Bridges zu internen Services
  `search-adapter` → OpenSearch • `graph-adapter` → Neo4j • `rag-adapter` → Laws/Docs
  `verify-adapter` → Claims/Evidence/RTE/Media • `geo-adapter` → Geocoding/Geo-Checks • `dossier-adapter` → Render/Export
- **Agent-Registry** (Postgres + YAML): signierte Agent-Definitionen, Versionierung.
- **Mem-Store** (Redis/PG): Chat-Memory, Tool-Caches, Rate-Counter.
- **Observability**: Logs→Loki, Traces→Tempo, Metrics→Prometheus.

**Datenfluss**
Flowise Flow → `agent-gateway` (JWT) → `tool-adapter` → Internal API (search/graph/rag/verify) → Flowise → optional `dossier-adapter` (Export).

## 🔒 Security & Governance
- **Sandbox**: Tool-Adapter laufen in gVisor/Kata; Default **no-net** außer whitelisted Egress.
- **OPA Policies**: pro Agent/Tool (Rego) → Endpunkte, Parameter-Limits, MaxDocs, MaxTokens.
- **Vault**: Secrets/Keys per Tenant/Agent, short-lived tokens.
- **PII/Compliance**: Prompt/Response-Scrubber, robots.txt-Enforcer, Audit-Trails.
- **Rate/Cost Guards**: QPS/TTL/Token-Budget; Stop bei Kosten-Limit.

> **Hinweis:** Intrusive/angriffsnahe Tools sind per Default **deaktiviert**. Nur passive OSINT-Werkzeuge und rechtlich zulässige Datenquellen. Exploitation/DoS/Intrusion werden durch Policy unterbunden.

## 🗺️ Roadmap-Anbindung
- **v0.2 (MVP):** Deploy Flowise, Agent-Gateway; Adapter v1 (search/graph/rag); Starter-Agents (Research Assistant, Graph Scout, Dossier Drafter).
- **v0.3:** Adapter v2 (verify, geo); Agents: Legal Compliance Checker, Disinfo Hunter, Supply Risk Scout, Video Evidence Extractor, Timeline Builder; n8n/NiFi-Nodes.
- **v0.5:** Adapter v3 (financial, geo-anomaly, humanitarian indicators); Agents: Financial Red-Flag, Geo Watch, Crisis Early-Warning, Lobby-Influence Mapper; Memory/Context & OPA Hardening.
- **v1.0:** Meta-Planner Agent, vollständige Preset-Agent-Sets, Eval-Suites, interner Agent-Store.

## 🧩 Preset → Default Agents
| Preset              | Default Agents                                              |
➡ Consolidated at: ../dev/guides/flowise-agents.md#
- `POST /tool/graph.cypher` → { query, params? } → rows[]
- `POST /tool/rag.retrieve` → { domain, query, topK? } → passages[]
- `POST /tool/verify.claim_extract` → { text } → claims[]
- `POST /tool/verify.evidence_retrieve` → { claim } → passages[]
- `POST /tool/verify.rte` → { claim, evidence } → { label, score }
- `POST /tool/forensics.image` → { url|bytes } → { exif, phash, reverse }
- `POST /tool/dossier.render` → { template, data } → { url }

## 📦 Agent-Registry Beispiel
```yaml
id: disinfo_hunter@1.2.0
title: "Disinfo Hunter"
owner: "intel-team"
llm: { provider: "openai", model: "gpt-4o-mini" }
tools: [verify.claim_extract, verify.evidence_retrieve, verify.rte, verify.media_forensics, search.query]
limits: { max_tokens: 4000, max_docs: 50, qps: 0.5 }
security: { policy: "policies/disinfo_hunter.rego", sandbox: "default-no-net" }
presets: [disinfo_watchdog]
observability: { tracing: true, redact_pii: true }
````

## 🧪 Evaluation

Metriken: factuality\@k, pass\@1, latency p95, cost/1k tokens, tool-error-rate.
Canary-Rollout 10 % → Auto-Rollback bei SLO-Bruch.

## ✅ Tickets (Auszug)

FLOWISE-1 Deploy • FLOWISE-2 Gateway • FLOWISE-3 Adapter v1 • FLOWISE-4 Registry • FLOWISE-5 Starter-Agents • FLOWISE-6 n8n-Node • FLOWISE-7 NiFi-Processor • FLOWISE-8 Adapter v2 • FLOWISE-9 OPA/Sandbox • FLOWISE-10 Preset Wiring • FLOWISE-11 Eval • FLOWISE-12 Meta-Planner • FLOWISE-13 Cost Guards • FLOWISE-14 Canary/Rollback


---

### `docs/api/agent-gateway.md`
```markdown
➡ Consolidated at: ../dev/guides/flowise-agents.md#agent-gateway-api
Base URL: `/api/agent` • Auth: **OIDC Bearer JWT** (`Authorization: Bearer <token>`)

## Gemeinsame Konventionen
- **Content-Type:** `application/json`
- **Errors:** RFC 7807 (Problem+JSON)
- **Rate-Limits:** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`
- **Tracing:** `X-Request-ID` (Client kann setzen)

## Health
`GET /healthz` → `200 {"status":"ok"}`
`GET /readyz` → Readiness

## Agents
- `GET /agents` → registrierte Agents (id, title, version, owner)
- `POST /agents/{id}:invoke`
  - Req: `{ "input": "...", "context": {...}, "preset":"disinfo_watchdog", "limits": { "maxDocs": 50, "timeoutMs": 30000 } }`
  - Res: `{ "steps": [...], "output": "...", "evidence": [...], "cost": {...} }`

## Tool-Adapter
- `POST /tool/search.query` → `{q, filter?, topK?}` → `{docs:[{id,score,source,excerpt}]}`
- `POST /tool/graph.cypher` → `{query, params?}` → `{rows:[...]}`
- `POST /tool/rag.retrieve` → `{domain:"laws|docs", query, topK?}` → `{passages:[...]}`
- `POST /tool/verify.claim_extract` → `{text}` → `{claims:[{id,text,spans}]}`
- `POST /tool/verify.evidence_retrieve` → `{claim}` → `{passages:[...]}`
- `POST /tool/verify.rte` → `{claim,evidence}` → `{label:"supports|refutes|neutral",score:0..1}`
- `POST /tool/forensics.image` → `{url|bytes}` → `{exif:{},phash:"...",reverse:[...]}`
- `POST /tool/dossier.render` → `{template,data}` → `{url:"/artifacts/..."}`

## Fehlercodes
- `400` Bad Request (Schema/Policy)
- `401/403` Auth/Policy verletzt (RBAC/OPA)
- `409` Limits (Rate/Cost/Docs) erreicht
- `422` Tool Validation (z. B. unsichere URL)
- `429` Throttle
- `5xx` Adapter/Backend Fehler

## Beispiele

### Invoke Agent
```bash
curl -H "Authorization: Bearer $JWT" \
     -H "Content-Type: application/json" \
     -d '{ "input":"Analysiere Posts zu Narrativ X", "preset":"disinfo_watchdog" }' \
     https://host/api/agent/agents/disinfo_hunter@1.2.0:invoke
````

### Evidence + RTE

```bash
curl -H "Authorization: Bearer $JWT" -H "Content-Type: application/json" \
     -d '{ "claim":"...", "topK":5 }' \
     https://host/api/agent/tool/verify.evidence_retrieve
```

## Sicherheit & Compliance

* Default: **read-only** Tools (passive OSINT). Intrusive Tools (Portscans, Exploits) sind **deaktiviert**.
* OPA Policies (Rego) erzwingen Param-Limits & Quellen-Whitelists.
* Secrets via Vault (per-tenant, short-lived).



---

### `docs/nodes/flowise_n8n.md`
```markdown
# n8n Node – Run Flowise Agent
➡ Consolidated at: ../dev/guides/flowise-agents.md#
Flowise-Agent aus n8n Workflows anstoßen (Alerts, Dossiers, Batch-Analysen).

## Inputs
- JSON:
  `case_id` (string), `prompt` (string), `context` (object), `preset` (string), `limits` (object)

## Optionen
- `agentId` (z. B. `disinfo_hunter@1.2.0`)
- `timeoutMs` (Default 30000)
- `budgetTokens` (Default 2000)

## Output
- `agent_result`: `{ steps, output, evidence, cost, request_id }`

## Beispiel (HTTP Request Node)
- Methode: POST
- URL: `/api/agent/agents/{{ $json.agentId }}:invoke`
- Header: `Authorization: Bearer {{$json.jwt}}`, `Content-Type: application/json`
- Body RAW JSON:
```json
{
  "input": "{{ $json.prompt }}",
  "context": {{ $json.context }},
  "preset": "{{ $json.preset }}",
  "limits": {{ $json.limits }}
}
````

## Fehlerbehandlung

* `429` → Wait & Retry mit Exponential Backoff
* `409` → Budget erhöhen oder Batch verkleinern
* `5xx` → Fallback Agent/Tool, Alert an On-Call

## Use-Cases

* Narrative-Alerts → Dossier Draft
* Compliance-Watchlist → Auto-Check + Report
* Crisis-Signals → Risk-Dossier



---

### `docs/nodes/flowise_nifi.md`
```markdown
# NiFi Processor – InvokeFlowiseAgent

➡ Consolidated at: ../dev/guides/flowise-agents.md#zweck

## Properties
- `Agent ID` (string, required) – `disinfo_hunter@1.2.0`
- `Preset` (string) – z. B. `disinfo_watchdog`
- `JWT Secret` (controller service) – Token Generator/Provider
- `Max Docs` (int) – 50
- `Timeout Ms` (int) – 30000
- `Gateway URL` – `/api/agent/agents/{id}:invoke`

## Relationships
- `success` – Agent-Result → FlowFile Attribute `agent.result`
- `failure` – Fehlerhaft → DLQ
- `retry` – Rate/Timeout → Retry Queue

## FlowFile Erwartung
- Input: JSON im Content (`{ "prompt":"...", "context":{...} }`)
- Output: Attribs: `request.id`, `agent.cost`, `agent.label`; Content passthrough.

## Hinweise
- Backpressure auf `retry` konfigurieren
- Secrets aus Vault Controller Service
- Policies: nur zugelassene Quellen/Hosts
````

---

## Aktualisierte Presets (mit `default_agents`)

### `docs/presets/journalism.yaml`

```yaml
profile: journalism
description: "Preset für Recherche & Fact-Checking (Incognito+)."
security:
  mode: incognito
  egress: tor+vpn
  doh: true
  block_dns: true
  ephemeral_fs: true
  logging_persist: false
verification:
  weights: {source:0.20, content:0.15, corro:0.25, rte:0.20, temporal:0.10, geo:0.05, media:0.05}
  thresholds:
    verified: {score: 0.85, conf: 0.70}
    likely_true: {score: 0.70, conf: 0.60}
nifi_context: JournalismContext
nifi_enable: [ingest_social, ingest_open_data, claim_extract_cluster, evidence_retrieval, rte_scoring, aggregate_upsert]
n8n_enable: [narrative_cluster_alerts, controversy_escalation, dossier_export]
frontend:
  dashboards: { default: disinformation }
  views: { narratives_panel: true, review_ui: true }
  search_defaults: { time_range: "30d", badges_min: "uncertain" }
  dossier_template: "journalism_short.md.tmpl"
plugins:
  whitelist: [exiftool, imagehash, whois]
default_agents: [research_assistant, disinfo_hunter, dossier_drafter]
```

### `docs/presets/agency.yaml`

```yaml
profile: agency
description: "Behörden/Firmen – Forensics+ (Compliance, Risk, Audit)."
security:
  mode: forensics
  egress: proxy
  doh: true
  block_dns: true
  ephemeral_fs: false
  logging_persist: true
  worm_buckets: true
  chain_of_custody: true
verification:
  weights: {source:0.25, content:0.10, corro:0.25, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds:
    verified: {score: 0.90, conf: 0.80}
nifi_context: AgencyContext
nifi_enable: [ingest_laws, rag_index, ingest_financial_data, enrich_sanctions, aggregate_upsert]
n8n_enable: [compliance_alerts, financial_red_flag_alerts, chain_of_custody_report]
frontend:
  dashboards: { default: compliance, tabs_enabled: ["legal","financial","search","graphx"] }
  search_defaults: { badges_min: "verified", audit_overlay: true }
  dossier_template: "compliance_risk_report.md.tmpl"
plugins:
  whitelist: [exiftool, pdfid, yara]   # Intrusive Tools bleiben deaktiviert
default_agents: [legal_compliance_checker, financial_red_flag, lobby_mapper]
```

### `docs/presets/research.yaml`

```yaml
profile: research
description: "Forschung – Balanced (Datenfusion, Trends, Dossiers)."
security:
  mode: standard
  egress: proxy
  doh: true
  block_dns: true
  ephemeral_fs: false
  logging_persist: true
verification:
  weights: {source:0.18, content:0.12, corro:0.22, rte:0.22, temporal:0.12, geo:0.08, media:0.06}
  thresholds:
    verified: {score: 0.82, conf: 0.70}
nifi_context: ResearchContext
nifi_enable: [ingest_open_data, ingest_economic_data, aggregate_upsert]
n8n_enable: [weekly_digest, trend_report, dossier_export]
frontend:
  dashboards: { default: search }
  views: { time_series: true, geo_layer: true }
  dossier_template: "journalism_short.md.tmpl"
plugins:
  whitelist: [exiftool, whois]
default_agents: [research_assistant, graph_scout, timeline_builder]
```

### `docs/presets/climate_researcher.yaml`

```yaml
profile: climate_researcher
description: "Preset für Klimarisiko-Analysen (Climate Intelligence)."
security: { mode: standard, egress: proxy, doh: true, block_dns: true, ephemeral_fs: false, logging_persist: true }
verification:
  weights: {source:0.15, content:0.10, corro:0.20, rte:0.20, temporal:0.10, geo:0.15, media:0.10}
  thresholds: { verified: {score: 0.80, conf: 0.70}, likely_true: {score: 0.65, conf: 0.55} }
nifi_context: ClimateContext
nifi_enable: [ingest_climate_data, ingest_open_data, geo_enrich_standard, aggregate_upsert]
n8n_enable: [climate_alerts, climate_quarterly_report]
frontend:
  dashboards: { default: climate }
  views: { climate_heatmap: true, geo_layer: true }
  search_defaults: { time_range: "90d", badges_min: "uncertain" }
  dossier_template: "climate_risk_report.md.tmpl"
plugins: { whitelist: [exiftool, imagehash, whois] }
default_agents: [climate_data_analyst, dossier_drafter]
```

### `docs/presets/compliance_officer.yaml`

```yaml
profile: compliance_officer
description: "Preset für Legal & Financial Intelligence mit forensischen Anforderungen."
security: { mode: forensics, egress: proxy, ephemeral_fs: false, logging_persist: true, worm_buckets: true, chain_of_custody: true }
verification:
  weights: {source:0.25, content:0.10, corro:0.25, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds: { verified: {score: 0.90, conf: 0.80}, likely_true: {score: 0.75, conf: 0.65} }
  evidence_required: { min_independent_sources: 3, must_include: ["gov","ngo","reputable_press"] }
nifi_context: ComplianceContext
nifi_enable: [ingest_laws, rag_index, ingest_financial_data, enrich_sanctions, link_leak_entities, aggregate_upsert]
n8n_enable: [compliance_alerts, lobbying_influence_report, financial_red_flag_alerts, chain_of_custody_report]
frontend:
  dashboards: { default: compliance, tabs_enabled: ["legal","financial","search","graphx"] }
  search_defaults: { badges_min: "verified", audit_overlay: true }
  dossier_template: "compliance_risk_report.md.tmpl"
plugins: { whitelist: [exiftool, pdfid, yara], policy: { sandbox: "default-no-net" } }
default_agents: [legal_compliance_checker, supply_risk_scout]
```

### `docs/presets/crisis_analyst.yaml`

```yaml
profile: crisis_analyst
description: "Preset für Humanitarian & Geopolitical Intelligence."
security: { mode: incognito, egress: tor+vpn, doh: true, block_dns: true, ephemeral_fs: true, logging_persist: false }
verification:
  weights: {source:0.20, content:0.10, corro:0.20, rte:0.20, temporal:0.15, geo:0.15, media:0.00}
  thresholds: { verified: {score: 0.82, conf: 0.70}, likely_true: {score: 0.68, conf: 0.58} }
nifi_context: CrisisContext
nifi_enable: [ingest_health_weather_data, ingest_adsb, ingest_ais, merge_geo_social, detect_geo_anomalies, aggregate_upsert]
n8n_enable: [crisis_risk_alerts, conflict_reports, humanitarian_weekly_digest]
frontend:
  dashboards: { default: crisis }
  views: { geo_map: true, timeline: true }
  search_defaults: { time_range: "30d", badges_min: "likely_true" }
  dossier_template: "humanitarian_crisis_report.md.tmpl"
plugins: { whitelist: [exiftool, imagehash, whois] }
default_agents: [crisis_early_warning, geo_watch, timeline_builder]
```

### `docs/presets/disinfo_watchdog.yaml`

```yaml
profile: disinfo_watchdog
description: "Preset für Desinformations-Erkennung (Narrative, Botnets, Kampagnen)."
security:
  mode: incognito
  egress: tor+vpn
  doh: true
  block_dns: true
  ephemeral_fs: true
  logging_persist: false
  browser_pool: { webrtc_off: true, robots_enforce: true }
verification:
  weights: {source:0.20, content:0.15, corro:0.25, rte:0.25, temporal:0.05, geo:0.05, media:0.05}
  thresholds: { verified: {score: 0.85, conf: 0.70}, likely_true: {score: 0.70, conf: 0.60} }
  active_learning: true
  sample_uncertain_for_labeling: 0.3
nifi_context: DisinfoContext
nifi_enable: [ingest_social, claim_extract_cluster, bot_detection, evidence_retrieval, rte_scoring, aggregate_upsert]
n8n_enable: [narrative_cluster_alerts, botnet_dossiers, controversy_escalation]
frontend:
  dashboards: { default: disinformation }
  views: { narratives_panel: true, review_ui: true }
  search_defaults: { time_range: "30d", badges_min: "uncertain", sort: "recency+score" }
  dossier_template: "disinfo_campaign_report.md.tmpl"
plugins: { whitelist: [exiftool, imagehash, whois] }
default_agents: [disinfo_hunter, media_auth_assistant]
```

### `docs/presets/economic_analyst.yaml`

```yaml
profile: economic_analyst
description: "Preset für Economic Intelligence (Branchen, Märkte, Risiken)."
security: { mode: standard, egress: proxy, doh: true, block_dns: true, ephemeral_fs: false, logging_persist: true }
verification:
  weights: {source:0.20, content:0.05, corro:0.20, rte:0.20, temporal:0.15, geo:0.10, media:0.10}
  thresholds: { verified: {score: 0.80, conf: 0.70}, likely_true: {score: 0.65, conf: 0.55} }
nifi_context: EconomicContext
nifi_enable: [ingest_economic_data, ingest_open_data, aggregate_upsert]
n8n_enable: [economic_weekly_report, market_risk_alerts, sector_trend_dossiers]
frontend:
  dashboards: { default: economic }
  views: { time_series: true, sector_heatmap: true }
  search_defaults: { time_range: "180d", badges_min: "uncertain" }
  dossier_template: "economic_intelligence_report.md.tmpl"
plugins: { whitelist: [whois, exiftool, imagehash] }
default_agents: [economic_trend_analyst, supply_risk_scout]
```

---

### **TODO-Index Ergänzung (neuer Abschnitt)**

> füge ans Ende von `docs/TODO-Index.md` hinzu:

```markdown
## 27. FlowiseAI Agents
- [ ] **[FLOWISE-1]** Flowise Deployment (Container, OIDC via Agent-Gateway)
- [ ] **[FLOWISE-2]** Agent-Gateway (Auth, RBAC, Rate-Limit, Audit, Vault)
- [ ] **[FLOWISE-3]** Tool-Adapter v1 (search, graph, rag)
- [ ] **[FLOWISE-4]** Agent-Registry (PG + YAML Sign + API)
- [ ] **[FLOWISE-5]** Starter-Agents (Research, Graph, Dossier)
- [ ] **[FLOWISE-6]** n8n Node `Run Flowise Agent`
- [ ] **[FLOWISE-7]** NiFi Processor `InvokeFlowiseAgent`
- [ ] **[FLOWISE-8]** Tool-Adapter v2 (verify, geo, forensics)
- [ ] **[FLOWISE-9]** Security Policies (OPA Rego + Sandbox Profiles)
- [ ] **[FLOWISE-10]** Preset Wiring (default_agents)
- [ ] **[FLOWISE-11]** Eval Suites + CI Scorer
- [ ] **[FLOWISE-12]** Meta-Planner Agent (v1.0)
- [ ] **[FLOWISE-13]** Cost/Token Budgets + Alerts
- [ ] **[FLOWISE-14]** Canary & Rollback Mechanik
```
