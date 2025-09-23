"""
InfoTerminal API v1 Test Framework

Comprehensive testing framework for InfoTerminal v1 APIs.
Tests API standards compliance, functionality, and integration.
"""

import asyncio
import json
import time
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path

import pytest
import httpx
from pydantic import BaseModel, ValidationError


@dataclass
class ServiceConfig:
    """Service configuration for testing."""
    name: str
    base_url: str
    health_endpoint: str = "/healthz"
    ready_endpoint: str = "/readyz"
    docs_endpoint: str = "/v1/docs"
    openapi_endpoint: str = "/v1/openapi.json"


@dataclass
class TestResult:
    """Test result container."""
    test_name: str
    service: str
    endpoint: str
    passed: bool
    duration_ms: float
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class APITestFramework:
    """Framework for testing InfoTerminal v1 APIs."""
    
    def __init__(self, services: List[ServiceConfig]):
        self.services = services
        self.results: List[TestResult] = []
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests for all services."""
        print("🧪 Starting InfoTerminal API v1 Test Suite")
        print("=" * 60)
        
        for service in self.services:
            print(f"\n📋 Testing {service.name}...")
            await self.test_service(service)
        
        await self.client.aclose()
        
        # Generate summary
        return self.generate_summary()
    
    async def test_service(self, service: ServiceConfig):
        """Run all tests for a single service."""
        # Test 1: Health Endpoints
        await self.test_health_endpoints(service)
        
        # Test 2: OpenAPI Documentation
        await self.test_openapi_docs(service)
        
        # Test 3: API Standards Compliance
        await self.test_api_standards(service)
        
        # Test 4: Endpoint Functionality
        await self.test_endpoints(service)
        
        # Test 5: Error Handling
        await self.test_error_handling(service)
    
    async def test_health_endpoints(self, service: ServiceConfig):
        """Test health and readiness endpoints."""
        # Test /healthz
        await self._test_endpoint(
            service=service,
            test_name="health_check",
            method="GET",
            endpoint=service.health_endpoint,
            expected_status=200,
            required_fields=["status", "service", "version"]
        )
        
        # Test /readyz
        await self._test_endpoint(
            service=service,
            test_name="readiness_check",
            method="GET",
            endpoint=service.ready_endpoint,
            expected_status=[200, 503],  # 503 is OK if dependencies are down
            required_fields=["status", "service", "version"]
        )
    
    async def test_openapi_docs(self, service: ServiceConfig):
        """Test OpenAPI documentation endpoints."""
        # Test OpenAPI JSON
        result = await self._test_endpoint(
            service=service,
            test_name="openapi_json",
            method="GET",
            endpoint=service.openapi_endpoint,
            expected_status=200,
            required_fields=["info", "paths", "components"]
        )
        
        if result.passed and result.details:
            openapi_data = result.details.get("response_data", {})
            
            # Validate OpenAPI structure
            await self._validate_openapi_structure(service, openapi_data)
        
        # Test docs UI accessibility
        await self._test_endpoint(
            service=service,
            test_name="docs_ui",
            method="GET",
            endpoint=service.docs_endpoint,
            expected_status=200,
            content_type="text/html"
        )
    
    async def test_api_standards(self, service: ServiceConfig):
        """Test API standards compliance."""
        if not await self._is_service_ready(service):
            print(f"   ⚠️  {service.name} not ready, skipping standards tests")
            return
        
        # Test error format on non-existent endpoint
        await self._test_endpoint(
            service=service,
            test_name="standard_error_format",
            method="GET",
            endpoint="/v1/nonexistent-endpoint",
            expected_status=404,
            validate_error_schema=True
        )
        
        # Test CORS headers
        await self._test_cors_headers(service)
        
        # Test security headers
        await self._test_security_headers(service)
    
    async def test_endpoints(self, service: ServiceConfig):
        """Test service-specific endpoints."""
        if service.name == "search-api":
            await self._test_search_api_endpoints(service)
        elif service.name == "graph-api":
            await self._test_graph_api_endpoints(service)
        elif service.name == "graph-views":
            await self._test_graph_views_endpoints(service)
        elif service.name == "doc-entities":
            await self._test_doc_entities_endpoints(service)
        elif service.name == "auth-service":
            await self._test_auth_service_endpoints(service)
    
    async def test_error_handling(self, service: ServiceConfig):
        """Test error handling scenarios."""
        if not await self._is_service_ready(service):
            return
        
        # Test malformed JSON
        await self._test_endpoint(
            service=service,
            test_name="malformed_json_error",
            method="POST",
            endpoint="/v1/test-endpoint",
            expected_status=[400, 404],
            json_data="invalid json",
            validate_error_schema=True
        )
        
        # Test invalid content type
        await self._test_endpoint(
            service=service,
            test_name="invalid_content_type",
            method="POST",
            endpoint="/v1/test-endpoint",
            expected_status=[400, 404, 415],
            content="not json",
            headers={"Content-Type": "text/plain"}
        )
    
    async def _test_endpoint(
        self,
        service: ServiceConfig,
        test_name: str,
        method: str,
        endpoint: str,
        expected_status: Union[int, List[int]],
        required_fields: Optional[List[str]] = None,
        json_data: Optional[Any] = None,
        content: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        content_type: Optional[str] = None,
        validate_error_schema: bool = False
    ) -> TestResult:
        """Test a single endpoint."""
        start_time = time.time()
        url = f"{service.base_url}{endpoint}"
        
        try:
            # Prepare request
            request_kwargs = {}
            if json_data is not None:
                if isinstance(json_data, str):
                    request_kwargs["content"] = json_data
                    request_kwargs["headers"] = {"Content-Type": "application/json"}
                else:
                    request_kwargs["json"] = json_data
            elif content is not None:
                request_kwargs["content"] = content
            
            if headers:
                request_kwargs.setdefault("headers", {}).update(headers)
            
            # Make request
            response = await self.client.request(method, url, **request_kwargs)
            duration_ms = (time.time() - start_time) * 1000
            
            # Check status code
            if isinstance(expected_status, list):
                status_ok = response.status_code in expected_status
            else:
                status_ok = response.status_code == expected_status
            
            if not status_ok:
                result = TestResult(
                    test_name=test_name,
                    service=service.name,
                    endpoint=endpoint,
                    passed=False,
                    duration_ms=duration_ms,
                    error=f"Expected status {expected_status}, got {response.status_code}",
                    details={"response_text": response.text[:500]}
                )
                self.results.append(result)
                return result
            
            # Parse response
            response_data = None
            if content_type == "text/html":
                if "text/html" not in response.headers.get("content-type", ""):
                    result = TestResult(
                        test_name=test_name,
                        service=service.name,
                        endpoint=endpoint,
                        passed=False,
                        duration_ms=duration_ms,
                        error=f"Expected HTML content, got {response.headers.get('content-type')}"
                    )
                    self.results.append(result)
                    return result
            else:
                try:
                    response_data = response.json()
                except:
                    if response.status_code < 400:  # Only fail if it's a success response
                        result = TestResult(
                            test_name=test_name,
                            service=service.name,
                            endpoint=endpoint,
                            passed=False,
                            duration_ms=duration_ms,
                            error="Response is not valid JSON",
                            details={"response_text": response.text[:200]}
                        )
                        self.results.append(result)
                        return result
            
            # Validate required fields
            if required_fields and response_data:
                missing_fields = []
                for field in required_fields:
                    if field not in response_data:
                        missing_fields.append(field)
                
                if missing_fields:
                    result = TestResult(
                        test_name=test_name,
                        service=service.name,
                        endpoint=endpoint,
                        passed=False,
                        duration_ms=duration_ms,
                        error=f"Missing required fields: {missing_fields}",
                        details={"response_data": response_data}
                    )
                    self.results.append(result)
                    return result
            
            # Validate error schema
            if validate_error_schema and response_data and response.status_code >= 400:
                if not self._validate_error_schema(response_data):
                    result = TestResult(
                        test_name=test_name,
                        service=service.name,
                        endpoint=endpoint,
                        passed=False,
                        duration_ms=duration_ms,
                        error="Error response does not follow standard schema",
                        details={"response_data": response_data}
                    )
                    self.results.append(result)
                    return result
            
            # Success
            result = TestResult(
                test_name=test_name,
                service=service.name,
                endpoint=endpoint,
                passed=True,
                duration_ms=duration_ms,
                details={
                    "status_code": response.status_code,
                    "response_data": response_data,
                    "headers": dict(response.headers)
                }
            )
            self.results.append(result)
            return result
            
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            result = TestResult(
                test_name=test_name,
                service=service.name,
                endpoint=endpoint,
                passed=False,
                duration_ms=duration_ms,
                error=str(e)
            )
            self.results.append(result)
            return result
    
    async def _is_service_ready(self, service: ServiceConfig) -> bool:
        """Check if service is ready for testing."""
        try:
            response = await self.client.get(f"{service.base_url}{service.health_endpoint}")
            return response.status_code == 200
        except:
            return False
    
    def _validate_error_schema(self, response_data: Dict[str, Any]) -> bool:
        """Validate error response follows standard schema."""
        if "error" not in response_data:
            return False
        
        error = response_data["error"]
        if not isinstance(error, dict):
            return False
        
        required_fields = ["code", "message"]
        return all(field in error for field in required_fields)
    
    async def _validate_openapi_structure(self, service: ServiceConfig, openapi_data: Dict[str, Any]):
        """Validate OpenAPI structure."""
        checks = []
        
        # Check info section
        info = openapi_data.get("info", {})
        checks.append(("has_title", "title" in info))
        checks.append(("has_version", "version" in info))
        checks.append(("has_description", "description" in info))
        
        # Check v1 paths
        paths = openapi_data.get("paths", {})
        v1_paths = [path for path in paths.keys() if path.startswith("/v1/")]
        checks.append(("has_v1_paths", len(v1_paths) > 0))
        
        # Check components
        components = openapi_data.get("components", {})
        schemas = components.get("schemas", {})
        checks.append(("has_error_schemas", "StandardError" in schemas))
        
        for check_name, passed in checks:
            result = TestResult(
                test_name=f"openapi_{check_name}",
                service=service.name,
                endpoint=service.openapi_endpoint,
                passed=passed,
                duration_ms=0,
                error=None if passed else f"OpenAPI validation failed: {check_name}"
            )
            self.results.append(result)
    
    async def _test_cors_headers(self, service: ServiceConfig):
        """Test CORS headers."""
        try:
            response = await self.client.options(f"{service.base_url}/v1/test")
            
            cors_headers = [
                "Access-Control-Allow-Origin",
                "Access-Control-Allow-Methods",
                "Access-Control-Allow-Headers"
            ]
            
            present_headers = [h for h in cors_headers if h in response.headers]
            
            result = TestResult(
                test_name="cors_headers",
                service=service.name,
                endpoint="/v1/test",
                passed=len(present_headers) > 0,
                duration_ms=0,
                details={"cors_headers": present_headers}
            )
            self.results.append(result)
            
        except Exception as e:
            result = TestResult(
                test_name="cors_headers",
                service=service.name,
                endpoint="/v1/test",
                passed=False,
                duration_ms=0,
                error=str(e)
            )
            self.results.append(result)
    
    async def _test_security_headers(self, service: ServiceConfig):
        """Test security headers."""
        try:
            response = await self.client.get(f"{service.base_url}{service.health_endpoint}")
            
            security_headers = [
                "X-Content-Type-Options",
                "X-Frame-Options",
                "X-XSS-Protection"
            ]
            
            present_headers = [h for h in security_headers if h in response.headers]
            
            result = TestResult(
                test_name="security_headers",
                service=service.name,
                endpoint=service.health_endpoint,
                passed=len(present_headers) >= 2,  # At least 2 security headers
                duration_ms=0,
                details={"security_headers": present_headers}
            )
            self.results.append(result)
            
        except Exception as e:
            result = TestResult(
                test_name="security_headers",
                service=service.name,
                endpoint=service.health_endpoint,
                passed=False,
                duration_ms=0,
                error=str(e)
            )
            self.results.append(result)
    
    # Service-specific endpoint tests
    async def _test_search_api_endpoints(self, service: ServiceConfig):
        """Test Search API specific endpoints."""
        # Test search endpoint with pagination
        await self._test_endpoint(
            service=service,
            test_name="search_pagination",
            method="POST",
            endpoint="/v1/search",
            expected_status=200,
            json_data={
                "q": "test query",
                "filters": {},
                "facets": []
            },
            required_fields=["items", "total", "page", "size"]
        )
        
        # Test document indexing
        await self._test_endpoint(
            service=service,
            test_name="document_indexing",
            method="POST",
            endpoint="/v1/index/documents",
            expected_status=200,
            json_data={
                "documents": [
                    {"id": "test_doc_1", "title": "Test Document", "body": "Test content"}
                ]
            },
            required_fields=["indexed", "errors", "took_ms"]
        )
    
    async def _test_graph_api_endpoints(self, service: ServiceConfig):
        """Test Graph API specific endpoints."""
        # Test Cypher endpoint
        await self._test_endpoint(
            service=service,
            test_name="cypher_query",
            method="POST",
            endpoint="/v1/cypher",
            expected_status=200,
            json_data={
                "query": "RETURN 1 as test",
                "parameters": {},
                "read_only": True
            },
            required_fields=["records", "took_ms"]
        )
        
        # Test algorithm endpoint
        await self._test_endpoint(
            service=service,
            test_name="algorithm_centrality",
            method="POST",
            endpoint="/v1/algorithms/centrality",
            expected_status=200,
            json_data={
                "algorithm": "pagerank",
                "parameters": {}
            },
            required_fields=["job_id", "status"]
        )
    
    async def _test_graph_views_endpoints(self, service: ServiceConfig):
        """Test Graph Views API specific endpoints."""
        # Test ego network view
        await self._test_endpoint(
            service=service,
            test_name="ego_network_view",
            method="GET",
            endpoint="/v1/views/ego?node_id=1&radius=2",
            expected_status=200,
            required_fields=["center_node", "nodes", "relationships", "metadata"]
        )
        
        # Test export endpoint
        await self._test_endpoint(
            service=service,
            test_name="dossier_export",
            method="GET",
            endpoint="/v1/export/dossier?node_id=1&radius=2&format=dossier",
            expected_status=200,
            required_fields=["format", "entities", "relationships"]
        )
    
    async def _test_doc_entities_endpoints(self, service: ServiceConfig):
        """Test Doc-Entities API specific endpoints."""
        # Test entity extraction
        await self._test_endpoint(
            service=service,
            test_name="entity_extraction",
            method="POST",
            endpoint="/v1/extract/entities",
            expected_status=200,
            json_data={
                "text": "John Doe works at Apple Inc in California.",
                "language": "en"
            },
            required_fields=["entities", "model", "processing_time_ms"]
        )
        
        # Test text summarization
        await self._test_endpoint(
            service=service,
            test_name="text_summarization",
            method="POST",
            endpoint="/v1/summarize",
            expected_status=200,
            json_data={
                "text": "This is a long text that needs to be summarized. It contains multiple sentences and important information.",
                "language": "en"
            },
            required_fields=["summary", "compression_ratio", "processing_time_ms"]
        )
    
    async def _test_auth_service_endpoints(self, service: ServiceConfig):
        """Test Auth Service API specific endpoints."""
        # Test user registration
        await self._test_endpoint(
            service=service,
            test_name="user_registration",
            method="POST",
            endpoint="/v1/auth/register",
            expected_status=[200, 409],  # 409 if user already exists
            json_data={
                "username": "testuser_api_test",
                "email": "testuser@example.com",
                "password": "testpassword123",
                "full_name": "Test User"
            }
        )
        
        # Test login
        await self._test_endpoint(
            service=service,
            test_name="user_login",
            method="POST",
            endpoint="/v1/auth/login",
            expected_status=200,
            json_data={
                "username": "admin",
                "password": "admin123"
            },
            required_fields=["access_token", "token_type", "user"]
        )
        
        # Test roles listing
        await self._test_endpoint(
            service=service,
            test_name="roles_listing",
            method="GET",
            endpoint="/v1/roles",
            expected_status=[200, 401]  # May require auth
        )
    
    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary."""
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.passed)
        failed_tests = total_tests - passed_tests
        
        # Group by service
        service_results = {}
        for result in self.results:
            if result.service not in service_results:
                service_results[result.service] = {"passed": 0, "failed": 0, "tests": []}
            
            if result.passed:
                service_results[result.service]["passed"] += 1
            else:
                service_results[result.service]["failed"] += 1
            
            service_results[result.service]["tests"].append(result)
        
        # Calculate overall score
        overall_score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Print summary
        print(f"\n📊 Test Summary")
        print("=" * 40)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {overall_score:.1f}%")
        
        print(f"\n📋 Service Results:")
        for service_name, results in service_results.items():
            total = results["passed"] + results["failed"]
            score = (results["passed"] / total * 100) if total > 0 else 0
            status = "✅" if score >= 80 else "❌"
            print(f"  {status} {service_name}: {score:.1f}% ({results['passed']}/{total})")
            
            # Show failed tests
            failed_tests = [t for t in results["tests"] if not t.passed]
            for test in failed_tests[:3]:  # Show first 3 failures
                print(f"    ⚠️  {test.test_name}: {test.error}")
        
        return {
            "overall_score": overall_score,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "service_results": service_results,
            "detailed_results": [
                {
                    "test_name": r.test_name,
                    "service": r.service,
                    "endpoint": r.endpoint,
                    "passed": r.passed,
                    "duration_ms": r.duration_ms,
                    "error": r.error
                }
                for r in self.results
            ]
        }


# Test configuration
SERVICES = [
    ServiceConfig(
        name="search-api",
        base_url="http://localhost:8401"
    ),
    ServiceConfig(
        name="graph-api", 
        base_url="http://localhost:8402"
    ),
    ServiceConfig(
        name="graph-views",
        base_url="http://localhost:8403"
    ),
    ServiceConfig(
        name="doc-entities",
        base_url="http://localhost:8404"
    ),
    ServiceConfig(
        name="auth-service",
        base_url="http://localhost:8405"
    )
]


async def main():
    """Run the complete test suite."""
    framework = APITestFramework(SERVICES)
    results = await framework.run_all_tests()
    
    # Save results
    output_file = Path(__file__).parent / "test_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Exit with appropriate code
    if results["overall_score"] >= 80:
        print("\n🎉 Test suite passed!")
        return 0
    else:
        print("\n❌ Test suite failed!")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
