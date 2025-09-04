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

### Infra commands

```bash
# start local stack (alias: `start`)
it infra start -f docker-compose.yml -f docker-compose.override.yml -p myproj -d

# stop services (aliases: `stop`, `halt`)
it infra stop -p myproj --services graph-api --services frontend

# restart with extras
it infra restart --agents --gateway

# check status for selected services
it infra status -s search-api -s graph-api --timeout 5

# tail logs for a service
it infra logs -s graph-api --compose-file docker-compose.yml -p myproj --follow
```

Compose files and project names are discovered in this order of precedence:
CLI flags > environment variables (`IT_COMPOSE_FILE`, `IT_PROJECT_NAME`) >
auto-discovery (`docker-compose.yml`, `compose.yml`).

Use `--dry-run` to print commands without executing them. `--verbose` shows
subprocess calls, while `--quiet` minimizes output. Set `NO_COLOR=1` or use
`--no-color` to disable colored output.

### Text User Interface

```bash
it ui run

# Key bindings within the TUI:
#   r refresh   u up   d down   s status   l logs of selected service
```

### Other examples

```bash
it search query "neo4j" --chart
```
