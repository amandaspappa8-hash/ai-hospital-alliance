from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.2/pandemic",
    tags=["AHOS 11.2.4 Pandemic Intelligence Engine"]
)

class PandemicRequest(BaseModel):
    region:str="North Africa"
    suspected_cases:int=250
    confirmed_cases:int=85
    hospitalized_cases:int=30
    deaths:int=3

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
        "phase":"11.2.4",
        "engine":"Pandemic Intelligence Engine",
        "timestamp":datetime.utcnow().isoformat()
    }

@router.post("/analyze")
def analyze(req:PandemicRequest):

    transmission_index = min(
        100,
        req.suspected_cases // 5 + random.randint(10,30)
    )

    outbreak_risk = min(
        100,
        req.confirmed_cases + random.randint(10,25)
    )

    hospitalization_pressure = min(
        100,
        req.hospitalized_cases * 2 + random.randint(5,20)
    )

    mortality_risk = min(
        100,
        req.deaths * 10 + random.randint(5,25)
    )

    pandemic_index = round(
        (
            transmission_index +
            outbreak_risk +
            hospitalization_pressure +
            mortality_risk
        ) / 4
    )

    return {
        "status":"success",
        "phase":"11.2.4 Pandemic Intelligence Engine",
        "region":req.region,

        "pandemic_analysis":{
            "transmission_index":transmission_index,
            "outbreak_risk":outbreak_risk,
            "hospitalization_pressure":hospitalization_pressure,
            "mortality_risk":mortality_risk,
            "pandemic_index":pandemic_index,
            "risk_level":level(pandemic_index)
        },

        "recommendations":[
            "Increase outbreak surveillance",
            "Activate infectious disease monitoring",
            "Prepare ICU contingency plans",
            "Expand laboratory testing",
            "Alert Regional Healthcare Intelligence"
        ],

        "timestamp":datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status":"success",

        "pandemic_metrics":{
            "transmission_rate":random.randint(20,95),
            "outbreak_probability":random.randint(20,95),
            "hospital_pressure":random.randint(20,95),
            "laboratory_load":random.randint(20,95),
            "preparedness_score":random.randint(40,98)
        },

        "alerts":[
            "Pandemic surveillance active",
            "Disease cluster monitoring active",
            "Regional outbreak intelligence active"
        ]
    }

@router.get("/clusters")
def clusters():

    return {
        "status":"success",

        "clusters":[
            {
                "location":"Tripoli",
                "risk":"MODERATE",
                "cases":random.randint(20,200)
            },
            {
                "location":"Benghazi",
                "risk":"HIGH",
                "cases":random.randint(50,300)
            },
            {
                "location":"Misrata",
                "risk":"LOW",
                "cases":random.randint(5,80)
            }
        ]
    }

@router.get("/forecast")
def forecast():

    return {
        "status":"success",

        "forecast":{
            "7_day_projection":
                random.randint(100,1000),

            "14_day_projection":
                random.randint(200,2000),

            "30_day_projection":
                random.randint(500,5000),

            "predicted_risk":
                random.choice([
                    "LOW",
                    "MODERATE",
                    "HIGH",
                    "CRITICAL"
                ])
        }
    }
