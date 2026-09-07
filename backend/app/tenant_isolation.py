import uuid
import logging
import os
from typing import AsyncGenerator, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

logger = logging.getLogger(__name__)


DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is required")

if DATABASE_URL.startswith("sqlite:///"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace(
        "sqlite:///",
        "sqlite+aiosqlite:///",
        1
    )
elif DATABASE_URL.startswith("postgresql+psycopg2://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace(
        "postgresql+psycopg2://",
        "postgresql+asyncpg://",
        1
    )
elif DATABASE_URL.startswith("postgresql://"):
    ASYNC_DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1
    )
else:
    ASYNC_DATABASE_URL = DATABASE_URL

engine = create_engine(DATABASE_URL, pool_size=20, max_overflow=40, pool_pre_ping=True, pool_recycle=3600, echo=False)
async_engine = create_async_engine(ASYNC_DATABASE_URL, pool_size=20, max_overflow=40, pool_pre_ping=True, echo=False)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is required")
ALGORITHM = "HS256"
bearer_scheme = HTTPBearer()

from .models import Tenant, User, TenantStatus, UserRole, AuditLog

class TenantContext:
    def __init__(self, tenant_id, tenant_slug, user_id, user_role, tenant=None, user=None):
        self.tenant_id = tenant_id
        self.tenant_slug = tenant_slug
        self.user_id = user_id
        self.user_role = user_role
        self.tenant = tenant
        self.user = user

    @property
    def is_super_admin(self):
        return self.user_role == UserRole.SUPER_ADMIN

    @property
    def is_tenant_admin(self):
        return self.user_role in (UserRole.SUPER_ADMIN, UserRole.TENANT_ADMIN)

    @property
    def is_clinical(self):
        return self.user_role in (UserRole.DOCTOR, UserRole.NURSE, UserRole.PHARMACIST, UserRole.LAB_TECH, UserRole.RADIOLOGIST)


class TenantSession:
    def __init__(self, db: Session, tenant_id: uuid.UUID):
        self._db = db
        self.tenant_id = tenant_id

    def query(self, model):
        if hasattr(model, "tenant_id"):
            return self._db.query(model).filter(model.tenant_id == self.tenant_id)
        return self._db.query(model)

    def add(self, obj):
        if hasattr(obj, "tenant_id") and obj.tenant_id is None:
            obj.tenant_id = self.tenant_id
        elif hasattr(obj, "tenant_id") and obj.tenant_id != self.tenant_id:
            raise PermissionError(f"Cross-tenant write attempt!")
        self._db.add(obj)

    def delete(self, obj):
        if hasattr(obj, "tenant_id") and obj.tenant_id != self.tenant_id:
            raise PermissionError("Cross-tenant delete attempt!")
        self._db.delete(obj)

    def commit(self):
        self._db.commit()

    def rollback(self):
        self._db.rollback()

    def refresh(self, obj):
        self._db.refresh(obj)

    def get_or_404(self, model, resource_id: uuid.UUID, resource_name: str = "Resource"):
        obj = self.query(model).filter(model.id == resource_id).first()
        if not obj:
            raise HTTPException(status_code=404, detail=f"{resource_name} not found")
        return obj


RLS_SETUP_SQL = """
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE encounters ENABLE ROW LEVEL SECURITY;
ALTER TABLE vitals ENABLE ROW LEVEL SECURITY;
ALTER TABLE lab_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE lab_results ENABLE ROW LEVEL SECURITY;
ALTER TABLE radiology_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE medication_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE clinical_ai_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE departments ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_patients ON patients USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_users ON users USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_encounters ON encounters USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_vitals ON vitals USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_lab_orders ON lab_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_lab_results ON lab_results USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_radiology ON radiology_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_medications ON medication_orders USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_ai ON clinical_ai_analyses USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_appointments ON appointments USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_departments ON departments USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
CREATE POLICY tenant_isolation_audit ON audit_logs USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
"""


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {str(e)}", headers={"WWW-Authenticate": "Bearer"})


def create_access_token(data: dict, expires_delta=None) -> str:
    from datetime import datetime, timedelta
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=8))
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def set_rls_tenant(db: Session, tenant_id: uuid.UUID):
    bind = db.get_bind()
    dialect = getattr(bind, "dialect", None)
    dialect_name = getattr(dialect, "name", "")

    # PostgreSQL Row Level Security only.
    # SQLite/dev mode does not support SET LOCAL, so skip safely.
    if dialect_name != "postgresql":
        return

    db.execute(text("SET LOCAL app.current_tenant_id = :tid"), {"tid": str(tenant_id)})


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_tenant_context(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> TenantContext:
    token = credentials.credentials
    payload = decode_token(token)

    user_id_str = payload.get("sub")
    tenant_id_str = payload.get("tenant_id")
    role_str = payload.get("role")

    if not all([user_id_str, tenant_id_str, role_str]):
        raise HTTPException(status_code=401, detail="Incomplete token claims")

    try:
        user_id = uuid.UUID(user_id_str)
        tenant_id = uuid.UUID(tenant_id_str)
        role = UserRole(role_str)
    except (ValueError, KeyError):
        raise HTTPException(status_code=401, detail="Invalid token format")

    is_dev_env = os.getenv("APP_ENV", "").strip().lower() in {"dev", "development", "local", "test"}

    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if is_dev_env and not tenant and str(tenant_id) == "00000000-0000-0000-0000-000000000100":
        class DevTenant:
            id = tenant_id
            slug = "dev-tenant"
            status = TenantStatus.ACTIVE
        tenant = DevTenant()
    if not tenant:
        raise HTTPException(status_code=401, detail="Tenant not found")
    if tenant.status == TenantStatus.SUSPENDED:
        raise HTTPException(status_code=403, detail="Account suspended.")
    if tenant.status == TenantStatus.CANCELLED:
        raise HTTPException(status_code=403, detail="Account cancelled.")

    user = db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id, User.is_active == True).first()
    if is_dev_env and not user and str(user_id) == "00000000-0000-0000-0000-000000000001":
        class DevUser:
            id = user_id
            tenant_id = tenant_id
            is_active = True
            email = "admin@aiha.local"
        user = DevUser()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or inactive")

    if not (is_dev_env and str(tenant_id) == "00000000-0000-0000-0000-000000000100"):
        set_rls_tenant(db, tenant_id)

    ctx = TenantContext(tenant_id=tenant_id, tenant_slug=tenant.slug, user_id=user_id, user_role=role, tenant=tenant, user=user)
    request.state.tenant_ctx = ctx
    return ctx


def get_tenant_db(
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
) -> TenantSession:
    return TenantSession(db, ctx.tenant_id)


def require_roles(*roles: UserRole):
    def dependency(ctx: TenantContext = Depends(get_tenant_context)) -> TenantContext:
        if ctx.user_role not in roles and ctx.user_role != UserRole.SUPER_ADMIN:
            raise HTTPException(status_code=403, detail=f"Access denied. Required: {[r.value for r in roles]}")
        return ctx
    return Depends(dependency)


def require_super_admin(ctx: TenantContext = Depends(get_tenant_context)) -> TenantContext:
    if ctx.user_role != UserRole.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="Super admin only")
    return ctx


def audit(db: Session, ctx: TenantContext, action: str, resource_type: str, resource_id=None, changes: dict = None, request: Request = None):
    log = AuditLog(
        tenant_id=ctx.tenant_id,
        user_id=ctx.user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        changes=changes,
        ip_address=request.client.host if request else None,
        user_agent=request.headers.get("user-agent") if request else None,
    )
    db.add(log)
