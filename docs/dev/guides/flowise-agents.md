# Flowise Agents

---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L1-L3
merged_at: 2025-09-09T13:55:10.770971Z
---

### `docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md`

````markdown
---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L88-L89
merged_at: 2025-09-09T13:55:10.772956Z
---

# Agent Gateway API

---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L156-L157
merged_at: 2025-09-09T13:55:10.774697Z
---


## Zweck
---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L205-L206
merged_at: 2025-09-09T13:55:10.776341Z
---

## Zweck
Batch-Analysen während des Ingests (Pre-Labels, Claim-Extract, Dossier-Snippets).
---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L41-L52
merged_at: 2025-09-09T13:55:10.858971Z
---

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
---
merged_from:
  - docs/dev/v0.2/FlowiseAI-Agents-integration.md#L100-L116
merged_at: 2025-09-09T13:55:10.860708Z
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
---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L142-L143
merged_at: 2025-09-09T14:17:02.137607Z
---

### `docs/nodes/flowise_n8n.md`
```markdown
---
merged_from:
  - docs/blueprints/FLOWISE-AGENTS-BLUEPRINT.md#L190-L191
merged_at: 2025-09-09T14:17:02.139466Z
---

```markdown
# NiFi Processor – InvokeFlowiseAgent
---
merged_from:
  - docs/export/AFFINE.md#L1-L2
merged_at: 2025-09-10T07:11:58.672158Z
---

### `docs/export/AFFINE.md`
```markdown
---
merged_from:
  - docs/export/AFFINE.md#L105-L106
merged_at: 2025-09-10T07:12:12.917045Z
---

### `docs/export/BUNDLE-SPEC.md`
```markdown
---
merged_from:
  - docs/waveterm/README.md#L8-L10
merged_at: 2025-09-10T07:23:57.733735Z
---

### `docs/waveterm/README.md`

```markdown
---
merged_from:
  - docs/waveterm/README.md#L229-L231
merged_at: 2025-09-10T07:23:57.739153Z
---

````markdown
# Job API (WaveTerm ↔ InfoTerminal)

---
merged_from:
  - docs/waveterm/README.md#L335-L337
merged_at: 2025-09-10T07:23:57.743479Z
---


## Zweck
Kommandos in WaveTerm-Workspaces aus n8n orchestrieren (Ingest → Analyse → Export).
---
merged_from:
  - docs/waveterm/README.md#L366-L367
merged_at: 2025-09-10T07:23:57.747077Z
---

- `Command` (string template)
- `Timeout Ms` (int, default 60000)
---
merged_from:
  - docs/export/APPFLOWY.md#L2-L4
merged_at: 2025-09-10T07:23:57.765584Z
---

### `docs/export/APPFLOWY.md`

```markdown
---
merged_from:
  - docs/waveterm/README.md#L331-L333
merged_at: 2025-09-10T07:24:02.254339Z
---

### `docs/n8n/waveterm_run.md`

````markdown
---
merged_from:
  - docs/waveterm/README.md#L360-L361
merged_at: 2025-09-10T07:24:02.258358Z
---

# NiFi Processor: WaveTermInvoker

