"""Core authentication utilities and password management."""

import os
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List

import pyotp
import qrcode
from passlib.context import CryptContext
from jose import jwt, JWTError
from email_validator import validate_email, EmailNotValidError

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))


class PasswordManager:
    """Password utilities for hashing and validation."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate a secure random password."""
        import string
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Any]:
        """Validate password strength and return detailed feedback."""
        errors = []
        score = 0
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        else:
            score += 1
            
        if len(password) >= 12:
            score += 1
            
        if any(c.islower() for c in password):
            score += 1
        else:
            errors.append("Password must contain lowercase letters")
            
        if any(c.isupper() for c in password):
            score += 1
        else:
            errors.append("Password must contain uppercase letters")
            
        if any(c.isdigit() for c in password):
            score += 1
        else:
            errors.append("Password must contain numbers")
            
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 1
        else:
            errors.append("Password must contain special characters")
        
        # Check for common patterns
        if password.lower() in ['password', '123456', 'qwerty', 'admin']:
            errors.append("Password is too common")
            score = max(0, score - 2)
        
        strength_levels = ["very_weak", "weak", "fair", "good", "strong", "very_strong"]
        strength = strength_levels[min(score, len(strength_levels) - 1)]
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "score": score,
            "strength": strength
        }


class TokenManager:
    """JWT token utilities for authentication."""
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def create_refresh_token(data: Dict[str, Any]) -> str:
        """Create a JWT refresh token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload.get("type") != token_type:
                return None
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def decode_token_without_verification(token: str) -> Optional[Dict[str, Any]]:
        """Decode token without verification (for debugging/logging)."""
        try:
            return jwt.get_unverified_claims(token)
        except JWTError:
            return None


class MFAManager:
    """Multi-factor authentication utilities."""
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new TOTP secret."""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(secret: str, user_email: str, issuer: str = "InfoTerminal") -> bytes:
        """Generate QR code for TOTP setup."""
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        from io import BytesIO
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        return img_buffer.getvalue()
    
    @staticmethod
    def verify_totp(secret: str, token: str) -> bool:
        """Verify a TOTP token."""
        totp = pyotp.TOTP(secret)
        return totp.verify(token, valid_window=1)  # Allow 1 window of tolerance
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """Generate backup codes for MFA recovery."""
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric codes
            code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
            codes.append(f"{code[:4]}-{code[4:]}")
        return codes
    
    @staticmethod
    def hash_backup_codes(codes: List[str]) -> List[str]:
        """Hash backup codes for secure storage."""
        return [hashlib.sha256(code.encode()).hexdigest() for code in codes]
    
    @staticmethod
    def verify_backup_code(code: str, hashed_codes: List[str]) -> bool:
        """Verify a backup code against hashed codes."""
        code_hash = hashlib.sha256(code.encode()).hexdigest()
        return code_hash in hashed_codes


class EmailValidator:
    """Email validation utilities."""
    
    @staticmethod
    def validate_email_format(email: str) -> Dict[str, Any]:
        """Validate email format and return detailed information."""
        try:
            validation = validate_email(email)
            return {
                "valid": True,
                "email": validation.email,
                "normalized": validation.email.lower(),
                "local": validation.local,
                "domain": validation.domain,
                "smtputf8": validation.smtputf8
            }
        except EmailNotValidError as e:
            return {
                "valid": False,
                "error": str(e),
                "email": email
            }
    
    @staticmethod
    def is_disposable_email(email: str) -> bool:
        """Check if email is from a disposable email provider."""
        # Simple check against common disposable email domains
        disposable_domains = {
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'throwaway.email', 'temp-mail.org'
        }
        domain = email.split('@')[-1].lower()
        return domain in disposable_domains


class SecurityUtils:
    """Security utilities for authentication."""
    
    @staticmethod
    def generate_session_token() -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def generate_api_key() -> tuple[str, str]:
        """Generate API key and return (key, prefix)."""
        # Generate random key
        key = secrets.token_urlsafe(32)
        # Create prefix for identification (first 8 chars)
        prefix = key[:8]
        return key, prefix
    
    @staticmethod
    def hash_api_key(api_key: str) -> str:
        """Hash API key for secure storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    @staticmethod
    def verify_api_key(api_key: str, api_key_hash: str) -> bool:
        """Verify API key against its hash."""
        return hashlib.sha256(api_key.encode()).hexdigest() == api_key_hash
    
    @staticmethod
    def generate_verification_token() -> str:
        """Generate email verification token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def is_password_compromised(password: str) -> bool:
        """Check if password appears in known breach databases (placeholder)."""
        # In a real implementation, you would check against HaveIBeenPwned API
        # or maintain a local database of compromised passwords
        return False
    
    @staticmethod
    def calculate_password_entropy(password: str) -> float:
        """Calculate password entropy in bits."""
        import math
        charset_size = 0
        
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            charset_size += 22
        
        if charset_size == 0:
            return 0.0
        
        return len(password) * math.log2(charset_size)


class RateLimiter:
    """Simple in-memory rate limiter for authentication attempts."""
    
    def __init__(self):
        self._attempts = {}
        self._lockouts = {}
    
    def is_rate_limited(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if identifier is rate limited."""
        now = datetime.now(timezone.utc)
        
        # Check if currently locked out
        if identifier in self._lockouts:
            if now < self._lockouts[identifier]:
                return True
            else:
                # Lockout expired, remove it
                del self._lockouts[identifier]
        
        # Clean old attempts
        if identifier in self._attempts:
            self._attempts[identifier] = [
                attempt for attempt in self._attempts[identifier]
                if now - attempt < timedelta(minutes=window_minutes)
            ]
        
        # Check current attempt count
        attempt_count = len(self._attempts.get(identifier, []))
        return attempt_count >= max_attempts
    
    def record_attempt(self, identifier: str, success: bool = False, lockout_minutes: int = 60):
        """Record an authentication attempt."""
        now = datetime.now(timezone.utc)
        
        if success:
            # Clear attempts on successful login
            if identifier in self._attempts:
                del self._attempts[identifier]
            if identifier in self._lockouts:
                del self._lockouts[identifier]
        else:
            # Record failed attempt
            if identifier not in self._attempts:
                self._attempts[identifier] = []
            self._attempts[identifier].append(now)
            
            # Check if should be locked out
            if len(self._attempts[identifier]) >= 5:
                self._lockouts[identifier] = now + timedelta(minutes=lockout_minutes)
