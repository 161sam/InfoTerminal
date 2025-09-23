"""User management API endpoints."""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from ..models.database import get_db
from ..models import User, Role, UserSession, ApiKey, AuditLog
from ..core.user_service import UserService
from ..core.auth import SecurityUtils
from .auth import get_current_user
from .schemas import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserListResponse,
    SessionResponse,
    SessionListResponse,
    ApiKeyCreate,
    ApiKeyResponse,
    ApiKeyCreateResponse,
    AuditLogResponse,
    AuditLogListResponse,
    UserStatsResponse,
    SuccessResponse,
    ErrorResponse
)

router = APIRouter(prefix="/users", tags=["user-management"])


def require_permission(permission: str):
    """Dependency to check if user has specific permission."""
    def check_permission(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_permissions = current_user.get("permissions", [])
        if permission not in user_permissions and "admin:users" not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission required: {permission}"
            )
        return current_user
    return check_permission


def require_admin():
    """Dependency to check if user is admin."""
    def check_admin(current_user: Dict[str, Any] = Depends(get_current_user)):
        user_roles = current_user.get("roles", [])
        if "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user
    return check_admin


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    is_verified: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_permission("admin:users"))
):
    """Get paginated list of users with filtering."""
    
    try:
        query = db.query(User)
        
        # Apply filters
        if search:
            search_filter = or_(
                User.email.ilike(f"%{search}%"),
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        if role:
            query = query.join(User.roles).filter(Role.name == role)
        
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        if is_verified is not None:
            query = query.filter(User.is_verified == is_verified)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * size
        users = query.offset(offset).limit(size).all()
        
        # Convert to response format
        user_responses = []
        for user in users:
            user_response = UserResponse.from_orm(user)
            user_response.roles = [role.name for role in user.roles]
            user_response.permissions = user.permissions
            user_responses.append(user_response)
        
        return UserListResponse(
            users=user_responses,
            total=total,
            page=page,
            size=size,
            has_next=offset + size < total,
            has_prev=page > 1
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users"
        )


@router.post("/", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_permission("admin:users"))
):
    """Create a new user account."""
    
    try:
        user_service = UserService(db)
        
        user, creation_info = await user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            username=user_data.username,
            roles=user_data.roles,
            is_verified=user_data.is_verified,
            oauth_provider=user_data.oauth_provider,
            oauth_id=user_data.oauth_id
        )
        
        # Log creation by admin
        await user_service._log_audit_event(
            user_id=str(user.id),
            event_type="user_created_by_admin",
            action="create_user",
            result="success",
            details={
                "created_by": current_user.get("sub"),
                "roles": user_data.roles or []
            }
        )
        
        user_response = UserResponse.from_orm(user)
        user_response.roles = [role.name for role in user.roles]
        user_response.permissions = user.permissions
        
        return user_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user by ID."""
    
    try:
        # Users can view their own profile, admins can view any profile
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        user_service = UserService(db)
        user = await user_service.get_user_by_id(str(user_id))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_response = UserResponse.from_orm(user)
        user_response.roles = [role.name for role in user.roles]
        user_response.permissions = user.permissions
        
        return user_response
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Update user information."""
    
    try:
        # Users can update their own profile, admins can update any profile
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        user_service = UserService(db)
        
        # Convert Pydantic model to dict, excluding None values
        updates = user_data.dict(exclude_none=True)
        
        user = await user_service.update_user(
            user_id=str(user_id),
            updates=updates,
            updated_by=current_user.get("sub")
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_response = UserResponse.from_orm(user)
        user_response.roles = [role.name for role in user.roles]
        user_response.permissions = user.permissions
        
        return user_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )


@router.delete("/{user_id}", response_model=SuccessResponse)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Delete user account (admin only)."""
    
    try:
        # Prevent self-deletion
        if str(user_id) == current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Log deletion before removing user
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=str(user.id),
            event_type="user_deleted",
            action="delete_user",
            result="success",
            details={
                "deleted_by": current_user.get("sub"),
                "user_email": user.email
            }
        )
        
        # Soft delete by deactivating instead of hard delete
        user.is_active = False
        user.email = f"deleted_{user.id}@deleted.local"  # Prevent email conflicts
        user.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        
        return SuccessResponse(message="User deleted successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )


@router.post("/{user_id}/activate", response_model=SuccessResponse)
async def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Activate user account (admin only)."""
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already active"
            )
        
        user.is_active = True
        user.updated_at = datetime.now(timezone.utc)
        db.commit()
        
        # Log activation
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=str(user.id),
            event_type="user_activated",
            action="activate_user",
            result="success",
            details={"activated_by": current_user.get("sub")}
        )
        
        return SuccessResponse(message="User activated successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user"
        )


@router.post("/{user_id}/deactivate", response_model=SuccessResponse)
async def deactivate_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Deactivate user account (admin only)."""
    
    try:
        # Prevent self-deactivation
        if str(user_id) == current_user.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account"
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already inactive"
            )
        
        user.is_active = False
        user.updated_at = datetime.now(timezone.utc)
        
        # Deactivate all user sessions
        db.query(UserSession).filter(
            and_(UserSession.user_id == user_id, UserSession.is_active == True)
        ).update({"is_active": False})
        
        db.commit()
        
        # Log deactivation
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=str(user.id),
            event_type="user_deactivated",
            action="deactivate_user",
            result="success",
            details={"deactivated_by": current_user.get("sub")}
        )
        
        return SuccessResponse(message="User deactivated successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate user"
        )


@router.post("/{user_id}/assign-roles", response_model=SuccessResponse)
async def assign_roles(
    user_id: UUID,
    role_names: List[str],
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Assign roles to user (admin only)."""
    
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get roles
        roles = db.query(Role).filter(Role.name.in_(role_names)).all()
        if len(roles) != len(role_names):
            found_roles = [role.name for role in roles]
            missing_roles = set(role_names) - set(found_roles)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Roles not found: {list(missing_roles)}"
            )
        
        # Clear existing roles and assign new ones
        user.roles.clear()
        user.roles.extend(roles)
        user.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        
        # Log role assignment
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=str(user.id),
            event_type="roles_assigned",
            action="assign_roles",
            result="success",
            details={
                "assigned_by": current_user.get("sub"),
                "roles": role_names
            }
        )
        
        return SuccessResponse(message="Roles assigned successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign roles"
        )


@router.get("/{user_id}/sessions", response_model=SessionListResponse)
async def get_user_sessions(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's active sessions."""
    
    try:
        # Users can view their own sessions, admins can view any user's sessions
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        sessions = db.query(UserSession).filter(
            and_(
                UserSession.user_id == user_id,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        ).order_by(UserSession.last_activity.desc()).all()
        
        session_responses = [SessionResponse.from_orm(session) for session in sessions]
        
        return SessionListResponse(
            sessions=session_responses,
            total=len(session_responses)
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve sessions"
        )


@router.delete("/{user_id}/sessions/{session_id}", response_model=SuccessResponse)
async def revoke_session(
    user_id: UUID,
    session_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke a specific user session."""
    
    try:
        # Users can revoke their own sessions, admins can revoke any session
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        session = db.query(UserSession).filter(
            and_(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.is_active == True
            )
        ).first()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        session.is_active = False
        db.commit()
        
        return SuccessResponse(message="Session revoked successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke session"
        )


@router.get("/{user_id}/api-keys", response_model=List[ApiKeyResponse])
async def get_user_api_keys(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get user's API keys."""
    
    try:
        # Users can view their own API keys, admins can view any user's API keys
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        api_keys = db.query(ApiKey).filter(ApiKey.user_id == user_id).all()
        
        return [ApiKeyResponse.from_orm(key) for key in api_keys]
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve API keys"
        )


@router.post("/{user_id}/api-keys", response_model=ApiKeyCreateResponse)
async def create_api_key(
    user_id: UUID,
    key_data: ApiKeyCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Create API key for user."""
    
    try:
        # Users can create their own API keys, admins can create for any user
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate API key
        api_key, key_prefix = SecurityUtils.generate_api_key()
        key_hash = SecurityUtils.hash_api_key(api_key)
        
        # Calculate expiration
        expires_at = None
        if key_data.expires_in_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=key_data.expires_in_days)
        
        # Create API key record
        api_key_record = ApiKey(
            user_id=user_id,
            name=key_data.name,
            key_hash=key_hash,
            key_prefix=key_prefix,
            permissions=key_data.permissions or [],
            allowed_ips=key_data.allowed_ips or [],
            rate_limit=key_data.rate_limit,
            expires_at=expires_at
        )
        
        db.add(api_key_record)
        db.commit()
        db.refresh(api_key_record)
        
        return ApiKeyCreateResponse(
            key=api_key,
            api_key=ApiKeyResponse.from_orm(api_key_record)
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create API key"
        )


@router.delete("/{user_id}/api-keys/{key_id}", response_model=SuccessResponse)
async def revoke_api_key(
    user_id: UUID,
    key_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Revoke API key."""
    
    try:
        # Users can revoke their own API keys, admins can revoke any API key
        user_roles = current_user.get("roles", [])
        if str(user_id) != current_user.get("sub") and "admin" not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        api_key = db.query(ApiKey).filter(
            and_(ApiKey.id == key_id, ApiKey.user_id == user_id)
        ).first()
        
        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="API key not found"
            )
        
        api_key.is_active = False
        db.commit()
        
        return SuccessResponse(message="API key revoked successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to revoke API key"
        )


@router.get("/stats", response_model=UserStatsResponse)
async def get_user_statistics(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Get user statistics (admin only)."""
    
    try:
        # Calculate statistics
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        total_users = db.query(User).count()
        active_users = db.query(User).filter(User.is_active == True).count()
        verified_users = db.query(User).filter(User.is_verified == True).count()
        mfa_enabled_users = db.query(User).filter(User.mfa_enabled == True).count()
        oauth_users = db.query(User).filter(User.oauth_provider.isnot(None)).count()
        new_users_last_30_days = db.query(User).filter(User.created_at >= thirty_days_ago).count()
        
        # Role distribution
        role_distribution = {}
        role_counts = db.query(
            Role.name, func.count(User.id)
        ).join(User.roles).group_by(Role.name).all()
        
        for role_name, count in role_counts:
            role_distribution[role_name] = count
        
        return UserStatsResponse(
            total_users=total_users,
            active_users=active_users,
            verified_users=verified_users,
            mfa_enabled_users=mfa_enabled_users,
            oauth_users=oauth_users,
            new_users_last_30_days=new_users_last_30_days,
            role_distribution=role_distribution
        )
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )


@router.get("/{user_id}/audit", response_model=AuditLogListResponse)
async def get_user_audit_logs(
    user_id: UUID,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    event_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Get user audit logs (admin only)."""
    
    try:
        query = db.query(AuditLog).filter(AuditLog.user_id == user_id)
        
        if event_type:
            query = query.filter(AuditLog.event_type == event_type)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        offset = (page - 1) * size
        logs = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(size).all()
        
        log_responses = [AuditLogResponse.from_orm(log) for log in logs]
        
        return AuditLogListResponse(
            logs=log_responses,
            total=total,
            page=page,
            size=size,
            has_next=offset + size < total,
            has_prev=page > 1
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve audit logs"
        )
