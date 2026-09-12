class MarService:
    def __init__(self, mar_repository):
        self.mar_repository = mar_repository

    def _scope_kwargs(
        self,
        tenant_id: str | None,
        principal_user_id: int | None,
    ) -> dict:
        scoped = (
            tenant_id is not None
            or principal_user_id is not None
        )

        if not scoped:
            return {}

        if tenant_id is None or principal_user_id is None:
            raise PermissionError(
                "Incomplete MAR tenant scope"
            )

        if not getattr(
            self.mar_repository,
            "supports_tenant_scope",
            False,
        ):
            raise PermissionError(
                "Tenant-scoped MAR repository unavailable"
            )

        return {
            "tenant_id": tenant_id,
            "principal_user_id": principal_user_id,
        }

    def list_items(
        self,
        patient_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.list_by_patient(
            patient_id,
            **scope,
        )

    def create_item(
        self,
        patient_id: str,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.create(
            patient_id,
            payload,
            **scope,
        )

    def update_item(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.update(
            patient_id,
            item_id,
            payload,
            **scope,
        )

    def set_status(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.set_status(
            patient_id,
            item_id,
            payload,
            **scope,
        )

    def set_pharmacy_review(
        self,
        patient_id: str,
        item_id: int,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.set_pharmacy_review(
            patient_id,
            item_id,
            payload,
            **scope,
        )

    def delete_item(
        self,
        patient_id: str,
        item_id: int,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ) -> bool:
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.mar_repository.delete(
            patient_id,
            item_id,
            **scope,
        )

    def resolve_item_id_by_index(
        self,
        patient_id: str,
        index: int,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        items = self.list_items(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )

        if index < 0 or index >= len(items):
            return None

        return items[index].get("id")
