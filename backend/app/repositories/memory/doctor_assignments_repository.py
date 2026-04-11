from typing import Any

class InMemoryDoctorAssignmentsRepository:
    def __init__(self, assignments_store: dict[str, list[dict[str, Any]]]):
        self.assignments_store = assignments_store

    def list_by_doctor(self, doctor_id: str) -> list[dict[str, Any]]:
        return list(self.assignments_store.get(doctor_id, []))

    def create(self, doctor_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if doctor_id not in self.assignments_store:
            self.assignments_store[doctor_id] = []

        next_id = len(self.assignments_store[doctor_id]) + 1
        new_assignment = {
            "id": next_id,
            "patientId": payload.get("patientId", ""),
            "patientName": payload.get("patientName", ""),
            "specialty": payload.get("specialty", ""),
            "priority": payload.get("priority", "routine"),
            "status": payload.get("status", "Pending"),
        }
        self.assignments_store[doctor_id].append(new_assignment)
        return new_assignment

    def update_status(self, doctor_id: str, assignment_id: int, status: str) -> dict[str, Any] | None:
        for assignment in self.assignments_store.get(doctor_id, []):
            if assignment.get("id") == assignment_id:
                assignment["status"] = status
                return assignment
        return None

    def delete(self, doctor_id: str, assignment_id: int) -> dict[str, Any] | None:
        items = self.assignments_store.get(doctor_id, [])
        for i, assignment in enumerate(items):
            if assignment.get("id") == assignment_id:
                return items.pop(i)
        return None
