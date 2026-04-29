"""
Multi-tenant Architecture
Each hospital gets isolated data via hospital_id
"""

from functools import wraps
from fastapi import HTTPException, Header
from typing import Optional

TENANT_REGISTRY = {
    "H-001": {"name": "AI Hospital Alliance", "plan": "enterprise", "active": True},
    "H-002": {"name": "Demo Hospital", "plan": "basic", "active": True},
}


def get_tenant(hospital_id: str) -> dict:
    tenant = TENANT_REGISTRY.get(hospital_id)
    if not tenant:
        raise HTTPException(status_code=403, detail="Invalid tenant")
    if not tenant["active"]:
        raise HTTPException(status_code=403, detail="Tenant suspended")
    return tenant


def require_enterprise(hospital_id: str):
    tenant = get_tenant(hospital_id)
    if tenant["plan"] not in ("enterprise", "professional"):
        raise HTTPException(status_code=402, detail="Enterprise plan required")


class TenantContext:
    def __init__(self, hospital_id: str = "H-001"):
        self.hospital_id = hospital_id
        self.tenant = get_tenant(hospital_id)

    @property
    def is_enterprise(self) -> bool:
        return self.tenant["plan"] == "enterprise"
