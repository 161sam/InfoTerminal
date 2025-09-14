# Graph-Analyse v1

Die Graph-API stellt einfache Algorithmen bereit. Ohne Neo4j GDS liefert nur `degree` echte Werte, `betweenness` und `louvain` antworten mit 501.

## Endpunkte

- `POST /alg/degree`
- `POST /alg/betweenness`
- `POST /alg/louvain`
- `GET /export/json`
- `GET /export/graphml`

## Frontend

Im Pfad `/graphx` gibt es ein Analyse-Panel zum Starten der Algorithmen. Ergebnisse erscheinen als Badges, Knoten-Popups zeigen Degree/Betweenness/Community. Ein Export-Dropdown bietet JSON oder GraphML.
