from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import structlog

logger = structlog.get_logger()

app = FastAPI(title="XAI Toolkit", version="0.1.0")


class ExplainRequest(BaseModel):
    text: str
    query: str | None = None


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.post("/explain/text")
def explain_text(req: ExplainRequest):
    text = req.text or ""
    query = (req.query or "").lower()
    tokens = [t for t in text.split() if t]
    highlights: List[Dict] = []
    if query:
        q_tokens = [qt for qt in query.split() if len(qt) > 2]
        for i, tok in enumerate(tokens):
            low = tok.lower().strip('.,;:()[]{}"\'')
            if any(qt in low for qt in q_tokens):
                highlights.append({"index": i, "token": tok, "reason": "query_match"})
    # naive heuristics: dates and amounts
    for i, tok in enumerate(tokens):
        if any(c.isdigit() for c in tok) and any(ch in tok for ch in ['/', '-', '.']):
            highlights.append({"index": i, "token": tok, "reason": "looks_like_date"})
        if tok.replace(',', '').replace('.', '').isdigit():
            highlights.append({"index": i, "token": tok, "reason": "numeric_value"})
    explanation = {
        "tokens": tokens,
        "highlights": highlights,
        "meta": {"method": "heuristic", "confidence": 0.5}
    }
    return explanation


@app.get("/model-card")
def model_card():
    return {
        "name": "Heuristic Explainer v0.1",
        "description": "Simple token highlight explainer for text",
        "intended_use": "Explain why certain terms matched or stand out",
        "limitations": ["Heuristic only", "No semantic understanding"],
        "metrics": {"explainability": "low", "confidence": 0.5}
    }

