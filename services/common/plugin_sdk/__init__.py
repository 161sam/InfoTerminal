from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ToolSpec(BaseModel):
    name: str
    description: Optional[str] = None
    argsSchema: Dict[str, Any]
    resultSchema: Optional[Dict[str, Any]] = None
    timeoutMs: Optional[int] = 15000
    auth: str = "inherit"
    permissions: List[str] = Field(default_factory=list)


class PluginManifest(BaseModel):
    apiVersion: str = "v1"
    name: str
    version: str
    description: Optional[str] = None
    provider: Optional[str] = None
    capabilities: Dict[str, List[ToolSpec]]
    endpoints: Optional[Dict[str, str]] = None
