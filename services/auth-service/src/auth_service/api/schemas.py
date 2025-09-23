"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


# Base schemas
class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


# User schemas
class UserCreate(BaseModel):
    """Schema for creating a new user."""
    
    email: EmailStr
    password: Optional[str] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    username: Optional[str] = Field(None, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    roles: Optional[List[str]] = None
    is_verified: bool = False
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is not None and len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    display_name: Optional[str] = Field(None, max_length=200)
    bio: Optional[str] = None
    avatar_url: Optional[str] = Field(None, max_length=500)
    preferences: Optional[Dict[str, Any]] = None
    user_metadata: Optional[Dict[str, Any]] = None


class UserResponse(BaseSchema):
    """Schema for user response."""
    
    id: UUID
    email: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    is_active: bool
    is_verified: bool
    email_verified: bool
    mfa_enabled: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    last_activity: Optional[datetime]
    oauth_provider: Optional[str]
    roles: List[str] = []
    permissions: List[str] = []
    
    @validator('roles', pre=True)
    def extract_role_names(cls, v):
        if isinstance(v, list) and v and hasattr(v[0], 'name'):
            return [role.name for role in v]
        return v or []


class UserListResponse(BaseModel):
    """Schema for paginated user list response."""
    
    users: List[UserResponse]
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool


# Authentication schemas
class LoginRequest(BaseModel):
    """Schema for login request."""
    
    email: EmailStr
    password: str
    mfa_token: Optional[str] = None
    remember_me: bool = False


class LoginResponse(BaseModel):
    """Schema for login response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
    requires_mfa: bool = False


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh request."""
    
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """Schema for token refresh response."""
    
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class PasswordChangeRequest(BaseModel):
    """Schema for password change request."""
    
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class PasswordResetRequest(BaseModel):
    """Schema for password reset request."""
    
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation."""
    
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


# MFA schemas
class MFASetupResponse(BaseModel):
    """Schema for MFA setup response."""
    
    secret: str
    qr_code: str  # Base64 encoded QR code
    backup_codes: List[str]


class MFAEnableRequest(BaseModel):
    """Schema for MFA enable request."""
    
    token: str


class MFADisableRequest(BaseModel):
    """Schema for MFA disable request."""
    
    password: str


class MFAVerifyRequest(BaseModel):
    """Schema for MFA verification request."""
    
    token: str


# Role schemas
class RoleCreate(BaseModel):
    """Schema for creating a new role."""
    
    name: str = Field(..., max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    display_name: str = Field(..., max_length=100)
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    priority: int = 0


class RoleUpdate(BaseModel):
    """Schema for updating role information."""
    
    display_name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    permissions: Optional[List[str]] = None
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    priority: Optional[int] = None


class RoleResponse(BaseSchema):
    """Schema for role response."""
    
    id: UUID
    name: str
    display_name: str
    description: Optional[str]
    is_default: bool
    is_system: bool
    priority: int
    color: Optional[str]
    icon: Optional[str]
    created_at: datetime
    updated_at: datetime
    permissions: List[str] = []
    user_count: int = 0
    
    @validator('permissions', pre=True)
    def extract_permission_names(cls, v):
        if isinstance(v, list) and v and hasattr(v[0], 'name'):
            return [perm.name for perm in v]
        return v or []


# Permission schemas
class PermissionResponse(BaseSchema):
    """Schema for permission response."""
    
    id: UUID
    name: str
    display_name: str
    description: Optional[str]
    service: str
    action: str
    resource: Optional[str]
    created_at: datetime


# Session schemas
class SessionResponse(BaseSchema):
    """Schema for user session response."""
    
    id: UUID
    device_type: Optional[str]
    ip_address: Optional[str]
    location: Optional[str]
    is_active: bool
    created_at: datetime
    last_activity: datetime
    expires_at: datetime


class SessionListResponse(BaseModel):
    """Schema for user sessions list."""
    
    sessions: List[SessionResponse]
    total: int


# API Key schemas
class ApiKeyCreate(BaseModel):
    """Schema for creating API key."""
    
    name: str = Field(..., max_length=100)
    permissions: Optional[List[str]] = None
    allowed_ips: Optional[List[str]] = None
    rate_limit: Optional[int] = Field(None, ge=1, le=10000)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


class ApiKeyResponse(BaseSchema):
    """Schema for API key response."""
    
    id: UUID
    name: str
    key_prefix: str
    permissions: List[str]
    allowed_ips: List[str]
    rate_limit: Optional[int]
    is_active: bool
    created_at: datetime
    expires_at: Optional[datetime]
    last_used: Optional[datetime]
    usage_count: int


class ApiKeyCreateResponse(BaseModel):
    """Schema for API key creation response with actual key."""
    
    key: str
    api_key: ApiKeyResponse


# Audit schemas
class AuditLogResponse(BaseSchema):
    """Schema for audit log response."""
    
    id: UUID
    user_id: Optional[UUID]
    event_type: str
    action: str
    resource: Optional[str]
    result: str
    ip_address: Optional[str]
    user_agent: Optional[str]
    details: Dict[str, Any]
    timestamp: datetime


class AuditLogListResponse(BaseModel):
    """Schema for audit logs list."""
    
    logs: List[AuditLogResponse]
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool


# Utility schemas
class SuccessResponse(BaseModel):
    """Generic success response."""
    
    success: bool = True
    message: str


class ErrorResponse(BaseModel):
    """Generic error response."""
    
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    timestamp: datetime
    version: str
    database: str
    services: Dict[str, str]


# Validation schemas
class PasswordValidationResponse(BaseModel):
    """Password validation response."""
    
    valid: bool
    score: int
    strength: str
    errors: List[str]


class EmailValidationResponse(BaseModel):
    """Email validation response."""
    
    valid: bool
    email: str
    normalized: Optional[str] = None
    error: Optional[str] = None


# Statistics schemas
class UserStatsResponse(BaseModel):
    """User statistics response."""
    
    total_users: int
    active_users: int
    verified_users: int
    mfa_enabled_users: int
    oauth_users: int
    new_users_last_30_days: int
    role_distribution: Dict[str, int]


class SystemStatsResponse(BaseModel):
    """System statistics response."""
    
    active_sessions: int
    failed_login_attempts_last_hour: int
    api_keys_total: int
    api_keys_active: int
    audit_events_last_24_hours: int
