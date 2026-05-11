from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/nursing", tags=["Nursing"])

class NursingVitalRequest(BaseModel):
    temperature: Optional[str] = ""
    bloodPressure: Optional[str] = ""
    heartRate: Optional[str] = ""
    respiratoryRate: Optional[str] = ""
    oxygenSaturation: Optional[str] = ""
    time: Optional[str] = ""

class NursingNoteRequest(BaseModel):
    text: str

@router.get("/vitals/{patient_id}")
def get_nursing_vitals(patient_id: str):
    from ..repositories.registry import SERVICES
    return SERVICES["nursing"].list_vitals(patient_id)

@router.post("/vitals/{patient_id}")
def create_nursing_vital(patient_id: str, payload: NursingVitalRequest):
    from ..repositories.registry import SERVICES
    return SERVICES["nursing"].create_vital(patient_id, {
        "temperature": payload.temperature,
        "bloodPressure": payload.bloodPressure,
        "heartRate": payload.heartRate,
        "respiratoryRate": payload.respiratoryRate,
        "oxygenSaturation": payload.oxygenSaturation,
        "time": payload.time,
    })

@router.get("/notes/{patient_id}")
def get_nursing_notes(patient_id: str):
    from ..repositories.registry import SERVICES
    return SERVICES["nursing"].list_notes(patient_id)

@router.post("/notes/{patient_id}")
def create_nursing_note(patient_id: str, payload: NursingNoteRequest):
    from ..repositories.registry import SERVICES
    return SERVICES["nursing"].create_note(patient_id, payload.text)
