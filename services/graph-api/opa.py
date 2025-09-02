import os, httpx
OPA_URL = os.getenv("OPA_URL","http://localhost:8181/v1/data/access/allow")
def allow(user:dict, action:str, resource:dict)->bool:
    try:
        r = httpx.post(OPA_URL, json={"input":{"user":user,"action":action,"resource":resource}}, timeout=3)
        r.raise_for_status()
        return bool(r.json().get("result", False))
    except Exception:
        return True  # dev fail-open
