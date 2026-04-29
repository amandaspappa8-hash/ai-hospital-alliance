from typing import Any


class InMemoryAppointmentsRepository:
    def __init__(self, appointments_store: list[dict[str, Any]]):
        self.appointments_store = appointments_store

    def list_all(self) -> list[dict[str, Any]]:
        return list(self.appointments_store)

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        next_id = f"A-{2000 + len(self.appointments_store) + 1}"
        new_appointment = {
            "id": next_id,
            "patientId": payload.get("patientId", ""),
            "patientName": payload.get("patientName", ""),
            "department": payload.get("department", ""),
            "doctor": payload.get("doctor", ""),
            "date": payload.get("date", ""),
            "time": payload.get("time", ""),
            "status": payload.get("status", "Scheduled"),
        }
        self.appointments_store.append(new_appointment)
        return new_appointment
