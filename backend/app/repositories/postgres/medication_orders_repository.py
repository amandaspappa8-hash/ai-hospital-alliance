from typing import Any

from sqlalchemy import text


class PostgresMedicationOrdersRepository:
    """Hospital/tenant-scoped read adapter for medication orders.

    Scope is derived from the authenticated principal. The caller cannot
    supply hospital_id. tenant_id is treated only as the authenticated
    tenant claim and must match server-derived principal scope.
    """

    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def _parse_principal_user_id(
        principal_user_id: int,
    ) -> int:
        try:
            user_id = int(principal_user_id)
        except (TypeError, ValueError) as exc:
            raise PermissionError(
                "Authenticated principal is invalid"
            ) from exc

        if user_id <= 0:
            raise PermissionError(
                "Authenticated principal is invalid"
            )

        return user_id

    def _resolve_scope(
        self,
        connection,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]:
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
                "Authenticated principal scope is unresolved"
            )

        row = rows[0]

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
                "Authenticated principal has incomplete scope"
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
    def _serialize(row) -> dict:
        mapping = getattr(row, "_mapping", row)

        return {
            "id": mapping["id"],
            "patient_id": mapping["patient_id"],
            "drug_name": mapping["drug_name"],
            "generic_name": mapping["generic_name"],
            "dose": mapping["dose"],
            "route": mapping["route"],
            "frequency": mapping["frequency"],
            "duration_days": mapping["duration_days"],
            "quantity": mapping["quantity"],
            "is_active": mapping["is_active"],
            "created_at": mapping["created_at"],
        }

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
        limit: int = 50,
    ) -> list[dict]:
        try:
            limit = int(limit)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Medication order limit must be an integer"
            ) from exc

        if limit < 1 or limit > 50:
            raise ValueError(
                "Medication order limit must be between 1 and 50"
            )

        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = (
                connection.execute(
                    text(
                        """
                        SELECT
                            mo.id,
                            mo.patient_id,
                            mo.drug_name,
                            mo.generic_name,
                            mo.dose,
                            mo.route,
                            mo.frequency,
                            mo.duration_days,
                            mo.quantity,
                            mo.is_active,
                            mo.created_at
                        FROM public.medication_orders_simple AS mo
                        JOIN public.patients AS p
                          ON p.id = mo.patient_id
                        JOIN public.hospitals AS h
                          ON h.id = p.hospital_id
                        WHERE p.hospital_id = :hospital_id
                          AND h.tenant_id = :tenant_id
                        ORDER BY mo.id DESC
                        LIMIT :limit
                        """
                    ),
                    {
                        "hospital_id": scope["hospital_id"],
                        "tenant_id": scope["tenant_id"],
                        "limit": limit,
                    },
                )
                .mappings()
                .all()
            )

        return [
            self._serialize(row)
            for row in rows
        ]
