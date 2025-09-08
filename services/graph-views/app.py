import os
import re
import asyncio
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Body, Query, Request
from pydantic import BaseModel

from _shared.cors import apply_cors
from _shared.health import make_healthz, make_readyz
from _shared.obs.metrics_boot import enable_prometheus_metrics
from _shared.obs.otel_boot import setup_otel
try:  # pragma: no cover - import fallback for tests
    from . import neo  # type: ignore
except ImportError:  # pragma: no cover
    import neo  # type: ignore

# -----------------------
# Neo4j (optional)
# -----------------------
HAVE_NEO4J = False
try:
    import neo4j  # type: ignore
    HAVE_NEO4J = True
except Exception:
    neo4j = None  # type: ignore

# Für Typerkennung bei Serialisierung (optional)
Neo4jNode = None
Neo4jRelationship = None
Neo4jPath = None
if HAVE_NEO4J:
    try:
        from neo4j.graph import Node as Neo4jNode, Relationship as Neo4jRelationship, Path as Neo4jPath  # type: ignore
    except Exception:
        pass

# -----------------------
# FastAPI-App
# -----------------------
app = FastAPI(title="graph-views")
apply_cors(app)
enable_prometheus_metrics(app, route="/metrics")
setup_otel(app)

# -----------------------
# App-Status
# -----------------------
SERVICE_NAME = os.getenv("SERVICE_NAME", "graph-views")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.1.0")

# Schreibschutz-Flag
GV_ALLOW_WRITES = str(os.getenv("GV_ALLOW_WRITES", "0")).lower() in ("1", "true", "yes", "on")


def require_write_auth(request: Request) -> None:
    user = os.getenv("GV_BASIC_USER")
    password = os.getenv("GV_BASIC_PASS")
    if not (user and password):
        return
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Basic "):
        raise HTTPException(status_code=401, detail="auth required", headers={"WWW-Authenticate": 'Basic realm="InfoTerminal"'})
    import base64
    try:
        decoded = base64.b64decode(auth.split(" ", 1)[1]).decode()
    except Exception:
        raise HTTPException(status_code=401, detail="bad auth", headers={"WWW-Authenticate": 'Basic realm="InfoTerminal"'})
    username, _, pw = decoded.partition(":")
    if username != user or pw != password:
        raise HTTPException(status_code=401, detail="bad auth", headers={"WWW-Authenticate": 'Basic realm="InfoTerminal"'})

async def _neo4j_ready() -> bool:
    if not HAVE_NEO4J:
        return True
    try:
        drv = neo.get_driver()
    except Exception:
        return False
    try:
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, drv.verify_connectivity)
        return True
    except Exception:
        return False


@app.on_event("startup")
async def on_startup():
    if HAVE_NEO4J:
        try:
            neo.get_driver()
        except Exception:
            pass


@app.on_event("shutdown")
async def on_shutdown():
    if HAVE_NEO4J:
        try:
            neo.get_driver().close()
        except Exception:
            pass


# -----------------------
# Health / Ready
# -----------------------
@app.get("/healthz")
async def healthz():
    handler = make_healthz()
    return await handler()


@app.get("/readyz")
async def readyz():
    # Wenn IT_FORCE_READY truthy ist, gibt make_readyz sofort "ready" zurück.
    handler = make_readyz(_neo4j_ready)
    return await handler()


# -----------------------
# Utils
# -----------------------
_LABEL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PROP_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _ensure_label(label: str) -> str:
    if not _LABEL_RE.match(label):
        raise HTTPException(status_code=400, detail="invalid label")
    return label


def _ensure_prop(prop: str) -> str:
    if not _PROP_RE.match(prop):
        raise HTTPException(status_code=400, detail="invalid property name")
    return prop


def _serialize_neo4j(value: Any) -> Any:
    # Knoten
    if Neo4jNode and isinstance(value, Neo4jNode):  # type: ignore
        return {
            "__type": "node",
            "id": getattr(value, "id", None),
            "labels": list(getattr(value, "labels", []) or []),
            "properties": dict(value),
        }
    # Beziehung
    if Neo4jRelationship and isinstance(value, Neo4jRelationship):  # type: ignore
        start_id = getattr(value, "start_node_id", None) or getattr(value, "start", None)
        end_id = getattr(value, "end_node_id", None) or getattr(value, "end", None)
        return {
            "__type": "relationship",
            "id": getattr(value, "id", None),
            "type": getattr(value, "type", None),
            "start": start_id,
            "end": end_id,
            "properties": dict(value),
        }
    # Pfad
    if Neo4jPath and isinstance(value, Neo4jPath):  # type: ignore
        nodes = [_serialize_neo4j(n) for n in getattr(value, "nodes", [])]
        rels = [_serialize_neo4j(r) for r in getattr(value, "relationships", [])]
        length = getattr(value, "length", None)
        if length is None:
            try:
                length = len(getattr(value, "relationships", []))
            except Exception:
                length = None
        return {"__type": "path", "nodes": nodes, "relationships": rels, "length": length}

    # Container
    if isinstance(value, list):
        return [_serialize_neo4j(v) for v in value]
    if isinstance(value, tuple):
        return [_serialize_neo4j(v) for v in value]
    if isinstance(value, dict):
        return {k: _serialize_neo4j(v) for k, v in value.items()}

    # Standard
    return value


def _run_cypher(query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    with neo.get_session() as session:
        result = neo.run_with_retries(session, query, params)
        return [_serialize_neo4j(r.data()) for r in result]


def _run_read(query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _run_cypher(query, params)


def _run_write(query: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _run_cypher(query, params)


def _is_write_query(q: str) -> bool:
    ql = q.strip().lower()
    # naive Heuristik – reicht für Absicherung im Dienst
    write_tokens = ("create ", "merge ", "delete ", "set ", "remove ", "drop ")
    return any(tok in ql for tok in write_tokens)


# -----------------------
# API Modelle
# -----------------------
class CypherRequest(BaseModel):
    query: str
    params: Dict[str, Any] | None = None


class PersonRow(BaseModel):
    id: str
    name: Optional[str] = None
    knows_id: Optional[str] = None


class CsvLoadRequest(BaseModel):
    rows: List[PersonRow]


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

CONSTRAINT_CYPHER = """
CREATE CONSTRAINT person_id_unique IF NOT EXISTS
FOR (p:Person) REQUIRE p.id IS UNIQUE
"""


# -----------------------
# Graph-Views Routen
# -----------------------
@app.get("/graphs/ping")
async def graphs_ping():
    """Liefert Info zum Neo4j-Backend (optional)."""
    if not HAVE_NEO4J:
        return {"neo4j": "driver-not-installed", "configured": False}
    try:
        neo.get_driver()
    except Exception:
        return {"neo4j": "not-configured", "configured": False}
    ok = await _neo4j_ready()
    return {"neo4j": "ok" if ok else "unreachable", "configured": True}


@app.post("/graphs/cypher")
async def graphs_cypher(request: Request, req: CypherRequest = Body(...), write: bool = Query(False)):
    """
    Führt eine (standardmäßig read-only) Cypher-Query aus.
    Schreibende Queries benötigen `GV_ALLOW_WRITES=1` **und** `?write=1`.
    """
    if not HAVE_NEO4J:
        raise HTTPException(status_code=503, detail="neo4j driver not installed")

    if write:
        require_write_auth(request)

    if _is_write_query(req.query) and not (GV_ALLOW_WRITES and write):
        raise HTTPException(status_code=403, detail="write queries are disabled")

    try:
        if _is_write_query(req.query):
            data = _run_write(req.query, req.params or {})
        else:
            data = _run_read(req.query, req.params or {})
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"cypher error: {e!r}")


@app.post("/graphs/load/csv")
async def load_csv_endpoint(request: Request, payload: CsvLoadRequest, write: bool = Query(False)):
    """Dev-Endpoint für Bulk-UPSERT von Person-Rows."""
    if not (GV_ALLOW_WRITES and write):
        return {"ok": False, "reason": "writes_disabled"}
    require_write_auth(request)
    if not HAVE_NEO4J:
        raise HTTPException(status_code=503, detail="neo4j driver not installed")

    rows = [r.model_dump() for r in payload.rows if r.id]
    if not rows:
        return {"ok": True, "nodesCreated": 0, "relsCreated": 0, "rows": 0}

    with neo.get_session() as session:
        neo.run_with_retries(session, CONSTRAINT_CYPHER).consume()
        res = neo.run_with_retries(session, MERGE_BATCH_CYPHER, {"rows": rows})
        summary = res.consume()
        counters = getattr(summary, "counters", None)
        nodes_created = getattr(counters, "nodes_created", 0) if counters else 0
        rels_created = getattr(counters, "relationships_created", 0) if counters else 0

    return {
        "ok": True,
        "nodesCreated": nodes_created,
        "relsCreated": rels_created,
        "rows": len(rows),
    }


@app.get("/graphs/view/ego")
async def graph_view_ego(
    label: str = Query(..., description="Label des Startknotens"),
    key: str = Query(..., description="Eigenschaftsname, z.B. 'id'"),
    value: str = Query(..., description="Eigenschaftswert"),
    depth: int = Query(1, ge=1, le=5, description="Radius der Umgebung"),
    limit: int = Query(1000, ge=1, le=10000, description="Max. Pfade/Ergebnisse"),
):
    """
    Einfache Ego-Netzwerk-Ansicht:
    - Sucht (n:Label {key: $value})
    - Holt Pfade bis `depth` Kanten in beide Richtungen
    - Aggregiert Knoten und Kanten in Nodes/Edges-Listen
    """
    if not HAVE_NEO4J:
        raise HTTPException(status_code=503, detail="neo4j driver not installed")

    _ensure_label(label)
    _ensure_prop(key)
    d = int(depth)
    # Hinweis: variable Längen im Pattern benötigen konstante Obergrenzen → per f-String einsetzen
    cypher = (
        f"MATCH (n:`{label}` {{{key}: $value}})\n"
        f"OPTIONAL MATCH p = (n)-[r*1..{d}]-(m)\n"
        f"RETURN n, collect(p) AS paths\n"
        f"LIMIT $limit"
    )

    try:
        records = _run_read(cypher, {"value": value, "limit": int(limit)})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ego-view error: {e!r}")

    # Aggregation der Paths zu Nodes/Relationships (einfache Serialisierung)
    nodes: Dict[Any, Dict[str, Any]] = {}
    rels: Dict[Any, Dict[str, Any]] = {}

    def add_node(nd: Dict[str, Any]):
        nid = nd.get("id")
        if nid not in nodes:
            nodes[nid] = nd

    def add_rel(rr: Dict[str, Any]):
        rid = rr.get("id")
        if rid not in rels:
            rels[rid] = rr

    for rec in records:
        # rec hat Struktur {"n": {...}, "paths": [path, path, ...]} – je nach Treiber/Serialisierung
        n_ser = rec.get("n")
        if isinstance(n_ser, dict) and n_ser.get("__type") == "node":
            add_node(n_ser)
        paths = rec.get("paths") or []
        if isinstance(paths, list):
            for p in paths:
                if isinstance(p, dict) and p.get("__type") == "path":
                    for nd in p.get("nodes", []):
                        if isinstance(nd, dict) and nd.get("__type") == "node":
                            add_node(nd)
                    for rr in p.get("relationships", []):
                        if isinstance(rr, dict) and rr.get("__type") == "relationship":
                            add_rel(rr)

    return {
        "nodes": [v for v in nodes.values()],
        "relationships": [v for v in rels.values()],
        "count": {"nodes": len(nodes), "relationships": len(rels)},
        "meta": {"label": label, "key": key, "value": value, "depth": d},
    }


@app.get("/graphs/view/shortest-path")
async def graph_view_shortest_path(
    src_label: str = Query(...),
    src_key: str = Query(...),
    src_value: str = Query(...),
    dst_label: str = Query(...),
    dst_key: str = Query(...),
    dst_value: str = Query(...),
    max_len: int = Query(6, ge=1, le=10),
):
    """
    Kürzester Pfad zwischen zwei Knoten.
    Gibt einen Pfad zurück (falls vorhanden) inkl. serialisierter Nodes/Relationships.
    """
    if not HAVE_NEO4J:
        raise HTTPException(status_code=503, detail="neo4j driver not installed")

    _ensure_label(src_label)
    _ensure_label(dst_label)
    _ensure_prop(src_key)
    _ensure_prop(dst_key)

    ml = int(max_len)
    cypher = (
        f"MATCH (a:`{src_label}` {{{src_key}: $src_value}}), (b:`{dst_label}` {{{dst_key}: $dst_value}})\n"
        f"MATCH p = shortestPath((a)-[*..{ml}]-(b))\n"
        f"RETURN p\n"
        f"LIMIT 1"
    )

    try:
        records = _run_read(cypher, {
            "src_value": src_value,
            "dst_value": dst_value,
        })
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"path-view error: {e!r}")

    if not records:
        return {"path": None, "found": False}

    # records[0] erwartet {"p": {...path...}}
    p = records[0].get("p")
    if not (isinstance(p, dict) and p.get("__type") == "path"):
        return {"path": None, "found": False}

    # Dedup
    nodes: Dict[Any, Dict[str, Any]] = {}
    rels: Dict[Any, Dict[str, Any]] = {}
    for nd in p.get("nodes", []):
        if isinstance(nd, dict) and nd.get("__type") == "node":
            nid = nd.get("id")
            if nid not in nodes:
                nodes[nid] = nd
    for rr in p.get("relationships", []):
        if isinstance(rr, dict) and rr.get("__type") == "relationship":
            rid = rr.get("id")
            if rid not in rels:
                rels[rid] = rr

    return {"path": p, "found": True, "nodes": list(nodes.values()), "relationships": list(rels.values())}

