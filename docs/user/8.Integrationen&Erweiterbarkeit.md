# 8. Integrationen & Erweiterbarkeit

Einer der größten Vorteile von **InfoTerminal** ist seine **Offenheit für externe Tools**.
Daten können nahtlos ein- und ausgekoppelt werden, und neue Funktionen lassen sich über Plugins hinzufügen.

---

## 8.1 NiFi Pipelines

**Apache NiFi** übernimmt die **Datenintegration (Ingest & ETL)**.

### Funktionen

- Dateien, APIs und Datenbanken anbinden
- Streaming-Daten verarbeiten (z. B. RSS, Social Media, Sensoren)
- Daten normalisieren und in das kanonische Schema überführen

### Typische Pipelines

- `ingest_normalize` → Datenaufnahme & Standardisierung
- `claim_extract` → Extraktion von Behauptungen aus Texten
- `evidence_retrieval` → Abruf von Quellen & Belegen
- `geo_time_media` → Prüfung auf Raum, Zeit & Medienmanipulation
- `aggregate_upsert` → Speicherung in OpenSearch & Neo4j

👉 NiFi ist der **Hauptmotor** für Datenaufnahme & Vorverarbeitung.

---

## 8.2 n8n Playbooks

**n8n** ergänzt NiFi um **Automatisierungen & Workflows**.

### Funktionen

- Playbooks für Investigations, Alerts & Reports
- Einfache Anbindung von APIs (Slack, Telegram, E-Mail, CRM-Systeme)
- Trigger-Logik für Eskalationen

### Beispiele

- **Veracity Alerts** → bei fragwürdigen Nachrichten Quellenprüfung auslösen
- **Auto-Dossiers** → Ergebnisse automatisch zusammenfassen & exportieren
- **Escalations** → Weiterleitung an Analystenteams oder Behörden

👉 n8n ist das **I/O-Gateway** von InfoTerminal.

---

## 8.3 Flowise Agents

**Flowise** bringt die **LLM-gestützten Assistenten** ins Spiel.

### Beispiele

- **Investigation Assistant**
  - nimmt Fall-IDs entgegen
  - erstellt Abfragepläne
  - ruft Search- & Graph-APIs
  - erzeugt Reports

- **Financial Risk Assistant**
  - kombiniert OpenBB-Daten, Firmenregister & Sanktionslisten
  - markiert verdächtige Muster

👉 Flowise ist die **Agenten-Schicht**, die KI mit InfoTerminal verbindet.

---

## 8.4 Export zu AppFlowy & AFFiNE

**AppFlowy** und **AFFiNE** können als **Dokumenten- und Workspace-Erweiterung** angebunden werden.

### Funktionen

- **Dossiers** direkt als Dokument exportieren
- **Graphen** als Diagramme in Notizen einfügen
- **Berichte** automatisch synchronisieren

👉 Damit wird InfoTerminal in bestehende **Team-Workspaces** integriert.

---

## 8.5 WaveTerm-Kompatibilität

**WaveTerm** ist ein modernes Terminal mit Plugin-Support.

### Zwei Ansätze

1. **WaveTerm als Plugin in InfoTerminal**
   - vorkonfigurierte Workspaces, Plugins & Settings
   - Terminal direkt im Browser-Frontend

2. **InfoTerminal als Plugin für WaveTerm**
   - CLI & Frontend in WaveTerm verfügbar
   - Integration mit Workspaces & Agenten

👉 Damit können Nutzer entscheiden, ob sie InfoTerminal als **Zentrale** oder **Erweiterung** nutzen.

---

## 8.6 Plugin-System

InfoTerminal ist durch ein **SDK für Plugins** erweiterbar.

- **Python SDK** → Analyse-Plugins & Pipelines
- **JavaScript SDK** → Frontend-Erweiterungen
- **CLI SDK** → neue `it`-Befehle
- **Kali Linux Tools Integration** → Security- & OSINT-Tools direkt als Plugin

👉 Das Plugin-System sorgt für maximale Flexibilität.

---
