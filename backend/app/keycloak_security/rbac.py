"""Role-based authorization dependencies for AHOS."""

from __future__ import annotations

from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from .dependencies import (
    get_authenticated_identity,
)
from .models import AuthenticatedIdentity


def require_any_role(
    *required_roles: str,
) -> Callable:
    normalized_roles = frozenset(
        role.strip()
        for role in required_roles
        if role.strip()
    )

    if not normalized_roles:
        raise ValueError(
            "At least one required role must be defined."
        )

    async def dependency(
        identity: AuthenticatedIdentity = Depends(
            get_authenticated_identity
        ),
    ) -> AuthenticatedIdentity:
        available_roles = identity.all_roles()

        if normalized_roles.isdisjoint(
            available_roles
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Authenticated identity does not "
                    "have the required role."
                ),
                headers={
                    "Cache-Control": "no-store",
                },
            )

        return identity

    return dependency
