from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class PostgresReportsRepository:
    """
    Read-only canonical reports repository.

    Security model:
      verified principal user id
        -> users.hospital_id
        -> hospitals.tenant_id

      report
        -> reports.patient_id
        -> patients.hospital_id
        -> hospitals.tenant_id

    The authenticated tenant claim must match the server-derived
    canonical tenant for the active principal.

    This repository performs no INSERT, UPDATE, or DELETE operations.
    """

    def __init__(self, engine: Engine):
        self._engine = engine

    @staticmethod
    def _validate_principal_user_id(
        principal_user_id: int,
    ) -> int:
        try:
            value = int(
                principal_user_id
            )
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "principal_user_id must be a positive integer"
            ) from exc

        if value <= 0:
            raise ValueError(
                "principal_user_id must be a positive integer"
            )

        return value

    @staticmethod
    def _validate_tenant_id(
        tenant_id: str,
    ) -> str:
        value = str(
            tenant_id or ""
        ).strip()

        if not value:
            raise ValueError(
                "tenant_id must be non-empty"
            )

        return value

    def _resolve_principal_scope(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> dict[str, str]:
        principal_id = (
            self._validate_principal_user_id(
                principal_user_id
            )
        )

        tenant_claim = (
            self._validate_tenant_id(
                tenant_id
            )
        )

        statement = text(
            """
            SELECT
                u.hospital_id AS hospital_id,
                h.tenant_id AS tenant_id
            FROM public.users AS u
            JOIN public.hospitals AS h
              ON h.id = u.hospital_id
            JOIN public.tenants AS t
              ON t.id = h.tenant_id
            WHERE u.id = :principal_user_id
              AND u.is_active IS TRUE
              AND h.tenant_id IS NOT NULL
            """
        )

        with self._engine.connect() as conn:
            row = conn.execute(
                statement,
                {
                    "principal_user_id":
                        principal_id,
                },
            ).mappings().one_or_none()

        if row is None:
            raise PermissionError(
                "Canonical principal scope unavailable"
            )

        derived_hospital = str(
            row["hospital_id"] or ""
        ).strip()

        derived_tenant = str(
            row["tenant_id"] or ""
        ).strip()

        if not derived_hospital:
            raise PermissionError(
                "Canonical principal hospital unavailable"
            )

        if (
            not derived_tenant
            or derived_tenant != tenant_claim
        ):
            raise PermissionError(
                "Authenticated tenant scope mismatch"
            )

        return {
            "hospital_id": derived_hospital,
            "tenant_id": derived_tenant,
        }

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        scope = (
            self._resolve_principal_scope(
                principal_user_id=
                    principal_user_id,
                tenant_id=tenant_id,
            )
        )

        statement = text(
            """
            SELECT
                r.id AS id,
                r.patient_id AS patient_id,
                COALESCE(r.title, '') AS title,
                COALESCE(r.type, '') AS type,
                COALESCE(r.status, '') AS status,
                COALESCE(r.body, '') AS body
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            ORDER BY
                r.created_at DESC NULLS LAST,
                r.id DESC
            """
        )

        with self._engine.connect() as conn:
            rows = conn.execute(
                statement,
                {
                    "hospital_id":
                        scope["hospital_id"],
                    "tenant_id":
                        scope["tenant_id"],
                },
            ).mappings().all()

        return [
            {
                "id": str(
                    row["id"]
                ),
                "patient_id": str(
                    row["patient_id"]
                ),
                "title": str(
                    row["title"] or ""
                ),
                "type": str(
                    row["type"] or ""
                ),
                "status": str(
                    row["status"] or ""
                ),
                "body": str(
                    row["body"] or ""
                ),
            }
            for row in rows
        ]
