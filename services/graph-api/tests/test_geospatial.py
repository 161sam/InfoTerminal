import asyncio
from typing import Any, Dict, List

import pytest

from metrics import GRAPH_GEO_QUERIES, GEO_QUERY_COUNT


class DummyResult:
    def __init__(self, records: List[Dict[str, Any]]):
        self._records = records

    def __iter__(self):
        return iter(self._records)

    def single(self):
        return self._records[0] if self._records else None


class DummySession:
    def __init__(self, records: List[Dict[str, Any]]):
        self._records = records

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def run(self, query: str, **kwargs):
        if "geocoding_percentage" in query:
            return DummyResult([
                {"total_nodes": 10, "geocoded_nodes": 5, "geocoding_percentage": 50.0}
            ])
        if "labels(n) as labels" in query:
            return DummyResult([
                {"node_id": "loc:1", "name": "Berlin", "latitude": 52.5, "longitude": 13.4, "labels": ["Location"]}
            ])
        if "labels(n) as label" in query:
            return DummyResult([
                {"label": "Location", "count": 1}
            ])
        if "geographic_spread" in query or "min(n.latitude)" in query:
            return DummyResult([
                {
                    "min_lat": 52.0,
                    "max_lat": 53.0,
                    "min_lon": 13.0,
                    "max_lon": 14.0,
                    "center_lat": 52.5,
                    "center_lon": 13.5,
                }
            ])
        return DummyResult(self._records)


class DummyDriver:
    def __init__(self, records: List[Dict[str, Any]]):
        self._records = records

    def session(self, database: str = None):
        return DummySession(self._records)


@pytest.mark.anyio
async def test_geo_entities_records_metrics(client):
    from app import app as graph_app

    graph_app.state.driver = DummyDriver(
        [{"node_id": "loc:1", "name": "Berlin", "latitude": 52.5, "longitude": 13.4, "labels": ["Location"]}]
    )

    response = await client.get(
        "/geo/entities",
        params={"south": 50.0, "west": 10.0, "north": 55.0, "east": 15.0, "limit": 10},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["entities"][0]["name"] == "Berlin"

    bbox_metric = GRAPH_GEO_QUERIES.labels(type="bbox")._value.get()
    compat_metric = GEO_QUERY_COUNT.labels(type="bbox")._value.get()
    assert bbox_metric >= 1
    assert compat_metric >= 1
