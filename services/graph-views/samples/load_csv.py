#!/usr/bin/env python3
import argparse
import csv
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import ServiceUnavailable, TransientError

DEFAULT_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
DEFAULT_USER = os.getenv("NEO4J_USER", "neo4j")
DEFAULT_PASSWORD = os.getenv("NEO4J_PASSWORD", "test12345")
DEFAULT_DB = os.getenv("NEO4J_DATABASE", "neo4j")
DEFAULT_CSV = os.getenv("CSV_PATH", str(Path(__file__).with_name("people.csv")))
DEFAULT_BATCH = int(os.getenv("BATCH_SIZE", "500"))

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
        yield rows[i : i + size]


def load_rows(csv_path: str) -> List[Dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        out = []
        for row in reader:
            out.append(
                {
                    "id": (row.get("id") or "").strip(),
                    "name": (row.get("name") or "").strip() or None,
                    "knows_id": (row.get("knows_id") or "").strip() or None,
                }
            )
        return out


def with_retries(fn, max_attempts: int = 5, base_delay: float = 0.2):
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            if attempt >= max_attempts - 1 or not isinstance(e, (ServiceUnavailable, TransientError)):
                raise
            time.sleep(base_delay * (2 ** attempt))


def run() -> Tuple[int, int]:
    parser = argparse.ArgumentParser(description="Load demo CSV into Neo4j")
    parser.add_argument("--uri", default=DEFAULT_URI)
    parser.add_argument("--user", default=DEFAULT_USER)
    parser.add_argument("--password", default=DEFAULT_PASSWORD)
    parser.add_argument("--database", default=DEFAULT_DB)
    parser.add_argument("--csv", default=DEFAULT_CSV)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH)
    args = parser.parse_args()

    if not Path(args.csv).exists():
        print(f"[ERR] CSV not found: {args.csv}", file=sys.stderr)
        sys.exit(1)

    rows = [r for r in load_rows(args.csv) if r["id"]]
    if not rows:
        print("[WARN] CSV contained no valid rows.")
        return (0, 0)

    driver = GraphDatabase.driver(args.uri, auth=basic_auth(args.user, args.password))
    try:
        with_retries(lambda: driver.verify_connectivity())
    except Exception as e:
        print(f"[ERR] Could not connect to {args.uri}: {e}", file=sys.stderr)
        print("Check URI/host/port and credentials.", file=sys.stderr)
        print("See README.md section 'Troubleshooting: Neo4j connection refused'.", file=sys.stderr)
        driver.close()
        sys.exit(2)

    nodes_created = 0
    rels_created = 0

    def summary_counts(s) -> Tuple[int, int]:
        c = getattr(s, "counters", None)
        if not c:
            return (0, 0)
        return (c.nodes_created, c.relationships_created)

    with driver.session(database=args.database) as session:
        with_retries(lambda: session.run(CONSTRAINT_CYPHER).consume())
        for batch in chunked(rows, args.batch_size):
            def do_merge():
                res = session.run(MERGE_BATCH_CYPHER, rows=batch)
                return summary_counts(res.consume())

            n, r = with_retries(do_merge, max_attempts=5, base_delay=0.2)
            nodes_created += n
            rels_created += r

    driver.close()
    print(
        f"[OK] Upsert done. nodesCreated={nodes_created} relsCreated={rels_created} totalRows={len(rows)}"
    )
    return nodes_created, rels_created


if __name__ == "__main__":
    run()
