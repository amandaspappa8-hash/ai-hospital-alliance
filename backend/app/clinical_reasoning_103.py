from fastapi import APIRouter
from datetime import datetime
import requests

router = APIRouter(
    prefix="/aiha/10.3",
    tags=["AIHA 10.3 Autonomous Clinical Reasoning Engine"]
)

STORY_URL = "http://127.0.0.1:8000/aiha/10.2/story"

@router.get("/health")
def health():
    return {
        "status": "online",
        "stage": "AI Hospital Alliance 10.3",
        "engine": "Autonomous Clinical Reasoning Engine",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def build_reasoning(findings):
    reasoning = []

    text = " ".join(findings).lower()

    if "troponin" in text:
        reasoning.append(
            "Troponin elevation suggests possible acute cardiac injury or Acute Coronary Syndrome."
        )

    if "creatinine" in text or "potassium" in text:
        reasoning.append(
            "Creatinine and potassium abnormalities suggest Acute Kidney Injury."
        )

    if "glucose" in text:
        reasoning.append(
            "Severe hyperglycemia detected requiring glucose management."
        )

    if "warfarin" in text or "aspirin" in text or "bleeding risk" in text:
        reasoning.append(
            "Medication profile indicates elevated bleeding risk."
        )

    if "radiology" in text:
        reasoning.append(
            "Radiology findings should be clinically correlated with laboratory and vital data."
        )

    return reasoning

def build_differential(findings):
    text = " ".join(findings).lower()

    dx = []

    if "troponin" in text:
        dx.append({
            "diagnosis": "Acute Coronary Syndrome",
            "confidence": 0.92
        })

    if "creatinine" in text or "potassium" in text:
        dx.append({
            "diagnosis": "Acute Kidney Injury",
            "confidence": 0.87
        })

    if "glucose" in text:
        dx.append({
            "diagnosis": "Uncontrolled Hyperglycemia",
            "confidence": 0.84
        })

    if "bleeding risk" in text:
        dx.append({
            "diagnosis": "Medication Related Bleeding Risk",
            "confidence": 0.90
        })

    return dx

@router.get("/reason/{patient_id}")
def reason(patient_id: str):

    story = requests.get(
        f"{STORY_URL}/{patient_id}",
        timeout=10
    ).json()

    findings = story.get("key_findings", [])

    reasoning = build_reasoning(findings)
    differential = build_differential(findings)

    return {
        "status": "success",
        "patient_id": patient_id,
        "overall_risk": story.get("risk"),
        "clinical_reasoning": reasoning,
        "differential_diagnosis": differential,
        "recommendations": story.get("recommendations", []),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/risk/{patient_id}")
def risk(patient_id: str):

    story = requests.get(
        f"{STORY_URL}/{patient_id}",
        timeout=10
    ).json()

    risk = story.get("risk", "LOW")

    return {
        "patient_id": patient_id,
        "overall_risk": risk,
        "mortality_risk":
            "HIGH" if risk == "HIGH" else
            "MODERATE" if risk == "MODERATE"
            else "LOW",
        "icu_risk":
            "HIGH" if risk == "HIGH"
            else "LOW",
        "bleeding_risk":
            "HIGH"
            if any(
                "bleeding" in x.lower()
                for x in story.get("key_findings", [])
            )
            else "LOW",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/differential/{patient_id}")
def differential(patient_id: str):

    story = requests.get(
        f"{STORY_URL}/{patient_id}",
        timeout=10
    ).json()

    return {
        "patient_id": patient_id,
        "differential_diagnosis":
            build_differential(
                story.get("key_findings", [])
            ),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
