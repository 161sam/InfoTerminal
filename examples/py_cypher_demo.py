import os, json, requests

VIEWS = os.getenv("VIEWS_API", "http://localhost:8403")

# 1) Constraint anlegen (write=1)
resp = requests.post(f"{VIEWS}/graphs/cypher", params={"write": 1}, json={
    "stmt": "CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
    "params": {}
})
print("Constraint:", resp.status_code, resp.json())

# 2) Einfache MATCH-Abfrage
resp = requests.post(f"{VIEWS}/graphs/cypher", json={
    "stmt": "MATCH (p:Person) RETURN p.id AS id, p.name AS name ORDER BY id LIMIT 10",
    "params": {}
})
print("People:", json.dumps(resp.json(), indent=2, ensure_ascii=False))
