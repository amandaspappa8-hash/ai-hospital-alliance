from fastapi import APIRouter
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/enterprise-auth", tags=["Enterprise Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "enterprise-secret-key")
ALGORITHM = "HS256"

USERS = {
    "doctor": {"password": "doctor123", "role": "Doctor"},
    "pharmacist": {"password": "pharma123", "role": "Pharmacist"},
    "admin": {"password": "admin123", "role": "Admin"},
}

@router.post("/login")
def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")

    user = USERS.get(username)

    if not user or user["password"] != password:
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
