from __future__ import annotations

from typing import Any

from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine

from backend.app.repositories.contracts.users_repository import (
    UsersRepositoryContract,
)


class PostgresUsersRepository(UsersRepositoryContract):
    """Read-only canonical users repository backed by public.users."""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        engine: Engine | None = None,
    ) -> None:
        if engine is not None:
            self._engine = engine
            return

        url = URL.create(
            drivername="postgresql+psycopg2",
            username=user,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        self._engine = create_engine(
            url,
            pool_pre_ping=True,
            future=True,
        )

    def get_by_username(self, username: str) -> dict | None:
        """Return one canonical user with trusted hospital/tenant scope.

        The tenant authority is resolved only through:
        users.hospital_id -> hospitals.tenant_id -> tenants.id.

        INNER JOIN semantics intentionally fail closed when hospital or
        tenant scope is unresolved.
        """
        query = text(
            """
            SELECT
                u.id,
                u.username,
                u.password,
                u.name,
                u.role,
                u.hospital_id,
                h.tenant_id,
                u.is_active
            FROM public.users AS u
            JOIN public.hospitals AS h
              ON h.id = u.hospital_id
            JOIN public.tenants AS t
              ON t.id = h.tenant_id
            WHERE u.username = :username
            """
        )

        with self._engine.connect() as connection:
            rows = (
                connection.execute(
                    query,
                    {"username": username},
                )
                .mappings()
                .all()
            )

        if not rows:
            return None

        if len(rows) != 1:
            raise RuntimeError(
                "Canonical username authority is not unique"
            )

        row = rows[0]

        tenant_id = row.get("tenant_id")

        if not tenant_id:
            return None

        return {
            "id": row.get("id"),
            "username": row.get("username"),
            "password": row.get("password"),
            "name": row.get("name"),
            "role": row.get("role"),
            "hospital_id": row.get("hospital_id"),
            "tenant_id": tenant_id,
            "is_active": row.get("is_active"),
        }
