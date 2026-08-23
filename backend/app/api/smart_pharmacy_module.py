from fastapi import APIRouter

router = APIRouter(prefix="/smart-pharmacy", tags=["Smart Pharmacy Module"])

@router.get("/patient/{patient_id}")
def smart_pharmacy_patient_review(patient_id: str):
    return {
        "patient_id": patient_id,
        "current_medications": [
            "Aspirin 100mg",
            "Atorvastatin 20mg",
            "Metoprolol 50mg"
        ],
        "drug_interactions": [
            {
                "severity": "moderate",
                "message": "Monitor bleeding risk with Aspirin."
            }
        ],
        "ai_pharmacy_summary": "Medication profile reviewed. Moderate interaction risk detected.",
        "recommendations": [
            "Review blood pressure before beta-blocker dose.",
            "Check liver enzymes for statin therapy.",
            "Confirm aspirin indication."
        ],
        "doctor_approval_required": True,
        "pharmacist_review_required": True
    }
