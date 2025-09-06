# Search API

FastAPI service providing search over OpenSearch.

## Reranking

Optional semantic reranking using sentence-transformer embeddings can be enabled with environment flags.

### Configuration

| Variable | Default | Description |
|---|---|---|
| `RERANK_ENABLED` | `0` | Activate embedding reranking |
| `RERANK_TOPK` | `50` | Number of BM25 hits to rerank |
| `RERANK_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Model name |
| `RERANK_TIMEOUT_MS` | `800` | Max rerank time before falling back |
| `RERANK_CACHE_TTL_S` | `1800` | Cache TTL for embeddings |

### Example Requests

```bash
curl "http://localhost:8001/search?q=acme&limit=20&rerank=1"
curl -H "X-Rerank: 1" "http://localhost:8001/search?q=acme&limit=20"
```

Reranking blends cosine similarity with BM25 score and is best-effort; if the timeout is exceeded or an error occurs the original order is returned.


## Development

Editable install is supported:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .
```

Run the API via the legacy shim or the package name:

```bash
PYTHONPATH=. IT_FORCE_READY=1 uvicorn app.main:app --port 8401 --reload
# or
uvicorn search_api.app.main:app --port 8401 --reload
```
