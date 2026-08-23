from __future__ import annotations

import threading
import time
from typing import Any

import httpx
from jose import JWTError, jwt

from .config import KeycloakSettings
from .models import AuthenticatedIdentity


class TokenValidationError(Exception):
    """Fail-closed token validation error."""


class KeycloakJWTValidator:
    def __init__(
        self,
        settings: KeycloakSettings | None = None,
    ) -> None:
        self.settings = (
            settings
            or KeycloakSettings.from_environment()
        )

        self._lock = threading.RLock()
        self._discovery: dict[str, Any] = {}
        self._jwks: dict[str, Any] = {}
        self._expires_at = 0.0

    def _get_json(
        self,
        url: str,
    ) -> dict[str, Any]:
        try:
            response = httpx.get(
                url,
                timeout=self.settings.timeout_seconds,
                follow_redirects=False,
            )

            response.raise_for_status()
            payload = response.json()

        except (
            httpx.HTTPError,
            ValueError,
        ) as exc:
            raise TokenValidationError(
                "Unable to retrieve identity-provider "
                "metadata."
            ) from exc

        if not isinstance(payload, dict):
            raise TokenValidationError(
                "Identity-provider response is invalid."
            )

        return payload

    def refresh(
        self,
        force: bool = False,
    ) -> None:
        with self._lock:
            now = time.monotonic()

            if (
                not force
                and self._jwks
                and now < self._expires_at
            ):
                return

            discovery = self._get_json(
                self.settings.discovery_url
            )

            if (
                discovery.get("issuer")
                != self.settings.issuer
            ):
                raise TokenValidationError(
                    "OIDC issuer mismatch."
                )

            jwks_uri = discovery.get("jwks_uri")

            if not isinstance(
                jwks_uri,
                str,
            ) or not jwks_uri:
                raise TokenValidationError(
                    "OIDC discovery has no jwks_uri."
                )

            jwks = self._get_json(jwks_uri)

            if not jwks.get("keys"):
                raise TokenValidationError(
                    "JWKS contains no keys."
                )

            self._discovery = discovery
            self._jwks = jwks
            self._expires_at = (
                now + self.settings.cache_seconds
            )

    def metadata_status(
        self,
    ) -> dict[str, Any]:
        self.refresh()

        signing_keys = [
            key
            for key in self._jwks.get("keys", [])
            if key.get("use") == "sig"
        ]

        return {
            "issuer": self.settings.issuer,
            "realm": self.settings.realm,
            "jwks_uri": self._discovery.get(
                "jwks_uri"
            ),
            "total_keys": len(
                self._jwks.get("keys", [])
            ),
            "signing_keys": len(signing_keys),
            "allowed_algorithms": list(
                self.settings.allowed_algorithms
            ),
            "audience_validation_enabled": (
                self.settings.verify_audience
            ),
            "audience": self.settings.audience,
        }

    def _select_key(
        self,
        token: str,
    ) -> dict[str, Any]:
        try:
            header = jwt.get_unverified_header(
                token
            )
        except JWTError as exc:
            raise TokenValidationError(
                "Malformed JWT header."
            ) from exc

        algorithm = header.get("alg")
        key_id = header.get("kid")

        if algorithm not in (
            self.settings.allowed_algorithms
        ):
            raise TokenValidationError(
                "JWT algorithm is not allowed."
            )

        if not key_id:
            raise TokenValidationError(
                "JWT has no key identifier."
            )

        self.refresh()

        for key in self._jwks.get("keys", []):
            if (
                key.get("kid") == key_id
                and key.get("use") == "sig"
                and key.get("alg") == algorithm
            ):
                return key

        self.refresh(force=True)

        for key in self._jwks.get("keys", []):
            if (
                key.get("kid") == key_id
                and key.get("use") == "sig"
                and key.get("alg") == algorithm
            ):
                return key

        raise TokenValidationError(
            "Matching signing key was not found."
        )

    def validate(
        self,
        token: str,
    ) -> AuthenticatedIdentity:
        if not token or not token.strip():
            raise TokenValidationError(
                "Bearer token is empty."
            )

        key = self._select_key(token)

        options = {
            "verify_signature": True,
            "verify_exp": True,
            "verify_nbf": True,
            "verify_iss": True,
            "verify_aud": (
                self.settings.verify_audience
            ),
            "require_exp": True,
            "require_iss": True,
            "require_sub": True,
        }

        arguments: dict[str, Any] = {
            "token": token,
            "key": key,
            "algorithms": list(
                self.settings.allowed_algorithms
            ),
            "issuer": self.settings.issuer,
            "options": options,
        }

        if self.settings.verify_audience:
            arguments["audience"] = (
                self.settings.audience
            )

        try:
            claims = jwt.decode(**arguments)
        except JWTError as exc:
            raise TokenValidationError(
                "JWT signature or claim validation "
                "failed."
            ) from exc

        subject = claims.get("sub")

        if not subject:
            raise TokenValidationError(
                "Validated JWT has no subject."
            )

        realm_access = claims.get(
            "realm_access",
            {},
        )

        realm_roles = frozenset(
            role
            for role in realm_access.get(
                "roles",
                [],
            )
            if isinstance(role, str)
        )

        client_roles: dict[
            str,
            frozenset[str],
        ] = {}

        resource_access = claims.get(
            "resource_access",
            {},
        )

        if isinstance(resource_access, dict):
            for client, content in (
                resource_access.items()
            ):
                if not isinstance(content, dict):
                    continue

                client_roles[client] = frozenset(
                    role
                    for role in content.get(
                        "roles",
                        [],
                    )
                    if isinstance(role, str)
                )

        raw_audience = claims.get("aud", [])

        if isinstance(raw_audience, str):
            audience = (raw_audience,)
        elif isinstance(raw_audience, list):
            audience = tuple(
                item
                for item in raw_audience
                if isinstance(item, str)
            )
        else:
            audience = ()

        username = (
            claims.get("preferred_username")
            or claims.get("email")
            or subject
        )

        return AuthenticatedIdentity(
            subject=str(subject),
            username=str(username),
            email=claims.get("email"),
            issuer=str(claims["iss"]),
            audience=audience,
            realm_roles=realm_roles,
            client_roles=client_roles,
            claims=claims,
        )
