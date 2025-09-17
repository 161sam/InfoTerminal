# rag-api (Legal/Compliance Retrieval)

FastAPI service providing:
- `/law/retrieve?q=...` – retrieve law paragraphs (OpenSearch index `${RAG_OS_INDEX}`)
- `/law/context?entity=...` – relevant laws for an entity via Neo4j links, fallback to text search
- `/law/index` – idempotent upsert of a law paragraph
- `/graph/law/upsert` – upsert Law node and `APPLIES_TO` relations (LEGAL-2)

Health:
- `/healthz`, `/readyz`

Env (defaults):
- `OS_URL=http://opensearch:9200`
- `RAG_OS_INDEX=laws`
- `NEO4J_URI=bolt://neo4j:7687`, `NEO4J_USER`, `NEO4J_PASSWORD`

Compose:
- Exposed on host `${IT_PORT_RAG_API:-8622}`

Idempotent bootstrap:
- On first run, the OpenSearch index is created automatically with a basic mapping.
- Neo4j constraints are created when calling `/graph/law/upsert`.

Example:
```bash
curl "http://localhost:8622/law/retrieve?q=%C2%A723%20ArbSchG"
curl "http://localhost:8622/law/context?entity=Automotive"
```

