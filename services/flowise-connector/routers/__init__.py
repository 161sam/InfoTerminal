"""
Flowise Connector Routers

API routers for the flowise-connector service.
"""

from .core_v1 import router as core_router
from .agents_v1 import router as agents_router

__all__ = [
    "core_router",
    "agents_router"
]
