# 🛰️ DISINFORMATION-INTELLIGENCE-BLUEPRINT.md

## 🎯 Ziel
Erkennung koordinierter Desinformationskampagnen in Social Media & News.  
Cluster von Narrativen, Bot-Netzwerke, Fake-News-Verbreitung.

---

## 🧭 Architektur
- **Claim Clustering**: Duplikate/Narrative erkennen (SimHash/MinHash).  
- **Bot-Detection**: Account-Verhalten, Follower-Muster.  
- **Temporal Patterns**: Häufung in kurzer Zeit.  
- **Cross-Source Verification**: Abgleich Social Claims ↔ News/Trusted Sources.  

---

## 🔬 Module
- **Narrativ-Erkennung**: Claim Extraction + Clustering.  
- **Bot-Likelihood**: Posting-Kadenz, Netzwerk-Asymmetrien.  
- **Campaign Detection**: Gleichartige Claims + gleiche Zeit + verbundene Accounts.  
- **Fact-Check Integration**: Verknüpfung zu bekannten Fact-Check-Datenbanken.  

---

## 📊 Workflows
### NiFi
1. `ingest_social` (Telegram, Reddit, Mastodon)  
2. `claim_extract_cluster` (Cluster Narratives)  
3. `bot_detection` (Account Features, Graph Enrichment)

### n8n
- **Narrative Alerts**: Wenn neues Claim-Cluster > N Accounts → Alert  
- **BotNet Dossier**: Cluster + Bots + Ursprung → Report  
- **Influence Dashboard**: Top-Narratives + Reach

---

## 🖥️ Frontend
- **Dashboard „Top Narratives“**  
- Graph-Ansicht: Claim-Cluster ↔ Accounts ↔ Bots  
- Badges: „Likely Coordinated“, „Verified False“  
- Review-UI: Analyst kann Cluster markieren/überschreiben

---

## ✅ Tickets
- **[DISINFO-1]** Claim-Cluster Pipeline (MinHash/SimHash)  
- **[DISINFO-2]** Bot-Likelihood Modul (Account-Features)  
- **[DISINFO-3]** Temporal Pattern Detection  
- **[DISINFO-4]** n8n Narrative Alerts + BotNet Dossier  
- **[DISINFO-5]** Frontend Dashboard Top Narratives + Graph View  
- **[DISINFO-6]** Integration Fact-Check APIs
