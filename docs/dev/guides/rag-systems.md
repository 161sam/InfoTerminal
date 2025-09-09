---
merged_from:
  - docs/dev/RAG-Systeme.md#L1-L117
merged_at: 2025-09-09T13:14:27.277117Z
---
# ⚖️ RAG-Systeme für Gesetzestexte & Compliance-Analysen

## 1) Zielbild

- **RAG-Layer** mit Gesetzestexten (z. B. SGB, StGB, EU-Verordnungen, Finanzmarktgesetze).
- **Verknüpfung mit Datenquellen** (Firmenregister, OpenBB, Open Data, News/SoMe, Threat Feeds).
- **Fragen beantworten können wie:**
  - „Welche Politiker aus Partei X haben über Lobby- oder Firmenverbindungen Einfluss auf Gesetz Y genommen?“
  - „Welche Firmen aus Branche Z verstoßen gegen Paragraph X?“
  - „Welche geplanten Gesetze hätten wirtschaftliche Auswirkungen auf Unternehmen A?“

---

## 2) Architektur-Erweiterung

### a) RAG-Speicher

- **Gesetze/Regelwerke**: in Chunks (Paragraph/Artikel), mit Metadaten (Quelle, Gültigkeit, Änderungsdatum).
- **Index**: OpenSearch (BM25 + Embeddings), ergänzt durch Neo4j-Knoten „(\:Law {id, title, paragraph, domain})“.
- **Versionierung**: Jede Änderung (z. B. neue Gesetzesnovelle) als neuer Node mit `[:AMENDS]` Relation.

### b) Abfrage & Verknüpfung

- **RAG Query Flow**:
  1. User-Frage → Query Expansion (Entities, Zeit, Gesetzesbegriffe).
  2. Retrieval: relevante Gesetzesparagraphen + Unternehmensdaten + Politische Akteure.
  3. **Pattern Engine**:
     - Verstößt eine Handlung gegen Paragraph X?
     - Existieren Verbindungen zwischen Akteur ↔ Firma ↔ Gesetz?

  4. Antwort: textuell + Graph-Visualisierung + Evidenz-Liste.

### c) Mustererkennung

- **Pattern Templates**:
  - _Compliance-Check_: Firma ↔ Aktivität ↔ Paragraph.
  - _Influence-Mapping_: Politiker ↔ Gesetz ↔ Firma ↔ Outcome.
  - _Risk-Scoring_: Wahrscheinlichkeit, dass eine Handlung als „illegal“ oder „kritisch“ einzustufen ist.

---

## 3) Szenario-Umsetzung

### Beispiel A – Politiker & Firmen

**Query:** „Welche Politiker der Partei X haben Verbindungen zu Firma Y und Gesetze mit Auswirkungen verabschiedet?“

- Retrieval: Partei X (Graph: Entities), Firma Y (Handelsregister, Lobbylisten), Gesetzesänderungen (Parlamentsdokumente).
- Pipeline:
  - Graph-API sucht Verbindungen (Politiker ↔ Lobbyliste ↔ Firma).
  - RAG sucht relevante Paragraphen zu Gesetzen.
  - Verifikation prüft Medienberichte (Faktencheck).

- Ergebnis: Graph + Dossier mit „Verbindungsketten“, Gesetzesbezug, Evidenz (Artikel/Parlament).

### Beispiel B – Branchen-Compliance

**Query:** „Welche Firmen aus Branche Z stehen in Verbindung zu Gesetzesverstößen?“

- Retrieval: Firmen-Cluster (Branche Z), News/Dossiers, Gesetzestexte.
- Pipeline:
  - NLP → Extract „Verstoß gegen §X“ aus Artikeln.
  - Mapping zu Firmen im Graph.
  - RAG → Paragraph X Definition + Auslegung.

- Ergebnis: Liste + Graph + Risikobewertung.

---

## 4) Technische Umsetzung (Integration in InfoTerminal)

- **RAG-Service (`rag-api`)**:
  - Indexierung von Gesetzestexten, Verträgen, Regularien.
  - API-Endpunkte:
    - `/law/retrieve?q=...`
    - `/law/context?entity=...` (zeigt, welche Gesetze für Entität relevant sind)

  - Backend: LangChain/LlamaIndex mit OpenSearch + Neo4j.

- **Graph-Erweiterung**:
  - `(:Law)-[:APPLIES_TO]->(:Sector|:Firm|:Event)`
  - `(:Politician)-[:SUPPORTED|:OPPOSED]->(:Law)`
  - `(:LawChange)-[:AMENDS]->(:Law)`

- **NLP/Verification Layer**:
  - Claim Extraction erkennt juristische Claims („Firma X verstößt gegen §23…“).
  - Mapping zu Paragraphen im RAG-Speicher.
  - Evidenz Panel zeigt Gesetzestext + relevante Artikel.

- **Frontend**:
  - Neuer Tab „⚖️ Compliance/Legal“:
    - User Query → Graph + Law-Panel + Evidenz.
    - Timeline: wann trat Gesetz in Kraft, welche Firmen/Politiker sind betroffen.

---

## 5) Erweiterungen & Differenzierung

- **Predictive Impact**: Simulation, wie geplante Gesetze Branchen/Unternehmen betreffen.
- **Comparative Law**: EU vs. nationales Recht nebeneinander.
- **Compliance Alerts**: n8n Flow → „Neue Gesetzesänderung betrifft Branche Z → Firmenwarnung“.
- **Auto-Dossiers**: „Top 10 Verstöße gegen Umweltgesetzgebung im letzten Quartal“.
- **Ethical Checks**: Kennzeichnung, wenn Analyse unsicher/mehrdeutig (Transparenz).

---

# 📌 Fazit

Deine Idee → **RAG auf Gesetze + Datenquellen** = **Compliance & Legal Intelligence Layer**.

- Kurzfristig: Gesetzeswerke (SGB, StGB, EU-Verordnungen) indexieren → Retrieval + Graph-Knoten.
- Mittelfristig: Pattern-Engine (Compliance, Influence, Risk).
- Langfristig: Predictive + Simulation (Impact geplanter Gesetze).

---

👉 Soll ich dir daraus eine neue **`LEGAL-INTELLIGENCE-BLUEPRINT.md`** schreiben (analog zu Security/Verification), mit Schema, APIs, Flows und Tickets, die direkt ins Repo passen?
---
merged_from:
  - docs/adr/0002-multi-storage-pattern.md#L1-L4
merged_at: 2025-09-09T13:55:10.778148Z
---

# ADR 0002: Multi-Storage Pattern

Date: 2025-09-02

---
merged_from:
  - docs/adr/0002-multi-storage-pattern.md#L5-L8
merged_at: 2025-09-09T13:55:10.779511Z
---


## Context

Different workloads require search, graph traversal and transactional storage.
---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L3-L14
merged_at: 2025-09-09T13:55:10.864302Z
---

## 1) Zielbild

* **RAG-Layer** mit Gesetzestexten (z. B. SGB, StGB, EU-Verordnungen, Finanzmarktgesetze).
* **Verknüpfung mit Datenquellen** (Firmenregister, OpenBB, Open Data, News/SoMe, Threat Feeds).
* **Fragen beantworten können wie:**

  * „Welche Politiker aus Partei X haben über Lobby- oder Firmenverbindungen Einfluss auf Gesetz Y genommen?“
  * „Welche Firmen aus Branche Z verstoßen gegen Paragraph X?“
  * „Welche geplanten Gesetze hätten wirtschaftliche Auswirkungen auf Unternehmen A?“

---

---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L17-L22
merged_at: 2025-09-09T13:55:10.865890Z
---

  2. Retrieval: relevante Gesetzesparagraphen + Unternehmensdaten + Politische Akteure.
  3. **Pattern Engine**:

     * Verstößt eine Handlung gegen Paragraph X?
     * Existieren Verbindungen zwischen Akteur ↔ Firma ↔ Gesetz?
  4. Antwort: textuell + Graph-Visualisierung + Evidenz-Liste.
---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L23-L34
merged_at: 2025-09-09T13:55:10.867723Z
---

  * *Compliance-Check*: Firma ↔ Aktivität ↔ Paragraph.
  * *Influence-Mapping*: Politiker ↔ Gesetz ↔ Firma ↔ Outcome.
  * *Risk-Scoring*: Wahrscheinlichkeit, dass eine Handlung als „illegal“ oder „kritisch“ einzustufen ist.

---

## 3) Szenario-Umsetzung

### Beispiel A – Politiker & Firmen

**Query:** „Welche Politiker der Partei X haben Verbindungen zu Firma Y und Gesetze mit Auswirkungen verabschiedet?“

---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L35-L44
merged_at: 2025-09-09T13:55:10.869349Z
---


* Retrieval: Firmen-Cluster (Branche Z), News/Dossiers, Gesetzestexte.
* Pipeline:

  * NLP → Extract „Verstoß gegen §X“ aus Artikeln.
  * Mapping zu Firmen im Graph.
  * RAG → Paragraph X Definition + Auslegung.
* Ergebnis: Liste + Graph + Risikobewertung.

---
---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L47-L58
merged_at: 2025-09-09T13:55:10.870781Z
---


* **Graph-Erweiterung**:

  * `(:Law)-[:APPLIES_TO]->(:Sector|:Firm|:Event)`
  * `(:Politician)-[:SUPPORTED|:OPPOSED]->(:Law)`
  * `(:LawChange)-[:AMENDS]->(:Law)`

* **NLP/Verification Layer**:

  * Claim Extraction erkennt juristische Claims („Firma X verstößt gegen §23…“).
  * Mapping zu Paragraphen im RAG-Speicher.
  * Evidenz Panel zeigt Gesetzestext + relevante Artikel.
---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L59-L72
merged_at: 2025-09-09T13:55:10.872275Z
---


* **Predictive Impact**: Simulation, wie geplante Gesetze Branchen/Unternehmen betreffen.
* **Comparative Law**: EU vs. nationales Recht nebeneinander.
* **Compliance Alerts**: n8n Flow → „Neue Gesetzesänderung betrifft Branche Z → Firmenwarnung“.
* **Auto-Dossiers**: „Top 10 Verstöße gegen Umweltgesetzgebung im letzten Quartal“.
* **Ethical Checks**: Kennzeichnung, wenn Analyse unsicher/mehrdeutig (Transparenz).

---

# 📌 Fazit

Deine Idee → **RAG auf Gesetze + Datenquellen** = **Compliance & Legal Intelligence Layer**.

* Kurzfristig: Gesetzeswerke (SGB, StGB, EU-Verordnungen) indexieren → Retrieval + Graph-Knoten.
---
merged_from:
  - docs/dev/v0.2/v0.3+/RAG-Systeme.md#L6-L11
merged_at: 2025-09-09T14:17:02.164373Z
---

### a) RAG-Speicher

* **Gesetze/Regelwerke**: in Chunks (Paragraph/Artikel), mit Metadaten (Quelle, Gültigkeit, Änderungsdatum).
* **Index**: OpenSearch (BM25 + Embeddings), ergänzt durch Neo4j-Knoten „(\:Law {id, title, paragraph, domain})“.
* **Versionierung**: Jede Änderung (z. B. neue Gesetzesnovelle) als neuer Node mit `[:AMENDS]` Relation.

