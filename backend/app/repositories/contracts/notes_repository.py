from typing import Protocol, Any


class NotesRepositoryContract(Protocol):
    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]: ...

    def create(self, patient_id: str, text: str) -> dict[str, Any]: ...
