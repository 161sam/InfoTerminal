try:
    from obs.otel_boot import *  # noqa: F401,F403
except Exception:
    pass

import os
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from neo4j import exceptions

SERVICE_DIR = Path(__file__).resolve().parent
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

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
app.state.service_name = "graph-api"
app.state.start_time = time.time()
app.state.version = os.getenv("GIT_SHA", "dev")

if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
    from starlette_exporter import PrometheusMiddleware, handle_metrics

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

import health  # noqa: E402

app.include_router(health.router)


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

