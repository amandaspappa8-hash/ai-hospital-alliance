"""
SaaS Multi-Tenant Management
- Hospital onboarding (self-service registration)
- Subscription plans & feature flags
- Tenant isolation enforcement
- Usage metering
"""

import os, uuid, secrets
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, JSON
from sqlalchemy.orm import Session

from .db import Base, SessionLocal
from .legacy_security import hash_password


# ─── Plans ───────────────────────────────────────────────────────────────────

PLANS = {
    "trial": {
        "name": "Trial (14 days)",
        "price_usd": 0,
        "max_users": 5,
        "max_patients": 50,
        "ai_calls_per_day": 20,
        "features": ["basic_emr", "labs", "radiology"],
        "trial_days": 14,
    },
    "starter": {
        "name": "Starter",
        "price_usd": 299,
        "max_users": 25,
        "max_patients": 500,
        "ai_calls_per_day": 200,
        "features": ["basic_emr", "labs", "radiology", "pharmacy", "reports"],
        "trial_days": 0,
    },
    "professional": {
        "name": "Professional",
        "price_usd": 799,
        "max_users": 100,
        "max_patients": 5000,
        "ai_calls_per_day": 1000,
        "features": [
            "basic_emr", "labs", "radiology", "pharmacy", "reports",
            "ai_diagnosis", "fhir_export", "audit_logs", "2fa",
        ],
        "trial_days": 0,
    },
    "enterprise": {
        "name": "Enterprise",
        "price_usd": 0,  # custom pricing
        "max_users": -1,  # unlimited
        "max_patients": -1,
        "ai_calls_per_day": -1,
        "features": ["*"],  # all features
        "trial_days": 0,
    },
}


# ─── Models ──────────────────────────────────────────────────────────────────

class Tenant(Base):
    __tablename__ = "tenants"
    __table_args__ = {"extend_existing": True}
    id = Column(String(20), primary_key=True)          # e.g. H-abc12
    name = Column(String(200), nullable=False)
    slug = Column(String(80), unique=True, nullable=False)  # url-safe name
    plan = Column(String(40), default="trial")
    admin_email = Column(String(200), nullable=False)
    admin_name = Column(String(120))
    country = Column(String(80))
    phone = Column(String(30))
    api_key = Column(String(64), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    trial_ends_at = Column(DateTime, nullable=True)
    plan_starts_at = Column(DateTime, default=datetime.utcnow)
    plan_ends_at = Column(DateTime, nullable=True)
    settings = Column(JSON, default={})
    ai_calls_today = Column(Integer, default=0)
    ai_calls_reset_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ─── Schemas ─────────────────────────────────────────────────────────────────

class HospitalRegisterRequest(BaseModel):
    hospital_name: str
    admin_name: str
    admin_email: str
    admin_password: str
    country: str = ""
    phone: str = ""
    plan: str = "trial"


class TenantPublic(BaseModel):
    id: str
    name: str
    slug: str
    plan: str
    plan_name: str
    is_active: bool
    is_verified: bool
    trial_ends_at: Optional[datetime]
    features: list
    limits: dict
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _make_slug(name: str) -> str:
    import re
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")[:40]
    return s


def _generate_hospital_id() -> str:
    return "H-" + secrets.token_hex(4).upper()


def _generate_api_key() -> str:
    return "aiha_" + secrets.token_urlsafe(40)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_tenant_by_id(tenant_id: str, db: Session) -> Tenant:
    t = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not t:
        raise HTTPException(404, "Tenant not found")
    if not t.is_active:
        raise HTTPException(403, "Tenant account is suspended")
    return t


def get_tenant_from_api_key(api_key: str, db: Session) -> Tenant:
    t = db.query(Tenant).filter(Tenant.api_key == api_key).first()
    if not t:
        raise HTTPException(401, "Invalid API key")
    if not t.is_active:
        raise HTTPException(403, "Tenant account is suspended")
    return t


def check_ai_quota(tenant: Tenant, db: Session) -> None:
    plan = PLANS.get(tenant.plan, PLANS["trial"])
    limit = plan["ai_calls_per_day"]
    if limit == -1:
        return  # unlimited (enterprise)
    # Reset counter if new day
    now = datetime.utcnow()
    if tenant.ai_calls_reset_at.date() < now.date():
        tenant.ai_calls_today = 0
        tenant.ai_calls_reset_at = now
        db.commit()
    if tenant.ai_calls_today >= limit:
        raise HTTPException(429, f"Daily AI quota exceeded ({limit}/day). Upgrade your plan.")


def increment_ai_usage(tenant: Tenant, db: Session) -> None:
    tenant.ai_calls_today = (tenant.ai_calls_today or 0) + 1
    db.commit()


def has_feature(tenant: Tenant, feature: str) -> bool:
    plan = PLANS.get(tenant.plan, PLANS["trial"])
    feats = plan["features"]
    return "*" in feats or feature in feats


def require_feature(tenant: Tenant, feature: str) -> None:
    if not has_feature(tenant, feature):
        raise HTTPException(402, f"Feature '{feature}' requires a higher plan. Visit /saas/plans to upgrade.")


def tenant_to_public(t: Tenant) -> dict:
    plan = PLANS.get(t.plan, PLANS["trial"])
    return {
        "id": t.id,
        "name": t.name,
        "slug": t.slug,
        "plan": t.plan,
        "plan_name": plan["name"],
        "is_active": t.is_active,
        "is_verified": t.is_verified,
        "trial_ends_at": t.trial_ends_at.isoformat() if t.trial_ends_at else None,
        "features": plan["features"],
        "limits": {
            "max_users": plan["max_users"],
            "max_patients": plan["max_patients"],
            "ai_calls_per_day": plan["ai_calls_per_day"],
        },
        "created_at": t.created_at.isoformat(),
    }


# ─── Registration ─────────────────────────────────────────────────────────────

def register_hospital(req: HospitalRegisterRequest, db: Session) -> dict:
    from .models import Hospital, User, Department

    if req.plan not in PLANS:
        raise HTTPException(400, f"Invalid plan. Choose from: {list(PLANS.keys())}")

    # Validate password strength
    if len(req.admin_password) < 12:
        raise HTTPException(400, "Password must be at least 12 characters")

    slug = _make_slug(req.hospital_name)
    # Ensure slug uniqueness
    base_slug = slug
    i = 1
    while db.query(Tenant).filter(Tenant.slug == slug).first():
        slug = f"{base_slug}-{i}"
        i += 1

    # Check email uniqueness
    if db.query(Tenant).filter(Tenant.admin_email == req.admin_email).first():
        raise HTTPException(409, "An account with this email already exists")

    tenant_id = _generate_hospital_id()
    # Ensure id uniqueness
    while db.query(Tenant).filter(Tenant.id == tenant_id).first():
        tenant_id = _generate_hospital_id()

    plan_cfg = PLANS[req.plan]
    trial_ends = (
        datetime.utcnow() + timedelta(days=plan_cfg["trial_days"])
        if plan_cfg["trial_days"] > 0
        else None
    )

    api_key = _generate_api_key()

    # Create tenant record
    tenant = Tenant(
        id=tenant_id,
        name=req.hospital_name,
        slug=slug,
        plan=req.plan,
        admin_email=req.admin_email,
        admin_name=req.admin_name,
        country=req.country,
        phone=req.phone,
        api_key=api_key,
        is_active=True,
        is_verified=False,
        trial_ends_at=trial_ends,
    )
    db.add(tenant)

    # Create Hospital record (for existing system compatibility)
    hospital = Hospital(
        id=tenant_id,
        name=req.hospital_name,
        address=req.country,
        phone=req.phone,
    )
    db.add(hospital)
    db.flush()

    # Create default departments
    default_depts = ["Emergency", "ICU", "Cardiology", "Radiology", "General"]
    dept_codes = ["ER", "ICU", "CARD", "RAD", "GEN"]
    for name, code in zip(default_depts, dept_codes):
        db.add(Department(name=name, code=f"{code}-{tenant_id[-4:]}", hospital_id=tenant_id))
    db.flush()

    # Create admin user
    admin = User(
        username=req.admin_email,
        password=hash_password(req.admin_password),
        name=req.admin_name,
        role="admin",
        hospital_id=tenant_id,
        is_active=True,
    )
    db.add(admin)
    db.commit()

    return {
        "message": "Hospital registered successfully",
        "hospital_id": tenant_id,
        "slug": slug,
        "api_key": api_key,
        "plan": req.plan,
        "trial_ends_at": trial_ends.isoformat() if trial_ends else None,
        "next_steps": [
            "Save your API key securely — it won't be shown again",
            "Login with your admin email and password at /auth/login",
            "Add departments and staff from the Admin panel",
        ],
    }
