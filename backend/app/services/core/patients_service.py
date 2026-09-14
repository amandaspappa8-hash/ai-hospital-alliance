from fastapi import HTTPException


class PatientsService:
    def __init__(self, patients_repository):
        self.patients_repository = patients_repository

    def list_patients(
        self,
        tenant_id: str,
        principal_user_id: int,
    ):
        try:
            return self.patients_repository.list_all(
                tenant_id,
                principal_user_id,
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc

    def get_patient(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
    ):
        try:
            patient = self.patients_repository.get_by_id(
                patient_id,
                tenant_id,
                principal_user_id,
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc

        if not patient:
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            )

        return patient

    def create_patient(
        self,
        data: dict,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ):
        try:
            return self.patients_repository.create(
                data,
                tenant_id,
                principal_user_id,
                ip_address,
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

    def update_patient(
        self,
        patient_id: str,
        data: dict,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ):
        try:
            patient = self.patients_repository.update(
                patient_id,
                data,
                tenant_id,
                principal_user_id,
                ip_address,
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc

        if patient is None:
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            )

        return patient

    def delete_patient(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ):
        try:
            deleted = self.patients_repository.delete(
                patient_id,
                tenant_id,
                principal_user_id,
                ip_address,
            )
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            )

        return True

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None:
        authorize = getattr(
            self.patients_repository,
            "authorize_patient_access",
            None,
        )

        if not callable(authorize):
            raise PermissionError(
                "Canonical patient authorization unavailable"
            )

        authorize(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
