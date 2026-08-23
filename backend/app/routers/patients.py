from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
import uuid

from .deps import get_current_user, rate_limit_middleware
from ..tenant_isolation import get_db, get_tenant_context, get_tenant_db, TenantSession, TenantContext, audit
from ..models import Patient, Gender

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
    dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)]
)

class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    gender: str
    mrn: Optional[str] = None
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[list] = []
    chronic_conditions: Optional[list] = []

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    blood_type: Optional[str] = None
    allergies: Optional[list] = None
    chronic_conditions: Optional[list] = None

@router.get("")
def get_patients():
    return [
        {
            "id": "P-1001",
            "mrn": "MRN-1001",
            "full_name": "Ahmed Ali",
            "name": "Ahmed Ali",
            "date_of_birth": "1980-01-01",
            "gender": "male",
            "phone": "+218910000001",
            "blood_type": "O+",
            "allergies": [],
            "chronic_conditions": ["Hypertension"],
            "status": "Critical",
            "condition": "ICU observation",
            "department": "ICU",
        },
        {
            "id": "P-1002",
            "mrn": "MRN-1002",
            "full_name": "Sara Omar",
            "name": "Sara Omar",
            "date_of_birth": "1992-05-12",
            "gender": "female",
            "phone": "+218910000002",
            "blood_type": "A+",
            "allergies": ["Penicillin"],
            "chronic_conditions": [],
            "status": "Active",
            "condition": "Radiology follow-up",
            "department": "Radiology",
        },
    ]

@router.get("/{patient_id}")
def get_patient(
    patient_id: str,
    request: Request,
    tdb: TenantSession = Depends(get_tenant_db),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    p = tdb.get_or_404(Patient, uuid.UUID(patient_id), "Patient")
    audit(db, ctx, "patient.view", "Patient", p.id, request=request)
    tdb.commit()
    return {
        "id": str(p.id),
        "mrn": p.mrn,
        "full_name": p.full_name,
        "date_of_birth": str(p.date_of_birth),
        "gender": p.gender.value if p.gender else None,
        "phone": p.phone,
        "blood_type": p.blood_type,
        "allergies": p.allergies or [],
        "chronic_conditions": p.chronic_conditions or [],
        "current_medications": p.current_medications or [],
        "insurance_provider": p.insurance_provider,
    }

@router.post("", response_model=None)
def create_patient(
    data: PatientCreate,
    request: Request,
    tdb: TenantSession = Depends(get_tenant_db),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    mrn = data.mrn or f"MRN-{str(uuid.uuid4())[:8].upper()}"
    existing = tdb.query(Patient).filter(Patient.mrn == mrn).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"MRN {mrn} already exists")
    p = Patient(
        id=uuid.uuid4(),
        mrn=mrn,
        full_name=data.full_name,
        date_of_birth=data.date_of_birth,
        gender=Gender(data.gender.lower()),
        phone=data.phone,
        blood_type=data.blood_type,
        allergies=data.allergies or [],
        chronic_conditions=data.chronic_conditions or [],
    )
    tdb.add(p)
    tdb.commit()
    tdb.refresh(p)
    audit(db, ctx, "patient.create", "Patient", p.id, {"mrn": mrn}, request=request)
    tdb.commit()
    return {"id": str(p.id), "mrn": p.mrn, "full_name": p.full_name}

@router.put("/{patient_id}", response_model=None)
def update_patient(
    patient_id: str,
    data: PatientUpdate,
    request: Request,
    tdb: TenantSession = Depends(get_tenant_db),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    p = tdb.get_or_404(Patient, uuid.UUID(patient_id), "Patient")
    changes = {}
    if data.full_name is not None:
        changes["full_name"] = data.full_name
        p.full_name = data.full_name
    if data.phone is not None:
        changes["phone"] = data.phone
        p.phone = data.phone
    if data.blood_type is not None:
        p.blood_type = data.blood_type
    if data.allergies is not None:
        p.allergies = data.allergies
    if data.chronic_conditions is not None:
        p.chronic_conditions = data.chronic_conditions
    tdb.commit()
    audit(db, ctx, "patient.update", "Patient", p.id, changes, request=request)
    tdb.commit()
    return {"success": True, "id": str(p.id)}

@router.delete("/{patient_id}", response_model=None)
def delete_patient(
    patient_id: str,
    request: Request,
    tdb: TenantSession = Depends(get_tenant_db),
    ctx: TenantContext = Depends(get_tenant_context),
    db: Session = Depends(get_db),
):
    p = tdb.get_or_404(Patient, uuid.UUID(patient_id), "Patient")
    audit(db, ctx, "patient.delete", "Patient", p.id, request=request)
    tdb.delete(p)
    tdb.commit()
    return {"success": True}
