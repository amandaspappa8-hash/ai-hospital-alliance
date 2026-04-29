from typing import Protocol, Any


class AppointmentsRepositoryContract(Protocol):
    def list_all(self) -> list[dict[str, Any]]: ...

    def create(self, payload: dict[str, Any]) -> dict[str, Any]: ...
