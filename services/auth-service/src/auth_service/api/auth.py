"""Authentication API endpoints."""

from datetime import datetime, timezone
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..core.user_service import UserService
from ..core.auth import TokenManager
from .schemas import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    PasswordChangeRequest,
    PasswordResetRequest,
    MFASetupResponse,
    MFAEnableRequest,
    MFADisableRequest,
    UserResponse,
    SuccessResponse,
    ErrorResponse
)

router = APIRouter(prefix="/auth", tags=["authentication"])


# Dependency to get current user from JWT token
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get current user from JWT token."""
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token = auth_header.split(" ")[1]
    payload = TokenManager.verify_token(token, "access")
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Verify user still exists and is active
    user_service = UserService(db)
    user = await user_service.get_user_by_id(payload.get("sub"))
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return payload



def get_client_info(request: Request) -> Dict[str, Any]:
    """Extract client information from request."""
    return {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "device_type": _detect_device_type(request.headers.get("user-agent", ""))
    }


def _detect_device_type(user_agent: str) -> str:
    """Detect device type from user agent."""
    user_agent_lower = user_agent.lower()
    if any(mobile in user_agent_lower for mobile in ['mobile', 'android', 'iphone']):
        return "mobile"
    elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
        return "tablet"
    else:
        return "desktop"


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Authenticate user and return access tokens."""
    
    try:
        user_service = UserService(db)
        client_info = get_client_info(http_request)
        
        # Authenticate user
        user, auth_result = await user_service.authenticate_user(
            email=request.email,
            password=request.password,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            mfa_token=request.mfa_token
        )
        
        # Check if MFA is required
        if auth_result.get("requires_mfa"):
            return LoginResponse(
                access_token="",
                refresh_token="",
                expires_in=0,
                user=UserResponse.from_orm(user),
                requires_mfa=True
            )
        
        # Create session and tokens
        access_token, refresh_token = await user_service.create_user_session(
            user=user,
            ip_address=client_info["ip_address"],
            user_agent=client_info["user_agent"],
            device_type=client_info["device_type"],
            remember_me=request.remember_me
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800,  # 30 minutes
            user=UserResponse.from_orm(user),
            requires_mfa=False
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    
    try:
        user_service = UserService(db)
        
        result = await user_service.refresh_token(request.refresh_token)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )
        
        access_token, refresh_token = result
        
        return RefreshTokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800  # 30 minutes
        )
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Logout user by invalidating session."""
    
    try:
        # Get current user from request
        current_user = await get_current_user(http_request, db)
        
        user_service = UserService(db)
        
        session_id = current_user.get("session_id")
        user_id = current_user.get("sub")
        
        if session_id and user_id:
            await user_service.logout_user(session_id, user_id)
        
        return SuccessResponse(message="Logged out successfully")
        
    except Exception:
        # Return success even if logout fails to prevent information disclosure
        return SuccessResponse(message="Logged out successfully")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    request: Request,
    db: Session = Depends(get_db)
):
    """Get current user information."""
    
    try:
        current_user = await get_current_user(request, db)
        user_service = UserService(db)
        user_id = current_user.get("sub")
        
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/change-password", response_model=SuccessResponse)
async def change_password(
    request: PasswordChangeRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Change user password."""
    
    try:
        current_user = await get_current_user(http_request, db)
        user_service = UserService(db)
        user_id = current_user.get("sub")
        
        success = await user_service.change_password(
            user_id=user_id,
            current_password=request.current_password,
            new_password=request.new_password
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to change password"
            )
        
        return SuccessResponse(message="Password changed successfully")
        
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
            detail="Password change failed"
        )


@router.post("/request-password-reset", response_model=SuccessResponse)
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset email."""
    
    try:
        user_service = UserService(db)
        
        user = await user_service.get_user_by_email(request.email)
        if user:
            # In a real implementation, send email with reset token
            # For now, just log the event
            await user_service._log_audit_event(
                user_id=str(user.id),
                event_type="password_reset_requested",
                action="request_password_reset",
                result="success"
            )
        
        # Always return success to prevent email enumeration
        return SuccessResponse(message="If the email exists, a reset link has been sent")
        
    except Exception:
        # Always return success to prevent email enumeration
        return SuccessResponse(message="If the email exists, a reset link has been sent")


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Setup MFA for current user."""
    
    try:
        current_user = await get_current_user(http_request, db)
        user_service = UserService(db)
        user_id = current_user.get("sub")
        
        mfa_data = await user_service.setup_mfa(user_id)
        
        # Convert QR code bytes to base64 string
        import base64
        qr_code_b64 = base64.b64encode(mfa_data["qr_code"]).decode()
        
        return MFASetupResponse(
            secret=mfa_data["secret"],
            qr_code=qr_code_b64,
            backup_codes=mfa_data["backup_codes"]
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MFA setup failed"
        )


@router.post("/mfa/enable", response_model=SuccessResponse)
async def enable_mfa(
    request: MFAEnableRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Enable MFA after verifying setup token."""
    
    try:
        current_user = await get_current_user(http_request, db)
        user_service = UserService(db)
        user_id = current_user.get("sub")
        
        success = await user_service.enable_mfa(user_id, request.token)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid MFA token"
            )
        
        return SuccessResponse(message="MFA enabled successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MFA enable failed"
        )


@router.post("/mfa/disable", response_model=SuccessResponse)
async def disable_mfa(
    request: MFADisableRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """Disable MFA after password verification."""
    
    try:
        current_user = await get_current_user(http_request, db)
        user_service = UserService(db)
        user_id = current_user.get("sub")
        
        success = await user_service.disable_mfa(user_id, request.password)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password"
            )
        
        return SuccessResponse(message="MFA disabled successfully")
        
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MFA disable failed"
        )
