from fastapi import APIRouter
from datetime import datetime
import requests

router = APIRouter(
    prefix="/aiha/10.4",
    tags=["AIHA 10.4 Autonomous Care Plan Generator"]
)

REASON_URL = "http://127.0.0.1:8000/aiha/10.3/reason"
RISK_URL = "http://127.0.0.1:8000/aiha/10.3/risk"

@router.get("/health")
def health():
    return {
        "status": "online",
        "stage": "AI Hospital Alliance 10.4",
        "engine": "Autonomous Care Plan Generator",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def build_problem_list(reasoning):
    problems = []
    dx = reasoning.get("differential_diagnosis", [])
    text = " ".join(reasoning.get("clinical_reasoning", [])).lower()

    for item in dx:
        problems.append({
            "problem": item.get("diagnosis"),
            "confidence": item.get("confidence"),
            "status": "active"
        })

    if "bleeding" in text:
        problems.append({
            "problem": "High medication-related bleeding risk",
            "confidence": 0.90,
            "status": "active"
        })

    return problems

def build_immediate_actions(reasoning, risk):
    actions = []
    text = " ".join(reasoning.get("clinical_reasoning", [])).lower()

    if risk.get("overall_risk") == "HIGH":
        actions.append("Escalate to senior physician / rapid clinical review.")

    if "coronary" in text or "troponin" in text:
        actions.extend([
            "Perform urgent ECG.",
            "Repeat troponin according to protocol.",
            "Request cardiology consultation."
        ])

    if "kidney" in text or "creatinine" in text or "potassium" in text:
        actions.extend([
            "Repeat renal function and electrolytes.",
            "Review urine output and fluid balance.",
            "Request nephrology review if abnormalities persist."
        ])

    if "hyperglycemia" in text or "glucose" in text:
        actions.append("Start or review glucose management protocol.")

    if risk.get("bleeding_risk") == "HIGH":
        actions.extend([
            "Hold or review high-risk anticoagulant/antiplatelet combination until physician review.",
            "Request pharmacist-led medication reconciliation."
        ])

    return list(dict.fromkeys(actions))

def build_monitoring_plan(risk):
    if risk.get("overall_risk") == "HIGH":
        return [
            "Monitor vital signs frequently.",
            "Continuous cardiac monitoring if clinically indicated.",
            "Repeat risk assessment after new lab/radiology results.",
            "Escalate to ICU review if deterioration occurs."
        ]

    return [
        "Continue routine monitoring.",
        "Repeat assessment if symptoms or vitals change."
    ]

def build_followups(reasoning):
    text = " ".join(reasoning.get("clinical_reasoning", [])).lower()

    labs = []
    imaging = []
    consults = []

    if "troponin" in text:
        labs.append("Repeat troponin.")
        consults.append("Cardiology")

    if "creatinine" in text or "potassium" in text or "kidney" in text:
        labs.extend(["Repeat creatinine.", "Repeat potassium.", "Check eGFR if available."])
        consults.append("Nephrology")

    if "glucose" in text:
        labs.append("Repeat glucose monitoring.")

    if "radiology" in text:
        imaging.append("Radiologist review and clinical correlation.")

    if "bleeding" in text:
        labs.extend(["CBC follow-up.", "Platelet count follow-up."])
        consults.append("Clinical Pharmacist")

    return {
        "lab_follow_up": list(dict.fromkeys(labs)),
        "radiology_follow_up": list(dict.fromkeys(imaging)),
        "consultations": list(dict.fromkeys(consults))
    }

@router.get("/plan/{patient_id}")
def care_plan(patient_id: str):
    reasoning = requests.get(f"{REASON_URL}/{patient_id}", timeout=10).json()
    risk = requests.get(f"{RISK_URL}/{patient_id}", timeout=10).json()

    followups = build_followups(reasoning)

    plan = {
        "problem_list": build_problem_list(reasoning),
        "immediate_actions": build_immediate_actions(reasoning, risk),
        "medication_safety": [
            "Review anticoagulants and antiplatelets.",
            "Check interaction risk before medication changes.",
            "Document pharmacist/doctor approval for high-risk combinations."
        ] if risk.get("bleeding_risk") == "HIGH" else [
            "Continue standard medication safety checks."
        ],
        "monitoring_plan": build_monitoring_plan(risk),
        "lab_follow_up": followups["lab_follow_up"],
        "radiology_follow_up": followups["radiology_follow_up"],
        "consultations": followups["consultations"],
        "discharge_criteria": [
            "Risk level reduced or clinically stable.",
            "Critical labs reviewed and improving.",
            "Medication risks reconciled.",
            "Follow-up plan documented."
        ]
    }

    return {
        "status": "success",
        "patient_id": patient_id,
        "stage": "AI Hospital Alliance 10.4",
        "overall_risk": risk.get("overall_risk"),
        "care_plan": plan,
        "source_engines": [
            "10.1 Unified Clinical Timeline",
            "10.2 Autonomous Clinical Story",
            "10.3 Autonomous Clinical Reasoning"
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
