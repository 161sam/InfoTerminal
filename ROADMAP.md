# 🌍 Erweiterte Roadmap InfoTerminal

## Phase 2 Execution Order (2025)

| Wave | Pakete | Fokus | Abhängigkeiten |
| --- | --- | --- | --- |
| Wave 1 (aktiv) | **A – Ontologie & Graph**, **F – Dossier & Collaboration** | Graph-Analysen (Degree, Louvain, Shortest Path) + Dossier-Lite Export (MD/PDF) und Shared Notes MVP. | Dossier-Export hängt vom neuen Subgraph-Hook des Graph-APIs ab. |
| Wave 2 | **B – NLP & Resolver**, **C – Geospatial** | Relationsextraktion, Entity-Linking, Geo-Layer mit Bounding-Box-API. | Nutzt Graph-Metriken & Dossier-Hooks aus Wave 1. |
| Wave 3 | **G – Plugins**, **D – Daten-Ingest & Workflows** | Plugin-Runner (inkl. nmap) + NiFi/n8n Automatisierung. | Baut auf Observability und Export-Flows von Wave 1–2 auf. |
| Wave 4 | **H – Agenten**, **I – Feeds** | Flowise-Agenten orchestrieren Plugins & NLP, externe Feeds mit Monitoring. | Benötigt stabile Plugins/Ingest. |
| Wave 5 | **J – Performance & Infra**, **K – Frontend & UX** | Health/Ready/Metrics komplettieren, OIDC/UX-Härtung. | Startet nach stabilen Funktionspaketen. |
| Wave 6 | **L – Docs & Tests**, **Hardening**, **Release** | Dokumentation angleichen, Security-Gates, Release-Playbook. | Finalisierung nach Feature-Waves. |

Alle Artefakte (Dashboards, Checklisten, Scripts) sind idempotent – wiederholte Ausführung aktualisiert bestehende Objekte statt Duplikate zu erzeugen.

## 1. Pflicht-Fokus (Gotham-Features + deine Must-Haves)

### 1.1 Ontologie & Graph (Wave 1)

* Graph-Datenmodell mit **Entities, Events, Relations**.
* **Graph-Algorithmen** (MVP): Degree-Centrality, Louvain-Communities, Shortest-Path mit Timeout & Pagination.
* **Superset-Dashboard** `graph_analytics_mvp` + Grafana-Panel `graph-analytics-mvp` für Queries, Dauer, Exporte.
* Subgraph-Export (`/graphs/analysis/subgraph-export`) liefert JSON/Markdown für das Dossier.
* Cross-Links: Search ↔ Graph ↔ Dossier (Smoke-E2E `graph-dossier`).

### 1.2 NLP & AI-Layer

* **NLP v1**: NER, Relation Extraction, Summarization.
* **AI/ML/DL v2** (fokussiert):

  * **Graph Neural Networks (GNNs)** für Community Detection, Link Prediction.
  * **Deep Learning Embeddings** (BERT/LLM) für Entity Linking & Cross-Doc-Korrelation.
  * **Active Learning**: Feedback-Loop User ↔ Model (wie Gotham Video).
  * Optional: **Federated Learning** für Datenschutz.

### 1.3 Geospatial-Layer

* Integration **Leaflet/MapLibre** im Frontend.
* Datenquellen: GeoJSON, OSM, Satellitendaten.
* **Geo-Queries**: Entities mit Location/Movement; Heatmaps; Movement Prediction.
* **NiFi Pipeline** für Geodaten-Ingest.

### 1.4 Data Ingest (NiFi & n8n)

* **NiFi**:

  * File Ingest (CSV, JSON, PDF→OCR).
  * API Ingest (REST/Kafka).
  * Streaming (CDR-like, Sensoren).
* **n8n**:

  * Automatisierte Investigations-Flows.
  * Orchestration zwischen NLP, Graph, Geospatial.
  * Option für **Multi-Agent-Playbooks** (Flowise Integration).

### 1.5 Video-Pipeline

* **NiFi → FFmpeg → ML**: Echtzeit-Streams ingestieren.
* ML-Pipelines: Object Detection, Face/License Recognition (modular).
* Feedback-Loop: User korrigiert Detection → Model verbessert.
* Export von Video-Snapshots mit Metadaten in Graph.

### 1.6 Collaboration & Dossier (Wave 1)

* **Dossier-Lite MVP**: Reports aus Search & Graph; exportierbar PDF/MD per `/dossier/export`.
* **Collaboration**: Feature-Flag Notes/Kommentare pro Fall, Audit-Events in Logs.
* **Metrics**: `dossier_exports_total`, `dossier_export_duration_seconds_bucket`, `collab_notes_total`.
* **Dashboards**: Superset-Dataset `graph_analytics_mvp` stellt Kontext bereit; Grafana zeigt Dossier-Export-Zähler.

---

## 2. Differenzierungs-Features (besser als Gotham)

* **Offene Plug-in-Architektur**:

  * Jede Komponente (Search, Graph, NLP, Geospatial, Video) erweiterbar via SDK (Python/JS).
  * Marketplace für Community-Plugins.
* **Dezentrale Architektur (DAO-ready)**:

  * Föderierte Deployments (mehrere Orgs, gemeinsame Ontologie).
  * Datenhoheit bei Usern → DSGVO-Plus.
* **Sustainability-Edge**:

  * Green Server Hosting (EcoSphere Network).
  * Ressourceneffizienz in ML-Pipelines (Distillation, Quantisierung).
* **Ethical AI**:

  * Bias-Checks eingebaut.
  * Transparente Model Cards.
* **Superset++ Dashboards**:

  * Cross-Filter, Deep-Links, Embeddings-Visuals.
  * „Investigation Timeline“ Dashboard (Events + Geo + Graph kombiniert).

---

## 3. Kali Linux Tools als universelles Plugin-System

### 3.1 Ziel

Alle **Kali Linux Tools** (z. B. nmap, metasploit, wireshark, hydra, sqlmap, etc.) als **integrierbare Datenquellen & Analyzer** für InfoTerminal.
→ Damit: **Digital Forensics, Cyber Threat Intel, Security Investigations** out-of-the-box.
→ Gotham kann das nicht – InfoTerminal schon.

### 3.2 Architektur

* **Wrapper-Layer**: Jeder Kali-Tool-Call wird in standardisiertes JSON/YAML-Ergebnis übersetzt.
* **Plugin-Interfaces**:

  * **CLI Wrapper** (bash → JSON).
  * **Python Adapter** (subprocess + parser).
  * **n8n Nodes** (z. B. nmap-node, sqlmap-node).
  * **REST API Bridge** (Tool → FastAPI-Service).
* **Sandboxing**: Tools laufen in isolierten Containern (Docker).
* **Registry**: JSON/YAML-Definition pro Tool → Doku, Inputs, Outputs.

### 3.3 Beispiel-Flow

1. User wählt in InfoTerminal „Run nmap on target 192.168.0.1“.
2. Plugin-Wrapper führt `nmap` aus, Ergebnis → JSON.
3. Ergebnis wird:

   * im Graph als Nodes/Edges gespeichert (Ports/Services).
   * in Search indexiert (Text + Metadata).
   * in Dossier eingebunden (Report).
4. n8n orchestriert Kette: nmap → whois → shodan → graph correlation.

---

# 🎯 Big Picture (USP gegenüber Gotham)

* **Alles, was Gotham kann** (Ontologie, Graph, Geo, Video, Dossiers, Collaboration).
* **+ Security & Forensics Layer (Kali-Tools)** → einzigartig.
* **+ Nachhaltigkeit/Dezentralität** → zukunftssicher.
* **+ Vollständige Open-Source/Plugin-Architektur** → Community-getrieben, skalierbar.

---
