"""
Shared dependencies — import هذا في كل router
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..security_compat import validate_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = validate_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload

async def require_admin(user: dict = Depends(get_current_user)):
    if user.get("role") != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user

async def require_doctor(user: dict = Depends(get_current_user)):
    if user.get("role") not in ("Admin", "Doctor"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Doctor access required",
        )
    return user

from fastapi import Request
from ..legacy_security import check_rate_limit

async def rate_limit_middleware(request: Request):
    client_ip = request.client.host
    key = f"rate:{client_ip}:{request.url.path}"
    if not check_rate_limit(key, max_requests=60, window=60):
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please slow down.",
            headers={"Retry-After": "60"},
        )

async def auth_rate_limit(request: Request):
    client_ip = request.client.host
    key = f"auth:{client_ip}"
    if not check_rate_limit(key, max_requests=10, window=60):
        raise HTTPException(
            status_code=429,
            detail="Too many login attempts. Try again in 60 seconds.",
            headers={"Retry-After": "60"},
        )
