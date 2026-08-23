from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from backend.app.db.database import get_db
from backend.app.db.models import RadiologyStudy, AuditLog

router = APIRouter(
    prefix="/ahos/22.0/ohif-viewer",
    tags=["AHOS 22.0.4 Real OHIF Viewer Integration"]
)

OHIF_URL = "http://localhost:3005"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "22.0.4",
        "engine": "Real OHIF Viewer Integration",
        "ohif_url": OHIF_URL,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/open/{study_uid}")
def open_study(study_uid: str, db: Session = Depends(get_db)):
    row = db.query(RadiologyStudy).filter(RadiologyStudy.study_uid == study_uid).first()

    if not row:
        return {
            "status": "not_found",
            "study_uid": study_uid
        }

    viewer_url = f"{OHIF_URL}/viewer?StudyInstanceUIDs={study_uid}"

    audit = AuditLog(
        tenant_id=row.tenant_id,
        actor="system",
        role="Radiology",
        action="OPEN_OHIF_VIEWER",
        resource=f"ImagingStudy/{study_uid}",
        severity="LOW",
        ip_address="127.0.0.1"
    )

    db.add(audit)
    db.commit()

    return {
        "status": "success",
        "study_uid": study_uid,
        "patient_id": row.patient_id,
        "modality": row.modality,
        "description": row.description,
        "ohif_viewer_url": viewer_url,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/viewer-links")
def viewer_links(db: Session = Depends(get_db)):
    rows = db.query(RadiologyStudy).order_by(RadiologyStudy.id.desc()).limit(20).all()

    return {
        "status": "success",
        "viewer_links": [
            {
                "patient_id": r.patient_id,
                "study_uid": r.study_uid,
                "modality": r.modality,
                "description": r.description,
                "ohif_viewer_url": f"{OHIF_URL}/viewer?StudyInstanceUIDs={r.study_uid}"
            }
            for r in rows
        ]
    }

@router.get("/config")
def config():
    return {
        "status": "success",
        "ohif": {
            "base_url": OHIF_URL,
            "viewer_template": f"{OHIF_URL}/viewer?StudyInstanceUIDs={{study_uid}}",
            "mode": "DICOMweb",
            "connected_to": "Orthanc",
            "recommended_next": "Add frontend radiology viewer page with clickable OHIF links"
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "22.0.4",
            "status": "Real OHIF Viewer Integration Active",
            "strategic_value": "Creates real OHIF viewer links for stored DICOM studies and logs viewer access events",
            "next_phase": "22.0.5 Real Drug Database"
        }
    }
