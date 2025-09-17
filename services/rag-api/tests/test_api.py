from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz():
    r = client.get('/healthz')
    assert r.status_code == 200

def test_index_and_retrieve():
    doc = {"id": "test_law_1", "title": "Test Law", "paragraph": "§1", "text": "Dies ist ein Test."}
    r = client.post('/law/index', json=doc)
    assert r.status_code == 200
    r2 = client.get('/law/retrieve?q=Test')
    assert r2.status_code == 200
    data = r2.json()
    assert 'items' in data

def test_knn_route():
    r = client.get('/law/knn?q=Test&k=3')
    assert r.status_code == 200

