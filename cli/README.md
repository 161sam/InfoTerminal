# InfoTerminal CLI

Modular developer command-line interface for InfoTerminal.

## Installation

Install via [pipx](https://pypa.github.io/pipx/) to avoid virtual
environments in your home directory:

```bash
pipx install --force ./cli
```

## Usage

```bash
it --help
it -V            # show version
IT_NO_BANNER=1 it status -n  # suppress banner
```

The CLI prints a banner once per run. Set `IT_NO_BANNER=1` to disable it.
`--version`/`-V` prints the version and exits.

### Lifecycle commands

The root command exposes a small set of docker-compose wrappers which
forward to the `infra` namespace:

- `start` – bring services up
- `stop` – stop running services
- `restart` – restart services via `docker compose restart`
- `rm` – remove environment via `docker compose down --remove-orphans`
- `status` – show service status
- `logs` – stream logs (requires `--services`)

Examples:

```bash
it start -n -f docker-compose.yml -p dev -s neo4j,opensearch --profile observability
it status -n --format json
it logs -n -s neo4j --lines 10
```

### Flags

Common flags are available across commands:

| Flag | Description |
| --- | --- |
| `-f`, `--compose-file` | Additional compose file (repeatable) |
| `-p`, `--project-name` | Compose project name |
| `--env-file` | Env file passed to compose |
| `--profile` | Compose profile (repeatable) |
| `-s`, `--services` | Limit to given services (comma separated or repeat) |
| `-n`, `--dry-run` | Print command without executing |
| `--verbose` | Show subprocess output |
| `-q`, `--quiet` | Minimal output |

Specific flags:

| Command | Extra flags |
| --- | --- |
| `start` | `-d/--detach`, `--retries`, `--timeout` |
| `restart` | `--retries`, `--timeout` |
| `rm` | `-v/--volumes`, `--images [all|local|none]` (use `--verbose` for verbosity) |
| `status` | `--format [table|text|json|yaml]` |
| `logs` | `-F/--follow`, `--lines N`, `--format [plain|jsonl]` |

Use `--dry-run` to print the composed `docker compose` command without
executing it. `--verbose` prints subprocess output, `--quiet` suppresses
it.

The `infra` namespace exposes the same commands for advanced use.
