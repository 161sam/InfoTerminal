# 📋 Codex Entwickler Prompt — InfoTerminal Docs Konsolidierung (idempotent)

**Ziel**
Ziel: Die gesamte Dokumentation konsolidieren und bereinigen (inkl. `docs/`), Roadmaps/TODOs zusammenführen, Deduplikate zusammenlegen – **ohne Detailverlust** – und alles versionssicher committen.

**Systemumgebung (gegeben)**

```
Repo Root: InfoTerminal/
Workdir mit Artefakten: InfoTerminal/WORK-ON-new_docs und InfoTerminal/docs
Vorhandene Artefakte: 
- InfoTerminal-analysis-reports.zip (+ entpackte Struktur)
- diverse "InfoTerminal-docs-clean-*.zip"
- tree-Texte, Migrationsberichte
Branch: main (aktuell synchronisiert)
```

---

## ✅ Regeln & Idempotenz

1. **Niemals Details löschen:** Bei Konsolidierung/Umzug stets **Provenance** (Quelle, Dateipfad, Zeilennummern) mitführen.
2. **Idempotent:** Auf jeder Ausführung

   * erkenne bereits migrierte Dateien/Abschnitte und **führe keine Doppelungen** herbei,
   * aktualisiere Indizes/Reports deterministisch,
   * lasse Dateiinhalte unverändert, sofern kein neuer inhaltlicher Merge nötig ist.
3. **Protokollierungspflicht:**

   * Schreibe **Änderungsjournal** mit exakten Pfaden, Abschnittsüberschriften, Zeilenbereichen und Kurz-Diff.
   * Halte **vorher/nachher**-Ziele fest.
4. **Git-Sicherheit:** Arbeite in einem **neuen Branch**; atomare, thematische Commits mit klaren Messages.
5. **Sprache & Benennung:**

   * User-Docs **DE**, Dev/API **EN**.
   * Dateinamen **kebab-case (ASCII)**, Umlaute zu `ae/oe/ue`, `ß`→`ss`.
   * Ports/Health/Ready/Metric-Konventionen konsistent dokumentieren.
6. **Pfadwahrung:** Behalte alle relativen Links funktionsfähig; aktualisiere Cross-Links nach Moves.

---

## 🧭 Arbeitsplan (Schritt für Schritt)

> **WICHTIG**: Führe die folgenden Befehle/Schritte **automatisiert** aus. Erstelle/aktualisiere die Skripte, führe sie aus, committe die Ergebnisse.

### 0) Vorbereitung

* Prüfe, ob Repo „sauber“ ist (`git status`).
* Erstelle/wechsele in Branch:

```
cd InfoTerminal/
git fetch --all
git checkout -b codex/docs-consolidation || git checkout codex/docs-consolidation
```

### 1) Hilfs-Tooling anlegen (idempotent)

Lege folgende Dateien an/aktualisiere sie **genau mit dem angegebenen Inhalt**:

#### a) `scripts/docs_pipeline.py`

* Python 3 Skript, das die folgenden Teilaufgaben kapselt:

  * **Analyse:**

    * Finde `docs/` im Repo.
    * Optional: entpacke `WORK-ON-new_docs/InfoTerminal-analysis-reports.zip` nach `WORK-ON-new_docs/_analysis_ws` (falls noch nicht vorhanden).
    * Erzeuge/aktualisiere:

      * `WORK-ON-new_docs/out/tree_with_summaries.txt` (virtuelles `tree` + erste sinnvolle Zeile je MD)
      * `WORK-ON-new_docs/out/inventory_blueprints_yaml_json.md` (Blueprints, YAML, JSON mit Pfaden)
      * `WORK-ON-new_docs/out/todo_index.md` (alle Checkboxen `- [ ]`/`- [x]`/nummerierte, plus `TODO:`/`FIXME:`/`NOTE:`; **mit IDs T####-hash, Datei, Zeile, Text**)
      * `WORK-ON-new_docs/out/duplicates_report.md` (Abschnitt-Ähnlichkeiten ≥0.88; Datei, Abschnittstitel, **Zeilenbereich**, Auszug A/B)
  * **Konsolidierung & Struktur:**

    * Zielstruktur herstellen:

      ```
      docs/
        README.md
        STYLE_GUIDE.md
        adr/
        architecture/
          overview.md (falls verfügbar; sonst aus diagrams/ARCHITECTURE.md migrieren)
          diagrams/
        blueprints/
          README.md
          blueprint-*.md
        dev/
          guides/
            testing.md
            rag-systems.md
            frontend-modernization.md
            preset-profiles.md
            flowise-agents.md
          research/
          roadmap/
            README.md (index)
            v0.1-overview.md
            v0.2-overview.md
            v0.3-plus/
              master-todo.md
              blueprint-ideas.md
              release-plan.md
              roadmap-gotham-gaps.md
        integrations/
          README.md
          n8n/ nifi/ waveterm/ export/
        presets/
          README.md
          waveterm/
        runbooks/
          stack.md (+ zusammengeführte Operability)
        user/
          01-einfuehrung.md, 02-..., (DE, nummeriert)
      ```
    * Wende **Rename-Regeln** an (kebab-case, ASCII), migriere veraltete Orte (z. B. `dev/runbooks/ → /docs/runbooks/`).
    * **Idempotenz:** Wenn Ziel bereits vorhanden und inhaltlich gleich/neuere Version, **nichts tun**; ansonsten **Merge** mit Front-Matter:

      ```yaml
      ---
      merged_from:
        - <alter_relativpfad1>#L<start>-L<end>
      merged_at: <UTC_ISO>
      ---
      ```
  * **Roadmaps & TODOs:**

    * `docs/dev/roadmap/v0.2-overview.md`: Abschnitt **„Offene Detail-Tasks (importiert)“** aus `todo_index.md` (Scope-Heuristik: `v0.2` im Pfad/Dateinamen).
    * `docs/dev/roadmap/v0.1-overview.md`: **„Abgeschlossene Detail-Tasks (importiert)“** für v0.1 Scope.
    * `docs/dev/roadmap/v0.3-plus/master-todo.md`: **alle offenen & erledigten** Tasks (Master-Register) mit Links zur Provenance.
    * `docs/dev/roadmap/task_provenance.md`: große Tabelle **(Status | Task | Quelle | Zeile)**.
  * **Deduplizierung (ohne Detailverlust):**

    * Für jeden Kandidaten aus `duplicates_report.md`:

      * Wähle **kanonischen Zielort** (z. B. `dev/guides/rag-systems.md` statt mehrfacher Fragmente).
      * Kopiere vollständigen Abschnitt **1:1** in Ziel (falls nicht identisch vorhanden), mit Front-Matter „merged\_from“ (Datei + Zeilen).
      * Ersetze Quelle in Sekundärdatei durch **Link** auf Zielabschnitt (Heading-Anchor); notiere die genaue **Zeilenersetzung**.
      * Schreibe eine **Änderungszeile** in das Journal (siehe unten).
  * **Indexseiten & Cross-Links:**

    * `docs/README.md`: Quicklinks auf Hauptordner (prüfe Existenz).
    * `docs/blueprints/README.md`: Liste aller `blueprint-*.md`.
    * `docs/presets/README.md`: Liste aller `profile-*.y*ml` (+ `waveterm/`).
    * `docs/integrations/README.md`: erste `.md` je Unterordner als Landing verlinken.
  * **Journal/Protokoll:**

    * `WORK-ON-new_docs/out/migration_journal.md`: jede Aktion als Eintrag:

      ```
      - ACTION: move|merge|link|rename
        SRC: docs/alt/pfad.md#L12-L88
        DST: docs/neu/pfad.md#<section-anchor>
        WHY: deduplicate | structure | index fix | i18n | naming
        DIFF: <kürzer Auszug vor/nach oder Hash>
      ```

> Implementiere robuste **Datei-/Abschnitts-Vergleiche** über Hashes der Normalform (Markdown ohne Links/Codeblöcke), um Idempotenz zu sichern.

#### b) `Makefile` Ergänzung

Füge (oder aktualisiere) Targets:

```
.PHONY: docs.analyze docs.consolidate docs.dedupe docs.all

docs.analyze:
\tpython3 scripts/docs_pipeline.py analyze

docs.consolidate:
\tpython3 scripts/docs_pipeline.py consolidate

docs.dedupe:
\tpython3 scripts/docs_pipeline.py dedupe

docs.all:
\tpython3 scripts/docs_pipeline.py analyze consolidate dedupe
```

#### c) `scripts/README-docs-pipeline.md`

Kurzer Leitfaden, wie `docs_pipeline.py` genutzt wird, inkl. Idempotenzhinweise.

> **Hinweis:** Wenn Dateien bereits existieren, **überschreibe nur** Tool-/Index-Artefakte und umgesetzt deduplizierte Abschnitte gem. Journal; Originalquellen bleiben per „merged\_from“ nachvollziehbar.

### 2) Ausführen

```
make docs.all
```

* Erwarte erzeugte/aktualisierte Artefakte in:

  * `WORK-ON-new_docs/out/tree_with_summaries.txt`
  * `WORK-ON-new_docs/out/inventory_blueprints_yaml_json.md`
  * `WORK-ON-new_docs/out/todo_index.md`
  * `WORK-ON-new_docs/out/duplicates_report.md`
  * `WORK-ON-new_docs/out/migration_journal.md`
* Prüfe, dass `docs/` jetzt der Zielstruktur entspricht (siehe oben).

### 3) Qualitätssicherung

* **Broken Links Check (Markdown):**
  Implementiere im Skript einen Link-Walker oder nutze ein leichtes Regex-Check, um relative `.md`-Links zu validieren.
  Schreibe Report nach `WORK-ON-new_docs/out/broken_links.md`.

* **Naming-Lint (ASCII/kebab-case):**
  Prüfe Dateinamen unter `docs/` und melde Verstöße in `WORK-ON_new_docs/out/naming_issues.md`.
  Auto-Rename nur, wenn Links/Querverweise anschließend **korrigiert** werden.

### 4) Git Commits (thematisch & atomar)

Führe **nur** wenn Änderungen vorhanden sind:

```
git add docs/ WORK-ON-new_docs/out/ Makefile scripts/
git commit -m "docs: consolidate structure, indices, and deduplicate with provenance

- Establish target structure (architecture/, blueprints/, dev/guides|roadmap, integrations/, presets/, runbooks/, user/)
- Generate tree/inventory/todo_index/duplicates_report (idempotent)
- Merge & link duplicate sections (no data loss, with merged_from provenance)
- Update indexes & cross-links (README files)
- Add docs_pipeline.py and Make targets
"
```

Wenn mehrere deduplizierende Merges erfolgten, teile in **Folge-Commits**:

* `docs: dedupe RAG systems sections (merge+link, provenance)`
* `docs: unify runbooks (stack + operability)`
* `docs: normalize blueprint filenames`

### 5) Push & PR

```
git push -u origin codex/docs-consolidation
```

Erzeuge/aktualisiere einen Pull Request mit Titel:

> **docs: consolidation, indices, dedup, roadmap & todo provenance (idempotent)**

Im PR-Text **anhängen**:

* kurze Übersicht der Moves/Merges,
* **Top-10 Dedupe-Einträge** aus `migration_journal.md`,
* Link auf `todo_index.md`, `duplicates_report.md`, `tree_with_summaries.txt`, `inventory_blueprints_yaml_json.md`.

---

## 🎯 Abnahmekriterien (Definition of Done)

* `docs/` entspricht der Zielstruktur; **keine toten Links**.
* **Alle** TODOs (Checkboxen + TODO/FIXME/NOTE) in `todo_index.md` mit **IDs + Quelle+Zeile**.
* Deduplizierte Abschnitte sind **nur** am kanonischen Ort vorhanden; Sekundärstellen enthalten **Links** dorthin.
* **Provenance** (merged\_from) in jedem konsolidierten Abschnitt.
* `migration_journal.md` listet **jede Änderung** mit Datei/Zeile/Anker und Begründung.
* Idempotent: erneutes `make docs.all` erzeugt **keine** ungewollten Änderungen.

---

## 🔧 Zusätzliche Hinweise für Codex (Implementierungsdetails)

* **Section-Split:** Headings `^#{1,6}\s+`; speichere `start_line`, `end_line`, `title`.
* **Normalisierung:**

  * entferne Codeblöcke `…`,
  * Links zu reinem Text (`[txt](url)` → `txt`),
  * Kleinbuchstaben, Interpunktion entfernen, Whitespace kollabieren.
* **Ähnlichkeit:** `difflib.SequenceMatcher` ≥ **0.88**.
* **Scope-Heuristik (Roadmaps):** Pfad/Dateiname enthält `v0.1|v0.2|v0.3-plus`; sonst `general`.
* **Filename-Normalize:** ASCII, `slug-kebab` (ersatz: ä→ae, ö→oe, ü→ue, ß→ss, `&`→`und`), Leerzeichen→`-`, mehrfach `-` zu einem.
* **Anchors:** Markdown-Heading-Anchor nach GitHub-Konvention (kebab-case).
* **Safe Writes:** erst in Temp schreiben, dann atomar ersetzen.
* **Backups/History:** nicht nötig (Git), aber bei riskanten Merges: `---` Front-Matter mit `merged_from`.

---

## 🛡️ Rollback

Falls nötig:

```
git reset --hard HEAD~1
# oder Branch verwerfen:
git checkout main
git branch -D codex/docs-consolidation
```

---

### Ende des Prompts

> Führe jetzt alle Schritte aus. Wenn Eingriffe notwendig sind, protokolliere sie in `WORK-ON-new_docs/out/migration_journal.md` und fahre fort, bis die Abnahmekriterien erfüllt sind.
