# 🏭 SUPPLY-CHAIN-INTELLIGENCE-BLUEPRINT.md

## 🎯 Ziel
Analyse globaler Lieferketten, Erkennen von Risiken, Engpässen und Sanktionen.  
Simulationen („Was passiert, wenn…?“).

---

## 🧭 Architektur
- **Graph-Schema**:  
  - `(:Firm)-[:SUPPLIES]->(:Firm)`  
  - `(:Firm)-[:LOCATED_IN]->(:Geo)`  
  - `(:Firm)-[:SANCTIONED_BY]->(:Authority)`  
- **Datenquellen**: Open Data, Handelsregister, NGO-Reports, Sanktionen, News.  
- **Simulation Engine**: Impact von Events (z. B. Hafen blockiert → Firmen X betroffen).  

---

## 🔬 Module
- **Supply Graph**: Firmen + Lieferkettenbeziehungen.  
- **Risk Scoring**: Abhängigkeiten, Single-Point-of-Failure.  
- **Sanktions-Integration**: Verknüpfung zu Sanktionen/Blacklist.  
- **Event-Simulation**: Blockaden, Naturkatastrophen, politische Krisen.  

---

## 📊 Workflows
### NiFi
1. `ingest_supply_data` (Handelsdaten, Firmenregister)  
2. `enrich_sanctions` (OFAC/EU Sanctions → Graph)  
3. `simulate_event` (Impact-Berechnung → Risk Scores)

### n8n
- **Risk Alerts**: Firma unter Sanktion → Warnung  
- **Impact Reports**: Event (Blockade, Krieg) → betroffene Branchen  
- **Auto-Dossier**: Quartals-Report Supply Risks

---

## 🖥️ Frontend
- **Supply Chain Graph**: Interaktive Ansicht mit Risiken markiert.  
- Heatmap: Geografische Verteilung von Lieferketten.  
- Simulation Tool: „Wenn Hafen X blockiert → Auswirkungen auf Firmen Y/Z“.  
- Dossier-Export: „Top 10 Risikoketten im Quartal“.

---

## ✅ Tickets
- **[SUPPLY-1]** Graph-Schema SupplyChains + Sanctions  
- **[SUPPLY-2]** NiFi ingest_supply_data + enrich_sanctions  
- **[SUPPLY-3]** Simulation Engine (Event → Impact)  
- **[SUPPLY-4]** n8n Risk Alerts + Impact Reports  
- **[SUPPLY-5]** Frontend Supply Graph + Simulation Tool  
- **[SUPPLY-6]** Dossier-Template Supply Chain Risk Report
