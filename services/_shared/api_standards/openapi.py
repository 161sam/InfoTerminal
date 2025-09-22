"""
Standard OpenAPI Configuration for InfoTerminal APIs

Provides consistent OpenAPI/Swagger documentation across all services.
All services MUST use these OpenAPI standards for API documentation.
"""

import os
from typing import Dict, List, Optional, Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def get_standard_openapi_config(
    app: FastAPI,
    title: str,
    description: str,
    version: str,
    service_name: str,
    tags_metadata: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Generate standard OpenAPI configuration for InfoTerminal services.
    
    Args:
        app: FastAPI application instance
        title: API title
        description: API description
        version: API version
        service_name: Service name for server URLs
        tags_metadata: Optional tag metadata for grouping endpoints
        
    Returns:
        OpenAPI schema dictionary
    """
    
    # Standard server URLs based on environment
    servers = []
    
    # Development servers
    dev_port_map = {
        "search-api": "8401",
        "graph-api": "8402", 
        "graph-views": "8403",
        "doc-entities": "8404",
        "auth-service": "8405"
    }
    
    # Docker servers  
    docker_port_map = {
        "search-api": "8611",
        "graph-api": "8612",
        "graph-views": "8613", 
        "doc-entities": "8614",
        "auth-service": "8616"
    }
    
    # Add development server
    dev_port = dev_port_map.get(service_name, "8000")
    servers.append({
        "url": f"http://localhost:{dev_port}",
        "description": "Development server (local process)"
    })
    
    # Add Docker server
    docker_port = docker_port_map.get(service_name, "8000")
    servers.append({
        "url": f"http://localhost:{docker_port}",
        "description": "Development server (Docker container)"
    })
    
    # Add production server if configured
    if os.getenv("PRODUCTION_URL"):
        servers.append({
            "url": os.getenv("PRODUCTION_URL"),
            "description": "Production server"
        })
    
    # Standard contact information
    contact = {
        "name": "InfoTerminal API Support",
        "url": "https://github.com/161sam/InfoTerminal",
        "email": "support@infoterminal.org"
    }
    
    # Standard license
    license_info = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
    
    # Standard security schemes
    security_schemes = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT Bearer token authentication"
        },
        "ApiKeyAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key authentication"
        }
    }
    
    # Generate OpenAPI schema
    openapi_schema = get_openapi(
        title=title,
        version=version,
        description=description,
        routes=app.routes,
        servers=servers,
        tags=tags_metadata
    )
    
    # Add standard components
    openapi_schema["info"]["contact"] = contact
    openapi_schema["info"]["license"] = license_info
    
    # Add security schemes
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    
    openapi_schema["components"]["securitySchemes"] = security_schemes
    
    # Add standard error responses
    openapi_schema["components"]["schemas"].update({
        "StandardError": {
            "type": "object",
            "properties": {
                "error": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Error code for programmatic handling"
                        },
                        "message": {
                            "type": "string", 
                            "description": "Human-readable error message"
                        },
                        "details": {
                            "type": "object",
                            "description": "Additional error context"
                        }
                    },
                    "required": ["code", "message"]
                }
            },
            "required": ["error"]
        },
        "ValidationError": {
            "allOf": [
                {"$ref": "#/components/schemas/StandardError"},
                {
                    "type": "object",
                    "properties": {
                        "validation_errors": {
                            "type": "array",
                            "items": {"type": "object"},
                            "description": "List of field validation errors"
                        }
                    }
                }
            ]
        }
    })
    
    return openapi_schema


def setup_standard_openapi(
    app: FastAPI,
    title: str,
    description: str,
    version: str,
    service_name: str,
    tags_metadata: Optional[List[Dict[str, Any]]] = None
) -> None:
    """
    Set up standard OpenAPI configuration for FastAPI app.
    
    Args:
        app: FastAPI application instance
        title: API title
        description: API description  
        version: API version
        service_name: Service name for server URLs
        tags_metadata: Optional tag metadata for grouping endpoints
    """
    
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        app.openapi_schema = get_standard_openapi_config(
            app=app,
            title=title,
            description=description,
            version=version,
            service_name=service_name,
            tags_metadata=tags_metadata
        )
        
        return app.openapi_schema
    
    app.openapi = custom_openapi


# Standard tag metadata for common InfoTerminal services
STANDARD_TAGS_METADATA = {
    "search-api": [
        {
            "name": "search",
            "description": "Search operations across indexed documents"
        },
        {
            "name": "indexing", 
            "description": "Document indexing and management"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ],
    "graph-api": [
        {
            "name": "cypher",
            "description": "Cypher query execution"
        },
        {
            "name": "analytics",
            "description": "Graph analytics and algorithms"
        },
        {
            "name": "export",
            "description": "Graph data export functionality"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ],
    "graph-views": [
        {
            "name": "views",
            "description": "Graph visualization data endpoints"
        },
        {
            "name": "ego",
            "description": "Ego network views"
        },
        {
            "name": "paths",
            "description": "Path finding and shortest path queries"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ],
    "doc-entities": [
        {
            "name": "nlp",
            "description": "Natural language processing operations"
        },
        {
            "name": "entities",
            "description": "Named entity recognition and resolution"
        },
        {
            "name": "relations",
            "description": "Relation extraction and management"
        },
        {
            "name": "documents",
            "description": "Document processing and storage"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ],
    "auth-service": [
        {
            "name": "auth",
            "description": "Authentication and authorization"
        },
        {
            "name": "users",
            "description": "User management operations"
        },
        {
            "name": "roles",
            "description": "Role and permission management"
        },
        {
            "name": "sessions",
            "description": "Session management"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ]
}


def get_service_tags_metadata(service_name: str) -> List[Dict[str, Any]]:
    """
    Get standard tags metadata for a specific service.
    
    Args:
        service_name: Name of the service
        
    Returns:
        List of tag metadata dictionaries
    """
    return STANDARD_TAGS_METADATA.get(service_name, [
        {
            "name": "general",
            "description": "General API operations"
        },
        {
            "name": "health",
            "description": "Health and readiness checks"
        }
    ])


# Standard OpenAPI examples
STANDARD_EXAMPLES = {
    "error_response": {
        "summary": "Standard error response",
        "value": {
            "error": {
                "code": "RESOURCE_NOT_FOUND",
                "message": "The requested resource was not found",
                "details": {
                    "resource_id": "123",
                    "resource_type": "document"
                }
            }
        }
    },
    "validation_error": {
        "summary": "Validation error response",
        "value": {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": {
                    "field": "email"
                }
            },
            "validation_errors": [
                {
                    "field": "email",
                    "message": "Invalid email format",
                    "rejected_value": "invalid-email"
                }
            ]
        }
    },
    "paginated_response": {
        "summary": "Paginated response",
        "value": {
            "items": [
                {"id": "1", "name": "Item 1"},
                {"id": "2", "name": "Item 2"}
            ],
            "total": 150,
            "page": 1,
            "size": 20,
            "pages": 8,
            "has_next": True,
            "has_prev": False
        }
    }
}
