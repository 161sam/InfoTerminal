import os
import re
import asyncio
import time
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Body, Query, Request
from pydantic import BaseModel

from response import ok, err, bool_qp, safe_counts
from rate_limit import TokenBucket, parse_rate
from audit import log_event, new_request_id

from _shared.cors import apply_cors
from _shared.health import make_healthz, make_readyz
from starlette_exporter import PrometheusMiddleware, handle_metrics
from common.request_id import RequestIdMiddleware
from _shared.obs.otel_boot import setup_otel
from it_logging import setup_logging
from ontology.api import router as ontology_router
from dossier.api import router as dossier_router
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    if HAVE_NEO4J:
        try:
            neo.get_driver()
        except Exception:
            pass
    yield
    if HAVE_NEO4J:
        try:
            neo.get_driver().close()
        except Exception:
            pass


# -----------------------
# FastAPI-App
# -----------------------
app = FastAPI(title="graph-views", lifespan=lifespan)
setup_logging(app, service_name="graph-views")
apply_cors(app)
app.add_middleware(RequestIdMiddleware)
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)
setup_otel(app)
app.include_router(ontology_router)
app.include_router(dossier_router)

app.state.rate_cfg = os.getenv("GV_RATE_LIMIT_WRITE", "")
app.state.rate_cap, app.state.rate_refill = parse_rate(app.state.rate_cfg)
app.state.rate_buckets = {}

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


@app.middleware("http")
async def write_guard_and_rate(request, call_next):
    rid = new_request_id()
    start = time.time()
    is_write = request.url.query.find("write=1") >= 0 or bool_qp(request.query_params.get("write"))
    response = None
    try:
        if is_write and app.state.rate_cap > 0:
            ip = request.headers.get("x-forwarded-for") or (request.client.host if request.client else None)
            bucket = app.state.rate_buckets.get(ip)
            if not bucket:
                bucket = app.state.rate_buckets[ip] = TokenBucket(app.state.rate_cap, app.state.rate_refill)
            ok_take, remaining, reset = bucket.take()
            if not ok_take:
                body, status = err("rate_limited", "Write rate limit exceeded", 429)
                from fastapi.responses import JSONResponse
                response = JSONResponse(content=body, status_code=status)
                response.headers["Retry-After"] = str(int(reset))
                response.headers["X-RateLimit-Limit"] = str(app.state.rate_cap)
                response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
                response.headers["X-RateLimit-Reset"] = str(int(reset))
                response.headers["X-Request-ID"] = rid
                return response

        response = await call_next(request)
        return response
    finally:
        if response is not None:
            response.headers["X-Request-ID"] = rid
        if is_write:
            log_event(
                {
                    "ts": int(time.time() * 1000),
                    "request_id": rid,
                    "route": str(request.url.path),
                    "ip": request.headers.get("x-forwarded-for")
                    or (request.client.host if request.client else None),
                    "user": request.headers.get("authorization", "").split()[1][:8] + "..."
                    if request.headers.get("authorization")
                    else None,
                    "write": True,
                    "status": response.status_code if response else None,
                    "latency_ms": int((time.time() - start) * 1000),
                }
            )

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


def _run_write(query: str, params: Dict[str, Any]):
    with neo.get_session() as session:
        result = neo.run_with_retries(session, query, params)
        records = [_serialize_neo4j(r.data()) for r in result]
        summary = result.consume()
        counters = getattr(summary, "counters", None)
        return records, counters


def _is_write_query(q: str) -> bool:
    ql = q.strip().lower()
    # naive Heuristik – reicht für Absicherung im Dienst
    write_tokens = ("create ", "merge ", "delete ", "set ", "remove ", "drop ")
    return any(tok in ql for tok in write_tokens)


# -----------------------
# API Modelle
# -----------------------
class CypherRequest(BaseModel):
    stmt: Optional[str] = None
    query: Optional[str] = None
    params: Dict[str, Any] | None = None

    @property
    def text(self) -> str:
        return self.stmt or self.query or ""


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


# Helper for ego view
async def _ego_view_data(label: str, key: str, value: str, depth: int, limit: int):
    """
    Reuse the same cypher/session logic as /graphs/view/ego and
    return a dict: {"nodes":[...], "relationships":[...]}
    """
    if not HAVE_NEO4J:
        raise HTTPException(status_code=503, detail="neo4j driver not installed")

    _ensure_label(label)
    _ensure_prop(key)
    d = int(depth)
    cypher = (
        f"MATCH (n:`{label}` {{{key}: $value}})\n"
        f"OPTIONAL MATCH p = (n)-[r*1..{d}]-(m)\n"
        f"RETURN n, collect(p) AS paths\n"
        f"LIMIT $limit"
    )
    records = _run_read(cypher, {"value": value, "limit": int(limit)})

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

    return {"nodes": list(nodes.values()), "relationships": list(rels.values())}

# -----------------------
# Graph-Views Routen
# -----------------------
@app.get("/graphs/ping")
async def graphs_ping():
    """Liefert Info zum Neo4j-Backend (optional)."""
    if not HAVE_NEO4J:
        return ok({"neo4j": "driver-not-installed", "configured": False})
    try:
        neo.get_driver()
    except Exception:
        return ok({"neo4j": "not-configured", "configured": False})
    ready = await _neo4j_ready()
    return ok({"neo4j": "ok" if ready else "unreachable", "configured": True})


@app.post("/graphs/cypher")
async def graphs_cypher(request: Request, req: CypherRequest = Body(...), write: bool = Query(False)):
    """
    Führt eine (standardmäßig read-only) Cypher-Query aus.
    Schreibende Queries benötigen `GV_ALLOW_WRITES=1` **und** `?write=1`.
    """
    from fastapi.responses import JSONResponse

    if not HAVE_NEO4J:
        body, status = err("server_error", "neo4j driver not installed", 503)
        return JSONResponse(content=body, status_code=status)

    if write and not GV_ALLOW_WRITES:
        body, status = err("writes_disabled", "write queries are disabled", 403)
        return JSONResponse(content=body, status_code=status)

    if write:
        try:
            require_write_auth(request)
        except HTTPException as e:
            body, status = err("unauthorized", e.detail, e.status_code)
            response = JSONResponse(content=body, status_code=status)
            if e.headers:
                for k, v in e.headers.items():
                    response.headers[k] = v
            return response

    q = req.text
    if not q:
        body, status = err("bad_request", "query missing", 400)
        return JSONResponse(content=body, status_code=status)

    is_write_query = _is_write_query(q)
    if is_write_query and not (GV_ALLOW_WRITES and write):
        body, status = err("writes_disabled", "write queries are disabled", 403)
        return JSONResponse(content=body, status_code=status)

    try:
        if is_write_query:
            records, counters = _run_write(q, req.params or {})
            return ok({"records": records}, counts=safe_counts(counters))
        records = _run_read(q, req.params or {})
        return ok({"records": records})
    except Exception as e:
        body, status = err("server_error", f"cypher error: {e}", 500)
        return JSONResponse(content=body, status_code=status)


@app.post("/graphs/load/csv")
async def load_csv_endpoint(request: Request, payload: CsvLoadRequest, write: bool = Query(False)):
    """Dev-Endpoint für Bulk-UPSERT von Person-Rows."""
    from fastapi.responses import JSONResponse

    if not (GV_ALLOW_WRITES and write):
        body, status = err("writes_disabled", "writes disabled", 403)
        return JSONResponse(content=body, status_code=status)

    try:
        require_write_auth(request)
    except HTTPException as e:
        body, status = err("unauthorized", e.detail, e.status_code)
        response = JSONResponse(content=body, status_code=status)
        if e.headers:
            for k, v in e.headers.items():
                response.headers[k] = v
        return response

    if not HAVE_NEO4J:
        body, status = err("server_error", "neo4j driver not installed", 503)
        return JSONResponse(content=body, status_code=status)

    rows = [r.model_dump() for r in payload.rows if r.id]
    if not rows:
        return ok({"rows": 0}, counts={"nodes": 0, "relationships": 0})

    try:
        with neo.get_session() as session:
            neo.run_with_retries(session, CONSTRAINT_CYPHER).consume()
            res = neo.run_with_retries(session, MERGE_BATCH_CYPHER, {"rows": rows})
            summary = res.consume()
            counters = getattr(summary, "counters", None)
            nodes_created = getattr(counters, "nodes_created", 0) if counters else 0
            rels_created = getattr(counters, "relationships_created", 0) if counters else 0
    except Exception as e:
        body, status = err("server_error", f"csv load error: {e}", 500)
        return JSONResponse(content=body, status_code=status)

    return ok({"rows": len(rows)}, counts={"nodes": nodes_created, "relationships": rels_created})


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
    from fastapi.responses import JSONResponse
    try:
        data = await _ego_view_data(label, key, value, depth, limit)
    except HTTPException as e:
        body, status = err("bad_request", e.detail, e.status_code)
        return JSONResponse(content=body, status_code=status)
    except Exception as e:
        body, status = err("server_error", f"ego-view error: {e}", 500)
        return JSONResponse(content=body, status_code=status)
    counts = {"nodes": len(data["nodes"]), "relationships": len(data["relationships"])}
    data["meta"] = {"label": label, "key": key, "value": value, "depth": int(depth)}
    return ok({"nodes": data["nodes"], "relationships": data["relationships"], "meta": data["meta"]}, counts=counts)


@app.get("/graphs/view/shortest-path")
async def graph_view_shortest_path(request: Request):
    """
    Kürzester Pfad zwischen zwei Knoten.
    Gibt einen Pfad zurück (falls vorhanden) inkl. serialisierter Nodes/Relationships.
    """
    if not HAVE_NEO4J:
        from fastapi.responses import JSONResponse
        body, status = err("server_error", "neo4j driver not installed", 503)
        return JSONResponse(content=body, status_code=status)

    qp = request.query_params
    src_label = qp.get("srcLabel") or qp.get("src_label")
    src_key = qp.get("srcKey") or qp.get("src_key")
    src_value = qp.get("srcValue") or qp.get("src_value")
    dst_label = qp.get("dstLabel") or qp.get("dst_label")
    dst_key = qp.get("dstKey") or qp.get("dst_key")
    dst_value = qp.get("dstValue") or qp.get("dst_value")
    max_len = qp.get("maxLen") or qp.get("max_len")
    if max_len is None:
        ml = 6
    else:
        ml = int(max_len)

    if not all([src_label, src_key, src_value, dst_label, dst_key, dst_value]):
        from fastapi.responses import JSONResponse
        body, status = err("bad_request", "missing parameters", 400)
        return JSONResponse(content=body, status_code=status)

    from fastapi.responses import JSONResponse
    try:
        _ensure_label(src_label)
        _ensure_label(dst_label)
        _ensure_prop(src_key)
        _ensure_prop(dst_key)
    except HTTPException as e:
        body, status = err("bad_request", e.detail, e.status_code)
        return JSONResponse(content=body, status_code=status)

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
    except Exception as e:
        from fastapi.responses import JSONResponse
        body, status = err("server_error", f"path-view error: {e}", 500)
        return JSONResponse(content=body, status_code=status)

    if not records:
        return ok({"path": None, "found": False, "nodes": [], "relationships": []}, counts={"nodes": 0, "relationships": 0})

    p = records[0].get("p")
    if not (isinstance(p, dict) and p.get("__type") == "path"):
        return ok({"path": None, "found": False, "nodes": [], "relationships": []}, counts={"nodes": 0, "relationships": 0})

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

    data = {"path": p, "found": True, "nodes": list(nodes.values()), "relationships": list(rels.values())}
    counts = {"nodes": len(nodes), "relationships": len(rels)}
    return ok(data, counts=counts)


@app.get("/graphs/export/dossier")
async def export_dossier(label: str, key: str, value: str, depth: int = 2, limit: int = 100):
    from fastapi.responses import JSONResponse
    try:
        data = await _ego_view_data(label, key, value, depth, limit)
        raw_nodes = data.get("nodes", [])
        raw_rels  = data.get("relationships", [])
        nodes = [{
            "id": n.get("id") or n.get("identity") or n.get("uid"),
            "labels": n.get("labels") or n.get("label") or [],
            "props": n.get("properties") or n
        } for n in raw_nodes]
        edges = [{
            "id": r.get("id") or f"{r.get('start')}-{r.get('type')}-{r.get('end')}",
            "source": r.get("start") or r.get("source"),
            "target": r.get("end") or r.get("target"),
            "type": r.get("type") or r.get("label") or "RELATIONSHIP",
            "props": r.get("properties") or r
        } for r in raw_rels]
        return ok({"nodes": nodes, "edges": edges}, counts={"nodes": len(nodes), "relationships": len(edges)})
    except HTTPException as e:
        body, status = err("bad_request", e.detail, e.status_code)
        return JSONResponse(content=body, status_code=status)
    except Exception as e:
        body, status = err("server_error", f"export failed: {e}", 500)
        return JSONResponse(content=body, status_code=status)

