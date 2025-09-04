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
# start local stack
it infra up

# check status (exit code 0 only if search/graph/views are up)
it infra status

# follow logs
it infra logs -f --service graph-api

# stop services
it infra down
```

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
