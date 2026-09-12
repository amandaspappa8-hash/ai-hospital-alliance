from __future__ import annotations

from typing import Any

import psycopg2
from psycopg2.extensions import connection as PgConnection


class PostgresDoctorAssignmentsRepository:
    """Tenant-aware PostgreSQL adapter for Doctors and Doctor Assignments."""

    supports_tenant_scope = True

    _DOCTOR_SELECT_BASE = """
        SELECT
            d.id,
            d.name,
            d.specialty,
            dep.name AS department,
            d.experience,
            d.status,
            d.rating,
            d.patients_count,
            d.schedule,
            d.phone
        FROM public.doctors AS d
        JOIN public.hospitals AS dh
          ON dh.id = d.hospital_id
        LEFT JOIN public.departments AS dep
          ON dep.id = d.department_id
    """

    _ASSIGNMENT_SELECT_BASE = """
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
        JOIN public.hospitals AS ph
          ON ph.id = p.hospital_id
        JOIN public.doctors AS d
          ON d.id = a.doctor_id
        JOIN public.hospitals AS dh
          ON dh.id = d.hospital_id
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
    def _row_to_doctor(
        row: tuple[Any, ...] | None,
    ) -> dict[str, Any] | None:
        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "specialty": row[2],
            "department": row[3],
            "experience": row[4],
            "status": row[5],
            "rating": row[6],
            "patients": row[7],
            "schedule": row[8],
            "phone": row[9],
        }

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

    @staticmethod
    def _parse_principal_user_id(
        principal_user_id: int,
    ) -> int:
        if (
            isinstance(principal_user_id, bool)
            or not isinstance(principal_user_id, int)
            or principal_user_id <= 0
        ):
            raise PermissionError(
                "Invalid authenticated principal"
            )

        return principal_user_id

    def _resolve_scope(
        self,
        cursor,
        tenant_id: str | None,
        principal_user_id: int | None,
    ) -> dict[str, str | int] | None:
        if (
            tenant_id is None
            and principal_user_id is None
        ):
            return None

        if (
            tenant_id is None
            or principal_user_id is None
        ):
            raise PermissionError(
                "Incomplete Doctor tenant scope"
            )

        claimed_tenant_id = str(
            tenant_id or ""
        ).strip()

        if not claimed_tenant_id:
            raise PermissionError(
                "Invalid authenticated tenant"
            )

        user_id = self._parse_principal_user_id(
            principal_user_id
        )

        cursor.execute(
            """
            SELECT
                u.id,
                u.hospital_id,
                h.tenant_id
            FROM public.users AS u
            JOIN public.hospitals AS h
              ON h.id = u.hospital_id
            JOIN public.tenants AS t
              ON t.id = h.tenant_id
            WHERE u.id = %s
            """,
            (user_id,),
        )

        row = cursor.fetchone()

        if row is None:
            raise PermissionError(
                "Authenticated principal has no trusted tenant binding"
            )

        hospital_id = str(
            row[1] or ""
        ).strip()

        derived_tenant_id = str(
            row[2] or ""
        ).strip()

        if (
            not hospital_id
            or not derived_tenant_id
        ):
            raise PermissionError(
                "Authenticated principal has incomplete tenant binding"
            )

        if derived_tenant_id != claimed_tenant_id:
            raise PermissionError(
                "Authenticated tenant mismatch"
            )

        return {
            "principal_user_id": user_id,
            "hospital_id": hospital_id,
            "tenant_id": derived_tenant_id,
        }

    @staticmethod
    def _scope_required(
        scope: dict[str, str | int] | None,
    ) -> dict[str, str | int]:
        if scope is None:
            raise PermissionError(
                "Tenant scope required for Doctor directory"
            )

        return scope

    def _doctor_exists_in_tenant(
        self,
        cursor,
        doctor_id: str,
        tenant_id: str,
    ) -> bool:
        cursor.execute(
            """
            SELECT 1
            FROM public.doctors AS d
            JOIN public.hospitals AS h
              ON h.id = d.hospital_id
            WHERE d.id = %s
              AND h.tenant_id = %s
            """,
            (
                doctor_id,
                tenant_id,
            ),
        )

        return cursor.fetchone() is not None

    def _patient_exists_in_tenant(
        self,
        cursor,
        patient_id: str,
        tenant_id: str,
    ) -> bool:
        cursor.execute(
            """
            SELECT 1
            FROM public.patients AS p
            JOIN public.hospitals AS h
              ON h.id = p.hospital_id
            WHERE p.id = %s
              AND h.tenant_id = %s
            """,
            (
                patient_id,
                tenant_id,
            ),
        )

        return cursor.fetchone() is not None

    def list_doctors(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        connection = self._connect()

        try:
            with connection.cursor() as cursor:
                scope = self._scope_required(
                    self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )
                )

                cursor.execute(
                    self._DOCTOR_SELECT_BASE
                    + """
                      WHERE dh.tenant_id = %s
                      ORDER BY d.id ASC
                    """,
                    (scope["tenant_id"],),
                )

                return [
                    self._row_to_doctor(row)
                    for row in cursor.fetchall()
                ]

        finally:
            connection.close()

    def list_doctors_by_specialty(
        self,
        specialty: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        normalized = specialty.strip().lower()

        connection = self._connect()

        try:
            with connection.cursor() as cursor:
                scope = self._scope_required(
                    self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )
                )

                cursor.execute(
                    self._DOCTOR_SELECT_BASE
                    + """
                      WHERE dh.tenant_id = %s
                        AND LOWER(
                            TRIM(
                                COALESCE(
                                    d.specialty,
                                    ''
                                )
                            )
                        ) = %s
                      ORDER BY d.id ASC
                    """,
                    (
                        scope["tenant_id"],
                        normalized,
                    ),
                )

                return [
                    self._row_to_doctor(row)
                    for row in cursor.fetchall()
                ]

        finally:
            connection.close()

    def get_doctor(
        self,
        doctor_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            with connection.cursor() as cursor:
                scope = self._scope_required(
                    self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )
                )

                cursor.execute(
                    self._DOCTOR_SELECT_BASE
                    + """
                      WHERE d.id = %s
                        AND dh.tenant_id = %s
                    """,
                    (
                        doctor_id,
                        scope["tenant_id"],
                    ),
                )

                return self._row_to_doctor(
                    cursor.fetchone()
                )

        finally:
            connection.close()

    def _select_assignment_one(
        self,
        cursor,
        doctor_id: str,
        assignment_id: int,
        tenant_id: str | None,
    ) -> dict[str, Any] | None:
        sql = (
            self._ASSIGNMENT_SELECT_BASE
            + """
              WHERE a.doctor_id = %s
                AND a.id = %s
            """
        )

        params: list[Any] = [
            doctor_id,
            assignment_id,
        ]

        if tenant_id is not None:
            sql += """
                AND dh.tenant_id = %s
                AND ph.tenant_id = %s
            """

            params.extend(
                [
                    tenant_id,
                    tenant_id,
                ]
            )

        cursor.execute(
            sql,
            tuple(params),
        )

        return self._row_to_assignment(
            cursor.fetchone()
        )

    def list_by_doctor(
        self,
        doctor_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        connection = self._connect()

        try:
            with connection.cursor() as cursor:
                scope = self._resolve_scope(
                    cursor,
                    tenant_id,
                    principal_user_id,
                )

                sql = (
                    self._ASSIGNMENT_SELECT_BASE
                    + """
                      WHERE a.doctor_id = %s
                    """
                )

                params: list[Any] = [
                    doctor_id,
                ]

                if scope is not None:
                    sql += """
                        AND dh.tenant_id = %s
                        AND ph.tenant_id = %s
                    """

                    params.extend(
                        [
                            scope["tenant_id"],
                            scope["tenant_id"],
                        ]
                    )

                sql += " ORDER BY a.id ASC"

                cursor.execute(
                    sql,
                    tuple(params),
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
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
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
                    scope = self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )

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

                    if scope is None:
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

                    else:
                        trusted_tenant = str(
                            scope["tenant_id"]
                        )

                        if not self._doctor_exists_in_tenant(
                            cursor,
                            doctor_id,
                            trusted_tenant,
                        ):
                            raise ValueError(
                                "Doctor not found"
                            )

                        if not self._patient_exists_in_tenant(
                            cursor,
                            patient_id,
                            trusted_tenant,
                        ):
                            raise ValueError(
                                "Patient not found"
                            )

                    existing_sql = (
                        self._ASSIGNMENT_SELECT_BASE
                        + """
                          WHERE a.doctor_id = %s
                            AND a.patient_id = %s
                        """
                    )

                    existing_params: list[Any] = [
                        doctor_id,
                        patient_id,
                    ]

                    if scope is not None:
                        existing_sql += """
                            AND dh.tenant_id = %s
                            AND ph.tenant_id = %s
                        """

                        existing_params.extend(
                            [
                                scope["tenant_id"],
                                scope["tenant_id"],
                            ]
                        )

                    existing_sql += """
                        ORDER BY a.id ASC
                        LIMIT 1
                    """

                    cursor.execute(
                        existing_sql,
                        tuple(existing_params),
                    )

                    existing = self._row_to_assignment(
                        cursor.fetchone()
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
                            payload.get("condition"),
                            status,
                        ),
                    )

                    assignment_id = (
                        cursor.fetchone()[0]
                    )

                    created = self._select_assignment_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                        (
                            str(scope["tenant_id"])
                            if scope is not None
                            else None
                        ),
                    )

                    if created is None:
                        raise RuntimeError(
                            "Created assignment could not be reloaded"
                        )

                    return created

        finally:
            connection.close()

    def update_status(
        self,
        doctor_id: str,
        assignment_id: int,
        status: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    scope = self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )

                    if scope is None:
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
                    else:
                        cursor.execute(
                            """
                            UPDATE public.doctor_assignments AS a
                            SET status = %s
                            WHERE a.doctor_id = %s
                              AND a.id = %s
                              AND EXISTS (
                                  SELECT 1
                                  FROM public.doctors AS d
                                  JOIN public.hospitals AS dh
                                    ON dh.id = d.hospital_id
                                  WHERE d.id = a.doctor_id
                                    AND dh.tenant_id = %s
                              )
                              AND EXISTS (
                                  SELECT 1
                                  FROM public.patients AS p
                                  JOIN public.hospitals AS ph
                                    ON ph.id = p.hospital_id
                                  WHERE p.id = a.patient_id
                                    AND ph.tenant_id = %s
                              )
                            RETURNING a.id
                            """,
                            (
                                status,
                                doctor_id,
                                assignment_id,
                                scope["tenant_id"],
                                scope["tenant_id"],
                            ),
                        )

                    updated = cursor.fetchone()

                    if updated is None:
                        return None

                    return self._select_assignment_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                        (
                            str(scope["tenant_id"])
                            if scope is not None
                            else None
                        ),
                    )

        finally:
            connection.close()

    def delete(
        self,
        doctor_id: str,
        assignment_id: int,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> dict[str, Any] | None:
        connection = self._connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    scope = self._resolve_scope(
                        cursor,
                        tenant_id,
                        principal_user_id,
                    )

                    trusted_tenant = (
                        str(scope["tenant_id"])
                        if scope is not None
                        else None
                    )

                    existing = self._select_assignment_one(
                        cursor,
                        doctor_id,
                        assignment_id,
                        trusted_tenant,
                    )

                    if existing is None:
                        return None

                    if scope is None:
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
                    else:
                        cursor.execute(
                            """
                            DELETE FROM public.doctor_assignments AS a
                            WHERE a.doctor_id = %s
                              AND a.id = %s
                              AND EXISTS (
                                  SELECT 1
                                  FROM public.doctors AS d
                                  JOIN public.hospitals AS dh
                                    ON dh.id = d.hospital_id
                                  WHERE d.id = a.doctor_id
                                    AND dh.tenant_id = %s
                              )
                              AND EXISTS (
                                  SELECT 1
                                  FROM public.patients AS p
                                  JOIN public.hospitals AS ph
                                    ON ph.id = p.hospital_id
                                  WHERE p.id = a.patient_id
                                    AND ph.tenant_id = %s
                              )
                            RETURNING a.id
                            """,
                            (
                                doctor_id,
                                assignment_id,
                                scope["tenant_id"],
                                scope["tenant_id"],
                            ),
                        )

                    deleted = cursor.fetchone()

                    if deleted is None:
                        return None

                    return existing

        finally:
            connection.close()
