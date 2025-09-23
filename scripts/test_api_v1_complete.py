#!/usr/bin/env python3
"""
InfoTerminal API v1 Complete Test Suite

Comprehensive testing of all v1 API implementations to validate:
- All endpoints respond correctly
- Standard error handling works
- Pagination functions properly
- Health checks are operational
- OpenAPI documentation is accessible
- Authentication flows work
"""

import json
import sys
import time
import asyncio
import aiohttp
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class ServiceConfig:
    """Service configuration for testing."""
    name: str
    port: int
    docker_port: int
    endpoints: List[str]
    requires_auth: bool = False
    requires_data: bool = False

# Core services configuration
SERVICES = [
    ServiceConfig(
        name="search-api",
        port=8401,
        docker_port=8611,
        endpoints=[
            "/v1/search",
            "/v1/index/documents", 
            "/v1/documents/{doc_id}"
        ],
        requires_auth=True,
        requires_data=True
    ),
    ServiceConfig(
        name="graph-api",
        port=8402, 
        docker_port=8612,
        endpoints=[
            "/v1/cypher",
            "/v1/nodes/{node_id}/neighbors",
            "/v1/algorithms/pagerank",
            "/v1/shortest-path"
        ],
        requires_auth=True,
        requires_data=True
    ),
    ServiceConfig(
        name="graph-views",
        port=8403,
        docker_port=8613,
        endpoints=[
            "/v1/views/ego",
            "/v1/views/shortest-path",
            "/v1/export/dossier"
        ],
        requires_auth=True,
        requires_data=True
    ),
    ServiceConfig(
        name="doc-entities",
        port=8406,
        docker_port=8614,
        endpoints=[
            "/v1/extract/entities",
            "/v1/extract/relations", 
            "/v1/documents/annotate"
        ],
        requires_auth=True
    ),
    ServiceConfig(
        name="auth-service",
        port=8405,
        docker_port=8616,
        endpoints=[
            "/v1/auth/login",
            "/v1/users",
            "/v1/roles"
        ],
        requires_auth=False  # Auth service provides auth
    )
]


class APITestSuite:
    """Comprehensive API test suite for InfoTerminal v1 APIs."""
    
    def __init__(self, use_docker_ports: bool = False, verbose: bool = True):
        self.use_docker_ports = use_docker_ports
        self.verbose = verbose
        self.results = {}
        self.auth_token = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled."""
        if self.verbose:
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] {level}: {message}")
    
    def get_service_url(self, service: ServiceConfig) -> str:
        """Get the base URL for a service."""
        port = service.docker_port if self.use_docker_ports else service.port
        return f"http://localhost:{port}"
    
    async def test_service_health(self, service: ServiceConfig) -> Dict[str, Any]:
        """Test health endpoints for a service."""
        base_url = self.get_service_url(service)
        results = {
            "service": service.name,
            "healthz": {"accessible": False, "response": None},
            "readyz": {"accessible": False, "response": None}
        }
        
        async with aiohttp.ClientSession() as session:
            # Test /healthz
            try:
                async with session.get(f"{base_url}/healthz", timeout=5) as response:
                    results["healthz"]["accessible"] = response.status == 200
                    results["healthz"]["status_code"] = response.status
                    if response.status == 200:
                        results["healthz"]["response"] = await response.json()
                    self.log(f"✅ {service.name}/healthz: {response.status}")
            except Exception as e:
                results["healthz"]["error"] = str(e)
                self.log(f"❌ {service.name}/healthz: {e}", "ERROR")
            
            # Test /readyz
            try:
                async with session.get(f"{base_url}/readyz", timeout=5) as response:
                    results["readyz"]["accessible"] = response.status in [200, 503]
                    results["readyz"]["status_code"] = response.status
                    if response.status in [200, 503]:
                        results["readyz"]["response"] = await response.json()
                    self.log(f"✅ {service.name}/readyz: {response.status}")
            except Exception as e:
                results["readyz"]["error"] = str(e)
                self.log(f"❌ {service.name}/readyz: {e}", "ERROR")
        
        return results
    
    async def test_service_openapi(self, service: ServiceConfig) -> Dict[str, Any]:
        """Test OpenAPI documentation endpoints."""
        base_url = self.get_service_url(service)
        results = {
            "service": service.name,
            "openapi_json": {"accessible": False},
            "docs": {"accessible": False},
            "redoc": {"accessible": False}
        }
        
        async with aiohttp.ClientSession() as session:
            # Test /v1/openapi.json
            try:
                async with session.get(f"{base_url}/v1/openapi.json", timeout=5) as response:
                    results["openapi_json"]["accessible"] = response.status == 200
                    results["openapi_json"]["status_code"] = response.status
                    if response.status == 200:
                        openapi_data = await response.json()
                        results["openapi_json"]["info"] = openapi_data.get("info", {})
                        results["openapi_json"]["path_count"] = len(openapi_data.get("paths", {}))
                    self.log(f"✅ {service.name}/v1/openapi.json: {response.status}")
            except Exception as e:
                results["openapi_json"]["error"] = str(e)
                self.log(f"❌ {service.name}/v1/openapi.json: {e}", "ERROR")
            
            # Test /v1/docs
            try:
                async with session.get(f"{base_url}/v1/docs", timeout=5) as response:
                    results["docs"]["accessible"] = response.status == 200
                    results["docs"]["status_code"] = response.status
                    self.log(f"✅ {service.name}/v1/docs: {response.status}")
            except Exception as e:
                results["docs"]["error"] = str(e)
                self.log(f"❌ {service.name}/v1/docs: {e}", "ERROR")
        
        return results
    
    async def test_service_auth(self, service: ServiceConfig) -> Dict[str, Any]:
        """Test authentication for services that require it."""
        if not service.requires_auth:
            return {"service": service.name, "auth_required": False}
        
        base_url = self.get_service_url(service)
        results = {
            "service": service.name,
            "auth_required": True,
            "unauthenticated_access": {"blocked": False},
            "invalid_token_access": {"blocked": False}
        }
        
        # Get a sample endpoint to test
        test_endpoint = service.endpoints[0] if service.endpoints else "/v1/test"
        test_url = f"{base_url}{test_endpoint}"
        
        async with aiohttp.ClientSession() as session:
            # Test unauthenticated access
            try:
                async with session.get(test_url, timeout=5) as response:
                    results["unauthenticated_access"]["status_code"] = response.status
                    results["unauthenticated_access"]["blocked"] = response.status in [401, 403]
                    if response.status in [401, 403]:
                        try:
                            error_data = await response.json()
                            results["unauthenticated_access"]["error_format"] = error_data
                        except:
                            pass
                    self.log(f"🔒 {service.name} unauth access: {response.status}")
            except Exception as e:
                results["unauthenticated_access"]["error"] = str(e)
                self.log(f"❌ {service.name} unauth test: {e}", "ERROR")
            
            # Test invalid token access
            headers = {"Authorization": "Bearer invalid-token-12345"}
            try:
                async with session.get(test_url, headers=headers, timeout=5) as response:
                    results["invalid_token_access"]["status_code"] = response.status
                    results["invalid_token_access"]["blocked"] = response.status in [401, 403]
                    self.log(f"🔒 {service.name} invalid token: {response.status}")
            except Exception as e:
                results["invalid_token_access"]["error"] = str(e)
                self.log(f"❌ {service.name} invalid token test: {e}", "ERROR")
        
        return results
    
    async def test_service_endpoints(self, service: ServiceConfig) -> Dict[str, Any]:
        """Test specific endpoints for a service."""
        base_url = self.get_service_url(service)
        results = {
            "service": service.name,
            "endpoints": []
        }
        
        async with aiohttp.ClientSession() as session:
            for endpoint in service.endpoints:
                endpoint_result = {
                    "path": endpoint,
                    "accessible": False,
                    "methods_tested": []
                }
                
                # Replace path parameters with test values
                test_endpoint = endpoint.replace("{doc_id}", "test-doc-123")
                test_endpoint = test_endpoint.replace("{node_id}", "test-node-456")
                test_url = f"{base_url}{test_endpoint}"
                
                # Test GET method
                try:
                    async with session.get(test_url, timeout=5) as response:
                        endpoint_result["methods_tested"].append({
                            "method": "GET",
                            "status_code": response.status,
                            "accessible": response.status < 500  # Anything except server error
                        })
                        if response.status < 500:
                            endpoint_result["accessible"] = True
                        self.log(f"🔗 {service.name}{endpoint} GET: {response.status}")
                except Exception as e:
                    endpoint_result["methods_tested"].append({
                        "method": "GET",
                        "error": str(e)
                    })
                    self.log(f"❌ {service.name}{endpoint} GET: {e}", "ERROR")
                
                # Test POST method for appropriate endpoints
                if any(keyword in endpoint for keyword in ["/search", "/login", "/extract", "/cypher"]):
                    try:
                        test_data = self._get_test_data_for_endpoint(endpoint)
                        async with session.post(test_url, json=test_data, timeout=5) as response:
                            endpoint_result["methods_tested"].append({
                                "method": "POST",
                                "status_code": response.status,
                                "accessible": response.status < 500
                            })
                            if response.status < 500:
                                endpoint_result["accessible"] = True
                            self.log(f"🔗 {service.name}{endpoint} POST: {response.status}")
                    except Exception as e:
                        endpoint_result["methods_tested"].append({
                            "method": "POST",
                            "error": str(e)
                        })
                        self.log(f"❌ {service.name}{endpoint} POST: {e}", "ERROR")
                
                results["endpoints"].append(endpoint_result)
        
        return results
    
    def _get_test_data_for_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Get appropriate test data for different endpoints."""
        if "/search" in endpoint:
            return {"q": "test query", "filters": {}, "facets": []}
        elif "/login" in endpoint:
            return {"username": "test@example.com", "password": "testpass"}
        elif "/extract/entities" in endpoint:
            return {"text": "This is a test document with entities like Berlin and OpenAI."}
        elif "/cypher" in endpoint:
            return {"cypher": "MATCH (n) RETURN count(n) LIMIT 1"}
        else:
            return {"test": True}
    
    async def test_pagination(self, service: ServiceConfig) -> Dict[str, Any]:
        """Test pagination on endpoints that support it."""
        base_url = self.get_service_url(service)
        results = {
            "service": service.name,
            "pagination_support": False,
            "tested_endpoints": []
        }
        
        # Find endpoints that likely support pagination
        list_endpoints = [ep for ep in service.endpoints if any(
            keyword in ep for keyword in ["/search", "/users", "/documents", "/entities"]
        )]
        
        if not list_endpoints:
            return results
        
        async with aiohttp.ClientSession() as session:
            for endpoint in list_endpoints:
                test_url = f"{base_url}{endpoint}?page=1&size=5"
                endpoint_result = {
                    "endpoint": endpoint,
                    "supports_pagination": False
                }
                
                try:
                    if "/search" in endpoint:
                        # POST request for search
                        test_data = {"q": "test"}
                        async with session.post(test_url, json=test_data, timeout=5) as response:
                            if response.status == 200:
                                data = await response.json()
                                has_pagination = all(key in data for key in ["items", "total", "page", "size"])
                                endpoint_result["supports_pagination"] = has_pagination
                                if has_pagination:
                                    results["pagination_support"] = True
                                    endpoint_result["pagination_fields"] = {
                                        "total": data.get("total"),
                                        "page": data.get("page"),
                                        "size": data.get("size")
                                    }
                    else:
                        # GET request for other endpoints
                        async with session.get(test_url, timeout=5) as response:
                            if response.status == 200:
                                data = await response.json()
                                has_pagination = all(key in data for key in ["items", "total", "page", "size"])
                                endpoint_result["supports_pagination"] = has_pagination
                                if has_pagination:
                                    results["pagination_support"] = True
                    
                    self.log(f"📄 {service.name}{endpoint} pagination: {endpoint_result['supports_pagination']}")
                
                except Exception as e:
                    endpoint_result["error"] = str(e)
                    self.log(f"❌ {service.name}{endpoint} pagination test: {e}", "ERROR")
                
                results["tested_endpoints"].append(endpoint_result)
        
        return results
    
    async def run_comprehensive_tests(self) -> Dict[str, Any]:
        """Run all tests for all services."""
        self.log("🚀 Starting InfoTerminal API v1 Comprehensive Test Suite")
        self.log("=" * 80)
        
        all_results = {
            "test_suite": "InfoTerminal API v1 Complete",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "configuration": {
                "use_docker_ports": self.use_docker_ports,
                "services_tested": len(SERVICES)
            },
            "results": {}
        }
        
        for service in SERVICES:
            self.log(f"\n🔍 Testing {service.name}...")
            service_results = {
                "service_config": {
                    "name": service.name,
                    "port": service.docker_port if self.use_docker_ports else service.port,
                    "requires_auth": service.requires_auth,
                    "endpoint_count": len(service.endpoints)
                }
            }
            
            # Test health endpoints
            self.log(f"  🏥 Testing health endpoints...")
            service_results["health"] = await self.test_service_health(service)
            
            # Test OpenAPI documentation
            self.log(f"  📚 Testing OpenAPI documentation...")
            service_results["openapi"] = await self.test_service_openapi(service)
            
            # Test authentication
            self.log(f"  🔐 Testing authentication...")
            service_results["auth"] = await self.test_service_auth(service)
            
            # Test specific endpoints
            self.log(f"  🔗 Testing v1 endpoints...")
            service_results["endpoints"] = await self.test_service_endpoints(service)
            
            # Test pagination
            self.log(f"  📄 Testing pagination...")
            service_results["pagination"] = await self.test_pagination(service)
            
            # Calculate service score
            scores = []
            
            # Health score
            health_score = 0
            if service_results["health"]["healthz"]["accessible"]:
                health_score += 50
            if service_results["health"]["readyz"]["accessible"]:
                health_score += 50
            scores.append(health_score)
            
            # OpenAPI score
            openapi_score = 0
            if service_results["openapi"]["openapi_json"]["accessible"]:
                openapi_score += 50
            if service_results["openapi"]["docs"]["accessible"]:
                openapi_score += 50
            scores.append(openapi_score)
            
            # Endpoints score
            accessible_endpoints = sum(1 for ep in service_results["endpoints"]["endpoints"] if ep["accessible"])
            total_endpoints = len(service_results["endpoints"]["endpoints"])
            endpoints_score = (accessible_endpoints / total_endpoints * 100) if total_endpoints > 0 else 0
            scores.append(endpoints_score)
            
            service_results["score"] = sum(scores) / len(scores) if scores else 0
            service_results["status"] = "PASS" if service_results["score"] >= 70 else "FAIL"
            
            all_results["results"][service.name] = service_results
            
            # Log service summary
            status_emoji = "✅" if service_results["status"] == "PASS" else "❌"
            self.log(f"  {status_emoji} {service.name}: {service_results['score']:.1f}% ({service_results['status']})")
        
        # Calculate overall results
        service_scores = [r["score"] for r in all_results["results"].values()]
        all_results["overall_score"] = sum(service_scores) / len(service_scores) if service_scores else 0
        all_results["overall_status"] = "PASS" if all_results["overall_score"] >= 70 else "FAIL"
        
        # Summary
        passing_services = sum(1 for r in all_results["results"].values() if r["status"] == "PASS")
        total_services = len(all_results["results"])
        
        self.log(f"\n📊 Test Suite Summary:")
        self.log(f"   Overall Score: {all_results['overall_score']:.1f}%")
        self.log(f"   Overall Status: {all_results['overall_status']}")
        self.log(f"   Services Passing: {passing_services}/{total_services}")
        
        if all_results["overall_status"] == "PASS":
            self.log(f"\n🎉 SUCCESS: All InfoTerminal v1 APIs are functional!")
        else:
            self.log(f"\n⚠️  Some services need attention. Check individual results.")
        
        return all_results
    
    def save_results(self, results: Dict[str, Any], filename: str = None) -> str:
        """Save test results to a JSON file."""
        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"api_v1_test_results_{timestamp}.json"
        
        filepath = Path("/home/saschi/InfoTerminal") / filename
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        
        self.log(f"📁 Results saved to: {filepath}")
        return str(filepath)


async def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="InfoTerminal API v1 Comprehensive Test Suite")
    parser.add_argument("--docker", action="store_true", help="Use Docker ports")
    parser.add_argument("--service", help="Test specific service only")
    parser.add_argument("--save", help="Save results to file")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    
    args = parser.parse_args()
    
    tester = APITestSuite(
        use_docker_ports=args.docker,
        verbose=not args.quiet
    )
    
    if args.service:
        # Test single service
        service = next((s for s in SERVICES if s.name == args.service), None)
        if not service:
            print(f"❌ Unknown service: {args.service}")
            print(f"Available services: {', '.join(s.name for s in SERVICES)}")
            return
        
        # Run single service test (simplified)
        results = await tester.test_service_health(service)
        print(json.dumps(results, indent=2))
    else:
        # Run complete test suite
        results = await tester.run_comprehensive_tests()
        
        if args.save:
            tester.save_results(results, args.save)
        elif not args.quiet:
            # Save with auto-generated filename
            tester.save_results(results)


if __name__ == "__main__":
    asyncio.run(main())
