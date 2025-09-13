try:
    from obs.otel_boot import setup_otel  # type: ignore
except Exception:  # pragma: no cover
    def setup_otel(app, service_name: str = "doc-entities"):
        return app

import html
import json
import os
import uuid
from typing import Any, Dict, List, Optional
import sys
from pathlib import Path

from fastapi import BackgroundTasks, FastAPI, HTTPException
from starlette_exporter import PrometheusMiddleware, handle_metrics
from common.request_id import RequestIdMiddleware
import importlib.util
from pathlib import Path
from nlp_loader import ner_spacy, summarize

SERVICE_DIR = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("doc_entities_metrics", SERVICE_DIR / "metrics.py")
_metrics = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_metrics)  # type: ignore
RESOLVER_RUNS = _metrics.RESOLVER_RUNS
RESOLVER_ENTS = _metrics.RESOLVER_ENTS
RESOLVER_LAT = _metrics.RESOLVER_LAT
from pydantic import BaseModel


class NERIn(BaseModel):
    text: str
    lang: str = "en"


class Entity(BaseModel):
    text: str
    label: str
    start: int
    end: int


class NEROut(BaseModel):
    entities: List[Entity]
    model: str


class TextIn(BaseModel):
    text: str
    lang: str = "en"


class RelIn(BaseModel):
    text: str
    lang: str = "en"


ALLOW_TEST = os.getenv("ALLOW_TEST_MODE")
SERVICE_DIR = Path(__file__).resolve().parent
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from db import SessionLocal, engine  # type: ignore
from models import Base, Document, Entity, EntityResolution  # type: ignore
from resolver import resolve_entities  # type: ignore
from nlp_client import ner as nlp_ner

if not ALLOW_TEST:
    Base.metadata.create_all(engine)

GRAPH_URL = os.getenv("GRAPH_UI", "http://localhost:3000/graphx")

app = FastAPI(title="Doc Entities", version="0.1.0")
app.add_middleware(RequestIdMiddleware)
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)
setup_otel(app)




class AnnotReq(BaseModel):
    text: str
    doc_id: Optional[str] = None
    title: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None


@app.get("/healthz")
def health() -> Dict[str, str]:
    """Simple health-check endpoint."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> Dict[str, str]:
    return {"ok": True}


@app.post("/ner", response_model=NEROut)
def ner(inp: NERIn):
    ents = ner_spacy(inp.text, inp.lang)
    return NEROut(entities=[Entity(**e) for e in ents], model="spaCy")


@app.post("/summary")
def summary(inp: TextIn):
    return {"summary": summarize(inp.text, inp.lang)}


@app.post("/relations")
def relations(inp: RelIn):
    return {"relations": []}


@app.post("/annotate")
def annotate(req: AnnotReq, resolve: int = 0, background_tasks: BackgroundTasks = None):
    doc_id = req.doc_id or str(uuid.uuid4())
    meta = req.meta or {}
    if ALLOW_TEST:
        ents = []
        if req.text.split():
            ent_id = str(uuid.uuid4())
            word = req.text.split()[0]
            context = _context(req.text, 0, len(word))
            ents.append(
                {
                    "id": ent_id,
                    "label": "TEST",
                    "value": word,
                    "span_start": 0,
                    "span_end": len(word),
                    "context": context,
                    "resolution": {"status": "pending", "node_id": None, "score": None},
                }
            )
        MEM_TEXTS[doc_id] = {"title": req.title, "text": req.text, "meta": meta}
        MEM_ENTS[doc_id] = ents
        entity_ids = [e["id"] for e in ents]
    else:
        with SessionLocal() as db:
            doc = Document(id=uuid.UUID(doc_id), title=req.title, aleph_id=meta.get("aleph_id"))
            db.merge(doc)
            ner_res = nlp_ner(req.text)
            ents = []
            entity_ids = []
            for e in ner_res:
                context = _context(req.text, e.get("start"), e.get("end"))
                ent = Entity(
                    doc_id=doc.id,
                    label=e.get("label", ""),
                    value=e.get("text", ""),
                    span_start=e.get("start"),
                    span_end=e.get("end"),
                    confidence=e.get("score"),
                    context=context,
                )
                db.add(ent)
                db.flush()
                res = EntityResolution(entity_id=ent.id, status="pending")
                db.add(res)
                ents.append(
                    {
                        "id": str(ent.id),
                        "label": ent.label,
                        "value": ent.value,
                        "span_start": ent.span_start,
                        "span_end": ent.span_end,
                        "context": context,
                        "resolution": {"status": "pending", "node_id": None, "score": None},
                    }
                )
                entity_ids.append(str(ent.id))
            db.commit()
    if resolve and entity_ids and background_tasks:
        background_tasks.add_task(resolve_entities, entity_ids)
    return {"doc_id": doc_id, "entities": ents, "aleph_id": meta.get("aleph_id")}


@app.get("/docs/{doc_id}")
def get_doc(doc_id: str):
    if ALLOW_TEST:
        info = MEM_TEXTS.get(doc_id)
        if not info:
            raise HTTPException(404, "not found")
        ents = MEM_ENTS.get(doc_id, [])
        return {
            "doc_id": doc_id,
            "title": info.get("title"),
            "text": info.get("text"),
            "meta": info.get("meta"),
            "entities": ents,
            "aleph_id": (info.get("meta") or {}).get("aleph_id"),
        }
    with SessionLocal() as db:
        doc = db.get(Document, uuid.UUID(doc_id))
        if not doc:
            raise HTTPException(404, "not found")
        ents = []
        for ent in db.query(Entity).filter_by(doc_id=doc.id).all():
            res = db.get(EntityResolution, ent.id)
            ents.append(
                {
                    "id": str(ent.id),
                    "label": ent.label,
                    "value": ent.value,
                    "span_start": ent.span_start,
                    "span_end": ent.span_end,
                    "context": ent.context,
                    "resolution": {
                        "status": res.status if res else "pending",
                        "node_id": res.node_id if res else None,
                        "score": res.score if res else None,
                    },
                }
            )
        return {
            "doc_id": doc_id,
            "title": doc.title,
            "text": None,
            "meta": None,
            "entities": ents,
            "aleph_id": doc.aleph_id,
        }


@app.post("/resolve/{doc_id}")
def resolve_doc(doc_id: str):
    raise HTTPException(status_code=501, detail="resolver not implemented")


@app.post("/resolve/entity/{entity_id}")
def resolve_entity(entity_id: str):
    raise HTTPException(status_code=501, detail="resolver not implemented")


def _decorate(text: str, entities: List[Dict[str, Any]]):
    spans = []
    for e in entities:
        res = e.get("resolution", {})
        if res.get("node_id"):
            spans.append((e.get("span_start"), e.get("span_end"), e.get("value"), res["node_id"]))
    if not spans:
        out = html.escape(text)
        for e in entities:
            res = e.get("resolution", {})
            if res.get("node_id"):
                t = html.escape(e.get("value", ""))
                nid = res["node_id"]
                out = out.replace(t, f'<a class="ent" href="{GRAPH_URL}?focus={nid}" title="open in graph">{t}</a>')
        return out
    spans = sorted([s for s in spans if s[0] is not None and s[1] is not None], key=lambda x: x[0])
    out, cur = [], 0
    for s, e, txt, nid in spans:
        s = max(0, s)
        e = min(len(text), e or s)
        out.append(html.escape(text[cur:s]))
        out.append(
            f'<a class="ent" href="{GRAPH_URL}?focus={html.escape(nid)}" title="open in graph">{html.escape(text[s:e])}</a>'
        )
        cur = e
    out.append(html.escape(text[cur:]))
    return "".join(out)


def _context(text: str, start: Optional[int], end: Optional[int], width: int = 30) -> str:
    if start is None or end is None:
        return ""
    s = max(0, start - width)
    e = min(len(text), end + width)
    return text[s:e]


@app.get("/docs/{doc_id}/html")
def get_doc_html(doc_id: str):
    d = get_doc(doc_id)
    body = _decorate(d.get("text", ""), d.get("entities", []))
    title = html.escape(d.get("title") or d["doc_id"])
    html_doc = f"""<!doctype html>
  <html><head><meta charset=\"utf-8\"><title>{title}</title>
  <style> body{{font:14px ui-sans-serif; max-width:860px; margin:24px auto;}}
  .ent{{background:#fffae6; padding:1px 3px; border-radius:3px; text-decoration:none; border-bottom:1px dotted #888;}}</style>
  </head><body><h1>{title}</h1><div>{body}</div></body></html>"""
    return html_doc


if ALLOW_TEST:
    MEM_TEXTS: Dict[str, Dict[str, Any]] = {}
    MEM_ENTS: Dict[str, List[Dict[str, Any]]] = {}
