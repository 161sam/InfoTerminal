from fastapi.testclient import TestClient


def test_list_entities(app_client: TestClient):
    r = app_client.get('/ontology/entities')
    assert r.status_code == 200
    assert any(e['name'] == 'Person' for e in r.json())


def test_validate_entity_ok(app_client: TestClient):
    payload = {'type': 'Person', 'data': {'id': 'alice', 'name': 'Alice'}}
    r = app_client.post('/ontology/validate', json=payload)
    assert r.status_code == 200
    assert r.json()['ok'] is True


def test_validate_entity_missing(app_client: TestClient):
    payload = {'type': 'Person', 'data': {'id': 'alice'}}
    r = app_client.post('/ontology/validate', json=payload)
    assert r.status_code == 400
    assert 'Missing required' in r.json()['detail']
