# CLI Inventory

_Generated on 2025-09-21T10:57:18Z by `scripts/generate_parity_reports.py`_

## cli/it_cli/commands/analytics.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| kpis | Fetch KPIs from analytics endpoint and display them. | chart | /analytics/kpis | views-api | cli/it_cli/commands/analytics.py:18 |

## cli/it_cli/commands/fe.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| build | — | — | /frontend | — | cli/it_cli/commands/fe.py:20 |
| dev | — | — | /frontend | — | cli/it_cli/commands/fe.py:15 |
| test | — | — | /frontend | — | cli/it_cli/commands/fe.py:25 |

## cli/it_cli/commands/graph.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| cypher | Execute a Cypher query via `/v1/cypher`. | query, param, read_only | /v1/cypher | graph-api | cli/it_cli/commands/graph.py:46 |
| neighbors | Fetch neighbors for a node via `/v1/nodes/{id}/neighbors`. | node_id, depth, limit, direction, relationship_types, visualize | /neighbors, /v1/nodes/, /v1/nodes/{id}/neighbors, /v1/nodes/{}/neighbors | graph-api | cli/it_cli/commands/graph.py:73 |
| ping | Ping graph-api health endpoint. | — | /healthz | graph-api | cli/it_cli/commands/graph.py:22 |
| shortest-path | Compute shortest path via `/v1/shortest-path`. | source, target, max_length | /v1/shortest-path | graph-api | cli/it_cli/commands/graph.py:116 |

## cli/it_cli/commands/search.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| query | Run a search query against search-api. | q, sort, limit, chart | /search | search-api | cli/it_cli/commands/search.py:18 |

## cli/it_cli/commands/settings.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| show | Print current configuration. | — | — | model-dump-json | cli/it_cli/commands/settings.py:15 |

## cli/it_cli/commands/tui.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| run | Run the Textual TUI. | — | — | — | cli/it_cli/commands/tui.py:11 |

## cli/it_cli/commands/views.py (groups: app)
| Command | Description | Parameters | API Paths | Services | Source |
|---|---|---|---|---|---|
| query | Execute a SQL query via views-api. | sql, limit | /query | views-api | cli/it_cli/commands/views.py:17 |
