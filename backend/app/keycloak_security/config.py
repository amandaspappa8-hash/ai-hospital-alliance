from __future__ import annotations

import os
from dataclasses import dataclass


def env_bool(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(
        name,
        str(default),
    )

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


@dataclass(frozen=True)
class KeycloakSettings:
    base_url: str
    realm: str
    issuer: str
    discovery_url: str
    audience: str | None
    verify_audience: bool
    allowed_algorithms: tuple[str, ...]
    timeout_seconds: float
    cache_seconds: int

    @classmethod
    def from_environment(
        cls,
    ) -> "KeycloakSettings":
        base_url = os.getenv(
            "KEYCLOAK_BASE_URL",
            "http://127.0.0.1:8081",
        ).rstrip("/")

        realm = os.getenv(
            "KEYCLOAK_REALM",
            "master",
        ).strip()

        if not realm:
            raise RuntimeError(
                "KEYCLOAK_REALM cannot be empty."
            )

        issuer = f"{base_url}/realms/{realm}"

        audience = (
            os.getenv("KEYCLOAK_AUDIENCE")
            or None
        )

        verify_audience = env_bool(
            "KEYCLOAK_VERIFY_AUDIENCE",
            False,
        )

        if verify_audience and not audience:
            raise RuntimeError(
                "KEYCLOAK_AUDIENCE is required "
                "when audience verification is enabled."
            )

        algorithms = tuple(
            item.strip()
            for item in os.getenv(
                "KEYCLOAK_ALLOWED_ALGORITHMS",
                "RS256",
            ).split(",")
            if item.strip()
        )

        if not algorithms:
            raise RuntimeError(
                "No allowed JWT algorithms configured."
            )

        return cls(
            base_url=base_url,
            realm=realm,
            issuer=issuer,
            discovery_url=(
                f"{issuer}/.well-known/"
                "openid-configuration"
            ),
            audience=audience,
            verify_audience=verify_audience,
            allowed_algorithms=algorithms,
            timeout_seconds=float(
                os.getenv(
                    "KEYCLOAK_HTTP_TIMEOUT_SECONDS",
                    "5",
                )
            ),
            cache_seconds=int(
                os.getenv(
                    "KEYCLOAK_JWKS_CACHE_SECONDS",
                    "300",
                )
            ),
        )
