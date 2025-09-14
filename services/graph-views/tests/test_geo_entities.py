from fastapi.testclient import TestClient


def test_geo_entities_smoke(app_client: TestClient):
    resp = app_client.get("/geo/entities")
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) >= 1


def test_geo_entities_bbox(app_client: TestClient):
    resp = app_client.get("/geo/entities", params={"bbox": "10,47,12,49"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["features"]) == 1
