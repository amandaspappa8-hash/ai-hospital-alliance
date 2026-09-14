from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine

from backend.app.repositories.ophthalmology_repository import (
    OphthalmologyRepository,
)


class PostgresOphthalmologyRepository(
    OphthalmologyRepository
):
    """
    Canonical PostgreSQL Ophthalmology repository.

    Every operation is scoped through the authenticated principal's
    canonical user -> hospital -> tenant binding.
    """

    def __init__(
        self,
        engine: Engine,
    ) -> None:
        self.engine = engine

    @staticmethod
    def _parse_principal_user_id(
        principal_user_id: int | None,
    ) -> int:
        try:
            user_id = int(principal_user_id)
        except (TypeError, ValueError) as exc:
            raise PermissionError(
                "Authenticated principal is invalid"
            ) from exc

        if user_id <= 0:
            raise PermissionError(
                "Authenticated principal is invalid"
            )

        return user_id

    def _resolve_scope(
        self,
        connection: Connection,
        tenant_id: str | None,
        principal_user_id: int | None,
    ) -> dict[str, str]:
        user_id = self._parse_principal_user_id(
            principal_user_id
        )

        tenant_id = str(
            tenant_id or ""
        ).strip()

        if not tenant_id:
            raise PermissionError(
                "Tenant claim is required"
            )

        row = connection.execute(
            text(
                """
                SELECT
                    u.id AS user_id,
                    u.hospital_id,
                    h.tenant_id
                FROM public.users AS u
                JOIN public.hospitals AS h
                  ON h.id = u.hospital_id
                JOIN public.tenants AS t
                  ON t.id = h.tenant_id
                WHERE u.id = :user_id
                LIMIT 1
                """
            ),
            {
                "user_id": user_id,
            },
        ).mappings().first()

        if not row:
            raise PermissionError(
                "Authenticated principal is not bound to a tenant"
            )

        derived_tenant_id = str(
            row.get("tenant_id") or ""
        ).strip()

        if not derived_tenant_id:
            raise PermissionError(
                "Authenticated principal has no tenant"
            )

        if derived_tenant_id != tenant_id:
            raise PermissionError(
                "Tenant scope mismatch"
            )

        hospital_id = str(
            row.get("hospital_id") or ""
        ).strip()

        if not hospital_id:
            raise PermissionError(
                "Authenticated principal has no hospital"
            )

        return {
            "tenant_id": derived_tenant_id,
            "hospital_id": hospital_id,
            "user_id": str(user_id),
        }

    def list_analyses(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        a."analysis_id",\n                    a."case_id",\n                    a."patient_id",\n                    a."image_type",\n                    a."filename",\n                    a."width",\n                    a."height",\n                    a."mode",\n                    a."quality_score",\n                    a."brightness",\n                    a."contrast",\n                    a."sharpness",\n                    a."risk_score",\n                    a."risk_level",\n                    a."findings_json",\n                    a."recommendations_json",\n                    a."safety_gate",\n                    a."clinical_status",\n                    a."created_at"
                    FROM public.ophthalmology_ai_analyses AS a
                    WHERE a.tenant_id = :tenant_id
                      AND a.hospital_id = :hospital_id
                    ORDER BY a.created_at DESC
                    LIMIT 100
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                    "hospital_id": scope["hospital_id"],
                },
            ).mappings().all()

            return [
                dict(row)
                for row in rows
            ]

    def list_reports(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            (
                resolved_tenant_id,
                hospital_id,
                _principal_user_id,
            ) = self._resolve_scope(
                connection,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        r.report_id,
                        r.case_id,
                        r.patient_id,
                        r.report_type,
                        r.risk_score,
                        r.risk_level,
                        r.language,
                        r.created_at
                    FROM public.ophthalmology_reports AS r
                    WHERE r.tenant_id = :tenant_id
                      AND r.hospital_id = :hospital_id
                    ORDER BY r.created_at DESC
                    LIMIT 100
                    """
                ),
                {
                    "tenant_id": resolved_tenant_id,
                    "hospital_id": hospital_id,
                },
            ).mappings().all()

        return [
            dict(row)
            for row in rows
        ]

    def list_audit_logs(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            (
                resolved_tenant_id,
                hospital_id,
                _principal_user_id,
            ) = self._resolve_scope(
                connection,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        a.audit_id,
                        a.case_id,
                        a.action,
                        a.details,
                        a.created_at
                    FROM public.ophthalmology_audit_logs AS a
                    WHERE a.tenant_id = :tenant_id
                      AND a.hospital_id = :hospital_id
                    ORDER BY a.created_at DESC
                    LIMIT 100
                    """
                ),
                {
                    "tenant_id": resolved_tenant_id,
                    "hospital_id": hospital_id,
                },
            ).mappings().all()

        return [
            dict(row)
            for row in rows
        ]

    def list_cases(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        q: str = "",
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            (
                resolved_tenant_id,
                hospital_id,
                _principal_user_id,
            ) = self._resolve_scope(
                connection,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

            normalized_q = q.strip()

            if normalized_q:
                rows = connection.execute(
                    text(
                        """
                        SELECT
                            c.case_id,
                            c.patient_id,
                            c.filename,
                            c.stored_path,
                            c.image_type,
                            c.language,
                            c.risk_score,
                            c.risk_level,
                            c.status,
                            c.ai_summary,
                            c.clinical_notice,
                            c.doctor_review_status,
                            c.doctor_review_decision,
                            c.created_at,
                            c.updated_at
                        FROM public.ophthalmology_cases AS c
                        WHERE c.tenant_id = :tenant_id
                          AND c.hospital_id = :hospital_id
                          AND (
                              c.case_id ILIKE :pattern
                              OR c.patient_id ILIKE :pattern
                              OR c.image_type ILIKE :pattern
                              OR c.risk_level ILIKE :pattern
                          )
                        ORDER BY c.created_at DESC
                        LIMIT 100
                        """
                    ),
                    {
                        "tenant_id": resolved_tenant_id,
                        "hospital_id": hospital_id,
                        "pattern": f"%{normalized_q}%",
                    },
                ).mappings().all()
            else:
                rows = connection.execute(
                    text(
                        """
                        SELECT
                            c.case_id,
                            c.patient_id,
                            c.filename,
                            c.stored_path,
                            c.image_type,
                            c.language,
                            c.risk_score,
                            c.risk_level,
                            c.status,
                            c.ai_summary,
                            c.clinical_notice,
                            c.doctor_review_status,
                            c.doctor_review_decision,
                            c.created_at,
                            c.updated_at
                        FROM public.ophthalmology_cases AS c
                        WHERE c.tenant_id = :tenant_id
                          AND c.hospital_id = :hospital_id
                        ORDER BY c.created_at DESC
                        LIMIT 100
                        """
                    ),
                    {
                        "tenant_id": resolved_tenant_id,
                        "hospital_id": hospital_id,
                    },
                ).mappings().all()

        return [
            dict(row)
            for row in rows
        ]

    def get_case_detail(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        case_id: str,
    ) -> dict[str, Any] | None:
        with self.engine.connect() as connection:
            (
                resolved_tenant_id,
                hospital_id,
                _principal_user_id,
            ) = self._resolve_scope(
                connection,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

            case = connection.execute(
                text(
                    """
                    SELECT
                        c.case_id,
                        c.patient_id,
                        c.filename,
                        c.stored_path,
                        c.image_type,
                        c.language,
                        c.risk_score,
                        c.risk_level,
                        c.status,
                        c.ai_summary,
                        c.clinical_notice,
                        c.doctor_review_status,
                        c.doctor_review_decision,
                        c.created_at,
                        c.updated_at
                    FROM public.ophthalmology_cases AS c
                    WHERE c.tenant_id = :tenant_id
                      AND c.hospital_id = :hospital_id
                      AND c.case_id = :case_id
                    """
                ),
                {
                    "tenant_id": resolved_tenant_id,
                    "hospital_id": hospital_id,
                    "case_id": case_id,
                },
            ).mappings().first()

            if case is None:
                return None

            reports = connection.execute(
                text(
                    """
                    SELECT
                        r.report_id,
                        r.case_id,
                        r.patient_id,
                        r.report_type,
                        r.risk_score,
                        r.risk_level,
                        r.language,
                        r.created_at
                    FROM public.ophthalmology_reports AS r
                    WHERE r.tenant_id = :tenant_id
                      AND r.hospital_id = :hospital_id
                      AND r.case_id = :case_id
                    ORDER BY r.created_at DESC
                    """
                ),
                {
                    "tenant_id": resolved_tenant_id,
                    "hospital_id": hospital_id,
                    "case_id": case_id,
                },
            ).mappings().all()

            audit_logs = connection.execute(
                text(
                    """
                    SELECT
                        a.audit_id,
                        a.case_id,
                        a.action,
                        a.details,
                        a.created_at
                    FROM public.ophthalmology_audit_logs AS a
                    WHERE a.tenant_id = :tenant_id
                      AND a.hospital_id = :hospital_id
                      AND a.case_id = :case_id
                    ORDER BY a.created_at DESC
                    """
                ),
                {
                    "tenant_id": resolved_tenant_id,
                    "hospital_id": hospital_id,
                    "case_id": case_id,
                },
            ).mappings().all()

        return {
            "case": dict(case),
            "reports": [
                dict(row)
                for row in reports
            ],
            "audit_logs": [
                dict(row)
                for row in audit_logs
            ],
        }

    def get_analysis(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        analysis_id: str,
    ) -> dict[str, Any] | None:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    """
                    SELECT
                        a."analysis_id",
                        a."case_id",
                        a."patient_id",
                        a."image_type",
                        a."filename",
                        a."width",
                        a."height",
                        a."mode",
                        a."quality_score",
                        a."brightness",
                        a."contrast",
                        a."sharpness",
                        a."risk_score",
                        a."risk_level",
                        a."findings_json",
                        a."recommendations_json",
                        a."safety_gate",
                        a."clinical_status",
                        a."created_at"
                    FROM public.ophthalmology_ai_analyses AS a
                    WHERE a.tenant_id = :tenant_id
                      AND a.hospital_id = :hospital_id
                      AND a.analysis_id = :analysis_id
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                    "hospital_id": scope["hospital_id"],
                    "analysis_id": analysis_id,
                },
            ).mappings().first()

            if row is None:
                return None

            return dict(row)

    def get_annotation(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        annotation_id: str,
    ) -> dict[str, Any] | None:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    """
                    SELECT
                        a."annotation_id",
                        a."analysis_id",
                        a."case_id",
                        a."patient_id",
                        a."annotation_type",
                        a."shape",
                        a."x_percent",
                        a."y_percent",
                        a."width_percent",
                        a."height_percent",
                        a."marker_x_percent",
                        a."marker_y_percent",
                        a."severity",
                        a."doctor_note",
                        a."doctor_name",
                        a."status",
                        a."created_at",
                        a."updated_at"
                    FROM public.ophthalmology_annotations AS a
                    WHERE a.tenant_id = :tenant_id
                      AND a.hospital_id = :hospital_id
                      AND a.annotation_id = :annotation_id
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                    "hospital_id": scope["hospital_id"],
                    "annotation_id": annotation_id,
                },
            ).mappings().first()

            if row is None:
                return None

            return dict(row)

    def get_review(
        self,
        *,
        principal_user_id: int,
        tenant_id: str,
        review_id: str,
    ) -> dict[str, Any] | None:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    """
                    SELECT
                        r."review_id",
                        r."analysis_id",
                        r."case_id",
                        r."patient_id",
                        r."decision",
                        r."priority",
                        r."review_status",
                        r."doctor_name",
                        r."doctor_signature",
                        r."review_note",
                        r."follow_up_plan",
                        r."annotation_count",
                        r."ai_risk_score",
                        r."ai_risk_level",
                        r."safety_gate",
                        r."created_at",
                        r."updated_at"
                    FROM public.ophthalmology_clinical_reviews AS r
                    WHERE r.tenant_id = :tenant_id
                      AND r.hospital_id = :hospital_id
                      AND r.review_id = :review_id
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                    "hospital_id": scope["hospital_id"],
                    "review_id": review_id,
                },
            ).mappings().first()

            if row is None:
                return None

            return dict(row)
