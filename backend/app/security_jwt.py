# Compatibility shim — delegates to security.py
from .security import (
    create_access_token,
    verify_access_token,
    hash_password,
    verify_password,
)
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def login_with_env(username: str, password: str):
    env_user = os.environ.get("ADMIN_USERNAME", "admin")
    env_pass = os.environ.get("ADMIN_PASSWORD")
    if username == env_user and password == env_pass:
        return create_access_token({"sub": username, "role": "Admin"})
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return payload


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
