# Dossier Templates & Export UX

The dossier builder now fetches a live template catalogue from the collab-hub
service and surfaces progress feedback while exports are running.

## Template Catalogue

- **Endpoint**: `GET /api/collab/dossier/templates`
- **Source**: Proxies to `collab-hub` (`/dossier/templates`) and returns the
  available templates with descriptions, sections, and supported formats.
- **Current Templates**:
  - `standard` – "Standard Investigation" with executive summary, key entities,
    references, and analyst notes; recommended for full hand-overs.
  - `brief` – "Executive Brief" with snapshot, top entities, and immediate
    actions; optimised for leadership updates.

The frontend template selector renders these metadata cards and lets analysts
preview the recommended structure before triggering an export.

## Export Flow & Progress

- **Endpoint**: `POST /api/collab/dossier/export`
- **Feedback**: Frontend subscribes to WebSocket broadcasts (or falls back to
  polling/simulation) and renders a modal with a live progress bar, history, and
  success/error states.
- **Smoke**: Export completion triggers notifications and automatically closes
  the modal once the job finishes.

The same progress system is shared with plugin runs and media forensic video
analysis, ensuring consistent feedback for long-running tasks.
