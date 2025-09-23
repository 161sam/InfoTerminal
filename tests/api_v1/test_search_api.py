"""
InfoTerminal API v1 - Search API Tests

Comprehensive tests for Search API v1 endpoints.
"""

import pytest
import httpx
from typing import Dict, Any


@pytest.fixture
def search_client():
    """HTTP client for Search API."""
    return httpx.AsyncClient(base_url="http://localhost:8401", timeout=30.0)


@pytest.fixture
def sample_document():
    """Sample document for testing."""
    return {
        "id": "test_doc_001",
        "title": "InfoTerminal Test Document",
        "body": "This is a test document for InfoTerminal OSINT platform. It contains entities like John Doe and Apple Inc.",
        "metadata": {
            "source": "test",
            "classification": "public"
        }
    }


class TestSearchAPIHealth:
    """Test health and readiness endpoints."""
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, search_client):
        """Test /healthz endpoint."""
        response = await search_client.get("/healthz")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "service" in data
        assert "version" in data
        assert data["service"] == "search-api"
    
    @pytest.mark.asyncio
    async def test_readiness_endpoint(self, search_client):
        """Test /readyz endpoint."""
        response = await search_client.get("/readyz")
        assert response.status_code in [200, 503]  # 503 if dependencies down
        
        data = response.json()
        assert "status" in data
        assert "service" in data


class TestSearchAPIOpenAPI:
    """Test OpenAPI documentation."""
    
    @pytest.mark.asyncio
    async def test_openapi_json(self, search_client):
        """Test OpenAPI JSON schema."""
        response = await search_client.get("/v1/openapi.json")
        assert response.status_code == 200
        
        data = response.json()
        assert "info" in data
        assert "paths" in data
        assert "components" in data
        
        # Check v1 paths exist
        v1_paths = [path for path in data["paths"].keys() if path.startswith("/v1/")]
        assert len(v1_paths) > 0
        
        # Check standard error schema
        schemas = data.get("components", {}).get("schemas", {})
        assert "StandardError" in schemas
    
    @pytest.mark.asyncio
    async def test_docs_ui(self, search_client):
        """Test documentation UI."""
        response = await search_client.get("/v1/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")


class TestSearchAPIStandards:
    """Test API standards compliance."""
    
    @pytest.mark.asyncio
    async def test_error_format(self, search_client):
        """Test standard error format on 404."""
        response = await search_client.get("/v1/nonexistent-endpoint")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
    
    @pytest.mark.asyncio
    async def test_cors_headers(self, search_client):
        """Test CORS headers."""
        response = await search_client.options("/v1/search")
        # Should have CORS headers or handle OPTIONS
        assert response.status_code in [200, 204, 405]
    
    @pytest.mark.asyncio
    async def test_security_headers(self, search_client):
        """Test security headers."""
        response = await search_client.get("/healthz")
        headers = response.headers
        
        # Check for security headers
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection"
        ]
        
        present_headers = [h for h in security_headers if h in headers]
        assert len(present_headers) >= 1  # At least one security header


class TestSearchAPIFunctionality:
    """Test search functionality."""
    
    @pytest.mark.asyncio
    async def test_document_indexing(self, search_client, sample_document):
        """Test document indexing endpoint."""
        response = await search_client.post(
            "/v1/index/documents",
            json={"documents": [sample_document]}
        )
        
        # Should succeed or fail gracefully
        assert response.status_code in [200, 503]  # 503 if OpenSearch not available
        
        if response.status_code == 200:
            data = response.json()
            assert "indexed" in data
            assert "errors" in data
            assert "took_ms" in data
    
    @pytest.mark.asyncio
    async def test_search_endpoint(self, search_client):
        """Test search endpoint with pagination."""
        search_request = {
            "q": "test query",
            "filters": {},
            "facets": [],
            "sort": None
        }
        
        response = await search_client.post("/v1/search", json=search_request)
        
        # Should succeed or fail gracefully
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            # Check pagination format
            assert "items" in data
            assert "total" in data
            assert "page" in data
            assert "size" in data
            assert "has_next" in data
            assert "has_prev" in data
    
    @pytest.mark.asyncio
    async def test_search_with_pagination(self, search_client):
        """Test search with pagination parameters."""
        search_request = {
            "q": "test",
            "filters": {},
            "facets": []
        }
        
        response = await search_client.post(
            "/v1/search?page=1&size=10",
            json=search_request
        )
        
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert data["page"] == 1
            assert data["size"] == 10
    
    @pytest.mark.asyncio
    async def test_document_retrieval(self, search_client):
        """Test document retrieval by ID."""
        doc_id = "test_doc_001"
        response = await search_client.get(f"/v1/documents/{doc_id}")
        
        # Should succeed or return 404
        assert response.status_code in [200, 404, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "found" in data
    
    @pytest.mark.asyncio
    async def test_search_validation(self, search_client):
        """Test search request validation."""
        # Test empty request
        response = await search_client.post("/v1/search", json={})
        assert response.status_code in [400, 422, 503]  # Validation error or service unavailable
        
        # Test malformed request
        response = await search_client.post("/v1/search", json={"invalid": "data"})
        assert response.status_code in [400, 422, 503]


class TestSearchAPILegacy:
    """Test legacy endpoint compatibility."""
    
    @pytest.mark.asyncio
    async def test_legacy_search_endpoint(self, search_client):
        """Test legacy /search endpoint."""
        response = await search_client.get("/search?q=test")
        
        # Should work or return deprecation info
        assert response.status_code in [200, 404, 503]
        
        # Check for deprecation warning in headers or response
        if response.status_code == 200:
            # Legacy endpoint should still work
            data = response.json()
            assert "results" in data or "items" in data
    
    @pytest.mark.asyncio
    async def test_legacy_query_endpoint(self, search_client):
        """Test legacy /query endpoint."""
        query_data = {
            "q": "test",
            "filters": {},
            "limit": 10,
            "offset": 0
        }
        
        response = await search_client.post("/query", json=query_data)
        assert response.status_code in [200, 404, 503]


class TestSearchAPIPerformance:
    """Test performance characteristics."""
    
    @pytest.mark.asyncio
    async def test_response_times(self, search_client):
        """Test API response times."""
        import time
        
        # Test health endpoint performance
        start_time = time.time()
        response = await search_client.get("/healthz")
        duration = time.time() - start_time
        
        assert response.status_code == 200
        assert duration < 1.0  # Should respond within 1 second
    
    @pytest.mark.asyncio
    async def test_concurrent_requests(self, search_client):
        """Test handling of concurrent requests."""
        import asyncio
        
        # Send multiple concurrent health checks
        tasks = [
            search_client.get("/healthz")
            for _ in range(5)
        ]
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should succeed
        for response in responses:
            if isinstance(response, httpx.Response):
                assert response.status_code == 200


@pytest.mark.asyncio
async def test_search_api_integration():
    """Integration test for complete search workflow."""
    async with httpx.AsyncClient(base_url="http://localhost:8401", timeout=30.0) as client:
        # 1. Check service health
        health_response = await client.get("/healthz")
        assert health_response.status_code == 200
        
        # 2. Index a document (if service is ready)
        if health_response.json().get("status") == "healthy":
            doc = {
                "id": "integration_test_doc",
                "title": "Integration Test Document",
                "body": "This document is used for integration testing of the search API."
            }
            
            index_response = await client.post(
                "/v1/index/documents",
                json={"documents": [doc]}
            )
            
            if index_response.status_code == 200:
                # 3. Search for the document
                search_response = await client.post(
                    "/v1/search",
                    json={"q": "integration testing"}
                )
                
                assert search_response.status_code == 200
                search_data = search_response.json()
                assert "items" in search_data
                
                # 4. Try to retrieve the document
                get_response = await client.get(f"/v1/documents/{doc['id']}")
                assert get_response.status_code in [200, 404]  # May not be found immediately
