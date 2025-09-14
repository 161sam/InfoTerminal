# Dossier-Lite

The graph-views service exposes a `POST /dossier` endpoint that renders a markdown report from selected documents, nodes and edges. When PDF support is available (`IT_DOSSIER_PDF=1` with WeasyPrint), the response also includes a `pdfUrl` for download.

## Example

```bash
curl -sS http://localhost:8403/dossier \
  -H 'Content-Type: application/json' \
  -d '{"title":"Demo","items":{"docs":["a"],"nodes":["1"],"edges":[]},"options":{"summary":false}}'
```

The web frontend provides a minimal builder at `/dossier` where users can enter items, generate the report and download the result.
