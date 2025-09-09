# Graph Linking

The document entity resolver links named entities detected in documents to
nodes in the Neo4j knowledge graph.

1. `/annotate` stores a document and marks all entities as `pending`.
2. The background resolver looks up candidates in Neo4j and updates the
   `entity_resolutions` table.
3. Resolved entities can optionally create `MENTIONS` relations in the
   graph.

For development, ensure the following indexes exist in Neo4j:

```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (o:Organization) REQUIRE o.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (e:Email) REQUIRE e.addr IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ip:IP) REQUIRE ip.addr IS UNIQUE;
```
