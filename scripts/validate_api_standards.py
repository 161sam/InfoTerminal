#!/usr/bin/env python3
"""
InfoTerminal API Standards Validation Script

Validates that services are following InfoTerminal API standards:
- /v1 namespace usage
- Standard error handling
- Health/ready endpoints  
- Pagination patterns
- OpenAPI documentation
"""

import json
import sys
import asyncio
import requests
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Service port mappings
DEV_PORTS = {
    "search-api": 8401,
    "graph-api": 8402,
    "graph-views": 8403,
    "doc-entities": 8404,
    "auth-service": 8405
}

DOCKER_PORTS = {
    "search-api": 8611,
    "graph-api": 8612,
    "graph-views": 8613, 
    "doc-entities": 8614,
    "auth-service": 8616
}


class APIStandardsValidator:
    """Validates API standards compliance across InfoTerminal services."""
    
    def __init__(self, use_docker_ports: bool = False):
        self.ports = DOCKER_PORTS if use_docker_ports else DEV_PORTS
        self.results = {}
    
    def validate_service(self, service_name: str) -> Dict[str, Any]:
        """Validate a single service against API standards."""
        port = self.ports.get(service_name)
        if not port:
            return {"error": f"Unknown service: {service_name}"}
        
        base_url = f"http://localhost:{port}"
        results = {
            "service": service_name,
            "port": port,
            "base_url": base_url,
            "checks": {}
        }
        
        # Check 1: Health endpoints
        results["checks"]["health"] = self._check_health_endpoints(base_url)
        
        # Check 2: V1 namespace
        results["checks"]["v1_namespace"] = self._check_v1_namespace(base_url)
        
        # Check 3: OpenAPI documentation
        results["checks"]["openapi"] = self._check_openapi_docs(base_url)
        
        # Check 4: Error handling
        results["checks"]["error_handling"] = self._check_error_handling(base_url)
        
        # Check 5: Pagination
        results["checks"]["pagination"] = self._check_pagination_support(base_url)
        
        # Calculate overall score
        passed_checks = sum(1 for check in results["checks"].values() if check.get("passed", False))
        total_checks = len(results["checks"])
        results["score"] = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
        results["status"] = "PASS" if results["score"] >= 80 else "FAIL"
        
        return results
    
    def _check_health_endpoints(self, base_url: str) -> Dict[str, Any]:
        """Check if standard health endpoints are implemented."""
        try:
            # Check /healthz
            healthz_response = requests.get(f"{base_url}/healthz", timeout=5)
            healthz_valid = (
                healthz_response.status_code == 200 and
                "status" in healthz_response.json() and
                "service" in healthz_response.json()
            )
            
            # Check /readyz
            readyz_response = requests.get(f"{base_url}/readyz", timeout=5)
            readyz_valid = (
                readyz_response.status_code in [200, 503] and  # 503 is OK if dependencies are down
                "status" in readyz_response.json() and
                "service" in readyz_response.json()
            )
            
            return {
                "passed": healthz_valid and readyz_valid,
                "healthz_status": healthz_response.status_code,
                "readyz_status": readyz_response.status_code,
                "details": {
                    "healthz_valid": healthz_valid,
                    "readyz_valid": readyz_valid
                }
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "details": "Health endpoints not accessible"
            }
    
    def _check_v1_namespace(self, base_url: str) -> Dict[str, Any]:
        """Check if service uses /v1 namespace."""
        try:
            # Try to access /v1/docs (OpenAPI docs)
            docs_response = requests.get(f"{base_url}/v1/docs", timeout=5)
            docs_accessible = docs_response.status_code == 200
            
            # Try to access /v1/openapi.json
            openapi_response = requests.get(f"{base_url}/v1/openapi.json", timeout=5)
            openapi_accessible = openapi_response.status_code == 200
            
            # Check if OpenAPI schema uses /v1 paths
            v1_paths_found = False
            if openapi_accessible:
                try:
                    openapi_data = openapi_response.json()
                    paths = openapi_data.get("paths", {})
                    v1_paths_found = any(path.startswith("/v1/") for path in paths.keys())
                except:
                    pass
            
            return {
                "passed": docs_accessible and openapi_accessible and v1_paths_found,
                "details": {
                    "docs_accessible": docs_accessible,
                    "openapi_accessible": openapi_accessible,
                    "v1_paths_found": v1_paths_found
                }
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "details": "V1 namespace not accessible"
            }
    
    def _check_openapi_docs(self, base_url: str) -> Dict[str, Any]:
        """Check OpenAPI documentation quality."""
        try:
            response = requests.get(f"{base_url}/v1/openapi.json", timeout=5)
            if response.status_code != 200:
                return {
                    "passed": False,
                    "details": "OpenAPI JSON not accessible"
                }
            
            openapi_data = response.json()
            
            # Check required fields
            required_fields = ["info", "paths", "components"]
            has_required = all(field in openapi_data for field in required_fields)
            
            # Check info section
            info = openapi_data.get("info", {})
            has_title = "title" in info and info["title"]
            has_version = "version" in info and info["version"]
            has_description = "description" in info and info["description"]
            
            # Check for standard error schemas
            components = openapi_data.get("components", {})
            schemas = components.get("schemas", {})
            has_error_schemas = "StandardError" in schemas
            
            # Check for security schemes
            security_schemes = components.get("securitySchemes", {})
            has_auth = len(security_schemes) > 0
            
            return {
                "passed": has_required and has_title and has_version and has_description,
                "details": {
                    "has_required_fields": has_required,
                    "has_title": has_title,
                    "has_version": has_version,
                    "has_description": has_description,
                    "has_error_schemas": has_error_schemas,
                    "has_security_schemes": has_auth,
                    "path_count": len(openapi_data.get("paths", {}))
                }
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "details": "OpenAPI documentation check failed"
            }
    
    def _check_error_handling(self, base_url: str) -> Dict[str, Any]:
        """Check if service uses standard error handling."""
        try:
            # Try to trigger a 404 error
            response = requests.get(f"{base_url}/v1/nonexistent-endpoint", timeout=5)
            
            if response.status_code == 404:
                try:
                    error_data = response.json()
                    # Check for standard error format
                    has_error_envelope = (
                        "error" in error_data and
                        isinstance(error_data["error"], dict) and
                        "code" in error_data["error"] and
                        "message" in error_data["error"]
                    )
                    
                    return {
                        "passed": has_error_envelope,
                        "details": {
                            "status_code": response.status_code,
                            "has_error_envelope": has_error_envelope,
                            "response_sample": error_data
                        }
                    }
                except:
                    return {
                        "passed": False,
                        "details": "Error response is not valid JSON"
                    }
            else:
                return {
                    "passed": False,
                    "details": f"Expected 404, got {response.status_code}"
                }
                
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "details": "Error handling check failed"
            }
    
    def _check_pagination_support(self, base_url: str) -> Dict[str, Any]:
        """Check if list endpoints support pagination."""
        try:
            # Common list endpoints to check
            list_endpoints = ["/v1/search", "/v1/documents", "/v1/users", "/v1/entities"]
            
            pagination_found = False
            tested_endpoints = []
            
            for endpoint in list_endpoints:
                try:
                    # Try with pagination parameters
                    response = requests.get(
                        f"{base_url}{endpoint}?page=1&size=10",
                        timeout=5
                    )
                    
                    tested_endpoints.append({
                        "endpoint": endpoint,
                        "status": response.status_code,
                        "accessible": response.status_code in [200, 401, 403]  # Auth errors are OK
                    })
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            # Check for pagination metadata
                            has_pagination = (
                                "total" in data and
                                "page" in data and
                                "size" in data and
                                "items" in data
                            )
                            if has_pagination:
                                pagination_found = True
                                break
                        except:
                            pass
                            
                except:
                    tested_endpoints.append({
                        "endpoint": endpoint,
                        "status": "error",
                        "accessible": False
                    })
            
            return {
                "passed": pagination_found,
                "details": {
                    "pagination_found": pagination_found,
                    "tested_endpoints": tested_endpoints
                }
            }
            
        except Exception as e:
            return {
                "passed": False,
                "error": str(e),
                "details": "Pagination check failed"
            }
    
    def validate_all_services(self) -> Dict[str, Any]:
        """Validate all known services."""
        print("🔍 Validating InfoTerminal API Standards Compliance")
        print("=" * 60)
        
        all_results = {}
        total_score = 0
        service_count = 0
        
        for service_name in self.ports.keys():
            print(f"\n📋 Validating {service_name}...")
            result = self.validate_service(service_name)
            all_results[service_name] = result
            
            if "score" in result:
                total_score += result["score"]
                service_count += 1
            
            # Print summary
            status_emoji = "✅" if result.get("status") == "PASS" else "❌"
            score = result.get("score", 0)
            print(f"   {status_emoji} {service_name}: {score:.1f}% ({result.get('status', 'ERROR')})")
            
            # Print failed checks
            for check_name, check_result in result.get("checks", {}).items():
                if not check_result.get("passed", False):
                    print(f"      ⚠️  {check_name}: {check_result.get('details', 'Failed')}")
        
        # Overall summary
        overall_score = total_score / service_count if service_count > 0 else 0
        overall_status = "PASS" if overall_score >= 80 else "FAIL"
        
        print(f"\n📊 Overall Compliance Score: {overall_score:.1f}% ({overall_status})")
        
        if overall_status == "FAIL":
            print("\n🔧 Recommendations:")
            print("   • Review the API Migration Guide: docs/API_MIGRATION_GUIDE.md")
            print("   • Use the API standards package: services/_shared/api_standards/")
            print("   • Check service-specific implementation examples")
        
        return {
            "overall_score": overall_score,
            "overall_status": overall_status,
            "service_results": all_results,
            "summary": {
                "services_tested": service_count,
                "services_passing": sum(1 for r in all_results.values() if r.get("status") == "PASS"),
                "average_score": overall_score
            }
        }
    
    def generate_report(self, output_file: str = None) -> str:
        """Generate a detailed compliance report."""
        results = self.validate_all_services()
        
        report_lines = [
            "# InfoTerminal API Standards Compliance Report",
            f"Generated: {Path(__file__).name}",
            "",
            "## Summary",
            f"- **Overall Score**: {results['overall_score']:.1f}%",
            f"- **Status**: {results['overall_status']}",
            f"- **Services Tested**: {results['summary']['services_tested']}",
            f"- **Services Passing**: {results['summary']['services_passing']}",
            "",
            "## Service Details",
            ""
        ]
        
        for service_name, service_result in results["service_results"].items():
            score = service_result.get("score", 0)
            status = service_result.get("status", "ERROR")
            status_emoji = "✅" if status == "PASS" else "❌"
            
            report_lines.extend([
                f"### {service_name} {status_emoji}",
                f"- **Score**: {score:.1f}%",
                f"- **Status**: {status}",
                f"- **Port**: {service_result.get('port')}",
                ""
            ])
            
            # Add check details
            for check_name, check_result in service_result.get("checks", {}).items():
                check_emoji = "✅" if check_result.get("passed") else "❌"
                report_lines.append(f"- **{check_name}**: {check_emoji}")
                
                if not check_result.get("passed") and "details" in check_result:
                    details = check_result["details"]
                    if isinstance(details, str):
                        report_lines.append(f"  - {details}")
                    elif isinstance(details, dict):
                        for key, value in details.items():
                            report_lines.append(f"  - {key}: {value}")
            
            report_lines.append("")
        
        report_content = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, "w") as f:
                f.write(report_content)
            print(f"📄 Report saved to: {output_file}")
        
        return report_content


def main():
    """Main validation script entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate InfoTerminal API Standards")
    parser.add_argument("--service", help="Validate specific service")
    parser.add_argument("--docker", action="store_true", help="Use Docker ports")
    parser.add_argument("--report", help="Generate report file")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    
    args = parser.parse_args()
    
    validator = APIStandardsValidator(use_docker_ports=args.docker)
    
    if args.service:
        # Validate single service
        result = validator.validate_service(args.service)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Service: {result['service']}")
            print(f"Score: {result.get('score', 0):.1f}%")
            print(f"Status: {result.get('status', 'ERROR')}")
    else:
        # Validate all services
        if args.json:
            results = validator.validate_all_services()
            print(json.dumps(results, indent=2))
        elif args.report:
            validator.generate_report(args.report)
        else:
            validator.validate_all_services()


if __name__ == "__main__":
    main()
