import json
from datetime import date
from typing import Any

from sqlalchemy import text


class PostgresPatientsRepository:
    """Canonical tenant-scoped PostgreSQL Patient persistence adapter."""

    def __init__(self, engine):
        self._engine = engine

    @staticmethod
    def _serialize_patient(row) -> dict[str, Any]:
        mapping = dict(row)

        date_of_birth = mapping.get("date_of_birth")
        if isinstance(date_of_birth, date):
            date_of_birth = date_of_birth.isoformat()

        # Keep the public Patient response stable while PostgreSQL becomes
        # the canonical persistence authority. Do not infer absent clinical
        # values or expose persistence-only identifiers.
        full_name = (
            mapping.get("full_name")
            or mapping.get("name")
        )

        return {
            "id": mapping.get("id"),
            "mrn": mapping.get("mrn"),
            "full_name": full_name,
            "name": mapping.get("name"),
            "date_of_birth": date_of_birth,
            "gender": mapping.get("gender"),
            "phone": mapping.get("phone"),
            "blood_type": mapping.get("blood_type"),
            "allergies": mapping.get("allergies") or [],
            "chronic_conditions": (
                mapping.get("chronic_conditions") or []
            ),
            "condition": mapping.get("condition"),
            "department": mapping.get("department"),
            "status": mapping.get("status"),
        }

    @staticmethod
    def _parse_principal_user_id(principal_user_id: int) -> int:
        try:
            value = int(principal_user_id)
        except (TypeError, ValueError) as exc:
            raise PermissionError(
                "Invalid canonical Patient principal"
            ) from exc

        if value <= 0:
            raise PermissionError(
                "Invalid canonical Patient principal"
            )

        return value

    def _resolve_scope(
        self,
        connection,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]:
        user_id = self._parse_principal_user_id(
            principal_user_id
        )

        tenant_id = str(tenant_id or "").strip()

        if not tenant_id:
            raise PermissionError(
                "Missing canonical tenant claim"
            )

        rows = (
            connection.execute(
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
                      AND u.is_active IS TRUE
                    """
                ),
                {
                    "user_id": user_id,
                },
            )
            .mappings()
            .all()
        )

        if len(rows) != 1:
            raise PermissionError(
                "Canonical Patient principal scope is unresolved"
            )

        row = rows[0]

        derived_tenant_id = str(
            row.get("tenant_id") or ""
        )

        if not derived_tenant_id:
            raise PermissionError(
                "Canonical Patient hospital tenant is unresolved"
            )

        if derived_tenant_id != tenant_id:
            raise PermissionError(
                "Canonical Patient tenant mismatch"
            )

        hospital_id = row.get("hospital_id")

        if not hospital_id:
            raise PermissionError(
                "Canonical Patient hospital is unresolved"
            )

        return {
            "user_id": user_id,
            "hospital_id": str(hospital_id),
            "tenant_id": derived_tenant_id,
        }

    @staticmethod
    def _patient_select_sql() -> str:
        return """
            SELECT
                p.id,
                p.mrn,
                p.full_name,
                p.name,
                p.date_of_birth,
                p.gender,
                p.phone,
                p.blood_type,
                p.allergies,
                p.chronic_conditions,
                p.condition,
                d.name AS department,
                p.status
            FROM public.patients AS p
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            LEFT JOIN public.departments AS d
              ON d.id = p.department_id
             AND (
                    d.hospital_id = p.hospital_id
                    OR d.hospital_id IS NULL
                 )
            WHERE h.tenant_id = :tenant_id
        """

    def list_all(
        self,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        with self._engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = (
                connection.execute(
                    text(
                        self._patient_select_sql()
                        + " ORDER BY p.id"
                    ),
                    {
                        "tenant_id": scope["tenant_id"],
                    },
                )
                .mappings()
                .all()
            )

        return [
            self._serialize_patient(row)
            for row in rows
        ]

    def get_by_id(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        with self._engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = (
                connection.execute(
                    text(
                        self._patient_select_sql()
                        + " AND p.id = :patient_id"
                    ),
                    {
                        "tenant_id": scope["tenant_id"],
                        "patient_id": patient_id,
                    },
                )
                .mappings()
                .all()
            )

        if not rows:
            return None

        if len(rows) != 1:
            raise RuntimeError(
                "Canonical Patient ID is not unique"
            )

        return self._serialize_patient(rows[0])

    @staticmethod
    def _write_audit(
        connection,
        *,
        scope: dict[str, Any],
        action: str,
        resource_id: str,
        details: dict[str, Any] | None,
        ip_address: str | None,
    ) -> None:
        connection.execute(
            text(
                """
                INSERT INTO public.audit_logs (
                    user_id,
                    action,
                    resource,
                    resource_id,
                    details,
                    ip_address,
                    success,
                    tenant_id
                )
                VALUES (
                    :user_id,
                    :action,
                    'Patient',
                    :resource_id,
                    :details,
                    :ip_address,
                    TRUE,
                    :tenant_id
                )
                """
            ),
            {
                "user_id": str(scope["user_id"]),
                "action": action,
                "resource_id": resource_id,
                "details": (
                    json.dumps(
                        details,
                        sort_keys=True,
                        default=str,
                    )
                    if details is not None
                    else None
                ),
                "ip_address": ip_address,
                "tenant_id": scope["tenant_id"],
            },
        )

    def create(
        self,
        patient: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any]:
        full_name = str(
            patient.get("full_name") or ""
        ).strip()

        if not full_name:
            raise ValueError(
                "Patient full_name is required"
            )

        gender = str(
            patient.get("gender") or ""
        ).strip().lower()

        if not gender:
            raise ValueError(
                "Patient gender is required"
            )

        mrn = patient.get("mrn")

        with self._engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            connection.execute(
                text(
                    """
                    SELECT pg_advisory_xact_lock(
                        hashtext(
                            'aiha.phase2.7.patients.id'
                        )
                    )
                    """
                )
            )

            next_number = connection.execute(
                text(
                    """
                    SELECT COALESCE(
                        MAX(
                            CASE
                                WHEN id ~ '^P-[0-9]+$'
                                THEN substring(id FROM 3)::integer
                                ELSE NULL
                            END
                        ),
                        1000
                    ) + 1
                    FROM public.patients
                    """
                )
            ).scalar_one()

            patient_id = f"P-{int(next_number)}"

            if mrn is None or not str(mrn).strip():
                mrn = f"MRN-{patient_id[2:]}"

            mrn = str(mrn).strip()

            duplicate = connection.execute(
                text(
                    """
                    SELECT COUNT(*)
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE h.tenant_id = :tenant_id
                      AND p.mrn = :mrn
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                    "mrn": mrn,
                },
            ).scalar_one()

            if duplicate:
                raise ValueError(
                    f"MRN {mrn} already exists"
                )

            current_medications = patient.get(
                "current_medications"
            )

            result = (
                connection.execute(
                    text(
                        """
                        INSERT INTO public.patients (
                            id,
                            name,
                            gender,
                            phone,
                            hospital_id,
                            mrn,
                            full_name,
                            date_of_birth,
                            blood_type,
                            allergies,
                            chronic_conditions,
                            current_medications,
                            insurance_provider
                        )
                        VALUES (
                            :id,
                            :name,
                            :gender,
                            :phone,
                            :hospital_id,
                            :mrn,
                            :full_name,
                            :date_of_birth,
                            :blood_type,
                            :allergies,
                            :chronic_conditions,
                            CAST(:current_medications AS JSONB),
                            :insurance_provider
                        )
                        RETURNING
                            id,
                            mrn,
                            full_name
                        """
                    ),
                    {
                        "id": patient_id,
                        "name": full_name,
                        "gender": gender,
                        "phone": patient.get("phone"),
                        "hospital_id": scope["hospital_id"],
                        "mrn": mrn,
                        "full_name": full_name,
                        "date_of_birth": patient.get(
                            "date_of_birth"
                        ),
                        "blood_type": patient.get(
                            "blood_type"
                        ),
                        "allergies": (
                            patient.get("allergies")
                            or []
                        ),
                        "chronic_conditions": (
                            patient.get(
                                "chronic_conditions"
                            )
                            or []
                        ),
                        "current_medications": (
                            json.dumps(
                                current_medications,
                                default=str,
                            )
                            if current_medications
                            is not None
                            else "null"
                        ),
                        "insurance_provider": patient.get(
                            "insurance_provider"
                        ),
                    },
                )
                .mappings()
                .one()
            )

            self._write_audit(
                connection,
                scope=scope,
                action="patient.create",
                resource_id=patient_id,
                details={
                    "mrn": mrn,
                },
                ip_address=ip_address,
            )

        return dict(result)

    def update(
        self,
        patient_id: str,
        changes: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any] | None:
        allowed = {
            "full_name",
            "phone",
            "blood_type",
            "allergies",
            "chronic_conditions",
        }

        filtered = {
            key: value
            for key, value in changes.items()
            if key in allowed
            and value is not None
        }

        with self._engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            exists = connection.execute(
                text(
                    """
                    SELECT p.id
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).scalar_one_or_none()

            if exists is None:
                return None

            if filtered:
                assignments = []
                parameters: dict[str, Any] = {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                }

                for index, (key, value) in enumerate(
                    filtered.items()
                ):
                    parameter = f"value_{index}"
                    assignments.append(
                        f"{key} = :{parameter}"
                    )
                    parameters[parameter] = value

                    if key == "full_name":
                        assignments.append(
                            f"name = :{parameter}"
                        )

                connection.execute(
                    text(
                        """
                        UPDATE public.patients AS p
                        SET
                        """
                        + ", ".join(assignments)
                        + """
                        FROM public.hospitals AS h
                        WHERE p.hospital_id = h.id
                          AND p.id = :patient_id
                          AND h.tenant_id = :tenant_id
                        """
                    ),
                    parameters,
                )

            self._write_audit(
                connection,
                scope=scope,
                action="patient.update",
                resource_id=patient_id,
                details=filtered,
                ip_address=ip_address,
            )

        return {
            "id": patient_id,
        }

    def delete(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> bool:
        with self._engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            deleted = connection.execute(
                text(
                    """
                    DELETE FROM public.patients AS p
                    USING public.hospitals AS h
                    WHERE p.hospital_id = h.id
                      AND p.id = :patient_id
                      AND h.tenant_id = :tenant_id
                    RETURNING p.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).scalar_one_or_none()

            if deleted is None:
                return False

            self._write_audit(
                connection,
                scope=scope,
                action="patient.delete",
                resource_id=patient_id,
                details=None,
                ip_address=ip_address,
            )

        return True

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None:
        patient_id = str(
            patient_id or ""
        ).strip()

        if not patient_id:
            raise PermissionError(
                "Patient scope cannot be established"
            )

        with self._engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            allowed = connection.execute(
                text(
                    """
                    SELECT 1
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND p.hospital_id = :hospital_id
                      AND h.tenant_id = :tenant_id
                    LIMIT 1
                    """
                ),
                {
                    "patient_id": patient_id,
                    "hospital_id": scope["hospital_id"],
                    "tenant_id": scope["tenant_id"],
                },
            ).scalar_one_or_none()

        if allowed is None:
            raise PermissionError(
                "Patient is outside authenticated hospital/tenant scope"
            )
