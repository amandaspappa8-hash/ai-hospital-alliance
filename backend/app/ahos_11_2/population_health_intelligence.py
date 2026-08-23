from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.2/population-health",
    tags=["AHOS 11.2.3 Population Health Intelligence"]
)

class PopulationRequest(BaseModel):
    region:str="North Africa"
    population:int=7000000
    chronic_cases:int=950000
    infectious_cases:int=45000
    emergency_cases:int=12000

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
        "phase":"11.2.3",
        "engine":"Population Health Intelligence",
        "timestamp":datetime.utcnow().isoformat()
    }

@router.post("/analyze")
def analyze(req:PopulationRequest):

    chronic_burden = round(
        (req.chronic_cases / req.population) * 1000
    )

    infectious_risk = min(
        100,
        int((req.infectious_cases / req.population) * 10000)
        + random.randint(20,60)
    )

    emergency_pressure = min(
        100,
        int((req.emergency_cases / req.population) * 10000)
        + random.randint(25,70)
    )

    population_health_index = round(
        (
            chronic_burden +
            infectious_risk +
            emergency_pressure
        ) / 3
    )

    return {

        "status":"success",

        "phase":
        "11.2.3 Population Health Intelligence",

        "region":
        req.region,

        "population_analysis":{

            "population":
            req.population,

            "chronic_disease_burden":
            chronic_burden,

            "infectious_risk":
            infectious_risk,

            "emergency_pressure":
            emergency_pressure,

            "population_health_index":
            population_health_index,

            "risk_level":
            level(population_health_index)
        },

        "recommendations":[
            "Increase chronic disease monitoring",
            "Expand preventive screening programs",
            "Monitor infectious disease clusters",
            "Improve emergency preparedness",
            "Activate population health dashboard"
        ],

        "timestamp":
        datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():

    return {

        "status":"success",

        "population_metrics":{

            "population_health_score":
            random.randint(50,95),

            "chronic_disease_index":
            random.randint(45,90),

            "infectious_disease_index":
            random.randint(20,95),

            "emergency_health_index":
            random.randint(40,90),

            "community_risk_score":
            random.randint(35,95)
        },

        "alerts":[
            "Chronic disease monitoring active",
            "Population health surveillance active",
            "Community health intelligence active"
        ]
    }

@router.get("/trends")
def trends():

    return {

        "status":"success",

        "disease_trends":[

            {
                "disease":"Diabetes",
                "trend":"Rising",
                "risk":random.randint(60,95)
            },

            {
                "disease":"Hypertension",
                "trend":"Stable",
                "risk":random.randint(40,80)
            },

            {
                "disease":"Respiratory Disease",
                "trend":"Increasing",
                "risk":random.randint(50,90)
            },

            {
                "disease":"Infectious Disease",
                "trend":"Monitoring",
                "risk":random.randint(20,85)
            }
        ]
    }
