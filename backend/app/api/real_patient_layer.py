from fastapi import APIRouter

router = APIRouter(prefix="/real-patient-layer", tags=["Real Patient Data Layer"])

@router.get("/patient/{patient_id}")
def get_real_patient_layer(patient_id: str):
    return {
        "patient_id": patient_id,
        "demographics": {
            "name": "Ahmed Ali",
            "age": 54,
            "gender": "Male"
        },
        "diagnoses": ["Hypertension", "Coronary Artery Disease"],
        "allergies": ["Penicillin"],
        "vitals": {
            "bp": "150/95",
            "hr": 88,
            "spo2": 97
        },
        "labs": {
            "egfr": 42,
            "creatinine": 1.4,
            "alt": 42,
            "ast": 39
        },
        "medications": [
            "Aspirin 100mg",
            "Atorvastatin 20mg",
            "Metoprolol 50mg"
        ],
        "orders": ["ECG", "Troponin", "Chest X-Ray"],
        "clinical_memory": [
            "Previous high blood pressure episode",
            "Medication safety review required"
        ]
    }
