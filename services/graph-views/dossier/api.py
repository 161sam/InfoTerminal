import tempfile, uuid, json, os
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
try:
    import markdown as md
except Exception:  # pragma: no cover
    md = None
try:
    from weasyprint import HTML
except Exception:  # pragma: no cover
    HTML = None

router = APIRouter(prefix="/dossier", tags=["dossier"])

class DossierIn(BaseModel):
    query: str
    entities: List[str] = []
    graphSelection: Dict[str, List[str]] = {"nodes": [], "edges": []}
    format: str | None = "md"

BASE = Path(__file__).resolve().parent
env = Environment(loader=FileSystemLoader(str(BASE)))

@router.post("")
def build_dossier(inp: DossierIn):
    rid = str(uuid.uuid4())
    data = inp.model_dump()
    fmt = (inp.format or "md").lower()
    tmp = Path(tempfile.gettempdir()) / f"dossier-{rid}.json"
    md_path = Path(tempfile.gettempdir()) / f"dossier-{rid}.md"

    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tpl = env.get_template("template.md.j2")
    md_text = tpl.render(**data)
    md_path.write_text(md_text, encoding="utf-8")

    out = {"id": rid, "json_path": str(tmp), "md_path": str(md_path)}

    if fmt in ("pdf", "both") and HTML and md and os.getenv("IT_DOSSIER_PDF", "0") == "1":
        html_content = "<html><body>" + md.markdown(md_text) + "</body></html>"
        pdf_path = Path(tempfile.gettempdir()) / f"dossier-{rid}.pdf"
        HTML(string=html_content).write_pdf(str(pdf_path))
        out["pdf_path"] = str(pdf_path)

    return out
