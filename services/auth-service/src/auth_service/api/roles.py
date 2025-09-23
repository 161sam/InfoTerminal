"""Role and permission management API endpoints."""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..models.database import get_db
from ..models import Role, Permission, User
from ..core.user_service import UserService
from .auth import get_current_user
from .schemas import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionResponse,
    SuccessResponse,
    ErrorResponse
)

router = APIRouter(prefix="/roles", tags=["role-management"])


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


@router.get("/", response_model=List[RoleResponse])
async def list_roles(
    include_system: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get list of all roles."""
    
    try:
        query = db.query(Role)
        
        # Filter system roles if requested
        if not include_system:
            query = query.filter(Role.is_system == False)
        
        roles = query.order_by(Role.priority.desc(), Role.name).all()
        
        # Add user count for each role
        role_responses = []
        for role in roles:
            user_count = db.query(func.count(User.id)).join(User.roles).filter(Role.id == role.id).scalar()
            
            role_response = RoleResponse.from_orm(role)
            role_response.permissions = [perm.name for perm in role.permissions]
            role_response.user_count = user_count or 0
            role_responses.append(role_response)
        
        return role_responses
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles"
        )


@router.post("/", response_model=RoleResponse)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Create a new role (admin only)."""
    
    try:
        # Check if role already exists
        existing_role = db.query(Role).filter(Role.name == role_data.name).first()
        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists"
            )
        
        # Create role
        role = Role(
            name=role_data.name,
            display_name=role_data.display_name,
            description=role_data.description,
            color=role_data.color,
            icon=role_data.icon,
            priority=role_data.priority,
            is_system=False  # User-created roles are never system roles
        )
        
        # Assign permissions if provided
        if role_data.permissions:
            permissions = db.query(Permission).filter(Permission.name.in_(role_data.permissions)).all()
            if len(permissions) != len(role_data.permissions):
                found_permissions = [perm.name for perm in permissions]
                missing_permissions = set(role_data.permissions) - set(found_permissions)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Permissions not found: {list(missing_permissions)}"
                )
            role.permissions.extend(permissions)
        
        db.add(role)
        db.commit()
        db.refresh(role)
        
        # Log role creation
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=current_user.get("sub"),
            event_type="role_created",
            action="create_role",
            result="success",
            details={
                "role_name": role_data.name,
                "permissions": role_data.permissions or []
            }
        )
        
        role_response = RoleResponse.from_orm(role)
        role_response.permissions = [perm.name for perm in role.permissions]
        role_response.user_count = 0
        
        return role_response
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create role"
        )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get role by ID."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Get user count
        user_count = db.query(func.count(User.id)).join(User.roles).filter(Role.id == role.id).scalar()
        
        role_response = RoleResponse.from_orm(role)
        role_response.permissions = [perm.name for perm in role.permissions]
        role_response.user_count = user_count or 0
        
        return role_response
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve role"
        )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: UUID,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Update role information (admin only)."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent modification of system roles
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot modify system roles"
            )
        
        # Track changes for audit
        changes = {}
        
        # Update fields
        update_fields = ['display_name', 'description', 'color', 'icon', 'priority']
        for field in update_fields:
            new_value = getattr(role_data, field)
            if new_value is not None:
                old_value = getattr(role, field)
                if old_value != new_value:
                    setattr(role, field, new_value)
                    changes[field] = {"old": old_value, "new": new_value}
        
        # Update permissions
        if role_data.permissions is not None:
            old_permissions = [perm.name for perm in role.permissions]
            
            # Get new permissions
            permissions = db.query(Permission).filter(Permission.name.in_(role_data.permissions)).all()
            if len(permissions) != len(role_data.permissions):
                found_permissions = [perm.name for perm in permissions]
                missing_permissions = set(role_data.permissions) - set(found_permissions)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Permissions not found: {list(missing_permissions)}"
                )
            
            # Update permissions
            role.permissions.clear()
            role.permissions.extend(permissions)
            
            new_permissions = [perm.name for perm in role.permissions]
            if set(old_permissions) != set(new_permissions):
                changes["permissions"] = {"old": old_permissions, "new": new_permissions}
        
        if changes:
            role.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(role)
            
            # Log role update
            user_service = UserService(db)
            await user_service._log_audit_event(
                user_id=current_user.get("sub"),
                event_type="role_updated",
                action="update_role",
                result="success",
                details={
                    "role_name": role.name,
                    "changes": changes
                }
            )
        
        # Get user count
        user_count = db.query(func.count(User.id)).join(User.roles).filter(Role.id == role.id).scalar()
        
        role_response = RoleResponse.from_orm(role)
        role_response.permissions = [perm.name for perm in role.permissions]
        role_response.user_count = user_count or 0
        
        return role_response
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update role"
        )


@router.delete("/{role_id}", response_model=SuccessResponse)
async def delete_role(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Delete role (admin only)."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent deletion of system roles
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete system roles"
            )
        
        # Check if role is assigned to users
        user_count = db.query(func.count(User.id)).join(User.roles).filter(Role.id == role.id).scalar()
        if user_count and user_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete role: {user_count} users are assigned to this role"
            )
        
        # Log role deletion before removing
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=current_user.get("sub"),
            event_type="role_deleted",
            action="delete_role",
            result="success",
            details={
                "role_name": role.name,
                "role_id": str(role.id)
            }
        )
        
        db.delete(role)
        db.commit()
        
        return SuccessResponse(message="Role deleted successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete role"
        )


@router.get("/{role_id}/users", response_model=List[Dict[str, Any]])
async def get_role_users(
    role_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Get users assigned to a specific role (admin only)."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        users = db.query(User).join(User.roles).filter(Role.id == role_id).all()
        
        user_list = []
        for user in users:
            user_list.append({
                "id": str(user.id),
                "email": user.email,
                "name": user.full_name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            })
        
        return user_list
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve role users"
        )


# Permission endpoints
@router.get("/permissions/", response_model=List[PermissionResponse])
async def list_permissions(
    service: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get list of all permissions."""
    
    try:
        query = db.query(Permission)
        
        if service:
            query = query.filter(Permission.service == service)
        
        permissions = query.order_by(Permission.service, Permission.action, Permission.name).all()
        
        return [PermissionResponse.from_orm(perm) for perm in permissions]
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve permissions"
        )


@router.get("/permissions/services", response_model=List[str])
async def list_services(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get list of all services with permissions."""
    
    try:
        services = db.query(Permission.service).distinct().order_by(Permission.service).all()
        return [service[0] for service in services]
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve services"
        )


@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: UUID,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get permission by ID."""
    
    try:
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        return PermissionResponse.from_orm(permission)
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve permission"
        )


@router.post("/{role_id}/permissions", response_model=SuccessResponse)
async def assign_permissions(
    role_id: UUID,
    permission_names: List[str],
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Assign permissions to role (admin only)."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent modification of system roles
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot modify system role permissions"
            )
        
        # Get permissions
        permissions = db.query(Permission).filter(Permission.name.in_(permission_names)).all()
        if len(permissions) != len(permission_names):
            found_permissions = [perm.name for perm in permissions]
            missing_permissions = set(permission_names) - set(found_permissions)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permissions not found: {list(missing_permissions)}"
            )
        
        # Update permissions
        old_permissions = [perm.name for perm in role.permissions]
        role.permissions.clear()
        role.permissions.extend(permissions)
        role.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        
        # Log permission assignment
        user_service = UserService(db)
        await user_service._log_audit_event(
            user_id=current_user.get("sub"),
            event_type="permissions_assigned",
            action="assign_permissions",
            result="success",
            details={
                "role_name": role.name,
                "old_permissions": old_permissions,
                "new_permissions": permission_names
            }
        )
        
        return SuccessResponse(message="Permissions assigned successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign permissions"
        )


@router.delete("/{role_id}/permissions/{permission_name}", response_model=SuccessResponse)
async def remove_permission(
    role_id: UUID,
    permission_name: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(require_admin())
):
    """Remove permission from role (admin only)."""
    
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found"
            )
        
        # Prevent modification of system roles
        if role.is_system:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot modify system role permissions"
            )
        
        # Find and remove permission
        permission = db.query(Permission).filter(Permission.name == permission_name).first()
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permission not found"
            )
        
        if permission in role.permissions:
            role.permissions.remove(permission)
            role.updated_at = datetime.now(timezone.utc)
            db.commit()
            
            # Log permission removal
            user_service = UserService(db)
            await user_service._log_audit_event(
                user_id=current_user.get("sub"),
                event_type="permission_removed",
                action="remove_permission",
                result="success",
                details={
                    "role_name": role.name,
                    "permission": permission_name
                }
            )
            
            return SuccessResponse(message="Permission removed successfully")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission not assigned to this role"
            )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove permission"
        )
