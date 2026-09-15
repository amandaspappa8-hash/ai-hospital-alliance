from __future__ import annotations

import secrets
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


class PostgresReportsRepository:
    """
    Canonical PostgreSQL Reports repository.

    Security authority:

      verified authenticated principal
        -> public.users.id
        -> public.users.hospital_id
        -> public.hospitals.tenant_id

      report patient
        -> public.patients.id
        -> public.patients.hospital_id
        -> public.hospitals.tenant_id

    The authenticated tenant claim must match the server-derived
    canonical tenant for the active principal.

    Writes authorize the principal, authorize the patient, and perform
    the INSERT using one PostgreSQL transaction.
    """

    _REPORT_ID_ATTEMPTS = 5

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

    @staticmethod
    def _validate_patient_id(
        patient_id: str,
    ) -> str:
        value = str(
            patient_id or ""
        ).strip()

        if not value:
            raise ValueError(
                "patient_id must be non-empty"
            )

        return value

    def _resolve_principal_scope_on_connection(
        self,
        connection,
        *,
        principal_user_id: int,
        tenant_id: str,
        lock_scope: bool = False,
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

        statement_sql = """
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

        if lock_scope:
            statement_sql += (
                "\n            FOR SHARE OF u, h"
            )

        statement = text(
            statement_sql
        )

        row = connection.execute(
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

    def _resolve_principal_scope(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> dict[str, str]:
        with self._engine.connect() as connection:
            return (
                self._resolve_principal_scope_on_connection(
                    connection,
                    principal_user_id=
                        principal_user_id,
                    tenant_id=tenant_id,
                )
            )

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

        with self._engine.connect() as connection:
            rows = connection.execute(
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

    def create_for_principal(
        self,
        *,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        title: str,
        report_type: str,
        summary: str,
        content: str,
        status: str,
    ) -> dict[str, Any]:
        patient = self._validate_patient_id(
            patient_id
        )

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

        title_value = str(
            title or ""
        )

        type_value = str(
            report_type
            or "Clinical Report"
        )

        summary_value = str(
            summary or ""
        )

        content_value = str(
            content or ""
        )

        status_value = str(
            status or "Draft"
        )

        patient_statement = text(
            """
            SELECT 1
            FROM public.patients AS p
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE p.id = :patient_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF p, h
            """
        )

        insert_statement = text(
            """
            INSERT INTO public.reports (
                id,
                patient_id,
                author_id,
                title,
                type,
                status,
                body,
                summary
            )
            VALUES (
                :id,
                :patient_id,
                :author_id,
                :title,
                :type,
                :status,
                :body,
                :summary
            )
            ON CONFLICT (id) DO NOTHING
            RETURNING
                id,
                patient_id,
                title,
                type,
                status,
                body,
                summary
            """
        )

        try:
            with self._engine.begin() as connection:
                scope = (
                    self._resolve_principal_scope_on_connection(
                        connection,
                        principal_user_id=
                            principal_id,
                        tenant_id=
                            tenant_claim,
                        lock_scope=True,
                    )
                )

                allowed = connection.execute(
                    patient_statement,
                    {
                        "patient_id":
                            patient,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).scalar_one_or_none()

                if allowed is None:
                    raise PermissionError(
                        "Patient is outside authenticated "
                        "hospital/tenant scope"
                    )

                for _ in range(
                    self._REPORT_ID_ATTEMPTS
                ):
                    report_id = (
                        "R-"
                        + secrets.token_urlsafe(13)
                    )

                    row = connection.execute(
                        insert_statement,
                        {
                            "id":
                                report_id,
                            "patient_id":
                                patient,
                            "author_id":
                                principal_id,
                            "title":
                                title_value,
                            "type":
                                type_value,
                            "status":
                                status_value,
                            "body":
                                content_value,
                            "summary":
                                summary_value,
                        },
                    ).mappings().one_or_none()

                    if row is None:
                        continue

                    return {
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
                        "summary": str(
                            row["summary"] or ""
                        ),
                        "content": str(
                            row["body"] or ""
                        ),
                        "status": str(
                            row["status"] or ""
                        ),
                    }

                raise RuntimeError(
                    "Unable to allocate unique report id"
                )

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc
