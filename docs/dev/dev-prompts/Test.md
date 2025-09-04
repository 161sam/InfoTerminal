## Codex Prompt — Vollständige Testabdeckung (100 %), idempotent

### Kontext & Ziele

* Monorepo „InfoTerminal“ mit Modulen:

  * services/search-api (FastAPI)
  * services/graph-api (FastAPI, Neo4j-Driver, Exponential-Backoff)
  * services/graph-views (FastAPI, psycopg2/SQLAlchemy, Lifespan-Pool)
  * apps/frontend (Next.js 14, Tailwind v4, React)
  * cli/it\_cli (Typer + Rich, Banner/Version, Infra-Kommandos, TUI-Logs)
* Bereits vorhandene Tests: pytest für Python-Dienste, erste CLI-Tests, rudimentäre Frontend-Tests.
* Ziel: **100 % Testabdeckung pro Teilprojekt** (Unit-/Komponententests). Integration/E2E optional separat, aber nicht für die 100 % nötig.
* **Idempotenz:** Mehrfaches Ausführen dieses Auftrags darf keine Duplikate erzeugen, keine Konfiguration überschreiben, wenn bereits korrekt, und keine User-Home-Venvs anlegen.

### Allgemeine Leitplanken

1. **Keine Netz-/Container-Abhängigkeit für Unit-Tests.** Externe Systeme (Neo4j, Postgres, HTTP-Backends) strikt mocken/stubben.
2. **Abdeckung messen & festschreiben.** Für Python via coverage/pytest, für Frontend via Jest. Coverage-Schwellen auf **100 %** setzen. Generierte/Framework-Dateien bewusst ignorieren.
3. **Idempotenzregeln:**

   * Vor Anlage neuer Testdateien prüfen, ob äquivalente bereits existieren (Namensschema, Testinhalt).
   * Konfigurationen nur ergänzen/vereinheitlichen, niemals duplizieren.
   * Keine venv im Home-Verzeichnis erzeugen; lokale/CI-Umgebungen nutzen projektlokale Mechanismen.
4. **Stabilität:** Tests deterministisch (keine Sleeps/Random ohne Seeding). Zeit/Backoff via Mocks fassbar machen.
5. **Dokumentation:** Kurznotizen in /docs über „Wie Tests lokal/CI laufen“ und „Coverage-Regeln“.

### Python-Dienste (search-api, graph-api, graph-views)

**Ziele:** 100 % Branch/Line-Coverage inkl. Fehlerpfade.

* **graph-api**

  * Abdecken: Lifespan-Initialisierung des Neo4j-Drivers, Exponential-Backoff inkl. „nach N Versuchen abbrechen“, Healthz 200/503, Ping, Query, Neighbors – je success/failure.
  * Neo4j-Driver & Netzwerk via Mocks. Keine echte Bolt-Verbindung.
  * Edge Cases: ungültige Cypher, Timeout, falsche Credentials, env-Variablen fehlen/fallback.
* **graph-views**

  * Abdecken: Lifespan-Poolaufbau (psycopg2/SQLAlchemy), Healthz 200 bei erfolgreichem SELECT 1, 503 bei Connection-Refused, Queries inkl. Parametrisierung/Fehlerpfade.
  * DB-Zugriffe strikt mocken; kein echter Postgres.
* **search-api**

  * Abdecken: Healthz, Suche-Endpoint, Validierungsfehler, Leere Ergebnisse, Fehler-Mapping.
* **Test-Infra**

  * Einheitliche pytest-Konfiguration, Coverage-Konfig (omit nur generierte/Setup-Dateien).
  * Fixtures für HTTP-Clients der FastAPI-Apps.
  * Keine doppelten Tests anlegen; bestehende bei API-Änderungen anpassen.

### CLI (cli/it\_cli)

**Ziele:** 100 % Coverage inklusive Fehlerpfade; TUI-Logs ohne Crash.

* Abdecken: Banner/Version-Flag, Konfig-Laden (Pydantic Settings), HTTP-Wrapper, Infra-Kommandos (status/health/logs), Search/Graph/Views-Kommandos (HTTP Aufrufe gemockt), Plugin-Discovery.
* **TUI-Logs-Refactor ist bereits geplant:** Teste die reinen Tail/Follow-Helper (Datei-Tail, Follow-Schleife, Fehlerbehandlung bei fehlenden Dateien). TUI testbar machen, ohne tatsächliche Typer-Option-Objekte zu übergeben (nur echte Werte).
* Respx/httpx-Mock oder äquivalent verwenden.
* Keine Network/Container Abhängigkeit.
* Snapshot-Tests dort sinnvoll, wo Ausgabeformat stabil sein soll (Tables/Panels).

### Frontend (apps/frontend)

**Ziele:** 100 % Jest-Coverage der **eigenen** Quellmodule (UI/Logic), Framework-Boilerplate ignorieren.

* Test-Setup:

  * Jest mit jsdom-Environment, Testing Library, Mocks für Canvas/React-CytoscapeJS (z. B. minimaler Shim/Mock-Module).
  * Coverage-Ignore für Next-Builder, .next/, generierte Typen, rein statische Re-Exports.
* Abdecken:

  * lib/config (Default-Export, Fallbacks), lib/safe (isBrowser, safeLog), hooks/useHealth (OK/Degradationspfade, Retry-Strategie falls vorhanden), Seiten: search, graphx, settings (rendern, Interaktionen, SSR-sichere Zugriffe), Layout-Navigation sichtbar.
  * Tailwind-Styles müssen für Tests nicht greifen; Komponenten rendern ohne CSS-Abhängigkeiten.
* Vorhandene Tests, die an jsdom-Canvas scheiterten, auf Mocks umstellen.
* „React.Children.only …“ Fehler durch Testarrange beheben (einzelnes Root-Element, Portal-Mocks, falls nötig).

### CI & Qualitätstore

* GitHub Actions/ähnlich: Zwei Jobs (Python, Frontend) parallel; beide mit Coverage-Bericht (XML/LCOV) und **Fail bei <100 %**.
* Artefakte: coverage.xml (Python), lcov.info (Frontend).
* Lint/Typecheck-Schritte integrieren (ruff/flake8/mypy optional; eslint/tsc optional), aber nicht blocker für 100 % Aufgabe, sofern bereits konfiguriert.

### Akzeptanzkriterien (Repository-weit)

1. „pytest …“ liefert 100 % Coverage in allen Python-Paketen (inkl. Fehlerpfade).
2. „npm test“ im Frontend liefert 100 % der definierten Quellpfade; Canvas/Cytoscape-Nutzung per Mocks stabil.
3. CI bricht ab, wenn irgendein Teilprojekt <100 % erreicht.
4. Re-Run dieses Prompts erzeugt **keine** neuen doppelten Tests oder Konfig-Dateien; es aktualisiert nur bei Abweichungen.
5. Kurze Doku unter docs/ mit „Tests lokal/CI ausführen“, „Coverage-Ziele“, „Mock-Strategien“ und „No-Network-Policy für Unit-Tests“.

### Erwartete Änderungsorte (ohne Snippets)

* services/\*/tests/... (neue/aktualisierte Tests, Fixtures, Mocks)
* cli/it\_cli/tests/... (Banner/Version/Config/Infra/Logs/TUI-Helper)
* apps/frontend/jest-Konfig, setupTests, **mocks**/\*, Tests für pages, lib, hooks, components
* Projektweite Coverage-Konfigs, CI-Workflows, kurze Doku in docs/

**Bitte alle Änderungen in feature-Branches mit Präfix „codex/coverage-100“ pro Teilprojekt bündeln, PRs erstellen und sicherstellen, dass wiederholtes Anwenden dieses Auftrags keine Duplikate erzeugt.**
