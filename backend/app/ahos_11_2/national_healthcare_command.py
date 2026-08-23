from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.2/national-command",
    tags=["AHOS 11.2.5 National Healthcare Command"]
)

class NationalCommandRequest(BaseModel):
    country:str="Libya"
    connected_regions:int=8
    connected_hospitals:int=120
    active_alerts:int=18
    emergency_events:int=4

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
        "phase":"11.2.5",
        "engine":"National Healthcare Command",
        "timestamp":datetime.utcnow().isoformat()
    }

@router.post("/analyze")
def analyze(req: NationalCommandRequest):

    national_pressure = min(
        100,
        int((req.active_alerts * 3) + (req.emergency_events * 8))
        + random.randint(5,20)
    )

    readiness_score = random.randint(60,98)

    command_index = round(
        (national_pressure + readiness_score) / 2
    )

    return {
        "status":"success",
        "phase":"11.2.5 National Healthcare Command",

        "country":req.country,

        "national_command":{

            "connected_regions":
                req.connected_regions,

            "connected_hospitals":
                req.connected_hospitals,

            "active_alerts":
                req.active_alerts,

            "emergency_events":
                req.emergency_events,

            "national_pressure":
                national_pressure,

            "readiness_score":
                readiness_score,

            "national_command_index":
                command_index,

            "risk_level":
                level(command_index)
        },

        "recommendations":[
            "Activate National Healthcare Dashboard",
            "Coordinate Regional Healthcare Networks",
            "Review National Emergency Readiness",
            "Monitor Pandemic Intelligence Engine",
            "Prepare Executive Healthcare Briefing"
        ],

        "timestamp":
            datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():

    return {

        "status":"success",

        "national_metrics":{

            "national_capacity":
                random.randint(60,99),

            "national_readiness":
                random.randint(60,99),

            "national_emergency_score":
                random.randint(40,95),

            "national_resource_score":
                random.randint(50,98),

            "national_health_index":
                random.randint(50,99)
        },

        "alerts":[
            "National Command Active",
            "Regional Networks Connected",
            "Executive Monitoring Enabled"
        ]
    }

@router.get("/regions")
def regions():

    return {

        "status":"success",

        "regions":[

            {
                "name":"Tripoli Region",
                "risk":"MODERATE",
                "capacity":random.randint(60,95)
            },

            {
                "name":"Benghazi Region",
                "risk":"HIGH",
                "capacity":random.randint(50,90)
            },

            {
                "name":"Misrata Region",
                "risk":"LOW",
                "capacity":random.randint(70,99)
            },

            {
                "name":"Southern Region",
                "risk":"MODERATE",
                "capacity":random.randint(45,85)
            }
        ]
    }

@router.get("/executive-summary")
def executive_summary():

    return {

        "status":"success",

        "summary":{
            "national_status":"Operational",
            "connected_regions":8,
            "connected_hospitals":120,
            "national_risk":
                random.choice([
                    "LOW",
                    "MODERATE",
                    "HIGH"
                ]),
            "executive_recommendation":
                "Continue monitoring all healthcare regions"
        }
    }
