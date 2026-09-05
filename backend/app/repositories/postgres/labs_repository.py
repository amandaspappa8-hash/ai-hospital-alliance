"""PostgreSQL persistence adapter for AIHA laboratory orders."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text


class PostgresLabsRepository:
    """Persist laboratory orders in the canonical PostgreSQL schema."""

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

    def get_catalog(self) -> dict[str, Any]:
        return dict(self.catalog_store)

    def list_orders(self) -> list[dict[str, Any]]:
        stmt = text(
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
            LEFT JOIN public.patients AS p
                ON p.id = lo.patient_id
            ORDER BY
                CASE
                    WHEN lo.id ~ '^L-[0-9]+$'
                    THEN substring(lo.id FROM '^L-([0-9]+)$')::integer
                    ELSE NULL
                END,
                lo.id
            """
        )

        with self.engine.connect() as connection:
            rows = connection.execute(
                stmt
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    def list_orders_by_patient(
        self,
        patient_id: str,
    ) -> list[dict[str, Any]]:
        stmt = text(
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
            LEFT JOIN public.patients AS p
                ON p.id = lo.patient_id
            WHERE lo.patient_id = :patient_id
            ORDER BY
                CASE
                    WHEN lo.id ~ '^L-[0-9]+$'
                    THEN substring(lo.id FROM '^L-([0-9]+)$')::integer
                    ELSE NULL
                END,
                lo.id
            """
        )

        with self.engine.connect() as connection:
            rows = connection.execute(
                stmt,
                {
                    "patient_id": patient_id,
                },
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    @staticmethod
    def _validate_patient(
        connection,
        patient_id: str,
    ) -> str:
        patient_name = connection.execute(
            text(
                """
                SELECT name
                FROM public.patients
                WHERE id = :patient_id
                """
            ),
            {
                "patient_id": patient_id,
            },
        ).scalar_one_or_none()

        if patient_name is None:
            raise ValueError(
                "Patient not found"
            )

        return patient_name

    def create_order(
        self,
        payload: dict[str, Any],
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
            patient_name = self._validate_patient(
                connection,
                patient_id,
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
                    VALUES (
                        :id,
                        :patient_id,
                        NULL,
                        :section,
                        CAST(:tests AS json),
                        :priority,
                        :status,
                        '',
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
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
                    "id": order_id,
                    "patient_id": patient_id,
                    "section": section,
                    "tests": json.dumps(tests),
                    "priority": priority,
                    "status": status,
                },
            ).one()

            data = dict(
                row._mapping
            )

            data[
                "patient_name"
            ] = patient_name

            return self._serialize(
                _MappingRow(data)
            )

    def set_result(
        self,
        order_id: str | int,
        payload: dict[str, Any],
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
            row = connection.execute(
                text(
                    """
                    UPDATE public.lab_orders
                    SET
                        result = :result,
                        status = :status,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :order_id
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
                    "order_id": str(
                        order_id
                    ),
                    "result": result,
                    "status": status,
                },
            ).one_or_none()

            if row is None:
                return None

            patient_name = connection.execute(
                text(
                    """
                    SELECT name
                    FROM public.patients
                    WHERE id = :patient_id
                    """
                ),
                {
                    "patient_id":
                        row._mapping[
                            "patient_id"
                        ],
                },
            ).scalar_one_or_none()

            data = dict(
                row._mapping
            )

            data[
                "patient_name"
            ] = (
                patient_name
                or ""
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
