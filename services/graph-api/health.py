import os
import time
from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from neo4j import exceptions as neo_exceptions

from utils.neo4j_client import neo_session

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

    if os.getenv("IT_FORCE_READY") == "1":
        checks["neo4j"] = {"status": "skipped", "reason": "IT_FORCE_READY"}
    else:
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASS") or os.getenv("NEO4J_PASSWORD")
        driver = getattr(request.app.state, "driver", None)
        if uri and user and password and driver:
            start = time.perf_counter()
            try:
                with neo_session(driver) as s:
                    s.run("RETURN 1").consume()
                latency = (time.perf_counter() - start) * 1000
                checks["neo4j"] = {
                    "status": "ok",
                    "latency_ms": round(latency, 2),
                }
            except neo_exceptions.AuthError:
                checks["neo4j"] = {"status": "fail", "reason": "auth"}
                status = "fail"
            except Exception as e:  # pragma: no cover - network errors
                checks["neo4j"] = {
                    "status": "fail",
                    "reason": str(e),
                }
                status = "fail"
        else:
            checks["neo4j"] = {
                "status": "skipped",
                "reason": "NEO4J configuration missing",
            }

    payload["checks"] = checks
    payload["status"] = status
    http_status = 200 if status == "ok" else 503
    return JSONResponse(payload, status_code=http_status)
