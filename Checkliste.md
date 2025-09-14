# ✅ Dev Setup Checkliste

Kurzanleitung für ein lokales End-to-End Setup von InfoTerminal (MVP).

## Schritte

1. **Services starten**
   - `make dev-up`
     - Startet OpenSearch, Neo4j, Postgres, Backend-Services und Frontend.
   - Optional separat: `services/nlp-service/dev_run.sh`

2. **Healthchecks prüfen**
   - `scripts/dev_health.sh`

3. **Seed-Daten laden**
   - `make seed-graph`
   - `make seed-demo` *(PDFs → Aleph, CSV → Postgres)*

4. **Policies testen**
   - `make opa-test`

5. **Optional: dbt Modelle ausführen**
   - `make dbt-all`

6. **Legacy NLP prüfen**
   - Sucht/ersetzt alte nlp-service Aufrufe
   - Frontend Tool-Calls → /api/plugins
   - grep direkte Hosts

Weitere Details siehe [TODO-Index](docs/dev/roadmap/TODO-Index.md).
