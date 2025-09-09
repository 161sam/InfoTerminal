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
|---------------------|-------------------------------------------------------------|
| Journalism          | research_assistant, disinfo_hunter, dossier_drafter        |
| Agency/Compliance   | legal_compliance_checker, financial_red_flag, lobby_mapper |
| Research            | research_assistant, graph_scout, timeline_builder          |
| Climate Researcher  | climate_data_analyst, dossier_drafter                      |
| Compliance Officer  | legal_compliance_checker, supply_risk_scout                |
| Crisis Analyst      | crisis_early_warning, geo_watch, timeline_builder          |
| Disinfo Watchdog    | disinfo_hunter, media_auth_assistant                       |
| Economic Analyst    | economic_trend_analyst, supply_risk_scout                  |

## 🔗 Tool-Adapter Endpunkte (Kurz)
- `POST /tool/search.query` → { q, filter?, topK? } → docs[]
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
