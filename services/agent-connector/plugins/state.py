import os, json
from pathlib import Path
from typing import Dict, Any

STATE_DIR = Path(os.getenv("IT_PLUGINS_STATE_DIR","/data/plugins"))
STATE_DIR.mkdir(parents=True, exist_ok=True)

def _read_json(p: Path) -> Dict[str, Any]:
    if not p.exists(): return {}
    try: return json.loads(p.read_text(encoding="utf-8"))
    except Exception: return {}

def _write_json(p: Path, data: Dict[str, Any]):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def read_global(): return _read_json(STATE_DIR / "global.json")
def write_global(d: Dict[str, Any]): _write_json(STATE_DIR / "global.json", d)

def read_user(uid: str): return _read_json(STATE_DIR / f"users/{uid}.json")
def write_user(uid: str, d: Dict[str, Any]): _write_json(STATE_DIR / f"users/{uid}.json", d)
