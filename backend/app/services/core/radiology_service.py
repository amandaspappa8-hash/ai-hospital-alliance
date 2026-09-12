from fastapi import HTTPException


class RadiologyService:
    def __init__(self, radiology_repository):
        self.radiology_repository = radiology_repository

    def get_catalog(self):
        return self.radiology_repository.get_catalog()

    def list_orders(
        self,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.radiology_repository,
            "supports_tenant_scope",
            False,
        ):
            return self.radiology_repository.list_orders(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

        return self.radiology_repository.list_orders()

    def list_orders_by_patient(
        self,
        patient_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.radiology_repository,
            "supports_tenant_scope",
            False,
        ):
            return self.radiology_repository.list_orders_by_patient(
                patient_id,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

        return self.radiology_repository.list_orders_by_patient(
            patient_id
        )

    def create_order(
        self,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.radiology_repository,
            "supports_tenant_scope",
            False,
        ):
            return self.radiology_repository.create_order(
                payload,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )

        return self.radiology_repository.create_order(
            payload
        )

    def set_result(
        self,
        order_id: str | int,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        if getattr(
            self.radiology_repository,
            "supports_tenant_scope",
            False,
        ):
            order = self.radiology_repository.set_result(
                order_id,
                payload,
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )
        else:
            order = self.radiology_repository.set_result(
                order_id,
                payload,
            )

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Radiology order not found",
            )

        return order

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None:
        if not getattr(
            self.radiology_repository,
            "supports_tenant_scope",
            False,
        ):
            raise PermissionError(
                "Tenant-scoped Radiology patient authorization unavailable"
            )

        authorize = getattr(
            self.radiology_repository,
            "authorize_patient_access",
            None,
        )

        if not callable(authorize):
            raise PermissionError(
                "Tenant-scoped Radiology patient authorization unavailable"
            )

        authorize(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
