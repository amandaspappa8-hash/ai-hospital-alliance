from typing import Protocol, Any


class PatientsRepositoryContract(Protocol):
    def list_all(self) -> list[dict[str, Any]]: ...

    def get_by_id(self, patient_id: str) -> dict[str, Any] | None: ...
