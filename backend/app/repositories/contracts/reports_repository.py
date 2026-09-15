from typing import Protocol, Any


class ReportsRepositoryContract(Protocol):
    def list_all(self) -> list[dict[str, Any]]: ...

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]: ...

    def create_for_principal(
        self,
        *,
        patient_id: str,
        tenant_id: str,
        principal_user_id: int,
        title: str,
        report_type: str,
        summary: str,
        content: str,
        status: str,
    ) -> dict[str, Any]: ...

    def register_verification_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any]: ...

    def get_verification_for_principal(
        self,
        *,
        report_id: str,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict[str, Any] | None: ...
