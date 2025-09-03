# doc-entities Service

The `doc-entities` service extracts named entities from documents and
resolves them against the knowledge graph. This version contains the
initial data model and placeholder APIs for the upcoming resolver.

## Setup

```bash
python -m pip install -e .
cp .env.example .env
```

Run the service:

```bash
uvicorn app:app --reload --port 8006
```

## API

### `POST /annotate`
Store a document and its entities using the NLP service. Each entity is
returned with a `resolution` field which is currently marked as
`pending`.

### `GET /docs/{id}`
Retrieve the stored document and its entities.

### `POST /resolve/{doc_id}`
Placeholder endpoint for triggering entity resolution for a document.
Currently returns HTTP 501.

### `POST /resolve/entity/{entity_id}`
Placeholder endpoint for resolving a single entity. Also returns HTTP
501.

## Environment Variables

See [`.env.example`](.env.example) for available settings.

## Migrations

SQL migrations are located in the `migrations/` directory. Apply them
using your preferred PostgreSQL migration tool:

```bash
psql "$DATABASE_URL" -f migrations/001_init.sql
```
