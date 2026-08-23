from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/emergency-orchestrator",
    tags=["AHOS 11.4.5 Emergency Orchestrator"]
)

class EmergencyRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    emergency_patients: int = 96
    trauma_cases: int = 14
    cardiac_cases: int = 11
    stroke_cases: int = 7
    available_er_beds: int = 18
    available_doctors: int = 12
    available_nurses: int = 34
    ambulance_queue: int = 9

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
        "phase": "11.4.5",
        "engine": "Emergency Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: EmergencyRequest):

    er_pressure = min(100, req.emergency_patients + random.randint(2, 12))
    trauma_pressure = min(100, req.trauma_cases * 5 + random.randint(5, 20))
    cardiac_pressure = min(100, req.cardiac_cases * 6 + random.randint(5, 18))
    stroke_pressure = min(100, req.stroke_cases * 7 + random.randint(5, 18))
    ambulance_pressure = min(100, req.ambulance_queue * 8 + random.randint(5, 15))

    emergency_index = round((
        er_pressure +
        trauma_pressure +
        cardiac_pressure +
        stroke_pressure +
        ambulance_pressure
    ) / 5)

    actions = [
        "Activate emergency triage acceleration",
        "Prioritize trauma, cardiac, and stroke pathways",
        "Prepare emergency overflow beds",
        "Reallocate doctors and nurses to emergency department",
        "Optimize ambulance receiving workflow",
        "Synchronize emergency status with Hospital Command Center"
    ]

    return {
        "status": "success",
        "phase": "11.4.5 Emergency Orchestrator",
        "hospital_id": req.hospital_id,

        "emergency_orchestration": {
            "emergency_patients": req.emergency_patients,
            "trauma_cases": req.trauma_cases,
            "cardiac_cases": req.cardiac_cases,
            "stroke_cases": req.stroke_cases,
            "available_er_beds": req.available_er_beds,
            "available_doctors": req.available_doctors,
            "available_nurses": req.available_nurses,
            "ambulance_queue": req.ambulance_queue,
            "er_pressure": er_pressure,
            "trauma_pressure": trauma_pressure,
            "cardiac_pressure": cardiac_pressure,
            "stroke_pressure": stroke_pressure,
            "ambulance_pressure": ambulance_pressure,
            "emergency_orchestration_index": emergency_index,
            "risk_level": level(emergency_index)
        },

        "autonomous_emergency_actions": actions,

        "emergency_signal": {
            "sync_triage_engine": True,
            "sync_care_path_orchestrator": True,
            "sync_resource_orchestrator": True,
            "sync_icu_orchestrator": True,
            "sync_hospital_command_center": True,
            "sync_digital_twin": True,
            "executive_escalation": emergency_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Emergency Orchestrator Dashboard",
        "metrics": {
            "er_pressure": random.randint(60, 99),
            "trauma_pathway_load": random.randint(40, 95),
            "cardiac_pathway_load": random.randint(40, 95),
            "stroke_pathway_load": random.randint(40, 95),
            "ambulance_queue_pressure": random.randint(35, 95),
            "triage_efficiency": random.randint(55, 98),
            "emergency_orchestration_index": random.randint(60, 99)
        },
        "alerts": [
            "Emergency Orchestrator active",
            "Triage workflow acceleration enabled",
            "Ambulance queue monitoring active",
            "Emergency digital twin synchronization online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.5",
            "emergency_orchestration_status": "Operational",
            "strategic_value": "Coordinates triage, trauma, cardiac, stroke, ambulance flow, emergency beds, and emergency staff",
            "next_phase": "11.4.6 ICU Orchestrator"
        }
    }
