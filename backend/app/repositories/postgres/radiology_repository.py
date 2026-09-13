from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Connection, Engine


class PostgresRadiologyRepository:
    supports_tenant_scope = True
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
    def _parse_principal_user_id(
        principal_user_id: int,
    ) -> int:
        try:
            value = int(principal_user_id)
        except (TypeError, ValueError) as exc:
            raise PermissionError(
                "Invalid authenticated principal"
            ) from exc

        if value <= 0:
            raise PermissionError(
                "Invalid authenticated principal"
            )

        return value

    def _resolve_scope(
        self,
        connection: Connection,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, str | int]:
        claimed_tenant_id = str(
            tenant_id or ""
        ).strip()

        if not claimed_tenant_id:
            raise PermissionError(
                "Authenticated tenant unavailable"
            )

        user_id = self._parse_principal_user_id(
            principal_user_id
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
                """
            ),
            {
                "user_id": user_id,
            },
        ).mappings().one_or_none()

        if row is None:
            raise PermissionError(
                "Authenticated principal has no tenant scope"
            )

        derived_tenant_id = str(
            row.get("tenant_id") or ""
        ).strip()

        hospital_id = str(
            row.get("hospital_id") or ""
        ).strip()

        if (
            not derived_tenant_id
            or not hospital_id
        ):
            raise PermissionError(
                "Authenticated principal has incomplete tenant scope"
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

    def _validate_patient(
        self,
        connection: Connection,
        patient_id: str,
        tenant_id: str,
    ) -> str:
        patient_name = connection.execute(
            text(
                """
                SELECT p.name
                FROM public.patients AS p
                JOIN public.hospitals AS h
                  ON h.id = p.hospital_id
                WHERE p.id = :patient_id
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

        return str(patient_name)

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None:
        with self.engine.connect() as connection:
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
                      AND h.tenant_id = :tenant_id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).scalar_one_or_none()

        if allowed is None:
            raise PermissionError(
                "Patient is outside authenticated tenant scope"
            )

    @staticmethod
    def _json_value(
        value: Any,
        default: Any,
    ) -> Any:
        if value is None:
            return default

        if isinstance(value, str):
            try:
                return json.loads(value)
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

    def get_catalog(
        self,
    ) -> dict[str, Any]:
        return self.catalog_store

    def list_orders(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

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
                    FROM public.radiology_orders AS ro
                    JOIN public.patients AS p
                      ON p.id = ro.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE h.tenant_id = :tenant_id
                    ORDER BY
                        ro.created_at NULLS LAST,
                        ro.id
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                },
            ).all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def list_orders_by_patient(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

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
                    FROM public.radiology_orders AS ro
                    JOIN public.patients AS p
                      ON p.id = ro.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE ro.patient_id = :patient_id
                      AND h.tenant_id = :tenant_id
                    ORDER BY
                        ro.created_at NULLS LAST,
                        ro.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).all()

        return [
            self._serialize(row)
            for row in rows
        ]

    def list_dashboard_studies(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]:
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                text(
                    """
                    SELECT
                        ro.id,
                        ro.patient_id,
                        ro.study_uid,
                        ro.studies,
                        ro.created_at,
                        h.tenant_id
                    FROM public.radiology_orders AS ro
                    JOIN public.patients AS p
                      ON p.id = ro.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE h.tenant_id = :tenant_id
                    ORDER BY
                        ro.created_at DESC NULLS LAST,
                        ro.id
                    """
                ),
                {
                    "tenant_id": scope["tenant_id"],
                },
            ).mappings().all()

        dashboard_studies: list[dict[str, Any]] = []

        for row in rows:
            studies = list(
                self._json_value(
                    row["studies"],
                    [],
                )
                or []
            )

            order_uid = row["study_uid"]

            if not studies and order_uid:
                studies = [{}]

            for item in studies:
                if not isinstance(item, dict):
                    continue

                study_uid = (
                    item.get("study_uid")
                    or item.get("studyUid")
                    or item.get("dicom_study_uid")
                    or item.get("StudyInstanceUID")
                )

                if (
                    not study_uid
                    and len(studies) == 1
                ):
                    study_uid = order_uid

                dashboard_studies.append(
                    {
                        "id": (
                            item.get("id")
                            or row["id"]
                        ),
                        "tenant_id": row["tenant_id"],
                        "patient_id": row["patient_id"],
                        "study_uid": study_uid,
                        "modality": item.get("modality"),
                        "description": (
                            item.get("description")
                            or item.get("study_description")
                        ),
                        "ohif_url": (
                            item.get("ohif_url")
                            or item.get("ohif_viewer_url")
                        ),
                        "dicom_study_uid": (
                            item.get("dicom_study_uid")
                            or item.get("StudyInstanceUID")
                            or study_uid
                        ),
                        "orthanc_id": item.get("orthanc_id"),
                        "created_at": (
                            item.get("created_at")
                            or row["created_at"]
                        ),
                    }
                )

        return dashboard_studies

    def get_study_by_uid(
        self,
        study_uid: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None:
        requested_uid = str(study_uid)

        for study in self.list_dashboard_studies(
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        ):
            identifiers = (
                study.get("study_uid"),
                study.get("dicom_study_uid"),
            )

            if any(
                value is not None
                and str(value) == requested_uid
                for value in identifiers
            ):
                return {
                    "patient_id": study.get("patient_id"),
                    "study_uid": study.get("study_uid"),
                    "modality": study.get("modality"),
                    "description": study.get("description"),
                    "ohif_url": study.get("ohif_url"),
                    "dicom_study_uid": study.get(
                        "dicom_study_uid"
                    ),
                    "orthanc_id": study.get("orthanc_id"),
                }

        return None

    def create_order(
        self,
        payload: dict[str, Any],
        *,
        tenant_id: str,
        principal_user_id: int,
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

        study_uid = (
            payload.get("study_uid")
            or payload.get("studyUid")
            or payload.get("dicom_study_uid")
            or payload.get("StudyInstanceUID")
        )

        if not study_uid:
            for study in studies:
                if not isinstance(study, dict):
                    continue

                study_uid = (
                    study.get("study_uid")
                    or study.get("studyUid")
                    or study.get("dicom_study_uid")
                    or study.get("StudyInstanceUID")
                )

                if study_uid:
                    break

        if study_uid is not None:
            study_uid = str(study_uid)

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
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            patient_name = self._validate_patient(
                connection,
                patient_id,
                str(scope["tenant_id"]),
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
                    "lock_key": self._ID_LOCK_KEY,
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
                    FROM public.radiology_orders
                    WHERE id ~ '^RAD-[0-9]+$'
                    """
                )
            ).scalar_one()

            next_number = (
                max(
                    5000,
                    int(max_suffix or 5000),
                )
                + 1
            )

            order_id = f"RAD-{next_number}"

            row = connection.execute(
                text(
                    """
                    INSERT INTO public.radiology_orders (
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
                    SELECT
                        :id,
                        p.id,
                        NULL,
                        :section,
                        CAST(:studies AS JSON),
                        :priority,
                        :status,
                        :study_uid,
                        :report,
                        NULL,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
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
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                    "section": (
                        payload.get(
                            "section",
                            "",
                        )
                        or ""
                    ),
                    "studies": json.dumps(studies),
                    "priority": priority,
                    "status": status,
                    "study_uid": study_uid,
                    "report": report,
                },
            ).one_or_none()

            if row is None:
                raise ValueError(
                    "Patient not found"
                )

            mapping = dict(row._mapping)
            mapping["patient_name"] = patient_name

            class RowAdapter:
                def __init__(
                    self,
                    values: dict[str, Any],
                ) -> None:
                    self._mapping = values

            return self._serialize(
                RowAdapter(mapping)
            )

    def set_result(
        self,
        order_id: str | int,
        payload: dict[str, Any],
        *,
        tenant_id: str,
        principal_user_id: int,
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
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            patient_id = connection.execute(
                text(
                    """
                    UPDATE public.radiology_orders AS ro
                    SET
                        report = :report,
                        status = :status,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE ro.id = :order_id
                      AND EXISTS (
                          SELECT 1
                          FROM public.patients AS p
                          JOIN public.hospitals AS h
                            ON h.id = p.hospital_id
                          WHERE p.id = ro.patient_id
                            AND h.tenant_id = :tenant_id
                      )
                    RETURNING ro.patient_id
                    """
                ),
                {
                    "order_id": str(order_id),
                    "report": report,
                    "status": status,
                    "tenant_id": scope["tenant_id"],
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
                    FROM public.radiology_orders AS ro
                    JOIN public.patients AS p
                      ON p.id = ro.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE ro.id = :order_id
                      AND h.tenant_id = :tenant_id
                    """
                ),
                {
                    "order_id": str(order_id),
                    "tenant_id": scope["tenant_id"],
                },
            ).one_or_none()

            if row is None:
                return None

            return self._serialize(row)
