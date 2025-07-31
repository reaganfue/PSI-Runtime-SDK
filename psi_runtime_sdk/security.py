"""
Enterprise Security Module for PSI Runtime SDK

Provides authentication, authorization, rate limiting, and security utilities.
"""

import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Set
from collections import defaultdict

import jwt
from cryptography.fernet import Fernet
from passlib.context import CryptContext

from .config import get_config
from .logging import get_logger, security_logger

# Initialize configuration and logger
config = get_config()
logger = get_logger("security")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SecurityException(Exception):
    """Base exception for security-related errors."""
    pass


class AuthenticationError(SecurityException):
    """Authentication failed."""
    pass


class AuthorizationError(SecurityException):
    """Authorization failed."""
    pass


class RateLimitExceeded(SecurityException):
    """Rate limit exceeded."""
    pass


class TokenManager:
    """JWT token management."""
    
    def __init__(self):
        self.secret_key = config.security.jwt_secret_key or self._generate_secret_key()
        self.algorithm = config.security.jwt_algorithm
        self.expiration_hours = config.security.jwt_expiration_hours
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key if none is configured."""
        logger.warning("No JWT secret key configured, generating a temporary one")
        return secrets.token_urlsafe(32)
    
    def create_token(self, user_id: str, additional_claims: Optional[Dict] = None) -> str:
        """Create a JWT token for a user."""
        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "iat": now,
            "exp": now + timedelta(hours=self.expiration_hours),
            "iss": "psi-runtime-sdk",
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        security_logger.log_security_event(
            "token_created",
            severity="info",
            user_id=user_id,
            expiration=payload["exp"].isoformat()
        )
        
        return token
    
    def verify_token(self, token: str) -> Dict:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                issuer="psi-runtime-sdk"
            )
            
            security_logger.log_security_event(
                "token_verified",
                severity="info",
                user_id=payload.get("user_id")
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            security_logger.log_security_event(
                "token_expired",
                severity="warning",
                token_preview=token[:20] + "..."
            )
            raise AuthenticationError("Token has expired")
        
        except jwt.InvalidTokenError as e:
            security_logger.log_security_event(
                "token_invalid",
                severity="warning",
                error=str(e),
                token_preview=token[:20] + "..."
            )
            raise AuthenticationError("Invalid token")
    
    def refresh_token(self, token: str) -> str:
        """Refresh an existing token."""
        payload = self.verify_token(token)
        user_id = payload["user_id"]
        
        # Create new token with same claims (excluding timestamps)
        additional_claims = {
            k: v for k, v in payload.items()
            if k not in ["iat", "exp", "user_id"]
        }
        
        return self.create_token(user_id, additional_claims)


class APIKeyManager:
    """API key management."""
    
    def __init__(self):
        self.valid_keys: Set[str] = set()
        self.key_metadata: Dict[str, Dict] = {}
        
        # Load API keys from environment or configuration
        self._load_api_keys()
    
    def _load_api_keys(self):
        """Load API keys from configuration."""
        # In a real implementation, these would come from a secure database
        # For now, we'll support environment variables
        import os
        
        api_keys = os.environ.get("API_KEYS", "").split(",")
        for key in api_keys:
            key = key.strip()
            if key:
                self.valid_keys.add(key)
                self.key_metadata[key] = {
                    "created_at": datetime.utcnow().isoformat(),
                    "usage_count": 0,
                    "last_used": None
                }
    
    def generate_api_key(self, description: str = "") -> str:
        """Generate a new API key."""
        key = "psi_" + secrets.token_urlsafe(32)
        
        self.valid_keys.add(key)
        self.key_metadata[key] = {
            "created_at": datetime.utcnow().isoformat(),
            "description": description,
            "usage_count": 0,
            "last_used": None
        }
        
        security_logger.log_security_event(
            "api_key_generated",
            severity="info",
            key_prefix=key[:10] + "...",
            description=description
        )
        
        return key
    
    def verify_api_key(self, key: str) -> bool:
        """Verify an API key."""
        is_valid = key in self.valid_keys
        
        if is_valid:
            # Update usage statistics
            metadata = self.key_metadata.get(key, {})
            metadata["usage_count"] = metadata.get("usage_count", 0) + 1
            metadata["last_used"] = datetime.utcnow().isoformat()
            
            security_logger.log_security_event(
                "api_key_used",
                severity="info",
                key_prefix=key[:10] + "...",
                usage_count=metadata["usage_count"]
            )
        else:
            security_logger.log_security_event(
                "api_key_invalid",
                severity="warning",
                key_preview=key[:10] + "..." if len(key) > 10 else key
            )
        
        return is_valid
    
    def revoke_api_key(self, key: str):
        """Revoke an API key."""
        if key in self.valid_keys:
            self.valid_keys.remove(key)
            self.key_metadata.pop(key, None)
            
            security_logger.log_security_event(
                "api_key_revoked",
                severity="info",
                key_prefix=key[:10] + "..."
            )


class RateLimiter:
    """Rate limiting implementation."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.cleanup_interval = 300  # Clean up old entries every 5 minutes
        self.last_cleanup = time.time()
    
    async def check_rate_limit(self, identifier: str, endpoint: str = "default"):
        """Check if a request is within rate limits."""
        now = time.time()
        key = f"{identifier}:{endpoint}"
        
        # Clean up old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries()
            self.last_cleanup = now
        
        # Get requests in the last minute
        minute_ago = now - 60
        recent_requests = [
            req_time for req_time in self.requests[key]
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(recent_requests) >= self.requests_per_minute:
            security_logger.log_security_event(
                "rate_limit_exceeded",
                severity="warning",
                identifier=identifier,
                endpoint=endpoint,
                requests_count=len(recent_requests)
            )
            raise RateLimitExceeded(
                f"Rate limit exceeded: {len(recent_requests)} requests in the last minute"
            )
        
        # Record this request
        recent_requests.append(now)
        self.requests[key] = recent_requests
    
    def _cleanup_old_entries(self):
        """Clean up old rate limiting entries."""
        cutoff_time = time.time() - 300  # 5 minutes ago
        
        for key in list(self.requests.keys()):
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if req_time > cutoff_time
            ]
            
            # Remove empty entries
            if not self.requests[key]:
                del self.requests[key]


class DataEncryption:
    """Data encryption utilities."""
    
    def __init__(self):
        self.key = self._get_or_generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def _get_or_generate_key(self) -> bytes:
        """Get encryption key from environment or generate one."""
        import os
        
        key_env = os.environ.get("ENCRYPTION_KEY")
        if key_env:
            return key_env.encode()
        
        # Generate a new key (in production, this should be stored securely)
        logger.warning("No encryption key configured, generating a temporary one")
        return Fernet.generate_key()
    
    def encrypt(self, data: str) -> str:
        """Encrypt a string."""
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt a string."""
        decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()
    
    def hash_password(self, password: str) -> str:
        """Hash a password securely."""
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(password, hashed_password)


class InputValidator:
    """Input validation and sanitization."""
    
    @staticmethod
    def sanitize_string(input_str: str, max_length: int = 10000) -> str:
        """Sanitize a string input."""
        if not isinstance(input_str, str):
            raise ValueError("Input must be a string")
        
        # Remove null bytes and control characters
        sanitized = "".join(char for char in input_str if ord(char) >= 32 or char in ['\n', '\r', '\t'])
        
        # Truncate if too long
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    @staticmethod
    def validate_json_structure(data: Dict, required_fields: Set[str]) -> bool:
        """Validate JSON structure has required fields."""
        if not isinstance(data, dict):
            return False
        
        return all(field in data for field in required_fields)
    
    @staticmethod
    def is_safe_filename(filename: str) -> bool:
        """Check if a filename is safe (no path traversal)."""
        import os.path
        
        # Check for path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            return False
        
        # Check for reserved names (Windows)
        reserved_names = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        }
        
        if filename.upper() in reserved_names:
            return False
        
        return True


# Global instances
token_manager = TokenManager()
api_key_manager = APIKeyManager()
data_encryption = DataEncryption()
input_validator = InputValidator()


# Convenience functions for API use
def verify_jwt_token(token: str) -> Dict:
    """Verify a JWT token."""
    return token_manager.verify_token(token)


def verify_api_key(key: str) -> bool:
    """Verify an API key."""
    return api_key_manager.verify_api_key(key)


def create_user_token(user_id: str, additional_claims: Optional[Dict] = None) -> str:
    """Create a JWT token for a user."""
    return token_manager.create_token(user_id, additional_claims)


def generate_api_key(description: str = "") -> str:
    """Generate a new API key."""
    return api_key_manager.generate_api_key(description)


def hash_password(password: str) -> str:
    """Hash a password securely."""
    return data_encryption.hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return data_encryption.verify_password(password, hashed_password)


def sanitize_input(input_str: str, max_length: int = 10000) -> str:
    """Sanitize string input."""
    return input_validator.sanitize_string(input_str, max_length)