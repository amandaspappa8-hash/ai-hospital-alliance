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
    env_pass = os.environ.get("ADMIN_PASSWORD", "admin123")
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
