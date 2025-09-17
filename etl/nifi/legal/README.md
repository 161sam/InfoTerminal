# NiFi Legal Pipelines (ingest_laws, rag_index)

This directory contains minimal templates to bootstrap legal ingestion.

- ingest_laws_template.xml: Fetch/scrape JSON chunks (paragraph-level) of laws
- rag_index_template.xml: POST JSON chunks to rag-api `/law/index`

Quick start (dev):
- Start NiFi and rag-api (`docker compose --profile nifi up -d` and base compose)
- Import both templates in NiFi UI
- Create a Parameter Context (e.g., `legal-ingest`) and define:
  - `laws.input.dir=/opt/nifi/laws/input`
  - `rag.api.url=http://rag-api:8000`
- Bind the Parameter Context to the instantiated Process Group
- For ingest_laws_watchfolder, drop JSON files with fields `{id,title,paragraph,text,...}` into `laws.input.dir`
- For rag_index_demo, click Run to index the demo JSON
- Use `MergeRecord` if needed to chunk inputs; set `Content-Type: application/json`

Idempotency: rag-api upserts on `id` field.
