from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/clinical-lifecycle", tags=["Clinical Lifecycle v1"])

ORDERS = []
LABS = []
MEDICATIONS = []

@router.post("/orders")
def create_order(payload: dict):
    order = {
        "id": f"ORD-{len(ORDERS)+1}",
        "patient_id": payload.get("patient_id"),
        "type": payload.get("type"),
        "name": payload.get("name"),
        "status": "ordered",
        "created_at": datetime.utcnow().isoformat()
    }
    ORDERS.append(order)
    return {"created": True, "order": order}

@router.get("/orders/{patient_id}")
def get_orders(patient_id: str):
    return [x for x in ORDERS if x.get("patient_id") == patient_id]

@router.post("/labs")
def create_lab(payload: dict):
    lab = {
        "id": f"LAB-{len(LABS)+1}",
        "patient_id": payload.get("patient_id"),
        "test": payload.get("test"),
        "result": payload.get("result"),
        "status": payload.get("status", "pending"),
        "created_at": datetime.utcnow().isoformat()
    }
    LABS.append(lab)
    return {"created": True, "lab": lab}

@router.get("/labs/{patient_id}")
def get_labs(patient_id: str):
    return [x for x in LABS if x.get("patient_id") == patient_id]

@router.post("/medications")
def create_medication(payload: dict):
    med = {
        "id": f"MED-{len(MEDICATIONS)+1}",
        "patient_id": payload.get("patient_id"),
        "drug": payload.get("drug"),
        "dose": payload.get("dose"),
        "frequency": payload.get("frequency"),
        "status": "active",
        "created_at": datetime.utcnow().isoformat()
    }
    MEDICATIONS.append(med)
    return {"created": True, "medication": med}

@router.put("/medications/{med_id}/status")
def update_medication_status(med_id: str, payload: dict):
    for med in MEDICATIONS:
        if med["id"] == med_id:
            med["status"] = payload.get("status", med["status"])
            med["updated_at"] = datetime.utcnow().isoformat()
            return {"updated": True, "medication": med}
    return {"error": "Medication not found"}

@router.get("/medications/{patient_id}")
def get_medications(patient_id: str):
    return [x for x in MEDICATIONS if x.get("patient_id") == patient_id]
