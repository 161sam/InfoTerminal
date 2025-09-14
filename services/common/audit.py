import os
import logging
import time

log = logging.getLogger("audit")
SINK = os.getenv("IT_AUDIT_SINK", "stdout")


def audit_log(
    action: str,
    actor: str,
    tenant: str,
    target: dict,
    status: str = "ok",
    extra: dict | None = None,
    req_id: str | None = None,
):
    evt = {
        "ts": int(time.time() * 1000),
        "action": action,
        "actor": actor,
        "tenant": tenant or "default",
        "target": target or {},
        "status": status,
        "request_id": req_id,
        "_type": "audit",
    }
    log.info(evt)
