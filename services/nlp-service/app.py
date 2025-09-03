import os
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import importlib.util
from pathlib import Path

SERVICE_DIR = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("nlp_metrics", SERVICE_DIR / "metrics.py")
_metrics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_metrics)  # type: ignore
NLP_REQS = _metrics.NLP_REQS
NLP_LATENCY = _metrics.NLP_LATENCY

app = FastAPI()
instrumentator = Instrumentator().instrument(app)


@app.on_event("startup")
async def _startup() -> None:
    instrumentator.expose(app, include_in_schema=False, should_gzip=True)

# Lazy holders for NLP models
_nlp = None
_summarizer = None


def get_nlp():
    global _nlp
    if _nlp is None:
        if os.getenv("ALLOW_TEST_MODE"):
            # In test mode, use a dummy implementation
            _nlp = True  # sentinel
        else:
            import spacy
            _nlp = spacy.load("en_core_web_sm")
    return _nlp


def get_summarizer():
    global _summarizer
    if _summarizer is None:
        if os.getenv("ALLOW_TEST_MODE"):
            _summarizer = True  # sentinel
        else:
            from transformers import pipeline
            _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    return _summarizer


class TextRequest(BaseModel):
    text: str


@app.post("/ner")
async def ner_endpoint(payload: TextRequest):
    NLP_REQS.labels(type="ner").inc()
    with NLP_LATENCY.labels(type="ner").time():
        nlp = get_nlp()
        text = payload.text
        if os.getenv("ALLOW_TEST_MODE"):
            first = text.split()[0] if text.split() else ""
            return {"entities": [{"text": first, "label": "TEST", "start": 0, "end": len(first)}]}
        doc = nlp(text)
        entities: List[dict] = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
            })
        return {"entities": entities}


@app.post("/summarize")
async def summarize_endpoint(payload: TextRequest):
    NLP_REQS.labels(type="summarize").inc()
    with NLP_LATENCY.labels(type="summarize").time():
        summarizer = get_summarizer()
        text = payload.text
        if os.getenv("ALLOW_TEST_MODE"):
            summary = " ".join(text.split()[:5])
            return {"summary": summary}
        result = summarizer(text)
        return {"summary": result[0]["summary_text"]}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
