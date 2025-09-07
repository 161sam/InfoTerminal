# 15. Dashboards mit Superset

**Apache Superset** ist das BI-Frontend für **Dashboards, KPIs und interaktive Analysen**.

---

## 15.1 Funktionen

- **SQL-basierte Abfragen** auf Postgres, Neo4j-Views, OpenSearch
- **KPI-Visualisierungen** (Tabellen, Charts, Karten)
- **Cross-Filter**: Filterung in einem Chart aktualisiert alle anderen
- **Deep-Links**: direkte Verknüpfung zu Such- oder Graph-Ergebnissen

---

## 15.2 Nutzung in InfoTerminal

1. Superset starten:

   ```bash
   docker compose --profile superset up -d
   ```

   UI: [http://localhost:8088](http://localhost:8088)

2. Datenquellen verbinden:
   - Postgres (`graph-views`)
   - OpenSearch (`search-api`)
   - Neo4j (über Treiber oder Export-Views)

3. Dashboard erstellen:
   - SQL-Query definieren
   - Visualisierung wählen (Tabelle, Balken, Netzdiagramm, Karte)
   - Filter hinzufügen

---

## 15.3 Beispiel-Dashboards

- **Investigations-Dashboard**
  - Anzahl neuer Dokumente (Aleph)
  - Top-Entities (Graph)
  - Netzwerk-Heatmap (Geospatial)

- **Compliance-Dashboard**
  - Firmen mit Risiko-Flag
  - Beteiligungsnetzwerke
  - Alerts aus n8n-Playbooks

---

## 15.4 Best Practices

- **Drill-Down-Queries** nutzen → schnelle Detailanalyse
- **Deep-Links zu Graph** einfügen → direkte Visualisierung von Netzwerken
- Dashboards **versionieren** (als JSON exportieren und ins Repo einchecken)
- **Cross-Filter aktivieren** für interaktive Analysen

---
