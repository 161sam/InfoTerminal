import os
import time
import os
import time
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from metrics import READYZ_LATENCY

router = APIRouter()


def _base_payload(request: Request) -> Dict[str, Any]:
    service = request.app.state.service_name
    version = getattr(request.app.state, "version", os.getenv("GIT_SHA", "dev"))
    start_time = getattr(request.app.state, "start_time", time.time())
    return {
        "status": "ok",
        "service": service,
        "version": version,
        "time": datetime.now(timezone.utc).isoformat(),
        "uptime_s": time.time() - start_time,
    }


@router.get("/healthz")
def healthz(request: Request):
    payload = _base_payload(request)
    return JSONResponse(payload)


@router.get("/readyz")
def readyz(request: Request):
    payload = _base_payload(request)
    checks: Dict[str, Any] = {}
    status = "ok"
    start_total = time.perf_counter()

    if os.getenv("IT_FORCE_READY") == "1":
        checks["postgres"] = {"status": "skipped", "reason": "IT_FORCE_READY"}
    else:
        pool = getattr(request.app.state, "pool", None)
        if pool:
            start = time.perf_counter()
            conn = None
            try:
                conn = pool.getconn()
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                latency = (time.perf_counter() - start) * 1000
                checks["postgres"] = {
                    "status": "ok",
                    "latency_ms": round(latency, 2),
                }
            except Exception as e:  # pragma: no cover - network errors
                checks["postgres"] = {
                    "status": "fail",
                    "reason": str(e),
                }
                status = "fail"
            finally:
                if conn:
                    pool.putconn(conn)
        else:
            checks["postgres"] = {
                "status": "skipped",
                "reason": "PG pool not initialised",
            }

    payload["checks"] = checks
    payload["status"] = status
    http_status = 200 if status == "ok" else 503
    duration = time.perf_counter() - start_total
    READYZ_LATENCY.labels(request.app.state.service_name).observe(duration)
    return JSONResponse(payload, status_code=http_status)
