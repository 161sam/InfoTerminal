import pytest
import search_api.app.main as app

@pytest.mark.anyio
async def test_query_facets_and_sort(client, monkeypatch):
    def fake_search(index, body):
        assert body["aggs"]["source"]["terms"]["field"] == "source"
        assert body["sort"][0]["meta.created_at"]["order"] == "desc"
        return {
            "took": 4,
            "hits": {
                "total": {"value": 1},
                "hits": [{"_id": "1", "_score": 1.0, "_source": {"title": "Doc"}}],
            },
            "aggregations": {"source": {"buckets": [{"key": "osint", "doc_count": 1}]}}
        }
    monkeypatch.setattr(app.client, "search", fake_search)
    payload = {
        "q": "apple",
        "facets": ["source"],
        "sort": {"field": "meta.created_at", "order": "desc"},
        "limit": 10,
        "offset": 0,
    }
    r = await client.post("/query", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 1
    assert data["tookMs"] == 4
    assert data["aggregations"]["source"][0]["key"] == "osint"
    assert data["items"][0]["title"] == "Doc"
