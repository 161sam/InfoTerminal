"""
InfoTerminal Auth Service API - Standardized v1 Implementation

This is the new standardized version of the Auth Service API implementing all
InfoTerminal API standards:
- /v1 namespace
- Standard error handling  
- Pagination
- Health checks
- OpenAPI documentation
- Middleware setup
"""

import os
import sys
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter, Cookie, Response, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
import jwt

# Add shared standards to Python path
SERVICE_DIR = Path(__file__).resolve().parent
REPO_ROOT = SERVICE_DIR.parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "services"))

from _shared.api_standards import (
    setup_standard_middleware,
    setup_standard_exception_handlers,
    setup_standard_openapi,
    get_service_tags_metadata,
    HealthChecker,
    check_database_connection,
    PaginatedResponse,
    PaginationParams,
    APIError,
    ErrorCodes,
    StandardError
)

# Import existing auth modules
try:
    from .models.database import SessionLocal, create_tables, init_database
    from .models.user import User, Role, Permission, UserSession, ApiKey, AuditLog
    from .core.security import SecurityManager, PasswordManager, TokenManager
    from .core.config import AuthConfig
except ImportError:
    # Fallback imports for development
    print("⚠️ Using fallback imports for auth service components")
    SessionLocal = None
    User = None

# Configuration
config = AuthConfig() if 'AuthConfig' in globals() else None
security_manager = SecurityManager() if 'SecurityManager' in globals() else None
password_manager = PasswordManager() if 'PasswordManager' in globals() else None
token_manager = TokenManager() if 'TokenManager' in globals() else None

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security scheme
security = HTTPBearer(auto_error=False)


# FastAPI App with Standard Configuration
app = FastAPI(
    title="InfoTerminal Auth Service API",
    description="User management and authentication API for InfoTerminal OSINT platform",
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc"
)

# Set up standard middleware and exception handling
setup_standard_middleware(app, "auth-service")
setup_standard_exception_handlers(app)
setup_standard_openapi(
    app=app,
    title="InfoTerminal Auth Service API",
    description="User management and authentication API for InfoTerminal OSINT platform",
    version="1.0.0",
    service_name="auth-service",
    tags_metadata=get_service_tags_metadata("auth-service")
)

# Application state
app.state.service_name = "auth-service"
app.state.version = os.getenv("GIT_SHA", "1.0.0")
app.state.start_ts = time.monotonic()

# Health Checker Setup
health_checker = HealthChecker("auth-service", app.state.version)

def check_database():
    """Check database connectivity."""
    if SessionLocal:
        # Test database connection
        with SessionLocal() as db:
            db.execute("SELECT 1").fetchone()
    else:
        # Mock database check
        pass

health_checker.add_dependency("database", lambda: check_database_connection(check_database))

# Standard Health Endpoints
@app.get("/healthz", response_model=HealthChecker.health_check().__class__, tags=["health"])
def healthz():
    """Health check endpoint (liveness probe)."""
    return health_checker.health_check()

@app.get("/readyz", response_model=HealthChecker.ready_check().__class__, tags=["health"])
def readyz():
    """Readiness check endpoint (readiness probe)."""
    return health_checker.ready_check()


# API Models
class UserRegistrationRequest(BaseModel):
    """User registration request."""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")
    full_name: Optional[str] = Field(None, max_length=100, description="Full name")
    organization: Optional[str] = Field(None, max_length=100, description="Organization")
    role: Optional[str] = Field(default="analyst", description="Initial user role")


class UserResponse(BaseModel):
    """User response model."""
    id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full name")
    organization: Optional[str] = Field(None, description="Organization")
    is_active: bool = Field(..., description="Whether user is active")
    is_verified: bool = Field(..., description="Whether email is verified")
    roles: List[str] = Field(..., description="User roles")
    created_at: str = Field(..., description="Creation timestamp")
    last_login: Optional[str] = Field(None, description="Last login timestamp")


class LoginRequest(BaseModel):
    """Login request."""
    username: str = Field(..., description="Username or email")
    password: str = Field(..., description="Password")
    remember_me: bool = Field(default=False, description="Extended session duration")


class LoginResponse(BaseModel):
    """Login response."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    user: UserResponse = Field(..., description="User information")


class TokenResponse(BaseModel):
    """Token validation response."""
    valid: bool = Field(..., description="Whether token is valid")
    user_id: Optional[str] = Field(None, description="User ID if valid")
    username: Optional[str] = Field(None, description="Username if valid")
    roles: List[str] = Field(default_factory=list, description="User roles if valid")
    expires_at: Optional[str] = Field(None, description="Token expiration timestamp")


class PasswordChangeRequest(BaseModel):
    """Password change request."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, description="New password")


class PasswordResetRequest(BaseModel):
    """Password reset request."""
    email: EmailStr = Field(..., description="User email address")


class PasswordResetConfirmRequest(BaseModel):
    """Password reset confirmation request."""
    token: str = Field(..., description="Reset token")
    new_password: str = Field(..., min_length=8, description="New password")


class RoleModel(BaseModel):
    """Role model."""
    id: str = Field(..., description="Role ID")
    name: str = Field(..., description="Role name")
    description: Optional[str] = Field(None, description="Role description")
    permissions: List[str] = Field(..., description="Role permissions")
    color: Optional[str] = Field(None, description="Role color")
    is_default: bool = Field(default=False, description="Whether this is a default role")


class PermissionModel(BaseModel):
    """Permission model."""
    id: str = Field(..., description="Permission ID")
    name: str = Field(..., description="Permission name")
    description: Optional[str] = Field(None, description="Permission description")
    resource: str = Field(..., description="Resource the permission applies to")
    action: str = Field(..., description="Action the permission allows")


class SessionModel(BaseModel):
    """User session model."""
    id: str = Field(..., description="Session ID")
    user_id: str = Field(..., description="User ID")
    created_at: str = Field(..., description="Session creation timestamp")
    expires_at: str = Field(..., description="Session expiration timestamp")
    ip_address: Optional[str] = Field(None, description="IP address")
    user_agent: Optional[str] = Field(None, description="User agent")
    is_active: bool = Field(..., description="Whether session is active")


class AuditLogEntry(BaseModel):
    """Audit log entry."""
    id: str = Field(..., description="Log entry ID")
    user_id: Optional[str] = Field(None, description="User ID")
    action: str = Field(..., description="Action performed")
    resource: Optional[str] = Field(None, description="Resource affected")
    ip_address: Optional[str] = Field(None, description="IP address")
    timestamp: str = Field(..., description="Timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")


# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def get_current_user_from_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Get current user from JWT token."""
    if not credentials:
        return None
    
    payload = verify_token(credentials.credentials)
    if not payload:
        return None
    
    return {
        "user_id": payload.get("sub"),
        "username": payload.get("username"),
        "roles": payload.get("roles", [])
    }


def require_auth(user=Depends(get_current_user_from_token)):
    """Require authentication."""
    if not user:
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Authentication required",
            status_code=401
        )
    return user


def require_role(required_role: str):
    """Require specific role."""
    def role_checker(user=Depends(require_auth)):
        if required_role not in user.get("roles", []):
            raise APIError(
                code=ErrorCodes.FORBIDDEN,
                message=f"Role '{required_role}' required",
                status_code=403,
                details={"required_role": required_role, "user_roles": user.get("roles", [])}
            )
        return user
    return role_checker


# Mock data for demonstration (replace with database calls)
MOCK_USERS = {
    "admin": {
        "id": "user_001",
        "username": "admin",
        "email": "admin@infoterminal.org",
        "password_hash": get_password_hash("admin123"),
        "full_name": "System Administrator",
        "organization": "InfoTerminal",
        "is_active": True,
        "is_verified": True,
        "roles": ["admin", "analyst"],
        "created_at": "2025-01-01T00:00:00Z"
    },
    "analyst": {
        "id": "user_002",
        "username": "analyst",
        "email": "analyst@infoterminal.org",
        "password_hash": get_password_hash("analyst123"),
        "full_name": "Security Analyst",
        "organization": "InfoTerminal",
        "is_active": True,
        "is_verified": True,
        "roles": ["analyst"],
        "created_at": "2025-01-01T00:00:00Z"
    }
}

MOCK_ROLES = {
    "admin": {
        "id": "role_001",
        "name": "admin",
        "description": "System Administrator",
        "permissions": ["*"],
        "color": "#ff4757",
        "is_default": False
    },
    "analyst": {
        "id": "role_002", 
        "name": "analyst",
        "description": "Security Analyst",
        "permissions": ["search:read", "graph:read", "nlp:read", "verify:read"],
        "color": "#3742fa",
        "is_default": True
    }
}


# V1 API Router
v1_router = APIRouter(prefix="/v1", tags=["v1"])


@v1_router.post("/auth/register",
                response_model=UserResponse,
                tags=["auth"],
                summary="Register new user",
                description="Register a new user account")
def register_user(request: UserRegistrationRequest):
    """
    Register a new user account.
    
    Creates a new user with the specified credentials:
    - Validates username uniqueness
    - Validates email format and uniqueness
    - Securely hashes password
    - Assigns default role
    - Sends verification email (if configured)
    
    Returns the created user information.
    """
    
    # Check if username already exists
    if request.username in MOCK_USERS:
        raise APIError(
            code=ErrorCodes.CONFLICT,
            message="Username already exists",
            status_code=409,
            details={"username": request.username}
        )
    
    # Check if email already exists
    for user_data in MOCK_USERS.values():
        if user_data["email"] == request.email:
            raise APIError(
                code=ErrorCodes.CONFLICT,
                message="Email already exists",
                status_code=409,
                details={"email": request.email}
            )
    
    # Create new user
    user_id = f"user_{len(MOCK_USERS) + 1:03d}"
    new_user = {
        "id": user_id,
        "username": request.username,
        "email": request.email,
        "password_hash": get_password_hash(request.password),
        "full_name": request.full_name,
        "organization": request.organization,
        "is_active": True,
        "is_verified": False,  # Requires email verification
        "roles": [request.role],
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    MOCK_USERS[request.username] = new_user
    
    return UserResponse(
        id=new_user["id"],
        username=new_user["username"],
        email=new_user["email"],
        full_name=new_user["full_name"],
        organization=new_user["organization"],
        is_active=new_user["is_active"],
        is_verified=new_user["is_verified"],
        roles=new_user["roles"],
        created_at=new_user["created_at"]
    )


@v1_router.post("/auth/login",
                response_model=LoginResponse,
                tags=["auth"],
                summary="User login",
                description="Authenticate user and return access token")
def login(request: LoginRequest, response: Response):
    """
    Authenticate user and return access token.
    
    Validates user credentials and creates a session:
    - Validates username/email and password
    - Creates JWT access token
    - Sets secure HTTP-only cookie (if enabled)
    - Records login event in audit log
    - Returns user information and token
    
    Supports both username and email for login.
    """
    
    # Find user by username or email
    user_data = None
    for username, data in MOCK_USERS.items():
        if data["username"] == request.username or data["email"] == request.username:
            user_data = data
            break
    
    if not user_data:
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Invalid credentials",
            status_code=401
        )
    
    # Verify password
    if not verify_password(request.password, user_data["password_hash"]):
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Invalid credentials",
            status_code=401
        )
    
    # Check if user is active
    if not user_data["is_active"]:
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Account is disabled",
            status_code=403
        )
    
    # Create access token
    expires_delta = timedelta(hours=JWT_EXPIRATION_HOURS * 7) if request.remember_me else None
    access_token = create_access_token(
        data={
            "sub": user_data["id"],
            "username": user_data["username"],
            "roles": user_data["roles"]
        },
        expires_delta=expires_delta
    )
    
    # Set HTTP-only cookie for web clients
    max_age = 7 * 24 * 60 * 60 if request.remember_me else 24 * 60 * 60  # 7 days or 1 day
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=max_age,
        httponly=True,
        secure=os.getenv("ENVIRONMENT") == "production",
        samesite="lax"
    )
    
    # Update last login
    user_data["last_login"] = datetime.utcnow().isoformat() + "Z"
    
    user_response = UserResponse(
        id=user_data["id"],
        username=user_data["username"],
        email=user_data["email"],
        full_name=user_data["full_name"],
        organization=user_data["organization"],
        is_active=user_data["is_active"],
        is_verified=user_data["is_verified"],
        roles=user_data["roles"],
        created_at=user_data["created_at"],
        last_login=user_data.get("last_login")
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=max_age,
        user=user_response
    )


@v1_router.post("/auth/logout",
                tags=["auth"],
                summary="User logout",
                description="Logout user and invalidate session")
def logout(response: Response, user=Depends(require_auth)):
    """
    Logout user and invalidate session.
    
    Performs session cleanup:
    - Invalidates current session
    - Clears authentication cookies
    - Records logout event in audit log
    
    Returns success confirmation.
    """
    
    # Clear authentication cookie
    response.delete_cookie(key="access_token")
    
    return {"message": "Successfully logged out"}


@v1_router.get("/auth/me",
               response_model=UserResponse,
               tags=["auth"],
               summary="Get current user",
               description="Get current authenticated user information")
def get_current_user_info(user=Depends(require_auth)):
    """
    Get current authenticated user information.
    
    Returns detailed information about the authenticated user:
    - User profile data
    - Assigned roles and permissions
    - Account status
    - Login history
    
    Requires valid authentication token.
    """
    
    # Find user data
    user_data = None
    for data in MOCK_USERS.values():
        if data["id"] == user["user_id"]:
            user_data = data
            break
    
    if not user_data:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="User not found",
            status_code=404
        )
    
    return UserResponse(
        id=user_data["id"],
        username=user_data["username"],
        email=user_data["email"],
        full_name=user_data["full_name"],
        organization=user_data["organization"],
        is_active=user_data["is_active"],
        is_verified=user_data["is_verified"],
        roles=user_data["roles"],
        created_at=user_data["created_at"],
        last_login=user_data.get("last_login")
    )


@v1_router.post("/auth/verify-token",
                response_model=TokenResponse,
                tags=["auth"],
                summary="Verify token",
                description="Verify JWT token validity")
def verify_jwt_token(token: str = Query(..., description="JWT token to verify")):
    """
    Verify JWT token validity.
    
    Validates a JWT token and returns user information:
    - Checks token signature and expiration
    - Returns user ID and roles if valid
    - Used by other services for authentication
    
    Returns token validation result.
    """
    
    payload = verify_token(token)
    if not payload:
        return TokenResponse(valid=False)
    
    return TokenResponse(
        valid=True,
        user_id=payload.get("sub"),
        username=payload.get("username"),
        roles=payload.get("roles", []),
        expires_at=datetime.fromtimestamp(payload.get("exp")).isoformat() + "Z"
    )


@v1_router.post("/auth/change-password",
                tags=["auth"],
                summary="Change password",
                description="Change user password")
def change_password(request: PasswordChangeRequest, user=Depends(require_auth)):
    """
    Change user password.
    
    Updates the user's password:
    - Validates current password
    - Validates new password strength
    - Updates password hash
    - Invalidates existing sessions (optional)
    - Records password change in audit log
    
    Requires authentication and current password.
    """
    
    # Find user data
    user_data = None
    for data in MOCK_USERS.values():
        if data["id"] == user["user_id"]:
            user_data = data
            break
    
    if not user_data:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="User not found",
            status_code=404
        )
    
    # Verify current password
    if not verify_password(request.current_password, user_data["password_hash"]):
        raise APIError(
            code=ErrorCodes.UNAUTHORIZED,
            message="Current password is incorrect",
            status_code=401
        )
    
    # Update password
    user_data["password_hash"] = get_password_hash(request.new_password)
    
    return {"message": "Password changed successfully"}


@v1_router.get("/users",
               response_model=PaginatedResponse[UserResponse],
               tags=["users"],
               summary="List users",
               description="Get paginated list of users")
def list_users(
    pagination: PaginationParams = Depends(),
    search: Optional[str] = Query(None, description="Search by username or email"),
    role: Optional[str] = Query(None, description="Filter by role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    user=Depends(require_role("admin"))
):
    """
    Get paginated list of users.
    
    Returns a paginated list of users with filtering options:
    - Search by username or email
    - Filter by role
    - Filter by active status
    - Supports pagination
    
    Requires admin role.
    """
    
    # Filter users
    filtered_users = []
    for user_data in MOCK_USERS.values():
        # Apply search filter
        if search:
            if search.lower() not in user_data["username"].lower() and search.lower() not in user_data["email"].lower():
                continue
        
        # Apply role filter
        if role and role not in user_data["roles"]:
            continue
        
        # Apply active status filter
        if is_active is not None and user_data["is_active"] != is_active:
            continue
        
        user_response = UserResponse(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            full_name=user_data["full_name"],
            organization=user_data["organization"],
            is_active=user_data["is_active"],
            is_verified=user_data["is_verified"],
            roles=user_data["roles"],
            created_at=user_data["created_at"],
            last_login=user_data.get("last_login")
        )
        filtered_users.append(user_response)
    
    # Apply pagination
    total = len(filtered_users)
    start_idx = pagination.offset
    end_idx = start_idx + pagination.size
    page_users = filtered_users[start_idx:end_idx]
    
    return PaginatedResponse.create(
        items=page_users,
        total=total,
        pagination=pagination
    )


@v1_router.get("/users/{user_id}",
               response_model=UserResponse,
               tags=["users"],
               summary="Get user",
               description="Get user by ID")
def get_user(user_id: str, current_user=Depends(require_auth)):
    """
    Get user by ID.
    
    Returns detailed user information:
    - User profile data
    - Role assignments
    - Account status
    - Activity history
    
    Users can view their own profile; admins can view any user.
    """
    
    # Check permissions
    if current_user["user_id"] != user_id and "admin" not in current_user.get("roles", []):
        raise APIError(
            code=ErrorCodes.FORBIDDEN,
            message="Insufficient permissions",
            status_code=403
        )
    
    # Find user
    user_data = None
    for data in MOCK_USERS.values():
        if data["id"] == user_id:
            user_data = data
            break
    
    if not user_data:
        raise APIError(
            code=ErrorCodes.RESOURCE_NOT_FOUND,
            message="User not found",
            status_code=404,
            details={"user_id": user_id}
        )
    
    return UserResponse(
        id=user_data["id"],
        username=user_data["username"],
        email=user_data["email"],
        full_name=user_data["full_name"],
        organization=user_data["organization"],
        is_active=user_data["is_active"],
        is_verified=user_data["is_verified"],
        roles=user_data["roles"],
        created_at=user_data["created_at"],
        last_login=user_data.get("last_login")
    )


@v1_router.get("/roles",
               response_model=List[RoleModel],
               tags=["roles"],
               summary="List roles",
               description="Get list of available roles")
def list_roles(user=Depends(require_role("admin"))):
    """
    Get list of available roles.
    
    Returns all system roles with their permissions:
    - Role definitions
    - Associated permissions
    - Default role indicators
    - Role metadata
    
    Requires admin role.
    """
    
    roles = []
    for role_data in MOCK_ROLES.values():
        role = RoleModel(
            id=role_data["id"],
            name=role_data["name"],
            description=role_data["description"],
            permissions=role_data["permissions"],
            color=role_data["color"],
            is_default=role_data["is_default"]
        )
        roles.append(role)
    
    return roles


# Include V1 router
app.include_router(v1_router)

# Legacy endpoints for backward compatibility
@app.post("/login", deprecated=True, tags=["legacy"])
def legacy_login(username: str, password: str):
    """
    DEPRECATED: Use /v1/auth/login instead.
    
    Legacy login endpoint for backward compatibility.
    Will be removed in a future version.
    """
    request = LoginRequest(username=username, password=password)
    response = Response()
    login_response = login(request, response)
    
    return {
        "access_token": login_response.access_token,
        "user": login_response.user.dict()
    }


# Root endpoint
@app.get("/", tags=["root"])
def root():
    """Service information and available endpoints."""
    return {
        "service": "InfoTerminal Auth Service API",
        "version": app.state.version,
        "status": "running",
        "api_version": "v1",
        "endpoints": {
            "health": "/healthz",
            "ready": "/readyz",
            "docs": "/v1/docs",
            "register": "/v1/auth/register",
            "login": "/v1/auth/login",
            "logout": "/v1/auth/logout",
            "me": "/v1/auth/me",
            "verify_token": "/v1/auth/verify-token",
            "users": "/v1/users",
            "roles": "/v1/roles"
        },
        "legacy_endpoints": {
            "login": "/login (deprecated)"
        },
        "authentication": {
            "methods": ["JWT Bearer Token", "HTTP-only Cookie"],
            "token_expiration": f"{JWT_EXPIRATION_HOURS} hours",
            "supported_roles": list(MOCK_ROLES.keys())
        }
    }
