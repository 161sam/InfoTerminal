from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_tasks_lifecycle():
    # create
    r = client.post('/tasks', json={"text": "Test Task", "priority": "high"})
    assert r.status_code == 200
    tid = r.json().get('id')
    assert tid
    # list
    r = client.get('/tasks')
    assert r.status_code == 200
    # move
    r = client.post(f'/tasks/{tid}/move?to=doing')
    assert r.status_code == 200
    # update
    r = client.post(f'/tasks/{tid}/update', json={"labels": ["alpha"]})
    assert r.status_code == 200
    # delete
    r = client.delete(f'/tasks/{tid}')
    assert r.status_code == 200

