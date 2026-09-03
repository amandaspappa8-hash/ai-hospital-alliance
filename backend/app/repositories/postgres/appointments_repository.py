from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine


class PostgresAppointmentsRepository:
    """
    PostgreSQL implementation of the existing appointments repository
    contract.

    Public repository contract intentionally matches:
      - list_all()
      - create(payload)

    The SQLAlchemy Engine is injected by the composition/root layer.
    This class does not read environment variables and contains no
    database credentials.
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    @staticmethod
    def _serialize(row: Any) -> dict[str, Any]:
        mapping = dict(row)

        return {
            "id": str(mapping.get("id") or ""),
            "patientId": str(mapping.get("patient_id") or ""),
            "patientName": str(mapping.get("patient_name") or ""),
            "department": str(mapping.get("department") or ""),
            "doctor": str(mapping.get("doctor_name") or ""),
            "date": str(mapping.get("date") or ""),
            "time": str(mapping.get("time") or ""),
            "status": str(mapping.get("status") or "Scheduled"),
        }

    def list_all(self) -> list[dict[str, Any]]:
        statement = text(
            """
            SELECT
                a.id,
                a.patient_id,
                p.name AS patient_name,
                a.department,
                d.name AS doctor_name,
                a."date" AS date,
                a."time" AS time,
                a.status
            FROM public.appointments AS a
            LEFT JOIN public.patients AS p
                   ON p.id = a.patient_id
            LEFT JOIN public.doctors AS d
                   ON d.id = a.doctor_id
            ORDER BY a.id
            """
        )

        with self.engine.connect() as connection:
            rows = connection.execute(
                statement
            ).mappings().all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:

        patient_id = str(
            payload.get("patientId") or ""
        )

        patient_name = str(
            payload.get("patientName") or ""
        )

        doctor_name = str(
            payload.get("doctor") or ""
        )

        department = str(
            payload.get("department") or ""
        )

        appointment_date = str(
            payload.get("date") or ""
        )

        appointment_time = str(
            payload.get("time") or ""
        )

        status = str(
            payload.get("status") or "Scheduled"
        )

        with self.engine.begin() as connection:

            # PostgreSQL-specific transaction advisory lock.
            # Prevents two concurrent creates from selecting the same
            # compatibility identifier.
            connection.execute(
                text(
                    """
                    SELECT pg_advisory_xact_lock(
                        hashtext(
                            'ahos:appointments:compatibility-id'
                        )
                    )
                    """
                )
            )

            next_number = connection.execute(
                text(
                    """
                    SELECT
                        COALESCE(
                            MAX(
                                CAST(
                                    SUBSTRING(id FROM 3)
                                    AS INTEGER
                                )
                            ),
                            2000
                        ) + 1
                    FROM public.appointments
                    WHERE id ~ '^A-[0-9]+$'
                    """
                )
            ).scalar_one()

            appointment_id = (
                f"A-{int(next_number)}"
            )

            doctor_id = None

            if doctor_name:
                doctor_id = connection.execute(
                    text(
                        """
                        SELECT id
                        FROM public.doctors
                        WHERE name = :doctor_name
                        ORDER BY id
                        LIMIT 1
                        """
                    ),
                    {
                        "doctor_name": doctor_name
                    },
                ).scalar_one_or_none()

            connection.execute(
                text(
                    """
                    INSERT INTO public.appointments (
                        id,
                        patient_id,
                        doctor_id,
                        department,
                        "date",
                        "time",
                        status,
                        created_at
                    )
                    VALUES (
                        :id,
                        :patient_id,
                        :doctor_id,
                        :department,
                        :appointment_date,
                        :appointment_time,
                        :status,
                        CURRENT_TIMESTAMP
                    )
                    """
                ),
                {
                    "id": appointment_id,
                    "patient_id": (
                        patient_id or None
                    ),
                    "doctor_id": doctor_id,
                    "department": department,
                    "appointment_date": (
                        appointment_date
                    ),
                    "appointment_time": (
                        appointment_time
                    ),
                    "status": status,
                },
            )

        # Preserve the established API-facing repository shape.
        return {
            "id": appointment_id,
            "patientId": patient_id,
            "patientName": patient_name,
            "department": department,
            "doctor": doctor_name,
            "date": appointment_date,
            "time": appointment_time,
            "status": status,
        }
