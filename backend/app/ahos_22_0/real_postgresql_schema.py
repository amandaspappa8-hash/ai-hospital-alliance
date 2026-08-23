from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from backend.app.db.database import Base, engine, get_db
from backend.app.db.models import (
    Tenant,
    Patient,
    Encounter,
    LabResult,
    RadiologyStudy,
    Prescription,
    DrugInventory,
    FHIRResource,
    AuditLog,
)

router = APIRouter(
    prefix="/ahos/22.0/postgresql-schema",
    tags=["AHOS 22.0.1 Real PostgreSQL Schema"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.1",
        "engine": "Real PostgreSQL Schema",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/create-tables")
def create_tables():
    Base.metadata.create_all(bind=engine)

    return {
        "status": "success",
        "message": "Database tables created successfully",
        "tables": [
            "tenants",
            "patients",
            "encounters",
            "lab_results",
            "radiology_studies",
            "prescriptions",
            "drug_inventory",
            "fhir_resources",
            "audit_logs"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/seed-demo")
def seed_demo(db: Session = Depends(get_db)):
    tenant_id = "TENANT-DEMO"

    tenant = Tenant(
        tenant_id=tenant_id,
        name="Tripoli Central AI Hospital",
        country="Libya",
        region="Tripoli",
        status="ACTIVE"
    )

    patient = Patient(
        tenant_id=tenant_id,
        patient_id="P-1001",
        full_name="Demo Patient",
        gender="unknown",
        birth_date="1970-01-01"
    )

    encounter = Encounter(
        tenant_id=tenant_id,
        encounter_id="ENC-2026-001",
        patient_id="P-1001",
        department="Emergency",
        status="in-progress"
    )

    lab = LabResult(
        tenant_id=tenant_id,
        patient_id="P-1001",
        test_code="CRP",
        test_name="C-Reactive Protein",
        value="78",
        unit="mg/L",
        abnormal_flag="H",
        critical=False
    )

    study = RadiologyStudy(
        tenant_id=tenant_id,
        patient_id="P-1001",
        study_uid="1.2.826.0.1.3680043.2.1125.1001",
        modality="CT",
        description="Demo Chest CT",
        ohif_url="http://localhost:3005/viewer?StudyInstanceUIDs=1.2.826.0.1.3680043.2.1125.1001"
    )

    prescription = Prescription(
        tenant_id=tenant_id,
        patient_id="P-1001",
        medication_name="Paracetamol",
        dosage="500 mg",
        frequency="TID",
        duration_days=5
    )

    inventory = DrugInventory(
        tenant_id=tenant_id,
        drug_name="Paracetamol",
        stock_quantity=1200,
        low_stock_threshold=100
    )

    audit = AuditLog(
        tenant_id=tenant_id,
        actor="system",
        role="Admin",
        action="SEED_DEMO_DATA",
        resource="Database",
        severity="LOW",
        ip_address="127.0.0.1"
    )

    db.add_all([
        tenant,
        patient,
        encounter,
        lab,
        study,
        prescription,
        inventory,
        audit
    ])

    db.commit()

    return {
        "status": "success",
        "message": "Demo production schema data inserted",
        "tenant_id": tenant_id,
        "patient_id": "P-1001",
        "encounter_id": "ENC-2026-001",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/counts")
def counts(db: Session = Depends(get_db)):
    return {
        "status": "success",
        "counts": {
            "tenants": db.query(Tenant).count(),
            "patients": db.query(Patient).count(),
            "encounters": db.query(Encounter).count(),
            "lab_results": db.query(LabResult).count(),
            "radiology_studies": db.query(RadiologyStudy).count(),
            "prescriptions": db.query(Prescription).count(),
            "drug_inventory": db.query(DrugInventory).count(),
            "fhir_resources": db.query(FHIRResource).count(),
            "audit_logs": db.query(AuditLog).count()
        }
    }

@router.get("/schema")
def schema():
    return {
        "status": "success",
        "phase": "22.0.1 Real PostgreSQL Schema",
        "schema": {
            "tenants": ["tenant_id", "name", "country", "region", "status"],
            "patients": ["tenant_id", "patient_id", "full_name", "gender", "birth_date"],
            "encounters": ["tenant_id", "encounter_id", "patient_id", "department", "status"],
            "lab_results": ["tenant_id", "patient_id", "test_code", "value", "critical"],
            "radiology_studies": ["tenant_id", "patient_id", "study_uid", "modality", "ohif_url"],
            "prescriptions": ["tenant_id", "patient_id", "medication_name", "dosage", "frequency"],
            "drug_inventory": ["tenant_id", "drug_name", "stock_quantity", "low_stock_threshold"],
            "fhir_resources": ["tenant_id", "resource_type", "resource_id", "resource_json"],
            "audit_logs": ["tenant_id", "actor", "role", "action", "resource", "severity"]
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "22.0.1",
            "status": "Real PostgreSQL Schema Active",
            "strategic_value": "Creates real database foundation for tenants, patients, encounters, labs, radiology, pharmacy, FHIR resources, and audit logs",
            "next_phase": "22.0.2 Real FHIR Resource Storage"
        }
    }
