from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any
import base64
import hashlib
import hmac
import json
import os
import sqlite3
import uuid

from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


ROOT = Path.home() / "Projects/ai-hospital-alliance-github"

PHASE_PREFIX = "/ahos/36.4/synthetic"

SYNTHETIC_DB = Path(
    os.environ.get(
        "AHOS_PHASE36_4_SYNTHETIC_DB",
        str(
            ROOT
            / "research/phase36_4/synthetic_runtime"
            / "phase36_4_synthetic.db"
        ),
    )
).resolve()

TOKEN_SECRET = os.environ.get(
    "AHOS_PHASE36_4_TOKEN_SECRET",
    "",
)

PHASE_ENABLED = (
    os.environ.get(
        "AHOS_PHASE36_4_ENABLED",
        "false",
    ).lower()
    == "true"
)

router = APIRouter(
    prefix=PHASE_PREFIX,
    tags=["AHOS Phase 36.4 Synthetic Tenant Integration"],
)


class SyntheticUpdate(BaseModel):
    synthetic_value: str


def connect() -> sqlite3.Connection:
    connection = sqlite3.connect(SYNTHETIC_DB)
    connection.row_factory = sqlite3.Row
    return connection


def decode_base64url(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(
        value + padding
    )


def decode_token(token: str) -> dict[str, Any]:
    if not PHASE_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="PHASE36_4_DISABLED",
        )

    if not TOKEN_SECRET:
        raise HTTPException(
            status_code=503,
            detail="PHASE36_4_SECRET_NOT_CONFIGURED",
        )

    try:
        payload_part, signature = token.split(
            ".",
            1,
        )

        expected = hmac.new(
            TOKEN_SECRET.encode("utf-8"),
            payload_part.encode("ascii"),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            signature,
            expected,
        ):
            raise ValueError(
                "INVALID_SIGNATURE"
            )

        claims = json.loads(
            decode_base64url(
                payload_part
            ).decode("utf-8")
        )

    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="INVALID_AUTHENTICATION_TOKEN",
        ) from error

    required_claims = {
        "sub",
        "tenant_id",
        "role",
        "exp",
        "environment",
    }

    if not required_claims.issubset(claims):
        raise HTTPException(
            status_code=401,
            detail="TOKEN_REQUIRED_CLAIMS_MISSING",
        )

    if claims.get("environment") != "phase36_4_synthetic":
        raise HTTPException(
            status_code=401,
            detail="INVALID_TOKEN_ENVIRONMENT",
        )

    now = int(datetime.now(UTC).timestamp())

    if int(claims["exp"]) < now:
        raise HTTPException(
            status_code=401,
            detail="TOKEN_EXPIRED",
        )

    return claims


def authenticate(
    authorization: str | None,
) -> dict[str, Any]:
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="AUTHORIZATION_REQUIRED",
        )

    prefix = "Bearer "

    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=401,
            detail="BEARER_TOKEN_REQUIRED",
        )

    return decode_token(
        authorization[len(prefix):]
    )


def record_denial(
    *,
    request: Request,
    actor_user_id: str,
    authenticated_tenant: str,
    requested_tenant: str,
    resource_id: str,
    reason: str,
) -> None:
    connection = connect()

    connection.execute(
        """
        INSERT INTO denied_access_audit (
            audit_id,
            generated_at_utc,
            request_method,
            request_path,
            actor_user_id,
            authenticated_tenant,
            requested_tenant,
            resource_id,
            authorization_decision,
            denial_reason,
            medical_payload_recorded
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"AUD-{uuid.uuid4().hex.upper()}",
            datetime.now(UTC).isoformat(),
            request.method,
            request.url.path,
            actor_user_id,
            authenticated_tenant,
            requested_tenant,
            resource_id,
            "DENY",
            reason,
            0,
        ),
    )

    connection.commit()
    connection.close()


def enforce_tenant(
    *,
    request: Request,
    claims: dict[str, Any],
    requested_tenant: str | None,
) -> str:
    authenticated_tenant = str(
        claims["tenant_id"]
    )

    if (
        requested_tenant
        and requested_tenant
        != authenticated_tenant
    ):
        record_denial(
            request=request,
            actor_user_id=str(claims["sub"]),
            authenticated_tenant=
                authenticated_tenant,
            requested_tenant=
                requested_tenant,
            resource_id="",
            reason=
                "TENANT_HEADER_OVERRIDE_DENIED",
        )

        raise HTTPException(
            status_code=403,
            detail="TENANT_SCOPE_CONFLICT",
        )

    return authenticated_tenant


class Phase36_4TenantMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        path = request.url.path

        if not path.startswith(PHASE_PREFIX):
            return await call_next(request)

        if path == f"{PHASE_PREFIX}/health":
            return await call_next(request)

        if not PHASE_ENABLED:
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "PHASE36_4_DISABLED",
                },
            )

        authorization = request.headers.get(
            "authorization"
        )

        try:
            claims = authenticate(authorization)

        except HTTPException as error:
            return JSONResponse(
                status_code=error.status_code,
                content={
                    "detail": error.detail,
                },
            )

        request.state.phase36_4_claims = claims

        return await call_next(request)


def middleware_claims(
    request: Request,
) -> dict[str, Any]:
    claims = getattr(
        request.state,
        "phase36_4_claims",
        None,
    )

    if not claims:
        raise HTTPException(
            status_code=401,
            detail="AUTHENTICATED_CLAIMS_MISSING",
        )

    return claims


@router.get("/health")
def phase_health() -> dict[str, Any]:
    if not PHASE_ENABLED:
        raise HTTPException(
            status_code=503,
            detail="PHASE36_4_DISABLED",
        )

    connection = connect()

    integrity = connection.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]

    connection.close()

    return {
        "status": "healthy",
        "phase": "36.4",
        "database": integrity,
        "scope": "protected_synthetic_routes_only",
        "main_medical_routes_modified": False,
    }


@router.get("/records")
def list_records(
    request: Request,
    x_tenant_id: str | None = Header(
        default=None,
    ),
) -> dict[str, Any]:
    claims = middleware_claims(request)

    tenant_id = enforce_tenant(
        request=request,
        claims=claims,
        requested_tenant=x_tenant_id,
    )

    connection = connect()

    rows = connection.execute(
        """
        SELECT
            record_id,
            tenant_id,
            synthetic_subject,
            synthetic_value
        FROM synthetic_records
        WHERE tenant_id = ?
        ORDER BY record_id
        """,
        (tenant_id,),
    ).fetchall()

    connection.close()

    return {
        "tenant_id": tenant_id,
        "count": len(rows),
        "records": [
            dict(row)
            for row in rows
        ],
    }


@router.get("/records/{record_id}")
def read_record(
    record_id: str,
    request: Request,
    x_tenant_id: str | None = Header(
        default=None,
    ),
) -> dict[str, Any]:
    claims = middleware_claims(request)

    tenant_id = enforce_tenant(
        request=request,
        claims=claims,
        requested_tenant=x_tenant_id,
    )

    connection = connect()

    row = connection.execute(
        """
        SELECT
            record_id,
            tenant_id,
            synthetic_subject,
            synthetic_value
        FROM synthetic_records
        WHERE record_id = ?
          AND tenant_id = ?
        """,
        (
            record_id,
            tenant_id,
        ),
    ).fetchone()

    connection.close()

    if row is None:
        record_denial(
            request=request,
            actor_user_id=str(claims["sub"]),
            authenticated_tenant=tenant_id,
            requested_tenant=
                x_tenant_id or tenant_id,
            resource_id=record_id,
            reason=
                "RESOURCE_OUTSIDE_AUTHENTICATED_TENANT_SCOPE",
        )

        raise HTTPException(
            status_code=404,
            detail="RESOURCE_NOT_FOUND",
        )

    return dict(row)


@router.put("/records/{record_id}")
def update_record(
    record_id: str,
    update: SyntheticUpdate,
    request: Request,
    x_tenant_id: str | None = Header(
        default=None,
    ),
) -> dict[str, Any]:
    claims = middleware_claims(request)

    tenant_id = enforce_tenant(
        request=request,
        claims=claims,
        requested_tenant=x_tenant_id,
    )

    connection = connect()

    cursor = connection.execute(
        """
        UPDATE synthetic_records
        SET synthetic_value = ?
        WHERE record_id = ?
          AND tenant_id = ?
        """,
        (
            update.synthetic_value,
            record_id,
            tenant_id,
        ),
    )

    if cursor.rowcount != 1:
        connection.rollback()
        connection.close()

        record_denial(
            request=request,
            actor_user_id=str(claims["sub"]),
            authenticated_tenant=tenant_id,
            requested_tenant=
                x_tenant_id or tenant_id,
            resource_id=record_id,
            reason=
                "CROSS_TENANT_UPDATE_DENIED",
        )

        raise HTTPException(
            status_code=404,
            detail="RESOURCE_NOT_FOUND",
        )

    connection.commit()
    connection.close()

    return {
        "status": "updated",
        "record_id": record_id,
        "tenant_id": tenant_id,
    }


@router.get("/audit/denied")
def denied_audit(
    request: Request,
) -> dict[str, Any]:
    claims = middleware_claims(request)

    if claims.get("role") != "security_auditor":
        record_denial(
            request=request,
            actor_user_id=str(claims["sub"]),
            authenticated_tenant=str(
                claims["tenant_id"]
            ),
            requested_tenant=str(
                claims["tenant_id"]
            ),
            resource_id="AUDIT-REGISTRY",
            reason=
                "SECURITY_AUDITOR_ROLE_REQUIRED",
        )

        raise HTTPException(
            status_code=403,
            detail=
                "SECURITY_AUDITOR_ROLE_REQUIRED",
        )

    connection = connect()

    rows = connection.execute(
        """
        SELECT *
        FROM denied_access_audit
        ORDER BY generated_at_utc
        """
    ).fetchall()

    connection.close()

    return {
        "count": len(rows),
        "events": [
            dict(row)
            for row in rows
        ],
    }
