import os
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Optional

router = APIRouter(
    prefix="/ahos/49.0.2/identity-rbac",
    tags=["AHOS 49.0.2 Identity & RBAC Platform"]
)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

users_db = {}
roles_db = {
    "super_admin": ["*"],
    "hospital_admin": ["patients:read", "patients:write", "reports:read", "users:read"],
    "doctor": ["patients:read", "reports:read", "clinical:write"],
    "nurse": ["patients:read", "vitals:write"],
    "viewer": ["patients:read"]
}

class RegisterUser(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    role: str = "viewer"
    tenant_id: str = "default_hospital"

class LoginUser(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email not in users_db:
            raise HTTPException(status_code=401, detail="Invalid token user")
        return users_db[email]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 49.0.2",
        "platform": "Identity & RBAC Platform",
        "readiness": "IDENTITY_RBAC_READY",
        "roles": list(roles_db.keys()),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/users/register")
async def register_user(user: RegisterUser):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    if user.role not in roles_db:
        raise HTTPException(status_code=400, detail="Invalid role")

    users_db[user.email] = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hash_password(user.password),
        "role": user.role,
        "tenant_id": user.tenant_id,
        "created_at": datetime.utcnow().isoformat(),
        "is_active": True
    }

    return {
        "status": "registered",
        "email": user.email,
        "role": user.role,
        "tenant_id": user.tenant_id
    }

@router.post("/auth/login")
async def login(user: LoginUser):
    db_user = users_db.get(user.email)

    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "email": db_user["email"],
        "role": db_user["role"],
        "tenant_id": db_user["tenant_id"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user["role"],
        "tenant_id": db_user["tenant_id"]
    }

@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "full_name": current_user["full_name"],
        "role": current_user["role"],
        "tenant_id": current_user["tenant_id"],
        "permissions": roles_db[current_user["role"]]
    }

@router.get("/roles")
async def roles():
    return roles_db

@router.get("/secure/clinical-dashboard")
async def clinical_dashboard(current_user: dict = Depends(get_current_user)):
    role = current_user["role"]
    permissions = roles_db.get(role, [])

    if "*" not in permissions and "patients:read" not in permissions:
        raise HTTPException(status_code=403, detail="Permission denied")

    return {
        "status": "authorized",
        "module": "clinical_dashboard",
        "user": current_user["email"],
        "role": role,
        "tenant_id": current_user["tenant_id"],
        "message": "AHOS secure clinical dashboard access granted"
    }
