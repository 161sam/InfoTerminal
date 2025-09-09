# 🚀 Detaillierter Entwicklungsplan InfoTerminal

## 🟢 Phase 1 – Gotham Gap Closing (v0.2)

**Ziel:** Alle Kernfunktionen entwickeln, um „Gotham-Parität“ zu erreichen.

### Aufgaben

* **Core APIs & Ontologie**

  * GRAPH-API: Ontologie-Layer (Entities, Relations, Events)
  * SEARCH-API: Index-Policies, NLP v1 (NER, RE, Summarization)
  * VIEWS: Postgres-Views + Superset-Integration
* **Security-Layer (Basic)**

  * Egress-Gateway (Proxy, VPN, Tor)
  * Incognito Mode (Ephemeral FS, Auto-Wipe)
* **Verification-Layer (MVP)**

  * Claim Extraction & Evidence Retrieval
  * RTE/Stance-Klassifizierung
* **Frontend**

  * /search, /graphx, /settings mit konfigurierbaren Endpoints
  * Dossier-Lite (PDF/MD Export)
* **Orchestration**

  * NiFi: RSS/API/File Pipelines
  * n8n: Investigation Playbooks
* **Observability**

  * Prometheus, Grafana, Loki, Tempo
* **CLI**

  * Lifecycle Commands (up/down/status/logs)
  * Erste Exportfunktionen

### Deliverables

* v0.2 Release (Gotham-Gap Closed)
* Docs: Developer Quickstart, User Quickstart
* Diagramme & Roadmap aktualisiert

---

## 🔵 Phase 2 – Intelligence Packs I (v0.3)

**Ziel:** Erste Beyond-Gotham Module (für Journalismus/Compliance/Supply Chains).

### Aufgaben

* **Blueprints umsetzen**

  * Legal-Intelligence (RAG auf Gesetze, Compliance Alerts)
  * Disinformation-Intelligence (Narrativ-Cluster, Bot Detection)
  * Supply-Chain-Intelligence (Graph: Firmen ↔ Lieferungen, Sanktionen)
* **Frontend**

  * Neue Tabs: Legal, Disinfo, Supply
  * Review-UI für Claims/Evidenz
* **Presets**

  * Journalism, Agency, Research
* **Dossier-Templates**

  * Compliance Report, Disinfo Campaign Report, Supply Risk Report
* **Security**

  * Remote Browser Pool (Fingerprint-Minimierung)
  * Vault-Integration (Secrets)
* **Automation**

  * n8n Flows für Alerts & Reports
* **Observability**

  * Erweiterte Metriken (Veracity Score Distribution, Pipeline-Health)

### Deliverables

* v0.3 Release
* 3 neue Blueprints produktiv
* Dossier-Pipeline vollständig nutzbar

---

## 🟡 Phase 3 – Intelligence Packs II (v0.5)

**Ziel:** Vertiefung in Finanz, Geopolitik, Humanitäre Krisen.

### Aufgaben

* **Blueprints**

  * Financial-Intelligence (Red Flags, Leaks, Offshore)
  * Geopolitical-Intelligence (Flug-, Schiffs-, Protestdaten)
  * Humanitarian-Intelligence (Krisen-Indikatoren, ML-Risk Models)
* **Frontend**

  * Geo-Dashboards mit Timeline
  * Risk Heatmaps
* **Presets**

  * Crisis Analyst, Compliance Officer
* **Security**

  * Forensics Mode (Chain-of-Custody, WORM-Buckets)
  * Dual-Plane Logging
* **Verification**

  * Active Learning Loop
  * Bot-Likelihood Engine
* **Integration**

  * Superset Dashboards (Financial/Geo/Humanitarian KPIs)

### Deliverables

* v0.5 Release
* 3 neue Intelligence Packs + Presets
* Simulation-Engine (Supply Chain & Geo)

---

## 🔴 Phase 4 – Full Spectrum Intelligence (v1.0)

**Ziel:** Komplettes Beyond-Gotham Framework, InfoTerminal > Gotham.

### Aufgaben

* **Blueprints**

  * Climate, Technology, Terrorism, Health, AI-Ethics, Media Forensics, Economic, Cultural
* **Multi-Modal Fusion**

  * Text + Geo + Audio/Video + Sensoren
* **Simulation Layer**

  * What-if Scenarios (Gesetze, Märkte, Konflikte)
* **DAO & Governance**

  * Föderierte Deployments
  * Plugin-Store (Kali Tools, SDKs, n8n/JS/Python Integrationen)
* **Frontend**

  * Investigation Timeline (Cross-Filter, Multi-User)
  * Ethical AI Dashboard (Bias, Explainability)
* **Security**

  * Vollständige Plugin-Sandbox (gVisor/Kata/OPA Validation)
  * robots.txt-Enforcer, Policy-Engine
* **Dossiers**

  * Vollständige Report-Bibliothek
* **Sustainability**

  * Green Hosting Guidelines
  * ML-Effizienz Pipelines

### Deliverables

* v1.0 Release (Production Ready)
* Alle Blueprints integriert
* Multi-Domain Intelligence Plattform (Beyond Gotham)
* Public Launch & Whitepaper

---

## 📊 Methoden & Tools

* **Entwicklung:** Python (FastAPI), Node.js (Next.js), TypeScript
* **Datenhaltung:** Neo4j, OpenSearch, Postgres
* **Orchestrierung:** Docker Compose, Helm/K8s
* **ETL/Automatisierung:** NiFi, n8n
* **AI/ML:** HuggingFace, OpenAI/Ollama Integration, Torch/Sklearn
* **Security:** OPA, Vault, gVisor, Tor/VPN
* **Observability:** Prometheus, Grafana, Loki, Tempo, Alertmanager
* **CI/CD:** GitHub Actions, SBOM, Trivy, Cosign

---

## 📅 Zeitliche Struktur (empfohlen)

* **Phase 1 (v0.2):** 2–3 Monate
* **Phase 2 (v0.3):** +3 Monate
* **Phase 3 (v0.5):** +4 Monate
* **Phase 4 (v1.0):** +6 Monate

Gesamt: \~12–16 Monate bis v1.0 (Production Ready)

