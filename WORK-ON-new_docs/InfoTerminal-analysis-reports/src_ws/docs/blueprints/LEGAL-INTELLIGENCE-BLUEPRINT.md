# ⚖️ LEGAL-INTELLIGENCE-BLUEPRINT.md

## 🎯 Ziel
RAG-System für Gesetzestexte (z. B. SGB, StGB, EU-Verordnungen) und deren Verknüpfung mit Datenquellen wie Firmenregister, Politiker-Profile, Open Data und News.  
Erkennen von Compliance-Verstößen, Lobbying-Einfluss und geplanten Gesetzesänderungen.

---

## 🧭 Architektur
- **RAG-Service (`rag-api`)** für Gesetzeswerke (Paragraph-Level Chunking, Embeddings, Versionierung).
- **Graph-Erweiterung**:  
  - `(:Law {id, paragraph, title})`  
  - `(:LawChange)-[:AMENDS]->(:Law)`  
  - `(:Law)-[:APPLIES_TO]->(:Firm|:Sector)`  
  - `(:Politician)-[:SUPPORTED|:OPPOSED]->(:Law)`  
- **Verknüpfung mit Quellen**: Firmenregister, Handelsregister, Lobbylisten, Parlamentsprotokolle.

---

## 🔬 Module
- **RAG Retrieval**: Gesetze (Paragraph/Artikel) + Kontext.
- **Influence Mapping**: Politiker ↔ Lobbykontakte ↔ Firmen ↔ Gesetz.
- **Compliance Check**: News/Reports → „Verstoß gegen Paragraph X“ → Mapping zu Firmen.
- **Forecast**: Event Extraction + Timeline → Wahrscheinlichkeit für geplante Gesetzesänderungen.

---

## 📊 Workflows
### NiFi
1. `ingest_laws` (Scrape Bundesanzeiger/Parlamentsdokumente → JSON Chunks)  
2. `rag_index` (Paragraph-Chunk + Embedding → OpenSearch/Neo4j)  
3. `link_firms_laws` (Registerdaten ↔ Gesetzes-IDs)

### n8n
- **Compliance Alerts**: Firma ↔ Verstoß → Alert  
- **Lobbying Influence Report**: Politiker ↔ Lobby ↔ Gesetz ↔ Firma → Dossier  
- **Forecast**: geplanter Entwurf erkannt → Impact-Report Branche X

---

## 🖥️ Frontend
- Neuer Tab „⚖️ Legal/Compliance“  
- Features:  
  - Query → Paragraph + Firmen/Politiker + Evidenzliste  
  - Timeline: Gesetzesentwurf → Novelle → Inkrafttreten  
  - Dossier: „Firma A – Verstoß gegen §23 ArbSchG – Evidenz: Quelle X“

---

## ✅ Tickets
- **[LEGAL-1]** RAG-Service (rag-api) für Gesetzestexte  
- **[LEGAL-2]** Graph-Schema Erweiterung (:Law, :LawChange, Relations)  
- **[LEGAL-3]** NiFi Pipeline ingest_laws + rag_index  
- **[LEGAL-4]** n8n Compliance Alerts + Lobbying Reports  
- **[LEGAL-5]** Frontend Tab Legal/Compliance + Timeline-View  
- **[LEGAL-6]** Dossier-Template Compliance Report
