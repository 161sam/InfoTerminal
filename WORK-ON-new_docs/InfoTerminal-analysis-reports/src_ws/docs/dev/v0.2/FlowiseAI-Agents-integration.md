alles klar — ich ergänze den Entwicklungsplan um die **FlowiseAI Agents** (so wie wir’s zuvor angedacht hatten) und mache es direkt **repo-tauglich**: Ziele, Architektur, Phasen-Roadmap, Integrationspunkte (NiFi/n8n), Security/Governance, Presets, Tickets, Beispiel-Configs.

---

# 🔌 FlowiseAI Agents – Ergänzung zum Entwicklungsplan

## 🎯 Ziele

* **Low-Code Orchestration** von Agents für Research/OSINT Tasks (Plan → Tools → Verifikation → Dossier).
* **Tool- und Datenzugriff** über sichere Adapter (Search, Graph, RAG, Verifikation, Forensics).
* **Presets** laden kuratierte Agents (z. B. *Disinfo-Analyst*, *Compliance-Checker*, *Crisis Watch*).
* **Governance/Security**: Sandboxing, Policy, Audit, Rate-Limits, Prompt/Response-Logging (PII-aware).

---

## 🧭 Architektur (Flowise ↔ InfoTerminal)

**Komponenten**

* **flowise/** (Container): FlowiseAI UI/Runtime (Nodes, Flows, Memory, Tracing).
* **agent-gateway (FastAPI)**: Auth (OIDC), Routing, Rate-Limits, RBAC, Audit, Secrets-Broker.
* **tool-adapter svc**: sichere Bridges zu internen Services:

  * `search-adapter` → OpenSearch
  * `graph-adapter` → Neo4j
  * `rag-adapter` → Gesetzes-RAG, Docs-RAG (OpenSearch+embeddings)
  * `verify-adapter` → Evidence/RTE/Forensics
  * `geo-adapter` → Geocoding/Geo-checks
  * `dossier-adapter` → Render/Export
* **agent-registry** (Postgres table + YAML): signierte Agent-Definitionen, Versionierung, Preset-Zuordnung.
* **mem-store** (Redis/PG): ChatMemory, ToolCaches, Rate Counters.
* **observability**: Logs→Loki, Traces→Tempo, Metrics→Prometheus.

**Datenfluss (vereinfachter Pfad)**
Flowise Flow → `agent-gateway` (JWT) → `tool-adapter` → Internal API (search/graph/rag/verify) → Rückgabe → Flowise → `dossier-adapter` (optional Export).

---

## 🚧 Phasen-Integration (an Roadmap andocken)

### Phase 1 — v0.2 (MVP)

* **Setup:** FlowiseAI als Service, OIDC-Login via `agent-gateway`.
* **Adapter v1:** `search-adapter`, `graph-adapter`, `rag-adapter`.
* **Starter-Agents (3):**

  * *Research Assistant* (Search+RAG)
  * *Graph Scout* (Entity/Relation Queries)
  * *Dossier Drafter* (Evidence → Dossier-Template)
* **Security:** API-Keys in Vault, per-user JWT passthrough, basic rate-limits.
* **Deliverables:** Flowise UI erreichbar, 3 Flows produktiv, Audit-Logs aktiv.

### Phase 2 — v0.3 (Intelligence Packs I)

* **Adapter v2:** `verify-adapter` (Claim, Evidence, RTE, Media), `geo-adapter`.
* **Agents (5):**

  * *Legal Compliance Checker* (RAG Laws + Mapping)
  * *Disinfo Hunter* (Claim-Cluster + Bot Hinweise)
  * *Supply Risk Scout* (Sanctions + Supply Graph)
  * *Video Evidence Extractor* (Transkript + Objects)
  * *Timeline Builder* (Events + Quellen)
* **n8n/NiFi Integration:** neue **Flowise-Nodes**:

  * `n8n:run_flowise_agent` (invoke agent with payload)
  * `nifi:flowise_webhook` (Flowise → NiFi ingest hook)
* **Governance:** Agent Registry + Signoff (owner, scope, tools, rate).

### Phase 3 — v0.5 (Intelligence Packs II)

* **Adapter v3:** Financial (transfers/leaks), Geo (ADS-B/AIS anomaly), Humanitarian (indicator fusion).
* **Agents (4):**

  * *Financial Red-Flag Analyst*
  * *Geo Watch* (movement anomalies)
  * *Crisis Early-Warning*
  * *Lobby-Influence Mapper* (Politicians ↔ Firms ↔ Laws)
* **Memory/Context:** episodic memory per Case, Retrieval Hints.
* **Safety:** Policy-Engine (OPA) erzwingt Tool-Cap Limits, PII Masking.

### Phase 4 — v1.0 (Full Spectrum)

* **Meta-Planner Agent:** wählt Sub-Agents/Pipelines (Toolformer-Stil).
* **Preset-Agent Sets** pro Profil (Climate, Tech, Terror, Health, AI-Ethics, Media, Economic, Cultural).
* **Evaluation:** scripted evals pro Agent (success\@k, factuality, latency, cost).
* **Marketplace/Store (internal):** genehmigte Agents versioniert, changelog, rollbacks.

---

## 🧱 Security & Governance

* **Sandbox:** Tool-Adapter laufen in gVisor/Kata; Default: **no-net** außer explizit freigegeben.
* **OPA Policies:** pro Agent/Tool (`agent.yaml`) → erlaubte Endpunkte, Parameter-Limits, Max-Docs, Max-Tokens.
* **Vault:** Secrets/Keys scopen per Tenant/Agent; short-lived tokens.
* **PII & Compliance:** Prompt/Response Scrubber, Domain-blacklist, robots.txt-Enforcer, Audit-Trails (Loki).
* **Rate/Cost Guards:** QPS, TTL, Token-Budgets; Hard Stop bei Kostenlimit.

---

## 🧩 Preset-Anbindung (Defaults)

| Preset             | Default Agents                                                               |
| ------------------ | ---------------------------------------------------------------------------- |
| Journalism         | Research Assistant, Disinfo Hunter, Dossier Drafter                          |
| Agency/Compliance  | Legal Compliance Checker, Financial Red-Flag Analyst, Lobby-Influence Mapper |
| Research           | Research Assistant, Graph Scout, Timeline Builder                            |
| Climate Researcher | Climate Data Analyst, Dossier Drafter                                        |
| Compliance Officer | Legal Compliance Checker, Supply Risk Scout                                  |
| Crisis Analyst     | Crisis Early-Warning, Geo Watch, Timeline Builder                            |
| Disinfo Watchdog   | Disinfo Hunter, Media Authenticity Assistant                                 |
| Economic Analyst   | Economic Trend Analyst, Supply Risk Scout                                    |

> Preset lädt passende Agents + begrenzte Tools (least-privilege).

---

## 📦 Beispiel: Agent Registry (YAML)

```yaml
id: disinfo_hunter@1.2.0
title: "Disinfo Hunter"
owner: "intel-team"
llm:
  provider: "openai"
  model: "gpt-4o-mini"
tools:
  - verify.claim_extract
  - verify.evidence_retrieve
  - verify.rte
  - verify.media_forensics
  - search.query
limits:
  max_tokens: 4000
  max_docs: 50
  qps: 0.5
security:
  policy: "policies/disinfo_hunter.rego"
  sandbox: "default-no-net"
presets:
  - disinfo_watchdog
observability:
  tracing: true
  redact_pii: true
```

---

## 🔗 Tool-Adapter – Beispiel Endpunkte

* `POST /tool/search.query` → { q, filter, topK } → OpenSearch
* `POST /tool/graph.cypher` → { query, params } → Neo4j
* `POST /tool/rag.retrieve` → { domain, query } → Laws/Docs
* `POST /tool/verify.claim_extract` → { text } → claims\[]
* `POST /tool/verify.evidence_retrieve` → { claim } → passages\[]
* `POST /tool/verify.rte` → { claim, evidence } → {label,score}
* `POST /tool/forensics.image` → { url|bytes } → {exif, phash, reverse}
* `POST /tool/dossier.render` → { template, data } → PDF/MD

Alle hinter dem **agent-gateway** (JWT, OPA, Rate-Limit).

---

## 🔄 NiFi / n8n Knoten (Integration)

* **n8n node:** `Run Flowise Agent`

  * Inputs: JSON (case\_id, prompt, context, constraints)
  * Options: agentId, timeout, budgetTokens, preset
  * Output: agent\_result (steps, evidence, dossier\_snippet)
* **NiFi processor:** `InvokeFlowiseAgent`

  * Properties: Agent ID, JWT Secret, MaxDocs, Output to FlowFile
  * Use-Cases: Batch-Analyse, On-Ingest Auto-Tagging, Claim-Prelabels

---

## 🧪 Evaluation & QA

* **Agent Eval Suites** (per Blueprint): curated tasks, gold labels.
* **Metriken:** factuality\@k, pass\@1, latency p95, cost/1k tokens, tool-error rate.
* **Canary Rollouts:** new agent\@version → 10% traffic, auto-revert on SLO breach.
* **Playbooks:** failure modes (hallucination, overreach, timeouts) → mitigations (tool fallback, retry w/ guardrails).

---

## 📋 Tickets (zum TODO-Index hinzufügen)

* **\[FLOWISE-1]** FlowiseAI Deployment (container, OIDC via agent-gateway)
* **\[FLOWISE-2]** Agent Gateway (FastAPI) – Auth, RBAC, Rate-Limit, Audit
* **\[FLOWISE-3]** Tool-Adapter v1 (search, graph, rag)
* **\[FLOWISE-4]** Agent Registry (PG + YAML sign + API)
* **\[FLOWISE-5]** Starter-Agents (Research, Graph, Dossier)
* **\[FLOWISE-6]** n8n Node `run_flowise_agent`
* **\[FLOWISE-7]** NiFi Processor `InvokeFlowiseAgent`
* **\[FLOWISE-8]** Tool-Adapter v2 (verify, geo, forensics)
* **\[FLOWISE-9]** Security Policies (OPA rego + sandbox profiles)
* **\[FLOWISE-10]** Preset-Wiring (defaults + least-privilege tools)
* **\[FLOWISE-11]** Eval Suites + CI Scorer
* **\[FLOWISE-12]** Meta-Planner Agent (v1.0)
* **\[FLOWISE-13]** Cost/Token Budgets + Alerts
* **\[FLOWISE-14]** Canary & Rollback Mechanik

---

## 🧩 Beispiel Flowise-Prompt (Disinfo Hunter, Schritt-Planer)

```
System:
Du bist ein Disinformation-Analyst. Vorgehen:
1) claim_extract(text) → claims
2) Für jeden Claim: evidence_retrieve + rte
3) media_forensics bei Medien
4) Aggregation: Veracity, Unsicherheiten, offene Fragen
5) Erzeuge Dossier-Snippet (Markdown Tabellen)

Tools sind strikt einzuhalten; keine freien Webzugriffe. MaxDocs=50.

User:
Analysiere die beigefügten Posts zur These '…'
```

---

## 📘 Doku-Updates (Dateien, die ich ergänzen/erstellen würde)

* `docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md` (obiger Inhalt als eigenes Doc)
* `docs/presets/*` → Preset-Defaults um `default_agents` erweitern
* `docs/api/agent-gateway.md` (Endpoints, Auth, Fehlercodes)
* `docs/nodes/flowise_n8n.md`, `docs/nodes/flowise_nifi.md` (Node/Processor Usage)

---

## TODO:

* `docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md`
* `TODO-Index.md` (FLOWISE-Tickets anhängen)
* Preset-YAMLs um `default_agents` erweitern.
