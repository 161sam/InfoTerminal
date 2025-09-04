"""Pydantic settings for InfoTerminal CLI."""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from env or config file."""

    # Services
    search_api: str = "http://127.0.0.1:8401"
    graph_api: str = "http://127.0.0.1:8402"
    views_api: str = "http://127.0.0.1:8403"
    nlp_api: str = "http://127.0.0.1:8404"

    # Neo4j
    neo4j_uri: str = "bolt://127.0.0.1:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "test12345"

    # Postgres
    pg_host: str = "127.0.0.1"
    pg_port: int = 5432
    pg_db: str = "it_graph"
    pg_user: str = "it_user"
    pg_password: str = "it_pass"

    class Config:
        env_prefix = "IT_"


@lru_cache
def get_settings() -> Settings:
    """Load settings once, merging optional JSON config."""
    config_path = Path.home() / ".config/infoterminal/config.json"
    base = Settings()
    if config_path.exists():
        data = json.loads(config_path.read_text())
        base = Settings(**{**base.model_dump(), **data})
    return base
