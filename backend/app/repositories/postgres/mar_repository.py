from sqlalchemy import text


class PostgresMarRepository:
    supports_tenant_scope = True

    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def _serialize(row):
        if row is None:
            return None

        mapping = (
            row._mapping
            if hasattr(row, "_mapping")
            else row
        )

        return {
            "id": mapping["id"],
            "medication": mapping["medication"],
            "dose": mapping["dose"],
            "route": mapping["route"],
            "schedule": mapping["schedule"],
            "status": mapping["status"],
            "givenAt": mapping["given_at"] or "",
            **(
                {
                    "pharmacyReview":
                        mapping["pharmacy_review"]
                }
                if mapping.get("pharmacy_review")
                is not None
                else {}
            ),
            **(
                {
                    "aiFlag":
                        mapping["ai_flag"]
                }
                if mapping.get("ai_flag")
                is not None
                else {}
            ),
        }

    @staticmethod
    def _select_columns(alias: str = "mi"):
        return f"""
            {alias}.id,
            {alias}.patient_id,
            {alias}.medication,
            {alias}.dose,
            {alias}.route,
            {alias}.schedule,
            {alias}.status,
            {alias}.given_at,
            {alias}.pharmacy_review,
            {alias}.ai_flag
        """

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
        connection,
        tenant_id: str,
        principal_user_id: int,
    ):
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
        connection,
        patient_id: str,
        tenant_id: str,
    ) -> None:
        exists = connection.execute(
            text(
                """
                SELECT 1
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
            raise ValueError(
                "Patient not found"
            )

    def list_by_patient(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        with self.engine.connect() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            rows = connection.execute(
                text(
                    f"""
                    SELECT
                        {self._select_columns("mi")}
                    FROM public.mar_items AS mi
                    JOIN public.patients AS p
                      ON p.id = mi.patient_id
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE mi.patient_id = :patient_id
                      AND h.tenant_id = :tenant_id
                    ORDER BY mi.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                },
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create(
        self,
        patient_id: str,
        payload: dict,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            self._validate_patient(
                connection,
                patient_id,
                str(scope["tenant_id"]),
            )

            row = connection.execute(
                text(
                    f"""
                    INSERT INTO public.mar_items (
                        patient_id,
                        medication,
                        dose,
                        route,
                        schedule,
                        status,
                        given_at,
                        pharmacy_review,
                        ai_flag,
                        created_at,
                        updated_at
                    )
                    SELECT
                        p.id,
                        :medication,
                        :dose,
                        :route,
                        :schedule,
                        :status,
                        :given_at,
                        NULL,
                        NULL,
                        CURRENT_TIMESTAMP,
                        CURRENT_TIMESTAMP
                    FROM public.patients AS p
                    JOIN public.hospitals AS h
                      ON h.id = p.hospital_id
                    WHERE p.id = :patient_id
                      AND h.tenant_id = :tenant_id
                    RETURNING
                        {self._select_columns("mar_items")}
                    """
                ),
                {
                    "patient_id": patient_id,
                    "tenant_id": scope["tenant_id"],
                    "medication": payload["medication"],
                    "dose": payload.get("dose"),
                    "route": payload.get("route"),
                    "schedule": payload.get("schedule"),
                    "status":
                        payload.get("status")
                        or "Pending",
                    "given_at":
                        payload.get("givenAt")
                        or "",
                },
            ).fetchone()

            if row is None:
                raise ValueError(
                    "Patient not found"
                )

        return self._serialize(row)

    def update(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    f"""
                    UPDATE public.mar_items AS mi
                    SET
                        medication = :medication,
                        dose = :dose,
                        route = :route,
                        schedule = :schedule,
                        status =
                            COALESCE(
                                :status,
                                mi.status
                            ),
                        given_at =
                            COALESCE(
                                :given_at,
                                mi.given_at
                            ),
                        updated_at =
                            CURRENT_TIMESTAMP
                    WHERE mi.patient_id = :patient_id
                      AND mi.id = :item_id
                      AND EXISTS (
                          SELECT 1
                          FROM public.patients AS p
                          JOIN public.hospitals AS h
                            ON h.id = p.hospital_id
                          WHERE p.id = mi.patient_id
                            AND h.tenant_id = :tenant_id
                      )
                    RETURNING
                        {self._select_columns("mi")}
                    """
                ),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "tenant_id": scope["tenant_id"],
                    "medication": payload["medication"],
                    "dose": payload.get("dose"),
                    "route": payload.get("route"),
                    "schedule": payload.get("schedule"),
                    "status": payload.get("status"),
                    "given_at": payload.get("givenAt"),
                },
            ).fetchone()

        return self._serialize(row)

    def set_status(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    f"""
                    UPDATE public.mar_items AS mi
                    SET
                        status = :status,
                        given_at =
                            COALESCE(
                                :given_at,
                                mi.given_at
                            ),
                        updated_at =
                            CURRENT_TIMESTAMP
                    WHERE mi.patient_id = :patient_id
                      AND mi.id = :item_id
                      AND EXISTS (
                          SELECT 1
                          FROM public.patients AS p
                          JOIN public.hospitals AS h
                            ON h.id = p.hospital_id
                          WHERE p.id = mi.patient_id
                            AND h.tenant_id = :tenant_id
                      )
                    RETURNING
                        {self._select_columns("mi")}
                    """
                ),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "tenant_id": scope["tenant_id"],
                    "status": payload["status"],
                    "given_at": payload.get("givenAt"),
                },
            ).fetchone()

        return self._serialize(row)

    def set_pharmacy_review(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str,
        principal_user_id: int,
    ):
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            row = connection.execute(
                text(
                    f"""
                    UPDATE public.mar_items AS mi
                    SET
                        pharmacy_review =
                            :pharmacy_review,
                        updated_at =
                            CURRENT_TIMESTAMP
                    WHERE mi.patient_id = :patient_id
                      AND mi.id = :item_id
                      AND EXISTS (
                          SELECT 1
                          FROM public.patients AS p
                          JOIN public.hospitals AS h
                            ON h.id = p.hospital_id
                          WHERE p.id = mi.patient_id
                            AND h.tenant_id = :tenant_id
                      )
                    RETURNING
                        {self._select_columns("mi")}
                    """
                ),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "tenant_id": scope["tenant_id"],
                    "pharmacy_review":
                        payload.get("status")
                        or "Reviewed",
                },
            ).fetchone()

        return self._serialize(row)

    def delete(
        self,
        patient_id: str,
        item_id: int,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> bool:
        with self.engine.begin() as connection:
            scope = self._resolve_scope(
                connection,
                tenant_id,
                principal_user_id,
            )

            deleted = connection.execute(
                text(
                    """
                    DELETE FROM public.mar_items AS mi
                    WHERE mi.patient_id = :patient_id
                      AND mi.id = :item_id
                      AND EXISTS (
                          SELECT 1
                          FROM public.patients AS p
                          JOIN public.hospitals AS h
                            ON h.id = p.hospital_id
                          WHERE p.id = mi.patient_id
                            AND h.tenant_id = :tenant_id
                      )
                    RETURNING mi.id
                    """
                ),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "tenant_id": scope["tenant_id"],
                },
            ).fetchone()

        return deleted is not None
