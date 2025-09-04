try:
    from obs.otel_boot import setup_otel  # type: ignore
except Exception:  # pragma: no cover
    def setup_otel(app, service_name: str = "graph-views"):
        return app

import asyncio
import logging
import os
import time
from contextlib import suppress
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from it_logging import setup_logging

SERVICE_DIR = Path(__file__).resolve().parent
PARENT_DIR = SERVICE_DIR.parent
import sys
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from _shared.cors import apply_cors, get_cors_settings_from_env
from _shared.health import make_healthz, make_readyz

from db import (
    build_database_url_from_env,
    create_pool_with_retry,
    close_pool,
    probe_select_1,
    logger as db_logger,
)

app = FastAPI(title="Graph Views API", version="0.1.0")
setup_logging(app, service_name="graph-views")
FastAPIInstrumentor().instrument_app(app)
setup_otel(app)
apply_cors(app, get_cors_settings_from_env())

if os.getenv("IT_ENABLE_METRICS") == "1" or os.getenv("IT_OBSERVABILITY") == "1":
    from starlette_exporter import PrometheusMiddleware, handle_metrics

    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)

app.state.service_name = "graph-views"
app.state.version = os.getenv("GIT_SHA", "dev")
app.state.start_ts = time.monotonic()
app.state.db_pool = None
app.state.db_init_task = None


async def db_init_worker():
    env = os.environ
    dsn = build_database_url_from_env(env)
    pool = await create_pool_with_retry(
        dsn,
        min_size=int(env.get("GV_PG_POOL_MIN_SIZE", "1")),
        max_size=int(env.get("GV_PG_POOL_MAX_SIZE", "5")),
        connect_timeout=float(env.get("GV_PG_CONNECT_TIMEOUT_S", "1.0")),
        max_retries=int(env.get("GV_PG_INIT_MAX_RETRIES", "-1")),
        backoff_base_ms=int(env.get("GV_PG_INIT_BACKOFF_BASE_MS", "200")),
        backoff_max_ms=int(env.get("GV_PG_INIT_BACKOFF_MAX_MS", "2000")),
        logger=db_logger,
    )
    app.state.db_pool = pool


@app.on_event("startup")
async def on_startup():
    app.state.start_ts = time.monotonic()
    app.state.db_init_task = asyncio.create_task(db_init_worker())


@app.on_event("shutdown")
async def on_shutdown():
    task = app.state.db_init_task
    if task:
        task.cancel()
        with suppress(BaseException):
            await task
    await close_pool(app.state.db_pool)
    app.state.db_pool = None



@app.get("/healthz")
def healthz():
    return make_healthz(app.state.service_name, app.state.version, app.state.start_ts)


@app.get("/readyz")
async def readyz():
    checks = {}
    if os.getenv("IT_FORCE_READY") != "1":
        pool = app.state.db_pool
        if pool is None:
            checks["postgres"] = {
                "status": "fail",
                "latency_ms": None,
                "error": "pool_unavailable",
                "reason": None,
            }
        else:
            ok, latency, err = await probe_select_1(pool, float(os.getenv("GV_PG_QUERY_TIMEOUT_S", "0.8")))
            status = "ok" if ok else "fail"
            checks["postgres"] = {
                "status": status,
                "latency_ms": latency,
                "error": err,
                "reason": None,
            }
    payload, status_code = make_readyz(
        app.state.service_name, app.state.version, app.state.start_ts, checks
    )
    return JSONResponse(payload, status_code=status_code)
