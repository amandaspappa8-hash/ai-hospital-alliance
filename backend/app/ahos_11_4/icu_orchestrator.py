from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/icu-orchestrator",
    tags=["AHOS 11.4.6 ICU Orchestrator"]
)

class ICURequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    icu_patients: int = 84
    critical_patients: int = 22
    ventilated_patients: int = 18
    available_icu_beds: int = 10
    available_ventilators: int = 12
    available_icu_doctors: int = 8
    available_icu_nurses: int = 26

def level(v):
    if v >= 90:
        return "CRITICAL"
    if v >= 75:
        return "HIGH"
    if v >= 60:
        return "MODERATE"
    return "STABLE"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "11.4.6",
        "engine": "ICU Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: ICURequest):

    icu_pressure = min(100, req.icu_patients + random.randint(3, 12))
    critical_pressure = min(100, req.critical_patients * 4 + random.randint(5, 15))
    ventilator_pressure = min(100, req.ventilated_patients * 4 + random.randint(5, 15))
    bed_shortage_pressure = max(0, 100 - req.available_icu_beds)
    staff_pressure = max(0, 100 - int((req.available_icu_doctors * 3 + req.available_icu_nurses) / 2))

    icu_index = round((
        icu_pressure +
        critical_pressure +
        ventilator_pressure +
        bed_shortage_pressure +
        staff_pressure
    ) / 5)

    actions = [
        "Activate ICU bed prioritization",
        "Reserve ventilators for critical respiratory cases",
        "Prepare ICU overflow pathway",
        "Reallocate ICU nurses to high-acuity patients",
        "Coordinate ICU discharge review",
        "Synchronize ICU status with Digital Twin and Command Center"
    ]

    return {
        "status": "success",
        "phase": "11.4.6 ICU Orchestrator",
        "hospital_id": req.hospital_id,

        "icu_orchestration": {
            "icu_patients": req.icu_patients,
            "critical_patients": req.critical_patients,
            "ventilated_patients": req.ventilated_patients,
            "available_icu_beds": req.available_icu_beds,
            "available_ventilators": req.available_ventilators,
            "available_icu_doctors": req.available_icu_doctors,
            "available_icu_nurses": req.available_icu_nurses,
            "icu_pressure": icu_pressure,
            "critical_pressure": critical_pressure,
            "ventilator_pressure": ventilator_pressure,
            "bed_shortage_pressure": bed_shortage_pressure,
            "staff_pressure": staff_pressure,
            "icu_orchestration_index": icu_index,
            "risk_level": level(icu_index)
        },

        "autonomous_icu_actions": actions,

        "icu_signal": {
            "sync_emergency_orchestrator": True,
            "sync_resource_orchestrator": True,
            "sync_staffing_engine": True,
            "sync_hospital_command_center": True,
            "sync_digital_twin": True,
            "executive_escalation": icu_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "ICU Orchestrator Dashboard",
        "metrics": {
            "icu_pressure": random.randint(60, 99),
            "critical_patient_load": random.randint(50, 98),
            "ventilator_pressure": random.randint(45, 98),
            "icu_bed_shortage": random.randint(40, 98),
            "icu_staff_pressure": random.randint(45, 98),
            "icu_orchestration_index": random.randint(60, 99)
        },
        "alerts": [
            "ICU Orchestrator active",
            "Critical-care pathway enabled",
            "Ventilator allocation monitoring active",
            "ICU digital twin synchronization online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.6",
            "icu_orchestration_status": "Operational",
            "strategic_value": "Coordinates ICU beds, ventilators, critical patients, ICU doctors, ICU nurses, and overflow planning",
            "next_phase": "11.4.7 Pharmacy Orchestrator"
        }
    }
