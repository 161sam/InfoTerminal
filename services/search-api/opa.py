import os, httpx

OPA_URL = os.getenv("OPA_URL", "http://localhost:8181/v1/data/access/allow")

def allow(user: dict, action: str, resource: dict) -> bool:
    payload = {"input": {"user": user, "action": action, "resource": resource}}
    try:
        with httpx.Client(timeout=3.0) as c:
            r = c.post(OPA_URL, json=payload)
            r.raise_for_status()
            decision = r.json()
            return bool(decision.get("result", False))
    except Exception:
        # fail-open in dev
        return True
