from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
import json
import uuid

from backend.app.db.database import get_db
from backend.app.db.models import FHIRResource, AuditLog

router = APIRouter(
    prefix="/ahos/22.0/fhir-storage",
    tags=["AHOS 22.0.2 Real FHIR Resource Storage"]
)

class PatientInput(BaseModel):
    patient_id: str = "P-1001"
    name: str = "Demo Patient"
    gender: str = "unknown"
    birth_date: str = "1970-01-01"
    tenant_id: str = "TENANT-DEMO"

class ObservationInput(BaseModel):
    observation_id: str | None = None
    patient_id: str = "P-1001"
    code: str = "AIHA Clinical Score"
    value: float = 88
    unit: str = "score"
    tenant_id: str = "TENANT-DEMO"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.2",
        "engine": "Real FHIR Resource Storage",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/store-patient")
def store_patient(req: PatientInput, db: Session = Depends(get_db)):
    resource_id = req.patient_id

    parts = req.name.strip().split()
    family = parts[-1] if parts else "Unknown"
    given = parts[:-1] if len(parts) > 1 else parts or ["Unknown"]

    patient_resource = {
        "resourceType": "Patient",
        "id": resource_id,
        "identifier": [{"system": "urn:aiha:patient", "value": resource_id}],
        "name": [{"use": "official", "family": family, "given": given}],
        "gender": req.gender,
        "birthDate": req.birth_date
    }

    fhir = (
        db.query(FHIRResource)
        .filter(FHIRResource.tenant_id == req.tenant_id)
        .filter(FHIRResource.resource_type == "Patient")
        .filter(FHIRResource.resource_id == resource_id)
        .first()
    )

    if fhir:
        fhir.resource_json = json.dumps(patient_resource)
    else:
        fhir = FHIRResource(
            tenant_id=req.tenant_id,
            resource_type="Patient",
            resource_id=resource_id,
            resource_json=json.dumps(patient_resource)
        )
        db.add(fhir)

    audit = AuditLog(
        tenant_id=req.tenant_id,
        actor="system",
        role="Admin",
        action="STORE_FHIR_PATIENT",
        resource=f"Patient/{resource_id}",
        severity="LOW",
        ip_address="127.0.0.1"
    )

    db.add(audit)
    db.commit()

    return {
        "status": "stored",
        "resourceType": "Patient",
        "resource_id": resource_id,
        "resource": patient_resource,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/store-observation")
def store_observation(req: ObservationInput, db: Session = Depends(get_db)):
    resource_id = req.observation_id or str(uuid.uuid4())

    observation_resource = {
        "resourceType": "Observation",
        "id": resource_id,
        "status": "final",
        "code": {"text": req.code},
        "subject": {"reference": f"Patient/{req.patient_id}"},
        "valueQuantity": {"value": req.value, "unit": req.unit},
        "effectiveDateTime": datetime.utcnow().isoformat()
    }

    fhir = (
        db.query(FHIRResource)
        .filter(FHIRResource.tenant_id == req.tenant_id)
        .filter(FHIRResource.resource_type == "Observation")
        .filter(FHIRResource.resource_id == resource_id)
        .first()
    )

    if fhir:
        fhir.resource_json = json.dumps(observation_resource)
    else:
        fhir = FHIRResource(
            tenant_id=req.tenant_id,
            resource_type="Observation",
            resource_id=resource_id,
            resource_json=json.dumps(observation_resource)
        )
        db.add(fhir)

    audit = AuditLog(
        tenant_id=req.tenant_id,
        actor="system",
        role="Admin",
        action="STORE_FHIR_OBSERVATION",
        resource=f"Observation/{resource_id}",
        severity="LOW",
        ip_address="127.0.0.1"
    )

    db.add(audit)
    db.commit()

    return {
        "status": "stored",
        "resourceType": "Observation",
        "resource_id": resource_id,
        "resource": observation_resource,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/resources")
def resources(db: Session = Depends(get_db)):
    rows = db.query(FHIRResource).order_by(FHIRResource.id.desc()).limit(20).all()

    return {
        "status": "success",
        "resources": [
            {
                "id": r.id,
                "tenant_id": r.tenant_id,
                "resource_type": r.resource_type,
                "resource_id": r.resource_id,
                "created_at": str(r.created_at)
            }
            for r in rows
        ]
    }

@router.get("/resource/{resource_type}/{resource_id}")
def get_resource(resource_type: str, resource_id: str, db: Session = Depends(get_db)):
    row = (
        db.query(FHIRResource)
        .filter(FHIRResource.resource_type == resource_type)
        .filter(FHIRResource.resource_id == resource_id)
        .first()
    )

    if not row:
        return {"status": "not_found", "resource_type": resource_type, "resource_id": resource_id}

    return {
        "status": "success",
        "resource_type": row.resource_type,
        "resource_id": row.resource_id,
        "resource": json.loads(row.resource_json)
    }

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "status": "success",
        "fhir_storage": {
            "patients": db.query(FHIRResource).filter(FHIRResource.resource_type == "Patient").count(),
            "observations": db.query(FHIRResource).filter(FHIRResource.resource_type == "Observation").count(),
            "diagnostic_reports": db.query(FHIRResource).filter(FHIRResource.resource_type == "DiagnosticReport").count(),
            "medication_requests": db.query(FHIRResource).filter(FHIRResource.resource_type == "MedicationRequest").count(),
            "imaging_studies": db.query(FHIRResource).filter(FHIRResource.resource_type == "ImagingStudy").count(),
            "total": db.query(FHIRResource).count()
        }
    }


@router.get("/audit-events")
def fhir_audit_events(db: Session = Depends(get_db)):
    rows = (
        db.query(AuditLog)
        .filter(AuditLog.action.in_(["STORE_FHIR_PATIENT", "STORE_FHIR_OBSERVATION"]))
        .order_by(AuditLog.id.desc())
        .limit(50)
        .all()
    )

    return {
        "status": "success",
        "total": len(rows),
        "events": [
            {
                "id": r.id,
                "tenant_id": r.tenant_id,
                "actor": r.actor,
                "role": r.role,
                "action": r.action,
                "resource": r.resource,
                "severity": r.severity,
                "ip_address": r.ip_address,
                "created_at": str(r.created_at)
            }
            for r in rows
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "22.0.2",
            "status": "Real FHIR Resource Storage Active",
            "strategic_value": "Stores real FHIR Patient and Observation resources in the production database with audit logging",
            "next_phase": "22.0.3 Real Orthanc DICOM Integration"
        }
    }
