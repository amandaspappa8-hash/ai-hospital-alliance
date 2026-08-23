from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.db.database import get_db
from backend.app.db.models import LabResult, AuditLog

router = APIRouter(
    prefix="/ahos/22.0/lab-db",
    tags=["AHOS 22.0.6 Real Laboratory Database"]
)

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.6",
        "engine": "Real Laboratory Database",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/seed-results")
def seed_results(db: Session = Depends(get_db)):
    results = [
        ("CBC", "WBC", "12.4", "10^9/L", "H", False),
        ("CBC", "Hemoglobin", "13.8", "g/dL", "N", False),
        ("CRP", "C-Reactive Protein", "78", "mg/L", "H", False),
        ("RFT", "Creatinine", "142", "umol/L", "H", False),
        ("CARDIAC", "Troponin", "420", "ng/L", "HH", True),
    ]

    for code, name, value, unit, flag, critical in results:
        db.add(LabResult(
            tenant_id="TENANT-DEMO",
            patient_id="P-1001",
            test_code=code,
            test_name=name,
            value=value,
            unit=unit,
            abnormal_flag=flag,
            critical=critical
        ))

    db.add(AuditLog(
        tenant_id="TENANT-DEMO",
        actor="system",
        role="Laboratory",
        action="SEED_LAB_RESULTS",
        resource="LabResult/P-1001",
        severity="LOW",
        ip_address="127.0.0.1"
    ))

    db.commit()

    return {
        "status": "success",
        "message": "Laboratory database seeded",
        "results_added": len(results),
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/results/{patient_id}")
def patient_results(patient_id: str, db: Session = Depends(get_db)):
    rows = db.query(LabResult).filter(LabResult.patient_id == patient_id).order_by(LabResult.id.desc()).all()

    return {
        "status": "success",
        "patient_id": patient_id,
        "results": [
            {
                "test_code": r.test_code,
                "test_name": r.test_name,
                "value": r.value,
                "unit": r.unit,
                "abnormal_flag": r.abnormal_flag,
                "critical": r.critical,
                "created_at": str(r.created_at)
            }
            for r in rows
        ]
    }

@router.get("/critical-results")
def critical_results(db: Session = Depends(get_db)):
    rows = db.query(LabResult).filter(LabResult.critical == True).order_by(LabResult.id.desc()).limit(20).all()

    return {
        "status": "success",
        "critical_results": [
            {
                "patient_id": r.patient_id,
                "test_code": r.test_code,
                "test_name": r.test_name,
                "value": r.value,
                "unit": r.unit,
                "abnormal_flag": r.abnormal_flag,
                "requires_physician_notification": True
            }
            for r in rows
        ]
    }

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    return {
        "status": "success",
        "laboratory_database": {
            "total_results": db.query(LabResult).count(),
            "critical_results": db.query(LabResult).filter(LabResult.critical == True).count(),
            "abnormal_results": db.query(LabResult).filter(LabResult.abnormal_flag != "N").count()
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "22.0.6",
            "status": "Real Laboratory Database Active",
            "strategic_value": "Stores real lab results, abnormal flags, critical result alerts, and laboratory audit events",
            "next_phase": "22.0.7 Real Multi-Tenant SaaS"
        }
    }
