from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.db.database import get_db
from backend.app.db.models import DrugInventory, Prescription, AuditLog

router = APIRouter(
    prefix="/ahos/22.0/drug-db",
    tags=["AHOS 22.0.5 Real Drug Database"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.5",
        "engine": "Real Drug Database",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/seed-drugs")
def seed_drugs(db: Session = Depends(get_db)):
    drugs = [
        ("Paracetamol", 1200, 100),
        ("Amoxicillin", 800, 80),
        ("Metformin", 950, 100),
        ("Aspirin", 700, 70),
        ("Atorvastatin", 650, 60),
        ("Insulin", 300, 50),
        ("Omeprazole", 900, 100),
        ("Ceftriaxone", 400, 40)
    ]

    for name, stock, threshold in drugs:
        db.add(DrugInventory(
            tenant_id="TENANT-DEMO",
            drug_name=name,
            stock_quantity=stock,
            low_stock_threshold=threshold
        ))

    db.add(AuditLog(
        tenant_id="TENANT-DEMO",
        actor="system",
        role="Pharmacist",
        action="SEED_DRUG_DATABASE",
        resource="DrugInventory",
        severity="LOW",
        ip_address="127.0.0.1"
    ))

    db.commit()

    return {
        "status": "success",
        "message": "Drug database seeded",
        "drugs_added": len(drugs),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/inventory")
def inventory(db: Session = Depends(get_db)):
    rows = db.query(DrugInventory).order_by(DrugInventory.id.desc()).limit(50).all()

    return {
        "status": "success",
        "inventory": [
            {
                "drug_name": r.drug_name,
                "stock_quantity": r.stock_quantity,
                "low_stock_threshold": r.low_stock_threshold,
                "low_stock": r.stock_quantity <= r.low_stock_threshold
            }
            for r in rows
        ]
    }

@router.post("/create-prescription")
def create_prescription(db: Session = Depends(get_db)):
    rx = Prescription(
        tenant_id="TENANT-DEMO",
        patient_id="P-1001",
        medication_name="Paracetamol",
        dosage="500 mg",
        frequency="TID",
        duration_days=5,
        status="ACTIVE"
    )

    db.add(rx)
    db.add(AuditLog(
        tenant_id="TENANT-DEMO",
        actor="system",
        role="Pharmacist",
        action="CREATE_PRESCRIPTION",
        resource="Prescription/P-1001",
        severity="LOW",
        ip_address="127.0.0.1"
    ))

    db.commit()

    return {
        "status": "success",
        "message": "Prescription created",
        "patient_id": "P-1001",
        "medication_name": "Paracetamol",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/prescriptions")
def prescriptions(db: Session = Depends(get_db)):
    rows = db.query(Prescription).order_by(Prescription.id.desc()).limit(50).all()

    return {
        "status": "success",
        "prescriptions": [
            {
                "patient_id": r.patient_id,
                "medication_name": r.medication_name,
                "dosage": r.dosage,
                "frequency": r.frequency,
                "duration_days": r.duration_days,
                "status": r.status,
                "created_at": str(r.created_at)
            }
            for r in rows
        ]
    }

@router.get("/interaction-check")
def interaction_check(drug_a: str = "Warfarin", drug_b: str = "Aspirin"):
    high_risk_pairs = {
        ("Warfarin", "Aspirin"): "HIGH",
        ("Insulin", "Metformin"): "MODERATE",
        ("Ceftriaxone", "Aspirin"): "LOW"
    }

    severity = high_risk_pairs.get((drug_a, drug_b)) or high_risk_pairs.get((drug_b, drug_a)) or "NONE"

    return {
        "status": "success",
        "drug_a": drug_a,
        "drug_b": drug_b,
        "interaction_severity": severity,
        "clinical_action": "Pharmacist review required" if severity in ["MODERATE", "HIGH"] else "No major action required"
    }

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(DrugInventory).count()
    low = db.query(DrugInventory).filter(DrugInventory.stock_quantity <= DrugInventory.low_stock_threshold).count()

    return {
        "status": "success",
        "drug_database": {
            "inventory_items": total,
            "low_stock_items": low,
            "prescriptions": db.query(Prescription).count()
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "22.0.5",
            "status": "Real Drug Database Active",
            "strategic_value": "Creates real pharmacy inventory, prescription storage, interaction checking, and pharmacy audit events",
            "next_phase": "22.0.6 Real Laboratory Database"
        }
    }
