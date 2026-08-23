from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/ahos/24.0/live-beds",
    tags=["AHOS 24.0.2 Live Bed Management"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "module": "AI Hospital Alliance 24.0.2 Live Bed Management",
        "timestamp": datetime.utcnow()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "hospital_capacity": {
            "total_beds": 300,
            "occupied": 218,
            "available": 82,
            "occupancy_rate": 73
        },
        "icu": {
            "total": 40,
            "occupied": 31,
            "available": 9,
            "critical_waiting": 3
        },
        "wards": [
            {"name":"ICU","beds":40,"occupied":31},
            {"name":"Emergency","beds":60,"occupied":44},
            {"name":"Cardiology","beds":50,"occupied":39},
            {"name":"Radiology","beds":25,"occupied":11}
        ]
    }

@router.get("/allocation")
def allocation():
    return {
        "recommendations": [
            "Transfer 1 patient from ICU to monitored ward",
            "Reserve 2 ICU beds for emergency arrivals",
            "Move stable patient to Cardiology floor",
            "Prepare overflow protocol"
        ]
    }
