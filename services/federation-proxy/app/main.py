from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import yaml
import os

CONFIG_PATH = os.getenv("FEDERATION_CONFIG", "/app/remotes.yaml")

app = FastAPI(title="Federation Proxy", version="0.1.0")


def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return {"remotes": []}
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f) or {"remotes": []}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/remotes")
def list_remotes():
    cfg = load_config()
    return cfg

