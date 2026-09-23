from __future__ import annotations

from functools import lru_cache
import os

from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine


_REQUIRED_ENVIRONMENT = (
    "AIHA_CANONICAL_PG_HOST",
    "AIHA_CANONICAL_PG_PORT",
    "AIHA_CANONICAL_PG_DATABASE",
    "AIHA_CANONICAL_PG_USER",
    "AIHA_CANONICAL_PG_PASSWORD",
)

_CANONICAL_DATABASE = "aiha_db"


def validate_canonical_postgres_environment() -> dict[str, str]:
    """Validate the isolated canonical application PostgreSQL authority."""

    values: dict[str, str] = {}
    missing: list[str] = []

    for name in _REQUIRED_ENVIRONMENT:
        value = os.getenv(name)

        if value is None or value.strip() == "":
            missing.append(name)
            continue

        values[name] = value.strip()

    if missing:
        raise RuntimeError(
            "Missing canonical PostgreSQL runtime configuration: "
            + ", ".join(sorted(missing))
        )

    try:
        port = int(
            values["AIHA_CANONICAL_PG_PORT"]
        )
    except (TypeError, ValueError) as exc:
        raise RuntimeError(
            "AIHA_CANONICAL_PG_PORT must be an integer"
        ) from exc

    if not 1 <= port <= 65535:
        raise RuntimeError(
            "AIHA_CANONICAL_PG_PORT must be between 1 and 65535"
        )

    if (
        values["AIHA_CANONICAL_PG_DATABASE"]
        != _CANONICAL_DATABASE
    ):
        raise RuntimeError(
            "AIHA_CANONICAL_PG_DATABASE must equal aiha_db"
        )

    values["AIHA_CANONICAL_PG_PORT"] = str(port)

    return values


def build_canonical_postgres_url() -> URL:
    """Construct the isolated canonical PostgreSQL URL."""

    values = validate_canonical_postgres_environment()

    return URL.create(
        drivername="postgresql+psycopg2",
        username=values["AIHA_CANONICAL_PG_USER"],
        password=values["AIHA_CANONICAL_PG_PASSWORD"],
        host=values["AIHA_CANONICAL_PG_HOST"],
        port=int(
            values["AIHA_CANONICAL_PG_PORT"]
        ),
        database=values[
            "AIHA_CANONICAL_PG_DATABASE"
        ],
    )


@lru_cache(maxsize=1)
def get_canonical_postgres_engine() -> Engine:
    """Return the lazily constructed canonical PostgreSQL Engine."""

    return create_engine(
        build_canonical_postgres_url(),
        future=True,
        pool_pre_ping=True,
    )
