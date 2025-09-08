# 📘 InfoTerminal – Benutzerhandbuch

## 1. Einführung

- Ziel und Vision von InfoTerminal
- Inspiration (Palantir Gotham, aber Open Source)
- Haupt-Features und Differenzierungsmerkmale

## 2. Installation & Setup

- Systemvoraussetzungen
- Schnellstart (dev_up.sh, patch_ports.sh, dev_install.sh)
- Zwei Betriebsmodi:
  - **A)** Lokale App-Prozesse (dev)
  - **B)** Voll Dockerisierte Umgebung

- Ports & Konfiguration (`.env.dev.ports`, `.env.local`, Helm)
- Troubleshooting

## 3. Erste Schritte

- Start der Plattform
- Login/Authentifizierung (OAuth2/OIDC)
- Überblick über die Oberfläche (Frontend: `/search`, `/graphx`, `/settings`)
- CLI-Quickstart (`infoterminal-cli` via pipx)

## 4. Kernfunktionen

- 🔎 **Suche** (search-api, Embeddings, NLP v1)
- 🌐 **Graph** (graph-api, Neo4j, Graph-Views/Postgres)
- 📊 **Dashboards** (Superset: BI, Cross-Filter, Deep-Links; Grafana für Logs/Traces)
- 📂 **Dokumentenmanagement** (Aleph + NiFi ingest, OCR, NER, Fingerprinting)
- 🤖 **NLP Services** (NER, Relation Extraction, Summarization, Reranking)
- 🧩 **Agents & Playbooks** (Flowise, n8n, Investigation Assistant, Financial Risk Assistant)
- 🗺️ **Geospatial-Layer** (OSM, GeoJSON, Leaflet/MapLibre)
- 🎥 **Video-Pipeline** (NiFi → FFmpeg → ML, Object/Face Detection)
- 👥 **Collaboration** (Shared Notes, Multi-User, Audit Logs)

## 5. Erweiterte Funktionen

- Sicherheit & Anonymität (Egress-Gateway, Vault, Sandbox, OPA)
- Verifikations-Layer (Fact-Checking, Veracity Badges, Evidence Panel)
- AI/ML/DL-Erweiterungen (Graph Neural Networks, Federated Learning)
- Plugin-Architektur (Python/JS/CLI SDKs, Kali Linux Tools Integration)

## 6. Observability & Monitoring

- Observability Profile (`docker compose --profile observability`)
- Prometheus, Grafana, Alertmanager, Loki, Tempo (Ports 3412–3416)
- Logs, Metriken & Traces (`/metrics`, IT_ENABLE_METRICS, IT_OTEL)

## 7. CLI-Handbuch

- Installation (`pipx install infoterminal-cli`)
- Befehle: start, stop, restart, rm, status, logs
- Unterbefehle: search.query, graph.ping, graph.cypher, views.query, analytics.kpis, settings.show, ui.run
- Ausgabeformate: Tabelle, JSON, YAML, Text

## 8. Integrationen & Erweiterbarkeit

- NiFi Pipelines (Ingest, Normalisierung, Claim Extraction)
- n8n Playbooks (Investigations, Veracity Alerts, Auto-Dossiers)
- Flowise Agents (Investigation Assistant, Risk Assistant)
- Export zu AppFlowy/AFFiNE (Dossiers, Graphen, Reports)
- WaveTerm-Kompatibilität

## 9. Sicherheit & Compliance

- Zugriffskontrolle (OAuth2/OIDC, RLS, OPA)
- Audit Logs & Nachvollziehbarkeit
- Ethical AI (Bias-Checks, Model Cards)
- Nachhaltigkeit (Green Server Hosting, effiziente ML)

## 10. Anwendungsfälle

- Investigations & Fact-Checking
- Finanz- & Risikoanalyse
- Journalismus & OSINT
- Verwaltung & Behörden
- Unternehmensdaten & Compliance

## 11. Tipps & Best Practices

- Optimale Nutzung von CLI + Frontend
- Troubleshooting Guide (Neo4j, Ports, Auth-Probleme)
- Monitoring & Debugging

## 12. Roadmap & Weiterentwicklung

- Versionierung (v0.1.9.1 → v0.1.9.9 → v0.2 → v1.0)
- Geplante Features bis v1.0
- Langfristige Vision (DAO-ready, föderierte Deployments, Plugin-Marktplatz)

## 13. Anhang

- Port-Tabelle
- Env-Variablen Übersicht
- Glossar (NLP, Graph, Observability etc.)
- Lizenz & Contributing
