"""Doc-Entities service with standardized v1 API."""
from __future__ import annotations

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI

# Ensure shared modules are importable
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    APIError,
    ErrorCodes,
    HealthChecker,
    check_database_connection,
    setup_standard_exception_handlers,
    setup_standard_middleware,
    setup_standard_openapi,
    get_service_tags_metadata,
)

from .routers.core_v1 import build_core_router
from .routers.doc_entities_v1 import DocEntitiesService, build_doc_entities_router
from .models.api_models import NERRequest, SummarizationRequest

from db import SessionLocal, engine
from models import Base
from it_logging import setup_logging

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ALLOW_TEST = os.getenv("ALLOW_TEST") or os.getenv("ALLOW_TEST_MODE")
GRAPH_URL = os.getenv("GRAPH_UI", "http://localhost:3000/graphx")
GRAPH_WRITE_RELATIONS = os.getenv("GRAPH_WRITE_RELATIONS", "0") == "1"
GRAPH_API_URL = os.getenv("GRAPH_API_URL", "http://localhost:8612")

if not ALLOW_TEST:
    Base.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise and tear down service resources."""
    print("✅ Doc-Entities API starting up")
    if not ALLOW_TEST:
        try:
            Base.metadata.create_all(engine)
            print("✅ Database tables created/verified")
        except Exception as exc:  # pragma: no cover - startup diagnostics
            print(f"⚠️ Database initialization warning: {exc}")
    yield
    print("🛑 Doc-Entities API shutting down")


app = FastAPI(
    title="InfoTerminal Doc-Entities API",
    description="Document processing and NLP API for InfoTerminal",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    lifespan=lifespan,
)

setup_logging(app, service_name="doc-entities")
setup_standard_middleware(app, "doc-entities")
setup_standard_exception_handlers(app)
setup_standard_openapi(
    app=app,
    title="InfoTerminal Doc-Entities API",
    description="Document processing and NLP API for InfoTerminal",
    version="1.0.0",
    service_name="doc-entities",
    tags_metadata=get_service_tags_metadata("doc-entities"),
)

app.state.service_name = "doc-entities"
app.state.version = os.getenv("GIT_SHA", "1.0.0")
import time
app.state.start_ts = time.monotonic()

# ---------------------------------------------------------------------------
# Health configuration
# ---------------------------------------------------------------------------
health_checker = HealthChecker("doc-entities", app.state.version)


def check_database() -> None:
    if ALLOW_TEST:
        return
    with SessionLocal() as db:
        db.execute("SELECT 1").fetchone()


def check_graph_api() -> None:
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise Exception("requests library not available") from exc
    response = requests.get(f"{GRAPH_API_URL}/healthz", timeout=5)
    if response.status_code != 200:
        raise Exception(f"Graph API unhealthy: {response.status_code}")


if not ALLOW_TEST:
    health_checker.add_dependency("database", lambda: check_database_connection(check_database))

try:  # Graph dependency optional
    import requests  # noqa: F401
    health_checker.add_dependency("graph_api", lambda: check_database_connection(check_graph_api))
except ImportError:  # pragma: no cover
    pass

app.include_router(
    build_core_router(
        health_check=lambda: health_checker.health_check(),
        ready_check=lambda: health_checker.ready_check(),
        service_name=app.state.service_name,
        version=str(app.state.version),
        start_ts=app.state.start_ts,
    )
)

# ---------------------------------------------------------------------------
# Domain router/service
# ---------------------------------------------------------------------------
service = DocEntitiesService(
    allow_test=bool(ALLOW_TEST),
    graph_api_url=GRAPH_API_URL,
    graph_write_relations=GRAPH_WRITE_RELATIONS,
)
app.include_router(build_doc_entities_router(service))

# ---------------------------------------------------------------------------
# Legacy endpoints (kept for backward compatibility)
# ---------------------------------------------------------------------------


@app.post("/ner", deprecated=True, tags=["legacy"])
def legacy_ner(text: str, lang: str = "en"):
    request = NERRequest(text=text, language=lang)
    response = service.extract_entities(request)
    return {
        "entities": [
            {"text": ent.text, "label": ent.label, "start": ent.start, "end": ent.end}
            for ent in response.entities
        ],
        "model": response.model,
    }


@app.post("/summary", deprecated=True, tags=["legacy"])
def legacy_summary(text: str, lang: str = "en"):
    request = SummarizationRequest(text=text, language=lang)
    response = service.summarize_text(request)
    return {"summary": response.summary}


@app.get("/", tags=["root"])
def root():
    return {
        "service": "InfoTerminal Doc-Entities API",
        "version": app.state.version,
        "status": "running",
        "api_version": "v1",
        "test_mode": bool(ALLOW_TEST),
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz",
            "docs": "/v1/docs",
            "extract_entities": "/v1/extract/entities",
            "extract_relations": "/v1/extract/relations",
            "summarize": "/v1/summarize",
            "annotate": "/v1/documents/annotate",
            "documents": "/v1/documents/{id}",
            "fuzzy_match": "/v1/fuzzy/match",
            "fuzzy_dedupe": "/v1/fuzzy/dedupe",
        },
        "legacy_endpoints": {
            "ner": "/ner (deprecated)",
            "summary": "/summary (deprecated)",
        },
    }
