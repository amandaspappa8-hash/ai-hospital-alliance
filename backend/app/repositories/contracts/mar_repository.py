from typing import Protocol, Any

class MarRepositoryContract(Protocol):
    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        ...

    def create(self, patient_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        ...
