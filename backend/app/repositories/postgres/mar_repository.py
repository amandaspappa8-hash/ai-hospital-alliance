from sqlalchemy import text


class PostgresMarRepository:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def _serialize(row):
        if row is None:
            return None

        mapping = row._mapping if hasattr(row, "_mapping") else row

        return {
            "id": mapping["id"],
            "medication": mapping["medication"],
            "dose": mapping["dose"],
            "route": mapping["route"],
            "schedule": mapping["schedule"],
            "status": mapping["status"],
            "givenAt": mapping["given_at"] or "",
            **(
                {"pharmacyReview": mapping["pharmacy_review"]}
                if mapping.get("pharmacy_review") is not None
                else {}
            ),
            **(
                {"aiFlag": mapping["ai_flag"]}
                if mapping.get("ai_flag") is not None
                else {}
            ),
        }

    @staticmethod
    def _select_columns():
        return """
            id,
            patient_id,
            medication,
            dose,
            route,
            schedule,
            status,
            given_at,
            pharmacy_review,
            ai_flag
        """

    def _validate_patient(self, connection, patient_id: str) -> None:
        exists = connection.execute(
            text("""
                SELECT 1
                FROM public.patients
                WHERE id = :patient_id
                LIMIT 1
            """),
            {"patient_id": patient_id},
        ).scalar()

        if exists is None:
            raise ValueError("Patient not found")

    def list_by_patient(self, patient_id: str):
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(f"""
                    SELECT {self._select_columns()}
                    FROM public.mar_items
                    WHERE patient_id = :patient_id
                    ORDER BY id
                """),
                {"patient_id": patient_id},
            ).fetchall()

        return [
            self._serialize(row)
            for row in rows
        ]

    def create(self, patient_id: str, payload: dict):
        with self.engine.begin() as connection:
            self._validate_patient(connection, patient_id)

            row = connection.execute(
                text(f"""
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
                    VALUES (
                        :patient_id,
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
                    )
                    RETURNING {self._select_columns()}
                """),
                {
                    "patient_id": patient_id,
                    "medication": payload["medication"],
                    "dose": payload.get("dose"),
                    "route": payload.get("route"),
                    "schedule": payload.get("schedule"),
                    "status": payload.get("status") or "Pending",
                    "given_at": payload.get("givenAt") or "",
                },
            ).fetchone()

        return self._serialize(row)

    def update(self, patient_id: str, item_id: int, payload: dict):
        with self.engine.begin() as connection:
            row = connection.execute(
                text(f"""
                    UPDATE public.mar_items
                    SET
                        medication = :medication,
                        dose = :dose,
                        route = :route,
                        schedule = :schedule,
                        status = COALESCE(:status, status),
                        given_at = COALESCE(:given_at, given_at),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE patient_id = :patient_id
                      AND id = :item_id
                    RETURNING {self._select_columns()}
                """),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "medication": payload["medication"],
                    "dose": payload.get("dose"),
                    "route": payload.get("route"),
                    "schedule": payload.get("schedule"),
                    "status": payload.get("status"),
                    "given_at": payload.get("givenAt"),
                },
            ).fetchone()

        return self._serialize(row)

    def set_status(self, patient_id: str, item_id: int, payload: dict):
        with self.engine.begin() as connection:
            row = connection.execute(
                text(f"""
                    UPDATE public.mar_items
                    SET
                        status = :status,
                        given_at = COALESCE(:given_at, given_at),
                        updated_at = CURRENT_TIMESTAMP
                    WHERE patient_id = :patient_id
                      AND id = :item_id
                    RETURNING {self._select_columns()}
                """),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "status": payload["status"],
                    "given_at": payload.get("givenAt"),
                },
            ).fetchone()

        return self._serialize(row)

    def set_pharmacy_review(self, patient_id: str, item_id: int, payload: dict):
        with self.engine.begin() as connection:
            row = connection.execute(
                text(f"""
                    UPDATE public.mar_items
                    SET
                        pharmacy_review = :pharmacy_review,
                        updated_at = CURRENT_TIMESTAMP
                    WHERE patient_id = :patient_id
                      AND id = :item_id
                    RETURNING {self._select_columns()}
                """),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                    "pharmacy_review": payload.get("status") or "Reviewed",
                },
            ).fetchone()

        return self._serialize(row)

    def delete(self, patient_id: str, item_id: int) -> bool:
        with self.engine.begin() as connection:
            deleted = connection.execute(
                text("""
                    DELETE FROM public.mar_items
                    WHERE patient_id = :patient_id
                      AND id = :item_id
                    RETURNING id
                """),
                {
                    "patient_id": patient_id,
                    "item_id": int(item_id),
                },
            ).fetchone()

        return deleted is not None
