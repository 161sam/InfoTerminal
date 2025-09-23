"""User management service layer."""

import uuid
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..models import User, Role, Permission, UserSession, ApiKey, AuditLog
from ..core.auth import (
    PasswordManager, 
    TokenManager, 
    MFAManager, 
    EmailValidator, 
    SecurityUtils,
    RateLimiter
)


class UserService:
    """Service for user management operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.rate_limiter = RateLimiter()
    
    async def create_user(
        self,
        email: str,
        password: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        roles: Optional[List[str]] = None,
        is_verified: bool = False,
        oauth_provider: Optional[str] = None,
        oauth_id: Optional[str] = None
    ) -> Tuple[User, Dict[str, Any]]:
        """Create a new user account."""
        
        # Validate email
        email_validation = EmailValidator.validate_email_format(email)
        if not email_validation["valid"]:
            raise ValueError(f"Invalid email format: {email_validation['error']}")
        
        normalized_email = email_validation["normalized"]
        
        # Check if user already exists
        existing_user = self.db.query(User).filter(
            or_(User.email == normalized_email, User.username == username)
        ).first()
        if existing_user:
            raise ValueError("User with this email or username already exists")
        
        # Validate password if provided
        password_hash = None
        if password:
            password_validation = PasswordManager.validate_password_strength(password)
            if not password_validation["valid"]:
                raise ValueError(f"Password validation failed: {password_validation['errors']}")
            password_hash = PasswordManager.hash_password(password)
        
        # Create user
        user = User(
            email=normalized_email,
            username=username,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            is_verified=is_verified,
            oauth_provider=oauth_provider,
            oauth_id=oauth_id,
            email_verified=oauth_provider is not None  # OAuth users are pre-verified
        )
        
        # Assign roles
        if roles:
            user_roles = self.db.query(Role).filter(Role.name.in_(roles)).all()
            user.roles.extend(user_roles)
        else:
            # Assign default role
            default_role = self.db.query(Role).filter(Role.is_default == True).first()
            if default_role:
                user.roles.append(default_role)
        
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        # Log user creation
        await self._log_audit_event(
            user_id=user.id,
            event_type="user_created",
            action="create_user",
            result="success",
            details={"email": normalized_email, "oauth_provider": oauth_provider}
        )
        
        return user, {"user_id": str(user.id), "email": normalized_email}
    
    async def authenticate_user(
        self,
        email: str,
        password: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        mfa_token: Optional[str] = None
    ) -> Tuple[Optional[User], Dict[str, Any]]:
        """Authenticate user with email/password and optional MFA."""
        
        identifier = f"auth:{email}:{ip_address or 'unknown'}"
        
        # Check rate limiting
        if self.rate_limiter.is_rate_limited(identifier):
            await self._log_audit_event(
                event_type="login_attempt",
                action="authenticate",
                result="rate_limited",
                details={"email": email, "ip_address": ip_address}
            )
            raise ValueError("Too many failed attempts. Please try again later.")
        
        # Find user
        user = self.db.query(User).filter(User.email == email.lower()).first()
        if not user:
            self.rate_limiter.record_attempt(identifier, success=False)
            await self._log_audit_event(
                event_type="login_attempt",
                action="authenticate",
                result="user_not_found",
                details={"email": email, "ip_address": ip_address}
            )
            raise ValueError("Invalid email or password")
        
        # Check if account is active
        if not user.is_active:
            await self._log_audit_event(
                user_id=user.id,
                event_type="login_attempt",
                action="authenticate",
                result="account_disabled",
                details={"email": email, "ip_address": ip_address}
            )
            raise ValueError("Account is disabled")
        
        # Check if account is locked
        if user.locked_until and datetime.now(timezone.utc) < user.locked_until:
            await self._log_audit_event(
                user_id=user.id,
                event_type="login_attempt",
                action="authenticate",
                result="account_locked",
                details={"email": email, "ip_address": ip_address}
            )
            raise ValueError("Account is temporarily locked")
        
        # Verify password
        if not user.password_hash or not PasswordManager.verify_password(password, user.password_hash):
            self.rate_limiter.record_attempt(identifier, success=False)
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.now(timezone.utc) + timedelta(hours=1)
            
            self.db.commit()
            
            await self._log_audit_event(
                user_id=user.id,
                event_type="login_attempt",
                action="authenticate",
                result="invalid_password",
                details={"email": email, "ip_address": ip_address}
            )
            raise ValueError("Invalid email or password")
        
        # Check MFA if enabled
        if user.mfa_enabled:
            if not mfa_token:
                return user, {"requires_mfa": True}
            
            if not MFAManager.verify_totp(user.mfa_secret, mfa_token):
                # Check backup codes
                if user.backup_codes and mfa_token in user.backup_codes:
                    # Remove used backup code
                    user.backup_codes.remove(mfa_token)
                    self.db.commit()
                else:
                    self.rate_limiter.record_attempt(identifier, success=False)
                    await self._log_audit_event(
                        user_id=user.id,
                        event_type="login_attempt",
                        action="authenticate",
                        result="invalid_mfa",
                        details={"email": email, "ip_address": ip_address}
                    )
                    raise ValueError("Invalid MFA token")
        
        # Authentication successful
        self.rate_limiter.record_attempt(identifier, success=True)
        
        # Clear failed attempts
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.now(timezone.utc)
        user.last_activity = datetime.now(timezone.utc)
        
        self.db.commit()
        
        await self._log_audit_event(
            user_id=user.id,
            event_type="login_success",
            action="authenticate",
            result="success",
            details={"email": email, "ip_address": ip_address}
        )
        
        return user, {"requires_mfa": False}
    
    async def create_user_session(
        self,
        user: User,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_type: Optional[str] = None,
        remember_me: bool = False
    ) -> Tuple[str, str]:
        """Create a new user session and return access and refresh tokens."""
        
        # Generate session tokens
        session_token = SecurityUtils.generate_session_token()
        refresh_token = SecurityUtils.generate_session_token()
        
        # Create session record
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=30 if remember_me else 1
        )
        
        session = UserSession(
            user_id=user.id,
            session_token=session_token,
            refresh_token=refresh_token,
            ip_address=ip_address,
            user_agent=user_agent,
            device_type=device_type,
            expires_at=expires_at
        )
        
        self.db.add(session)
        self.db.commit()
        
        # Create JWT tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "session_id": str(session.id),
            "roles": [role.name for role in user.roles],
            "permissions": user.permissions
        }
        
        access_token = TokenManager.create_access_token(token_data)
        refresh_jwt = TokenManager.create_refresh_token({"sub": str(user.id), "session_id": str(session.id)})
        
        return access_token, refresh_jwt
    
    async def refresh_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Refresh access token using refresh token."""
        
        # Verify refresh token
        payload = TokenManager.verify_token(refresh_token, "refresh")
        if not payload:
            return None
        
        user_id = payload.get("sub")
        session_id = payload.get("session_id")
        
        # Find session
        session = self.db.query(UserSession).filter(
            and_(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        ).first()
        
        if not session:
            return None
        
        # Get user
        user = session.user
        if not user or not user.is_active:
            return None
        
        # Update session activity
        session.last_activity = datetime.now(timezone.utc)
        user.last_activity = datetime.now(timezone.utc)
        self.db.commit()
        
        # Create new tokens
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "session_id": str(session.id),
            "roles": [role.name for role in user.roles],
            "permissions": user.permissions
        }
        
        new_access_token = TokenManager.create_access_token(token_data)
        new_refresh_token = TokenManager.create_refresh_token({
            "sub": str(user.id), 
            "session_id": str(session.id)
        })
        
        # Update session token
        session.refresh_token = SecurityUtils.generate_session_token()
        self.db.commit()
        
        return new_access_token, new_refresh_token
    
    async def logout_user(self, session_id: str, user_id: str) -> bool:
        """Logout user by deactivating session."""
        
        session = self.db.query(UserSession).filter(
            and_(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.is_active == True
            )
        ).first()
        
        if session:
            session.is_active = False
            self.db.commit()
            
            await self._log_audit_event(
                user_id=user_id,
                event_type="logout",
                action="logout",
                result="success",
                details={"session_id": session_id}
            )
            return True
        
        return False
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            return self.db.query(User).filter(User.id == uuid.UUID(user_id)).first()
        except ValueError:
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email.lower()).first()
    
    async def update_user(
        self,
        user_id: str,
        updates: Dict[str, Any],
        updated_by: Optional[str] = None
    ) -> Optional[User]:
        """Update user information."""
        
        user = await self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Track changes for audit
        changes = {}
        
        # Update allowed fields
        updatable_fields = [
            'first_name', 'last_name', 'display_name', 'bio', 
            'avatar_url', 'preferences', 'user_metadata'
        ]
        
        for field in updatable_fields:
            if field in updates:
                old_value = getattr(user, field)
                new_value = updates[field]
                if old_value != new_value:
                    setattr(user, field, new_value)
                    changes[field] = {"old": old_value, "new": new_value}
        
        # Handle email update with validation
        if 'email' in updates:
            email_validation = EmailValidator.validate_email_format(updates['email'])
            if not email_validation["valid"]:
                raise ValueError(f"Invalid email format: {email_validation['error']}")
            
            normalized_email = email_validation["normalized"]
            if user.email != normalized_email:
                # Check for conflicts
                existing_user = self.db.query(User).filter(
                    and_(User.email == normalized_email, User.id != user.id)
                ).first()
                if existing_user:
                    raise ValueError("Email already in use")
                
                changes['email'] = {"old": user.email, "new": normalized_email}
                user.email = normalized_email
                user.email_verified = False  # Require re-verification
        
        if changes:
            user.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(user)
            
            await self._log_audit_event(
                user_id=user.id,
                event_type="user_updated",
                action="update_user",
                result="success",
                details={"changes": changes, "updated_by": updated_by}
            )
        
        return user
    
    async def change_password(
        self,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> bool:
        """Change user password."""
        
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify current password (skip for OAuth users)
        if user.password_hash and not PasswordManager.verify_password(current_password, user.password_hash):
            await self._log_audit_event(
                user_id=user.id,
                event_type="password_change",
                action="change_password",
                result="invalid_current_password"
            )
            raise ValueError("Current password is incorrect")
        
        # Validate new password
        password_validation = PasswordManager.validate_password_strength(new_password)
        if not password_validation["valid"]:
            raise ValueError(f"Password validation failed: {password_validation['errors']}")
        
        # Update password
        user.password_hash = PasswordManager.hash_password(new_password)
        user.password_changed_at = datetime.now(timezone.utc)
        user.updated_at = datetime.now(timezone.utc)
        
        self.db.commit()
        
        await self._log_audit_event(
            user_id=user.id,
            event_type="password_change",
            action="change_password",
            result="success"
        )
        
        return True
    
    async def setup_mfa(self, user_id: str) -> Dict[str, Any]:
        """Setup MFA for user and return QR code data."""
        
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if user.mfa_enabled:
            raise ValueError("MFA is already enabled")
        
        # Generate secret and backup codes
        secret = MFAManager.generate_secret()
        backup_codes = MFAManager.generate_backup_codes()
        
        # Store secret (not enabled yet)
        user.mfa_secret = secret
        user.backup_codes = backup_codes
        self.db.commit()
        
        # Generate QR code
        qr_code = MFAManager.generate_qr_code(secret, user.email)
        
        return {
            "secret": secret,
            "qr_code": qr_code,
            "backup_codes": backup_codes
        }
    
    async def enable_mfa(self, user_id: str, token: str) -> bool:
        """Enable MFA after verifying setup token."""
        
        user = await self.get_user_by_id(user_id)
        if not user or not user.mfa_secret:
            return False
        
        # Verify token
        if not MFAManager.verify_totp(user.mfa_secret, token):
            return False
        
        # Enable MFA
        user.mfa_enabled = True
        self.db.commit()
        
        await self._log_audit_event(
            user_id=user.id,
            event_type="mfa_enabled",
            action="enable_mfa",
            result="success"
        )
        
        return True
    
    async def disable_mfa(self, user_id: str, password: str) -> bool:
        """Disable MFA after password verification."""
        
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Verify password
        if user.password_hash and not PasswordManager.verify_password(password, user.password_hash):
            return False
        
        # Disable MFA
        user.mfa_enabled = False
        user.mfa_secret = None
        user.backup_codes = None
        self.db.commit()
        
        await self._log_audit_event(
            user_id=user.id,
            event_type="mfa_disabled",
            action="disable_mfa",
            result="success"
        )
        
        return True
    
    async def _log_audit_event(
        self,
        event_type: str,
        action: str,
        result: str,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> None:
        """Log audit event."""
        
        audit_log = AuditLog(
            user_id=uuid.UUID(user_id) if user_id else None,
            event_type=event_type,
            action=action,
            result=result,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        self.db.add(audit_log)
        # Don't commit here - let the calling method handle it
