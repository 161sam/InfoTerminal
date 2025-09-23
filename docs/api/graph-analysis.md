# Graph Analysis API – Phase 2 Wave 1

Die Graph-Analyse-Endpunkte des `graph-api` Services liefern die MVP-Algorithmen für Paket A (Ontologie & Graph). Standard-Port im Docker-Profil: `http://localhost:8612`.

> 💡 **Seed-Daten:** `scripts/seed_demo.sh` legt zwei Knoten (`p1`, `p2`) und eine `KNOWS`-Relation an. Die folgenden Beispiele funktionieren direkt nach dem Seed.

## 1. Degree Centrality

```bash
curl -s "http://localhost:8612/graphs/analysis/degree?limit=5&offset=0" \
  | jq '{algorithm, results: [.results[] | {name, degree}]}'
```

Antwort enthält:
- `algorithm: "degree"`
- `results`: Liste sortiert nach Grad (Labels + Node-ID enthalten)
- `pagination`: `limit/offset/next_offset`

## 2. Louvain-Communities

```bash
curl -s "http://localhost:8612/graphs/analysis/communities?min_size=1&limit=5" \
  | jq '{community_count, communities: [.communities[] | {id, size}]}'
```

- `community_count` liefert Anzahl der Community-Buckets.
- Jeder Eintrag enthält `members` mit `node_id`, `name`, `labels`.

## 3. Shortest Path

```bash
curl -s -X POST "http://localhost:8612/graphs/analysis/shortest-path" \
  -H 'Content-Type: application/json' \
  -d '{"start_node_id":"p1","end_node_id":"p2","max_length":6}' \
  | jq '{path_found, length, nodes}'
```

- Antwort liefert deterministischen Pfad gemäß Fixture (`p1` → `p2`).
- `path_found` bleibt `false`, falls keine Verbindung ≤ `max_length` existiert.

## 4. Subgraph-Export (Dossier-Hook)

```bash
curl -s "http://localhost:8612/graphs/analysis/subgraph-export?center_id=p1&format=markdown" \
  | jq -r '.markdown'
```

- Markdown-Block dient als Hook für die Dossier-Pipeline (`collab-hub` `/dossier/export`).
- JSON-Antwort enthält zusätzlich `nodes`, `relationships` und `center` mit Neo4j-IDs.

## Observability & Smoke Tests

- Prometheus-Metriken: `graph_analysis_queries_total{algorithm,status}`, `graph_analysis_duration_seconds_bucket{algorithm,status}`, `graph_subgraph_exports_total{format,status}` (`/metrics`).
- Smoke-Test: `scripts/smoke_graph_analysis.sh` prüft Healthz, Degree, Louvain, Shortest-Path und Subgraph-Export.
- Dashboards: Grafana `grafana/dashboards/graph-analytics-mvp.json`, Superset `apps/superset/assets/dashboard/graph_analytics_mvp.json`.

## Weiterführend

- CLI: `it graph export-subgraph --center p1 --format markdown` nutzt dieselben Endpunkte.
- Dossier-Export: `curl http://localhost:8625/dossier/export -d '{"case_id":"demo-case",...}'` (siehe README-Demo).
