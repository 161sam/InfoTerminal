import pytest


@pytest.mark.anyio
async def test_ner(client):
    r = await client.post("/ner", json={"text": "Alice and Bob went to Wonderland"})
    assert r.status_code == 200
    data = r.json()["entities"]
    assert data and data[0]["text"] == "Alice"


@pytest.mark.anyio
async def test_summarize(client):
    text = "This service uses NLP models to provide useful features for developers."
    r = await client.post("/summarize", json={"text": text})
    assert r.status_code == 200
    summary = r.json()["summary"]
    assert summary.split()[0] == "This"
