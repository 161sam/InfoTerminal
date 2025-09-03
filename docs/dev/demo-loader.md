# Demo Loader

Der Demo-Loader füllt lokale Services mit Beispieldaten.
Er ist nur in Entwicklungsumgebungen aktiv, wenn `ALLOW_DEMO_LOADER=1` gesetzt ist.

## Beispielaufruf

```bash
curl -s -X POST http://localhost:3000/api/demo/load \
  -H "Content-Type: application/json" \
  -d '{"ingestAleph":true,"annotate":true}'
```

Die geladenen Dateien und ihre Hashes werden in `data/demo/loaded.json` gespeichert und bei weiteren Läufen übersprungen.
Ein Reset kann per `POST /api/demo/reset` erfolgen.
