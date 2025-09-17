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

# Fuzzy matching integration
from fuzzy_matcher import FuzzyMatcher, MatchRequest, DedupeRequest, EntityDeduplicator


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
    doc_id: Optional[str] = None
    extract_new: bool = True


ALLOW_TEST = os.getenv("ALLOW_TEST_MODE")
SERVICE_DIR = Path(__file__).resolve().parent
if str(SERVICE_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICE_DIR))

from db import SessionLocal, engine  # type: ignore
from models import Base, Document, Entity, EntityResolution, Relation, RelationResolution  # type: ignore
from resolver import resolve_entities  # type: ignore
from nlp_client import ner as nlp_ner
from relation_extractor import extract_relations  # type: ignore

if not ALLOW_TEST:
    Base.metadata.create_all(engine)

GRAPH_URL = os.getenv("GRAPH_UI", "http://localhost:3000/graphx")
GRAPH_WRITE_RELATIONS = os.getenv("GRAPH_WRITE_RELATIONS", "0") == "1"

app = FastAPI(title="Doc Entities", version="0.1.0")
app.add_middleware(RequestIdMiddleware)
if os.getenv("IT_ENABLE_METRICS") == "1":
    app.add_middleware(PrometheusMiddleware)
    app.add_route("/metrics", handle_metrics)
setup_otel(app)




class AnnotReq(BaseModel):
    text: str
    lang: str = "en"
    doc_id: Optional[str] = None
    title: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    do_summary: bool = False
    extract_relations: bool = True


class LinkReq(BaseModel):
    doc_id: str
    entities: List[Dict[str, Any]]


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


@app.post("/match")
def fuzzy_match(req: MatchRequest):
    """
    Fuzzy string matching using RapidFuzz.
    Integrated from entity-resolution service.
    """
    try:
        results = FuzzyMatcher.match(req)
        return {
            "query": req.query,
            "matches": [{
                "candidate": r.candidate,
                "score": r.score,
                "index": r.index
            } for r in results],
            "scorer": req.scorer,
            "total_candidates": len(req.candidates),
            "returned_matches": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fuzzy matching failed: {str(e)}")


@app.post("/dedupe")
def fuzzy_dedupe(req: DedupeRequest):
    """
    String deduplication using fuzzy clustering.
    Integrated from entity-resolution service.
    """
    try:
        result = FuzzyMatcher.dedupe(req)
        return {
            "clusters": result.clusters,
            "total_items": result.total_items,
            "unique_clusters": result.unique_clusters,
            "deduplication_ratio": result.deduplication_ratio,
            "threshold": req.threshold,
            "scorer": req.scorer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deduplication failed: {str(e)}")


@app.post("/entities/dedupe")
def dedupe_entities(entities: List[Dict[str, Any]], threshold: float = 85.0, key_field: str = "value"):
    """
    Deduplicate entity list using fuzzy matching.
    Enhanced functionality combining NLP and fuzzy matching.
    """
    try:
        result = EntityDeduplicator.dedupe_entities(entities, threshold, key_field)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity deduplication failed: {str(e)}")


@app.post("/relations")
def relations(inp: RelIn):
    """Extract relations from text or retrieve stored relations for a document."""
    if inp.doc_id and not inp.extract_new:
        # Retrieve stored relations for existing document
        if ALLOW_TEST:
            # Return test data
            return {"relations": [
                {
                    "subject": "John Smith",
                    "predicate": "WORKS_AT", 
                    "object": "Apple Inc",
                    "confidence": 0.85,
                    "extraction_method": "pattern_match"
                }
            ]}
        else:
            with SessionLocal() as db:
                doc = db.get(Document, uuid.UUID(inp.doc_id))
                if not doc:
                    raise HTTPException(404, "Document not found")
                
                relations = db.query(Relation).filter_by(doc_id=doc.id).all()
                result = []
                
                for relation in relations:
                    # Get entity details
                    subject_entity = db.get(Entity, relation.subject_entity_id)
                    object_entity = db.get(Entity, relation.object_entity_id)
                    
                    if subject_entity and object_entity:
                        result.append({
                            "id": str(relation.id),
                            "subject": subject_entity.value,
                            "subject_label": subject_entity.label,
                            "subject_entity_id": str(relation.subject_entity_id),
                            "predicate": relation.predicate,
                            "predicate_text": relation.predicate_text,
                            "object": object_entity.value,
                            "object_label": object_entity.label,
                            "object_entity_id": str(relation.object_entity_id),
                            "confidence": relation.confidence,
                            "span_start": relation.span_start,
                            "span_end": relation.span_end,
                            "context": relation.context,
                            "extraction_method": relation.extraction_method,
                            "created_at": relation.created_at.isoformat() if relation.created_at else None
                        })
                
                return {"relations": result}
    
    else:
        # Extract relations from provided text
        # First extract entities if not provided with text
        ner_result = ner_spacy(inp.text, inp.lang)
        entities = [
            {
                "id": str(uuid.uuid4()),
                "text": ent["text"],
                "label": ent["label"],
                "span_start": ent["start"],
                "span_end": ent["end"],
                "value": ent["text"]
            }
            for ent in ner_result
        ]
        
        if len(entities) < 2:
            return {"relations": []}
        
        # Extract relations
        extracted_relations = extract_relations(inp.text, entities)
        
        # Format for response
        result = []
        for rel in extracted_relations:
            # Find entity details
            subject_entity = next((e for e in entities if e["id"] == rel["subject_entity_id"]), None)
            object_entity = next((e for e in entities if e["id"] == rel["object_entity_id"]), None)
            
            if subject_entity and object_entity:
                result.append({
                    "subject": subject_entity["value"],
                    "subject_label": subject_entity["label"],
                    "predicate": rel["predicate"],
                    "predicate_text": rel.get("predicate_text", ""),
                    "object": object_entity["value"],
                    "object_label": object_entity["label"],
                    "confidence": rel.get("confidence", 0.5),
                    "span_start": rel.get("span_start"),
                    "span_end": rel.get("span_end"),
                    "context": rel.get("context", ""),
                    "extraction_method": rel.get("extraction_method", "unknown"),
                    "metadata": rel.get("metadata", {})
                })
        
        return {"relations": result}


@app.post("/annotate")
def annotate(req: AnnotReq, resolve: int = 0, background_tasks: BackgroundTasks = None):
    """Combine NER, relation extraction and optional summary.

    Returns HTML with highlighted entities alongside the raw entity and
    relation lists. In non-test mode the document and entities are
    persisted just like the legacy implementation."""

    doc_id = req.doc_id or str(uuid.uuid4())
    meta = req.meta or {}
    
    if ALLOW_TEST:
        ents: List[Dict[str, Any]] = []
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
        
        # Extract relations in test mode
        relations = []
        if req.extract_relations and len(ents) >= 2:
            extracted_relations = extract_relations(req.text, ents)
            for rel in extracted_relations:
                relations.append({
                    "subject": rel.get("subject_entity_id", ""),
                    "predicate": rel.get("predicate", "RELATED_TO"),
                    "object": rel.get("object_entity_id", ""),
                    "confidence": rel.get("confidence", 0.5),
                    "extraction_method": rel.get("extraction_method", "test")
                })
        
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
            
            # Extract and store relations
            relations = []
            if req.extract_relations and len(ents) >= 2:
                extracted_relations = extract_relations(req.text, ents)
                
                for rel in extracted_relations:
                    # Create relation record
                    relation_obj = Relation(
                        doc_id=doc.id,
                        subject_entity_id=uuid.UUID(rel["subject_entity_id"]),
                        object_entity_id=uuid.UUID(rel["object_entity_id"]),
                        predicate=rel["predicate"],
                        predicate_text=rel.get("predicate_text"),
                        confidence=rel.get("confidence"),
                        span_start=rel.get("span_start"),
                        span_end=rel.get("span_end"),
                        context=rel.get("context"),
                        extraction_method=rel.get("extraction_method"),
                        metadata=rel.get("metadata")
                    )
                    db.add(relation_obj)
                    db.flush()
                    
                    # Create relation resolution record
                    rel_resolution = RelationResolution(
                        relation_id=relation_obj.id,
                        status="pending"
                    )
                    db.add(rel_resolution)
                    
                    # Format for response
                    subject_entity = next((e for e in ents if e["id"] == rel["subject_entity_id"]), None)
                    object_entity = next((e for e in ents if e["id"] == rel["object_entity_id"]), None)
                    
                    if subject_entity and object_entity:
                        relations.append({
                            "id": str(relation_obj.id),
                            "subject": subject_entity["value"],
                            "subject_label": subject_entity["label"],
                            "predicate": rel["predicate"],
                            "predicate_text": rel.get("predicate_text", ""),
                            "object": object_entity["value"],
                            "object_label": object_entity["label"],
                            "confidence": rel.get("confidence", 0.5),
                            "extraction_method": rel.get("extraction_method", "unknown")
                        })
                
                # Optionally write relations to graph
                if GRAPH_WRITE_RELATIONS:
                    background_tasks.add_task(_write_relations_to_graph, doc_id, relations)
            
            db.commit()
    
    if resolve and entity_ids and background_tasks:
        background_tasks.add_task(resolve_entities, entity_ids)

    html_out = _highlight(req.text, ents)
    summary_text = summarize(req.text, req.lang) if req.do_summary else None
    
    return {
        "doc_id": doc_id,
        "html": html_out,
        "entities": ents,
        "relations": relations,
        "summary": summary_text,
    }


def _write_relations_to_graph(doc_id: str, relations: List[Dict[str, Any]]):
    """Write extracted relations to the knowledge graph."""
    try:
        import requests
        graph_api_url = os.getenv("GRAPH_API_URL", "http://localhost:8612")
        
        for relation in relations:
            # Create nodes and relationship in Neo4j
            payload = {
                "subject": {
                    "name": relation["subject"],
                    "type": relation["subject_label"],
                    "doc_id": doc_id
                },
                "predicate": relation["predicate"],
                "object": {
                    "name": relation["object"],
                    "type": relation["object_label"],
                    "doc_id": doc_id
                },
                "metadata": {
                    "confidence": relation.get("confidence", 0.5),
                    "extraction_method": relation.get("extraction_method", "nlp"),
                    "doc_id": doc_id
                }
            }
            
            response = requests.post(f"{graph_api_url}/relations", json=payload, timeout=10)
            if response.status_code == 200:
                # Update relation resolution status
                with SessionLocal() as db:
                    if relation.get("id"):
                        rel_resolution = db.get(RelationResolution, uuid.UUID(relation["id"]))
                        if rel_resolution:
                            rel_resolution.status = "resolved"
                            rel_resolution.graph_edge_id = response.json().get("edge_id")
                            db.commit()
    
    except Exception as e:
        print(f"Failed to write relations to graph: {e}")


@app.post("/link-entities")
def link_entities(req: LinkReq):
    """Forward entities to graph-views when configured."""
    url = os.getenv("GRAPH_VIEWS_LINK_URL")
    if not url:
        return {"status": "disabled"}
    try:
        import requests

        r = requests.post(url, json=req.dict())
        return {"status": "ok", "upstream": r.status_code}
    except Exception as exc:  # pragma: no cover - network issues
        raise HTTPException(status_code=502, detail=f"link hook failed: {exc}")


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
            "relations": [],  # TODO: Add test relations
            "aleph_id": (info.get("meta") or {}).get("aleph_id"),
        }
    with SessionLocal() as db:
        doc = db.get(Document, uuid.UUID(doc_id))
        if not doc:
            raise HTTPException(404, "not found")
        
        # Get entities
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
        
        # Get relations
        relations = []
        for relation in db.query(Relation).filter_by(doc_id=doc.id).all():
            subject_entity = db.get(Entity, relation.subject_entity_id)
            object_entity = db.get(Entity, relation.object_entity_id)
            
            if subject_entity and object_entity:
                relations.append({
                    "id": str(relation.id),
                    "subject": subject_entity.value,
                    "subject_label": subject_entity.label,
                    "predicate": relation.predicate,
                    "predicate_text": relation.predicate_text,
                    "object": object_entity.value,
                    "object_label": object_entity.label,
                    "confidence": relation.confidence,
                    "extraction_method": relation.extraction_method
                })
        
        return {
            "doc_id": doc_id,
            "title": doc.title,
            "text": None,
            "meta": None,
            "entities": ents,
            "relations": relations,
            "aleph_id": doc.aleph_id,
        }


@app.post("/resolve/{doc_id}")
def resolve_doc(doc_id: str, background_tasks: BackgroundTasks):
    """Trigger entity resolution for all entities in document."""
    if ALLOW_TEST:
        # Test mode - use in-memory data
        if doc_id not in MEM_ENTS:
            raise HTTPException(404, "Document not found")
        
        entity_ids = [e["id"] for e in MEM_ENTS[doc_id]]
        if entity_ids and background_tasks:
            background_tasks.add_task(resolve_entities, entity_ids)
        
        return {
            "doc_id": doc_id,
            "status": "resolution_started", 
            "entity_count": len(entity_ids),
            "message": "Background resolution initiated"
        }
    else:
        # Database mode
        with SessionLocal() as db:
            doc = db.get(Document, uuid.UUID(doc_id))
            if not doc:
                raise HTTPException(404, "Document not found")
            
            # Get all entities for this document
            entities = db.query(Entity).filter_by(doc_id=doc.id).all()
            entity_ids = [str(e.id) for e in entities]
            
            # Update status to processing
            for entity in entities:
                resolution = db.get(EntityResolution, entity.id)
                if resolution:
                    resolution.status = "processing"
                else:
                    resolution = EntityResolution(entity_id=entity.id, status="processing")
                    db.add(resolution)
            db.commit()
            
            # Trigger background resolution
            if entity_ids and background_tasks:
                background_tasks.add_task(resolve_entities, entity_ids)
            
            return {
                "doc_id": doc_id,
                "status": "resolution_started", 
                "entity_count": len(entity_ids),
                "message": "Background resolution initiated"
            }


@app.post("/resolve/entity/{entity_id}")
def resolve_entity(entity_id: str):
    """Resolve single entity against knowledge graph."""
    if ALLOW_TEST:
        # Test mode - find entity in memory
        entity_found = None
        for doc_id, entities in MEM_ENTS.items():
            for entity in entities:
                if entity["id"] == entity_id:
                    entity_found = entity
                    break
            if entity_found:
                break
        
        if not entity_found:
            raise HTTPException(404, "Entity not found")
        
        # Mock resolution result for test mode
        return {
            "entity_id": entity_id,
            "value": entity_found["value"],
            "label": entity_found["label"],
            "resolution": {
                "status": "resolved",
                "node_id": f"test:node:{entity_id[:8]}",
                "score": 0.85,
                "candidates": [
                    {
                        "node_id": f"test:node:{entity_id[:8]}",
                        "score": 0.85,
                        "name": entity_found["value"],
                        "type": entity_found["label"]
                    }
                ]
            }
        }
    else:
        # Database mode - use actual resolver
        from resolver import resolve_single_entity
        
        with SessionLocal() as db:
            entity = db.get(Entity, uuid.UUID(entity_id))
            if not entity:
                raise HTTPException(404, "Entity not found")
            
            # Perform resolution
            resolution_result = resolve_single_entity(entity_id)
            if not resolution_result:
                raise HTTPException(500, "Resolution failed")
            
            # Get updated resolution from database
            resolution = db.get(EntityResolution, entity.id)
            
            return {
                "entity_id": entity_id,
                "value": entity.value,
                "label": entity.label,
                "resolution": {
                    "status": resolution.status if resolution else "unknown",
                    "node_id": resolution.node_id if resolution else None,
                    "score": resolution.score if resolution else None,
                    "candidates": resolution.candidates if resolution else []
                }
            }


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


def _highlight(text: str, entities: List[Dict[str, Any]]):
    """Render entities as HTML spans without requiring resolution."""
    spans = sorted(
        [
            (
                e.get("span_start"),
                e.get("span_end"),
                e.get("label"),
                e.get("value"),
            )
            for e in entities
            if e.get("span_start") is not None and e.get("span_end") is not None
        ],
        key=lambda x: x[0],
    )
    out, cur = [], 0
    for s, e, label, val in spans:
        s = max(0, s)
        e = min(len(text), e)
        out.append(html.escape(text[cur:s]))
        out.append(
            f"<span class=\"ent\" data-label=\"{html.escape(label or '')}\">{html.escape(text[s:e])}</span>"
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
