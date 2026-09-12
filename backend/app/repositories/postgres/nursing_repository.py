from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Connection


class PostgresNursingRepository:
    """
    PostgreSQL Nursing adapter with canonical principal-to-tenant isolation.

    Trusted scope:
      verified JWT sub + tenant_id
          -> users.id
          -> users.hospital_id
          -> hospitals.tenant_id

    Patient-scoped Nursing data is accessible only when the patient belongs
    to the same database-derived tenant as the authenticated principal.
    """

    supports_tenant_scope = True

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
    def _parse_principal_user_id(
        principal_user_id: int | None,
    ) -> int:
        try:
            user_id = int(principal_user_id)
        except (TypeError, ValueError):
            raise PermissionError(
                "Authenticated principal unavailable"
            )

        if user_id <= 0:
            raise PermissionError(
                "Authenticated principal unavailable"
            )

        return user_id

    def _resolve_scope(
        self,
        connection: Connection,
        tenant_id: str | None,
        principal_user_id: int | None,
    ) -> dict[str, Any]:
        user_id = self._parse_principal_user_id(
            principal_user_id
        )

        claimed_tenant_id = str(
            tenant_id or ""
        ).strip()

        if not claimed_tenant_id:
            raise PermissionError(
                "Authenticated tenant unavailable"
            )

        row = connection.execute(
            text(
                """
                SELECT
                    u.id AS user_id,
                    u.hospital_id AS hospital_id,
                    h.tenant_id AS tenant_id
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

        if row is None:
            raise PermissionError(
                "Authenticated principal has no hospital tenant scope"
            )

        hospital_id = row.get("hospital_id")
        derived_tenant_id = str(
            row.get("tenant_id") or ""
        ).strip()

        if hospital_id is None or not derived_tenant_id:
            raise PermissionError(
                "Authenticated principal has no hospital tenant scope"
            )

        if derived_tenant_id != claimed_tenant_id:
            raise PermissionError(
                "Authenticated tenant does not match principal scope"
            )

        return {
            "user_id": user_id,
            "hospital_id": hospital_id,
            "tenant_id": derived_tenant_id,
        }

    @staticmethod
    def _validate_patient(
        connection: Connection,
        patient_id: str,
        tenant_id: str,
    ) -> None:
        exists = connection.execute(
            text(
                """
                SELECT p.id
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
                "tenant_id": tenant_id,
            },
        ).scalar_one_or_none()

        if exists is None:
            raise LookupError(
                "Patient not found in authenticated tenant"
            )

    def list_vitals(
        self,
        patient_id: str,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            self._validate_patient(
                connection,
                patient_id,
                scope["tenant_id"],
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        nv.id,
                        nv.temperature,
                        nv.blood_pressure,
                        nv.heart_rate,
                        nv.respiratory_rate,
                        nv.oxygen_saturation,
                        nv.display_time
                    FROM public.nursing_vitals AS nv
                    JOIN public.patients AS p
                      ON p.id = nv.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE nv.patient_id = :patient_id
                      AND h.tenant_id = :tenant_id
                    ORDER BY nv.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).fetchall()

        return [
            self._serialize_vital(row)
            for row in rows
        ]

    def create_vital(
        self,
        patient_id: str,
        payload: dict[str, Any],
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> dict[str, Any]:
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            self._validate_patient(
                connection,
                patient_id,
                scope["tenant_id"],
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
                    SELECT
                        p.id,
                        NULL,
                        :temperature,
                        :blood_pressure,
                        :heart_rate,
                        :respiratory_rate,
                        :oxygen_saturation,
                        CURRENT_TIMESTAMP,
                        :display_time
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
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
                    "tenant_id": scope["tenant_id"],
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
            ).one_or_none()

            if row is None:
                raise LookupError(
                    "Patient not found in authenticated tenant"
                )

        return self._serialize_vital(row)

    def list_notes(
        self,
        patient_id: str,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            self._validate_patient(
                connection,
                patient_id,
                scope["tenant_id"],
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        nn.id,
                        nn.text
                    FROM public.nursing_notes AS nn
                    JOIN public.patients AS p
                      ON p.id = nn.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE nn.patient_id = :patient_id
                      AND h.tenant_id = :tenant_id
                    ORDER BY nn.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).fetchall()

        return [
            self._serialize_note(row)
            for row in rows
        ]

    def create_note(
        self,
        patient_id: str,
        text_value: str,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> dict[str, Any]:
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            self._validate_patient(
                connection,
                patient_id,
                scope["tenant_id"],
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
                    SELECT
                        p.id,
                        NULL,
                        :text,
                        CURRENT_TIMESTAMP
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
                    RETURNING
                        id,
                        text
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                    "text": text_value,
                },
            ).one_or_none()

            if row is None:
                raise LookupError(
                    "Patient not found in authenticated tenant"
                )

        return self._serialize_note(row)
