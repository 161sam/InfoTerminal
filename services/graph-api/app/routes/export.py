import xml.etree.ElementTree as ET
from fastapi import APIRouter, Response, HTTPException
from .alg import driver

router = APIRouter(prefix="/export", tags=["export"])


def _fetch(node_ids=None, edge_ids=None, query=None):
    with driver.session() as s:
        if query:
            g = s.run(query).graph()
        else:
            q = (
                "MATCH (n) WHERE $nids IS NULL OR id(n) IN $nids "
                "OPTIONAL MATCH (n)-[r]-() WHERE $eids IS NULL OR id(r) IN $eids "
                "RETURN n,r"
            )
            g = s.run(q, nids=node_ids, eids=edge_ids).graph()
    nodes = [
        {"id": n.id, "labels": list(n.labels), "properties": dict(n)} for n in g.nodes
    ]
    rels = [
        {
            "id": r.id,
            "type": r.type,
            "source": r.start_node.id,
            "target": r.end_node.id,
            "properties": dict(r),
        }
        for r in g.relationships
    ]
    return nodes, rels


@router.get("/json")
def export_json(nodeIds: str | None = None, edgeIds: str | None = None, query: str | None = None):
    nids = [int(x) for x in nodeIds.split(",") if x] if nodeIds else None
    eids = [int(x) for x in edgeIds.split(",") if x] if edgeIds else None
    nodes, rels = _fetch(nids, eids, query)
    return {"nodes": nodes, "relationships": rels}


@router.get("/graphml")
def export_graphml(nodeIds: str | None = None, edgeIds: str | None = None, query: str | None = None):
    nids = [int(x) for x in nodeIds.split(",") if x] if nodeIds else None
    eids = [int(x) for x in edgeIds.split(",") if x] if edgeIds else None
    nodes, rels = _fetch(nids, eids, query)
    gml = ET.Element("graphml", xmlns="http://graphml.graphdrawing.org/xmlns")
    graph = ET.SubElement(gml, "graph", edgedefault="undirected")
    for n in nodes:
        ET.SubElement(graph, "node", id=str(n["id"]))
    for r in rels:
        ET.SubElement(
            graph,
            "edge",
            id=str(r["id"]),
            source=str(r["source"]),
            target=str(r["target"]),
        )
    xml_str = ET.tostring(gml, encoding="utf-8")
    return Response(content=xml_str, media_type="application/graphml+xml")
