# InfoTerminal

[![CI](https://github.com/161sam/InfoTerminal/actions/workflows/ci.yml/badge.svg)](https://github.com/161sam/InfoTerminal/actions/workflows/ci.yml)
[![CodeQL](https://github.com/161sam/InfoTerminal/actions/workflows/codeql.yml/badge.svg)](https://github.com/161sam/InfoTerminal/actions/workflows/codeql.yml)

> **Open-Source Intelligence Plattform – modular, sicher, erweiterbar.**
> Ziel: Mehr können als Palantir Gotham – mit offenen Technologien, AI/ML und Ethical Design.

[![Status](https://img.shields.io/badge/status-v0.2--dev-blue)](#)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](#)
[![K8s](https://img.shields.io/badge/kubernetes-ready-326ce5)](#)
[![Python](https://img.shields.io/badge/python-3.10%2B-yellow)](#)

---

## 🎯 Mission

**InfoTerminal** ist eine modulare OSINT/Intelligence-Plattform, die Nutzer:innen befähigt:

- Daten aus **News, Social Media, Open Data, Feeds, Sensoren** sicher und anonym zu sammeln
- **Graph-Analysen, NLP und Verifikations-Algorithmen** darauf anzuwenden
- Erkenntnisse in **Dossiers, Dashboards und Kollaborations-Workflows** bereitzustellen
- Vollständig mit **Security-Layer** (Incognito, Tor/VPN, Sandbox) und **Verification-Layer** (AI-Fact-Checking).

---

## ⚙️ InfoTerminal CLI

Die **`infoterminal-cli`** (Typer-basiert, via `pipx` installierbar) ist der zentrale Zugang:

```bash
# Installation
pipx install infoterminal-cli

# Basisbefehle
it up          # Infrastruktur + Services starten
it down        # Stoppen
it status      # Status-Übersicht
it logs        # Logs einsehen
it export      # Daten/Dossiers exportieren
it plugin run  # Plugins/Kali-Tools nutzen
it login       # OIDC/OAuth2 Login
```

Die CLI bietet:

- **Infra-Management:** Docker Compose + lokale Services
- **Abfragen:** Search, Graph, Views direkt aus dem Terminal
- **Exports:** GraphML, JSON, CSV, Dossier-Reports
- **Plugin-Runner:** Integration externer Tools (z. B. Kali Linux, nmap, exiftool)
- **Presets:** Profilbasierte Startkonfigurationen (`--preset journalism`, `--preset compliance`)

---

## 🔄 Flows & Pipelines

### 1. **Ingest (NiFi)**

- **RSS/API/File Watchers**: News, Dokumente, PDFs (OCR)
- **Social/Web Scraper**: Telegram, Reddit, Mastodon, Blogs
- **Streaming/Kafka**: Sensoren, CDR, Echtzeitfeeds
- **Video-Pipeline**: NiFi → FFmpeg → ML (Face/Object Detection)
- **Geospatial Enrichment**: Geocoding (OSM/Nominatim)

### 2. **Processing & Storage**

- **search-api (OpenSearch)**: Volltext, Embeddings, Ranking
- **graph-api (Neo4j)**: Entitäten, Relationen, Algorithmen
- **graph-views (Postgres)**: SQL-Views für BI (Superset, Grafana)
- **nlp-verif (FastAPI)**: NER, Relation Extraction, Summarization, RTE

### 3. **Verification-Layer**

- **Claim Extraction & Clustering**
- **Evidence Retrieval** (BM25 + Dense Rerank)
- **RTE/Stance Classification** (AI-Entailment)
- **Geo/Temporal Checks** (Mordecai, Heuristik)
- **Media Forensics** (pHash, EXIF, ELA, Reverse Search)
- **Veracity Score** + Active Learning + Review-UI

### 4. **Security-Layer**

- **Egress-Gateway** (Tor/VPN/Proxy, Kill-Switch, DNS-Sinkhole)
- **Ephemeral Filesystem** (Incognito Mode, Auto-Wipe)
- **Vault-Integration** (Secrets, Keys, WORM-Buckets)
- **Remote Browser Pool** (Fingerprints, Identity Profiles)
- **Plugin Sandbox** (gVisor/Kata/OPA Validation)

### 5. **Frontend**

- **/search**: Facetten, Ranking, Badges
- **/graphx**: Graph + Geo-Visualisierung, Algorithmen
- **/settings**: Endpoints, OAuth2/OIDC Config
- **Dossier-Builder**: PDF/MD-Reports, Vorlagen
- **Collaboration**: Shared Notes, CRDT, Audit-Logs

### 6. **Outputs**

- **Dossiers**: Templates für Legal, Disinfo, Financial, Crisis, Climate …
- **Dashboards**: Superset (BI, Cross-Filter), Grafana (Logs/Metrics)
- **Presets**: Profile (Journalism, Agency, Research, Climate Researcher, Compliance Officer, Crisis Analyst, Disinfo Watchdog, Economic Analyst)

---

## 🧩 Module & Blueprints

- **Security-Blueprint** (Incognito, Vault, Sandbox, Logging)
- **Verification-Blueprint** (AI Fact-Checking, Veracity Layer)
- **Intelligence Packs (Beyond Gotham):**
  - v0.3 → Legal, Disinformation, Supply-Chain
  - v0.5 → Financial, Geopolitical, Humanitarian
  - v1.0 → Climate, Technology, Terrorism, Health, AI-Ethics, Media-Forensics, Economic, Cultural

---

## 🛠️ Einsatzszenarien

- **Journalismus:** Fake-News erkennen, Narrative-Cluster analysieren, Beweisketten nachvollziehen
- **Behörden & Firmen:** Compliance-Verstöße prüfen, Sanktionen überwachen, Lieferketten simulieren
- **Forschung/NGOs:** Humanitäre Krisen erkennen, Klimarisiken simulieren, Datenquellen fusionieren
- **Sicherheitsanalyse:** Terrornetzwerke, Propaganda, Finanzströme sichtbar machen
- **Ethik & Governance:** Bias in KI erkennen, Transparenz in Modellen durchsetzen

---

## ❓ Q\&A

### Warum InfoTerminal?

Weil es eine **offene, erweiterbare Alternative zu Palantir Gotham** bietet – für Journalist\:innen, Behörden, NGOs und Forschende.

### Wofür ist es gedacht?

- **Datenintegration & Analyse** aus heterogenen Quellen
- **Graph Intelligence** (Beziehungen, Netzwerke, Communities)
- **Verifikation & Fact-Checking** in Echtzeit
- **Simulation & Vorhersagen** (Supply Chains, Geopolitik, Klima)

### Für wen?

- Journalist\:innen (Recherche, Fake-News Erkennung)
- Behörden & Sicherheitsorgane (Compliance, Risiko, Forensics)
- Forschung & NGOs (Krisen, Klima, Humanitär)
- Think Tanks & Unternehmen (Wirtschaft, Supply Chains, Märkte)

### Was kann InfoTerminal?

- Datenquellen anbinden (APIs, RSS, Social, Sensoren)
- NLP, Graph-Analysen, AI-Verifikation
- Incognito/Forensics-Modus für sichere Recherchen
- Reports/Dossiers automatisch generieren
- Presets & Playbooks für typische Nutzergruppen

### Was kann es (noch) nicht?

- Keine Echtzeit-Massenüberwachung (rechtlich & ethisch ausgeschlossen)
- Keine closed-source Abhängigkeit – Fokus auf Open-Source
- Kein Ersatz für menschliche Bewertung → Human-in-the-Loop bleibt Pflicht
- Kein Data-Lake für beliebige Rohdaten (fokus auf kuratierten Ingest)

### Was unterscheidet InfoTerminal von Gotham?

- **Open Source, modular, föderiert**
- **Ethical AI Toolkit** (Bias Checks, Transparenz)
- **Beyond Gotham Packs** (Climate, Cultural, Media-Forensics …)
- **Plugin-Architektur** (Kali Tools, OSINT Scripts, APIs, SDKs)
- **Sustainability** (Green Hosting, effiziente ML Pipelines)

### Weitere Fragen

- **Wie starte ich?** → siehe Quickstart unten
- **Wie erweitere ich?** → eigene NiFi/n8n Flows, Plugins via YAML/SDK
- **Wie exportiere ich Ergebnisse?** → CLI `it export` oder Dossier-Builder

---

## 👩‍💻 Quickstart (Dev)

```bash
# 1. Infrastruktur starten (OpenSearch, Neo4j, Postgres, Prometheus, Grafana, ...)
docker compose --profile infra up -d

# 2. Lokale Services starten
./scripts/dev_up.sh

# 3. Frontend öffnen
http://localhost:3411
```

---

## 📜 License

Apache 2.0 – frei nutzbar, erweiterbar, beitragbar.

---

## 🤝 Contributing

Pull Requests willkommen.
Bitte beachte: kleine, deterministische PRs mit Tests & Docs.
