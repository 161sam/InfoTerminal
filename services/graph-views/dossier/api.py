import tempfile, uuid, json
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

router = APIRouter(prefix="/dossier", tags=["dossier"])

class DossierIn(BaseModel):
    query: str
    entities: List[str] = []
    graphSelection: Dict[str, List[str]] = {"nodes": [], "edges": []}

BASE = Path(__file__).resolve().parent
env = Environment(loader=FileSystemLoader(str(BASE)))

@router.post("")
def build_dossier(inp: DossierIn):
    rid = str(uuid.uuid4())
    data = inp.model_dump()
    tmp = Path(tempfile.gettempdir()) / f"dossier-{rid}.json"
    md  = Path(tempfile.gettempdir()) / f"dossier-{rid}.md"

    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tpl = env.get_template("template.md.j2")
    md.write_text(tpl.render(**data), encoding="utf-8")

    return {
        "id": rid,
        "json_path": str(tmp),
        "md_path": str(md),
        "message": "Dossier generated"
    }
