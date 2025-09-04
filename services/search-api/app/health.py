import os
import time
from datetime import datetime, timezone
from typing import Any, Dict
from urllib import request as urlrequest

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

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
        checks["opensearch"] = {"status": "skipped", "reason": "IT_FORCE_READY"}
    else:
        os_url = os.getenv("OPENSEARCH_URL")
        if os_url:
            start = time.perf_counter()
            try:
                with urlrequest.urlopen(os_url, timeout=0.8) as resp:
                    code = resp.getcode()
                    latency = (time.perf_counter() - start) * 1000
                    if 200 <= code < 300 or code == 401:
                        checks["opensearch"] = {
                            "status": "ok",
                            "latency_ms": round(latency, 2),
                        }
                    else:
                        checks["opensearch"] = {
                            "status": "fail",
                            "code": code,
                        }
                        status = "fail"
            except Exception as e:  # pragma: no cover - network errors
                checks["opensearch"] = {
                    "status": "fail",
                    "reason": str(e),
                }
                status = "fail"
        else:
            checks["opensearch"] = {
                "status": "skipped",
                "reason": "OPENSEARCH_URL not set",
            }

    payload["checks"] = checks
    payload["status"] = status
    http_status = 200 if status == "ok" else 503
    return JSONResponse(payload, status_code=http_status)
