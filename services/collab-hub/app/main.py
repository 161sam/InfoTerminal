from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import os, json
import json

app = FastAPI(title="Collaboration Hub", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
