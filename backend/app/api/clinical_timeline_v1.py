from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/clinical-timeline", tags=["Clinical Timeline v1"])

@router.get("/patient/{patient_id}")
def get_timeline(patient_id: str):
    now = datetime.utcnow().isoformat()

    return {
        "patient_id": patient_id,
        "timeline": [
            {"time": now, "type": "order", "title": "Troponin ordered", "status": "ordered", "source": "Clinical Lifecycle"},
            {"time": now, "type": "lab", "title": "Creatinine result 1.4", "status": "completed", "source": "Labs"},
            {"time": now, "type": "medication", "title": "Metformin 500mg BID active", "status": "active", "source": "Medication Lifecycle"},
            {"time": now, "type": "ai", "title": "AI recommended renal monitoring", "status": "review", "source": "AI Clinical"},
            {"time": now, "type": "audit", "title": "Doctor approval / pharmacist verification logged", "status": "approved", "source": "Audit Trail"}
        ]
    }
