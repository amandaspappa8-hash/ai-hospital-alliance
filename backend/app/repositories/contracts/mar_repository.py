from typing import Protocol, Any


class MarRepositoryContract(Protocol):
    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]: ...

    def create(self, patient_id: str, payload: dict[str, Any]) -> dict[str, Any]: ...

    def update(self, patient_id: str, item_id: int, payload: dict):
        raise NotImplementedError

    def set_status(self, patient_id: str, item_id: int, payload: dict):
        raise NotImplementedError

    def set_pharmacy_review(self, patient_id: str, item_id: int, payload: dict):
        raise NotImplementedError

    def delete(self, patient_id: str, item_id: int) -> bool:
        raise NotImplementedError
