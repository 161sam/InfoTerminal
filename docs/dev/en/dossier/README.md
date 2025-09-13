# Dossier Export

`graph-views` can build simple dossiers from queries and graph selections.

## Endpoint
`POST /dossier` with a payload:
```json
{
  "query": "payments",
  "entities": ["Person:Alice"],
  "graphSelection": {"nodes": ["p1"], "edges": ["e1"]},
  "format": "md"
}
```
`format` may be `md`, `pdf`, or `both`. When `IT_DOSSIER_PDF=1` and WeasyPrint is installed, a PDF is generated in addition to Markdown.
