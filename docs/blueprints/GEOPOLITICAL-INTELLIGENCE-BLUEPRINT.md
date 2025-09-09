# 🌍 GEOPOLITICAL-INTELLIGENCE-BLUEPRINT.md

## 🎯 Ziel
Analyse geopolitischer Bewegungen, Konflikte und sicherheitsrelevanter Muster.  
Fokus: Flugbewegungen, Schiffsbewegungen, Proteste, Konflikt-Events.

---

## 🧭 Architektur
- **Graph Schema**  
  - `(:Event)-[:LOCATED_AT]->(:GeoPoint)`  
  - `(:Asset)-[:OBSERVED_AT]->(:Event)`  
  - `(:Event)-[:RELATED_TO]->(:Conflict|:Protest)`  
- **Datenquellen**: ADS-B (Flugzeuge), AIS (Schiffe), OSM, Social Media (Geo-Tags), NGO/UN Reports.  
- **Muster**: ungewöhnliche Bewegungen, Häufung von Events, Protest-Cluster.

---

## 🔬 Module
- **Geo-Anomaly Detection**: Abweichungen vom Normalverkehr.  
- **Event Clustering**: mehrere Quellen berichten → höherer Confidence.  
- **Conflict Mapping**: Proteste ↔ Bewegungen ↔ staatliche Akteure.  
- **Simulation**: Ausbreitung oder Eskalation von Konflikten.

---

## 📊 Workflows
### NiFi
1. `ingest_adsb` (Flugbewegungen)  
2. `ingest_ais` (Schiffsbewegungen)  
3. `merge_geo_social` (OSM + Geo-Posts)  
4. `detect_geo_anomalies`  

### n8n
- **Alert**: „Ungewöhnliche Bewegung in Region X“  
- **Conflict Report**: Ereignisse + Akteure → Dossier  
- **Dashboard**: Timeline + Heatmap

---

## 🖥️ Frontend
- Map Dashboard: Flugzeuge, Schiffe, Proteste, Konflikte.  
- Timeline: Abfolge von Ereignissen mit Geo-Relation.  
- Simulation: „Wenn Truppenbewegung X, Wahrscheinlichkeit Eskalation Y%“.  
- Dossier: „Region X – Konflikt-Analyse“.

---

## ✅ Tickets
- **[GEO-1]** NiFi ingest_adsb + ingest_ais + merge_geo_social  
- **[GEO-2]** Graph-Schema Events/Assets/Conflicts  
- **[GEO-3]** Anomaly Detection Modul (Geo-Time)  
- **[GEO-4]** n8n Alerts + Conflict Reports  
- **[GEO-5]** Frontend Map Dashboard + Timeline  
- **[GEO-6]** Simulation Engine (Eskalations-Szenarien)  
- **[GEO-7]** Dossier-Vorlage „Geopolitical Conflict Report“
