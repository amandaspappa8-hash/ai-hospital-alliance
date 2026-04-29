from fastapi import HTTPException


class DoctorAssignmentsService:
    def __init__(self, assignments_repository):
        self.assignments_repository = assignments_repository

    def list_by_doctor(self, doctor_id: str):
        return self.assignments_repository.list_by_doctor(doctor_id)

    def create(self, doctor_id: str, payload: dict):
        return self.assignments_repository.create(doctor_id, payload)

    def update_status(self, doctor_id: str, assignment_id: int, status: str):
        assignment = self.assignments_repository.update_status(
            doctor_id, assignment_id, status
        )
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return assignment

    def delete(self, doctor_id: str, assignment_id: int):
        assignment = self.assignments_repository.delete(doctor_id, assignment_id)
        if not assignment:
            raise HTTPException(status_code=404, detail="Assignment not found")
        return {"success": True, "deleted": assignment}
