from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(prefix="/ahos/11.1/resource-forecast", tags=["AHOS 11.1 Resource Forecast Engine"])

class ForecastRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    horizon_hours: int = 24
    current_icu_patients: int = 42
    current_beds_occupied: int = 620
    emergency_queue: int = 38
    active_staff: int = 210

def risk_level(value):
    if value >= 85:
        return "CRITICAL"
    if value >= 70:
        return "HIGH"
    if value >= 50:
        return "MODERATE"
    return "STABLE"

@router.get("/health")
def health():
    return {
        "status": "online",
        "module": "AI Hospital Alliance 11.1.1",
        "engine": "Autonomous Resource Forecast Engine",
        "timestamp": datetime.utcnow().isoformat(),
    }

@router.post("/predict")
def predict_resources(req: ForecastRequest):
    icu_demand = min(100, req.current_icu_patients + random.randint(5, 22))
    bed_demand = min(100, int((req.current_beds_occupied / 750) * 100) + random.randint(3, 15))
    emergency_demand = min(100, req.emergency_queue + random.randint(10, 35))
    staff_pressure = min(100, 100 - int(req.active_staff / 3) + random.randint(5, 18))

    hospital_load_index = int((icu_demand + bed_demand + emergency_demand + staff_pressure) / 4)

    return {
        "status": "success",
        "hospital_id": req.hospital_id,
        "phase": "11.1.1 Resource Forecast Engine",
        "forecast_horizon_hours": req.horizon_hours,
        "forecast": {
            "icu_demand_prediction": icu_demand,
            "bed_demand_prediction": bed_demand,
            "emergency_demand_prediction": emergency_demand,
            "staff_pressure_prediction": staff_pressure,
            "hospital_load_index": hospital_load_index,
            "risk_level": risk_level(hospital_load_index),
        },
        "recommendations": [
            "Prepare additional ICU beds",
            "Increase emergency triage staff",
            "Review discharge candidates",
            "Activate resource monitoring protocol",
            "Notify Hospital Command Center",
        ],
        "timestamp": datetime.utcnow().isoformat(),
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Resource Forecast Dashboard",
        "metrics": {
            "icu_forecast": random.randint(65, 94),
            "bed_pressure": random.randint(58, 91),
            "staff_pressure": random.randint(50, 88),
            "emergency_pressure": random.randint(62, 96),
            "pharmacy_demand": random.randint(40, 82),
            "laboratory_demand": random.randint(45, 85),
            "radiology_demand": random.randint(50, 89),
        },
        "alerts": [
            "ICU demand may increase within 24 hours",
            "Emergency pressure rising",
            "Staff redistribution recommended",
        ],
    }
