# 🌍 Erweiterte Roadmap InfoTerminal

## 1. Pflicht-Fokus (Gotham-Features + deine Must-Haves)

### 1.1 Ontologie & Graph

* Graph-Datenmodell mit **Entities, Events, Relations**.
* **Graph-Algorithmen**: Centrality, Communities, Pathfinding, Clustering.
* **Superset-Dashboards** für Graph-Metriken.
* Cross-Links: Search ↔ Graph ↔ Dossier.

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

### 1.6 Collaboration & Dossier

* **Dossier-Lite v1**: Reports aus Search & Graph; exportierbar PDF/MD.
* **Collaboration**:

  * Shared Notes pro Case.
  * Live-Multi-User Edit (CRDT).
  * Kommentare an Graph-Nodes.
* **Audit**: Immutable Logs (Loki/Tempo).

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
