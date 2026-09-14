from typing import Any, Protocol


class PatientsRepositoryContract(Protocol):
    def list_all(
        self,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]: ...

    def get_by_id(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None: ...

    def create(
        self,
        patient: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any]: ...

    def update(
        self,
        patient_id: str,
        changes: dict[str, Any],
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> dict[str, Any] | None: ...

    def delete(
        self,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        ip_address: str | None = None,
    ) -> bool: ...

    def authorize_patient_access(
        self,
        patient_id: str,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> None: ...
