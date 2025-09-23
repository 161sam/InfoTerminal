"""
Shared Router Templates for InfoTerminal Services

This package provides standardized router templates that can be used
across all InfoTerminal services for consistency.
"""

from .core_v1 import router as core_router, set_health_checker

__all__ = [
    "core_router",
    "set_health_checker"
]
