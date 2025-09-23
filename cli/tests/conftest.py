"""Global test configuration for InfoTerminal CLI testing."""
import asyncio
import json
import os
import pytest
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from unittest.mock import AsyncMock, MagicMock

import httpx
from typer.testing import CliRunner

# Import CLI app and utilities
from it_cli.__main__ import app
from it_cli.config import get_settings

# Test configuration
TEST_TIMEOUT = 30.0
API_BASE_URL = "http://localhost:8000"
TEST_DATA_DIR = Path(__file__).parent / "fixtures"

class MockResponse:
    """Mock HTTP response for testing."""
    
    def __init__(self, json_data: Dict[str, Any], status_code: int = 200, headers: Optional[Dict[str, str]] = None):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers or {}
        self.text = json.dumps(json_data)
        
    def json(self) -> Dict[str, Any]:
        return self.json_data
        
    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"HTTP {self.status_code}", 
                request=MagicMock(), 
                response=self
            )

@pytest.fixture
def cli_runner():
    """CLI test runner fixture."""
    return CliRunner()

@pytest.fixture
def temp_config_file():
    """Temporary config file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config = {
            "search_api": "http://localhost:8401",
            "graph_api": "http://localhost:8402", 
            "auth_api": "http://localhost:8616",
            "nlp_api": "http://localhost:8613",
            "verification_api": "http://localhost:8614",
            "rag_api": "http://localhost:8615",
            "agents_api": "http://localhost:3417",
            "plugins_api": "http://localhost:8617",
            "forensics_api": "http://localhost:8618",
            "media_forensics_api": "http://localhost:8619",
            "feedback_api": "http://localhost:8620",
            "performance_api": "http://localhost:8621",
            "ops_api": "http://localhost:8622",
            "cache_api": "http://localhost:8623",
            "websocket_api": "http://localhost:8624",
            "collab_api": "http://localhost:8625"
        }
        json.dump(config, f)
        temp_path = f.name
    
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def mock_settings(temp_config_file, monkeypatch):
    """Mock settings fixture."""
    def mock_get_settings():
        from it_cli.config import Settings
        # Load from temp config file
        with open(temp_config_file) as f:
            config_data = json.load(f)
        return Settings(**config_data)
    
    monkeypatch.setattr("it_cli.config.get_settings", mock_get_settings)
    return mock_get_settings()

@pytest.fixture 
async def mock_http_client():
    """Mock HTTP client for API testing."""
    async with httpx.AsyncClient() as client:
        yield client

@pytest.fixture
def api_health_response():
    """Standard API health response."""
    return {
        "status": "healthy",
        "version": "v1.0.0",
        "uptime": 3600,
        "timestamp": "2025-09-22T10:00:00Z"
    }

@pytest.fixture
def api_error_response():
    """Standard API error response."""
    return {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Invalid request parameters",
            "details": {"field": "value", "error": "required"}
        }
    }

@pytest.fixture
def paginated_response():
    """Standard paginated API response."""
    return {
        "items": [
            {"id": "1", "name": "Item 1"},
            {"id": "2", "name": "Item 2"}
        ],
        "total": 2,
        "page": 1,
        "size": 10
    }

@pytest.fixture
def sample_search_results():
    """Sample search API results."""
    return {
        "hits": [
            {
                "id": "doc1",
                "title": "Sample Document 1", 
                "score": 0.95,
                "content": "This is a sample document for testing."
            },
            {
                "id": "doc2",
                "title": "Sample Document 2",
                "score": 0.87,
                "content": "Another sample document for testing."
            }
        ],
        "total": 2,
        "took": 15
    }

@pytest.fixture
def sample_graph_nodes():
    """Sample graph API nodes."""
    return {
        "nodes": [
            {"id": "node1", "labels": ["Person"], "properties": {"name": "Alice"}},
            {"id": "node2", "labels": ["Person"], "properties": {"name": "Bob"}}
        ],
        "relationships": [
            {"id": "rel1", "type": "KNOWS", "start": "node1", "end": "node2"}
        ],
        "total": 2
    }

@pytest.fixture
def sample_nlp_entities():
    """Sample NLP entities extraction."""
    return {
        "entities": [
            {
                "text": "Alice",
                "label": "PERSON",
                "start": 0,
                "end": 5,
                "confidence": 0.95
            },
            {
                "text": "New York", 
                "label": "GPE",
                "start": 15,
                "end": 23,
                "confidence": 0.92
            }
        ],
        "processing_time": 0.05
    }

@pytest.fixture
def sample_verification_claims():
    """Sample verification claims."""
    return {
        "claims": [
            {
                "text": "The Earth is round",
                "confidence": 0.98,
                "type": "factual",
                "source": "scientific_consensus"
            }
        ],
        "processing_time": 0.12
    }

# Performance testing fixtures
@pytest.fixture
def performance_thresholds():
    """Performance thresholds for testing."""
    return {
        "cli_startup_time": 2.0,  # seconds
        "api_response_time": 1.0,  # seconds  
        "search_response_time": 0.5,  # seconds
        "graph_query_time": 2.0,  # seconds
        "nlp_processing_time": 3.0,  # seconds
        "memory_usage_mb": 100,  # MB
        "concurrent_requests": 10
    }

# Mock service responses for each command group
@pytest.fixture
def service_mock_responses():
    """Mock responses for all InfoTerminal services."""
    return {
        "auth": {
            "login": {"token": "test_token", "expires_at": "2025-09-22T20:00:00Z"},
            "whoami": {"username": "test_user", "role": "admin", "email": "test@example.com"},
            "users": {"items": [{"username": "user1", "role": "user"}], "total": 1}
        },
        "search": {
            "query": {"hits": [{"id": "1", "title": "Test Doc", "score": 0.9}], "total": 1},
            "index": {"id": "doc123", "status": "indexed"}
        },
        "graph": {
            "cypher": {"data": [{"n": 42}], "summary": {"stats": {"nodes_created": 0}}},
            "neighbors": {"nodes": [], "relationships": [], "total": 0}
        },
        "nlp": {
            "extract": {"entities": [], "relations": [], "processing_time": 0.1},
            "resolve": {"resolved": [], "confidence": 0.8}
        },
        "verify": {
            "extract": {"claims": [], "processing_time": 0.2},
            "evidence": {"evidence": [], "relevance_scores": []}
        },
        "rag": {
            "search": {"documents": [], "total": 0},
            "embed": {"embedding": [0.1, 0.2, 0.3], "dimensions": 3}
        },
        "agents": {
            "list": {"agents": [], "total": 0},
            "chat": {"response": "Hello!", "session_id": "sess123"}
        },
        "plugins": {
            "list": {"plugins": [], "total": 0},
            "status": {"plugins": {}, "total": 0}
        },
        "forensics": {
            "ingest": {"evidence_hash": "abc123", "chain_position": 1},
            "verify": {"valid": True, "chain_valid": True}
        },
        "media": {
            "analyze": {"file_type": "image/jpeg", "sha256": "def456"},
            "compare": {"similarity_score": 0.85, "is_match": True}
        },
        "feedback": {
            "post": {"id": 123, "category": "general", "status": "received"},
            "list": {"items": [], "total": 0}
        },
        "perf": {
            "summary": {"metrics": {"avg_response_time": 100}, "grade": "A"},
            "system": {"metrics": {"cpu_percent": 25}}
        },
        "ops": {
            "stacks": {"stacks": [], "total": 0},
            "health": {"status": "healthy", "components": []}
        },
        "cache": {
            "get": {"value": "test_value", "ttl": 3600},
            "stats": {"overall": {"total_keys": 100, "hit_rate": 85.5}}
        },
        "ws": {
            "token": {"token": "ws_token", "websocket_url": "ws://localhost:8624"},
            "clients": {"clients": [], "total": 0}
        },
        "collab": {
            "workspaces": {"items": [], "total": 0},
            "tasks": {"items": [], "total": 0}
        }
    }

# Event loop for async tests
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# CLI command groups to test
CLI_COMMAND_GROUPS = [
    "auth", "search", "graph", "views", "nlp", "verify", "rag", 
    "agents", "plugins", "forensics", "media", "feedback", "perf",
    "ops", "cache", "ws", "collab", "fe", "analytics", "settings", "tui"
]

# API endpoints mapping
API_ENDPOINTS = {
    "auth": "/v1/auth",
    "search": "/v1/search", 
    "graph": "/v1/cypher",
    "nlp": "/v1/extract/entities",
    "verify": "/v1/claims/extract",
    "rag": "/v1/documents/search",
    "agents": "/v1/agents",
    "plugins": "/v1/plugins/registry",
    "forensics": "/v1/evidence",
    "media": "/v1/images/analyze",
    "feedback": "/v1/feedback",
    "perf": "/v1/metrics",
    "ops": "/v1/stacks",
    "cache": "/v1/cache",
    "ws": "/v1/clients",
    "collab": "/v1/workspaces"
}
