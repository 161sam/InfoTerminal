- ACTION: mkdir
  DST: docs/architecture/diagrams
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/guides
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/research
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/roadmap/v0.3-plus
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/integrations
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/presets/waveterm
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/architecture/diagrams
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/guides
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/research
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/roadmap/v0.3-plus
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/integrations
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/presets/waveterm
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/architecture/diagrams
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/guides
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/research
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/dev/roadmap/v0.3-plus
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/integrations
  WHY: ensure structure
- ACTION: mkdir
  DST: docs/presets/waveterm
  WHY: ensure structure
- ACTION: move
  SRC: docs/testing.md
  DST: docs/dev/guides/testing.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/RAG-Systeme.md
  DST: docs/dev/guides/rag-systems.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Frontend-Modernisierung.md
  DST: docs/dev/guides/frontend-modernization.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Frontend-Modernisierung_Setup-Guide.md
  DST: docs/dev/guides/frontend-modernization-setup-guide.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/ROADMAPv0.1.0.md
  DST: docs/dev/roadmap/v0.1-overview.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/dev/Release-Planv0.2-v1.0.md
  DST: docs/dev/roadmap/v0.2-overview.md
  WHY: structure
  DIFF: moved
- ACTION: move
  SRC: docs/runbooks/RUNBOOK-obs-opa-secrets.md
  DST: docs/runbooks/obs-opa-secrets.md
  WHY: naming
  DIFF: moved
- ACTION: merge
  SRC: docs/runbooks/RUNBOOK-stack.md & docs/OPERABILITY.md
  DST: docs/runbooks/stack.md
  WHY: runbooks
  DIFF: merged
