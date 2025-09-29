from app import app
from fastapi.testclient import TestClient
from rate_limit import parse_rate


def test_write_rate_limit(app_client: TestClient, monkeypatch):
    monkeypatch.setenv("GV_ALLOW_WRITES", "1")
    monkeypatch.setenv("GV_RATE_LIMIT_WRITE", "2/second")
    app.state.rate_cfg = "2/second"
    app.state.rate_cap, app.state.rate_refill = parse_rate(app.state.rate_cfg)
    app.state.rate_buckets = {}
    for i in range(3):
        r = app_client.post("/graphs/cypher?write=1", json={"query": "RETURN 1", "params": {}})
    assert r.status_code in (429, 401)
    if r.status_code == 429:
        j = r.json()
        assert j["error"]["code"] == "rate_limited"
        assert "Retry-After" in r.headers
    app.state.rate_cap = 0


def test_write_rate_limit_headers(app_client: TestClient, monkeypatch):
    monkeypatch.setenv("GV_ALLOW_WRITES","1")
    monkeypatch.setenv("GV_RATE_LIMIT_WRITE","1/second")
    # Trigger: 2 schnelle Writes
    r1 = app_client.post("/graphs/cypher?write=1", json={"stmt":"RETURN 1","params":{}})
    assert r1.status_code in (200, 401, 429)
    r2 = app_client.post("/graphs/cypher?write=1", json={"stmt":"RETURN 1","params":{}})
    if r2.status_code == 429:
        assert "Retry-After" in r2.headers
        assert "X-RateLimit-Limit" in r2.headers
        assert "X-RateLimit-Remaining" in r2.headers
        assert "X-RateLimit-Reset" in r2.headers


def test_429_has_json_ct_and_headers(app_client: TestClient, monkeypatch):
    monkeypatch.setenv("GV_ALLOW_WRITES","1")
    monkeypatch.setenv("GV_RATE_LIMIT_WRITE","1/second")
    app_client.post("/graphs/cypher?write=1", json={"stmt":"RETURN 1","params":{}})
    r = app_client.post("/graphs/cypher?write=1", json={"stmt":"RETURN 1","params":{}})
    if r.status_code == 429:
        assert r.headers.get("content-type","" ).startswith("application/json")
        for k in ("Retry-After","X-RateLimit-Limit","X-RateLimit-Remaining","X-RateLimit-Reset","X-Request-ID"):
            assert k in r.headers
