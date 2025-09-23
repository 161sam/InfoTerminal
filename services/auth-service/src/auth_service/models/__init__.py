"""Database models for user management and authentication."""

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import (
    Column, 
    String, 
    Boolean, 
    DateTime, 
    Text, 
    Table, 
    ForeignKey,
    Integer,
    JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.sql import func

Base = declarative_base()

# Association table for many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
    Column('assigned_at', DateTime(timezone=True), server_default=func.now()),
    Column('assigned_by', UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
)

# Association table for many-to-many relationship between roles and permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True),
    Column('assigned_at', DateTime(timezone=True), server_default=func.now())
)


class User(Base):
    """User model with comprehensive authentication and profile management."""
    
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for OAuth-only users
    
    # Profile information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # Account status and security
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    
    # MFA settings
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(32), nullable=True)  # TOTP secret
    backup_codes = Column(JSON, nullable=True)  # List of backup codes
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    
    # OAuth integration
    oauth_provider = Column(String(50), nullable=True)  # google, github, microsoft
    oauth_id = Column(String(255), nullable=True)
    
    # User preferences and metadata
    preferences = Column(JSON, nullable=True, default=dict)
    user_metadata = Column(JSON, nullable=True, default=dict)
    
    # Security tracking
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    roles: Mapped[List["Role"]] = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy="select",
        primaryjoin=lambda: User.id == user_roles.c.user_id,
        secondaryjoin=lambda: Role.id == user_roles.c.role_id,
        foreign_keys=lambda: (user_roles.c.user_id, user_roles.c.role_id)
    )
    sessions: Mapped[List["UserSession"]] = relationship(
        "UserSession", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    api_keys: Mapped[List["ApiKey"]] = relationship(
        "ApiKey", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    audit_logs: Mapped[List["AuditLog"]] = relationship(
        "AuditLog", 
        back_populates="user"
    )

    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.display_name or self.username or self.email.split('@')[0]

    @property
    def permissions(self) -> List[str]:
        """Get all permissions from user's roles."""
        perms = set()
        for role in self.roles:
            for permission in role.permissions:
                perms.add(permission.name)
        return list(perms)

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        return permission in self.permissions

    def has_role(self, role_name: str) -> bool:
        """Check if user has a specific role."""
        return any(role.name == role_name for role in self.roles)


class Role(Base):
    """Role model for role-based access control."""
    
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Role configuration
    is_default = Column(Boolean, default=False, nullable=False)
    is_system = Column(Boolean, default=False, nullable=False)  # System roles cannot be deleted
    priority = Column(Integer, default=0, nullable=False)  # Higher number = higher priority
    
    # Metadata
    color = Column(String(7), nullable=True)  # Hex color for UI
    icon = Column(String(50), nullable=True)  # Icon name for UI
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    users: Mapped[List[User]] = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        primaryjoin=lambda: Role.id == user_roles.c.role_id,
        secondaryjoin=lambda: User.id == user_roles.c.user_id,
        foreign_keys=lambda: (user_roles.c.role_id, user_roles.c.user_id)
    )
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", 
        secondary=role_permissions, 
        back_populates="roles"
    )


class Permission(Base):
    """Permission model for granular access control."""
    
    __tablename__ = 'permissions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False, index=True)  # e.g., "search:read"
    display_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    # Permission categorization
    service = Column(String(50), nullable=False, index=True)  # search, graph, nlp, etc.
    action = Column(String(50), nullable=False, index=True)   # read, write, delete, execute
    resource = Column(String(100), nullable=True)  # Optional specific resource
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    roles: Mapped[List[Role]] = relationship(
        "Role", 
        secondary=role_permissions, 
        back_populates="permissions"
    )


class UserSession(Base):
    """User session tracking for security and session management."""
    
    __tablename__ = 'user_sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Session identification
    session_token = Column(String(255), unique=True, nullable=False, index=True)
    refresh_token = Column(String(255), unique=True, nullable=True, index=True)
    device_fingerprint = Column(String(255), nullable=True)
    
    # Session metadata
    ip_address = Column(String(45), nullable=True)  # IPv6 support
    user_agent = Column(Text, nullable=True)
    location = Column(String(200), nullable=True)
    device_type = Column(String(50), nullable=True)  # desktop, mobile, tablet
    
    # Session state
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Relationships
    user: Mapped[User] = relationship("User", back_populates="sessions")


class ApiKey(Base):
    """API key management for programmatic access."""
    
    __tablename__ = 'api_keys'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Key identification
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    key_prefix = Column(String(10), nullable=False)  # First few chars for identification
    
    # Key configuration
    permissions = Column(JSON, nullable=True, default=list)  # List of specific permissions
    allowed_ips = Column(JSON, nullable=True, default=list)  # IP whitelist
    rate_limit = Column(Integer, nullable=True)  # Requests per minute
    
    # Key state
    is_active = Column(Boolean, default=True, nullable=False)
    last_used = Column(DateTime(timezone=True), nullable=True)
    usage_count = Column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user: Mapped[User] = relationship("User", back_populates="api_keys")


class AuditLog(Base):
    """Audit logging for compliance and security monitoring."""
    
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True, index=True)
    
    # Event information
    event_type = Column(String(100), nullable=False, index=True)  # login, logout, password_change
    action = Column(String(100), nullable=False)
    resource = Column(String(200), nullable=True)
    result = Column(String(50), nullable=False)  # success, failure, error
    
    # Request context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    session_id = Column(String(255), nullable=True)
    
    # Event data
    details = Column(JSON, nullable=True, default=dict)
    event_metadata = Column(JSON, nullable=True, default=dict)
    
    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    
    # Relationships
    user: Mapped[Optional[User]] = relationship("User", back_populates="audit_logs")
