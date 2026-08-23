from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/laboratory-orchestrator",
    tags=["AHOS 11.4.8 Laboratory Orchestrator"]
)

class LaboratoryRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    pending_orders: int = 260
    urgent_orders: int = 72
    critical_results: int = 14
    available_lab_staff: int = 18
    active_analyzers: int = 7
    analyzer_downtime: int = 1
    blood_bank_alerts: int = 5

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
        "phase": "11.4.8",
        "engine": "Laboratory Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: LaboratoryRequest):

    order_pressure = min(100, int(req.pending_orders / 3) + random.randint(5, 15))
    urgent_pressure = min(100, req.urgent_orders + random.randint(5, 20))
    critical_pressure = min(100, req.critical_results * 6 + random.randint(5, 15))
    staff_pressure = max(0, 100 - (req.available_lab_staff * 4))
    analyzer_pressure = min(100, req.analyzer_downtime * 25 + random.randint(5, 20))
    blood_bank_pressure = min(100, req.blood_bank_alerts * 10 + random.randint(5, 20))

    lab_index = round((
        order_pressure +
        urgent_pressure +
        critical_pressure +
        staff_pressure +
        analyzer_pressure +
        blood_bank_pressure
    ) / 6)

    actions = [
        "Prioritize urgent and critical laboratory orders",
        "Route critical results to physician notification workflow",
        "Balance analyzer workload across active machines",
        "Activate blood bank monitoring workflow",
        "Reallocate lab staff to urgent sample processing",
        "Synchronize laboratory state with Hospital Command Center"
    ]

    return {
        "status": "success",
        "phase": "11.4.8 Laboratory Orchestrator",
        "hospital_id": req.hospital_id,

        "laboratory_orchestration": {
            "pending_orders": req.pending_orders,
            "urgent_orders": req.urgent_orders,
            "critical_results": req.critical_results,
            "available_lab_staff": req.available_lab_staff,
            "active_analyzers": req.active_analyzers,
            "analyzer_downtime": req.analyzer_downtime,
            "blood_bank_alerts": req.blood_bank_alerts,
            "order_pressure": order_pressure,
            "urgent_pressure": urgent_pressure,
            "critical_pressure": critical_pressure,
            "staff_pressure": staff_pressure,
            "analyzer_pressure": analyzer_pressure,
            "blood_bank_pressure": blood_bank_pressure,
            "laboratory_orchestration_index": lab_index,
            "risk_level": level(lab_index)
        },

        "autonomous_laboratory_actions": actions,

        "laboratory_signal": {
            "sync_care_path_orchestrator": True,
            "sync_resource_orchestrator": True,
            "sync_staffing_engine": True,
            "sync_critical_results": True,
            "sync_blood_bank": True,
            "sync_hospital_command_center": True,
            "sync_digital_twin": True,
            "executive_escalation": lab_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Laboratory Orchestrator Dashboard",
        "metrics": {
            "pending_order_pressure": random.randint(55, 98),
            "urgent_lab_load": random.randint(50, 98),
            "critical_result_pressure": random.randint(40, 95),
            "analyzer_efficiency": random.randint(55, 99),
            "blood_bank_readiness": random.randint(60, 99),
            "laboratory_orchestration_index": random.randint(60, 99)
        },
        "alerts": [
            "Laboratory Orchestrator active",
            "Critical result routing enabled",
            "Analyzer workload balancing active",
            "Blood bank monitoring online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.8",
            "laboratory_orchestration_status": "Operational",
            "strategic_value": "Coordinates lab orders, critical results, analyzers, staff, and blood bank readiness",
            "next_phase": "11.4.9 Radiology Orchestrator"
        }
    }
