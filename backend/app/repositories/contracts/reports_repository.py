from typing import Protocol, Any

class ReportsRepositoryContract(Protocol):
    def list_all(self) -> list[dict[str, Any]]:
        ...
