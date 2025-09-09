# 📋 Codex Entwickler Folge Prompt — Docs Konsolidierung Phase 2 (idempotent)

**Kontext:**
Repo: `/home/saschi/InfoTerminal`
Branch: `codex/docs-consolidation` (falls nicht vorhanden, neu anlegen)
Bestehendes Skript: `scripts/docs_pipeline.py` (mit analyze/consolidate/dedupe Platzhaltern)
Ziel: Roadmap-Integration + echte Deduplizierung implementieren.

---

## 🧭 Aufgaben

### 1) Roadmap Task Integration

* Erweitere `scripts/docs_pipeline.py` um Logik in `consolidate`:

  * Lade `WORK-ON-new_docs/out/todo_index.md`.
  * Finde Tasks, deren Pfad auf `v0.1`, `v0.2` oder `v0.3+` verweist.
  * Schreibe in:

    * `docs/dev/roadmap/v0.1-overview.md` → Abschnitt **„Abgeschlossene Detail-Tasks“** (done-Tasks).
    * `docs/dev/roadmap/v0.2-overview.md` → Abschnitt **„Offene Detail-Tasks“** (open-Tasks).
    * `docs/dev/roadmap/v0.3-plus/master-todo.md` → Liste aller Tasks (open+done) mit Verweis (File, Zeile, ID).
  * Format:

    ```markdown
    - [ ] T0123-abcd1234 Implement NER API in `services/nlp` (docs/dev/roadmap/v0.2-to-build.md:14)
    ```

### 2) Deduplizierung & Link-Rewrites

* Erweitere `dedupe` in `scripts/docs_pipeline.py`:

  * Eingabe: `WORK-ON-new_docs/out/duplicates_report.md`.
  * Für jeden Eintrag:

    * Wähle **kanonischen Zielort** (Heuristik):

      * `rag` → `docs/dev/guides/rag-systems.md`
      * `frontend-modernisierung` → `docs/dev/guides/frontend-modernization.md`
      * `preset-profile` → `docs/dev/guides/preset-profiles.md`
      * `flowise`+`agent` → `docs/dev/guides/flowise-agents.md`
      * `operability` → `docs/runbooks/stack.md`
      * Sonst: Roadmap-Dateien nur für Plan/Strategie-Inhalte.
    * Prüfe, ob Abschnitt (per Hash) bereits am Ziel vorhanden → wenn ja, SKIP.
    * Wenn nicht:

      * Kopiere Abschnitt **1:1** ans Zielende, mit Front-Matter:

        ```yaml
        ---
        merged_from:
          - <rel_path>#L<start>-L<end>
        merged_at: <UTC_ISO>
        ---
        ```
      * Ersetze Quellabschnitt durch:

        ```
        ➡ Consolidated at: ../<target>.md#<heading-anchor>
        ```
    * Trage Änderung in `WORK-ON-new_docs/out/migration_journal.md` ein:

      ```
      - ACTION: merge+link
        SRC: docs/dev/v0.2/RAG-Systeme.md#L12-L88
        DST: docs/dev/guides/rag-systems.md#retrieval
        WHY: deduplicate
        HASH: <section-hash>
      ```

### 3) Idempotenz

* Bei erneutem Lauf:

  * Keine doppelten Einträge im Ziel (prüfe Hash).
  * Keine erneuten Pointers in der Quelle (prüfe bereits vorhandene Zeilen).
  * Journal-Einträge nur für **neue Änderungen**.

### 4) Reports

* Nach Konsolidierung & Deduplizierung → `make docs.all` neu laufen lassen.
* Aktualisiere Reports (`todo_index.md`, `duplicates_report.md`, `migration_journal.md`).

### 5) Commits

* Thematische Commits:

  * `docs: integrate TODO index into roadmap files (idempotent)`
  * `docs: implement deduplication with provenance + link rewrites`
* Branch: `codex/docs-consolidation`
* Push: `git push -u origin codex/docs-consolidation`

---

## 🎯 Output für mich

* Anzahl Tasks, die in Roadmaps integriert wurden.
* Anzahl deduplizierter Abschnitte (mit Ziel-Dateien).
* Top-5 Journal-Einträge aus `migration_journal.md`.
* Commit-Hashes der letzten beiden Commits.


Willst du, dass ich dir parallel noch einen **Reviewer-Guide für den nächsten PR** formuliere (worauf dein Review-Fokus liegen sollte)?
