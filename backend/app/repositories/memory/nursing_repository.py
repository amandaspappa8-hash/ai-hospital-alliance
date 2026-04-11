from typing import Any

class InMemoryNursingRepository:
    def __init__(self, vitals_store: dict[str, list[dict[str, Any]]], notes_store: dict[str, list[dict[str, Any]]]):
        self.vitals_store = vitals_store
        self.notes_store = notes_store

    def list_vitals(self, patient_id: str) -> list[dict[str, Any]]:
        return list(self.vitals_store.get(patient_id, []))

    def create_vital(self, patient_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if patient_id not in self.vitals_store:
            self.vitals_store[patient_id] = []

        next_id = len(self.vitals_store[patient_id]) + 1
        new_vital = {
            "id": next_id,
            "temperature": payload.get("temperature", ""),
            "bloodPressure": payload.get("bloodPressure", ""),
            "heartRate": payload.get("heartRate", ""),
            "respiratoryRate": payload.get("respiratoryRate", ""),
            "oxygenSaturation": payload.get("oxygenSaturation", ""),
            "time": payload.get("time", ""),
        }
        self.vitals_store[patient_id].append(new_vital)
        return new_vital

    def list_notes(self, patient_id: str) -> list[dict[str, Any]]:
        return list(self.notes_store.get(patient_id, []))

    def create_note(self, patient_id: str, text: str) -> dict[str, Any]:
        if patient_id not in self.notes_store:
            self.notes_store[patient_id] = []

        next_id = len(self.notes_store[patient_id]) + 1
        new_note = {
            "id": next_id,
            "text": text,
        }
        self.notes_store[patient_id].append(new_note)
        return new_note
