

> **Legacy Notice (v0.1)**  
> This document describes pre-v0.2 behavior and is kept for historical reference.  
> See the updated docs in `docs/` and the v0.2 roadmap for current guidance.

# 🤖 AGENTS.md – InfoTerminal

Dieses Dokument beschreibt, wie autonome Entwickler-Agenten (z. B. Codex, Claude, OpenHands) im Projekt InfoTerminal eingesetzt werden.  
Ziel: Koordinierte Arbeit an Modulen, schrittweise Fertigstellung bis **Release v0.1.0**.

---

## 🎯 Ziel
InfoTerminal ist ein Open-Source-Framework für Datenintegration, Suche, Graphanalyse, Dokumentenmanagement und KI.  
Release **v0.1.0** soll einen vollständigen MVP enthalten, der Datenfluss **(PDF → OCR → Suche/Graph → Dashboard)** demonstriert.

---

## 🧩 Agentenrollen

### 1. **Architect Agent**
- Aufgabe: Analyse, Architekturentscheidungen, technische Konzepte.
- Outputs: `docs/architecture/*`, Diagramme, ADRs.
- Checkliste:
  - [ ] Architektur konsistent halten (Services, APIs, DBs).
  - [ ] Abhängigkeiten prüfen (Python, Node, Docker).
  - [ ] Security-Policies vorbereiten (Keycloak, OPA).

### 2. **Builder Agent**
- Aufgabe: Implementierung von Services, APIs, Pipelines.
- Arbeitsbereiche: `services/*`, `etl/*`, `web/*`.
- Checkliste:
  - [ ] Microservices implementieren (search-api, graph-api, nlp-service, doc-entities).
  - [ ] Frontend (Suche, Graph-Viewer, Dokumentenanzeige).
  - [ ] ETL-Pipelines (NiFi, Airflow, dbt).

### 3. **Ops Agent**
- Aufgabe: Deployment & Betrieb.
- Arbeitsbereiche: `deploy/*`, `docker-compose.yml`, `charts/`.
- Checkliste:
  - [ ] Dockerfiles für alle Services.
  - [ ] Compose-Bundle lauffähig machen (`make dev-up`).
  - [ ] Helm Chart vorbereiten (minimal).
  - [ ] systemd-Units für native Installation (Kali/Debian).
  - [ ] Observability (Prometheus, Grafana, Logs).

### 4. **QA Agent**
- Aufgabe: Tests, Qualitätssicherung, Docs.
- Arbeitsbereiche: `tests/*`, `docs/*`, `README.md`.
- Checkliste:
  - [ ] Unit-Tests pro Service (Health, Endpunkte).
  - [ ] E2E-Test: PDF → OCR → NER → Suche/Graph.
  - [ ] CI-Konfiguration (Lint, Test).
  - [ ] Screenshots & Quickstart-Anleitungen.

---

## 📈 Workflow (Loop)

1. **Plan**: Architect Agent erstellt/aktualisiert Roadmap (`TODO-Index.md`).
2. **Build**: Builder Agent implementiert Module.
3. **Deploy**: Ops Agent integriert in Compose/Helm.
4. **Test**: QA Agent führt Tests & Reviews durch.
5. **Loop** bis Release-Definition erreicht.

---

## 🗺️ Aktuelle Mission (v0.1.0)

- [ ] NLP-Service (`services/nlp-service`) fertigstellen
- [ ] NiFi → Aleph Pipeline vorbereiten
- [ ] Frontend Tabs für NLP/Docs finalisieren
- [ ] Compose-Bundle mit allen Services lauffähig
- [ ] Superset Dashboard (Demo) hinzufügen
- [ ] Quickstart-Doku + Screenshots erstellen
- [ ] GitHub Release mit Tag `v0.1.0`

---

## 📜 Regeln für Agenten

- **Keine Monolithen** → Code modular, pro Service in eigenem Ordner.  
- **Keine Geheimnisse im Code** → Secrets nur über `.env`, nie hardcoden.  
- **Automatisierung bevorzugen** → Make, Helm, CI.  
- **Docs immer mitziehen** → Jede neue Funktion bekommt eine Doku-Seite oder README.  
- **Tests sind Pflicht** → Kein Commit ohne mindestens 1 Test für neue Funktion.  

---

## 🔄 Fortschrittstracking

- Alle abgeschlossenen Tasks → `TODO-Index.md` abhaken.  
- Jeder Service hat eigene README mit Setup/Usage.  
- `AGENTS.md` wird nach jedem Major-Sprint aktualisiert.  

---

## 🔖 Version
`AGENTS.md` erstellt für InfoTerminal **v0.1.0-pre**.  
Wird nach Release auf **v0.2** angepasst.


> Archived on 20250913-102414. Superseded by v0.2.
