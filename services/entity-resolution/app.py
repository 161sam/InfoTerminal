try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import make_asgi_app
from pydantic import BaseModel
from rapidfuzz import process, fuzz
from typing import List, Dict, Any

app = FastAPI(title="Entity Resolution v0")
FastAPIInstrumentor().instrument_app(app)
app.mount("/metrics", make_asgi_app())

class MatchReq(BaseModel):
    query: str
    candidates: List[str]
    limit: int = 5
    scorer: str = "token_sort_ratio"  # or "partial_ratio"

SCORERS = {
  "token_sort_ratio": fuzz.token_sort_ratio,
  "partial_ratio": fuzz.partial_ratio,
}

@app.post("/match")
def match(req: MatchReq):
    scorer = SCORERS.get(req.scorer, fuzz.token_sort_ratio)
    res = process.extract(req.query, req.candidates, scorer=scorer, limit=req.limit)
    # res: List[(candidate, score, index)]
    return [{"candidate": c, "score": float(s)} for c, s, _ in res]

class DedupeReq(BaseModel):
    items: List[str]
    threshold: float = 90.0
    scorer: str = "token_sort_ratio"

@app.post("/dedupe")
def dedupe(req: DedupeReq):
    scorer = SCORERS.get(req.scorer, fuzz.token_sort_ratio)
    clusters: List[List[str]] = []
    visited = set()
    for i, x in enumerate(req.items):
        if i in visited: continue
        group=[x]; visited.add(i)
        for j, y in enumerate(req.items[i+1:], start=i+1):
            if j in visited: continue
            if scorer(x,y) >= req.threshold:
                group.append(y); visited.add(j)
        clusters.append(group)
    return {"clusters": clusters}
