from fastapi import APIRouter
from datetime import datetime
import requests

router = APIRouter(
    prefix="/aiha/10.5",
    tags=["AIHA 10.5 Autonomous Outcome Prediction Engine"]
)

CARE_PLAN_URL = "http://127.0.0.1:8000/aiha/10.4/plan"
REASON_URL = "http://127.0.0.1:8000/aiha/10.3/reason"
RISK_URL = "http://127.0.0.1:8000/aiha/10.3/risk"

@router.get("/health")
def health():
    return {
        "status": "online",
        "stage": "AI Hospital Alliance 10.5",
        "engine": "Autonomous Outcome Prediction Engine",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def get_context(patient_id: str):
    care = requests.get(f"{CARE_PLAN_URL}/{patient_id}", timeout=10).json()
    reasoning = requests.get(f"{REASON_URL}/{patient_id}", timeout=10).json()
    risk = requests.get(f"{RISK_URL}/{patient_id}", timeout=10).json()
    return care, reasoning, risk

def score_context(care, reasoning, risk):
    score = 0

    if risk.get("overall_risk") == "HIGH":
        score += 35
    elif risk.get("overall_risk") == "MODERATE":
        score += 20
    else:
        score += 8

    if risk.get("icu_risk") == "HIGH":
        score += 20

    if risk.get("bleeding_risk") == "HIGH":
        score += 15

    text = " ".join(reasoning.get("clinical_reasoning", [])).lower()

    if "coronary" in text or "troponin" in text:
        score += 12

    if "kidney" in text or "creatinine" in text or "potassium" in text:
        score += 10

    if "hyperglycemia" in text or "glucose" in text:
        score += 6

    problems = care.get("care_plan", {}).get("problem_list", [])
    score += min(len(problems) * 3, 12)

    return min(score, 100)

def probability_from_score(score, base=0.1, scale=0.008):
    return round(min(0.95, max(0.03, base + score * scale)), 2)

@router.get("/prognosis/{patient_id}")
def prognosis(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)

    deterioration = probability_from_score(score, base=0.08, scale=0.007)
    recovery = round(max(0.05, 1 - deterioration - 0.12), 2)
    survival = round(max(0.05, 1 - probability_from_score(score, base=0.02, scale=0.003)), 2)

    return {
        "status": "success",
        "patient_id": patient_id,
        "overall_prognosis": "GUARDED" if score >= 60 else "FAIR" if score >= 35 else "GOOD",
        "risk_score": score,
        "survival_probability": survival,
        "deterioration_probability": deterioration,
        "recovery_probability": recovery,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/icu-risk/{patient_id}")
def icu_risk(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)
    prob = probability_from_score(score, base=0.12, scale=0.008)

    return {
        "status": "success",
        "patient_id": patient_id,
        "icu_probability": prob,
        "recommended_level": "ICU" if prob >= 0.70 else "HDU" if prob >= 0.45 else "WARD",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/mortality/{patient_id}")
def mortality(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)
    prob = probability_from_score(score, base=0.03, scale=0.003)

    return {
        "status": "success",
        "patient_id": patient_id,
        "mortality_risk": "HIGH" if prob >= 0.25 else "MODERATE" if prob >= 0.12 else "LOW",
        "probability": prob,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/readmission/{patient_id}")
def readmission(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)
    prob = probability_from_score(score, base=0.18, scale=0.006)

    return {
        "status": "success",
        "patient_id": patient_id,
        "risk": "HIGH" if prob >= 0.65 else "MODERATE" if prob >= 0.35 else "LOW",
        "probability": prob,
        "window_days": 30,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/length-of-stay/{patient_id}")
def length_of_stay(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)

    expected_days = 2 + round(score / 12)

    return {
        "status": "success",
        "patient_id": patient_id,
        "expected_days": expected_days,
        "confidence": 0.86,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/outcome-score/{patient_id}")
def outcome_score(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)

    survival = round(max(0.05, 1 - probability_from_score(score, base=0.02, scale=0.003)), 2)
    icu = probability_from_score(score, base=0.12, scale=0.008)
    readmission_prob = probability_from_score(score, base=0.18, scale=0.006)
    deterioration = probability_from_score(score, base=0.08, scale=0.007)

    return {
        "status": "success",
        "patient_id": patient_id,
        "risk_score": score,
        "survival": survival,
        "icu": icu,
        "readmission": readmission_prob,
        "deterioration": deterioration,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/early-warning/{patient_id}")
def early_warning(patient_id: str):
    care, reasoning, risk = get_context(patient_id)
    score = score_context(care, reasoning, risk)

    return {
        "status": "success",
        "patient_id": patient_id,
        "alert_level": "HIGH" if score >= 65 else "MODERATE" if score >= 35 else "LOW",
        "warning": "Potential clinical deterioration" if score >= 65 else "Continue monitoring",
        "risk_score": score,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
