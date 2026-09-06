from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extensions import connection as PgConnection


class PostgresDoctorAssignmentsRepository:
    """PostgreSQL persistence adapter for canonical doctor assignments."""

    _SELECT_BASE = """
        SELECT
            a.id,
            a.patient_id AS "patientId",
            p.name AS "patientName",
            dep.name AS department,
            a.condition,
            COALESCE(a.status, 'Assigned') AS status
        FROM public.doctor_assignments AS a
        JOIN public.patients AS p
          ON p.id = a.patient_id
        JOIN public.doctors AS d
          ON d.id = a.doctor_id
        LEFT JOIN public.departments AS dep
          ON dep.id = d.department_id
    """

    def __init__(
        self,
        *,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        self._connection_kwargs = {
            "host": host,
            "port": port,
            "dbname": database,
            "user": user,
            "password": password,
        }

    def _connect(self) -> PgConnection:
        return psycopg2.connect(
            **self._connection_kwargs
        )

    @staticmethod
    def _row_to_assignment(
        row: tuple[Any, ...] | None,
    ) -> dict[str, Any] | None:
        if row is None:
            return None

        return {
            "id": row[0],
            "patientId": row[1],
            "patientName": row[2],
            "department": row[3],
            "condition": row[4],
            "status": row[5],
        }

    def _select_one(
        self,
        cursor,
        doctor_id: str,
        assignment_id: int,
    ) -> dict[str, Any] | None:
        cursor.execute(
            self._SELECT_BASE
            + """
              WHERE a.doctor_id = %s
                AND a.id = %s
            """,
            (
                doctor_id,
                assignment_id,
            ),
        )

        return self._row_to_assignment(
            cursor.fetchone()
        )

    def list_by_doctor(
        self,
        doctor_id: str,
    ) -> list[dict[str, Any]]:
        connection = self._connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    self._SELECT_BASE
                    + """
                      WHERE a.doctor_id = %s
                      ORDER BY a.id ASC
                    """,
                    (doctor_id,),
                )

                return [
                    self._row_to_assignment(row)
                    for row in cursor.fetchall()
                ]

        finally:
            connection.close()

    def create(
        self,
        doctor_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        patient_id = payload.get(
            "patientId",
            "",
        )

        status = (
            payload.get("status")
            or "Assigned"
        )

        connection = self._connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT
                            pg_advisory_xact_lock(
                                hashtextextended(
                                    %s || ':' || %s,
                                    0
                                )
                            )
                        """,
                        (
                            doctor_id,
                            patient_id,
                        ),
                    )

                    cursor.execute(
                        """
                        SELECT 1
                        FROM public.doctors
                        WHERE id = %s
                        """,
                        (doctor_id,),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError(
                            "Doctor not found"
                        )

                    cursor.execute(
                        """
                        SELECT 1
                        FROM public.patients
                        WHERE id = %s
                        """,
                        (patient_id,),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError(
                            "Patient not found"
                        )

                    cursor.execute(
                        self._SELECT_BASE
                        + """
                          WHERE a.doctor_id = %s
                            AND a.patient_id = %s
                          ORDER BY a.id ASC
                          LIMIT 1
                        """,
                        (
                            doctor_id,
                            patient_id,
                        ),
                    )

                    existing = (
                        self._row_to_assignment(
                            cursor.fetchone()
                        )
                    )

                    if existing is not None:
                        return existing

                    cursor.execute(
                        """
                        INSERT INTO public.doctor_assignments (
                            doctor_id,
                            patient_id,
                            condition,
                            status,
                            assigned_at
                        )
                        VALUES (
                            %s,
                            %s,
                            %s,
                            %s,
                            CURRENT_TIMESTAMP
                        )
                        RETURNING id
                        """,
                        (
                            doctor_id,
                            patient_id,
                            payload.get(
                                "condition"
                            ),
                            status,
                        ),
                    )

                    assignment_id = (
                        cursor.fetchone()[0]
                    )

                    created = self._select_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                    )

                    if created is None:
                        raise RuntimeError(
                            "Created assignment "
                            "could not be reloaded"
                        )

                    return created

        finally:
            connection.close()

    def update_status(
        self,
        doctor_id: str,
        assignment_id: int,
        status: str,
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE public.doctor_assignments
                        SET status = %s
                        WHERE doctor_id = %s
                          AND id = %s
                        RETURNING id
                        """,
                        (
                            status,
                            doctor_id,
                            assignment_id,
                        ),
                    )

                    updated = cursor.fetchone()

                    if updated is None:
                        return None

                    return self._select_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                    )

        finally:
            connection.close()

    def delete(
        self,
        doctor_id: str,
        assignment_id: int,
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    existing = self._select_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                    )

                    if existing is None:
                        return None

                    cursor.execute(
                        """
                        DELETE FROM public.doctor_assignments
                        WHERE doctor_id = %s
                          AND id = %s
                        RETURNING id
                        """,
                        (
                            doctor_id,
                            assignment_id,
                        ),
                    )

                    deleted = cursor.fetchone()

                    if deleted is None:
                        return None

                    return existing

        finally:
            connection.close()
