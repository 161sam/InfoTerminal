import os
from neo4j import GraphDatabase

uri = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
user = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD") or os.getenv("NEO4J_PASS", "neo4jpass")

driver = GraphDatabase.driver(uri, auth=(user, password))
with driver.session() as session:
    session.run("MERGE (a:Person {id:'p1', name:'Alice'})").consume()
    session.run("MERGE (b:Person {id:'p2', name:'Bob'})").consume()
    session.run("MATCH (a:Person {id:'p1'}), (b:Person {id:'p2'}) MERGE (a)-[:KNOWS]->(b)").consume()
print("[seed-graph] OK")
