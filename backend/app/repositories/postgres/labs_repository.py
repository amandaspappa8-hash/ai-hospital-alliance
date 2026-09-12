"""PostgreSQL persistence adapter for AIHA laboratory orders."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Connection


class PostgresLabsRepository:
    """Persist tenant-scoped laboratory orders in canonical PostgreSQL."""

    supports_tenant_scope = True

    _ID_LOCK_KEY = "aiha:labs:lab_orders:id"

    def __init__(
        self,
        engine,
        catalog_store: dict[str, Any],
    ):
        self.engine = engine
        self.catalog_store = catalog_store

    @staticmethod
    def _serialize(row) -> dict[str, Any]:
        mapping = row._mapping

        tests = mapping["tests"]

        if isinstance(tests, str):
            try:
                tests = json.loads(tests)
            except json.JSONDecodeError:
                tests = []

        return {
            "id": mapping["id"],
            "patientId": mapping["patient_id"] or "",
            "patientName": mapping["patient_name"] or "",
            "section": mapping["section"] or "",
            "tests": tests or [],
            "priority": mapping["priority"] or "Routine",
            "status": mapping["status"] or "Pending",
            "result": mapping["result"] or "",
        }

    @staticmethod
    def _parse_principal_user_id(
        principal_user_id: int | str | None,
    ) -> int:
        try:
            parsed = int(principal_user_id)
        except (TypeError, ValueError) as exc:
            raise PermissionError(
                "Invalid authenticated principal"
            ) from exc

        if parsed <= 0:
            raise PermissionError(
                "Invalid authenticated principal"
            )

        return parsed

    @classmethod
    def _resolve_scope(
        cls,
        connection: Connection,
        tenant_id: str | None,
        principal_user_id: int | str | None,
    ) -> str:
        claimed_tenant_id = str(
            tenant_id or ""
        ).strip()

        if not claimed_tenant_id:
            raise PermissionError(
                "Authenticated tenant unavailable"
            )

        user_id = cls._parse_principal_user_id(
            principal_user_id
        )

        row = connection.execute(
            text(
                """
                SELECT
                    t.id AS tenant_id
                FROM public.users AS u
                JOIN public.hospitals AS h
                    ON h.id = u.hospital_id
                JOIN public.tenants AS t
                    ON t.id = h.tenant_id
                WHERE u.id = :user_id
                """
            ),
            {
                "user_id": user_id,
            },
        ).one_or_none()

        if row is None:
            raise PermissionError(
                "Authenticated principal has no tenant scope"
            )

        derived_tenant_id = str(
            row._mapping["tenant_id"] or ""
        ).strip()

        if (
            not derived_tenant_id
            or derived_tenant_id
            != claimed_tenant_id
        ):
            raise PermissionError(
                "Authenticated tenant scope mismatch"
            )

        return derived_tenant_id

    @staticmethod
    def _validate_patient(
        connection: Connection,
        patient_id: str,
        tenant_id: str,
    ) -> str:
        patient_name = connection.execute(
            text(
                """
                SELECT
                    p.name
                FROM public.patients AS p
                JOIN public.hospitals AS h
                    ON h.id = p.hospital_id
                WHERE
                    p.id = :patient_id
                    AND h.tenant_id = :tenant_id
                """
            ),
            {
                "patient_id": patient_id,
                "tenant_id": tenant_id,
            },
        ).scalar_one_or_none()

        if patient_name is None:
            raise ValueError(
                "Patient not found"
            )

        return patient_name

    def get_catalog(self) -> dict[str, Any]:
        # Shared reference data. It contains no patient records and therefore
        # intentionally remains outside tenant row filtering.
        return dict(self.catalog_store)

    def list_orders(
        self,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | str | None = None,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            trusted_tenant_id = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        lo.id,
                        lo.patient_id,
                        p.name AS patient_name,
                        lo.section,
                        lo.tests,
                        lo.priority,
                        lo.status,
                        lo.result
                    FROM public.lab_orders AS lo
                    JOIN public.patients AS p
                        ON p.id = lo.patient_id
                    JOIN public.hospitals AS h
                        ON h.id = p.hospital_id
                    WHERE
                        h.tenant_id = :tenant_id
                    ORDER BY
                        CASE
                            WHEN lo.id ~ '^L-[0-9]+$'
                            THEN substring(
                                lo.id FROM '^L-([0-9]+)$'
                            )::integer
                            ELSE NULL
                        END,
                        lo.id
                    """
                ),
                {
                    "tenant_id":
                        trusted_tenant_id,
                },
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    def list_orders_by_patient(
        self,
        patient_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | str | None = None,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            trusted_tenant_id = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        lo.id,
                        lo.patient_id,
                        p.name AS patient_name,
                        lo.section,
                        lo.tests,
                        lo.priority,
                        lo.status,
                        lo.result
                    FROM public.lab_orders AS lo
                    JOIN public.patients AS p
                        ON p.id = lo.patient_id
                    JOIN public.hospitals AS h
                        ON h.id = p.hospital_id
                    WHERE
                        lo.patient_id = :patient_id
                        AND h.tenant_id = :tenant_id
                    ORDER BY
                        CASE
                            WHEN lo.id ~ '^L-[0-9]+$'
                            THEN substring(
                                lo.id FROM '^L-([0-9]+)$'
                            )::integer
                            ELSE NULL
                        END,
                        lo.id
                    """
                ),
                {
                    "patient_id":
                        patient_id,
                    "tenant_id":
                        trusted_tenant_id,
                },
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create_order(
        self,
        payload: dict[str, Any],
        *,
        tenant_id: str | None = None,
        principal_user_id: int | str | None = None,
    ) -> dict[str, Any]:
        patient_id = payload.get(
            "patientId",
            "",
        )

        tests = payload.get(
            "tests",
            [],
        )

        priority = (
            payload.get("priority")
            or "Routine"
        )

        status = (
            payload.get("status")
            or "Pending"
        )

        section = (
            payload.get("section")
            or ""
        )

        with self.engine.begin() as connection:
            trusted_tenant_id = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            patient_name = self._validate_patient(
                connection,
                patient_id,
                trusted_tenant_id,
            )

            connection.execute(
                text(
                    """
                    SELECT pg_advisory_xact_lock(
                        hashtext(:lock_key)
                    )
                    """
                ),
                {
                    "lock_key":
                        self._ID_LOCK_KEY,
                },
            )

            next_number = connection.execute(
                text(
                    """
                    SELECT
                        GREATEST(
                            COALESCE(
                                MAX(
                                    CASE
                                        WHEN id ~ '^L-[0-9]+$'
                                        THEN substring(
                                            id FROM '^L-([0-9]+)$'
                                        )::integer
                                        ELSE NULL
                                    END
                                ),
                                4000
                            ),
                            4000
                        ) + 1
                    FROM public.lab_orders
                    """
                )
            ).scalar_one()

            order_id = (
                f"L-{int(next_number)}"
            )

            row = connection.execute(
                text(
                    """
                    INSERT INTO public.lab_orders (
                        id,
                        patient_id,
                        ordered_by,
                        section,
                        tests,
                        priority,
                        status,
                        result,
                        created_at,
                        updated_at
                    )
                    SELECT
                        :id,
                        p.id,
                        NULL,
                        :section,
                        CAST(:tests AS json),
                        :priority,
                        :status,
                        '',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                        ON h.id = p.hospital_id
                    WHERE
                        p.id = :patient_id
                        AND h.tenant_id = :tenant_id
                    RETURNING
                        id,
                        patient_id,
                        section,
                        tests,
                        priority,
                        status,
                        result
                    """
                ),
                {
                    "id":
                        order_id,
                    "patient_id":
                        patient_id,
                    "tenant_id":
                        trusted_tenant_id,
                    "section":
                        section,
                    "tests":
                        json.dumps(tests),
                    "priority":
                        priority,
                    "status":
                        status,
                },
            ).one_or_none()

            if row is None:
                raise ValueError(
                    "Patient not found"
                )

            data = dict(
                row._mapping
            )

            data["patient_name"] = (
                patient_name
            )

            return self._serialize(
                _MappingRow(data)
            )

    def set_result(
        self,
        order_id: str | int,
        payload: dict[str, Any],
        *,
        tenant_id: str | None = None,
        principal_user_id: int | str | None = None,
    ) -> dict[str, Any] | None:
        status = (
            payload.get("status")
            or "Completed"
        )

        result = payload.get(
            "result",
            "",
        )

        with self.engine.begin() as connection:
            trusted_tenant_id = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    """
                    UPDATE public.lab_orders AS lo
                    SET
                        result = :result,
                        status = :status,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE
                        lo.id = :order_id
                        AND EXISTS (
                            SELECT 1
                            FROM public.patients AS p
                            JOIN public.hospitals AS h
                                ON h.id = p.hospital_id
                            WHERE
                                p.id = lo.patient_id
                                AND h.tenant_id = :tenant_id
                        )
                    RETURNING
                        lo.id,
                        lo.patient_id,
                        lo.section,
                        lo.tests,
                        lo.priority,
                        lo.status,
                        lo.result
                    """
                ),
                {
                    "order_id":
                        str(order_id),
                    "result":
                        result,
                    "status":
                        status,
                    "tenant_id":
                        trusted_tenant_id,
                },
            ).one_or_none()

            if row is None:
                return None

            patient_name = connection.execute(
                text(
                    """
                    SELECT
                        p.name
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                        ON h.id = p.hospital_id
                    WHERE
                        p.id = :patient_id
                        AND h.tenant_id = :tenant_id
                    """
                ),
                {
                    "patient_id":
                        row._mapping[
                            "patient_id"
                        ],
                    "tenant_id":
                        trusted_tenant_id,
                },
            ).scalar_one_or_none()

            if patient_name is None:
                return None

            data = dict(
                row._mapping
            )

            data["patient_name"] = (
                patient_name
            )

            return self._serialize(
                _MappingRow(data)
            )


class _MappingRow:
    """Small adapter used by the serializer for constructed mappings."""

    def __init__(
        self,
        mapping: dict[str, Any],
    ):
        self._mapping = mapping
