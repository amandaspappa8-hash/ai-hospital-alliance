from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from backend.app.repositories.ophthalmology_repository import (
    OphthalmologyRepository,
)
from backend.app.repositories.postgres.ophthalmology_repository import (
    PostgresOphthalmologyRepository,
)


class OphthalmologyService:
    """Ophthalmology application service boundary."""

    def __init__(
        self,
        repository: OphthalmologyRepository,
    ) -> None:
        self._repository = repository

    def list_analyses(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        return self._repository.list_analyses(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
        )

    def list_reports(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        return self.repository.list_reports(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
        )

    def list_audit_logs(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        return self.repository.list_audit_logs(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
        )

    def list_cases(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        q: str = "",
    ) -> list[dict[str, Any]]:
        return self.repository.list_cases(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
            q=q,
        )

    def get_case_detail(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        case_id: str,
    ) -> dict[str, Any] | None:
        return self.repository.get_case_detail(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
            case_id=case_id,
        )

    def get_analysis(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        analysis_id: str,
    ) -> dict[str, Any] | None:
        return self.repository.get_analysis(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
            analysis_id=analysis_id,
        )

    def get_annotation(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        annotation_id: str,
    ) -> dict[str, Any] | None:
        return self.repository.get_annotation(
            principal_user_id=principal_user_id,
            tenant_id=tenant_id,
            annotation_id=annotation_id,
        )


def get_ophthalmology_repository_mode() -> str:
    mode = os.getenv(
        "AIHA_OPHTHALMOLOGY_REPOSITORY",
        "sqlite",
    ).strip().lower()

    if mode not in {
        "sqlite",
        "postgres",
    }:
        raise RuntimeError(
            "Invalid AIHA_OPHTHALMOLOGY_REPOSITORY. "
            "Expected 'sqlite' or 'postgres'."
        )

    return mode


@lru_cache(maxsize=1)
def get_postgres_ophthalmology_service() -> OphthalmologyService:
    names = {
        "host": "AIHA_OPHTHALMOLOGY_PG_HOST",
        "port": "AIHA_OPHTHALMOLOGY_PG_PORT",
        "database": "AIHA_OPHTHALMOLOGY_PG_DATABASE",
        "username": "AIHA_OPHTHALMOLOGY_PG_USER",
        "password": "AIHA_OPHTHALMOLOGY_PG_PASSWORD",
    }

    values = {
        key: os.getenv(
            env_name,
            "",
        ).strip()
        for key, env_name in names.items()
    }

    missing = [
        names[key]
        for key, value in values.items()
        if not value
    ]

    if missing:
        raise RuntimeError(
            "Missing PostgreSQL Ophthalmology configuration: "
            + ", ".join(missing)
        )

    try:
        port = int(values["port"])
    except ValueError as exc:
        raise RuntimeError(
            "AIHA_OPHTHALMOLOGY_PG_PORT must be an integer"
        ) from exc

    url = URL.create(
        drivername="postgresql+psycopg2",
        username=values["username"],
        password=values["password"],
        host=values["host"],
        port=port,
        database=values["database"],
    )

    engine = create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        pool_recycle=3600,
    )

    return OphthalmologyService(
        PostgresOphthalmologyRepository(
            engine
        )
    )
