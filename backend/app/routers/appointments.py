from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Appointments"])

class AppointmentRequest(BaseModel):
    patientId: Optional[str] = ""
    patientName: Optional[str] = ""
    patient: Optional[str] = ""
    department: Optional[str] = ""
    doctor: Optional[str] = ""
    date: Optional[str] = ""
    time: Optional[str] = ""
    status: Optional[str] = "Scheduled"

@router.get("/appointments")
def get_appointments():
    from ..repositories.registry import SERVICES
    return SERVICES["appointments"].list_appointments()

@router.post("/appointments")
def create_appointment(payload: AppointmentRequest):
    from ..repositories.registry import SERVICES
    return SERVICES["appointments"].create_appointment({
        "patientId": payload.patientId or "",
        "patientName": payload.patientName or payload.patient or "",
        "department": payload.department,
        "doctor": payload.doctor,
        "date": payload.date or "",
        "time": payload.time,
        "status": payload.status or "Scheduled",
    })
