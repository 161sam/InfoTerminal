"""Pydantic settings for InfoTerminal CLI."""
from __future__ import annotations

import json
import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from env or config file."""

    # Core Services
    search_api: str = "http://127.0.0.1:8401"
    graph_api: str = "http://127.0.0.1:8402"
    views_api: str = "http://127.0.0.1:8403"
    frontend_url: str = "http://127.0.0.1:3411"
    nlp_api: str = "http://127.0.0.1:8404"
    
    # Authentication & Users
    auth_api: str = "http://127.0.0.1:8616"
    
    # NLP & Document Processing
    doc_entities_api: str = "http://127.0.0.1:8613"
    
    # Verification & Fact-Checking
    verification_api: str = "http://127.0.0.1:8614"
    
    # RAG & Document Retrieval
    rag_api: str = "http://127.0.0.1:8615"
    
    # Agent Management
    agents_api: str = "http://127.0.0.1:3417"
    
    # Plugin System
    plugins_api: str = "http://127.0.0.1:8617"
    
    # Forensics & Evidence
    forensics_api: str = "http://127.0.0.1:8618"
    media_forensics_api: str = "http://127.0.0.1:8619"
    
    # User Feedback
    feedback_api: str = "http://127.0.0.1:8620"
    
    # Performance & Monitoring
    performance_api: str = "http://127.0.0.1:8621"
    
    # Operations & System Management
    ops_api: str = "http://127.0.0.1:8622"
    
    # Cache Management
    cache_api: str = "http://127.0.0.1:8623"
    
    # WebSocket & Real-time
    websocket_api: str = "http://127.0.0.1:8624"
    
    # Collaboration & Tasks
    collab_api: str = "http://127.0.0.1:8625"

    # Ports for local dockerized services
    gateway_port: int = 8610
    agents_port: int = 3417
    opensearch_port: int = 9200
    neo4j_port: int = 7687
    
    # Additional service ports
    auth_port: int = 8616
    doc_entities_port: int = 8613
    verification_port: int = 8614
    rag_port: int = 8615
    plugins_port: int = 8617
    forensics_port: int = 8618
    media_forensics_port: int = 8619
    feedback_port: int = 8620
    performance_port: int = 8621
    ops_port: int = 8622
    cache_port: int = 8623
    websocket_port: int = 8624
    collab_port: int = 8625

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

    # Mode
    dev_local: bool = True

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
