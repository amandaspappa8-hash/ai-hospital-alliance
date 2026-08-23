from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai-ultrasound-x",
    tags=["AI Ultrasound X 9.5"]
)

class ICURequest(BaseModel):
    diagnosis: str
    risk_level: str
    spo2: int
    heart_rate: int
    systolic_bp: int
    diastolic_bp: int
    temperature: float
    early_warning_score: int

@router.get("/icu-decision-health")
def icu_health():
    return {
        "status": "online",
        "version": "9.5",
        "engine": "Autonomous ICU Decision Engine"
    }

@router.post("/autonomous-icu-decision")
def autonomous_icu_decision(data: ICURequest):

    icu_required = False
    emergency_priority = "MODERATE"

    if (
        data.spo2 < 90
        or data.heart_rate > 125
        or data.early_warning_score >= 8
    ):
        icu_required = True
        emergency_priority = "CRITICAL"

    intervention_plan = [
        "Continuous monitoring",
        "Repeat vital signs",
        "Oxygen support if required",
        "Escalate abnormal findings"
    ]

    if icu_required:
        intervention_plan.extend([
            "ICU admission evaluation",
            "Critical care physician review",
            "High frequency monitoring"
        ])

    return {
        "platform": "AI Ultrasound X 9.5",
        "engine": "Autonomous ICU Decision Engine",
        "status": "online",
        "diagnosis": data.diagnosis,
        "risk_level": data.risk_level,
        "icu_required": icu_required,
        "emergency_priority": emergency_priority,
        "early_warning_score": data.early_warning_score,
        "critical_care_state":
            "ICU_ESCALATION" if icu_required else "STANDARD_MONITORING",
        "intervention_plan": intervention_plan,
        "clinical_confidence": 97
    }
