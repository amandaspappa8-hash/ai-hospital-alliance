"""
AHOS Compatibility Layer
"""

import os

from .legacy_security import (
    create_access_token,
    verify_access_token,
    hash_password,
    verify_password,
)

from .security_jwt import get_current_user

try:
    from .keycloak_security.jwt_validator import KeycloakJWTValidator

    validator = KeycloakJWTValidator()

    KEYCLOAK_AVAILABLE = True

except Exception:
    validator = None
    KEYCLOAK_AVAILABLE = False


def issue_access_token(payload):
    return create_access_token(payload)


def validate_token(token):
    return verify_access_token(token)


def keycloak_enabled():
    return KEYCLOAK_AVAILABLE

def login_with_env(username: str, password: str):
    env_user = os.environ.get("ADMIN_USERNAME", "admin")
    env_pass = os.environ.get("ADMIN_PASSWORD")
    if username == env_user and password == env_pass:
        return create_access_token({"sub": username, "role": "Admin"})
    return None

def login_with_db(email: str, password: str, db):
    """Login from PostgreSQL with tenant_id in JWT."""
    from .models import User, TenantStatus
    import bcrypt

    user = db.query(User).filter(User.email == email, User.is_active == True).first()
    if not user:
        return None

    try:
        if not bcrypt.checkpw(password.encode(), user.hashed_password.encode()):
            return None
    except Exception:
        return None

    # Check tenant is active
    if user.tenant.status == TenantStatus.SUSPENDED:
        return None

    token = create_access_token({
        "sub": str(user.id),
        "tenant_id": str(user.tenant_id),
        "role": user.role.value,
        "email": user.email,
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "tenant_id": str(user.tenant_id),
        "role": user.role.value,
        "email": user.email,
    }
