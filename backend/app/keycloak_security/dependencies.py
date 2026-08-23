"""FastAPI authentication dependencies for AHOS Keycloak."""

from __future__ import annotations

from functools import lru_cache

from fastapi import HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from .jwt_validator import (
    KeycloakJWTValidator,
    TokenValidationError,
)
from .models import AuthenticatedIdentity


bearer_scheme = HTTPBearer(
    auto_error=False,
    scheme_name="KeycloakBearer",
    description=(
        "Keycloak-issued OAuth2 access token."
    ),
)


@lru_cache(maxsize=1)
def get_keycloak_validator(
) -> KeycloakJWTValidator:
    return KeycloakJWTValidator()


def _unauthorized(
    detail: str = "Authentication required.",
) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={
            "WWW-Authenticate": "Bearer",
            "Cache-Control": "no-store",
        },
    )


async def get_authenticated_identity(
    request: Request,
    credentials: (
        HTTPAuthorizationCredentials | None
    ) = None,
) -> AuthenticatedIdentity:
    """
    Validate a Keycloak bearer token and return its
    normalized authenticated identity.

    Tokens and raw claims are never written to logs here.
    """

    if credentials is None:
        credentials = await bearer_scheme(request)

    if credentials is None:
        raise _unauthorized()

    if credentials.scheme.lower() != "bearer":
        raise _unauthorized(
            "Bearer authentication is required."
        )

    token = credentials.credentials.strip()

    if not token:
        raise _unauthorized(
            "Bearer token is empty."
        )

    validator = get_keycloak_validator()

    try:
        identity = validator.validate(token)

    except TokenValidationError:
        # Do not expose internal signature, issuer,
        # algorithm, or JWKS validation details.
        raise _unauthorized(
            "Invalid or expired access token."
        ) from None

    request.state.authenticated_identity = identity

    return identity
