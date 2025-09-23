# CLI Inventory - Comprehensive Analysis

_Updated on 2025-09-21 by Claude for CLI/API Parity Project Phase 1_

## Executive Summary

**CLI Coverage:** 8 commands implemented (~20% of API functionality)  
**Missing Commands:** 80%+ of API endpoints lack CLI equivalents  
**Implementation:** Typer-based, pipx installable as 'it'  
**Config:** ~/.config/infoterminal/config.toml + ENV overrides

**Critical Gap:** Only 8 of 280+ API endpoints have CLI coverage

## Current CLI Architecture

### CLI Tool Structure
```
it_cli/
├── __main__.py          # Entry point
├── root.py              # Main Typer app
├── config.py            # Configuration management
├── http.py              # HTTP client utilities
├── commands/            # Command implementations
│   ├── analytics.py     # ✅ 1 command
│   ├── fe.py           # ✅ 3 commands (dev ops)
│   ├── graph.py        # ✅ 4 commands
│   ├── infra.py        # ✅ Infrastructure commands
│   ├── search.py       # ✅ 1 command
│   ├── settings.py     # ✅ 1 command
│   ├── tui.py          # ✅ 1 command
│   └── views.py        # ✅ 1 command
├── renderers/          # Output formatting
└── utils/              # Shared utilities
```

### Configuration System
- **Config File:** `~/.config/infoterminal/config.toml`
- **Environment:** Variables override config
- **Port Discovery:** Uses `scripts/patch_ports.sh` mappings
- **Authentication:** Basic token support

## Implemented Commands (8 total)

### 1. Graph Commands (4/40 endpoints = 10% coverage)

#### `it graph cypher`
- **API Mapping:** `POST /v1/cypher`
- **Service:** graph-api
- **Parameters:** `--query`, `--param`, `--read-only`
- **Output:** JSON results
- **Status:** ✅ Working

#### `it graph neighbors`
- **API Mapping:** `GET /v1/nodes/{id}/neighbors`
- **Service:** graph-api
- **Parameters:** `--node-id`, `--depth`, `--limit`, `--direction`, `--relationship-types`, `--visualize`
- **Output:** JSON results
- **Status:** ✅ Working

#### `it graph shortest-path`
- **API Mapping:** `POST /v1/shortest-path`
- **Service:** graph-api
- **Parameters:** `--source`, `--target`, `--max-length`
- **Output:** JSON results
- **Status:** ✅ Working

#### `it graph ping`
- **API Mapping:** `GET /healthz`
- **Service:** graph-api
- **Parameters:** None
- **Output:** Health status
- **Status:** ✅ Working

**Missing Graph Commands (36):**
- Algorithms: centrality, communities, pagerank
- Analytics: degree, betweenness, node influence
- Geospatial: geocode, entities, heatmap
- Export: graphml, json
- Jobs: status, cancel

### 2. Search Commands (1/15 endpoints = 7% coverage)

#### `it search query`
- **API Mapping:** `POST /search` (legacy)
- **Service:** search-api
- **Parameters:** `--query`, `--sort`, `--limit`, `--chart`
- **Output:** Search results
- **Status:** ⚠️ Uses legacy endpoint

**Missing Search Commands (14):**
- Document management: index, get, delete
- v1 search endpoint
- Audio transcriptions
- Model management

### 3. Analytics Commands (1/? endpoints = Unknown coverage)

#### `it analytics kpis`
- **API Mapping:** `/analytics/kpis`
- **Service:** views-api (not in API inventory)
- **Parameters:** `--chart`
- **Output:** KPI chart
- **Status:** ⚠️ Service not documented

### 4. Views Commands (1/? endpoints = Unknown coverage)

#### `it views query`
- **API Mapping:** `/query`
- **Service:** views-api (not in API inventory)
- **Parameters:** `--sql`, `--limit`
- **Output:** SQL results
- **Status:** ⚠️ Service not documented

### 5. Settings Commands (1 command)

#### `it settings show`
- **API Mapping:** None (local config)
- **Service:** Local configuration
- **Parameters:** None
- **Output:** Current config JSON
- **Status:** ✅ Working

### 6. Frontend Commands (3 commands)

#### `it fe dev`
- **API Mapping:** None (local command)
- **Service:** Frontend build system
- **Parameters:** None
- **Output:** Dev server
- **Status:** ✅ Working

#### `it fe build`
- **API Mapping:** None (local command)
- **Service:** Frontend build system
- **Parameters:** None
- **Output:** Production build
- **Status:** ✅ Working

#### `it fe test`
- **API Mapping:** None (local command)
- **Service:** Frontend build system
- **Parameters:** None
- **Output:** Test results
- **Status:** ✅ Working

### 7. TUI Commands (1 command)

#### `it tui run`
- **API Mapping:** None (local TUI)
- **Service:** Terminal UI
- **Parameters:** None
- **Output:** Interactive TUI
- **Status:** ✅ Working

## Missing Command Groups (80%+ Coverage Gaps)

### 🔴 Critical Missing: Authentication (0/51 endpoints)
**Priority:** CRITICAL - No auth management via CLI

**Missing Commands:**
```bash
it auth login                    # POST /v1/auth/login
it auth logout                   # POST /v1/auth/logout  
it auth whoami                   # GET /v1/auth/me
it auth register                 # POST /v1/auth/register
it auth change-password          # POST /v1/auth/change-password
it auth setup-mfa               # POST /v1/auth/mfa/setup
it users list                   # GET /v1/users
it users create                 # POST /v1/users
it users get <id>               # GET /v1/users/{id}
it users update <id>            # PUT /v1/users/{id}
it users delete <id>            # DELETE /v1/users/{id}
it users activate <id>          # POST /v1/users/{id}/activate
it users deactivate <id>        # POST /v1/users/{id}/deactivate
it roles list                   # GET /v1/roles
it roles create                 # POST /v1/roles
it roles get <id>               # GET /v1/roles/{id}
it roles assign <user> <role>   # POST /v1/users/{id}/assign-roles
```

### 🔴 Critical Missing: NLP & Document Processing (0/19 endpoints)
**Priority:** CRITICAL - No document analysis via CLI

**Missing Commands:**
```bash
it nlp extract <file>           # POST /v1/extract/entities
it nlp summarize <file>         # POST /summary  
it nlp ner <text>               # POST /ner
it resolve entities <file>      # POST /match
it resolve dedupe <file>        # POST /dedupe
it xai explain <text>           # POST /explain/text
it docs annotate <file>         # POST /v1/documents/annotate
```

### 🔴 Critical Missing: Verification (0/11 endpoints)  
**Priority:** CRITICAL - No claim verification via CLI

**Missing Commands:**
```bash
it verify extract-claims <text>  # POST /verify/extract-claims
it verify image <file>          # POST /verify/image
it verify similarity <f1> <f2>  # POST /verify/image-similarity
it verify stats                 # GET /verify/stats
```

### 🔴 Critical Missing: Agents & Workflows (0/26 endpoints)
**Priority:** HIGH - No agent interaction via CLI

**Missing Commands:**
```bash
it agents list                  # GET /workflows
it agents chat <msg>            # POST /chat
it agents tools                 # GET /tools
it agents execute <tool> <args> # POST /tools/execute
it plugins list                 # GET /plugins
it plugins run <name> <args>    # POST /execute
it plugins status               # GET /plugins/state
```

### 🔴 Missing: Media & Forensics (0/11 endpoints)
**Priority:** HIGH - No forensic analysis via CLI

**Missing Commands:**
```bash
it forensics ingest <file>      # POST /ingest
it forensics verify <file>      # POST /verify
it forensics receipt <hash>     # GET /receipt/{sha256}
it media analyze <image>        # POST /image/analyze
it media compare <img1> <img2>  # POST /image/compare
it media formats               # GET /formats
```

### 🟡 Missing: Operations & Infrastructure (0/42 endpoints)
**Priority:** MEDIUM - No ops management via CLI

**Missing Commands:**
```bash
it ops stacks list             # GET /ops/stacks
it ops stack status <name>     # GET /ops/stacks/{name}/status
it ops stack up <name>         # POST /ops/stacks/{name}/up
it ops stack down <name>       # POST /ops/stacks/{name}/down
it ops stack restart <name>    # POST /ops/stacks/{name}/restart
it ops stack logs <name>       # GET /ops/stacks/{name}/logs
it cache get <key>             # GET /cache/{key}
it cache set <key> <value>     # POST /cache
it cache del <key>             # DELETE /cache/{key}
it cache stats                 # GET /cache/stats
```

### 🟡 Missing: Collaboration & Feedback (0/13 endpoints)
**Priority:** MEDIUM - No collaboration via CLI

**Missing Commands:**
```bash
it collab tasks list           # GET /tasks
it collab tasks create         # POST /tasks  
it collab tasks update <id>    # POST /tasks/{id}/update
it collab tasks delete <id>    # DELETE /tasks/{id}
it feedback post <msg>         # POST /feedback
it feedback list               # GET /feedback
it feedback stats              # GET /feedback/stats
```

### 🟡 Missing: Performance & Monitoring (0/5 endpoints)
**Priority:** LOW - Basic monitoring via CLI

**Missing Commands:**
```bash
it perf summary <service>      # GET /metrics/{service}/summary
it perf alerts                 # GET /alerts
it perf metrics <service>      # GET /metrics/{service}
```

## CLI Standards Analysis

### ✅ Current Standards (Implemented)
- **Framework:** Typer for modern CLI UX
- **Installation:** pipx installable package
- **Configuration:** TOML + ENV override pattern
- **Help System:** Auto-generated from Typer

### ❌ Missing Standards (Critical Gaps)

#### Output Formatting
- **Missing:** `--json`, `--yaml`, `--table` standardization
- **Current:** Mostly JSON-only output
- **Need:** Consistent rendering across all commands

#### Error Handling  
- **Missing:** Standard error envelope parsing
- **Current:** Basic HTTP error display
- **Need:** Parse API Error-Envelope format

#### Exit Codes
- **Missing:** Consistent exit code strategy
- **Current:** Basic success/failure
- **Need:** Standard UNIX exit codes

#### Authentication
- **Missing:** Token management, session handling
- **Current:** Basic token support
- **Need:** Login/logout workflow, token refresh

#### Progress & Feedback
- **Missing:** Progress bars, verbose output
- **Current:** Minimal feedback
- **Need:** Rich progress indication

## CLI Implementation Strategy

### Phase 2.3: Core Command Groups (4 weeks)

#### Week 1: Authentication Foundation
```bash
it auth login/logout/whoami
it users create/list/get/update/delete  
it roles list/create/assign
```

#### Week 2: Document & NLP Processing
```bash
it nlp extract/summarize/ner
it verify extract-claims/image/stats
it docs annotate/index
```

#### Week 3: Agents & Workflows
```bash
it agents list/chat/tools/execute
it plugins list/run/status
it workflows list/trigger
```

#### Week 4: Operations & Infrastructure
```bash
it ops stack up/down/status/logs
it cache get/set/del/stats
it perf summary/alerts/metrics
```

### Phase 2.4: Standards Implementation (2 weeks)

#### Week 5: Output & Error Handling
- Implement `--json/--yaml/--table` for all commands
- Standard error envelope parsing
- Consistent exit codes
- Progress bars and verbose output

#### Week 6: Advanced Features
- Configuration validation
- Health check integration
- Batch operations
- Shell completion

## Definition of Done: CLI Parity

### Quantitative Targets
- **Coverage:** 95%+ of API endpoints have CLI equivalents
- **Commands:** 80+ commands across 15+ groups
- **Output:** All commands support --json/--yaml/--table
- **Error Handling:** All commands parse Error-Envelope format
- **Exit Codes:** UNIX-standard exit codes for all scenarios

### Qualitative Targets
- **Discoverability:** Comprehensive help system
- **Usability:** Intuitive command structure and naming
- **Consistency:** Uniform patterns across all commands
- **Performance:** <1s startup time for all commands
- **Reliability:** Graceful error handling and recovery

**Total Estimated Effort:** 6 weeks for complete CLI parity across all 280+ API endpoints.
