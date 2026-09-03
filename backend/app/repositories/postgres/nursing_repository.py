from __future__ import annotations

from typing import Any

from sqlalchemy import text


class PostgresNursingRepository:
    """PostgreSQL compatibility adapter for the existing Nursing API contract."""

    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def _serialize_vital(row) -> dict[str, Any]:
        mapping = row._mapping

        return {
            "id": mapping["id"],
            "temperature": mapping["temperature"] or "",
            "bloodPressure": mapping["blood_pressure"] or "",
            "heartRate": mapping["heart_rate"] or "",
            "respiratoryRate": mapping["respiratory_rate"] or "",
            "oxygenSaturation": mapping["oxygen_saturation"] or "",
            "time": mapping["display_time"] or "",
        }

    @staticmethod
    def _serialize_note(row) -> dict[str, Any]:
        mapping = row._mapping

        return {
            "id": mapping["id"],
            "text": mapping["text"],
        }

    @staticmethod
    def _validate_patient(connection, patient_id: str) -> None:
        exists = connection.execute(
            text(
                """
                SELECT 1
                FROM public.patients
                WHERE id = :patient_id
                LIMIT 1
                """
            ),
            {"patient_id": patient_id},
        ).scalar_one_or_none()

        if exists is None:
            raise ValueError(
                f"Unknown patient_id: {patient_id}"
            )

    def list_vitals(
        self,
        patient_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT
                        id,
                        temperature,
                        blood_pressure,
                        heart_rate,
                        respiratory_rate,
                        oxygen_saturation,
                        display_time
                    FROM public.nursing_vitals
                    WHERE patient_id = :patient_id
                    ORDER BY id
                    """
                ),
                {"patient_id": patient_id},
            ).fetchall()

        return [
            self._serialize_vital(row)
            for row in rows
        ]

    def create_vital(
        self,
        patient_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        with self.engine.begin() as connection:
            self._validate_patient(
                connection,
                patient_id,
            )

            row = connection.execute(
                text(
                    """
                    INSERT INTO public.nursing_vitals (
                        patient_id,
                        nurse_id,
                        temperature,
                        blood_pressure,
                        heart_rate,
                        respiratory_rate,
                        oxygen_saturation,
                        recorded_at,
                        display_time
                    )
                    VALUES (
                        :patient_id,
                        NULL,
                        :temperature,
                        :blood_pressure,
                        :heart_rate,
                        :respiratory_rate,
                        :oxygen_saturation,
                        CURRENT_TIMESTAMP,
                        :display_time
                    )
                    RETURNING
                        id,
                        temperature,
                        blood_pressure,
                        heart_rate,
                        respiratory_rate,
                        oxygen_saturation,
                        display_time
                    """
                ),
                {
                    "patient_id": patient_id,
                    "temperature": payload.get(
                        "temperature",
                        "",
                    ),
                    "blood_pressure": payload.get(
                        "bloodPressure",
                        "",
                    ),
                    "heart_rate": payload.get(
                        "heartRate",
                        "",
                    ),
                    "respiratory_rate": payload.get(
                        "respiratoryRate",
                        "",
                    ),
                    "oxygen_saturation": payload.get(
                        "oxygenSaturation",
                        "",
                    ),
                    "display_time": payload.get(
                        "time",
                        "",
                    ),
                },
            ).one()

        return self._serialize_vital(row)

    def list_notes(
        self,
        patient_id: str,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT
                        id,
                        text
                    FROM public.nursing_notes
                    WHERE patient_id = :patient_id
                    ORDER BY id
                    """
                ),
                {"patient_id": patient_id},
            ).fetchall()

        return [
            self._serialize_note(row)
            for row in rows
        ]

    def create_note(
        self,
        patient_id: str,
        text_value: str,
    ) -> dict[str, Any]:
        with self.engine.begin() as connection:
            self._validate_patient(
                connection,
                patient_id,
            )

            row = connection.execute(
                text(
                    """
                    INSERT INTO public.nursing_notes (
                        patient_id,
                        nurse_id,
                        text,
                        created_at
                    )
                    VALUES (
                        :patient_id,
                        NULL,
                        :text,
                        CURRENT_TIMESTAMP
                    )
                    RETURNING
                        id,
                        text
                    """
                ),
                {
                    "patient_id": patient_id,
                    "text": text_value,
                },
            ).one()

        return self._serialize_note(row)
