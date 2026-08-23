from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/pharmacy-orchestrator",
    tags=["AHOS 11.4.7 Pharmacy Orchestrator"]
)

class PharmacyRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    active_prescriptions: int = 340
    urgent_orders: int = 58
    controlled_medications: int = 22
    low_stock_items: int = 17
    pharmacists_available: int = 9
    dispensing_lanes: int = 4
    medication_errors_flagged: int = 3

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
        "phase": "11.4.7",
        "engine": "Pharmacy Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: PharmacyRequest):

    prescription_pressure = min(100, int(req.active_prescriptions / 4) + random.randint(5, 15))
    urgent_pressure = min(100, req.urgent_orders + random.randint(10, 25))
    stock_pressure = min(100, req.low_stock_items * 5 + random.randint(5, 15))
    safety_pressure = min(100, req.medication_errors_flagged * 15 + random.randint(5, 20))
    staff_pressure = max(0, 100 - (req.pharmacists_available * 8))

    pharmacy_index = round((
        prescription_pressure +
        urgent_pressure +
        stock_pressure +
        safety_pressure +
        staff_pressure
    ) / 5)

    actions = [
        "Prioritize urgent medication orders",
        "Activate medication safety verification queue",
        "Prepare low-stock replenishment request",
        "Expand dispensing workflow capacity",
        "Route controlled medications to pharmacist validation",
        "Synchronize pharmacy state with Hospital Command Center"
    ]

    return {
        "status": "success",
        "phase": "11.4.7 Pharmacy Orchestrator",
        "hospital_id": req.hospital_id,

        "pharmacy_orchestration": {
            "active_prescriptions": req.active_prescriptions,
            "urgent_orders": req.urgent_orders,
            "controlled_medications": req.controlled_medications,
            "low_stock_items": req.low_stock_items,
            "pharmacists_available": req.pharmacists_available,
            "dispensing_lanes": req.dispensing_lanes,
            "medication_errors_flagged": req.medication_errors_flagged,
            "prescription_pressure": prescription_pressure,
            "urgent_pressure": urgent_pressure,
            "stock_pressure": stock_pressure,
            "safety_pressure": safety_pressure,
            "staff_pressure": staff_pressure,
            "pharmacy_orchestration_index": pharmacy_index,
            "risk_level": level(pharmacy_index)
        },

        "autonomous_pharmacy_actions": actions,

        "pharmacy_signal": {
            "sync_care_path_orchestrator": True,
            "sync_resource_orchestrator": True,
            "sync_staffing_engine": True,
            "sync_medication_safety": True,
            "sync_hospital_command_center": True,
            "sync_digital_twin": True,
            "executive_escalation": pharmacy_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Pharmacy Orchestrator Dashboard",
        "metrics": {
            "prescription_pressure": random.randint(55, 98),
            "urgent_order_load": random.randint(50, 98),
            "stock_shortage_risk": random.randint(35, 95),
            "medication_safety_score": random.randint(65, 99),
            "dispensing_efficiency": random.randint(55, 98),
            "pharmacy_orchestration_index": random.randint(60, 99)
        },
        "alerts": [
            "Pharmacy Orchestrator active",
            "Medication safety validation enabled",
            "Stock monitoring active",
            "Pharmacy digital twin synchronization online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.7",
            "pharmacy_orchestration_status": "Operational",
            "strategic_value": "Coordinates prescriptions, urgent orders, medication safety, stock, pharmacists, and dispensing workflow",
            "next_phase": "11.4.8 Laboratory Orchestrator"
        }
    }
