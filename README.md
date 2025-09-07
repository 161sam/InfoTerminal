# InfoTerminal

> **Open-Source-Plattform für Datenintegration, Suche, Graph-Analyse und Dokumentenmanagement**

[![Status](https://img.shields.io/badge/status-v0.1.0--pre-blue)](#) [![License](https://img.shields.io/badge/license-Apache--2.0-green)](#)

---

## 🚀 Was ist InfoTerminal?

Mit InfoTerminal kannst du große Datenmengen **durchsuchen, analysieren und visualisieren**.  
Die Plattform kombiniert Volltextsuche, Graph-Analyse und Dokumentenmanagement – mit einer modernen Web-Oberfläche.

**Du bekommst:**
- 🔍 **Suche** in Text- und Metadaten  
- 🕸️ **Graph-Analyse** von Personen, Organisationen, Ereignissen  
- 📄 **Dokumenten-Upload** mit automatischer Entitätserkennung (NER)  
- 📊 **Dashboards** und Visualisierungen für schnelle Einsichten  
- 🤖 **KI-Unterstützung** (Texterkennung, Zusammenfassungen, Embeddings)

---

## 🖥️ Installation & Start

### 1. Docker Compose (empfohlen)

```bash
cp .env.example .env
docker compose build
docker compose up -d
````

Danach:
👉 [http://localhost:3411](http://localhost:3411)

---

### 2. Helm Chart (für Kubernetes)

```bash
helm upgrade --install infoterm charts/infoterminal -n infoterm --create-namespace
kubectl port-forward svc/infoterminal-web 3411:3411 -n infoterm
```

👉 [http://localhost:3411](http://localhost:3411)

---

### 3. CLI (optional)

Installiere die CLI separat per `pipx`:

```bash
cd cli/ && pipx install infoterminal-cli
```

Die wichtigsten Kommandos:

```bash
it start    # Services hochfahren
it stop     # Services stoppen
it restart  # Neustart via docker compose restart
it rm       # Umgebung entfernen (down --remove-orphans)
it status   # Status der Container
it logs -s SERVICE --lines 50
```

`-n/--dry-run` zeigt nur die ausgeführten `docker compose` Kommandos an.

---

### NPM Workspaces

Workspaces: im Repo-Root `npm i`, dann `npm -w apps/frontend test` oder `npm -w apps/frontend run build`.

---

## ⚙️ Konfiguration

Die wichtigsten Einstellungen findest du in der Datei **`.env`**:

* **Frontend:** läuft standardmäßig auf Port `3411`
* **Monitoring:** Prometheus/Grafana unter `3412–3416`
* **Zugangsdaten:** Standardwerte hier ändern
* **Optionen:** Telemetrie (`IT_OTEL`), Metriken (`IT_ENABLE_METRICS`)

Beispiel `.env`:

```ini
IT_ENABLE_METRICS=1
IT_OTEL=0
NEO4J_PASSWORD=test12345
```

---

## 🌐 Nutzung

### 🔍 Suche

Unter [http://localhost:3411/search](http://localhost:3411/search) kannst du Daten durchsuchen und filtern.
![Search UI](docs/dev/img/search-ui.png)

---

### 🕸️ Graph

Interaktive Netzwerke von Personen, Organisationen und Ereignissen.
![Graph UI](docs/screenshots/04-graph.svg)

---

### 📄 Dokumente

Unter [http://localhost:3411/documents](http://localhost:3411/documents) kannst du Dateien per **Drag & Drop** hochladen.

* Entitäten werden automatisch hervorgehoben
* Fortschrittsanzeige beim Upload
* Detailansicht mit Kontext

![Upload Progress](docs/dev/img/upload-progress.png)

---

### 📊 Dashboards

Unter [http://localhost:3413](http://localhost:3413) (Login: `admin/admin`) findest du vorgefertigte Dashboards zu:

* API-Status
* Suchanfragen & Reranking
* Dokumenten-Annotationen

---

## 📈 Monitoring & Status

![Health Badge](docs/img/health-badge.svg)

* **Prometheus:** [http://localhost:3412](http://localhost:3412)
* **Grafana:** [http://localhost:3413](http://localhost:3413)

ℹ️ **Hinweis:** Wird das Badge oben **rot**, prüfe die Logs:

```bash
docker compose logs -f
```

---

## 🎯 Typische Einsatzszenarien

* **Ermittlungen & Sicherheit:** Verbindungen in Telefonlisten, Finanzdaten, Ermittlungsakten aufdecken
* **Compliance & Risiko:** Automatisierte Red-Flag-Analysen von Jahresberichten, Sanktionslisten
* **Journalismus & OSINT:** Große Datenleaks strukturieren und Netzwerke sichtbar machen
* **Unternehmen:** Lieferketten überwachen und Risiken früh erkennen
* **Forschung:** Netzwerke aus Interviews, Publikationen oder Open Data untersuchen

---

## 🧠 KI-Funktionen (Beispiele)

```bash
# Entitäten extrahieren
curl -X POST http://localhost:8003/ner -H "Content-Type: application/json" \
  -d '{"text":"Barack Obama was born in Hawaii."}'

# Zusammenfassen
curl -X POST http://localhost:8003/summarize -H "Content-Type: application/json" \
  -d '{"text":"..."}'
```

---

## 📚 Weiterführend

* 📄 [Doku & Handbücher](docs/)
* 🗺️ [Roadmap](#-roadmap)
* 🤝 [Beitragen](CONTRIBUTING.md)
* 📄 [Lizenz (Apache 2.0)](LICENSE)

---

## 💬 Kontakt

* Fragen & Feedback: bitte ein [Issue im Repo](../../issues) eröffnen
* Community-Chat: siehe `docs/community.md`

---

## ✨ Warum InfoTerminal?

* **Open Source & modular** – volle Kontrolle, keine Abhängigkeit
* **Benutzerfreundlich** – intuitive Web-Oberfläche
* **Erweiterbar** – neue Datenquellen, KI-Module und Dashboards einfach integrierbar
* **Sicher** – Rollen, Richtlinien, Audit & Governance

> Ziel: **Ein praktisches, erschwingliches & anpassbares Framework**, das Datenanalyse und Investigations beschleunigt – mit voller Transparenz.

---
