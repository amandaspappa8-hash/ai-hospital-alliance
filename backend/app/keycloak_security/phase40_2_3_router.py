"""Phase 40.2.3 valid-token and RBAC endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from .models import AuthenticatedIdentity
from .rbac import require_any_role


READER_ROLE = "ahos_reader"
ADMIN_ROLE = "ahos_admin"


router = APIRouter(
    prefix="/ahos/40.2.3",
    tags=[
        "AHOS Phase 40.2.3 Keycloak RBAC",
    ],
)


@router.get("/status")
async def phase40_2_3_status() -> dict:
    return {
        "phase": "40.2.3",
        "status": "ACTIVE",
        "authentication_provider": "Keycloak",
        "valid_token_flow": True,
        "audience_validation": True,
        "rbac_enforcement": True,
        "reader_role": READER_ROLE,
        "admin_role": ADMIN_ROLE,
        "global_api_enforcement": False,
        "real_patient_data_used": False,
        "clinical_payload_recorded": False,
        "access_tokens_recorded": False,
    }


@router.get("/rbac/reader")
async def phase40_2_3_reader(
    identity: AuthenticatedIdentity = Depends(
        require_any_role(READER_ROLE)
    ),
) -> dict:
    return {
        "phase": "40.2.3",
        "endpoint": "rbac/reader",
        "authenticated": True,
        "authorized": True,
        "required_role": READER_ROLE,
        "subject": identity.subject,
        "username": identity.username,
        "token_returned": False,
        "raw_claims_returned": False,
    }


@router.get("/rbac/admin")
async def phase40_2_3_admin(
    identity: AuthenticatedIdentity = Depends(
        require_any_role(ADMIN_ROLE)
    ),
) -> dict:
    return {
        "phase": "40.2.3",
        "endpoint": "rbac/admin",
        "authenticated": True,
        "authorized": True,
        "required_role": ADMIN_ROLE,
        "subject": identity.subject,
        "username": identity.username,
        "token_returned": False,
        "raw_claims_returned": False,
    }
