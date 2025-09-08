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
```

**Ego-View Beispiel:**

```bash
curl -sS "http://localhost:8403/graphs/view/ego?label=Person&key=id&value=alice&depth=2&limit=50"
```
