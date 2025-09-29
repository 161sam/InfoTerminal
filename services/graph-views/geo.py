import json
import os
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

GEO_DIR = Path(os.getenv("GEO_UPLOAD_DIR", "/data/geo"))
GEO_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/geo", tags=["geo"])

@router.post("/upload")
async def upload_geo(file: UploadFile = File(...)):
    if not file.filename.endswith(".geojson"):
        raise HTTPException(400, "expected .geojson")
    try:
        data = json.loads((await file.read()).decode())
    except Exception:
        raise HTTPException(400, "invalid json")
    if data.get("type") != "FeatureCollection":
        raise HTTPException(400, "expected FeatureCollection")
    GEO_DIR.mkdir(parents=True, exist_ok=True)
    path = GEO_DIR / file.filename
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f)
    return {"ok": True, "name": file.filename}

@router.get("/list")
def list_geo():
    items = []
    if GEO_DIR.exists():
        for p in GEO_DIR.glob("*.geojson"):
            items.append({"name": p.name, "size": p.stat().st_size})
    return {"items": items}

@router.get("/get")
def get_geo(name: str = Query(...)):
    path = GEO_DIR / name
    if not path.exists():
        raise HTTPException(404, "not found")
    with path.open() as f:
        return json.load(f)

@router.get("/query")
def query_geo(bbox: str, name: str):
    path = GEO_DIR / name
    if not path.exists():
        raise HTTPException(404, "not found")
    try:
        minLon, minLat, maxLon, maxLat = map(float, bbox.split(","))
    except Exception:
        raise HTTPException(400, "bad bbox")
    with path.open() as f:
        data = json.load(f)
    features: List[dict] = []
    for feat in data.get("features", []):
        geom = feat.get("geometry", {})
        coords = geom.get("coordinates")
        if not coords or isinstance(coords[0], list):
            continue  # only handle Point for now
        lon, lat = coords
        if minLon <= lon <= maxLon and minLat <= lat <= maxLat:
            features.append(feat)
    return {"type": "FeatureCollection", "features": features}


@router.get("/entities")
def geo_entities(bbox: Optional[str] = None):
    """Return a small set of sample entities as GeoJSON."""
    sample = [
        {"id": "1", "name": "Berlin", "lat": 52.52, "lon": 13.405},
        {"id": "2", "name": "Munich", "lat": 48.137, "lon": 11.575},
    ]
    features: List[dict] = []
    bounds = None
    if bbox:
        try:
            bounds = tuple(map(float, bbox.split(",")))
        except Exception:
            raise HTTPException(400, "bad bbox")
    for ent in sample:
        lon = ent["lon"]
        lat = ent["lat"]
        if bounds:
            min_lon, min_lat, max_lon, max_lat = bounds
            if not (min_lon <= lon <= max_lon and min_lat <= lat <= max_lat):
                continue
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {"id": ent["id"], "name": ent["name"]},
            }
        )
    return {"type": "FeatureCollection", "features": features}
