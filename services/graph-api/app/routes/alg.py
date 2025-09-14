import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from neo4j import GraphDatabase

router = APIRouter(prefix="/alg", tags=["algorithms"])

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://it-neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD", "test12345")
USE_GDS = os.getenv("IT_NEO4J_GDS", "0") == "1"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

class DegreeIn(BaseModel):
    nodeLabel: str | None = None
    direction: str | None = None  # "IN" | "OUT" | "BOTH"

@router.post("/degree")
def degree(inp: DegreeIn):
    with driver.session() as s:
        if USE_GDS:
            # simple GDS degree
            q = "CALL gds.degree.stream({nodeProjection: $label}) YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS id, score"
            return {"items": s.run(q, label=inp.nodeLabel or "*").data()}
        else:
            # Cypher fallback
            if inp.nodeLabel:
                q = f"MATCH (n:`{inp.nodeLabel}`) OPTIONAL MATCH (n)-[r]-() RETURN id(n) AS id, coalesce(count(r),0) AS degree"
            else:
                q = "MATCH (n) OPTIONAL MATCH (n)-[r]-() RETURN id(n) AS id, coalesce(count(r),0) AS degree"
            return {"items": s.run(q).data()}


class BetweennessIn(BaseModel):
    nodeLabel: str | None = None


@router.post("/betweenness")
def betweenness(inp: BetweennessIn):
    with driver.session() as s:
        if USE_GDS:
            q = (
                "CALL gds.betweenness.stream({nodeProjection: $label}) "
                "YIELD nodeId, score RETURN gds.util.asNode(nodeId).id AS id, score"
            )
            return {"items": s.run(q, label=inp.nodeLabel or "*").data()}
        raise HTTPException(501, "Betweenness requires GDS")


class LouvainIn(BaseModel):
    nodeLabel: str | None = None


@router.post("/louvain")
def louvain(inp: LouvainIn):
    with driver.session() as s:
        if USE_GDS:
            q = (
                "CALL gds.louvain.stream({nodeProjection:$label, relationshipProjection:'*'}) "
                "YIELD nodeId, communityId RETURN id(gds.util.asNode(nodeId)) AS id, communityId"
            )
            return {"items": s.run(q, label=inp.nodeLabel or "*").data()}
        raise HTTPException(501, "Louvain requires GDS")

class ShortestIn(BaseModel):
    sourceId: int
    targetId: int
    weightProp: str | None = None

@router.post("/shortest")
def shortest(inp: ShortestIn):
    with driver.session() as s:
        if USE_GDS:
            q = """
            MATCH (s),(t) WHERE id(s)=$sid AND id(t)=$tid
            CALL gds.shortestPath.dijkstra.stream($g, {sourceNode:s, targetNode:t, relationshipWeightProperty:$w})
            YIELD totalCost, nodeIds
            RETURN totalCost, nodeIds
            """
            raise HTTPException(501, "GDS graph config required")
        else:
            # simple unweighted path
            q = """
            MATCH (s),(t) WHERE id(s)=$sid AND id(t)=$tid
            MATCH p = shortestPath((s)-[*..10]-(t)) RETURN p
            """
            rec = s.run(q, sid=inp.sourceId, tid=inp.targetId).single()
            return {"path": rec["p"] if rec else None}
