from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine


class PostgresAppointmentsRepository:
    """
    PostgreSQL appointments repository with canonical tenant isolation.

    Security authority:
      JWT sub + tenant_id
          -> users.id
          -> users.hospital_id
          -> hospitals.tenant_id
          -> tenants.id

    Client-supplied patient/doctor identifiers are never accepted as
    tenant authority.
    """

    supports_tenant_scope = True

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

    @staticmethod
    def _parse_principal_user_id(
        principal_user_id: int | None,
    ) -> int:
        try:
            user_id = int(principal_user_id)
        except (TypeError, ValueError):
            raise PermissionError(
                "Invalid authenticated principal"
            )

        if user_id <= 0:
            raise PermissionError(
                "Invalid authenticated principal"
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

    def list_all(
        self,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> list[dict[str, Any]]:
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
            JOIN public.patients AS p
              ON p.id = a.patient_id
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            LEFT JOIN public.doctors AS d
              ON d.id = a.doctor_id
            WHERE h.tenant_id = :tenant_id
            ORDER BY a.id
            """
        )

        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                statement,
                {
                    "tenant_id": scope["tenant_id"],
                },
            ).mappings().all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create(
        self,
        payload: dict[str, Any],
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> dict[str, Any]:

        patient_id = str(
            payload.get("patientId") or ""
        ).strip()

        patient_name = str(
            payload.get("patientName") or ""
        )

        doctor_name = str(
            payload.get("doctor") or ""
        ).strip()

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

        if not patient_id:
            raise LookupError(
                "Patient not found"
            )

        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            patient_row = connection.execute(
                text(
                    """
                    SELECT
                        p.id,
                        p.hospital_id
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
                    LIMIT 1
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).mappings().first()

            if not patient_row:
                # Deliberately use not-found semantics rather than exposing
                # whether the patient exists in another tenant.
                raise LookupError(
                    "Patient not found"
                )

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
                        SELECT d.id
                        FROM public.doctors AS d
                        JOIN public.hospitals AS h
                          ON h.id = d.hospital_id
                        WHERE d.name = :doctor_name
                          AND h.tenant_id = :tenant_id
                        ORDER BY d.id
                        LIMIT 1
                        """
                    ),
                    {
                        "doctor_name": doctor_name,
                        "tenant_id": scope["tenant_id"],
                    },
                ).scalar_one_or_none()

                if doctor_id is None:
                    raise LookupError(
                        "Doctor not found"
                    )

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
                    "patient_id": patient_id,
                    "doctor_id": doctor_id,
                    "department": department,
                    "appointment_date": appointment_date,
                    "appointment_time": appointment_time,
                    "status": status,
                },
            )

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
