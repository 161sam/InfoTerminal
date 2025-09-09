# Search UI

The search page is available at `/search` and supports multiple URL parameters which make search results shareable.

## Parameters

- `q` – free text query
- `entity` – repeated param to filter entity types, e.g. `entity=Person&entity=Organization`
- `filter.<facet>` – comma separated values for a facet (e.g. `filter.source=osint,openbb`)
- `sort` – `relevance` (default), `date_desc` or `date_asc`
- `rerank` – `1` enables embedding reranking
- `page` – page number starting at 1
- `pageSize` – items per page (default 20)

Example:

```bash
/search?q=acme&filter.source=osint&sort=date_desc&rerank=1&page=2
```

The page exposes facet filters with chips, a rerank toggle,
pagination and sort selector.
Each result links to its document detail view and, when available,
to the graph viewer via `/graphx?focus=<node_id>`.

Backend reranking is only active when the `search-api` service runs
with `RERANK_ENABLED=1`.
The UI simply forwards the `rerank=1` parameter or `X-Rerank: 1` header.
