from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.1/capacity",
    tags=["AHOS 11.1.2 Hospital Capacity Predictor"]
)

class CapacityRequest(BaseModel):
    total_beds:int = 1000
    occupied_beds:int = 780
    icu_total:int = 120
    icu_occupied:int = 96
    emergency_patients:int = 74
    active_staff:int = 240

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
        "status":"online",
        "phase":"11.1.2",
        "engine":"Hospital Capacity Predictor",
        "timestamp":datetime.utcnow().isoformat()
    }

@router.post("/predict")
def predict(req: CapacityRequest):

    bed_utilization = round((req.occupied_beds/req.total_beds)*100)

    icu_utilization = round((req.icu_occupied/req.icu_total)*100)

    emergency_pressure = min(
        100,
        req.emergency_patients + random.randint(5,25)
    )

    resource_exhaustion = round(
        (
            bed_utilization+
            icu_utilization+
            emergency_pressure
        )/3
    )

    hospital_stress = round(
        (
            bed_utilization+
            icu_utilization+
            emergency_pressure+
            resource_exhaustion
        )/4
    )

    return {
        "status":"success",
        "phase":"11.1.2 Hospital Capacity Predictor",

        "capacity":{

            "bed_utilization":bed_utilization,
            "bed_status":level(bed_utilization),

            "icu_utilization":icu_utilization,
            "icu_status":level(icu_utilization),

            "emergency_pressure":emergency_pressure,
            "emergency_status":level(emergency_pressure),

            "resource_exhaustion_risk":resource_exhaustion,
            "resource_status":level(resource_exhaustion),

            "hospital_stress_index":hospital_stress,
            "stress_status":level(hospital_stress)
        },

        "recommendations":[
            "Expand ICU capacity",
            "Prepare overflow beds",
            "Reallocate nursing staff",
            "Monitor emergency congestion",
            "Activate Hospital Command Center"
        ],

        "timestamp":datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status":"success",

        "capacity_dashboard":{

            "bed_capacity":random.randint(65,95),
            "icu_capacity":random.randint(70,98),
            "emergency_load":random.randint(60,99),
            "resource_pressure":random.randint(55,95),
            "hospital_stress":random.randint(60,98)
        },

        "alerts":[
            "ICU approaching saturation",
            "Emergency congestion detected",
            "Resource pressure increasing"
        ]
    }
