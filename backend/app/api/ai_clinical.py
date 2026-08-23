from fastapi import APIRouter

router = APIRouter(prefix="/ai-clinical", tags=["AI Clinical"])

@router.get("/analyze/{patient_id}")
def analyze_patient(patient_id: str):

    return {
        "patient_id": patient_id,

        "possible_conditions": [
            "Hypertension",
            "Coronary Artery Disease"
        ],

        "suggested_orders": [
            "ECG",
            "Troponin",
            "Chest X-Ray"
        ],

        "risk_level": "moderate",

        "ai_summary":
        "Possible cardiac-related condition detected.",

        "doctor_action_required": True
    }
