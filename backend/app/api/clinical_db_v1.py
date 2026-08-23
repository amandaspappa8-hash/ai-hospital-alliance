from fastapi import APIRouter

router = APIRouter(prefix="/clinical-db", tags=["Clinical Database v1"])

PATIENTS = {
    "P-1001": {
        "patient_id": "P-1001",
        "name": "Ahmed Ali",
        "age": 54,
        "gender": "Male",
        "diagnoses": ["Hypertension", "Coronary Artery Disease"],
        "allergies": ["Penicillin"],
        "medications": ["Aspirin 100mg", "Atorvastatin 20mg", "Metoprolol 50mg"],
        "labs": {"egfr": 42, "creatinine": 1.4, "alt": 42, "ast": 39},
        "orders": ["ECG", "Troponin", "Chest X-Ray"],
        "status": "Active"
    }
}

@router.get("/patients")
def list_patients():
    return list(PATIENTS.values())

@router.get("/patients/{patient_id}")
def get_patient(patient_id: str):
    return PATIENTS.get(patient_id, {"error": "Patient not found"})

@router.post("/patients")
def create_patient(payload: dict):
    patient_id = payload.get("patient_id")
    if not patient_id:
        return {"error": "patient_id is required"}

    PATIENTS[patient_id] = payload

    return {
        "created": True,
        "patient": payload
    }

@router.put("/patients/{patient_id}")
def update_patient(patient_id: str, payload: dict):
    PATIENTS[patient_id] = {
        **PATIENTS.get(patient_id, {}),
        **payload,
        "patient_id": patient_id
    }

    return {
        "updated": True,
        "patient": PATIENTS[patient_id]
    }
