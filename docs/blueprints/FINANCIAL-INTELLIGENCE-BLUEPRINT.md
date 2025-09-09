# 💰 FINANCIAL-INTELLIGENCE-BLUEPRINT.md

## 🎯 Ziel
Aufdecken von Geldwäsche, Steuerhinterziehung, Offshore-Netzwerken und illegalen Finanzflüssen.  
Fokus: Firmenregister + Finanzdaten + Leaks (Panama/Pandora Papers) + Sanktionen.

---

## 🧭 Architektur
- **Graph Schema**  
  - `(:Firm)-[:OWNS]->(:Account)-[:TRANSFERS]->(:Account)`  
  - `(:Firm)-[:REGISTERED_IN]->(:Jurisdiction)`  
  - `(:Account)-[:LINKED_TO]->(:SanctionList)`  
- **Datenquellen**: OpenBB, Firmenregister, Finanzaufsicht, Sanktionen, Leaks (ICIJ).  
- **Muster**: Layering, zyklische Transfers, Offshore-Knoten, Shell-Firmen.

---

## 🔬 Module
- **Transaction Graph Analysis**: Pfade, Kreisläufe, Häufungen.  
- **Risk Scoring**: High-Risk Jurisdictions, viele Offshore-Verbindungen.  
- **Anomaly Detection**: ungewöhnliche Transaktionsmuster (Betrag, Frequenz, Netzwerkknoten).  
- **Leak Integration**: Personen-/Firmen-Namen aus Leaks in Graph verknüpfen.

---

## 📊 Workflows
### NiFi
1. `ingest_financial_data` (OpenBB, Register, CSV, APIs)  
2. `enrich_sanctions` (OFAC/EU Listen)  
3. `link_leak_entities` (ICIJ Leaks → Graph-Knoten)  
4. `detect_anomalies` (Pattern Engine)  

### n8n
- **Red Flag Alerts**: ungewöhnliche Transfers, neue Offshore-Verbindungen.  
- **Dossier-Generator**: „Firmennetzwerk X – High Risk Score“.  
- **Escalation**: Hohe Scores → Compliance- oder Ermittlungsfall.  

---

## 🖥️ Frontend
- Finanzgraph: Firmen ↔ Accounts ↔ Transfers.  
- Heatmap: Offshore-Hubs, High-Risk Jurisdictions.  
- Risk-Dashboards: Scorecards pro Firma/Branche.  
- Dossier: „Top 10 Red Flag Netzwerke Q1“.

---

## ✅ Tickets
- **[FIN-1]** Graph-Schema Accounts/Transfers  
- **[FIN-2]** NiFi ingest_financial_data + enrich_sanctions  
- **[FIN-3]** Leak-Integration (ICIJ → Graph)  
- **[FIN-4]** Anomaly Detection Module  
- **[FIN-5]** n8n Red Flag Alerts + Escalations  
- **[FIN-6]** Frontend Finanzgraph + Risk-Dashboard  
- **[FIN-7]** Dossier-Vorlage „Financial Red Flags“
