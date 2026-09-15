from typing import Protocol, Any


class ReportsRepositoryContract(Protocol):
    def list_all(self) -> list[dict[str, Any]]: ...

    def list_for_principal(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> list[dict[str, Any]]: ...
