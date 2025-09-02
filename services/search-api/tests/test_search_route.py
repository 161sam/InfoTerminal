import pytest
import app

@pytest.mark.anyio
async def test_search_minimal(client, monkeypatch):
    def fake_search(index, body):
        return {"hits": {"hits": []}, "aggregations": {}}
    monkeypatch.setattr(app.client, "search", fake_search)
    r = await client.get("/search", params={"q": "apple"})
    assert r.status_code == 200
    body = r.json()
    assert "results" in body
    assert isinstance(body["results"], list)
