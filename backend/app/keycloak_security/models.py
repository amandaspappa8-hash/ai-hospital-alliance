from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuthenticatedIdentity:
    subject: str
    username: str
    email: str | None
    issuer: str
    audience: tuple[str, ...]
    realm_roles: frozenset[str]
    client_roles: dict[str, frozenset[str]]
    claims: dict[str, Any]

    def all_roles(
        self,
    ) -> frozenset[str]:
        roles = set(self.realm_roles)

        for client_role_set in (
            self.client_roles.values()
        ):
            roles.update(client_role_set)

        return frozenset(roles)

    def has_role(
        self,
        role: str,
    ) -> bool:
        return role in self.all_roles()
