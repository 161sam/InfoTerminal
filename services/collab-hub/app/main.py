from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel, Field

app = FastAPI(title="Collaboration Hub", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Observability primitives
DOSSIER_EXPORTS = Counter(
    "dossier_exports_total",
    "Total number of dossier exports",
    ["format", "source", "status"],
)

DOSSIER_EXPORT_DURATION = Histogram(
    "dossier_export_duration_seconds",
    "Duration of dossier export operations",
    ["format", "source", "status"],
)

COLLAB_NOTES_COUNTER = Counter(
    "collab_notes_total",
    "Number of collaboration notes processed",
    ["status"],
)


TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates" / "dossier"
TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
JINJA_ENV = Environment(
    loader=FileSystemLoader(str(TEMPLATE_DIR)),
    autoescape=select_autoescape(disabled_extensions=(".md",)),
)

NOTES_FEATURE_FLAG = "IT_ENABLE_COLLAB_NOTES"
NOTES_STORE: Dict[str, List[Dict[str, str]]] = {}


def record_audit(event: str, payload: Dict[str, object]) -> None:
    try:
        os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)
        entry = {"ts": time.time(), "event": event, **payload}
        with open(AUDIT_PATH, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception:
        pass


class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active:
            self.active.remove(websocket)

    async def broadcast(self, message: Dict):
        data = json.dumps(message, ensure_ascii=False)
        for ws in self.active:
            await ws.send_text(data)


manager = ConnectionManager()

TASKS_PATH = os.getenv("CH_TASKS_PATH", "/data/collab_tasks.json")
os.makedirs(os.path.dirname(TASKS_PATH), exist_ok=True)
TASKS: List[Dict] = []
AUDIT_PATH = os.getenv("CH_AUDIT_PATH", "/data/collab_audit.jsonl")

def load_tasks():
    global TASKS
    try:
        if os.path.exists(TASKS_PATH):
            with open(TASKS_PATH, 'r', encoding='utf-8') as f:
                TASKS = json.load(f)
    except Exception:
        TASKS = []

def save_tasks():
    try:
        with open(TASKS_PATH, 'w', encoding='utf-8') as f:
            json.dump(TASKS, f, ensure_ascii=False)
    except Exception:
        pass

load_tasks()


@app.get("/healthz")
def healthz():
    return {"status": "ok", "connections": len(manager.active), "tasks": len(TASKS)}


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


class TaskCreate(BaseModel):
    text: str
    priority: str | None = None  # low|normal|high|critical
    labels: list[str] | None = None


@app.get("/tasks")
def list_tasks():
    return {"items": TASKS}


@app.post("/tasks")
async def create_task(body: TaskCreate):
    prio = body.priority or "normal"
    labels = body.labels or []
    t = {"id": f"{int(__import__('time').time()*1000)}", "text": body.text, "status": "todo", "priority": prio, "labels": labels}
    TASKS.append(t)
    save_tasks()
    await manager.broadcast({"type": "task_add", "task": t})
    return t


@app.post("/tasks/{task_id}/move")
async def move_task(task_id: str, to: str):
    if to not in ("todo", "doing", "done"):
        raise HTTPException(400, "invalid status")
    found = False
    for t in TASKS:
        if t["id"] == task_id:
            t["status"] = to
            found = True
            break
    if not found:
        raise HTTPException(404, "not found")
    save_tasks()
    await manager.broadcast({"type": "task_move", "id": task_id, "to": to})
    return {"status": "ok"}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    global TASKS
    before = len(TASKS)
    TASKS = [t for t in TASKS if t["id"] != task_id]
    if len(TASKS) == before:
        raise HTTPException(404, "not found")
    save_tasks()
    await manager.broadcast({"type": "task_delete", "id": task_id})
    return {"status": "ok"}


class TaskUpdate(BaseModel):
    text: str | None = None
    priority: str | None = None
    labels: list[str] | None = None


class DossierExportRequest(BaseModel):
    case_id: str
    title: Optional[str] = None
    summary: Optional[str] = None
    source: str = Field(default="graph", pattern="^(search|graph)$")
    format: str = Field(default="markdown", pattern="^(markdown|pdf)$")
    template: str = Field(default="standard", pattern="^(standard|brief)$")
    analysts: List[str] = Field(default_factory=list)
    entities: List[Dict[str, str]] = Field(default_factory=list)
    references: List[Dict[str, str]] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)


class NoteCreate(BaseModel):
    case_id: str
    author: str = Field(default="analyst", min_length=1, max_length=80)
    body: str = Field(..., min_length=1, max_length=2000)
    node_id: Optional[str] = None


def _get_template(template: str):
    try:
        return JINJA_ENV.get_template(f"{template}.md.j2")
    except Exception as exc:  # pragma: no cover - configuration issue
        raise HTTPException(status_code=400, detail=f"Unknown template '{template}'") from exc


def _render_markdown(req: DossierExportRequest) -> Dict[str, object]:
    template = _get_template(req.template)
    context = {
        "case_id": req.case_id,
        "title": req.title or f"Case {req.case_id}",
        "summary": req.summary or "",
        "source": req.source,
        "analysts": req.analysts or ["Unknown Analyst"],
        "entities": req.entities,
        "references": req.references,
        "notes": req.notes,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    markdown = template.render(**context)
    return {"markdown": markdown, "context": context}


def _markdown_to_pdf(markdown_text: str) -> bytes:
    lines = markdown_text.splitlines() or [""]

    def _escape(value: str) -> str:
        return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    content_lines = ["BT", "/F1 12 Tf", "72 780 Td"]
    first = True
    for line in lines:
        safe = _escape(line)
        if first:
            content_lines.append(f"({safe}) Tj")
            first = False
        else:
            content_lines.append("T*")
            content_lines.append(f"({safe}) Tj")
    content_lines.append("ET")
    content_stream = "\n".join(content_lines).encode("latin-1", "ignore")

    objects = []
    objects.append(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    objects.append(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    objects.append(
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n"
    )
    stream_header = f"4 0 obj<< /Length {len(content_stream)} >>stream\n".encode("ascii")
    objects.append(stream_header + content_stream + b"\nendstream\nendobj\n")
    objects.append(b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n")

    offsets = []
    cursor = len(b"%PDF-1.4\n")
    for obj in objects:
        offsets.append(cursor)
        cursor += len(obj)

    pdf_body = b"%PDF-1.4\n" + b"".join(objects)
    xref = [b"xref\n", f"0 {len(objects) + 1}\n".encode("ascii"), b"0000000000 65535 f \n"]
    for offset in offsets:
        xref.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    xref.append(b"trailer<< /Size 6 /Root 1 0 R >>\n")
    xref.append(f"startxref\n{len(pdf_body)}\n".encode("ascii"))
    xref.append(b"%%EOF")
    return pdf_body + b"".join(xref)


@app.post("/tasks/{task_id}/update")
async def update_task(task_id: str, body: TaskUpdate):
    for t in TASKS:
        if t["id"] == task_id:
            if body.text is not None:
                t["text"] = body.text
            if body.priority is not None:
                t["priority"] = body.priority
            if body.labels is not None:
                t["labels"] = body.labels
            save_tasks()
            await manager.broadcast({"type": "task_update", "task": t})
            return t
    raise HTTPException(404, "not found")


@app.post("/dossier/export")
def dossier_export(req: DossierExportRequest):
    started = time.perf_counter()
    status = "success"
    duration = 0.0

    try:
        rendered = _render_markdown(req)
        markdown = rendered["markdown"]
        metadata = {
            "case_id": req.case_id,
            "source": req.source,
            "template": req.template,
            "generated_at": time.time(),
            "analysts": req.analysts,
            "entities": req.entities,
            "references": req.references,
        }

        if req.format == "pdf":
            pdf_bytes = _markdown_to_pdf(markdown)
            duration = time.perf_counter() - started
            record_audit(
                "dossier.export",
                {"case_id": req.case_id, "format": req.format, "source": req.source},
            )
            return Response(
                content=pdf_bytes,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={req.case_id}.pdf"},
            )

        duration = time.perf_counter() - started
        record_audit(
            "dossier.export",
            {"case_id": req.case_id, "format": req.format, "source": req.source},
        )
        return {
            "case_id": req.case_id,
            "format": "markdown",
            "markdown": markdown,
            "metadata": metadata,
        }
    except HTTPException:
        status = "error"
        duration = time.perf_counter() - started
        raise
    except Exception as exc:  # pragma: no cover
        status = "error"
        duration = time.perf_counter() - started
        raise HTTPException(status_code=500, detail=f"Export failed: {exc}") from exc
    finally:
        DOSSIER_EXPORTS.labels(
            format=req.format,
            source=req.source,
            status=status,
        ).inc()
        DOSSIER_EXPORT_DURATION.labels(
            format=req.format,
            source=req.source,
            status=status,
        ).observe(duration)


@app.get("/labels")
def list_labels():
    counts: Dict[str, int] = {}
    for t in TASKS:
        for lb in t.get('labels', []) or []:
            counts[lb] = counts.get(lb, 0) + 1
    top = sorted(({"label": k, "count": v} for k, v in counts.items()), key=lambda x: -x["count"])[:50]
    return {"items": top}


def _notes_enabled() -> bool:
    return os.getenv(NOTES_FEATURE_FLAG, "0") == "1"


@app.post("/collab/notes")
def create_note(note: NoteCreate):
    if not _notes_enabled():
        raise HTTPException(status_code=503, detail="Collaboration notes feature disabled")

    note_entry = {
        "id": str(uuid.uuid4()),
        "case_id": note.case_id,
        "author": note.author,
        "body": note.body,
        "node_id": note.node_id,
        "created_at": time.time(),
    }
    NOTES_STORE.setdefault(note.case_id, []).append(note_entry)
    COLLAB_NOTES_COUNTER.labels(status="created").inc()
    record_audit("collab.note", note_entry)
    return note_entry


@app.get("/collab/notes/{case_id}")
def list_notes(case_id: str):
    if not _notes_enabled():
        raise HTTPException(status_code=503, detail="Collaboration notes feature disabled")
    return {"case_id": case_id, "items": NOTES_STORE.get(case_id, [])}


@app.post("/audit")
def write_audit(entry: Dict):
    record_audit("manual", {"payload": entry})
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except Exception:
                msg = {"type": "message", "text": data}
            await manager.broadcast({"type": "event", **msg})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
