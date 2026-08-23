from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/ai-ultrasound-x", tags=["AI Ultrasound X 8.9"])

class ClinicalCase(BaseModel):
    symptoms: List[str] = []
    labs: Dict[str, Any] = {}
    imaging: str = ""
    medications: List[str] = []
    age: int | None = None
    gender: str | None = None

@router.post("/real-clinical-case-simulator")
def real_clinical_case_simulator(case: ClinicalCase):
    symptoms = [s.lower() for s in case.symptoms]
    imaging = case.imaging.lower()
    labs = case.labs

    diagnosis = "General Clinical Review"
    risk = "MODERATE"
    confidence = 82
    icd11 = "MG30"
    action = "Clinical evaluation and follow-up recommended"

    if "flank pain" in symptoms or "renal colic" in symptoms or "hydronephrosis" in imaging:
        diagnosis = "Renal Colic / Possible Ureteric Stone"
        risk = "HIGH"
        confidence = 94
        icd11 = "GB70"
        action = "Urgent radiology follow-up, renal ultrasound/CT KUB, pain control, hydration"

    elif "fever" in symptoms and ("cough" in symptoms or "dyspnea" in symptoms):
        diagnosis = "Community Acquired Pneumonia"
        risk = "HIGH"
        confidence = 92
        icd11 = "CA40"
        action = "Chest imaging, CBC/CRP, oxygen assessment, antibiotic review"

    elif labs.get("hba1c", 0) >= 6.5 or labs.get("glucose", 0) >= 126:
        diagnosis = "Diabetes Mellitus — Likely Type 2"
        risk = "MODERATE"
        confidence = 91
        icd11 = "5A11"
        action = "Repeat HbA1c/fasting glucose, lifestyle plan, medication review"

    elif "chest pain" in symptoms:
        diagnosis = "Acute Coronary Syndrome Rule-Out"
        risk = "CRITICAL"
        confidence = 90
        icd11 = "BA40"
        action = "Immediate ECG, troponin, emergency assessment"

    consensus_sources = {
        "radiology": 93 if case.imaging else 70,
        "laboratory": 92 if case.labs else 68,
        "pharmacy": 88 if case.medications else 72,
        "clinical_brain": confidence,
        "risk_engine": 96 if risk in ["HIGH", "CRITICAL"] else 82,
        "icd11": 90
    }

    return {
        "platform": "AI Ultrasound X 8.9",
        "engine": "Real Clinical Case Simulator",
        "status": "online",
        "input_case": case.model_dump(),
        "final_diagnosis": diagnosis,
        "clinical_confidence": confidence,
        "risk_level": risk,
        "icd11_suggestion": icd11,
        "recommended_action": action,
        "consensus_sources": consensus_sources
    }
