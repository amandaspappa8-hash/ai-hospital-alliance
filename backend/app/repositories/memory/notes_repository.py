from typing import Any


class InMemoryNotesRepository:
    def __init__(self, notes_store: dict[str, list[dict[str, Any]]]):
        self.notes_store = notes_store

    def list_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        return list(self.notes_store.get(patient_id, []))

    def create(self, patient_id: str, text: str) -> dict[str, Any]:
        if patient_id not in self.notes_store:
            self.notes_store[patient_id] = []

        next_id = len(self.notes_store[patient_id]) + 1
        new_note = {
            "id": next_id,
            "text": text,
        }
        self.notes_store[patient_id].append(new_note)
        return new_note
