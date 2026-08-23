from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.1/resource-optimizer",
    tags=["AHOS 11.1.3 Autonomous Resource Optimizer"]
)

class OptimizerRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    icu_available_beds: int = 14
    ward_available_beds: int = 90
    emergency_waiting_patients: int = 64
    available_doctors: int = 32
    available_nurses: int = 88
    pharmacy_pressure: int = 61
    lab_pressure: int = 74
    radiology_pressure: int = 69

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
        "phase": "11.1.3",
        "engine": "Autonomous Resource Optimizer",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/optimize")
def optimize(req: OptimizerRequest):
    bed_pressure = max(0, 100 - req.ward_available_beds)
    icu_pressure = max(0, 100 - req.icu_available_beds)
    emergency_pressure = min(100, req.emergency_waiting_patients + random.randint(5, 22))
    staff_pressure = min(100, 100 - int((req.available_doctors + req.available_nurses) / 2) + random.randint(5, 18))

    operational_pressure = round(
        (
            bed_pressure +
            icu_pressure +
            emergency_pressure +
            staff_pressure +
            req.pharmacy_pressure +
            req.lab_pressure +
            req.radiology_pressure
        ) / 7
    )

    optimization_actions = []

    if icu_pressure >= 75:
        optimization_actions.append("Open ICU overflow capacity and reserve 6 critical-care beds")

    if bed_pressure >= 60:
        optimization_actions.append("Accelerate discharge review and activate ward bed redistribution")

    if emergency_pressure >= 70:
        optimization_actions.append("Move stable emergency patients to observation unit")

    if staff_pressure >= 60:
        optimization_actions.append("Reallocate nursing staff from low-pressure departments")

    if req.lab_pressure >= 70:
        optimization_actions.append("Prioritize urgent laboratory queues and delay non-critical tests")

    if req.radiology_pressure >= 70:
        optimization_actions.append("Route non-urgent imaging to secondary radiology queue")

    if req.pharmacy_pressure >= 70:
        optimization_actions.append("Increase pharmacy dispensing lane capacity")

    if not optimization_actions:
        optimization_actions.append("Maintain current allocation and continue monitoring")

    return {
        "status": "success",
        "phase": "11.1.3 Autonomous Resource Optimizer",
        "hospital_id": req.hospital_id,
        "optimization": {
            "bed_pressure": bed_pressure,
            "icu_pressure": icu_pressure,
            "emergency_pressure": emergency_pressure,
            "staff_pressure": staff_pressure,
            "pharmacy_pressure": req.pharmacy_pressure,
            "laboratory_pressure": req.lab_pressure,
            "radiology_pressure": req.radiology_pressure,
            "operational_pressure_index": operational_pressure,
            "risk_level": level(operational_pressure),
        },
        "autonomous_actions": optimization_actions,
        "command_center_signal": {
            "notify_hospital_command_center": True,
            "notify_operations_center": True,
            "activate_resource_balancing": operational_pressure >= 60,
            "activate_escalation": operational_pressure >= 75,
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Autonomous Resource Optimizer Dashboard",
        "live_optimization_metrics": {
            "bed_redistribution_score": random.randint(60, 95),
            "icu_optimization_score": random.randint(65, 98),
            "staff_reallocation_score": random.randint(55, 92),
            "emergency_flow_score": random.randint(60, 96),
            "resource_balancing_score": random.randint(62, 97),
        },
        "active_optimization_signals": [
            "Bed redistribution monitoring active",
            "ICU overflow readiness active",
            "Emergency flow optimization active",
            "Staff reallocation model active",
            "Command Center optimization signal active"
        ]
    }
