from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.2/regional-intelligence",
    tags=["AHOS 11.2.2 Regional Healthcare Intelligence"]
)

class RegionalRequest(BaseModel):
    region_name: str = "North Africa Healthcare Region"
    population: int = 7000000
    connected_hospitals: int = 12
    emergency_cases: int = 420
    icu_occupancy: int = 78
    bed_occupancy: int = 72
    infectious_alerts: int = 8

def level(v: int):
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
        "phase": "11.2.2",
        "engine": "Regional Healthcare Intelligence",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/analyze")
def analyze_region(req: RegionalRequest):
    emergency_pressure = min(100, int(req.emergency_cases / 5) + random.randint(1, 12))
    regional_capacity_pressure = round((req.icu_occupancy + req.bed_occupancy + emergency_pressure) / 3)
    infectious_risk = min(100, req.infectious_alerts * 8 + random.randint(5, 25))
    population_health_risk = round((regional_capacity_pressure + infectious_risk) / 2)

    return {
        "status": "success",
        "phase": "11.2.2 Regional Healthcare Intelligence",
        "region_name": req.region_name,
        "regional_intelligence": {
            "connected_hospitals": req.connected_hospitals,
            "emergency_pressure": emergency_pressure,
            "regional_capacity_pressure": regional_capacity_pressure,
            "infectious_risk_index": infectious_risk,
            "population_health_risk": population_health_risk,
            "regional_risk_level": level(population_health_risk)
        },
        "recommendations": [
            "Increase regional emergency coordination",
            "Prepare ICU redistribution plan",
            "Monitor infectious disease clusters",
            "Activate regional command dashboard",
            "Share alerts with connected hospitals"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Regional Healthcare Intelligence Dashboard",
        "regional_metrics": {
            "connected_hospitals": random.randint(8, 40),
            "regional_bed_pressure": random.randint(50, 92),
            "regional_icu_pressure": random.randint(55, 96),
            "regional_emergency_pressure": random.randint(50, 98),
            "infectious_alert_index": random.randint(20, 90),
            "regional_readiness_score": random.randint(45, 95)
        },
        "alerts": [
            "Regional emergency load rising",
            "ICU redistribution may be needed",
            "Infectious disease monitoring active"
        ]
    }

@router.get("/map")
def regional_map():
    return {
        "status": "success",
        "regional_nodes": [
            {"hospital": "Tripoli Central AI Hospital", "status": "online", "load": random.randint(55, 95)},
            {"hospital": "Benghazi Medical Center", "status": "online", "load": random.randint(40, 90)},
            {"hospital": "Misrata Smart Hospital", "status": "online", "load": random.randint(45, 88)},
            {"hospital": "Sebha Regional Hospital", "status": "monitoring", "load": random.randint(35, 82)},
            {"hospital": "Stockholm AI Care", "status": "online", "load": random.randint(30, 80)}
        ]
    }
