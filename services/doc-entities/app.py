try:
    from obs.otel_boot import *  # noqa
except Exception:
    pass

import os, json, html
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentation
from prometheus_client import make_asgi_app
from pydantic import BaseModel
import psycopg2, httpx

PG = dict(
  host=os.getenv("PG_HOST","localhost"),
  port=int(os.getenv("PG_PORT","5432")),
  dbname=os.getenv("PG_DB","infoterminal"),
  user=os.getenv("PG_USER","app"),
  password=os.getenv("PG_PASS","app"),
)
NLP_URL = os.getenv("NLP_URL","http://127.0.0.1:8005")
GRAPH_URL = os.getenv("GRAPH_UI","http://localhost:3000/graphx")  # UI link

def conn(): return psycopg2.connect(**PG)

def init():
  with conn() as c, c.cursor() as cur:
    cur.execute("""
      CREATE TABLE IF NOT EXISTS doc_texts (
        doc_id text primary key,
        title text,
        text  text,
        meta  jsonb,
        created_at timestamptz default now(),
        updated_at timestamptz default now()
      );
      CREATE TABLE IF NOT EXISTS doc_entities (
        doc_id text references doc_texts(doc_id) on delete cascade,
        ents   jsonb not null,
        links  jsonb not null,
        created_at timestamptz default now(),
        primary key (doc_id)
      );
    """)
init()

app = FastAPI(title="Doc Entities", version="0.1.0")
FastAPIInstrumentation().instrument_app(app)
app.mount("/metrics", make_asgi_app())

class AnnotReq(BaseModel):
  doc_id: str
  title: Optional[str] = None
  text: str
  meta: Optional[Dict[str, Any]] = None

@app.get("/healthz")
def health(): return {"ok": True}

@app.post("/annotate")
def annotate(req: AnnotReq):
  # store text
  with conn() as c, c.cursor() as cur:
    cur.execute("""
      INSERT INTO doc_texts (doc_id, title, text, meta)
      VALUES (%s,%s,%s,%s)
      ON CONFLICT (doc_id) DO UPDATE SET title=EXCLUDED.title, text=EXCLUDED.text, meta=EXCLUDED.meta, updated_at=now()
    """, (req.doc_id, req.title, req.text, json.dumps(req.meta or {})))
  # NER
  with httpx.Client(timeout=30.0) as cli:
    ner = cli.post(f"{NLP_URL}/ner", json={"text": req.text}).json()
    links = cli.post(f"{NLP_URL}/resolve", json={"text": req.text, "ents": ner.get("ents", [])}).json()
  ents = ner.get("ents", [])
  lks  = links.get("links", [])
  with conn() as c, c.cursor() as cur:
    cur.execute("""
      INSERT INTO doc_entities (doc_id, ents, links) VALUES (%s,%s,%s)
      ON CONFLICT (doc_id) DO UPDATE SET ents=EXCLUDED.ents, links=EXCLUDED.links, created_at=now()
    """, (req.doc_id, json.dumps(ents), json.dumps(lks)))
  return {"doc_id": req.doc_id, "ents": ents, "links": lks}

@app.get("/docs/{doc_id}")
def get_doc(doc_id: str):
  with conn() as c, c.cursor() as cur:
    cur.execute("SELECT title,text,meta FROM doc_texts WHERE doc_id=%s", (doc_id,))
    row = cur.fetchone()
    if not row: raise HTTPException(404, "not found")
    title, text, meta = row
    cur.execute("SELECT ents,links FROM doc_entities WHERE doc_id=%s", (doc_id,))
    er = cur.fetchone()
  ents, links = (er or ([ ] ,[ ]) )
  return {"doc_id": doc_id, "title": title, "text": text, "meta": meta, "ents": ents, "links": links}

def _decorate(text: str, links: List[Dict[str,Any]]):
  # markiere nur gelinkte Entitäten (mit node_id)
  spans = []
  for lk in links:
    if "text" in lk and "node_id" in lk:
      spans.append((lk.get("start"), lk.get("end"), lk["text"], lk["node_id"]))
  # falls start/end fehlen, simple global replace (low-fi)
  if not spans:
    out = html.escape(text)
    for lk in links:
      t = html.escape(lk.get("text",""))
      nid = lk.get("node_id","")
      if not t or not nid: continue
      out = out.replace(
        t, f'<a class="ent" href="{GRAPH_URL}?focus={html.escape(nid)}" title="open in graph">{t}</a>'
      )
    return out
  # mit Offsets (robuster)
  spans = sorted([s for s in spans if s[0] is not None and s[1] is not None], key=lambda x: x[0])
  out, cur = [], 0
  for s,e,txt,nid in spans:
    s = max(0, s); e = min(len(text), e or s)
    out.append(html.escape(text[cur:s]))
    out.append(f'<a class="ent" href="{GRAPH_URL}?focus={html.escape(nid)}" title="open in graph">{html.escape(text[s:e])}</a>')
    cur = e
  out.append(html.escape(text[cur:]))
  return "".join(out)

@app.get("/docs/{doc_id}/html")
def get_doc_html(doc_id: str):
  d = get_doc(doc_id)
  body = _decorate(d["text"], d.get("links", []))
  title = html.escape(d.get("title") or d["doc_id"])
  html_doc = f"""<!doctype html>
  <html><head><meta charset="utf-8"><title>{title}</title>
  <style> body{{font:14px ui-sans-serif; max-width:860px; margin:24px auto;}}
  .ent{{background:#fffae6; padding:1px 3px; border-radius:3px; text-decoration:none; border-bottom:1px dotted #888;}}</style>
  </head><body><h1>{title}</h1><div>{body}</div></body></html>"""
  return html_doc
