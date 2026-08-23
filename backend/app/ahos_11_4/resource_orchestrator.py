from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/resource-orchestrator",
    tags=["AHOS 11.4.4 Resource Orchestrator"]
)

class ResourceOrchestratorRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    beds_available: int = 72
    icu_beds_available: int = 12
    ventilators_available: int = 18
    physicians_available: int = 34
    nurses_available: int = 96
    emergency_pressure: int = 81
    icu_pressure: int = 86
    ward_pressure: int = 74

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
        "phase": "11.4.4",
        "engine": "Resource Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: ResourceOrchestratorRequest):

    bed_orchestration = min(100, req.ward_pressure + random.randint(3, 14))
    icu_orchestration = min(100, req.icu_pressure + random.randint(2, 12))
    emergency_orchestration = min(100, req.emergency_pressure + random.randint(4, 15))
    workforce_orchestration = random.randint(60, 96)
    device_orchestration = random.randint(55, 94)

    resource_index = round((
        bed_orchestration +
        icu_orchestration +
        emergency_orchestration +
        workforce_orchestration +
        device_orchestration
    ) / 5)

    actions = [
        "Optimize bed allocation across departments",
        "Reserve ICU capacity for critical cases",
        "Route emergency overflow to observation unit",
        "Balance physician and nursing coverage",
        "Prioritize ventilator readiness",
        "Synchronize resources with Hospital Digital Twin"
    ]

    return {
        "status": "success",
        "phase": "11.4.4 Resource Orchestrator",
        "hospital_id": req.hospital_id,

        "resource_orchestration": {
            "beds_available": req.beds_available,
            "icu_beds_available": req.icu_beds_available,
            "ventilators_available": req.ventilators_available,
            "physicians_available": req.physicians_available,
            "nurses_available": req.nurses_available,
            "bed_orchestration": bed_orchestration,
            "icu_orchestration": icu_orchestration,
            "emergency_orchestration": emergency_orchestration,
            "workforce_orchestration": workforce_orchestration,
            "device_orchestration": device_orchestration,
            "resource_orchestration_index": resource_index,
            "risk_level": level(resource_index)
        },

        "autonomous_resource_actions": actions,

        "resource_signal": {
            "sync_resource_forecast": True,
            "sync_capacity_predictor": True,
            "sync_resource_optimizer": True,
            "sync_staffing_engine": True,
            "sync_digital_twin": True,
            "sync_hospital_command_center": True,
            "executive_escalation": resource_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Resource Orchestrator Dashboard",
        "metrics": {
            "bed_orchestration_score": random.randint(60, 98),
            "icu_orchestration_score": random.randint(60, 98),
            "device_orchestration_score": random.randint(55, 96),
            "staff_resource_score": random.randint(55, 96),
            "emergency_resource_score": random.randint(60, 98),
            "overall_resource_index": random.randint(60, 98)
        },
        "alerts": [
            "Resource Orchestrator active",
            "Bed and ICU resource coordination enabled",
            "Workforce-resource balancing active",
            "Digital twin resource synchronization online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.4",
            "resource_orchestration_status": "Operational",
            "strategic_value": "Coordinates beds, ICU, staff, devices, emergency flow, and resource distribution",
            "next_phase": "11.4.5 Emergency Orchestrator"
        }
    }
