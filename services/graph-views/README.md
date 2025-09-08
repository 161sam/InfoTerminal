# Graph Views Service

This service exposes graph-related views via FastAPI.

## Development

Create a virtual environment and install the package in editable mode:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

Graph-Views initialisiert Postgres asynchron via `asyncpg`; die Abhängigkeit ist Bestandteil des Pakets.

For running tests install the dev requirements:

```bash
pip install -r requirements-dev.txt
```

## Tests & Coverage

Run the test suite locally without Docker:

```bash
pytest -q
```

Coverage configuration lives in `.coveragerc`. Test files, samples and other
non-service code are excluded so the reported percentage focuses on the
service implementation. All database interactions are mocked; tests should run
without a Neo4j instance. If coverage is slightly below the threshold, add
targeted tests for edge cases such as write guards or `401` responses.

Start the service during development with:

```bash
IT_FORCE_READY=1 uvicorn app:app --port 8403 --reload
```

## CSV → Neo4j (Demo)

**ENV (local dev):**

```
GV_ALLOW_WRITES=1
NEO4J_URI=bolt://it-neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=test12345
NEO4J_DATABASE=neo4j
```

**CSV laden (Script, idempotent):**

```bash
python services/graph-views/samples/load_csv.py
```

**API-Variante (Bulk):**

```bash
curl -sS -X POST "http://localhost:8403/graphs/load/csv?write=1" \
 -H "Content-Type: application/json" \
 -d '{"rows":[{"id":"alice","name":"Alice","knows_id":"bob"},{"id":"bob","name":"Bob","knows_id":"carol"},{"id":"carol","name":"Carol"}]}'
```

**Cypher testen:**

```bash
# Constraint (write=1)
curl -sS -X POST "http://localhost:8403/graphs/cypher?write=1" \
 -H "Content-Type: application/json" \
 -d '{"stmt":"CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE","params":{}}'

# Abfrage
curl -sS -X POST "http://localhost:8403/graphs/cypher" \
 -H "Content-Type: application/json" \
 -d '{"stmt":"MATCH (p:Person) RETURN p.id AS id, p.name AS name ORDER BY id LIMIT 10","params":{}}'

## v0.2 Polish

### Unified Responses

All endpoints return a common envelope:

```json
{ "ok": true, "data": {...}, "counts": {"nodes":0, "relationships":0}, "error": null }
```

Example:

```bash
curl -sS "http://localhost:8403/graphs/view/ego?label=Person&key=id&value=alice"
```

### Write Rate-Limit

Enable per-IP write limits with `GV_RATE_LIMIT_WRITE` (e.g. `20/minute`). On
exceeding the limit the service responds with **429** and
`error.code="rate_limited"` plus a `Retry-After` header.

### Audit Log

Set `GV_AUDIT_LOG=1` to emit JSON audit events for write requests on STDOUT:

```json
{"ts": 1690000000000, "route": "/graphs/cypher", "ip": "127.0.0.1", ...}
```

### Export Dossier

`GET /graphs/export/dossier` builds an ego view and returns a JSON dossier:

```bash
curl -sS "http://localhost:8403/graphs/export/dossier?label=Person&key=id&value=alice&depth=2"
```
```

**Ego-View Beispiel:**

```bash
curl -sS "http://localhost:8403/graphs/view/ego?label=Person&key=id&value=alice&depth=2&limit=50"
```

## Write-Auth (Basic)

Optionaler Basic-Auth-Schutz für schreibende Endpunkte. Wenn `GV_BASIC_USER` und
`GV_BASIC_PASS` gesetzt sind, müssen Anfragen mit `?write=1` entsprechende
Credentials mitsenden:

```bash
curl -u user:pass -X POST "http://localhost:8403/graphs/cypher?write=1" \
  -H "Content-Type: application/json" \
  -d '{"query":"CREATE (:Person {id:\"x\"})"}'
```

## Neo4j-Verbindung & Retry

Der Dienst nutzt eine zentrale Driver-Factory (`neo.py`) mit einfacher
Retry-Logik bei transienten Verbindungsfehlern. Relevante ENV-Variablen:

```
NEO4J_URI
NEO4J_USER
NEO4J_PASSWORD
NEO4J_DATABASE
NEO4J_MAX_CONN_LIFETIME
```

## Troubleshooting: Neo4j connection refused

Wenn `connection refused` auftritt:

1. Stimmt URI/Host/Port? (`--uri` Parameter nutzen)
2. Richtiger Datenbankname und Credentials?
3. Service läuft und erreichbar?

Beispiel für das CSV-Loader-Script mit Overrides:

```bash
python services/graph-views/samples/load_csv.py --uri bolt://localhost:7687 \
  --csv my.csv
```

## Smoke-Checks

```bash
export GV_ALLOW_WRITES=1
export GV_BASIC_USER=dev
export GV_BASIC_PASS=devpass
export GV_RATE_LIMIT_WRITE=2/second
export GV_AUDIT_LOG=1
make smoke.gv
```

## Git Remote Hinweis

Falls `git push origin main` fehlschlägt:

```bash
git remote -v
# ggf.
git remote add origin <URL>
```

### Serve & Smoke (ohne Docker)

Start (lokal, uvicorn):
```bash
make gv.serve
```

Smoke-Checks (auto-boot & wait):

```bash
make smoke.gv.up
# ENV optional:
# export GV_ALLOW_WRITES=1 GV_BASIC_USER=dev GV_BASIC_PASS=devpass GV_RATE_LIMIT_WRITE=2/second GV_AUDIT_LOG=1
```

### Robust Smoke (JSON-aware)
Das Script prüft Content-Type und nutzt `jq` nur bei JSON. Ohne `jq` zeigt es die ersten 400 Zeichen des Bodys an.

Start mit Auto-Boot:
```bash
make smoke.gv.up
# oder manuell, wenn Service schon läuft:
BASE=http://localhost:8403 scripts/smoke_graph_views.sh
```
