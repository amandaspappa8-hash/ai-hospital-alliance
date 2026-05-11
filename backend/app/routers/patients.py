from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])

# ── GET all patients ──────────────────────────────────────────────────────────
@router.get("")
def get_patients():
    from ..repositories.registry import SERVICES
    return SERVICES["patients"].list_patients()

# ── GET single patient ────────────────────────────────────────────────────────
@router.get("/{patient_id}")
def get_patient(patient_id: str):
    from ..repositories.registry import SERVICES
    return SERVICES["patients"].get_patient(patient_id)

# ── POST create patient ───────────────────────────────────────────────────────
@router.post("", response_model=None)
def create_patient(data: dict, db: Session = Depends(get_db)):
    from ..models import Patient
    import uuid
    p = Patient(
        id=f"P-{str(uuid.uuid4())[:6].upper()}",
        name=data.get("name", ""),
        age=data.get("age", 0),
        gender=data.get("gender", "Male"),
        phone=data.get("phone", ""),
        condition=data.get("condition", ""),
        department_id=None,
        hospital_id="H-001",
        status=data.get("status", "Active"),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "name": p.name, "status": p.status}

# ── PUT update patient ────────────────────────────────────────────────────────
@router.put("/{patient_id}", response_model=None)
def update_patient(patient_id: str, data: dict, db: Session = Depends(get_db)):
    from ..models import Patient
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    for k, v in data.items():
        if hasattr(p, k) and k not in ("id", "hospital_id"):
            setattr(p, k, v)
    db.commit()
    return {"success": True}

# ── DELETE patient ────────────────────────────────────────────────────────────
@router.delete("/{patient_id}", response_model=None)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    from ..models import Patient
    p = db.query(Patient).filter(Patient.id == patient_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(p)
    db.commit()
    return {"success": True}
