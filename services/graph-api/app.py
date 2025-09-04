try:
    from obs.otel_boot import setup_otel  # type: ignore
except Exception:  # pragma: no cover
    def setup_otel(app, service_name: str = "graph-api"):
        return app

import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from it_logging import setup_logging
from neo4j import exceptions
from typing import Dict, Any
from fastapi.responses import JSONResponse

SERVICE_DIR = Path(__file__).resolve().parent
PARENT_DIR = SERVICE_DIR.parent
for p in (SERVICE_DIR, PARENT_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from _shared.health import make_healthz, make_readyz, probe_db
from _shared.cors import apply_cors, get_cors_settings_from_env
from utils.neo4j_client import get_driver, neo_session


NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS") or os.getenv("NEO4J_PASSWORD", "test12345")

driver = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global driver
    driver = get_driver(NEO4J_URI, NEO4J_USER, NEO4J_PASS)
    app.state.driver = driver
    yield
    if driver:
        driver.close()
        app.state.driver = None


app = FastAPI(title="InfoTerminal Graph API", version="0.1.0", lifespan=lifespan)
setup_logging(app, service_name="graph-api")
apply_cors(app, get_cors_settings_from_env())
app.state.service_name = "graph-api"
app.state.start_ts = time.monotonic()
app.state.version = os.getenv("GIT_SHA", "dev")

if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
    from starlette_exporter import PrometheusMiddleware, handle_metrics

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

@app.get("/healthz")
def healthz():
    return make_healthz(app.state.service_name, app.state.version, app.state.start_ts)

@app.get("/readyz")
def readyz(verbose: int = 0):
    checks: Dict[str, Dict[str, Any]] = {}
    if os.getenv("IT_FORCE_READY") != "1":
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASS") or os.getenv("NEO4J_PASSWORD")
        driver = getattr(app.state, "driver", None)
        if uri and user and password and driver:
            def _call():
                with neo_session(driver) as s:
                    s.run("RETURN 1").consume()
            checks["neo4j"] = probe_db(_call)
        else:
            checks["neo4j"] = {"status": "skipped", "latency_ms": None, "error": None, "reason": "missing config"}
    payload, status = make_readyz(app.state.service_name, app.state.version, app.state.start_ts, checks)
    return JSONResponse(payload, status_code=status)



setup_otel(app)


@app.get("/neo4j/ping")
def neo4j_ping():
    if not driver:
        raise HTTPException(503, "driver not ready")
    try:
        with neo_session(driver) as s:
            s.run("RETURN 1").consume()
        return {"result": 1}
    except exceptions.AuthError:
        raise HTTPException(401, "check NEO4J_USER/NEO4J_PASSWORD")


@app.post("/query")
def query(payload: dict):
    if not driver:
        raise HTTPException(503, "driver not ready")
    cypher = payload.get("cypher") or payload.get("query")
    if not cypher:
        raise HTTPException(400, "missing cypher")
    try:
        with neo_session(driver) as s:
            res = s.run(cypher, timeout=5).data()
        return {"results": res}
    except exceptions.AuthError:
        raise HTTPException(401, "check NEO4J_USER/NEO4J_PASSWORD")
    except exceptions.CypherError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@app.get("/neighbors")
def neighbors(node_id: str, limit: int = 20):
    if not driver:
        raise HTTPException(503, "driver not ready")
    with neo_session(driver) as s:
        recs = s.run(
            "MATCH (n {id: $id})-[r]-(m) RETURN n, type(r) as rel, m LIMIT $limit",
            id=node_id,
            limit=limit,
        )
        out = [
            {"from": dict(r["n"]), "rel": r["rel"], "to": dict(r["m"])}
            for r in recs
        ]
    return out

