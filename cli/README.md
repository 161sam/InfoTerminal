# InfoTerminal CLI

Modular developer command-line interface for the InfoTerminal platform.

## Installation

```bash
pip install -e .
```

## Usage

```bash
it --help

# show version
it -V
```

The CLI prints a banner on each run. Set `IT_NO_BANNER=1` to disable it
for scripting or CI environments.

Each domain is available as a subcommand, e.g.:

```bash
it infra health
it search query "neo4j" --chart
```
