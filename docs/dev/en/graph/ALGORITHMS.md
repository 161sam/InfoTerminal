# Graph Algorithms

The graph API exposes several analysis endpoints under `/alg`:

- `POST /alg/degree` — degree centrality via GDS or Cypher fallback.
- `POST /alg/betweenness` — requires Neo4j GDS; returns betweenness scores.
- `POST /alg/communities` — Louvain community detection when GDS is enabled.

Set `IT_NEO4J_GDS=1` to enable GDS-based algorithms. Without it, betweenness and communities return `501 Not Implemented`.
