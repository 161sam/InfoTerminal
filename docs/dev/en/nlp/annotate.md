# Document Annotation API

The `doc-entities` service exposes a combined `/annotate` endpoint.

```
POST /annotate {text, lang?, do_summary?}
```

It returns HTML highlights, the raw entity list, optional summary and an
identifier. Entities can optionally be forwarded to the graph view via
`POST /link-entities` when `GRAPH_VIEWS_LINK_URL` is configured.
