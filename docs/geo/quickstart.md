# Geospatial Quickstart

This guide shows how to work with the geospatial layer.

## API

`GET /geo/entities` (Graph API) returns a JSON payload with matching nodes. Provide south/west/north/east bounds:

```sh
curl "http://localhost:8612/geo/entities?south=40&west=-75&north=41&east=-73"
```

Nearby search:

```sh
curl -X POST "http://localhost:8612/geo/entities/nearby" \
  -H 'Content-Type: application/json' \
  -d '{"latitude":52.5,"longitude":13.4,"radius_km":10}'
```

Prometheus counters `graph_geo_queries_total{type="bbox"}` and `graph_geo_query_errors_total` are exposed via `http://localhost:8612/metrics`.

> ℹ️ External geocoding (Nominatim) is opt-in. Set `GRAPH_ENABLE_GEOCODING=1` before starting the Graph API if you need live coordinate lookups.

## Frontend

Run the frontend and open the map panel:

```sh
npm run dev:fe
```

Open `http://localhost:3411/map` to see bounding boxes, nearby search and heatmap layers powered by the Graph API. Use the *Entities* toggle to show/hide live data.
