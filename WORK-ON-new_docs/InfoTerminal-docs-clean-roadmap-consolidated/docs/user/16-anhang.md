# 16. Anhang

---

## 16.1 Port-Tabelle

InfoTerminal verwendet **keine Standard-Ports**, um Konflikte zu vermeiden.
Alle Ports werden über `.env.dev.ports` und `scripts/patch_ports.sh` konsistent gesetzt.

| Service                | Port |
| ---------------------- | ---- |
| **Frontend** (Next.js) | 3411 |
| **Search API**         | 8401 |
| **Graph API**          | 8402 |
| **Graph Views**        | 8403 |
| **Gateway**            | 8610 |
| **Flowise Connector**  | 3417 |
| **Prometheus**         | 3412 |
| **Grafana**            | 3416 |
| **Alertmanager**       | 3414 |
| **Loki**               | 3415 |
| **Tempo**              | 3416 |

👉 Bei Änderungen: immer `scripts/patch_ports.sh` ausführen.

---

## 16.2 Umgebungsvariablen

Wichtige Variablen in `.env.local` / `.env.dev.ports`:

```env
# Ports
FRONTEND_PORT=3411
SEARCH_API_PORT=8401
GRAPH_API_PORT=8402
VIEWS_PORT=8403
GATEWAY_PORT=8610
FLOWISE_CONNECTOR_PORT=3417

# Observability
PROMETHEUS_PORT=3412
GRAFANA_PORT=3416
ALERTMANAGER_PORT=3414
LOKI_PORT=3415
TEMPO_PORT=3416

# Auth / Security
NEO4J_USER=neo4j
NEO4J_PASSWORD=test12345
IT_ENABLE_METRICS=1   # aktiviert Prometheus-Exports
IT_OTEL=1             # aktiviert OpenTelemetry
IT_FORCE_READY=1      # erzwingt Readiness (z. B. für Tests)
```

---

## 16.3 Glossar

- **Aleph** – Open-Source-Tool für Dokumentenmanagement & Investigations
- **AppFlowy / AFFiNE** – Open-Source-Notiz- & Workspace-Apps, angebunden an InfoTerminal
- **Audit Logs** – Protokolle aller Aktionen zur Nachvollziehbarkeit
- **Centrality** – Graph-Algorithmus, der wichtige Knoten identifiziert
- **Cypher** – Abfragesprache für Neo4j
- **DAO** – Dezentrale autonome Organisation; Governance-Modell für Community-Steuerung
- **Embeddings** – Vektordarstellungen von Texten/Bildern für semantische Suche
- **Flowise** – Open-Source-Plattform für LLM-gestützte Agents
- **Graph API** – Schnittstelle von InfoTerminal zur Abfrage von Neo4j-Daten
- **Loki** – Open-Source-Log-Aggregator
- **Neo4j** – Graph-Datenbank für Entitäten & Beziehungen
- **NiFi** – Daten-Ingest & ETL-System (Batch + Stream)
- **n8n** – Automatisierungsplattform für Playbooks & Workflows
- **Observability** – Gesamtheit von Logs, Metriken & Traces zur Systemüberwachung
- **OPA (Open Policy Agent)** – Engine für Zugriffs-Policies
- **OpenSearch** – Suchmaschine für Volltext- und Dokumentensuche
- **Prometheus** – Monitoring-System für Metriken
- **Superset** – Open-Source-BI-Tool für Dashboards
- **Tempo** – Distributed Tracing Backend (Komponente von Grafana Stack)

---

## 16.4 Lizenz

InfoTerminal ist unter der **Apache 2.0 Lizenz** veröffentlicht.

### Rechte

- Freie Nutzung, Änderung und Verbreitung
- Kommerzieller Einsatz erlaubt

### Pflichten

- Lizenzhinweis und Copyright müssen erhalten bleiben
- Keine Haftung oder Gewährleistung durch die Autoren

👉 Proprietäre Erweiterungen oder Enterprise-Module sind möglich, solange der Open-Source-Kern unverändert unter Apache 2.0 bleibt.

---

## 16.5 Contributing

Beiträge aus der Community sind willkommen!

- Issues & Feature Requests über GitHub
- Pull Requests mit Tests & Dokumentation
- Coding Guidelines:
  - Python (PEP8, Black, Ruff)
  - JavaScript/TypeScript (ESLint 9, Prettier)
  - Commits nach _Conventional Commits_

---
