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
