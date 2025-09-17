from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List, Dict
import json

app = FastAPI(title="Collaboration Hub", version="0.1.0")


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


@app.get("/healthz")
def healthz():
    return {"status": "ok", "connections": len(manager.active)}


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

