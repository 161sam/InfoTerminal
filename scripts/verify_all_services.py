#!/usr/bin/env python3
"""
InfoTerminal Service Verification Script
Verifies all 24+ services are properly implemented and connected.
"""

import os
import sys
import json
import time
import yaml
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class ServiceStatus:
    name: str
    port: int
    status: str  # 'healthy', 'unhealthy', 'not_found', 'timeout'
    response_time: Optional[float] = None
    version: Optional[str] = None
    endpoints: List[str] = None
    docker_running: bool = False
    has_v1_api: bool = False
    error: Optional[str] = None

class ServiceVerification:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.services_dir = project_root / "services"
        self.docker_compose_files = self._find_docker_compose_files()
        self.expected_services = self._load_expected_services()
        
    def _find_docker_compose_files(self) -> List[Path]:
        """Find all docker-compose files in the project."""
        files = []
        for file_pattern in ["docker-compose*.yml", "docker-compose*.yaml"]:
            files.extend(self.project_root.glob(file_pattern))
        return files
    
    def _load_expected_services(self) -> Dict[str, int]:
        """Load expected services from docker-compose files and services directory."""
        services = {}
        
        # From services directory
        if self.services_dir.exists():
            for service_dir in self.services_dir.iterdir():
                if service_dir.is_dir() and not service_dir.name.startswith('.'):
                    # Try to extract port from various sources
                    port = self._extract_service_port(service_dir.name)
                    if port:
                        services[service_dir.name] = port
        
        # From docker-compose files  
        for compose_file in self.docker_compose_files:
            try:
                with open(compose_file) as f:
                    compose_data = yaml.safe_load(f)
                    
                if 'services' in compose_data:
                    for service_name, config in compose_data['services'].items():
                        if 'ports' in config:
                            for port_mapping in config['ports']:
                                if isinstance(port_mapping, str):
                                    # Format: "8611:8080" or "${VAR:-8611}:8080"
                                    host_port = port_mapping.split(':')[0]
                                    if host_port.startswith('${') and ':-' in host_port:
                                        # Extract default port from ${VAR:-8611}
                                        port = int(host_port.split(':-')[1].rstrip('}'))
                                    else:
                                        port = int(host_port)
                                    services[service_name] = port
                                    break
            except Exception as e:
                print(f"Warning: Could not parse {compose_file}: {e}")
        
        return services
    
    def _extract_service_port(self, service_name: str) -> Optional[int]:
        """Extract service port from various sources."""
        # Port mapping from InfoTerminal convention
        port_map = {
            'search-api': 8611,
            'graph-api': 8612, 
            'doc-entities': 8613,
            'ops-controller': 8614,
            'egress-gateway': 8615,
            'auth-service': 8616,
            'verification': 8617,
            'media-forensics': 8618,
            'nifi': 8619,
            'rag-api': 8622,
            'collab-hub': 8625,
            'xai': 8626,
            'forensics': 8627,
            'federation-proxy': 8628,
            'performance-monitor': 8629,
            'cache-manager': 8630,
            'websocket-manager': 8631,
            'feedback-aggregator': 8632,
            'plugin-runner': 8621,
            'flowise-connector': 3417,
            'agent-connector': 8633,
            'graph-views': 8634,
            'gateway': 8635,
            'policy': 8636,
            'openbb-connector': 8637,
            'opa-audit-sink': 8638,
            'common': None,  # Shared library
            '_shared': None,  # Shared library
            'archive': 8639,
        }
        
        return port_map.get(service_name)
    
    def check_service_health(self, service_name: str, port: int, timeout: int = 10) -> ServiceStatus:
        """Check if a service is healthy by calling its health endpoint."""
        
        # Try common health check endpoints
        health_endpoints = [
            f"http://localhost:{port}/health",
            f"http://localhost:{port}/healthz", 
            f"http://localhost:{port}/v1/health",
            f"http://localhost:{port}/",
        ]
        
        status = ServiceStatus(name=service_name, port=port, status='not_found', endpoints=[])
        
        start_time = time.time()
        
        for endpoint in health_endpoints:
            try:
                response = requests.get(endpoint, timeout=timeout)
                response_time = time.time() - start_time
                
                if response.status_code == 200:
                    status.status = 'healthy'
                    status.response_time = response_time
                    status.endpoints.append(endpoint)
                    
                    # Try to extract version info
                    try:
                        data = response.json()
                        if isinstance(data, dict):
                            status.version = data.get('version', data.get('service_version'))
                    except:
                        pass
                    
                    break
                elif response.status_code < 500:
                    status.status = 'unhealthy'
                    status.response_time = response_time
                    status.endpoints.append(endpoint)
                    status.error = f"HTTP {response.status_code}"
                    
            except requests.exceptions.Timeout:
                status.status = 'timeout'
                status.error = f"Timeout after {timeout}s"
            except requests.exceptions.ConnectionError:
                continue  # Try next endpoint
            except Exception as e:
                status.error = str(e)
        
        # Check for v1 API
        try:
            v1_response = requests.get(f"http://localhost:{port}/v1", timeout=5)
            if v1_response.status_code < 500:
                status.has_v1_api = True
        except:
            pass
        
        # Check if Docker container is running
        status.docker_running = self._check_docker_container(service_name)
        
        return status
    
    def _check_docker_container(self, service_name: str) -> bool:
        """Check if Docker container for service is running."""
        try:
            import subprocess
            result = subprocess.run(
                ['docker', 'ps', '--filter', f'name={service_name}', '--format', '{{.Names}}'],
                capture_output=True, text=True, timeout=10
            )
            return service_name in result.stdout
        except:
            return False
    
    def check_service_implementation(self, service_name: str) -> Dict[str, bool]:
        """Check if service has proper implementation structure."""
        service_dir = self.services_dir / service_name
        
        checks = {
            'has_directory': service_dir.exists(),
            'has_dockerfile': (service_dir / 'Dockerfile').exists(),
            'has_app_py': (service_dir / 'app.py').exists(),
            'has_app_v1_py': (service_dir / 'app_v1.py').exists(),
            'has_requirements': (service_dir / 'requirements.txt').exists() or (service_dir / 'pyproject.toml').exists(),
            'has_routers': (service_dir / 'routers').exists(),
            'has_models': (service_dir / 'models').exists(),
        }
        
        return checks
    
    def verify_all_services(self) -> Dict[str, ServiceStatus]:
        """Verify all services concurrently."""
        results = {}
        
        print(f"🔍 Verifying {len(self.expected_services)} services...")
        print(f"📁 Services directory: {self.services_dir}")
        print(f"🐳 Docker Compose files: {len(self.docker_compose_files)}")
        print()
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            
            for service_name, port in self.expected_services.items():
                if port is None:
                    # Skip shared libraries
                    continue
                    
                future = executor.submit(self.check_service_health, service_name, port)
                futures[future] = service_name
            
            for future in as_completed(futures):
                service_name = futures[future]
                try:
                    status = future.result()
                    results[service_name] = status
                except Exception as e:
                    results[service_name] = ServiceStatus(
                        name=service_name,
                        port=self.expected_services[service_name],
                        status='error',
                        error=str(e)
                    )
        
        return results
    
    def generate_report(self, results: Dict[str, ServiceStatus]) -> str:
        """Generate a comprehensive verification report."""
        
        healthy = sum(1 for s in results.values() if s.status == 'healthy')
        total = len(results)
        
        report = [
            "# InfoTerminal Service Verification Report",
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"## 📊 Overall Status: {healthy}/{total} services healthy ({healthy/total*100:.1f}%)",
            ""
        ]
        
        # Group by status
        by_status = {}
        for status in results.values():
            category = status.status
            if category not in by_status:
                by_status[category] = []
            by_status[category].append(status)
        
        # Healthy services
        if 'healthy' in by_status:
            report.extend([
                f"## ✅ Healthy Services ({len(by_status['healthy'])})",
                ""
            ])
            
            for service in sorted(by_status['healthy'], key=lambda s: s.name):
                v1_indicator = " 🔄 v1-API" if service.has_v1_api else ""
                docker_indicator = " 🐳" if service.docker_running else ""
                report.append(f"- **{service.name}** (:{service.port}) - {service.response_time:.2f}s{v1_indicator}{docker_indicator}")
            report.append("")
        
        # Unhealthy services
        for status_type in ['unhealthy', 'timeout', 'not_found', 'error']:
            if status_type in by_status:
                status_emoji = {'unhealthy': '⚠️', 'timeout': '⏱️', 'not_found': '❌', 'error': '💥'}
                report.extend([
                    f"## {status_emoji[status_type]} {status_type.title()} Services ({len(by_status[status_type])})",
                    ""
                ])
                
                for service in sorted(by_status[status_type], key=lambda s: s.name):
                    error_info = f" - {service.error}" if service.error else ""
                    docker_info = " (🐳 Docker running)" if service.docker_running else " (🐳 Docker not running)"
                    report.append(f"- **{service.name}** (:{service.port}){docker_info}{error_info}")
                report.append("")
        
        # Service Implementation Status
        report.extend([
            "## 🏗️ Implementation Status",
            ""
        ])
        
        for service_name in sorted(self.expected_services.keys()):
            if self.expected_services[service_name] is None:
                continue
                
            impl = self.check_service_implementation(service_name)
            impl_score = sum(impl.values())
            total_checks = len(impl)
            
            status_emoji = "✅" if impl_score >= total_checks - 1 else ("⚠️" if impl_score >= 3 else "❌")
            
            impl_details = []
            if impl['has_app_v1_py']:
                impl_details.append("v1-API")
            if impl['has_routers']:
                impl_details.append("routers")
            if impl['has_models']:
                impl_details.append("models")
            
            details = f" ({', '.join(impl_details)})" if impl_details else ""
            report.append(f"- {status_emoji} **{service_name}**: {impl_score}/{total_checks}{details}")
        
        report.extend([
            "",
            "## 🔧 Recommendations",
            ""
        ])
        
        if 'not_found' in by_status:
            report.append("### Services to Start:")
            for service in by_status['not_found']:
                if service.docker_running:
                    report.append(f"- {service.name} (Docker running, but service not responding - check configuration)")
                else:
                    report.append(f"- {service.name} (Start Docker container)")
            report.append("")
        
        if 'unhealthy' in by_status or 'timeout' in by_status:
            report.append("### Services to Fix:")
            for service in by_status.get('unhealthy', []) + by_status.get('timeout', []):
                report.append(f"- {service.name} - {service.error}")
            report.append("")
        
        # Missing v1 APIs
        missing_v1 = [s for s in results.values() if s.status == 'healthy' and not s.has_v1_api]
        if missing_v1:
            report.append("### Services needing v1 API migration:")
            for service in missing_v1:
                report.append(f"- {service.name} (migrate to app_v1.py pattern)")
            report.append("")
        
        return "\n".join(report)

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    verifier = ServiceVerification(project_root)
    
    print("InfoTerminal Service Verification")
    print("=" * 50)
    
    results = verifier.verify_all_services()
    report = verifier.generate_report(results)
    
    # Save report
    report_file = project_root / "reports" / f"service_verification_{int(time.time())}.md"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(report)
    print(f"\n💾 Report saved to: {report_file}")
    
    # Also save JSON for programmatic use
    json_file = report_file.with_suffix('.json')
    with open(json_file, 'w') as f:
        json.dump({name: asdict(status) for name, status in results.items()}, f, indent=2)
    
    print(f"📊 JSON data saved to: {json_file}")

if __name__ == "__main__":
    main()
