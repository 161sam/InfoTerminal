# Codex Prompt — Vollständige Testabdeckung (100 %), idempotent

## Kontext & Ziele
Monorepo **InfoTerminal** mit Modulen:
- services/search-api (FastAPI)
- services/graph-api (FastAPI, Neo4j-Driver, Backoff)
- services/graph-views (FastAPI, psycopg2/SQLAlchemy)
- apps/frontend (Next.js 14, Tailwind v4, React)
- cli/it_cli (Typer + Rich, Banner/Version, Infra-Kommandos, TUI-Logs)

Aktueller Stand:
- search-api: 83 % Coverage, Lücken in app/main.py, app/rerank.py, auth.py, obs/otel_boot.py
- graph-api: 60 % Coverage, große Teile ungetestet (auth.py, metrics.py, opa.py, errorpfade)
- graph-views: Tests laufen, Coverage nicht erzwungen, nur Minimaltests vorhanden
- cli: Tests vorhanden, Coverage nicht enforced
- frontend: Tests schlagen fehl (React.Children.only Fehler), Coverage nicht messbar

**Ziel:** 100 % Testabdeckung (Branch + Line) pro Teilprojekt. Integration/E2E optional separat.

**Idempotenz:** Mehrfaches Ausführen darf keine Duplikate oder überschriebenen Konfigurationen erzeugen. Nur fehlende oder fehlerhafte Tests/Konfigs ergänzen.

---

## Allgemeine Leitplanken
1. **Keine Netzwerk-/Container-Abhängigkeit.** Alle externen Systeme strikt mocken (Neo4j, Postgres, HTTP).
2. **Coverage erzwingen.** Python: pytest+coverage, Frontend: Jest mit coverageThreshold 100 %. Generierte Dateien ignorieren.
3. **Idempotenz-Regeln:**
   - Vor Anlage neuer Testdateien prüfen, ob funktional äquivalente existieren.
   - Konfigs vereinheitlichen, nicht duplizieren.
   - Keine venvs im $HOME, nur pipx für CLI oder lokale .venv.
4. **Deterministisch:** Keine sleeps/unseeded Randoms. Zeit/Backoff per Mock steuerbar.
5. **Doku:** Kurzer Guide in docs/ („Tests lokal/CI laufen“, „Coverage-Regeln“, „Mocks/No-Network-Policy“).

---

## Python-Dienste

### search-api
- Abdecken: app/main.py (alle Pfade), app/rerank.py (Suche/Fehlerpfade), auth.py (Valider Token/Invalid), obs/otel_boot.py (OTEL enabled/disabled).
- Healthz, Search, Validierungsfehler, Empty, Fehler-Mapping.

### graph-api
- Lifespan: Neo4j-Driver init + Backoff (alle Versuchspfade, Abbruch nach N).
- Endpoints: /healthz, /ping, /query, /neighbors (Success + Fehler).
- Fehlerpfade: ungültige Cypher, Timeout, falsche Credentials, fehlende ENV.
- Module auth.py, metrics.py, opa.py abdecken.

### graph-views
- Lifespan: DB-Pool Aufbau/Fehler.
- /healthz: 200 bei SELECT 1 ok, 503 bei Connection-Fehler.
- Query-Endpunkte: Success, SQL-Fehler, Parametrisierung.
- Strikt Mocken, kein echter PG.

### Test-Infra
- Zentrale pytest.ini + coverage-Konfig.
- Fixtures für FastAPI-Clients.
- Coverage-Ziel: 100 %, omit nur __init__, setup-Dateien.

---

## CLI (cli/it_cli)
- Banner: sichtbar/unterdrückt (Env IT_NO_BANNER=1, Flag --no-banner), TTY vs Non-TTY.
- Version-Flag, Config-Laden, HTTP-Wrapper, Infra-Kommandos (status/health/logs), Search/Graph/Views Kommandos (HTTP gemockt).
- Plugins: Discovery + Fehlerpfade.
- TUI: Tail/Follow-Helper (Datei fehlt, EOF, Stop).
- respx/httpx Mock einsetzen.
- Snapshot-Tests für Rich-Ausgabe (Tabellen/Panels).

---

## Frontend (apps/frontend)
- Jest mit jsdom, Testing Library.
- Mocks: Canvas/React-CytoscapeJS (Shims).
- Coverage ignoriert: .next/, Next internals, Re-Exports.
- Abdecken:
  - lib/config (Default + Fallbacks)
  - lib/safe (isBrowser, safeLog)
  - hooks/useHealth (ok, degraded, fail, retry)
  - pages/search, graphx, settings (Rendern, SSR-sicher, Interaktionen)
  - Layout-Komponenten (Navigation sichtbar).
- Fix für „React.Children.only“: Test-Arrangements mit einzelner Root-Node, ggf. Portal-Mocks.

---

## CI & Qualitätstore
- GitHub Actions: 2 Jobs parallel (Python, Frontend).
- Coverage-Ziel 100 %, Fail bei Unterschreitung.
- Artefakte: coverage.xml (Python), lcov.info (Frontend).
- Optional: ruff/mypy/eslint/tsc – kein Blocker.

---

## Akzeptanzkriterien
1. pytest aller Dienste: 100 % Coverage inkl. Fehlerpfade.
2. Jest im Frontend: 100 % Coverage der Quellpfade, stabile Mocks.
3. CI bricht ab <100 %.
4. Wiederholtes Ausführen idempotent (keine Duplikate).
5. docs/: Guide zu Tests, Coverage, Mocks, No-Network.

---

## Erwartete Änderungsorte
- services/*/tests/… (neue/erweiterte Tests, Fixtures, Mocks)
- cli/it_cli/tests/… (Banner, Version, Kommandos, TUI)
- apps/frontend/__tests__/…, setupTests, mocks/*
- Coverage-Konfigs, CI-Workflows
- docs/Testing.md oder docs/OPERABILITY.md Abschnitt

---

## Arbeitsweise
- Branches: `codex/coverage-100/<teilprojekt>`
- PRs: Je Teilprojekt. Beschreibung: Coverage-Gaps, neue Tests, Mock-Strategien.
- Tests deterministisch, idempotent.
- Keine Änderungen an User-Umgebungen außerhalb des Projekts.
