import os
from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
user = os.getenv("NEO4J_USER", "neo4j")
pwd = os.getenv("NEO4J_PASSWORD") or os.getenv("NEO4J_PASS", "neo4jpass")

drv = GraphDatabase.driver(uri, auth=(user, pwd))
with drv.session() as s:
    s.run("MERGE (a:Person {id:'p1', name:'Alice'})").consume()
    s.run("MERGE (b:Person {id:'p2', name:'Bob'})").consume()
    s.run(
        "MATCH (a:Person{id:'p1'}),(b:Person{id:'p2'}) MERGE (a)-[:KNOWS]->(b)"
    ).consume()
print("[seed-graph] OK")
