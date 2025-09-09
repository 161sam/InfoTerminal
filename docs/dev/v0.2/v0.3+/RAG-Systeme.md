# ⚖️ RAG-Systeme für Gesetzestexte & Compliance-Analysen

➡ Consolidated at: ../../guides/rag-systems.md#1-zielbild
## 2) Architektur-Erweiterung

### a) RAG-Speicher

* **Gesetze/Regelwerke**: in Chunks (Paragraph/Artikel), mit Metadaten (Quelle, Gültigkeit, Änderungsdatum).
* **Index**: OpenSearch (BM25 + Embeddings), ergänzt durch Neo4j-Knoten „(\:Law {id, title, paragraph, domain})“.
* **Versionierung**: Jede Änderung (z. B. neue Gesetzesnovelle) als neuer Node mit `[:AMENDS]` Relation.

### b) Abfrage & Verknüpfung

* **RAG Query Flow**:

  1. User-Frage → Query Expansion (Entities, Zeit, Gesetzesbegriffe).
➡ Consolidated at: ../../guides/rag-systems.md#2-retrieval-relevante-gesetzesparagraphen-unternehmensdaten-politische-akteure

### c) Mustererkennung

* **Pattern Templates**:

➡ Consolidated at: ../../guides/rag-systems.md#compliance-check-firma-aktivit-t-paragraph
* Retrieval: Partei X (Graph: Entities), Firma Y (Handelsregister, Lobbylisten), Gesetzesänderungen (Parlamentsdokumente).
* Pipeline:

  * Graph-API sucht Verbindungen (Politiker ↔ Lobbyliste ↔ Firma).
  * RAG sucht relevante Paragraphen zu Gesetzen.
  * Verifikation prüft Medienberichte (Faktencheck).
* Ergebnis: Graph + Dossier mit „Verbindungsketten“, Gesetzesbezug, Evidenz (Artikel/Parlament).

### Beispiel B – Branchen-Compliance

**Query:** „Welche Firmen aus Branche Z stehen in Verbindung zu Gesetzesverstößen?“
➡ Consolidated at: ../../guides/rag-systems.md#

## 4) Technische Umsetzung (Integration in InfoTerminal)

* **RAG-Service (`rag-api`)**:

  * Indexierung von Gesetzestexten, Verträgen, Regularien.
  * API-Endpunkte:

    * `/law/retrieve?q=...`
    * `/law/context?entity=...` (zeigt, welche Gesetze für Entität relevant sind)
  * Backend: LangChain/LlamaIndex mit OpenSearch + Neo4j.
➡ Consolidated at: ../../guides/rag-systems.md#

* **Frontend**:

  * Neuer Tab „⚖️ Compliance/Legal“:

    * User Query → Graph + Law-Panel + Evidenz.
    * Timeline: wann trat Gesetz in Kraft, welche Firmen/Politiker sind betroffen.

---

## 5) Erweiterungen & Differenzierung
➡ Consolidated at: ../../guides/rag-systems.md#
* Mittelfristig: Pattern-Engine (Compliance, Influence, Risk).
* Langfristig: Predictive + Simulation (Impact geplanter Gesetze).

---

👉 Daraus einen **`LEGAL-INTELLIGENCE-BLUEPRINT.md`** schreiben (analog zu Security/Verification), mit Schema, APIs, Flows und Tickets, die direkt ins Repo passen.
