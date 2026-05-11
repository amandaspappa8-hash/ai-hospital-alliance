from fastapi import Depends
from .deps import get_current_user
from fastapi import Depends
from .deps import get_current_user, rate_limit_middleware
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Doctors"], dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)])

class DoctorAssignmentRequest(BaseModel):
    patientId: str
    patientName: str
    department: str
    condition: str
    status: Optional[str] = "Assigned"

class DoctorAssignmentStatusRequest(BaseModel):
    status: str

@router.get("/doctors/summary")
def get_doctors_summary():
    from ..main import DOCTORS
    return DOCTORS

@router.get("/doctors/by-specialty/{name}")
def get_doctors_by_specialty(name: str):
    from ..main import DOCTORS
    normalized = name.strip().lower()
    return [d for d in DOCTORS if d["specialty"].strip().lower() == normalized]

@router.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: str):
    from ..main import DOCTORS
    for doctor in DOCTORS:
        if doctor["id"] == doctor_id:
            return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")

@router.get("/doctor-assignments/{doctor_id}")
def get_doctor_assignments(doctor_id: str):
    from ..main import DOCTOR_ASSIGNMENTS
    return DOCTOR_ASSIGNMENTS.get(doctor_id, [])

@router.post("/doctor-assignments/{doctor_id}")
def create_doctor_assignment(doctor_id: str, payload: DoctorAssignmentRequest):
    from ..main import DOCTOR_ASSIGNMENTS
    if doctor_id not in DOCTOR_ASSIGNMENTS:
        DOCTOR_ASSIGNMENTS[doctor_id] = []
    existing = next((i for i in DOCTOR_ASSIGNMENTS[doctor_id] if i["patientId"] == payload.patientId), None)
    if existing:
        return existing
    new_assignment = {
        "id": len(DOCTOR_ASSIGNMENTS[doctor_id]) + 1,
        "patientId": payload.patientId,
        "patientName": payload.patientName,
        "department": payload.department,
        "condition": payload.condition,
        "status": payload.status or "Assigned",
    }
    DOCTOR_ASSIGNMENTS[doctor_id].append(new_assignment)
    return new_assignment

@router.post("/doctor-assignments/{doctor_id}/{assignment_id}/status")
def update_assignment_status(doctor_id: str, assignment_id: int, payload: DoctorAssignmentStatusRequest):
    from ..main import DOCTOR_ASSIGNMENTS
    for item in DOCTOR_ASSIGNMENTS.get(doctor_id, []):
        if item["id"] == assignment_id:
            item["status"] = payload.status
            return item
    raise HTTPException(status_code=404, detail="Assignment not found")

@router.delete("/doctor-assignments/{doctor_id}/{assignment_id}")
def delete_doctor_assignment(doctor_id: str, assignment_id: int):
    from ..main import DOCTOR_ASSIGNMENTS
    assignments = DOCTOR_ASSIGNMENTS.get(doctor_id, [])
    for index, item in enumerate(assignments):
        if item["id"] == assignment_id:
            return assignments.pop(index)
    raise HTTPException(status_code=404, detail="Assignment not found")

@router.get("/specialties/summary")
def get_specialties_summary():
    from ..main import SPECIALTIES_SUMMARY
    return SPECIALTIES_SUMMARY
