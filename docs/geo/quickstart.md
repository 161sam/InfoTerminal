# Geospatial Quickstart

This guide shows how to work with the geospatial layer.

## API

`GET /geo/entities` returns a GeoJSON `FeatureCollection` of known entity locations. A bounding box can filter the result:

```sh
curl "http://localhost:8403/geo/entities?bbox=10,47,12,49"
```

## Frontend

Run the frontend and open the map panel:

```sh
npm run dev:fe
```

The map displays entity points and uploaded layers. Use the *Entities* toggle to show or hide built-in data.
