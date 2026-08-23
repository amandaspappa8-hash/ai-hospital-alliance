from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

router = APIRouter(prefix="/ai-ultrasound-x/reports", tags=["AI Ultrasound X Reports"])

ULTRASOUND_REPORTS = []

class UltrasoundReportCreate(BaseModel):
    patient_id: str
    patient_name: Optional[str] = None
    study_type: str = "Ultrasound"
    finding: str
    confidence: float
    risk_level: str
    lesion_area: Optional[int] = None
    ai_model: str = "MONAI UNet"
    notes: Optional[str] = None

@router.post("/save")
def save_ultrasound_report(report: UltrasoundReportCreate):
    new_report = {
        "report_id": f"USX-{len(ULTRASOUND_REPORTS)+1:04d}",
        "created_at": datetime.utcnow().isoformat(),
        "status": "saved",
        **report.model_dump()
    }

    ULTRASOUND_REPORTS.append(new_report)

    return {
        "status": "success",
        "message": "AI Ultrasound X report saved successfully",
        "report": new_report
    }

@router.get("/")
def list_ultrasound_reports():
    return {
        "status": "success",
        "count": len(ULTRASOUND_REPORTS),
        "reports": ULTRASOUND_REPORTS
    }

@router.get("/patient/{patient_id}")
def get_patient_ultrasound_reports(patient_id: str):
    patient_reports = [
        r for r in ULTRASOUND_REPORTS if r["patient_id"] == patient_id
    ]

    return {
        "status": "success",
        "patient_id": patient_id,
        "count": len(patient_reports),
        "reports": patient_reports
    }

@router.get("/{report_id}")
def get_ultrasound_report(report_id: str):
    for report in ULTRASOUND_REPORTS:
        if report["report_id"] == report_id:
            return {
                "status": "success",
                "report": report
            }

    return {
        "status": "not_found",
        "message": "Report not found"
    }
