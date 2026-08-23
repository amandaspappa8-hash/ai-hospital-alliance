"""Phase 40.2.2 public and protected test endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from .dependencies import (
    get_authenticated_identity,
    get_keycloak_validator,
)
from .models import AuthenticatedIdentity


router = APIRouter(
    prefix="/ahos/40.2.2",
    tags=[
        "AHOS Phase 40.2.2 Authentication",
    ],
)


@router.get("/status")
async def phase40_2_2_status() -> dict:
    """
    Public operational status.

    This endpoint exposes configuration state only.
    It never exposes tokens, credentials, or claims.
    """

    validator = get_keycloak_validator()
    metadata = validator.metadata_status()

    return {
        "phase": "40.2.2",
        "status": "ACTIVE",
        "authentication_provider": "Keycloak",
        "authentication_dependency": True,
        "protected_test_router": True,
        "global_enforcement": False,
        "rbac_enforcement": False,
        "issuer": metadata["issuer"],
        "signing_keys": metadata["signing_keys"],
        "allowed_algorithms": (
            metadata["allowed_algorithms"]
        ),
        "audience_validation_enabled": (
            metadata[
                "audience_validation_enabled"
            ]
        ),
        "real_patient_data_used": False,
        "clinical_payload_recorded": False,
        "access_tokens_recorded": False,
    }


@router.get("/public")
async def phase40_2_2_public() -> dict:
    return {
        "phase": "40.2.2",
        "endpoint": "public",
        "authentication_required": False,
        "status": "PASSED",
    }


@router.get("/protected/whoami")
async def phase40_2_2_whoami(
    identity: AuthenticatedIdentity = Depends(
        get_authenticated_identity
    ),
) -> dict:
    """
    Return a restricted identity projection.

    Raw JWT claims and access tokens are intentionally
    excluded from the response.
    """

    return {
        "phase": "40.2.2",
        "endpoint": "protected/whoami",
        "authentication_required": True,
        "authenticated": True,
        "identity": {
            "subject": identity.subject,
            "username": identity.username,
            "email": identity.email,
            "issuer": identity.issuer,
            "audience": list(identity.audience),
            "realm_roles": sorted(
                identity.realm_roles
            ),
            "client_roles": {
                client: sorted(roles)
                for client, roles
                in identity.client_roles.items()
            },
        },
        "token_returned": False,
        "raw_claims_returned": False,
        "clinical_payload_recorded": False,
    }
