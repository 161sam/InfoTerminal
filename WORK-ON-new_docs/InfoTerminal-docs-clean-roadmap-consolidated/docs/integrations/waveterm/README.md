# WaveTerm Integration
---

super — hier sind **alle repo-fertigen Dateien** für die WaveTerm-Kompatibilität. Du kannst sie 1:1 unter den jeweiligen Pfaden ablegen.

---

### `docs/waveterm/README.md`

```markdown
# WaveTerm Integration (Open-Source Terminal)

> Ziel: WaveTerm als Pro-Workspace in InfoTerminal nutzen **und** InfoTerminal (CLI/Frontend) nahtlos in WaveTerm einbinden.
> Drei Pfade: (1) WaveTerm **embedded** in InfoTerminal, (2) InfoTerminal als **WaveTerm-Plugin**, (3) optionale **IPC/Job-Brücke**.

---

## Architekturüberblick

```

WaveTerm <plugin> ─┬─ Command Adapter (exec it, call APIs)
├─ Panel Adapter (embeds: /search, /graphx, dossier preview)
└─ Job Adapter (POST /api/jobs, artifacts watcher)

InfoTerminal ──────┬─ wave-plugin (embedded webview /terminal)
├─ agent-gateway + tool-adapter (search/graph/rag/verify)
├─ artifacts svc (PUT/GET artifacts)
└─ bundle/export svc (AppFlowy/AFFiNE kompatibel)

```

**Auth & Security**
- OIDC/JWT zwischen WaveTerm↔InfoTerminal (`Authorization: Bearer …`)
- OPA Policies: Tool-Allowlist, Export-Gates, Rate-Limits
- Sandbox-Runtime: gVisor/Kata für Terminal-Sessions (Default **no-net**, Egress via Gateway)

---

## Pfad A — WaveTerm **embedded** in InfoTerminal
- UI-Tab `/terminal` lädt WaveTerm (sandboxed)
- Profile-Picker (journalism/compliance/crisis/…)
- Actions „**Send to WaveTerm**“: übergeben Queries/Case-Kontext an Shell

**Konfig:** [`docs/waveterm/embed.yaml`](embed.yaml)

---

## Pfad B — InfoTerminal als **WaveTerm-Plugin**
- Command Palette: `it up`, `it export …`, `it query …`
- Panels: `/search`, `/graphx`, Dossier-Preview (MD/SVG live)
- Live-Artefakte: Workdir `WT_WORKSPACE/out` wird gerendert

**Manifest:** [`docs/waveterm/it-plugin.json`](it-plugin.json)

---

## Pfad C — IPC/Jobs (optional)
- WaveTerm stößt Jobs an: `POST /api/jobs` (z. B. „export_dossier“, „graph_export“)
- Ergebnisse als Artefakte im Workspace; Previews in Panels

**Spezifikation:** [`docs/api/jobs.md`](../api/jobs.md)

---

## Preset-Workspaces
Beispiele unter [`docs/waveterm/presets/`](presets/) (Journalism, Compliance, Crisis):
- vorkonfigurierte Pakete/Aliases
- Recording (asciinema) optional, PII-Redaktion
- Limits (CPU, RAM), Egress-Policy

---

## Sicherheit & Governance
- **Least-Privilege**: Profile definieren Tool-Allowlist & erlaubte Hosts/Ports
- **Vault**: JWT/Token via short-lived leases, nie in Klartext speichern
- **OPA**: Policies in `policies/waveterm.rego` (Beispiele beiliegend)
- **Recording**: Opt-in, Hashes → Dossier-Appendix (Chain-of-Custody)

---

## Quickstart

1) **InfoTerminal UI** → Tab **Terminal** (lädt WaveTerm, siehe `embed.yaml`)
2) **WaveTerm** → Plugin „InfoTerminal Integration“ installieren (siehe `it-plugin.json`)
3) **Run**: `it up` → `/search` Panel öffnen → „Send to WaveTerm“ auf eine Suche → `it export dossier …` im Terminal

---

## Tests & SLOs
- **Hermetic Workspaces** in CI: Snapshots von Artefakten vergleichen
- **Session QA**: asciinema validieren, PII-Redaktion prüfen
- **SLO**: Panel-Latenz < 1.5s, Job Completion p95 < 60s (kleine Dossiers)
```

---

### `docs/waveterm/it-plugin.json`

```json
{
  "id": "infoterminal.core",
  "title": "InfoTerminal Integration",
  "version": "0.1.0",
  "description": "WaveTerm-Plugin: InfoTerminal CLI-Kommandos, Panels und Artefakt-Previews.",
  "commands": [
    { "id": "it.up", "title": "Start Infra", "exec": "it up" },
    { "id": "it.down", "title": "Stop Infra", "exec": "it down" },
    { "id": "it.status", "title": "Status", "exec": "it status --format table" },
    { "id": "it.query", "title": "Search Query", "exec": "it query --q '${input:q}'" },
    { "id": "it.export.dossier", "title": "Export Dossier", "exec": "it export dossier --template ${input:template} --data ${input:data} --out ${env:WT_WORKSPACE}/out" },
    { "id": "it.export.graph", "title": "Export Graph (Mermaid+SVG)", "exec": "it export graph --case ${input:case} --formats mermaid,svg --out ${env:WT_WORKSPACE}/out/graphs" }
  ],
  "panels": [
    { "id": "it.search", "title": "InfoTerminal Search", "type": "web", "url": "http://localhost:3411/search", "sso": "oidc" },
    { "id": "it.graphx", "title": "GraphX", "type": "web", "url": "http://localhost:3411/graphx", "sso": "oidc" },
    { "id": "it.dossier.preview", "title": "Dossier Preview", "type": "markdown", "path": "${env:WT_WORKSPACE}/out/index.md" },
    { "id": "it.graph.preview", "title": "Graph SVG", "type": "image", "path": "${env:WT_WORKSPACE}/out/graphs/graph.svg" }
  ],
  "env": {
    "IT_API": "http://localhost:3410",
    "WT_PROFILE": "journalism"
  },
  "permissions": {
    "fs": { "paths": ["${env:WT_WORKSPACE}/out"], "write": true },
    "network": { "allow": ["localhost:3410", "localhost:3411"], "deny": ["*"] }
  }
}
```

---

### `docs/waveterm/embed.yaml`

```yaml
id: waveterm.embed
title: "WaveTerm Workspace"
type: webview
url: "http://localhost:7676"  # WaveTerm Web-UI
sandbox:
  allow_scripts: false
  allow_same_origin: false
  allow_popups: false
profiles:
  default: journalism
  allowed: [journalism, compliance, crisis, disinfo, economic]
security:
  container_runtime: "gvisor"
  egress: "proxy"     # journalism/disinfo → tor+vpn
  policy: "policies/waveterm.rego"
bindings:
  # optional: Case-Folder ReadOnly Mount
  - source: "/var/infoterminal/cases/${CASE_ID}"
    target: "/home/wt/cases/${CASE_ID}"
    mode: "ro"
```

---

### `docs/waveterm/presets/journalism.yaml`

```yaml
name: journalism
shell: bash
packages: [infoterminal-cli, jq, yq, exiftool, imagemagick]
aliases:
  itq: "it query --q"
  itd: "it export dossier"
paths:
  case_dir: "${HOME}/cases/${CASE_ID}"
recording:
  mode: opt_in
  tool: asciinema
  redact_pii: true
limits:
  network: "egress-gateway"   # via IT egress
  cpu: "2"
  mem: "4Gi"
env:
  IT_API: "http://localhost:3410"
  IT_UI: "http://localhost:3411"
```

---

### `docs/waveterm/presets/compliance.yaml`

```yaml
name: compliance
shell: bash
packages: [infoterminal-cli, jq, yq, exiftool, pdfid, yara]
aliases:
  check: "it query --domain legal --q"
  report: "it export dossier --template docs/dossiers/compliance_risk_report.md.tmpl"
recording:
  mode: opt_in
  tool: asciinema
limits:
  network: "egress-proxy"
  cpu: "4"
  mem: "8Gi"
env:
  IT_API: "http://localhost:3410"
```

---

### `docs/waveterm/presets/crisis.yaml`

```yaml
name: crisis
shell: bash
packages: [infoterminal-cli, jq, yq, exiftool]
aliases:
  geo: "it query --domain geo --q"
  crisis_dossier: "it export dossier --template docs/dossiers/humanitarian_crisis_report.md.tmpl"
recording:
  mode: off
limits:
  network: "egress-tor-vpn"
  cpu: "2"
  mem: "4Gi"
env:
  IT_API: "http://localhost:3410"
```

---

### `docs/api/jobs.md`

````markdown
# Job API (WaveTerm ↔ InfoTerminal)

Base: `/api/jobs` • Auth: **OIDC Bearer JWT** • Errors: RFC7807

## POST /api/jobs
Queue Job (z. B. Export, Graph, Analyse).

**Request**
```json
{
  "type": "export_dossier",
  "params": { "template": "docs/dossiers/compliance_risk_report.md.tmpl", "data": "cases/123.json" },
  "artifacts_dir": "/workspace/out",
  "timeout_ms": 60000
}
````

**Response**

```json
{ "job_id": "job_01H...", "status": "queued" }
```

## GET /api/jobs/{id}

Status & Artefakte

```json
{
  "job_id": "job_01H...",
  "status": "running|succeeded|failed",
  "logs": ["..."],
  "artifacts": [
    { "path": "/workspace/out/index.md", "sha256": "…" },
    { "path": "/workspace/out/graphs/graph.svg", "sha256": "…" }
  ]
}
```

## Fehlercodes

* 400 Schema/Param-Fehler
* 401/403 Auth/Policy (RBAC/OPA)
* 409 Limits (Rate/Budget/Docs)
* 429 Throttle
* 5xx Adapter/Backend

## Policies (Beispiele)

* Export nur wenn `classification in ["PUBLIC","INTERNAL"]`
* MaxDocs/MaxTokens pro Job-Typ
* Artefakt-Pfade nur unter `WT_WORKSPACE`

````

---

### `policies/waveterm.rego`
```rego
package waveterm.policy

default allow = false

# Eingehende Job-Requests
allow {
  input.kind == "job"
  valid_job_type
  allowed_classification
  within_limits
}

valid_job_type {
  input.job.type == "export_dossier"
} else {
  input.job.type == "export_graph"
} else {
  input.job.type == "run_query"
}

allowed_classification {
  # Dossier-Klassifikation muss erlaubt sein (PUBLIC/INTERNAL); CONFIDENTIAL/RESTRICTED default verboten
  not input.job.params.classification
  # ohne Klassifikation: strengere Gate → nur PUBLIC
  input.job.params.classification == "PUBLIC"
} else {
  input.job.params.classification == "INTERNAL"
}

within_limits {
  # Beispiel-Limits
  input.job.limits.max_docs <= 50
  input.job.limits.max_tokens <= 6000
}

# WaveTerm FS Schreibpfad beschränken
allow_fs_write {
  input.kind == "fs"
  startswith(input.path, input.env.WT_WORKSPACE)
}
````

---

### `docs/n8n/waveterm_run.md`

````markdown
# n8n: WaveTerm Run Node

## Zweck
Kommandos in WaveTerm-Workspaces aus n8n orchestrieren (Ingest → Analyse → Export).

## Inputs
```json
{
  "workspace": "/workspaces/case-123",
  "command": "it export dossier --template docs/dossiers/journalism_short.md.tmpl --data cases/123.json --out out/",
  "timeoutMs": 60000
}
````

## Output

* `exit_code`, `stdout`, `stderr`
* optionale Artefakt-Liste (aus `/out`)

## Fehler

* `timeout` → Retry mit Backoff
* `exit_code != 0` → Fail → Alert

````

---

### `docs/nifi/WaveTermInvoker.md`
```markdown
# NiFi Processor: WaveTermInvoker

## Properties
- `Workspace Path` (string, required)
- `Command` (string template)
- `Timeout Ms` (int, default 60000)
- `WT URL` (optional, falls HTTP-Adapter)

## Flow
1) Liest FlowFile JSON (Case-Kontext)
2) Rendert Command Template (z. B. `it query --q "${q}"`)
3) Führt Kommando im Workspace aus (lokal/HTTP)
4) Schreibt Artefakt-Pfad/Hashes ins FlowFile Attribut

## Relationships
- `success`, `failure`, `retry`
````

---

### **TODO-Index – Ergänzung**

> Hänge an `docs/TODO-Index.md` an:

```markdown
## 29. WaveTerm Integration
- [ ] **[WT-EMBED-1]** Webview Tab `/terminal` + SSO (OIDC)
- [ ] **[WT-EMBED-2]** Profiles Loader (journalism/compliance/crisis/…)
- [ ] **[WT-EMBED-3]** “Send to WaveTerm” Actions (+context payload)
- [ ] **[WT-EMBED-4]** Session Recording → Dossier Appendix
- [ ] **[WT-PLUGIN-1]** WaveTerm Plugin Manifest (`it` commands, panels)
- [ ] **[WT-PLUGIN-2]** Dossier/Graph Previews (MD/SVG)
- [ ] **[WT-PLUGIN-3]** Command Palettes & Snippets
- [ ] **[WT-JOBS-1]** `/api/jobs` (queue, artifacts)
- [ ] **[WT-JOBS-2]** n8n Node `waveterm.run`
- [ ] **[WT-JOBS-3]** NiFi Processor `WaveTermInvoker`
- [ ] **[WT-SEC-1]** gVisor/Kata runtime + default no-net
- [ ] **[WT-SEC-2]** OPA policies (tool allowlist, export gates)
- [ ] **[WT-SEC-3]** Vault tokens (short-lived) for CLI/API
- [ ] **[WT-DOC-1]** `docs/waveterm/README.md` (Setup, Profiles, Safety)
- [ ] **[WT-DOC-2]** `docs/waveterm/presets/*.yaml` Beispiele
- [ ] **[WT-DOC-3]** `docs/api/jobs.md` Spezifikation
```

---

Wenn du willst, erweitere ich zusätzlich die **CLI-Doku** um einen Abschnitt *„WaveTerm-Aware Commands“* (z. B. `it waveterm open`, `it waveterm send --cmd …`) – sag einfach Bescheid.
