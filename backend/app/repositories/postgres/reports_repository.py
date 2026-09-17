from __future__ import annotations

from collections.abc import Callable

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

    @staticmethod
    def _validate_report_id(
        report_id: str,
    ) -> str:
        value = str(
            report_id or ""
        ).strip()

        if not value:
            raise ValueError(
                "report_id must be non-empty"
            )

        if len(value) > 20:
            raise ValueError(
                "report_id exceeds canonical VARCHAR(20)"
            )

        return value

    def register_verification_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]:
        report = (
            self._validate_report_id(
                report_id
            )
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

        report_scope_statement = text(
            """
            SELECT 1
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        insert_statement = text(
            """
            INSERT INTO public.report_verification_events (
                report_id,
                verification_type,
                status,
                verified_by_user_id
            )
            VALUES (
                :report_id,
                'REGISTRATION',
                'REGISTERED',
                :verified_by_user_id
            )
            ON CONFLICT (
                report_id,
                verification_type
            )
            DO NOTHING
            RETURNING
                id,
                report_id,
                verification_type,
                status,
                verified_by_user_id,
                verified_at
            """
        )

        existing_statement = text(
            """
            SELECT
                id,
                report_id,
                verification_type,
                status,
                verified_by_user_id,
                verified_at
            FROM public.report_verification_events
            WHERE report_id = :report_id
              AND verification_type = 'REGISTRATION'
            LIMIT 1
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
                    report_scope_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).scalar_one_or_none()

                if allowed is None:
                    raise PermissionError(
                        "Report is outside authenticated "
                        "hospital/tenant scope"
                    )

                row = connection.execute(
                    insert_statement,
                    {
                        "report_id":
                            report,
                        "verified_by_user_id":
                            principal_id,
                    },
                ).mappings().one_or_none()

                if row is None:
                    row = connection.execute(
                        existing_statement,
                        {
                            "report_id":
                                report,
                        },
                    ).mappings().one_or_none()

                if row is None:
                    raise RuntimeError(
                        "Canonical report verification "
                        "registration unavailable"
                    )

                return {
                    "id": int(
                        row["id"]
                    ),
                    "report_id": str(
                        row["report_id"]
                    ),
                    "verification_type": str(
                        row["verification_type"]
                    ),
                    "status": str(
                        row["status"]
                    ),
                    "verified_by_user_id": int(
                        row[
                            "verified_by_user_id"
                        ]
                    ),
                    "verified_at":
                        row["verified_at"],
                }

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc

    def get_verification_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        report = (
            self._validate_report_id(
                report_id
            )
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

        report_scope_statement = text(
            """
            SELECT 1
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        event_statement = text(
            """
            SELECT
                id,
                report_id,
                verification_type,
                status,
                verified_by_user_id,
                verified_at
            FROM public.report_verification_events
            WHERE report_id = :report_id
              AND verification_type = 'REGISTRATION'
            LIMIT 1
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
                    report_scope_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).scalar_one_or_none()

                if allowed is None:
                    raise PermissionError(
                        "Report is outside authenticated "
                        "hospital/tenant scope"
                    )

                row = connection.execute(
                    event_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one_or_none()

                if row is None:
                    return None

                return {
                    "id": int(
                        row["id"]
                    ),
                    "report_id": str(
                        row["report_id"]
                    ),
                    "verification_type": str(
                        row["verification_type"]
                    ),
                    "status": str(
                        row["status"]
                    ),
                    "verified_by_user_id": int(
                        row[
                            "verified_by_user_id"
                        ]
                    ),
                    "verified_at":
                        row["verified_at"],
                }

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc


    @staticmethod
    def _canonical_report_digest(
        row,
    ) -> str:
        import hashlib
        import json

        canonical = {
            "report_id":
                row["report_id"],
            "patient_id":
                row["patient_id"],
            "author_id":
                row["author_id"],
            "title":
                row["title"],
            "type":
                row["type"],
            "status":
                row["status"],
            "body":
                row["body"],
            "summary":
                row["summary"],
        }

        serialized = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        return hashlib.sha256(
            serialized
        ).hexdigest()

    def register_content_digest_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]:
        report = (
            self._validate_report_id(
                report_id
            )
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

        report_statement = text(
            """
            SELECT
                r.id AS report_id,
                r.patient_id AS patient_id,
                r.author_id AS author_id,
                r.title AS title,
                r.type AS type,
                r.status AS status,
                r.body AS body,
                r.summary AS summary
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        existing_statement = text(
            """
            SELECT
                id,
                report_id,
                canonicalization_version,
                digest_algorithm,
                digest_hex,
                secured_by_user_id,
                secured_at
            FROM public.report_content_digests
            WHERE report_id = :report_id
              AND canonicalization_version =
                    'AIHA_REPORT_DIGEST_V1'
            LIMIT 1
            """
        )

        insert_statement = text(
            """
            INSERT INTO public.report_content_digests (
                report_id,
                canonicalization_version,
                digest_algorithm,
                digest_hex,
                secured_by_user_id
            )
            VALUES (
                :report_id,
                'AIHA_REPORT_DIGEST_V1',
                'SHA-256',
                :digest_hex,
                :secured_by_user_id
            )
            ON CONFLICT (
                report_id,
                canonicalization_version
            )
            DO NOTHING
            RETURNING
                id,
                report_id,
                canonicalization_version,
                digest_algorithm,
                digest_hex,
                secured_by_user_id,
                secured_at
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

                report_row = connection.execute(
                    report_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).mappings().one_or_none()

                if report_row is None:
                    raise PermissionError(
                        "Report is outside authenticated "
                        "hospital/tenant scope"
                    )

                digest_hex = (
                    self._canonical_report_digest(
                        report_row
                    )
                )

                existing = connection.execute(
                    existing_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one_or_none()

                if existing is not None:
                    if str(
                        existing["digest_hex"]
                    ) != digest_hex:
                        raise FileExistsError(
                            "Canonical report content "
                            "digest baseline conflict"
                        )

                    return {
                        "id": int(
                            existing["id"]
                        ),
                        "report_id": str(
                            existing["report_id"]
                        ),
                        "canonicalization_version":
                            str(
                                existing[
                                    "canonicalization_version"
                                ]
                            ),
                        "digest_algorithm": str(
                            existing[
                                "digest_algorithm"
                            ]
                        ),
                        "digest_hex": str(
                            existing["digest_hex"]
                        ),
                        "secured_by_user_id": int(
                            existing[
                                "secured_by_user_id"
                            ]
                        ),
                        "secured_at":
                            existing["secured_at"],
                    }

                row = connection.execute(
                    insert_statement,
                    {
                        "report_id":
                            report,
                        "digest_hex":
                            digest_hex,
                        "secured_by_user_id":
                            principal_id,
                    },
                ).mappings().one_or_none()

                if row is None:
                    row = connection.execute(
                        existing_statement,
                        {
                            "report_id":
                                report,
                        },
                    ).mappings().one_or_none()

                if row is None:
                    raise RuntimeError(
                        "Canonical report content "
                        "digest registration unavailable"
                    )

                if str(
                    row["digest_hex"]
                ) != digest_hex:
                    raise FileExistsError(
                        "Canonical report content "
                        "digest baseline conflict"
                    )

                return {
                    "id": int(
                        row["id"]
                    ),
                    "report_id": str(
                        row["report_id"]
                    ),
                    "canonicalization_version":
                        str(
                            row[
                                "canonicalization_version"
                            ]
                        ),
                    "digest_algorithm": str(
                        row["digest_algorithm"]
                    ),
                    "digest_hex": str(
                        row["digest_hex"]
                    ),
                    "secured_by_user_id": int(
                        row[
                            "secured_by_user_id"
                        ]
                    ),
                    "secured_at":
                        row["secured_at"],
                }

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc

    def verify_content_digest_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        import hmac

        report = (
            self._validate_report_id(
                report_id
            )
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

        report_statement = text(
            """
            SELECT
                r.id AS report_id,
                r.patient_id AS patient_id,
                r.author_id AS author_id,
                r.title AS title,
                r.type AS type,
                r.status AS status,
                r.body AS body,
                r.summary AS summary
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        digest_statement = text(
            """
            SELECT
                id,
                report_id,
                canonicalization_version,
                digest_algorithm,
                digest_hex,
                secured_by_user_id,
                secured_at
            FROM public.report_content_digests
            WHERE report_id = :report_id
              AND canonicalization_version =
                    'AIHA_REPORT_DIGEST_V1'
            LIMIT 1
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
                    )
                )

                report_row = connection.execute(
                    report_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).mappings().one_or_none()

                if report_row is None:
                    raise PermissionError(
                        "Report is outside authenticated "
                        "hospital/tenant scope"
                    )

                baseline = connection.execute(
                    digest_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one_or_none()

                if baseline is None:
                    return None

                current_digest = (
                    self._canonical_report_digest(
                        report_row
                    )
                )

                stored_digest = str(
                    baseline["digest_hex"]
                )

                matches = hmac.compare_digest(
                    stored_digest,
                    current_digest,
                )

                return {
                    "id": int(
                        baseline["id"]
                    ),
                    "report_id": str(
                        baseline["report_id"]
                    ),
                    "canonicalization_version":
                        str(
                            baseline[
                                "canonicalization_version"
                            ]
                        ),
                    "digest_algorithm": str(
                        baseline[
                            "digest_algorithm"
                        ]
                    ),
                    "stored_digest":
                        stored_digest,
                    "current_digest":
                        current_digest,
                    "matches":
                        bool(matches),
                    "secured_by_user_id": int(
                        baseline[
                            "secured_by_user_id"
                        ]
                    ),
                    "secured_at":
                        baseline["secured_at"],
                }

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc

    @staticmethod
    def _canonical_report_mac(
        row,
        mac_key: bytes,
    ) -> str:
        import hashlib
        import hmac
        import json

        if (
            not isinstance(mac_key, bytes)
            or not mac_key
        ):
            raise RuntimeError(
                "Report MAC key unavailable"
            )

        canonical = {
            "mac_version":
                "AIHA_REPORT_CONTENT_MAC_V1",
            "report_id":
                row["report_id"],
            "patient_id":
                row["patient_id"],
            "author_id":
                row["author_id"],
            "title":
                row["title"],
            "type":
                row["type"],
            "status":
                row["status"],
            "body":
                row["body"],
            "summary":
                row["summary"],
        }

        serialized = json.dumps(
            canonical,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        return hmac.new(
            mac_key,
            serialized,
            hashlib.sha256,
        ).hexdigest()

    def register_content_mac_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
        active_key_id: str,
        mac_key_resolver: Callable[[str], bytes],
    ) -> dict[str, Any]:
        import hmac
        import re

        if (
            not isinstance(active_key_id, str)
            or re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9._:-]{0,63}",
                active_key_id,
            )
            is None
        ):
            raise RuntimeError(
                "Report MAC active key identity unavailable"
            )

        if not callable(mac_key_resolver):
            raise RuntimeError(
                "Report MAC key resolver unavailable"
            )

        from ..contracts.reports_repository import (
            ReportContentMacConflictError,
        )

        report = self._validate_report_id(
            report_id
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


        report_statement = text(
            """
            SELECT
                r.id AS report_id,
                r.patient_id AS patient_id,
                r.author_id AS author_id,
                r.title AS title,
                r.type AS type,
                r.status AS status,
                r.body AS body,
                r.summary AS summary
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        baseline_statement = text(
            """
            SELECT
                id,
                report_id,
                mac_version,
                mac_algorithm,
                mac_hex,
                key_id,
                created_by_user_id,
                created_at
            FROM public.report_content_macs
            WHERE report_id = :report_id
              AND mac_version =
                    'AIHA_REPORT_CONTENT_MAC_V1'
            LIMIT 1
            FOR UPDATE
            """
        )

        insert_statement = text(
            """
            INSERT INTO public.report_content_macs (
                report_id,
                mac_version,
                mac_algorithm,
                mac_hex,
                key_id,
                created_by_user_id
            )
            VALUES (
                :report_id,
                'AIHA_REPORT_CONTENT_MAC_V1',
                'HMAC-SHA256',
                :mac_hex,
                :key_id,
                :created_by_user_id
            )
            ON CONFLICT (
                report_id,
                mac_version
            )
            DO NOTHING
            RETURNING
                id,
                report_id,
                mac_version,
                mac_algorithm,
                mac_hex,
                key_id,
                created_by_user_id,
                created_at
            """
        )

        def result_from_row(row):
            return {
                "id":
                    int(row["id"]),
                "report_id":
                    str(row["report_id"]),
                "mac_version":
                    str(row["mac_version"]),
                "mac_algorithm":
                    str(row["mac_algorithm"]),
                "mac_hex":
                    str(row["mac_hex"]),
                "key_id":
                    str(row["key_id"]),
                "created_by_user_id":
                    int(
                        row[
                            "created_by_user_id"
                        ]
                    ),
                "created_at":
                    row["created_at"],
            }

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

                report_row = connection.execute(
                    report_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).mappings().one_or_none()

                if report_row is None:
                    raise PermissionError(
                        "Report outside principal scope"
                    )


                baseline = connection.execute(
                    baseline_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one_or_none()

                if baseline is not None:

                    baseline_key_id = str(
                        baseline["key_id"]
                    )
                    baseline_mac_key = (
                        mac_key_resolver(
                            baseline_key_id
                        )
                    )
                    current_mac = (
                        self._canonical_report_mac(
                            report_row,
                            baseline_mac_key,
                        )
                    )

                    stored_mac = str(
                        baseline["mac_hex"]
                    )

                    if hmac.compare_digest(
                        stored_mac,
                        current_mac,
                    ):
                        return result_from_row(
                            baseline
                        )

                    raise (
                        ReportContentMacConflictError(
                            "Immutable report content "
                            "MAC baseline conflict"
                        )
                    )

                active_mac_key = (
                    mac_key_resolver(
                        active_key_id
                    )
                )
                current_mac = (
                    self._canonical_report_mac(
                        report_row,
                        active_mac_key,
                    )
                )

                inserted = connection.execute(
                    insert_statement,
                    {
                        "report_id":
                            report,
                        "mac_hex":
                            current_mac,
                        "key_id":
                            active_key_id,
                        "created_by_user_id":
                            principal_id,
                    },
                ).mappings().one_or_none()

                if inserted is not None:
                    return result_from_row(
                        inserted
                    )

                baseline = connection.execute(
                    baseline_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one()

                baseline_key_id = str(
                    baseline["key_id"]
                )
                baseline_mac_key = (
                    mac_key_resolver(
                        baseline_key_id
                    )
                )
                current_mac = (
                    self._canonical_report_mac(
                        report_row,
                        baseline_mac_key,
                    )
                )

                if hmac.compare_digest(
                    str(baseline["mac_hex"]),
                    current_mac,
                ):
                    return result_from_row(
                        baseline
                    )

                raise (
                    ReportContentMacConflictError(
                        "Immutable report content "
                        "MAC baseline conflict"
                    )
                )

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc

    def verify_content_mac_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
        mac_key_resolver: Callable[[str], bytes],
    ) -> dict[str, Any] | None:
        import hmac

        if not callable(mac_key_resolver):
            raise RuntimeError(
                "Report MAC key resolver unavailable"
            )

        report = self._validate_report_id(
            report_id
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


        report_statement = text(
            """
            SELECT
                r.id AS report_id,
                r.patient_id AS patient_id,
                r.author_id AS author_id,
                r.title AS title,
                r.type AS type,
                r.status AS status,
                r.body AS body,
                r.summary AS summary
            FROM public.reports AS r
            JOIN public.patients AS p
              ON p.id = r.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE r.id = :report_id
              AND p.hospital_id = :hospital_id
              AND h.tenant_id = :tenant_id
            LIMIT 1
            FOR SHARE OF r, p, h
            """
        )

        baseline_statement = text(
            """
            SELECT
                id,
                report_id,
                mac_version,
                mac_algorithm,
                mac_hex,
                key_id,
                created_by_user_id,
                created_at
            FROM public.report_content_macs
            WHERE report_id = :report_id
              AND mac_version =
                    'AIHA_REPORT_CONTENT_MAC_V1'
            LIMIT 1
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

                report_row = connection.execute(
                    report_statement,
                    {
                        "report_id":
                            report,
                        "hospital_id":
                            scope["hospital_id"],
                        "tenant_id":
                            scope["tenant_id"],
                    },
                ).mappings().one_or_none()

                if report_row is None:
                    raise PermissionError(
                        "Report outside principal scope"
                    )

                baseline = connection.execute(
                    baseline_statement,
                    {
                        "report_id":
                            report,
                    },
                ).mappings().one_or_none()

                if baseline is None:
                    return None

                baseline_key_id = str(
                    baseline["key_id"]
                )
                baseline_mac_key = (
                    mac_key_resolver(
                        baseline_key_id
                    )
                )
                current_mac = (
                    self._canonical_report_mac(
                        report_row,
                        baseline_mac_key,
                    )
                )

                stored_mac = str(
                    baseline["mac_hex"]
                )

                return {
                    "id":
                        int(baseline["id"]),
                    "report_id":
                        str(
                            baseline[
                                "report_id"
                            ]
                        ),
                    "mac_version":
                        str(
                            baseline[
                                "mac_version"
                            ]
                        ),
                    "mac_algorithm":
                        str(
                            baseline[
                                "mac_algorithm"
                            ]
                        ),
                    "key_id":
                        str(
                            baseline[
                                "key_id"
                            ]
                        ),
                    "stored_mac":
                        stored_mac,
                    "current_mac":
                        current_mac,
                    "created_by_user_id":
                        int(
                            baseline[
                                "created_by_user_id"
                            ]
                        ),
                    "created_at":
                        baseline[
                            "created_at"
                        ],
                    "matches":
                        hmac.compare_digest(
                            stored_mac,
                            current_mac,
                        ),
                }

        except SQLAlchemyError as exc:
            raise RuntimeError(
                "Canonical Reports database unavailable"
            ) from exc
