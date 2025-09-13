import yaml, pathlib
from fastapi import APIRouter, HTTPException
from .models import EntityType, RelationType, EntityInstance

router = APIRouter(prefix="/ontology", tags=["ontology"])

BASE = pathlib.Path(__file__).resolve().parent.parent / "schema" / "ontology"

def _load_entities():
    with open(BASE / "entities.yaml", "r", encoding="utf-8") as f:
        return [EntityType(**e) for e in yaml.safe_load(f)]

def _load_relations():
    with open(BASE / "relations.yaml", "r", encoding="utf-8") as f:
        return [RelationType(**r) for r in yaml.safe_load(f)]

@router.get("/entities")
def get_entities():
    return [e.model_dump() for e in _load_entities()]

@router.get("/relations")
def get_relations():
    return [r.model_dump(by_alias=True) for r in _load_relations()]

@router.post("/validate")
def validate_entity(payload: EntityInstance):
    ents = {e.name: e for e in _load_entities()}
    et = ents.get(payload.type)
    if not et:
        raise HTTPException(400, f"Unknown entity type: {payload.type}")
    data = payload.data or {}
    # required properties
    missing = [p.name for p in et.properties if p.required and p.name not in data]
    if missing:
        raise HTTPException(400, f"Missing required: {missing}")
    return {"ok": True}
