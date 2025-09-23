"""Database configuration and session management."""

import os
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from . import Base

# Database configuration
DATABASE_URL = os.getenv(
    "AUTH_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/infoterminal_auth"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=20,
    max_overflow=0,
    echo=os.getenv("DEBUG", "false").lower() == "true"
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get database session dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database() -> None:
    """Initialize database with default data."""
    from . import Role, Permission
    
    db = SessionLocal()
    try:
        # Create default roles if they don't exist
        default_roles = [
            {
                "name": "admin",
                "display_name": "Administrator",
                "description": "Full system access and user management",
                "is_system": True,
                "priority": 1000,
                "color": "#dc2626",
                "icon": "shield-check"
            },
            {
                "name": "security_analyst",
                "display_name": "Security Analyst",
                "description": "Advanced security and verification features",
                "is_system": True,
                "priority": 800,
                "color": "#ea580c",
                "icon": "shield"
            },
            {
                "name": "intelligence_analyst",
                "display_name": "Intelligence Analyst",
                "description": "Full OSINT capabilities and analysis tools",
                "is_system": True,
                "priority": 600,
                "color": "#0891b2",
                "icon": "search"
            },
            {
                "name": "analyst",
                "display_name": "Analyst",
                "description": "Standard analysis and research capabilities",
                "is_default": True,
                "is_system": True,
                "priority": 400,
                "color": "#059669",
                "icon": "user-check"
            },
            {
                "name": "viewer",
                "display_name": "Viewer",
                "description": "Read-only access to search and basic features",
                "is_system": True,
                "priority": 200,
                "color": "#6b7280",
                "icon": "eye"
            }
        ]
        
        for role_data in default_roles:
            existing_role = db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing_role:
                role = Role(**role_data)
                db.add(role)
        
        # Create default permissions
        default_permissions = [
            # Search service permissions
            ("search:read", "Search Read", "View search results", "search", "read"),
            ("search:write", "Search Write", "Create and modify searches", "search", "write"),
            ("search:export", "Search Export", "Export search results", "search", "export"),
            
            # Graph service permissions
            ("graph:read", "Graph Read", "View graph data", "graph", "read"),
            ("graph:write", "Graph Write", "Modify graph data", "graph", "write"),
            ("graph:analysis", "Graph Analysis", "Run graph analytics", "graph", "analysis"),
            ("graph:export", "Graph Export", "Export graph data", "graph", "export"),
            
            # NLP service permissions
            ("nlp:read", "NLP Read", "Use NLP analysis", "nlp", "read"),
            ("nlp:write", "NLP Write", "Create NLP models", "nlp", "write"),
            ("nlp:analysis", "NLP Analysis", "Run NLP analysis", "nlp", "analysis"),
            
            # Verification service permissions
            ("verification:read", "Verification Read", "View verification results", "verification", "read"),
            ("verification:write", "Verification Write", "Create verification checks", "verification", "write"),
            ("verification:analysis", "Verification Analysis", "Run verification analysis", "verification", "analysis"),
            
            # Security service permissions
            ("security:read", "Security Read", "View security data", "security", "read"),
            ("security:write", "Security Write", "Modify security settings", "security", "write"),
            ("security:analysis", "Security Analysis", "Run security analysis", "security", "analysis"),
            
            # Admin permissions
            ("admin:users", "User Management", "Manage users and roles", "admin", "users"),
            ("admin:system", "System Management", "Manage system settings", "admin", "system"),
            ("admin:audit", "Audit Access", "View audit logs", "admin", "audit"),
            
            # Agent permissions
            ("agent:read", "Agent Read", "View agent interactions", "agent", "read"),
            ("agent:write", "Agent Write", "Create agent workflows", "agent", "write"),
            ("agent:execute", "Agent Execute", "Execute agent workflows", "agent", "execute"),
        ]
        
        for perm_name, display_name, description, service, action in default_permissions:
            existing_perm = db.query(Permission).filter(Permission.name == perm_name).first()
            if not existing_perm:
                permission = Permission(
                    name=perm_name,
                    display_name=display_name,
                    description=description,
                    service=service,
                    action=action
                )
                db.add(permission)
        
        db.commit()
        
        # Assign permissions to roles
        role_permissions_mapping = {
            "admin": [p[0] for p in default_permissions],  # All permissions
            "security_analyst": [
                "search:read", "search:write", "search:export",
                "graph:read", "graph:write", "graph:analysis", "graph:export",
                "verification:read", "verification:write", "verification:analysis",
                "security:read", "security:write", "security:analysis",
                "admin:audit"
            ],
            "intelligence_analyst": [
                "search:read", "search:write", "search:export",
                "graph:read", "graph:write", "graph:analysis", "graph:export",
                "nlp:read", "nlp:analysis",
                "verification:read", "verification:analysis",
                "agent:read", "agent:write", "agent:execute"
            ],
            "analyst": [
                "search:read", "search:export",
                "graph:read", "graph:analysis",
                "nlp:read", "nlp:analysis",
                "verification:read",
                "agent:read"
            ],
            "viewer": [
                "search:read",
                "graph:read",
                "nlp:read",
                "verification:read"
            ]
        }
        
        for role_name, permission_names in role_permissions_mapping.items():
            role = db.query(Role).filter(Role.name == role_name).first()
            if role and not role.permissions:  # Only assign if not already assigned
                for perm_name in permission_names:
                    permission = db.query(Permission).filter(Permission.name == perm_name).first()
                    if permission:
                        role.permissions.append(permission)
        
        db.commit()
        
    finally:
        db.close()


# Event listeners for database monitoring
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Set SQLite pragmas for better performance (if using SQLite)."""
    if "sqlite" in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
