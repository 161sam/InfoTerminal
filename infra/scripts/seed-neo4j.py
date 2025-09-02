from neo4j import GraphDatabase

uri="bolt://localhost:7687"; user="neo4j"; pwd="neo4jpass"
driver=GraphDatabase.driver(uri, auth=(user,pwd))
with driver.session() as s:
    s.run("MATCH (n) DETACH DELETE n")
    s.run("""
    MERGE (p1:Person {id:'P:alice', name:'Alice'})
    MERGE (p2:Person {id:'P:bob', name:'Bob'})
    MERGE (o1:Org {id:'O:acme', name:'ACME Inc.'})
    MERGE (o2:Org {id:'O:globex', name:'Globex'})
    MERGE (p1)-[:EMPLOYED_AT]->(o1)
    MERGE (p2)-[:EMPLOYED_AT]->(o2)
    MERGE (o1)-[:PARTNER_OF]->(o2)
    """)
print("Seeded.")
