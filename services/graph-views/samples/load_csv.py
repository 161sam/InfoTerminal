#!/usr/bin/env python3
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from neo4j import GraphDatabase, basic_auth

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")  # in Compose: bolt://it-neo4j:7687
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test12345")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")
CSV_PATH = os.getenv("CSV_PATH", str(Path(__file__).with_name("people.csv")))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "500"))

CONSTRAINT_CYPHER = """
CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE
"""

MERGE_BATCH_CYPHER = """
UNWIND $rows AS r
MERGE (p:Person {id: r.id})
  ON CREATE SET p.name = r.name
  ON MATCH  SET p.name = COALESCE(r.name, p.name)
WITH r, p
WHERE r.knows_id IS NOT NULL AND r.knows_id <> ''
MERGE (q:Person {id: r.knows_id})
MERGE (p)-[:KNOWS]->(q)
"""

def chunked(rows: List[Dict], size: int):
    for i in range(0, len(rows), size):
        yield rows[i:i+size]

def load_rows(csv_path: str) -> List[Dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        out = []
        for row in reader:
            out.append({
                "id": (row.get("id") or "").strip(),
                "name": (row.get("name") or "").strip() or None,
                "knows_id": (row.get("knows_id") or "").strip() or None,
            })
        return out

def run() -> Tuple[int, int]:
    if not Path(CSV_PATH).exists():
        print(f"[ERR] CSV not found: {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    rows = [r for r in load_rows(CSV_PATH) if r["id"]]
    if not rows:
        print("[WARN] CSV contained no valid rows.")
        return (0, 0)

    driver = GraphDatabase.driver(NEO4J_URI, auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD))
    nodes_created = 0
    rels_created = 0

    def summary_counts(s) -> Tuple[int, int]:
        # Some versions expose counters differently; keep defensive
        c = getattr(s, "counters", None)
        if not c:
            return (0, 0)
        return (c.nodes_created, c.relationships_created)

    with driver.session(database=NEO4J_DATABASE) as session:
        session.run(CONSTRAINT_CYPHER).consume()
        for batch in chunked(rows, BATCH_SIZE):
            res = session.run(MERGE_BATCH_CYPHER, rows=batch)
            s = res.consume()
            n, r = summary_counts(s)
            nodes_created += n
            rels_created += r

    driver.close()
    print(f"[OK] Upsert done. nodesCreated={nodes_created} relsCreated={rels_created} totalRows={len(rows)}")
    return nodes_created, rels_created

if __name__ == "__main__":
    run()

