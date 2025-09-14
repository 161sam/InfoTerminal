import os
import tempfile
import uuid
from pathlib import Path
from typing import List

from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

try:
    import markdown as md
except Exception:  # pragma: no cover
    md = None

try:
    from weasyprint import HTML
except Exception:  # pragma: no cover
    HTML = None


router = APIRouter(prefix="/dossier", tags=["dossier"])


class DossierItems(BaseModel):
    docs: List[str] = []
    nodes: List[str] = []
    edges: List[str] = []


class DossierOptions(BaseModel):
    summary: bool = False


class DossierIn(BaseModel):
    title: str
    items: DossierItems = DossierItems()
    options: DossierOptions = DossierOptions()


BASE = Path(__file__).resolve().parent
env = Environment(loader=FileSystemLoader(str(BASE / "templates")))


@router.post("")
def build_dossier(inp: DossierIn):
    data = inp.model_dump()
    tpl = env.get_template("basic.md.j2")
    md_text = tpl.render(**data)
    out = {"markdown": md_text}
    if HTML and md and os.getenv("IT_DOSSIER_PDF", "0") == "1":
        rid = uuid.uuid4()
        pdf_path = Path(tempfile.gettempdir()) / f"dossier-{rid}.pdf"
        html_content = "<html><body>" + md.markdown(md_text) + "</body></html>"
        HTML(string=html_content).write_pdf(str(pdf_path))
        out["pdfUrl"] = str(pdf_path)
    return out
