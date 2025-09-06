# 4. Kernfunktionen

Die folgenden Kapitel beschreiben die zentralen Bausteine von **InfoTerminal**.
Jede Kernfunktion ist modular aufgebaut und kann einzeln oder in Kombination genutzt werden.

---

## 4.1 🔎 Suche

Die **Search API** bildet das Herzstück der Plattform für Volltextrecherche und semantische Suche.

### Funktionen

* Klassische Volltextsuche über **OpenSearch**
* KI-gestützte **NER (Named Entity Recognition)** zur Extraktion von Personen, Organisationen und Orten
* **Embeddings & Reranking** für präzisere Ergebnisse
* Filter nach Zeit, Quelle und Entitätstyp

### Bedienung

* **Frontend (/search)**: intuitive Eingabemaske, Facettenfilter, Ergebnislisten
* **CLI**:

  ```bash
  it search.query "Beispiel AG"
  ```

---

## 4.2 🌐 Graph

Die **Graph API** erlaubt es, Entitäten und Beziehungen zu visualisieren und zu analysieren.
Daten werden in **Neo4j** gespeichert und mit Algorithmen ausgewertet.

### Funktionen

* Graph-Visualisierung (Frontend: /graphx)
* Abfragen in **Cypher**
* Graph-Algorithmen:

  * **Centrality** – wichtige Knoten finden
  * **Communities** – Cluster identifizieren
  * **Pathfinding** – kürzeste/verbindende Pfade

### Bedienung

* **Frontend (/graphx)**: Interaktives Graph-UI mit Zoom & Filter
* **CLI**:

  ```bash
  it graph.cypher "MATCH (n) RETURN count(n)"
  ```

---

## 4.3 📊 Dashboards

Für die **Visualisierung und Analyse** von Daten stehen zwei Tools zur Verfügung:

* **Superset** – für BI-Dashboards mit Cross-Filter & Deep-Links
* **Grafana** – für Logs, Metriken & Traces

### Funktionen

* KPI-Dashboards aus Suche & Graphen
* Cross-Filterung und Drill-Downs in Superset
* Metrics (Prometheus), Logs (Loki), Traces (Tempo) via Grafana

👉 Ziel: **Operative Einblicke + strategische BI in einem System**

---

## 4.4 📂 Dokumentenmanagement

Über die Integration von **Aleph** können Dokumente verarbeitet, durchsucht und verknüpft werden.

### Pipeline

1. **Ingest** (NiFi): Uploads, APIs, Web-Crawler
2. **Vorverarbeitung**: OCR (Tesseract), Language ID
3. **Analyse**: NER, Fingerprinting (Shingling)
4. **Indexierung**: OpenSearch + Graph-Verknüpfungen

### Nutzen

* Automatisches Erkennen von Namen, Organisationen, Orten in Dokumenten
* Cross-Referenzen zwischen Dokumenten & Graph-Daten
* Dossier-Funktion für Recherchen

---

## 4.5 🤖 Agents & Playbooks

**Agents** bieten KI-gestützte Unterstützung für komplexe Analysen.
Die Integration erfolgt über **Flowise** und **n8n**.

### Beispiele

* **Investigation Assistant**

  * erstellt Abfragepläne
  * ruft Search- & Graph-APIs
  * fertigt Notizen & Reports

* **Financial Risk Assistant**

  * kombiniert OpenBB-Daten mit Firmenregistern & Sanktionslisten
  * markiert Red Flags

### Playbooks (n8n)

* Automatisierte Pipelines für Alerts, Reports, Eskalationen
* Einbindung externer Tools & Datenquellen

---

## 4.6 🗺️ Geospatial-Layer

Der Geospatial-Layer ergänzt Graph-Analysen um **geografische Dimensionen**.

### Funktionen

* Kartenanzeige mit **Leaflet/MapLibre**
* Unterstützung für **GeoJSON**
* Visualisierung von Bewegungen, Orten, Clustern

### Nutzen

* Mapping von Entitäten auf reale Orte
* Geografische Analysen (z. B. Bewegungsmuster)
* Kombination mit Graph- und Dokumentendaten

---

## 4.7 🎥 Video-Pipeline

InfoTerminal unterstützt die Analyse von Videodaten.

### Pipeline

1. **Ingest** über NiFi (Streams oder Dateien)
2. **FFmpeg** für Vorverarbeitung
3. **ML-Modelle** für Objekterkennung & Gesichtserkennung

### Nutzen

* Analyse von CCTV, Livestreams, Archivmaterial
* Automatisches Erkennen relevanter Szenen/Personen
* Verbindung mit Graph- und Dokumentendaten

---

## 4.8 👥 Collaboration

InfoTerminal ist für **Teamarbeit** optimiert.

### Funktionen

* **Shared Notes** – gemeinsame Notizen zu Fällen
* **Multi-User Sessions** – mehrere Nutzer an denselben Daten
* **Audit Logs** – Nachvollziehbarkeit aller Aktionen

### Nutzen

* Bessere Zusammenarbeit in Investigations
* Vollständige Transparenz bei Analysen
* Grundlage für Compliance & Revisionssicherheit

---
