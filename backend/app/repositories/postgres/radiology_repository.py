from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class PostgresRadiologyRepository:
    _ID_LOCK_KEY = "aiha:radiology:radiology_orders:id"

    def __init__(
        self,
        engine: Engine,
        catalog_store: dict[str, Any] | None = None,
    ) -> None:
        self.engine = engine
        self.catalog_store = (
            catalog_store
            if catalog_store is not None
            else {}
        )

    @staticmethod
    def _json_value(
        value: Any,
        default: Any,
    ) -> Any:
        if value is None:
            return default

        if isinstance(
            value,
            str,
        ):
            try:
                return json.loads(
                    value
                )
            except json.JSONDecodeError:
                return default

        return value

    def _serialize(
        self,
        row: Any,
    ) -> dict[str, Any]:
        mapping = row._mapping

        return {
            "id": mapping["id"],
            "patientId": (
                mapping["patient_id"]
                or ""
            ),
            "patientName": (
                mapping["patient_name"]
                or ""
            ),
            "section": (
                mapping["section"]
                or ""
            ),
            "studies": list(
                self._json_value(
                    mapping["studies"],
                    [],
                )
                or []
            ),
            "priority": (
                mapping["priority"]
                or "Routine"
            ),
            "status": (
                mapping["status"]
                or "Pending"
            ),
            "report": (
                mapping["report"]
                or ""
            ),
        }

    def _validate_patient(
        self,
        connection: Any,
        patient_id: str,
    ) -> str:
        patient_name = connection.execute(
            text(
                """
                SELECT name
                FROM patients
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

        return str(
            patient_name
        )

    def get_catalog(
        self,
    ) -> dict[str, Any]:
        return self.catalog_store

    def list_orders(
        self,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT
                        ro.id,
                        ro.patient_id,
                        p.name AS patient_name,
                        ro.section,
                        ro.studies,
                        ro.priority,
                        ro.status,
                        ro.report
                    FROM radiology_orders AS ro
                    LEFT JOIN patients AS p
                      ON p.id = ro.patient_id
                    ORDER BY
                        ro.created_at NULLS LAST,
                        ro.id
                    """
                )
            ).all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def list_orders_by_patient(
        self,
        patient_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT
                        ro.id,
                        ro.patient_id,
                        p.name AS patient_name,
                        ro.section,
                        ro.studies,
                        ro.priority,
                        ro.status,
                        ro.report
                    FROM radiology_orders AS ro
                    LEFT JOIN patients AS p
                      ON p.id = ro.patient_id
                    WHERE ro.patient_id = :patient_id
                    ORDER BY
                        ro.created_at NULLS LAST,
                        ro.id
                    """
                ),
                {
                    "patient_id": patient_id,
                },
            ).all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create_order(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        patient_id = str(
            payload.get(
                "patientId",
                "",
            )
            or ""
        )

        studies = list(
            payload.get(
                "studies",
                [],
            )
            or []
        )

        priority = (
            payload.get("priority")
            or "Routine"
        )

        status = (
            payload.get("status")
            or "Pending"
        )

        report = (
            payload.get(
                "report",
                "",
            )
            or ""
        )

        with self.engine.begin() as connection:
            patient_name = (
                self._validate_patient(
                    connection,
                    patient_id,
                )
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

            max_suffix = connection.execute(
                text(
                    """
                    SELECT COALESCE(
                        MAX(
                            substring(
                                id
                                FROM 5
                            )::integer
                        ),
                        5000
                    )
                    FROM radiology_orders
                    WHERE id ~ '^RAD-[0-9]+$'
                    """
                )
            ).scalar_one()

            next_number = (
                max(
                    5000,
                    int(
                        max_suffix
                        or 5000
                    ),
                )
                + 1
            )

            order_id = (
                f"RAD-{next_number}"
            )

            row = connection.execute(
                text(
                    """
                    INSERT INTO radiology_orders (
                        id,
                        patient_id,
                        ordered_by,
                        section,
                        studies,
                        priority,
                        status,
                        study_uid,
                        report,
                        ai_result,
                        created_at,
                        updated_at
                    )
                    VALUES (
                        :id,
                        :patient_id,
                        NULL,
                        :section,
                        CAST(:studies AS JSON),
                        :priority,
                        :status,
                        NULL,
                        :report,
                        NULL,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    )
                    RETURNING
                        id,
                        patient_id,
                        section,
                        studies,
                        priority,
                        status,
                        report
                    """
                ),
                {
                    "id": order_id,
                    "patient_id":
                        patient_id,
                    "section": (
                        payload.get(
                            "section",
                            "",
                        )
                        or ""
                    ),
                    "studies": json.dumps(
                        studies
                    ),
                    "priority": priority,
                    "status": status,
                    "report": report,
                },
            ).one()

            mapping = dict(
                row._mapping
            )

            mapping[
                "patient_name"
            ] = patient_name

            class RowAdapter:
                def __init__(
                    self,
                    values: dict[str, Any],
                ) -> None:
                    self._mapping = values

            return self._serialize(
                RowAdapter(
                    mapping
                )
            )

    def set_result(
        self,
        order_id: str | int,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        report = (
            payload.get(
                "report",
                "",
            )
            or ""
        )

        status = (
            payload.get("status")
            or "Completed"
        )

        with self.engine.begin() as connection:
            patient_id = connection.execute(
                text(
                    """
                    UPDATE radiology_orders
                    SET
                        report = :report,
                        status = :status,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE id = :order_id
                    RETURNING patient_id
                    """
                ),
                {
                    "order_id":
                        str(order_id),
                    "report": report,
                    "status": status,
                },
            ).scalar_one_or_none()

            if patient_id is None:
                return None

            row = connection.execute(
                text(
                    """
                    SELECT
                        ro.id,
                        ro.patient_id,
                        p.name AS patient_name,
                        ro.section,
                        ro.studies,
                        ro.priority,
                        ro.status,
                        ro.report
                    FROM radiology_orders AS ro
                    LEFT JOIN patients AS p
                      ON p.id = ro.patient_id
                    WHERE ro.id = :order_id
                    """
                ),
                {
                    "order_id":
                        str(order_id),
                },
            ).one()

            return self._serialize(
                row
            )
