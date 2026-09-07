from fastapi import APIRouter, HTTPException
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/enterprise-auth", tags=["Enterprise Auth"])

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")
ALGORITHM = "HS256"

USERS = {
    "doctor": {
        "password_env": "AIHA_ENTERPRISE_DOCTOR_PASSWORD",
        "role": "Doctor",
    },
    "pharmacist": {
        "password_env": "AIHA_ENTERPRISE_PHARMACIST_PASSWORD",
        "role": "Pharmacist",
    },
    "admin": {
        "password_env": "AIHA_ENTERPRISE_ADMIN_PASSWORD",
        "role": "Admin",
    },
}

@router.post("/login")
def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")

    user = USERS.get(username)

    if not user:
        return {"error": "Invalid credentials"}

    expected_password = os.environ.get(user["password_env"])

    if not expected_password:
        raise HTTPException(
            status_code=503,
            detail="Enterprise authentication is not configured",
        )

    if expected_password != password:
        return {"error": "Invalid credentials"}

    token = jwt.encode(
        {
            "sub": username,
            "role": user["role"],
            "exp": datetime.utcnow() + timedelta(hours=8),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
    }
