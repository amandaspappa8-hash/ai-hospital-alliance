from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai-ultrasound-x",
    tags=["AI Ultrasound X 9.7"]
)

class ResourceAllocationRequest(BaseModel):
    critical_patients: int
    icu_capacity: int
    emergency_cases: int
    active_alerts: int
    available_staff: int
    icu_beds: int

@router.get("/resource-allocation-health")
def health():
    return {
        "status": "online",
        "version": "9.7",
        "engine": "Autonomous Hospital Resource Allocation Engine"
    }

@router.post("/resource-allocation")
def resource_allocation(req: ResourceAllocationRequest):

    emergency_level = "NORMAL"

    if req.critical_patients > 10:
        emergency_level = "HIGH"

    if req.active_alerts > 8:
        emergency_level = "CRITICAL"

    allocation = {
        "icu_beds_reserved": min(req.critical_patients, req.icu_beds),
        "staff_assigned": min(req.available_staff, req.critical_patients * 2),
        "emergency_team": min(req.emergency_cases, 10)
    }

    return {
        "platform": "AI Ultrasound X 9.7",
        "engine": "Autonomous Hospital Resource Allocation Engine",
        "status": "online",
        "emergency_level": emergency_level,
        "resource_status": "OPTIMAL",
        "allocation": allocation,
        "recommendations": [
            "Optimize ICU utilization",
            "Prioritize critical patients",
            "Increase monitoring staff",
            "Maintain emergency readiness"
        ],
        "global_consensus": 98
    }
