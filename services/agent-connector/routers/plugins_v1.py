"""
Plugin Management Router for Agent Connector Service

Provides standardized v1 endpoints for plugin management, discovery, and execution.
All endpoints follow InfoTerminal API conventions with error envelopes and pagination.
"""

import os
import time
import json
import glob
import yaml
import httpx
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Depends, Query

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = SERVICE_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    PaginatedResponse,
    PaginationParams,
    StandardError,
    APIError,
    ErrorCodes
)

from ..models.requests import (
    PluginToggleRequest,
    PluginConfigRequest,
    PluginInvokeRequest,
    PluginRegistryFilter,
    PluginToolFilter,
    PluginStateFilter
)
from ..models.responses import (
    PluginRegistryResponse,
    PluginStateResponse,
    PluginToggleResponse,
    PluginConfigResponse,
    PluginToolsResponse,
    PluginInvokeResponse,
    PluginHealthResponse,
    PluginManifest,
    PluginRegistryItem,
    PluginStateItem,
    PluginTool
)

# Import legacy dependencies
try:
    from ..plugins.state import read_global, write_global, read_user, write_user
    from ..auth import require_user, require_admin
    from services.common.audit import audit_log
except ImportError:
    # Fallback implementations for testing
    def read_global(): return {}
    def write_global(data): pass
    def read_user(uid): return {}
    def write_user(uid, data): pass
    def require_user(): return {"sub": "test", "email": "test@example.com"}
    def require_admin(user): pass
    def audit_log(*args, **kwargs): pass

# Configuration
PLUGINS_DIR = Path(os.getenv("IT_PLUGINS_DIR", "plugins"))
API_VERSION = os.getenv("IT_PLUGIN_API_VERSION", "v1")
CACHE_TTL = int(os.getenv("IT_PLUGINS_CACHE_TTL_SEC", "30"))

# Optional jsonschema for validation
try:
    import jsonschema
except ImportError:
    jsonschema = None

router = APIRouter()

# Registry cache
_registry_cache = {"ts": 0.0, "items": []}


def _load_plugin_registry() -> List[PluginRegistryItem]:
    """Load and cache plugin registry from filesystem."""
    now = time.time()
    if _registry_cache["items"] and now - _registry_cache["ts"] < CACHE_TTL:
        return _registry_cache["items"]
    
    items = []
    try:
        for manifest_file in glob.glob(str(PLUGINS_DIR / "*" / "plugin.*")):
            try:
                manifest_path = Path(manifest_file)
                
                # Load manifest data
                if manifest_path.suffix.lower() in (".yml", ".yaml"):
                    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
                else:
                    data = json.loads(manifest_path.read_text(encoding="utf-8"))
                
                # Validate API version
                if data.get("apiVersion") != API_VERSION:
                    continue
                
                # Create manifest object
                manifest = PluginManifest(
                    name=data["name"],
                    version=data.get("version", "unknown"),
                    provider=data.get("provider"),
                    description=data.get("description"),
                    category=data.get("category"),
                    api_version=data.get("apiVersion", API_VERSION),
                    capabilities=data.get("capabilities"),
                    endpoints=data.get("endpoints"),
                    requirements=data.get("requirements"),
                    tags=data.get("tags")
                )
                
                # Create registry item
                item = PluginRegistryItem(
                    manifest=manifest,
                    status="available",
                    last_updated=datetime.fromtimestamp(manifest_path.stat().st_mtime)
                )
                items.append(item)
                
            except Exception as e:
                # Log error but continue processing other plugins
                print(f"Error loading plugin manifest {manifest_file}: {e}")
                continue
                
    except Exception as e:
        print(f"Error scanning plugins directory: {e}")
    
    _registry_cache.update(ts=now, items=items)
    return items


def _filter_registry(
    items: List[PluginRegistryItem], 
    filters: PluginRegistryFilter
) -> List[PluginRegistryItem]:
    """Filter plugin registry items based on filter criteria."""
    filtered = items
    
    if filters.category:
        filtered = [item for item in filtered if item.manifest.category == filters.category]
    
    if filters.provider:
        filtered = [item for item in filtered if item.manifest.provider == filters.provider]
    
    if filters.search:
        search_lower = filters.search.lower()
        filtered = [
            item for item in filtered 
            if (search_lower in item.manifest.name.lower() or 
                (item.manifest.description and search_lower in item.manifest.description.lower()))
        ]
    
    return filtered


def _get_user_id(user: dict) -> str:
    """Extract user ID from user object."""
    return user.get("sub") or user.get("email") or "anon"


# =============================================================================
# PLUGIN REGISTRY ENDPOINTS
# =============================================================================

@router.get(
    "/registry",
    response_model=PaginatedResponse[PluginRegistryItem],
    summary="List Plugin Registry",
    description="Get a paginated list of available plugins from the registry",
    tags=["Plugin Registry"]
)
def list_plugin_registry(
    pagination: PaginationParams = Depends(),
    category: Optional[str] = Query(None, description="Filter by plugin category"),
    provider: Optional[str] = Query(None, description="Filter by plugin provider"),
    search: Optional[str] = Query(None, description="Search in plugin name or description"),
    user: dict = Depends(require_user)
) -> PaginatedResponse[PluginRegistryItem]:
    """
    List all available plugins in the registry with optional filtering.
    
    Returns paginated list of plugins with their manifest information.
    """
    try:
        # Load registry
        all_items = _load_plugin_registry()
        
        # Apply filters
        filters = PluginRegistryFilter(
            category=category,
            provider=provider,
            search=search
        )
        filtered_items = _filter_registry(all_items, filters)
        
        # Apply pagination
        start = pagination.offset
        end = start + pagination.size
        paginated_items = filtered_items[start:end]
        
        return PaginatedResponse.create(paginated_items, len(filtered_items), pagination)
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve plugin registry",
            status_code=500,
            details={"error": str(e)}
        )


@router.get(
    "/registry/summary",
    response_model=PluginRegistryResponse,
    summary="Plugin Registry Summary",
    description="Get registry summary with categories and providers",
    tags=["Plugin Registry"]
)
def get_registry_summary(
    user: dict = Depends(require_user)
) -> PluginRegistryResponse:
    """
    Get summary information about the plugin registry.
    
    Returns total count, available categories, and providers.
    """
    try:
        items = _load_plugin_registry()
        
        # Extract categories and providers
        categories = list(set(item.manifest.category for item in items if item.manifest.category))
        providers = list(set(item.manifest.provider for item in items if item.manifest.provider))
        
        return PluginRegistryResponse(
            items=items,
            total=len(items),
            categories=sorted(categories),
            providers=sorted(providers)
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve registry summary",
            status_code=500,
            details={"error": str(e)}
        )


# =============================================================================
# PLUGIN STATE ENDPOINTS
# =============================================================================

@router.get(
    "/state",
    response_model=PaginatedResponse[PluginStateItem],
    summary="List Plugin States",
    description="Get user-specific and global plugin states (enabled/disabled, config)",
    tags=["Plugin State"]
)
def list_plugin_states(
    pagination: PaginationParams = Depends(),
    scope: Optional[str] = Query("user", regex="^(user|global|all)$", description="State scope to retrieve"),
    enabled_only: Optional[bool] = Query(False, description="Show only enabled plugins"),
    search: Optional[str] = Query(None, description="Search in plugin name"),
    user: dict = Depends(require_user)
) -> PaginatedResponse[PluginStateItem]:
    """
    List plugin states with configuration and enabled status.
    
    Combines global and user-specific settings based on scope parameter.
    """
    try:
        uid = _get_user_id(user)
        registry = _load_plugin_registry()
        
        # Load state data
        global_state = read_global()
        user_state = read_user(uid)
        
        # Build state items
        state_items = []
        for item in registry:
            plugin_name = item.manifest.name
            
            # Get global and user config
            global_config = global_state.get(plugin_name, {})
            user_config = user_state.get(plugin_name, {})
            
            # Create state items based on scope
            if scope in ["global", "all"]:
                global_item = PluginStateItem(
                    name=plugin_name,
                    version=item.manifest.version,
                    provider=item.manifest.provider,
                    enabled=global_config.get("enabled", False),
                    config=global_config.get("config", {}),
                    scope="global"
                )
                state_items.append(global_item)
            
            if scope in ["user", "all"]:
                # Merge global and user config for user scope
                merged_config = {**global_config.get("config", {}), **user_config.get("config", {})}
                user_enabled = user_config.get("enabled", global_config.get("enabled", False))
                
                user_item = PluginStateItem(
                    name=plugin_name,
                    version=item.manifest.version,
                    provider=item.manifest.provider,
                    enabled=user_enabled,
                    config=merged_config,
                    scope="user"
                )
                state_items.append(user_item)
        
        # Apply filters
        if enabled_only:
            state_items = [item for item in state_items if item.enabled]
        
        if search:
            search_lower = search.lower()
            state_items = [item for item in state_items if search_lower in item.name.lower()]
        
        # Apply pagination
        start = pagination.offset
        end = start + pagination.size
        paginated_items = state_items[start:end]
        
        return PaginatedResponse.create(paginated_items, len(state_items), pagination)
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to retrieve plugin states",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/{plugin_name}/enable",
    response_model=PluginToggleResponse,
    summary="Enable/Disable Plugin",
    description="Enable or disable a plugin for user or global scope",
    tags=["Plugin State"]
)
def toggle_plugin(
    plugin_name: str,
    request_body: PluginToggleRequest,
    request: Request,
    user: dict = Depends(require_user)
) -> PluginToggleResponse:
    """
    Enable or disable a plugin.
    
    Can be scoped to the current user or globally (requires admin).
    """
    try:
        uid = _get_user_id(user)
        
        # Check if plugin exists
        registry = _load_plugin_registry()
        plugin_exists = any(item.manifest.name == plugin_name for item in registry)
        if not plugin_exists:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message=f"Plugin '{plugin_name}' not found in registry",
                status_code=404
            )
        
        # Get previous state
        if request_body.scope == "global":
            require_admin(user)
            current_state = read_global()
            previous_enabled = current_state.get(plugin_name, {}).get("enabled", False)
            
            # Update global state
            current_state[plugin_name] = {
                **current_state.get(plugin_name, {}),
                "enabled": request_body.enabled
            }
            write_global(current_state)
            
            # Audit log
            audit_log(
                "plugin.enable",
                uid,
                request.headers.get("X-Tenant-Id", "default"),
                {"name": plugin_name, "scope": "global", "enabled": request_body.enabled}
            )
            
        else:  # user scope
            current_state = read_user(uid)
            previous_enabled = current_state.get(plugin_name, {}).get("enabled", False)
            
            # Update user state
            current_state[plugin_name] = {
                **current_state.get(plugin_name, {}),
                "enabled": request_body.enabled
            }
            write_user(uid, current_state)
            
            # Audit log
            audit_log(
                "plugin.enable",
                uid,
                request.headers.get("X-Tenant-Id", "default"),
                {"name": plugin_name, "scope": "user", "enabled": request_body.enabled}
            )
        
        return PluginToggleResponse(
            name=plugin_name,
            enabled=request_body.enabled,
            scope=request_body.scope,
            previous_enabled=previous_enabled
        )
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to toggle plugin '{plugin_name}'",
            status_code=500,
            details={"error": str(e)}
        )


# =============================================================================
# PLUGIN CONFIGURATION ENDPOINTS
# =============================================================================

@router.get(
    "/{plugin_name}/config",
    response_model=PluginConfigResponse,
    summary="Get Plugin Configuration",
    description="Get current configuration for a plugin (merged user + global)",
    tags=["Plugin Configuration"]
)
def get_plugin_config(
    plugin_name: str,
    user: dict = Depends(require_user)
) -> PluginConfigResponse:
    """
    Get the current configuration for a plugin.
    
    Returns merged configuration from global and user-specific settings.
    """
    try:
        uid = _get_user_id(user)
        
        # Load configurations
        global_config = read_global().get(plugin_name, {}).get("config", {})
        user_config = read_user(uid).get(plugin_name, {}).get("config", {})
        
        # Merge configurations (user overrides global)
        merged_config = {**global_config, **user_config}
        
        return PluginConfigResponse(
            name=plugin_name,
            config=merged_config,
            scope="merged"
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to retrieve configuration for plugin '{plugin_name}'",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/{plugin_name}/config",
    response_model=PluginConfigResponse,
    summary="Set Plugin Configuration",
    description="Set configuration for a plugin (user or global scope)",
    tags=["Plugin Configuration"]
)
def set_plugin_config(
    plugin_name: str,
    request_body: PluginConfigRequest,
    request: Request,
    user: dict = Depends(require_user)
) -> PluginConfigResponse:
    """
    Set configuration for a plugin.
    
    Can be scoped to the current user or globally (requires admin).
    Secrets must be configured via environment variables, not API.
    """
    try:
        uid = _get_user_id(user)
        
        if request_body.scope == "global":
            require_admin(user)
            current_state = read_global()
            plugin_state = current_state.get(plugin_name, {})
            plugin_state["config"] = {
                **plugin_state.get("config", {}),
                **request_body.config
            }
            current_state[plugin_name] = plugin_state
            write_global(current_state)
            
            # Audit log
            audit_log(
                "plugin.config",
                uid,
                request.headers.get("X-Tenant-Id", "default"),
                {"name": plugin_name, "scope": "global"}
            )
            
            return PluginConfigResponse(
                name=plugin_name,
                config=plugin_state["config"],
                scope="global"
            )
            
        else:  # user scope
            current_state = read_user(uid)
            plugin_state = current_state.get(plugin_name, {})
            plugin_state["config"] = {
                **plugin_state.get("config", {}),
                **request_body.config
            }
            current_state[plugin_name] = plugin_state
            write_user(uid, current_state)
            
            # Audit log
            audit_log(
                "plugin.config",
                uid,
                request.headers.get("X-Tenant-Id", "default"),
                {"name": plugin_name, "scope": "user"}
            )
            
            return PluginConfigResponse(
                name=plugin_name,
                config=plugin_state["config"],
                scope="user"
            )
            
    except APIError:
        raise
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to set configuration for plugin '{plugin_name}'",
            status_code=500,
            details={"error": str(e)}
        )


# =============================================================================
# TOOL DISCOVERY AND INVOCATION ENDPOINTS
# =============================================================================

@router.get(
    "/tools",
    response_model=PluginToolsResponse,
    summary="Discover Available Tools",
    description="List all available tools from enabled plugins",
    tags=["Tool Discovery"]
)
def list_tools(
    plugin: Optional[str] = Query(None, description="Filter by specific plugin name"),
    category: Optional[str] = Query(None, description="Filter by tool category"),
    search: Optional[str] = Query(None, description="Search in tool name or description"),
    user: dict = Depends(require_user)
) -> PluginToolsResponse:
    """
    Discover available tools from all plugins.
    
    Returns comprehensive list of tools with their schemas and capabilities.
    """
    try:
        # Load registry
        registry = _load_plugin_registry()
        
        # Build tools list
        tools = []
        plugins = set()
        categories = set()
        
        for item in registry:
            plugin_name = item.manifest.name
            capabilities = item.manifest.capabilities or {}
            plugin_tools = capabilities.get("tools", [])
            
            plugins.add(plugin_name)
            
            for tool_def in plugin_tools:
                tool = PluginTool(
                    name=tool_def["name"],
                    plugin=plugin_name,
                    description=tool_def.get("description"),
                    category=tool_def.get("category"),
                    args_schema=tool_def.get("argsSchema"),
                    capabilities=tool_def.get("capabilities"),
                    examples=tool_def.get("examples")
                )
                
                if tool.category:
                    categories.add(tool.category)
                
                tools.append(tool)
        
        # Apply filters
        if plugin:
            tools = [t for t in tools if t.plugin == plugin]
        
        if category:
            tools = [t for t in tools if t.category == category]
        
        if search:
            search_lower = search.lower()
            tools = [
                t for t in tools 
                if (search_lower in t.name.lower() or 
                    (t.description and search_lower in t.description.lower()))
            ]
        
        return PluginToolsResponse(
            api_version=API_VERSION,
            tools=tools,
            total=len(tools),
            plugins=sorted(list(plugins)),
            categories=sorted(list(categories))
        )
        
    except Exception as e:
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message="Failed to discover tools",
            status_code=500,
            details={"error": str(e)}
        )


@router.post(
    "/invoke/{plugin_name}/{tool_name}",
    response_model=PluginInvokeResponse,
    summary="Invoke Plugin Tool",
    description="Execute a specific tool from a plugin",
    tags=["Tool Invocation"]
)
async def invoke_tool(
    plugin_name: str,
    tool_name: str,
    request_body: PluginInvokeRequest,
    request: Request,
    user: dict = Depends(require_user)
) -> PluginInvokeResponse:
    """
    Invoke a specific tool from a plugin.
    
    Validates arguments against schema if available and proxies the request
    to the plugin's tool endpoint.
    """
    start_time = time.time()
    uid = _get_user_id(user)
    tenant = request.headers.get("X-Tenant-Id", "default")
    request_id = request.headers.get("X-Request-Id", "")
    
    try:
        # Find plugin in registry
        registry = _load_plugin_registry()
        plugin_item = next(
            (item for item in registry if item.manifest.name == plugin_name), 
            None
        )
        
        if not plugin_item:
            raise APIError(
                code=ErrorCodes.RESOURCE_NOT_FOUND,
                message=f"Plugin '{plugin_name}' not found",
                status_code=404
            )
        
        manifest = plugin_item.manifest
        base_url = (manifest.endpoints or {}).get("baseUrl")
        
        if not base_url:
            raise APIError(
                code=ErrorCodes.EXTERNAL_SERVICE_ERROR,
                message=f"Plugin '{plugin_name}' missing baseUrl configuration",
                status_code=502
            )
        
        # Validate arguments against schema if available
        if jsonschema and manifest.capabilities:
            tools = manifest.capabilities.get("tools", [])
            tool_spec = next((t for t in tools if t.get("name") == tool_name), None)
            
            if tool_spec and tool_spec.get("argsSchema"):
                try:
                    jsonschema.validate(
                        instance=request_body.args, 
                        schema=tool_spec["argsSchema"]
                    )
                except Exception as e:
                    raise APIError(
                        code=ErrorCodes.VALIDATION_ERROR,
                        message=f"Arguments validation failed: {e}",
                        status_code=400
                    )
        
        # Prepare headers for plugin request
        headers = {}
        for header in ("Authorization", "X-Request-Id", "X-Tenant-Id"):
            value = request.headers.get(header)
            if value:
                headers[header] = value
        
        # Make request to plugin
        url = f"{base_url.rstrip('/')}/tools/{tool_name}"
        timeout = httpx.Timeout(request_body.timeout or 15.0)
        
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                url,
                json=request_body.args,
                headers=headers
            )
            
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            if response.status_code >= 400:
                # Audit log error
                audit_log(
                    "plugin.invoke",
                    uid,
                    tenant,
                    {"plugin": plugin_name, "tool": tool_name},
                    "error",
                    {"status_code": response.status_code, "detail": response.text},
                    req_id=request_id
                )
                
                raise APIError(
                    code=ErrorCodes.EXTERNAL_SERVICE_ERROR,
                    message=f"Plugin tool execution failed: {response.text}",
                    status_code=response.status_code
                )
            
            result = response.json()
            
            # Audit log success
            audit_log(
                "plugin.invoke",
                uid,
                tenant,
                {"plugin": plugin_name, "tool": tool_name},
                "ok",
                req_id=request_id
            )
            
            return PluginInvokeResponse(
                success=True,
                result=result,
                plugin=plugin_name,
                tool=tool_name,
                execution_time_ms=execution_time_ms,
                request_id=request_id
            )
            
    except APIError:
        raise
    except Exception as e:
        # Audit log error
        audit_log(
            "plugin.invoke",
            uid,
            tenant,
            {"plugin": plugin_name, "tool": tool_name},
            "error",
            {"detail": str(e)},
            req_id=request_id
        )
        
        raise APIError(
            code=ErrorCodes.INTERNAL_ERROR,
            message=f"Failed to invoke tool '{tool_name}' from plugin '{plugin_name}'",
            status_code=500,
            details={"error": str(e)}
        )


# =============================================================================
# PLUGIN HEALTH ENDPOINTS
# =============================================================================

@router.get(
    "/{plugin_name}/health",
    response_model=PluginHealthResponse,
    summary="Check Plugin Health",
    description="Check the health status of a specific plugin",
    tags=["Plugin Health"]
)
async def check_plugin_health(
    plugin_name: str,
    request: Request,
    user: dict = Depends(require_user)
) -> PluginHealthResponse:
    """
    Check the health status of a plugin.
    
    Makes a request to the plugin's health endpoint and returns status information.
    """
    try:
        # Find plugin in registry
        registry = _load_plugin_registry()
        plugin_item = next(
            (item for item in registry if item.manifest.name == plugin_name), 
            None
        )
        
        if not plugin_item:
            return PluginHealthResponse(
                name=plugin_name,
                status="unknown",
                error="Plugin not found in registry"
            )
        
        manifest = plugin_item.manifest
        base_url = (manifest.endpoints or {}).get("baseUrl")
        
        if not base_url:
            return PluginHealthResponse(
                name=plugin_name,
                status="unknown",
                error="Plugin missing baseUrl configuration"
            )
        
        # Determine health endpoint
        health_path = (manifest.endpoints or {}).get("health", "healthz")
        url = f"{base_url.rstrip('/')}/{health_path}"
        
        # Prepare headers
        headers = {}
        for header in ("X-Request-Id", "X-Tenant-Id"):
            value = request.headers.get(header)
            if value:
                headers[header] = value
        
        # Make health check request
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url, headers=headers)
                latency_ms = int((time.time() - start_time) * 1000)
                
                if response.status_code < 400:
                    status = "up"
                else:
                    status = "degraded"
                
                return PluginHealthResponse(
                    name=plugin_name,
                    status=status,
                    latency_ms=latency_ms,
                    checked_at=int(time.time() * 1000),
                    endpoint=url
                )
                
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            return PluginHealthResponse(
                name=plugin_name,
                status="down",
                latency_ms=latency_ms,
                checked_at=int(time.time() * 1000),
                error=str(e),
                endpoint=url
            )
            
    except Exception as e:
        return PluginHealthResponse(
            name=plugin_name,
            status="unknown",
            error=f"Health check failed: {str(e)}"
        )
