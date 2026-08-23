from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/enterprise-mar", tags=["Enterprise MAR"])

MAR = []

@router.post("/give")
def give_medication(payload: dict):
    entry = {
        "patient_id": payload.get("patient_id"),
        "drug": payload.get("drug"),
        "dose": payload.get("dose"),
        "nurse": payload.get("nurse"),
        "status": "given",
        "timestamp": datetime.utcnow().isoformat(),
    }

    MAR.append(entry)

    return {
        "given": True,
        "entry": entry,
    }

@router.get("/{patient_id}")
def get_mar(patient_id: str):
    return [x for x in MAR if x.get("patient_id") == patient_id]
