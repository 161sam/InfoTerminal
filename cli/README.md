# InfoTerminal CLI

Modular developer command-line interface for the InfoTerminal platform.

## Installation

Install via [pipx](https://pypa.github.io/pipx/) to keep the CLI isolated
without creating virtual environments in your home directory:

```bash
pipx install --force ./cli
```

## Usage

```bash
it --help

# show version
it -V
```

The CLI prints a banner on each run. Set `IT_NO_BANNER=1` to disable it
for scripting or CI environments.

### Lifecycle commands

```bash
it start -f docker-compose.yml -p myproj -d -s neo4j,opensearch
it stop --services neo4j
it restart -n -s neo4j
it rm -n -v --images local
it status -s graph-api,search-api
it logs -s neo4j -F --lines 200
it start -d --profile observability
```

Structured logs can be streamed as NDJSON via:

```bash
it logs --format jsonl -s search-api
```

`infra` ist ein Power-User-Namespace und hält die traditionellen
Subcommands bereit:

```bash
it infra --help   # zeigt up/down/status/logs/start/stop/restart/halt
```

Compose files und Projekt-Namen werden wie folgt ermittelt:
CLI-Flags > Umgebungsvariablen (`IT_COMPOSE_FILE`, `IT_PROJECT_NAME`) >
Auto-Discovery (`docker-compose.yml`, `compose.yml`).

### Flags

| Flag                          | start | stop | rm | restart | status | logs |
| ----------------------------- | :---: | :--: | :-:| :-----: | :----: | :--: |
| `-f`, `--compose-file`        |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✔️ |
| `-p`, `--project-name`        |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✔️ |
| `--env-file`                  |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✔️ |
| `--profile`                   |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✔️ |
| `-s`, `--services`            |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✔️ (req) |
| `-d`, `--detach`              |  ✔️   |  ✖️  | ✖️ |   ✔️    |   ✖️   | ✖️ |
| `--retries` / `--timeout`     |  ✔️   |  ✖️  | ✖️ |   ✔️    |   ✔️   | ✖️ |
| `-n`, `--dry-run`             |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✖️ |
| `-v`, `--verbose`             |  ✔️   |  ✔️  | --verbose | ✔️ | ✔️ | ✖️ |
| `-q`, `--quiet`               |  ✔️   |  ✔️  | ✔️ |   ✔️    |   ✔️   | ✖️ |
| `-v`, `--volumes`             |  ✖️   |  ✖️  | ✔️ |   ✖️    |   ✖️   | ✖️ |
| `--images`                    |  ✖️   |  ✖️  | ✔️ |   ✖️    |   ✖️   | ✖️ |
| `-F`, `--follow` / `--lines`  |  ✖️   |  ✖️  | ✖️ |   ✖️    |   ✖️   | ✔️ |

`rm` nutzt `-v` für Volumes; hier steht `--verbose` nur als Langform zur Verfügung.

Use `--dry-run` to print commands without executing them. `--verbose` shows
subprocess calls, while `--quiet` minimizes output. Set `NO_COLOR=1` or use
`--no-color` to disable colored output.

### Text User Interface

```bash
it ui run

# Key bindings within the TUI:
#   r refresh   u up   d down   s status   l logs   f follow logs
# Die TUI ruft den internen Helper `show_logs` aus `infra` auf –
# Typer-Commands selbst werden im UI nicht verwendet.
```

### Other examples

```bash
it search query "neo4j" --chart
```

### Ports

| Service      | Port |
| ------------ | ---- |
| Prometheus   | 3412 |
| Grafana      | 3413 |
| Alertmanager | 3414 |
| Loki         | 3415 |
| Tempo        | 3416 |

### Quickstart Observability

```bash
it status
docker compose -f docker-compose.observability.yml --profile observability up -d
open http://localhost:3413
open http://localhost:3412
```
