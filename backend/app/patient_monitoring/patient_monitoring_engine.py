from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai-ultrasound-x",
    tags=["AI Ultrasound X 9.4"]
)

class MonitoringRequest(BaseModel):
    diagnosis: str
    risk_level: str
    heart_rate: int
    spo2: int
    systolic_bp: int
    diastolic_bp: int
    pain_score: int
    temperature: float

@router.get("/patient-monitoring-health")
def monitoring_health():
    return {
        "status": "online",
        "version": "9.4",
        "engine": "Autonomous Patient Monitoring & Alert Engine"
    }

@router.post("/autonomous-patient-monitoring")
def autonomous_patient_monitoring(data: MonitoringRequest):

    alerts = []
    monitoring_state = "STABLE"

    if data.spo2 < 92:
        alerts.append({
            "type": "oxygen",
            "level": "CRITICAL",
            "message": "Low oxygen saturation detected"
        })

    if data.heart_rate > 120:
        alerts.append({
            "type": "heart_rate",
            "level": "HIGH",
            "message": "Tachycardia detected"
        })

    if data.temperature >= 38.5:
        alerts.append({
            "type": "temperature",
            "level": "HIGH",
            "message": "Possible infection or sepsis"
        })

    if data.pain_score >= 8:
        alerts.append({
            "type": "pain",
            "level": "HIGH",
            "message": "Severe pain requires intervention"
        })

    if len(alerts) > 0:
        monitoring_state = "ALERT"

    early_warning_score = (
        (130 - min(data.heart_rate,130))
        + data.spo2
        + (10 - min(data.pain_score,10))
    ) // 10

    return {
        "platform": "AI Ultrasound X 9.4",
        "engine": "Autonomous Patient Monitoring & Alert Engine",
        "status": "online",
        "monitoring_state": monitoring_state,
        "diagnosis": data.diagnosis,
        "risk_level": data.risk_level,
        "early_warning_score": early_warning_score,
        "vitals": {
            "heart_rate": data.heart_rate,
            "spo2": data.spo2,
            "blood_pressure": f"{data.systolic_bp}/{data.diastolic_bp}",
            "temperature": data.temperature,
            "pain_score": data.pain_score
        },
        "alerts": alerts,
        "recommendations": [
            "Continue monitoring",
            "Repeat vital signs",
            "Escalate if condition worsens",
            "Notify clinician if alerts persist"
        ]
    }
