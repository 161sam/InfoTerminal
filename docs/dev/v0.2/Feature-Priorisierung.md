# 📊 Feature-Priorisierung InfoTerminal (ab v0.2)

| Feature/Erweiterung                                                        | Impact 🚀              | Aufwand ⚙️  | Prio ⭐              |
| -------------------------------------------------------------------------- | ---------------------- | ----------- | ------------------- |
| **Ontologie-Layer** (Entities/Relations/Events)                            | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **Graph-Algorithmen v1** (Centrality, Communities, Pathfinding)            | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **NLP v1** (NER, Relation Extraction, Summarization)                       | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **OAuth2/OIDC Auth**                                                       | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **Observability Profile** (Prometheus, Grafana, Loki, Tempo, Alertmanager) | Hoch                   | Niedrig     | ⭐⭐⭐ High            |
| **Dossier-Lite v1** (Reports/Export PDF)                                   | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **Geospatial-Layer** (Leaflet/MapLibre, Movement Queries)                  | Hoch                   | Mittel-Hoch | ⭐⭐⭐ High            |
| **NiFi Pipelines** (File, API, Streaming ingest)                           | Hoch                   | Hoch        | ⭐⭐⭐ High            |
| **n8n Playbooks** (Investigations)                                         | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **Collaboration v1** (Notes, CRDT, Shared Boards)                          | Hoch                   | Mittel-Hoch | ⭐⭐ Mid              |
| **Video-Pipeline** (NiFi→FFmpeg→ML, Object/Face Detection)                 | Mittel-Hoch            | Hoch        | ⭐⭐ Mid              |
| **Plugin-Architektur (Kali Tools etc.)**                                   | Sehr hoch              | Hoch        | ⭐⭐⭐ High            |
| **External Live-Data Sources** (News, Social, Feeds, Web)                  | Sehr hoch              | Hoch        | ⭐⭐⭐ High            |
| **Graph ML** (Link Prediction, GNNs, Embeddings)                           | Sehr hoch              | Hoch        | ⭐⭐ Mid              |
| **Event Extraction / Timeline**                                            | Hoch                   | Hoch        | ⭐⭐ Mid              |
| **Cross-Lingual NLP**                                                      | Mittel                 | Mittel      | ⭐ Mid               |
| **Active Learning (Human-in-the-Loop)**                                    | Mittel-Hoch            | Mittel      | ⭐⭐ Mid              |
| **Federated Learning**                                                     | Hoch (Differenzierung) | Sehr hoch   | ⭐ Low               |
| **Explainable AI (XAI)**                                                   | Mittel                 | Mittel      | ⭐ Mid               |
| **Investigation Agents** (Flowise + n8n)                                   | Sehr hoch              | Mittel      | ⭐⭐⭐ High            |
| **Cyber Threat Feeds** (MISP, OTX, Shodan)                                 | Hoch                   | Mittel      | ⭐⭐⭐ High            |
| **Kali Wrappers (nmap, theHarvester, sqlmap)**                             | Sehr hoch              | Mittel      | ⭐⭐⭐ High            |
| **3D Visualization (Deck.gl, Cesium)**                                     | Mittel                 | Hoch        | ⭐ Low               |
| **Darknet/OSINT Sources**                                                  | Mittel-Hoch            | Hoch        | ⭐⭐ Mid              |
| **Forensics Mode (Chain-of-Custody)**                                      | Hoch                   | Mittel-Hoch | ⭐⭐ Mid              |
| **Decentralized Deployments (DAO-ready)**                                  | Sehr hoch              | Sehr hoch   | ⭐ Low (Strategisch) |
| **Ethical AI Toolkit (Bias, Model Cards)**                                 | Hoch                   | Mittel      | ⭐⭐ Mid              |
| **Investigation Timeline Dashboard**                                       | Sehr hoch              | Mittel      | ⭐⭐⭐ High            |

---

## 📌 Zusammenfassung Priorisierung

### **High Prio (direkt nach v0.2)**

* Plugin-Architektur (Kali Integration)
* External Live Data Sources (News, Social, Web)
* Investigation Agents (Flowise+n8n)
* Cyber Threat Feeds
* Investigation Timeline Dashboard

### **Mid Prio (0.3–0.5)**

* Collaboration Features
* Video Pipeline (PoC → Stabilisierung)
* Graph ML (Embeddings, Prediction)
* Active Learning
* Event Extraction + Timeline
* Darknet/OSINT Quellen
* Ethical AI Toolkit

### **Low Prio (strategisch/later)**

* Federated Learning
* 3D Visualization
* Decentralized DAO Deployments
* Forensics Mode

---
