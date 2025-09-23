# Installation (Kurzfassung)

1. Repository klonen und `.env`/`.env.local` aus den Beispieldateien ableiten.
2. `pipx install --force ./cli` ausführen, danach `it start -f docker-compose.yml`.
3. Frontend unter `http://localhost:3411` öffnen. Standardmodi:
   - Kernservices (Search, Graph, Views, Doc-Entities) starten automatisch.
   - Optional `--profile observability` oder `AGENTS=1` (Flowise) hinzufügen.
4. Feature-Flags im Frontend über `.env.local` steuern:
   - `NEXT_PUBLIC_FEATURE_AGENT=1` → `/agent` sichtbar.
   - `NEXT_PUBLIC_FEATURE_NLP=1` → `/nlp` aktiv.

Backend-Overrides (Gateway, Doc-Entities) lassen sich über `NEXT_PUBLIC_*` Variablen anpassen. Ohne gesetzte Ziele fällt das Frontend auf lokale Ports (8401/8402/8403/8406) zurück.
