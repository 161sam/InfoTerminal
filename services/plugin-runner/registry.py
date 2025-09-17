# Plugin Registry Management for InfoTerminal
# Enhanced plugin system with security sandboxing and result integration

import os
import json
import yaml
import asyncio
import tempfile
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import docker
from docker.errors import DockerException
import xml.etree.ElementTree as ET
import re

from pydantic import BaseModel, validator
import structlog

logger = structlog.get_logger()


class PluginConfig(BaseModel):
    name: str
    version: str
    description: str
    category: str
    author: str
    risk_level: str
    requires_network: bool
    requires_root: bool
    parameters: List[Dict[str, Any]]
    docker_image: Optional[str]
    command_templates: Dict[str, str]
    output_format: List[str]
    security: Dict[str, Any]
    output_parsing: Dict[str, Any]
    integration: Dict[str, Any]


class PluginExecutionResult(BaseModel):
    job_id: str
    plugin_name: str
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    execution_time: Optional[float] = None
    raw_output: str
    parsed_output: Dict[str, Any]
    output_files: List[str] = []
    graph_entities: List[Dict[str, Any]] = []
    search_documents: List[Dict[str, Any]] = []
    error: Optional[str] = None


class PluginRegistry:
    """Enhanced plugin registry with security validation and result processing."""
    
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, PluginConfig] = {}
        self.docker_client = None
        self._init_docker()
        self._load_plugins()
    
    def _init_docker(self):
        """Initialize Docker client if available."""
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except DockerException as e:
            logger.warning("Docker not available", error=str(e))
    
    def _load_plugins(self):
        """Load and validate all plugin configurations."""
        if not self.plugins_dir.exists():
            logger.warning("Plugins directory does not exist", path=str(self.plugins_dir))
            return
        
        loaded_count = 0
        for plugin_dir in self.plugins_dir.iterdir():
            if plugin_dir.is_dir():
                config_file = plugin_dir / "plugin.yaml"
                if config_file.exists():
                    try:
                        with open(config_file) as f:
                            config_data = yaml.safe_load(f)
                        
                        # Validate configuration
                        plugin_config = PluginConfig(**config_data)
                        
                        # Security validation
                        if self._validate_plugin_security(plugin_config):
                            self.plugins[plugin_config.name] = plugin_config
                            loaded_count += 1
                            logger.info("Plugin loaded", name=plugin_config.name, version=plugin_config.version)
                        else:
                            logger.error("Plugin security validation failed", name=plugin_config.name)
                    
                    except Exception as e:
                        logger.error("Failed to load plugin", plugin=plugin_dir.name, error=str(e))
        
        logger.info("Plugin registry initialized", total_plugins=loaded_count)
    
    def _validate_plugin_security(self, plugin_config: PluginConfig) -> bool:
        """Validate plugin security configuration."""
        security = plugin_config.security
        
        # Require sandboxing for high-risk plugins
        if plugin_config.risk_level == "high" and security.get("sandbox") != "docker":
            logger.error("High-risk plugin must use docker sandbox", plugin=plugin_config.name)
            return False
        
        # Validate timeout limits
        timeout = security.get("timeout", 300)
        if timeout > 600:  # Max 10 minutes
            logger.error("Plugin timeout too high", plugin=plugin_config.name, timeout=timeout)
            return False
        
        # Validate resource limits
        memory_limit = security.get("memory_limit", "256m")
        if not re.match(r'^\d+[kmg]?$', memory_limit.lower()):
            logger.error("Invalid memory limit format", plugin=plugin_config.name, limit=memory_limit)
            return False
        
        return True
    
    def list_plugins(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """List available plugins with optional category filter."""
        plugins_list = []
        
        for name, config in self.plugins.items():
            if category is None or config.category == category:
                plugins_list.append({
                    "name": config.name,
                    "version": config.version,
                    "description": config.description,
                    "category": config.category,
                    "risk_level": config.risk_level,
                    "parameters": config.parameters,
                    "output_formats": config.output_format
                })
        
        return plugins_list
    
    def get_plugin(self, name: str) -> Optional[PluginConfig]:
        """Get plugin configuration by name."""
        return self.plugins.get(name)
    
    async def execute_plugin(self, plugin_name: str, parameters: Dict[str, Any], 
                           job_id: str, output_format: str = "json") -> PluginExecutionResult:
        """Execute a plugin with the given parameters."""
        plugin_config = self.get_plugin(plugin_name)
        if not plugin_config:
            raise ValueError(f"Plugin '{plugin_name}' not found")
        
        result = PluginExecutionResult(
            job_id=job_id,
            plugin_name=plugin_name,
            status="running",
            started_at=datetime.utcnow(),
            parsed_output={},
            raw_output=""
        )
        
        try:
            # Validate parameters
            validated_params = self._validate_parameters(plugin_config, parameters)
            
            # Choose execution method based on security config
            if plugin_config.security.get("sandbox") == "docker":
                raw_output = await self._execute_in_docker(plugin_config, validated_params)
            else:
                raw_output = await self._execute_local(plugin_config, validated_params)
            
            result.raw_output = raw_output
            result.completed_at = datetime.utcnow()
            result.execution_time = (result.completed_at - result.started_at).total_seconds()
            
            # Parse output
            result.parsed_output = self._parse_output(plugin_config, raw_output, output_format)
            
            # Extract graph entities and search documents
            result.graph_entities = self._extract_graph_entities(plugin_config, result.parsed_output)
            result.search_documents = self._extract_search_documents(plugin_config, result.parsed_output)
            
            result.status = "completed"
            
        except Exception as e:
            result.status = "failed"
            result.error = str(e)
            result.completed_at = datetime.utcnow()
            logger.error("Plugin execution failed", plugin=plugin_name, error=str(e))
        
        return result
    
    def _validate_parameters(self, plugin_config: PluginConfig, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and sanitize plugin parameters."""
        validated = {}
        
        for param_config in plugin_config.parameters:
            param_name = param_config["name"]
            param_type = param_config["type"]
            required = param_config.get("required", False)
            default = param_config.get("default")
            
            # Get parameter value
            value = parameters.get(param_name, default)
            
            # Check required parameters
            if required and value is None:
                raise ValueError(f"Required parameter '{param_name}' is missing")
            
            # Skip validation for optional parameters with no value
            if value is None:
                continue
            
            # Type validation and conversion
            if param_type == "string":
                value = str(value)
                # Validation regex if provided
                if "validation" in param_config:
                    if not re.match(param_config["validation"], value):
                        raise ValueError(f"Parameter '{param_name}' does not match required format")
                
                # Choice validation
                if "choices" in param_config:
                    if value not in param_config["choices"]:
                        raise ValueError(f"Parameter '{param_name}' must be one of {param_config['choices']}")
                        
            elif param_type == "integer":
                try:
                    value = int(value)
                    # Range validation
                    if "min" in param_config and value < param_config["min"]:
                        raise ValueError(f"Parameter '{param_name}' must be >= {param_config['min']}")
                    if "max" in param_config and value > param_config["max"]:
                        raise ValueError(f"Parameter '{param_name}' must be <= {param_config['max']}")
                except ValueError:
                    raise ValueError(f"Parameter '{param_name}' must be an integer")
                    
            elif param_type == "boolean":
                if isinstance(value, str):
                    value = value.lower() in ("true", "1", "yes", "on")
                else:
                    value = bool(value)
            
            validated[param_name] = value
        
        return validated
    
    async def _execute_in_docker(self, plugin_config: PluginConfig, parameters: Dict[str, Any]) -> str:
        """Execute plugin in Docker container for security."""
        if not self.docker_client:
            raise RuntimeError("Docker not available")
        
        # Choose command template
        scan_type = parameters.get("scan_type", "default")
        if scan_type not in plugin_config.command_templates:
            scan_type = "default"
        
        command_template = plugin_config.command_templates[scan_type]
        command = command_template.format(**parameters)
        
        # Security settings
        security = plugin_config.security
        
        try:
            # Run container with security constraints
            container = self.docker_client.containers.run(
                plugin_config.docker_image,
                command,
                detach=True,
                remove=True,
                network_mode="bridge" if plugin_config.requires_network else "none",
                read_only=security.get("read_only_filesystem", True),
                mem_limit=security.get("memory_limit", "256m"),
                cpu_quota=int(float(security.get("cpu_limit", "1.0")) * 100000),
                cpu_period=100000,
                security_opt=["no-new-privileges:true"] if security.get("no_new_privileges", True) else [],
                cap_drop=["ALL"] if not plugin_config.requires_root else [],
            )
            
            # Wait for completion with timeout
            timeout = security.get("timeout", 300)
            try:
                container.wait(timeout=timeout)
                logs = container.logs().decode('utf-8', errors='ignore')
                return logs
            except:
                container.kill()
                raise asyncio.TimeoutError(f"Plugin execution timed out after {timeout} seconds")
                
        except DockerException as e:
            raise RuntimeError(f"Docker execution failed: {str(e)}")
    
    async def _execute_local(self, plugin_config: PluginConfig, parameters: Dict[str, Any]) -> str:
        """Execute plugin locally (less secure, for low-risk plugins only)."""
        if plugin_config.risk_level == "high":
            raise ValueError("High-risk plugins cannot be executed locally")
        
        # Choose command template  
        scan_type = parameters.get("scan_type", "default")
        if scan_type not in plugin_config.command_templates:
            scan_type = "default"
            
        command_template = plugin_config.command_templates[scan_type]
        command = command_template.format(**parameters)
        
        try:
            # Execute with timeout
            timeout = plugin_config.security.get("timeout", 300)
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT
            )
            
            stdout, _ = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return stdout.decode('utf-8', errors='ignore')
            
        except asyncio.TimeoutError:
            if process:
                process.kill()
            raise asyncio.TimeoutError(f"Plugin execution timed out after {timeout} seconds")
        except Exception as e:
            raise RuntimeError(f"Local execution failed: {str(e)}")
    
    def _parse_output(self, plugin_config: PluginConfig, raw_output: str, output_format: str) -> Dict[str, Any]:
        """Parse plugin output based on configuration."""
        parsing_config = plugin_config.output_parsing
        parser_type = parsing_config.get("parser", "generic")
        
        if parser_type == "nmap_xml_parser":
            return self._parse_nmap_xml(raw_output)
        elif parser_type == "whois_text_parser":
            return self._parse_whois_text(raw_output)
        elif parser_type == "subfinder_json_parser":
            return self._parse_subfinder_json(raw_output)
        else:
            # Generic parsing
            return {"raw_output": raw_output, "lines": raw_output.split('\n')}
    
    def _parse_nmap_xml(self, raw_output: str) -> Dict[str, Any]:
        """Parse nmap XML output."""
        try:
            # Extract XML from output
            xml_start = raw_output.find('<?xml')
            if xml_start != -1:
                xml_content = raw_output[xml_start:]
                root = ET.fromstring(xml_content)
                
                results = {
                    "scan_info": {},
                    "hosts": []
                }
                
                # Parse scan info
                scaninfo = root.find('scaninfo')
                if scaninfo is not None:
                    results["scan_info"] = dict(scaninfo.attrib)
                
                # Parse hosts
                for host in root.findall('host'):
                    host_data = {
                        "addresses": [],
                        "hostnames": [],
                        "ports": [],
                        "os": {}
                    }
                    
                    # Addresses
                    for addr in host.findall('address'):
                        host_data["addresses"].append(dict(addr.attrib))
                    
                    # Hostnames
                    hostnames = host.find('hostnames')
                    if hostnames is not None:
                        for hostname in hostnames.findall('hostname'):
                            host_data["hostnames"].append(dict(hostname.attrib))
                    
                    # Ports
                    ports = host.find('ports')
                    if ports is not None:
                        for port in ports.findall('port'):
                            port_data = dict(port.attrib)
                            state = port.find('state')
                            if state is not None:
                                port_data["state"] = dict(state.attrib)
                            service = port.find('service')
                            if service is not None:
                                port_data["service"] = dict(service.attrib)
                            host_data["ports"].append(port_data)
                    
                    results["hosts"].append(host_data)
                
                return results
        except Exception as e:
            logger.error("Failed to parse nmap XML", error=str(e))
        
        return {"raw_output": raw_output, "parse_error": "Failed to parse XML"}
    
    def _parse_whois_text(self, raw_output: str) -> Dict[str, Any]:
        """Parse whois text output."""
        results = {
            "domain": "",
            "registrar": "",
            "creation_date": "",
            "expiration_date": "",
            "name_servers": [],
            "contacts": {},
            "raw_whois": raw_output
        }
        
        lines = raw_output.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('%') or line.startswith('#'):
                continue
                
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                # Extract key information
                if 'domain name' in key or 'domain' in key:
                    results["domain"] = value
                elif 'registrar' in key:
                    results["registrar"] = value
                elif 'creation date' in key or 'created' in key:
                    results["creation_date"] = value
                elif 'expir' in key:
                    results["expiration_date"] = value
                elif 'name server' in key or 'nserver' in key:
                    if value not in results["name_servers"]:
                        results["name_servers"].append(value)
        
        return results
    
    def _parse_subfinder_json(self, raw_output: str) -> Dict[str, Any]:
        """Parse subfinder JSON Lines output."""
        results = {
            "subdomains": [],
            "sources": set(),
            "total_found": 0
        }
        
        for line in raw_output.split('\n'):
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    results["subdomains"].append(data)
                    if "source" in data:
                        results["sources"].add(data["source"])
                except json.JSONDecodeError:
                    continue
        
        results["sources"] = list(results["sources"])
        results["total_found"] = len(results["subdomains"])
        
        return results
    
    def _extract_graph_entities(self, plugin_config: PluginConfig, parsed_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract entities for graph database integration."""
        entities = []
        integration_config = plugin_config.integration
        
        if "graph_entities" not in integration_config:
            return entities
        
        for entity_config in integration_config["graph_entities"]:
            entity_type = entity_config["type"]
            id_field = entity_config["id_field"]
            properties = entity_config.get("properties", [])
            
            # Extract entities based on plugin type
            if plugin_config.name == "nmap" and entity_type == "Host":
                for host in parsed_output.get("hosts", []):
                    if host.get("addresses"):
                        ip_address = host["addresses"][0].get("addr", "")
                        entity = {
                            "type": "Host",
                            "id": ip_address,
                            "properties": {
                                "ip_address": ip_address,
                                "status": "up",
                                "scan_timestamp": datetime.utcnow().isoformat()
                            }
                        }
                        
                        # Add hostname if available
                        if host.get("hostnames"):
                            entity["properties"]["hostname"] = host["hostnames"][0].get("name", "")
                        
                        entities.append(entity)
            
            elif plugin_config.name == "subfinder" and entity_type == "Subdomain":
                for subdomain in parsed_output.get("subdomains", []):
                    entity = {
                        "type": "Subdomain", 
                        "id": subdomain.get("host", ""),
                        "properties": {
                            "host": subdomain.get("host", ""),
                            "source": subdomain.get("source", ""),
                            "discovered_at": datetime.utcnow().isoformat()
                        }
                    }
                    entities.append(entity)
        
        return entities
    
    def _extract_search_documents(self, plugin_config: PluginConfig, parsed_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract documents for search index integration."""
        documents = []
        integration_config = plugin_config.integration
        
        if not integration_config.get("search_indexing", {}).get("enabled", False):
            return documents
        
        # Create search documents based on plugin results
        if plugin_config.name == "nmap":
            for host in parsed_output.get("hosts", []):
                doc = {
                    "id": f"nmap_{host.get('addresses', [{}])[0].get('addr', '')}", 
                    "type": "nmap_scan",
                    "title": f"Nmap scan of {host.get('addresses', [{}])[0].get('addr', '')}",
                    "content": f"Host scan results: {json.dumps(host)}",
                    "metadata": {
                        "tool": "nmap",
                        "scan_timestamp": datetime.utcnow().isoformat(),
                        "ip_address": host.get('addresses', [{}])[0].get('addr', ''),
                        "ports_count": len(host.get('ports', []))
                    }
                }
                documents.append(doc)
        
        return documents
