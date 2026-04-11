from typing import Any

class InMemoryPatientsRepository:
    def __init__(self, patients_store: list[dict[str, Any]]):
        self.patients_store = patients_store

    def list_all(self) -> list[dict[str, Any]]:
        return list(self.patients_store)

    def get_by_id(self, patient_id: str) -> dict[str, Any] | None:
        for patient in self.patients_store:
            if patient.get("id") == patient_id:
                return patient
        return None
