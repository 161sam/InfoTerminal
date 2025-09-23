# InfoTerminal

[![CI](https://github.com/161sam/InfoTerminal/actions/workflows/ci.yml/badge.svg)](https://github.com/161sam/InfoTerminal/actions/workflows/ci.yml)
[![CodeQL](https://github.com/161sam/InfoTerminal/actions/workflows/codeql.yml/badge.svg)](https://github.com/161sam/InfoTerminal/actions/workflows/codeql.yml)

> **Open-Source Intelligence Plattform – modular, sicher, erweiterbar.**
> – Beyond Gotham – mit offenen Technologien, AI/ML und Ethical Design.

[![Status](https://img.shields.io/badge/status-phase--2--wave--1-blue)](#)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](#)
[![K8s](https://img.shields.io/badge/kubernetes-ready-326ce5)](#)
[![Python](https://img.shields.io/badge/python-3.10%2B-yellow)](#)

---

## 🧱 Build-Stabilisierung (lokal)

- TypeScript-Audit: `npm run bs:ts-audit`
- Build-Validierung: `npm run bs:validate`
- Final-Check (Produktion): `npm run bs:final`

Details und Reports: `build-stabilization/README.md`

---

## 🎯 Mission

**InfoTerminal** ist eine modulare OSINT/Intelligence-Plattform, die Nutzer:innen befähigt:

- Daten aus **News, Social Media, Open Data, Feeds, Sensoren** sicher und anonym zu sammeln
- **Graph-Analysen, NLP und Verifikations-Algorithmen** darauf anzuwenden
- Erkenntnisse in **Dossiers, Dashboards und Kollaborations-Workflows** bereitzustellen
- Vollständig mit **Security-Layer** (Incognito, Tor/VPN, Sandbox) und **Verification-Layer** (AI-Fact-Checking).

---

## 🚦 Phase 2 – Wave 1 (Pakete A & F)

- **Priorität & Scope:** Graph-Analysen (Degree, Louvain, Shortest Path) und Dossier-Lite Export (Markdown/PDF) plus geteilte Notizen.
- **Artefakte:**
  - Planung & DoD: [`backlog/phase2/ITERATION-01_PLAN.md`](backlog/phase2/ITERATION-01_PLAN.md), [`backlog/phase2/WAVE1_DOD_CHECKLIST.md`](backlog/phase2/WAVE1_DOD_CHECKLIST.md)
  - Sequenz: [`backlog/phase2/PACKAGE_SEQUENCE.yaml`](backlog/phase2/PACKAGE_SEQUENCE.yaml)
  - Superset-Assets: `apps/superset/assets/datasets/graph_analytics_mvp.yaml`, `apps/superset/assets/charts/graph_degree_histogram.json`, `apps/superset/assets/dashboard/graph_analytics_mvp.json`
  - Grafana: `grafana/dashboards/graph-analytics-mvp.json`
- **Observability:** Neue Prometheus-Metriken `graph_analysis_queries_total`, `graph_analysis_duration_seconds_bucket`, `graph_subgraph_exports_total`, `dossier_exports_total`, `collab_notes_total`.
- **Gates:** Inventory/Policy, Health-Ready-Metrics, API/Docs und Smoke-E2E müssen nach jedem Merge grün bleiben (`scripts/generate_inventory.py`, `test_infoterminal_v030_features.sh --suite graph-dossier`).

## 🧪 5-Minuten-Demo (offline, Wave 1–3)

> Ziel: In fünf Minuten den End-to-End-Fluss **Search → Graph-Analyse → Dossier-Export → NLP-Linking → Geo-Overlay** demonstrieren – komplett offline und reproduzierbar.

1. **Services & Seed-Daten starten**
   ```bash
   scripts/dev_up.sh graph dossier
   scripts/fixtures/load_graph_mini.sh
   ```
2. **Degree-Centrality prüfen**
   ```bash
   curl -s "http://localhost:8612/graphs/analysis/degree?limit=10" |
     jq '.results[0:3]'
   ```
3. **Shortest-Path & Subgraph-Export**
   ```bash
   curl -s "http://localhost:8612/graphs/analysis/subgraph-export?center_id=demo-node&format=markdown" \
     -H 'Accept: application/json' > exports/demo-subgraph.json
   jq -r '.markdown' exports/demo-subgraph.json > exports/demo-subgraph.md
   ```
4. **Dossier-Lite (Markdown & PDF)**
   ```bash
   curl -s "http://localhost:8625/dossier/export" \
     -H 'Content-Type: application/json' \
     -d '{"case_id":"demo-case","format":"pdf","source":"graph","template":"brief"}' \
     -o exports/demo-dossier.pdf
   ```
5. **NLP Linking & Resolver anstoßen**
   ```bash
   cat <<'JSON' > tmp/linking-input.json
   {
     "text": "Barack Obama met Donald Trump in Berlin to discuss cooperation with OpenAI.",
     "language": "en",
     "extract_entities": true,
     "extract_relations": true,
     "resolve_entities": true
   }
   JSON

   curl -s -X POST "http://localhost:8613/v1/documents/annotate" \
     -H 'Content-Type: application/json' \
     -d @tmp/linking-input.json > tmp/linking-result.json

   jq '.metadata.linking_status_counts' tmp/linking-result.json
   DOC_ID=$(jq -r '.doc_id' tmp/linking-result.json)
   curl -s -X POST "http://localhost:8613/v1/documents/${DOC_ID}/resolve" -H 'Content-Type: application/json' -d '{}'
   sleep 1
   curl -s "http://localhost:8613/v1/documents/${DOC_ID}" | jq '.entities[] | {text,label,resolution_status,resolution_target,resolution_score}'
   ```
6. **Geo-Overlay & Map Query prüfen**
   ```bash
   curl -s "http://localhost:8612/geo/entities?south=40&west=-75&north=41&east=-73" | jq '.count'
   curl -s "http://localhost:8612/geo/entities?south=52&west=13&east=14&north=53" | jq '.entities[0]'
   ```
7. **Observability & Dashboards kontrollieren**
   - Prometheus: `/metrics` auf `graph-api`, `graph-views`, `collab-hub`, `plugin-runner`, `media-forensics` prüfen (neue Counter/Histograms).
   - Prometheus: `doc_entities_resolver_runs_total`, `doc_entities_resolver_outcomes_total`, `doc_entities_linking_status_total`, `doc_entities_resolver_latency_seconds` beobachten.
   - Prometheus: `graph_geo_queries_total`, `geo_query_count`, `graph_geo_query_errors_total` auf der Graph-API.
   - Prometheus: `plugin_run_total{plugin="nmap"}`, `plugin_run_failures_total{plugin="nmap"}`, `video_frames_processed_total{pipeline="media_forensics"}` prüfen.
   - Grafana: Dashboard **Graph Analytics MVP** (`grafana/dashboards/graph-analytics-mvp.json`).
   - Grafana: Panels **NLP Resolver Outcomes**, **Geo Query Volume**, **Plugin Execution Rate** und **Video Frames Processed Rate** (siehe `monitoring/grafana-dashboards/infoterminal-overview.json`).
   - Superset: Dashboard **Graph Analytics – MVP** (`apps/superset/assets/dashboard/graph_analytics_mvp.json`).
   - Smoke: `scripts/smoke_graph_analysis.sh` verifiziert Degree, Louvain, Shortest Path & Subgraph Export.
8. **Plugin-Runner (nmap → Graph ingest)**
   ```bash
   export PLUGINS_DIR="$(pwd)/plugins"
   export RESULTS_DIR="$(pwd)/tmp/plugin-results"
   export PLUGIN_TEST_MODE=1
   export IT_ENABLE_METRICS=1

   curl -s -X POST "http://localhost:8621/v1/plugins/nmap/execute" \
     -H 'Content-Type: application/json' \
     -d '{"parameters":{"target":"scan.example"},"output_format":"json"}' | jq '.'

   # Wait a moment and fetch the job payload including graph/search artefacts
   curl -s "http://localhost:8621/v1/jobs" | jq '.jobs[0] | {status,graph_entities}'
   cat tmp/plugin-results/graph_ingest/plugin_run_*.json | jq '.graph_entities[0]'
   ```
9. **Video-Pipeline (Frames → Graph ingest)**
   ```bash
   export VIDEO_PIPELINE_ENABLED=1
   export MEDIA_GRAPH_FALLBACK_DIR="$(pwd)/tmp/video-graph"

   VIDEO_FILE=$(python - <<'PY'
import numpy as np
import tempfile
from PIL import Image

frames = []
for i in range(6):
    frame = np.zeros((64, 64, 3), dtype=np.uint8)
    frame[10 + i : 30 + i, 10:30] = 255
    frames.append(Image.fromarray(frame))

tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.gif')
frames[0].save(tmp.name, save_all=True, append_images=frames[1:], duration=120, loop=0)
print(tmp.name)
PY
   )

   curl -s -X POST "http://localhost:8631/v1/videos/analyze" \
     -F "file=@${VIDEO_FILE}" -F frame_interval=1 -F min_area=50 | jq '.summary, .scenes[0]'

   cat tmp/video-graph/video_analysis_*.json | jq '.summary'
   ```

> 💡 **Idempotent:** Wiederholtes Ausführen aktualisiert Exporte/Dashboards und überschreibt Artefakte ohne Duplikate.

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

### Frontend via CLI
```bash
it fe dev     # Next.js dev
it fe build   # Production build
it fe test    # Vitest (dot reporter)
```

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
- **doc-entities (FastAPI)**: NER, Relation Extraction, Summarization (replaces legacy `nlp-service`)

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

## 🕔 5-Minuten-Demo (Offline)

1. **Services starten** – Für den Wave-1-Durchstich reichen Neo4j, Graph-API, Collab-Hub, Superset und Grafana:
   ```bash
   # Basis-Services (Neo4j, Graph-API, Collab-Hub)
   docker compose up -d neo4j graph-api collab-hub

   # Superset (Profil aktivieren)
   docker compose --profile superset up -d superset

   # Grafana + Prometheus aus dem Observability-Stack
   docker compose -f docker-compose.yml -f docker-compose.observability.yml \
     --profile observability up -d grafana prometheus
   ```
2. **Beispielgraph laden** – Seeds importieren (idempotent, überschreibt vorhandene Demo-Daten nicht):
   ```bash
   python examples/py_cypher_demo.py --file examples/seeds/entities.json
   ```
3. **Graph-Analyse triggern** – Degree-Centrality und Louvain Communities abrufen (zeigt auch Metrics-Zähler):
   ```bash
   curl -s "http://localhost:8612/graphs/analysis/degree?limit=10" | jq '.results'
   curl -s "http://localhost:8612/graphs/analysis/communities?limit=5" | jq '.communities'
   ```
4. **Dossier-Hook verwenden** – Subgraph-Export anfordern und als Markdown speichern:
   ```bash
   curl -s "http://localhost:8612/graphs/analysis/subgraph-export?center_id=demo-node&format=markdown" \
     -H 'Accept: application/json' > exports/demo-subgraph.json
   jq -r '.markdown' exports/demo-subgraph.json > exports/demo-subgraph.md
   ```
5. **Dossier-Lite erzeugen** – Export als PDF/MD via Collab-Hub (Feature-Flag aktivieren falls nötig):
   ```bash
   curl -s -X POST "http://localhost:8625/dossier/export" \
     -H 'Content-Type: application/json' \
     -d '{"case_id":"demo","format":"pdf","source":"graph"}' \
     -o exports/demo-dossier.pdf
   ```
6. **Dashboards prüfen** –
   - Grafana → Dashboard „Graph Analytics MVP“: Query-Rate, Dauer p95, Subgraph-Exporte.
   - Superset → Dashboard „graph_analytics_mvp“: Degree-Histogramm, Community-Count.

Die Schritte sind wiederholbar und funktionieren ohne Internet-Zugriff. Alle Exportbefehle sind idempotent – bestehende Artefakte werden überschrieben statt dupliziert.

---

## 🧹 Dev Hygiene

**Lint & Format**

```bash
make gv.venv    # einmalig
make lint       # strikt (CI-ähnlich)
make format     # auto-fix, tolerant
```

**Tipps**

- Pre-commit installiert/aktualisiert sich automatisch bei `make lint`. Einmalige manuelle Installation ist nicht nötig.
- Falls `make lint` scheitert: `make format` ausführen und erneut `make lint` starten.

**Helm/Templated YAML**
Prettier überspringt Helm-Templates via `.prettierignore` und Hook-`exclude`. Falls neue Charts/Templates hinzukommen, bitte Pfade in `.prettierignore` ergänzen.

**Lint/Format**

```bash
make gv.venv   # einmalig
make format    # auto-fix (tolerant)
make lint      # strikt
```

**Safe Prettier**
Für schnelle, stabile Formatierung ohne Templating-/Ops-Dateien:
```bash
make fmt.safe      # schreibt nur kuratierte Pfade
make lint.safe     # checkt nur kuratierte Pfade
```

Die kuratierten Pfade liegen in `scripts/prettier_safe.list`. Bei Bedarf erweitern.

---

## 📜 License

Apache 2.0 – frei nutzbar, erweiterbar, beitragbar.

---

## 🤝 Contributing

Pull Requests willkommen.
Bitte beachte: kleine, deterministische PRs mit Tests & Docs.
