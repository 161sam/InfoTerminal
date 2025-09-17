from typing import Dict, Any, List
from neo4j import GraphDatabase


class Neo4jClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def ping(self) -> bool:
        with self.driver.session() as s:
            rec = s.run("RETURN 1 as ok").single()
            return bool(rec and rec["ok"] == 1)

    def ensure_schema(self):
        cypher = [
            "CREATE CONSTRAINT law_id IF NOT EXISTS FOR (l:Law) REQUIRE l.id IS UNIQUE",
            "CREATE CONSTRAINT firm_name IF NOT EXISTS FOR (f:Firm) REQUIRE f.name IS UNIQUE",
            "CREATE CONSTRAINT sector_name IF NOT EXISTS FOR (s:Sector) REQUIRE s.name IS UNIQUE",
        ]
        with self.driver.session() as s:
            for stmt in cypher:
                s.run(stmt)

    def upsert_law(self, law: Dict[str, Any], applies_to_sectors: List[str] = None, applies_to_firms: List[str] = None):
        with self.driver.session() as s:
            s.run(
                "MERGE (l:Law {id: $id}) SET l += $props",
                id=law.get("id"),
                props={k: v for k, v in law.items() if k != "id"},
            )
            # Link to Sector by name
            for name in (applies_to_sectors or []):
                s.run(
                    "MERGE (l:Law {id: $id}) "
                    "MERGE (x:Sector {name: $name}) "
                    "MERGE (l)-[:APPLIES_TO]->(x)",
                    id=law.get("id"), name=name,
                )
            # Link to Firm by name
            for name in (applies_to_firms or []):
                s.run(
                    "MERGE (l:Law {id: $id}) "
                    "MERGE (f:Firm {name: $name}) "
                    "MERGE (l)-[:APPLIES_TO]->(f)",
                    id=law.get("id"), name=name,
                )

    def get_laws_for_entity(self, entity: str, limit: int = 10) -> List[Dict[str, Any]]:
        with self.driver.session() as s:
            # Check Firm
            res = s.run(
                "MATCH (f:Firm {name: $entity})-[:APPLIES_TO]-(l:Law) "
                "RETURN l.id as id, l.title as title, l.paragraph as paragraph LIMIT $limit",
                entity=entity, limit=limit,
            ).data()
            if res:
                return res
            # Check Sector
            res = s.run(
                "MATCH (s:Sector {name: $entity})<-[:APPLIES_TO]-(l:Law) "
                "RETURN l.id as id, l.title as title, l.paragraph as paragraph LIMIT $limit",
                entity=entity, limit=limit,
            ).data()
            return res
