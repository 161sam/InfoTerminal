# 🚀 Codex Entwickler Prompt — Produkt-Weiterentwicklung bis v0.5.0 (idempotent, konfliktfrei zur Docs-Konsolidierung)

**Kontext / Arbeitsumgebung**

* Repo: `/home/saschi/InfoTerminal`
* Primärer Arbeitsbranch für diese Instanz: **`codex/dev-tasks-v0.5`**
* Die **andere** Instanz arbeitet parallel an: `codex/docs-consolidation`
* Die **Docs** dienen als Spezifikation (Roadmaps, Guides, TODO-IDs)

**Konfliktvermeidung (sehr wichtig)**

* **Diese Instanz fasst `docs/` nicht proaktiv an.** Nur die folgenden *append-only* Stellen sind erlaubt, und auch nur mit ID-referenzierten, kleinen Ergänzungen:

  * `docs/dev/roadmap/v0.3-plus/master-todo.md` → Häkchen setzen/kurze Statuszeile **am Ende** eines Listeneintrags
  * `docs/dev/roadmap/release-plan.md` → Release-Notizen **append-only** unter deinem Release-Block
* Alle anderen Änderungen an `docs/` bleiben **der Konsolidierungs-Instanz** vorbehalten.
* Vor **jedem** Push: `git fetch --all && git rebase origin/main` (statt Merge).
* Wenn Rebase-Konflikt **in docs/**: **abbrechen**, nur Code pushen, Docs-Status an Konsolidierung überlassen.

---

## 🎯 Ziele (bis maximal v0.5.0)

* **v0.2**: NLP v1, Geo-Layer, NiFi/n8n Flows, Superset Dashboards, OIDC Auth, minimale Collaboration
* **v0.3**: Verification-Layer, Media Forensics Hooks, SDKs (Py/JS)
* **v0.4**: Security Hardening (Vault, SBOM, Cosign, Trivy Gates), Observability++ (SLO/SLI)
* **v0.5**: Dossier-Lite, Active Learning Loop, Stabilisierung

> Umsetzungsreihenfolge: **TODO-IDs → Epics → Releases** (DoD erfüllt), danach nächsten Block.

---

## 🧭 Ablauf (idempotent)

1. **Branching & Setup**

```
cd /home/saschi/InfoTerminal
git fetch --all
git checkout -B codex/dev-tasks-v0.5 origin/main
```

* Lege/aktualisiere Working-State:

  * `WORK-ON_new_docs/dev_progress/` (Logs, Artefakt-Listen, SBOMs)
  * `WORK-ON_new_docs/out/todo_index.md` **nicht** erzeugen – nur **lesen** (kommt von der anderen Instanz)

2. **Backlog-Import (nur lesen)**

* Parse `WORK-ON_new_docs/out/todo_index.md`
* Filter **offene** Tasks (`status=open`)
* Baue Epics nach Themen (Heuristik anhand Datei-/Pfadnamen/Tags):
  `nlp`, `geo`, `graph`, `ingest/nifi`, `n8n`, `superset`, `auth/oidc`, `verification`, `mediaforensics`, `sdk`, `observability`, `security`, `dossier`, `active-learning`
* Schreibe/aktualisiere **lokalen Plan** (idempotent):

  * `WORK-ON_new_docs/dev_progress/workplan.json`:

    ```json
    {
      "generated_at": "<UTC_ISO>",
      "epics": [{ "key": "nlp", "todo_ids": [...], "status": "pending|in_progress|done" }],
      "done_ids": [...],
      "skipped_ids": [{ "id": "T####-hash", "reason": "obsolete|blocked" }]
    }
    ```

3. **Implementieren pro Epic (idempotent)**

* Für jede Epic in definierter Reihenfolge:

  * Erzeuge Feature-Branch: `codex/feat-<epic>-v0.x`
  * Für jeden TODO-Eintrag (z. B. `T0123-abcd1234`):

    * Finde betroffene Pfade aus dem TODO-Eintrag (Quellangabe in der Tabelle)
    * Implementiere kleinste sinnvolle Einheit (Commit-Granularität)
    * **DoD pro Task:**

      * Code + **Unit/Component Tests**
      * Lint/Format (pre-commit / Makefile)
      * Wenn Dienst: **/healthz /readyz /metrics** vorhanden und dokumentiert im Code (README im Serviceordner)
      * **Trivy** (Container/FS) sauber oder akzeptierte Findings dokumentiert
      * **SBOM** generiert (CycloneDX/ SPDX) → ablegen unter `WORK-ON_new_docs/dev_progress/sbom/<service>.json`
    * Commit-Message-Schema:

      * `feat(nlp): <kurz> (closes T0123-abcd1234)`
      * `test(geo): add e2e bbox query (refs T0456-ef98ab10)`
      * `chore(ci): add trivy gate (refs T0789-11aa22bb)`
  * **Idempotenz:** Wenn der Commit-Inhalt bereits vorhanden (Hash gleich / Dateien unverändert), **kein weiterer Commit**.
  * Push Feature-Branch; eröffne PR **gegen `codex/dev-tasks-v0.5`**:

    * Titel: `feat(<epic>): <Kurzbeschreibung> [v0.x]`
    * Body: Liste der erledigten TODO-IDs, Test-Protokoll, SBOM-Pfad, evtl. bekannte Limitierungen

4. **Release-Schritte pro Minor (v0.2, v0.3, v0.4, v0.5)**

* Sammel-PR von `codex/dev-tasks-v0.5` → `main`, wenn:

  * CI grün (lint, tests, trivy, sbom)
  * **Idempotenz**: zweimaliger Lauf des CI-Jobs „build+test“ ergibt **keine** Artefakt-Diffs
* Tagging (lokal, **nur wenn erlaubt**):

  * `git tag v0.2.0` (oder `-rc.X`), Release-Notes **append-only** nach
    `docs/dev/roadmap/release-plan.md` → **nur anhängen, nicht umschreiben**
* Niemals Dateien unter `docs/` verschieben/umbenennen – das bleibt der anderen Instanz

5. **Konfliktvermeidung mit der Docs-Instanz**

* Vor **jedem** Push:

  ```
  git fetch --all
  git rebase origin/main
  ```
* Falls Rebase einen **docs/**-Konflikt bringt:

  * `git rebase --abort`
  * Nur Code-Änderungen (außer docs) committen & pushen
  * **Keine** manuellen Edits in `docs/` vornehmen

6. **Berichte & Artefakte**

* Für jeden Feature-PR:

  * `WORK-ON_new_docs/dev_progress/summary-<epic>-<timestamp>.md`
    mit: erledigte TODO-IDs, Testlauf-Zusammenfassung, Pfade zu SBOM/Reports
* Für jede Minor-Version:

  * `WORK-ON_new_docs/dev_progress/release-v0.x.0.md` + Liste aller PRs/Commits/IDs

---

## 🧪 Test- & CI-Leitplanken (idempotent)

* **Make-Targets nutzen** (falls nicht vorhanden, selbst anlegen/erweitern):

  ```
  make lint
  make test
  make build
  make security.scan      # trivy fs && trivy image
  make sbom               # z.B. cyclonedx/bom
  make check.idempotence  # zweimal build/test und Artefakte diffen
  ```
* Bei nicht vorhandenen Tools: defensiv abfangen, **Hinweis** in den Summary-Report schreiben, aber Build nicht hart failen (außer für sicherheitsrelevante Gates in Release-PRs).

---

## 📌 Umsetzungsreihenfolge (empfohlen)

1. **v0.2**

   * `nlp` (NER/summarize/relations APIs + Tests)
   * `geo` (within/nearest/layers + Map-Viewer Hooks)
   * `ingest/nifi` Flows + exportierbare Templates
   * `n8n` Playbooks (veracity/auto-dossier)
   * `superset` Dashboards + Deep-Links
   * `auth/oidc` (Keycloak / OPA ForwardAuth)
   * Minimal-Collab (Notes/Audit)

2. **v0.3**

   * `verification` Kernel (reputation, stance hooks)
   * `mediaforensics` (stub-Hooks + API contracts)
   * `sdk` (py/js skeleton + sample plugins)

3. **v0.4**

   * `security` (Vault, Trivy, SBOM, Cosign), Gates in CI
   * `observability` (SLO/SLI, Alerting)

4. **v0.5**

   * `dossier`-Lite Generator
   * `active-learning` Feedback → retrain loop (stub+pipeline)

> Überspringe Epics mit **blockierten** Abhängigkeiten; markiere im Workplan `skipped_ids` mit Grund.

---

## 🔁 Idempotenz-Regeln

* Vor jedem Schritt Hash/Existenz prüfen (Dateien, Configs, Tests).
* Commits nur, wenn sich **tatsächlich** etwas ändert.
* Workplan (`workplan.json`) **überschreiben** statt anhängen; Statusfelder aktualisieren.
* SBOM/Reports mit **deterministischen** Dateinamen (z. B. `<service>-<gitsha>.json`).
* Keine `docs/`-Moves/Renames von dieser Instanz.

---

## 🧾 Output an mich (je Lauf)

* **Zusammenfassung**:

  * Anzahl verarbeiteter TODO-IDs (done/refused/blocked)
  * Liste der **neuen** Feature-Branches/PRs
  * Letzte **Commit-SHAs**
  * Pfade zu neuen **SBOMs** und **Summary-Reports**
* Hinweise, falls Tasks blockiert (fehlende Spezifikation, unklarer Akzeptanztest)

---

## 🧨 Rollback

* Feature-Branch: `git reset --hard origin/<branch>`
* Sammel-Branch: `git checkout codex/dev-tasks-v0.5 && git reset --hard origin/codex/dev-tasks-v0.5`

---

**Los geht’s:** Führe diese Anweisungen **idempotent** aus. Achte streng auf die *Konfliktvermeidung mit `docs/`*. Implementiere Tasks gemäß TODO-IDs und liefere bis **v0.5.0** incrementell in Feature-Branches mit Tests, CI-Gates und SBOMs.
