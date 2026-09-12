from fastapi import HTTPException


class DoctorAssignmentsService:
    def __init__(self, assignments_repository):
        self.assignments_repository = assignments_repository

    def _scope_kwargs(
        self,
        tenant_id: str | None,
        principal_user_id: int | None,
    ) -> dict:
        has_tenant = tenant_id is not None
        has_principal = principal_user_id is not None

        if not has_tenant and not has_principal:
            return {}

        if not has_tenant or not has_principal:
            raise PermissionError(
                "Incomplete Doctor tenant scope"
            )

        if not getattr(
            self.assignments_repository,
            "supports_tenant_scope",
            False,
        ):
            raise PermissionError(
                "Tenant-scoped Doctor repository unavailable"
            )

        return {
            "tenant_id": tenant_id,
            "principal_user_id": principal_user_id,
        }

    def list_doctors(
        self,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        method = getattr(
            self.assignments_repository,
            "list_doctors",
            None,
        )

        if method is None:
            if scope:
                raise PermissionError(
                    "Tenant-scoped Doctor directory unavailable"
                )
            raise RuntimeError(
                "Doctor directory repository unavailable"
            )

        return method(**scope)

    def list_doctors_by_specialty(
        self,
        specialty: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        method = getattr(
            self.assignments_repository,
            "list_doctors_by_specialty",
            None,
        )

        if method is None:
            if scope:
                raise PermissionError(
                    "Tenant-scoped Doctor directory unavailable"
                )
            raise RuntimeError(
                "Doctor directory repository unavailable"
            )

        return method(
            specialty,
            **scope,
        )

    def get_doctor(
        self,
        doctor_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        method = getattr(
            self.assignments_repository,
            "get_doctor",
            None,
        )

        if method is None:
            if scope:
                raise PermissionError(
                    "Tenant-scoped Doctor directory unavailable"
                )
            raise RuntimeError(
                "Doctor directory repository unavailable"
            )

        return method(
            doctor_id,
            **scope,
        )

    def list_by_doctor(
        self,
        doctor_id: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        return self.assignments_repository.list_by_doctor(
            doctor_id,
            **scope,
        )

    def create(
        self,
        doctor_id: str,
        payload: dict,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        try:
            return self.assignments_repository.create(
                doctor_id,
                payload,
                **scope,
            )
        except ValueError as exc:
            raise HTTPException(
                status_code=404,
                detail=str(exc),
            ) from exc

    def update_status(
        self,
        doctor_id: str,
        assignment_id: int,
        status: str,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        assignment = (
            self.assignments_repository.update_status(
                doctor_id,
                assignment_id,
                status,
                **scope,
            )
        )

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found",
            )

        return assignment

    def delete(
        self,
        doctor_id: str,
        assignment_id: int,
        *,
        tenant_id: str | None = None,
        principal_user_id: int | None = None,
    ):
        scope = self._scope_kwargs(
            tenant_id,
            principal_user_id,
        )

        assignment = self.assignments_repository.delete(
            doctor_id,
            assignment_id,
            **scope,
        )

        if not assignment:
            raise HTTPException(
                status_code=404,
                detail="Assignment not found",
            )

        return assignment
