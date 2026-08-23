import io
import time
import json
import zipfile
from backend.app.ahos_41_0_4.regulatory_submission_package import build_submission_package, list_submission_packages
from backend.app.ahos_41_0_4.regulatory_pdf_dossier import generate_regulatory_pdf_dossier, list_regulatory_dossiers
from backend.app.ahos_41_0_4.regulatory_audit_export import build_regulatory_export, list_regulatory_exports
from backend.app.ahos_41_0_4.integrity_recovery import recover_integrity, list_recoveries
from backend.app.ahos_41_0_4.tamper_detection import (
    verify_integrity,
    list_integrity_alerts,
    simulate_tamper
)
from backend.app.ahos_41_0_4.blockchain_verification import (
    register_locked_report_on_chain,
    verify_locked_report_chain,
    list_chain_blocks
)
from backend.app.ahos_41_0_4.final_report_locking import (
    lock_report,
    get_lock_status,
    list_locked_reports
)
from backend.app.ahos_41_0_4.review_decision_engine import (
    create_decision,
    list_decisions,
    get_decision_status
)
from backend.app.ahos_41_0_4.clinical_review import save_review, list_reviews
from fastapi.responses import FileResponse
from backend.app.ahos_41_0_4.evidence_package import build_evidence_package, list_evidence_packages
from backend.app.ahos_41_0_4.xai.gradcam import save_heatmap
from backend.app.ahos_41_0_4.export_reports_xai import export_pdf_xai, export_json_xai
from backend.app.ahos_41_0_4.xai.gradcam import save_heatmap
from backend.app.ahos_41_0_4.audit_governance import (
    log_ai_event,
    register_model,
    list_audit_events,
    list_models
)
from backend.app.ahos_41_0_4.dicom_upload_pipeline import process_uploaded_dicom
from backend.app.ahos_41_0_4.export_reports import (
    export_pdf,
    export_json
)
from backend.app.ahos_41_0_4.report_db_2000 import save_report, list_reports, get_report
from backend.app.ahos_41_0_4.clinical_report_2000 import generate_clinical_report
from fastapi import APIRouter, UploadFile, File, Response
from pydantic import BaseModel
from backend.app.ahos_41_0_4.infer_rsna_2000 import predict

router = APIRouter(
    prefix="/ahos/41.1/rsna-2000-ai",
    tags=["AHOS 41.1 RSNA 2000 AI"]
)

class RSNAInferenceRequest(BaseModel):
    image_path: str

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.1.4",
        "module": "RSNA 2000 Radiology AI",
        "model": "ResNet18-2000",
        "threshold": 0.30,
        "dataset": "RSNA Pneumonia Detection Challenge"
    }

@router.post("/predict")
async def predict_rsna(request: RSNAInferenceRequest):
    result = predict(request.image_path)

    return {
        "status": "success",
        "phase": "AHOS 41.1.4",
        "model": "rsna_resnet18_2000.pt",
        "threshold": 0.30,
        "result": result
    }


@router.post("/clinical-report")
async def clinical_report_rsna(request: RSNAInferenceRequest):
    report = generate_clinical_report(request.image_path)
    saved = save_report(report)
    audit = log_ai_event(report)

    return {
        "status": "success",
        "phase": "AHOS 41.2.0",
        "result": report,
        "database": saved,
        "audit": audit
    }

@router.get("/reports")
async def reports(limit: int = 20):
    return {
        "status": "success",
        "phase": "AHOS 41.1.6",
        "count": len(list_reports(limit)),
        "reports": list_reports(limit)
    }

@router.get("/reports/{report_id}")
async def report_detail(report_id: str):
    report = get_report(report_id)

    if not report:
        return {
            "status": "not_found",
            "phase": "AHOS 41.1.6",
            "report_id": report_id
        }

    return {
        "status": "success",
        "phase": "AHOS 41.1.6",
        "report": report
    }



@router.get("/reports/{report_id}/export/json")
async def export_report_json(report_id: str):

    report = get_report(report_id)

    if not report:
        return {
            "status":"not_found"
        }

    path = export_json(report)

    return {
        "status":"success",
        "phase":"AHOS 41.1.7",
        "json_file":path
    }


@router.get("/reports/{report_id}/export/pdf")
async def export_report_pdf(report_id: str):

    report = get_report(report_id)

    if not report:
        return {
            "status":"not_found"
        }

    path = export_pdf(report)

    return {
        "status":"success",
        "phase":"AHOS 41.1.7",
        "pdf_file":path
    }


class DICOMUploadPathRequest(BaseModel):
    dicom_path: str

@router.post("/upload-dicom-path")
async def upload_dicom_path(request: DICOMUploadPathRequest):
    result = process_uploaded_dicom(request.dicom_path)
    return {
        "status": "success",
        "phase": "AHOS 41.1.8",
        "pipeline": "DICOM Upload + AI Analysis + PDF/JSON Export",
        "result": result
    }



@router.post("/upload-dicom-file")
async def upload_dicom_file(file: UploadFile = File(...)):
    import shutil
    from pathlib import Path
    from backend.app.ahos_41_0_4.dicom_upload_pipeline import process_uploaded_dicom

    upload_dir = Path("uploads/rsna_dicom")
    upload_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file.filename).name
    saved_path = upload_dir / safe_name

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = process_uploaded_dicom(str(saved_path))

    return {
        "status": "success",
        "phase": "AHOS 41.1.9",
        "pipeline": "Real DICOM File Upload + AI Analysis + PDF/JSON Export",
        "uploaded_file": str(saved_path),
        "result": result
    }




@router.post("/governance/register-model")
async def governance_register_model():
    return {
        "status": "success",
        "phase": "AHOS 41.2.0",
        "result": register_model()
    }


@router.get("/governance/models")
async def governance_models():
    models = list_models()
    return {
        "status": "success",
        "phase": "AHOS 41.2.0",
        "count": len(models),
        "models": models
    }


@router.get("/audit/events")
async def audit_events(limit: int = 20):
    events = list_audit_events(limit)
    return {
        "status": "success",
        "phase": "AHOS 41.2.0",
        "count": len(events),
        "events": events
    }



@router.post("/explain")
async def explain_rsna(request: RSNAInferenceRequest):

    result = save_heatmap(
        request.image_path
    )

    return {
        "status":"success",
        "phase":"AHOS 41.2.1",
        "module":"Explainable Radiology AI",
        "result":result
    }




@router.post("/clinical-report-xai")
async def clinical_report_xai(request: RSNAInferenceRequest):
    report = generate_clinical_report(request.image_path)
    xai = save_heatmap(request.image_path)

    report["xai"] = xai

    saved = save_report(report)
    audit = log_ai_event(report)

    pdf = export_pdf_xai(report)
    js = export_json_xai(report)

    return {
        "status": "success",
        "phase": "AHOS 41.2.2",
        "module": "XAI Clinical PDF Report",
        "result": report,
        "database": saved,
        "audit": audit,
        "exports": {
            "pdf": pdf,
            "json": js
        }
    }




@router.post("/reports/{report_id}/evidence-package")
async def create_evidence_package(report_id: str):
    package = build_evidence_package(report_id)

    if not package:
        return {
            "status": "not_found",
            "phase": "AHOS 41.2.3",
            "report_id": report_id
        }

    return {
        "status": "success",
        "phase": "AHOS 41.2.3",
        "result": package
    }


@router.get("/evidence-packages")
async def evidence_packages():
    packages = list_evidence_packages()

    return {
        "status": "success",
        "phase": "AHOS 41.2.3",
        "count": len(packages),
        "packages": packages
    }



class ClinicalReviewRequest(BaseModel):
    reviewer_name: str
    decision: str
    comments: str



@router.get("/evidence-packages/{report_id}/download")
async def download_evidence_package(report_id: str):
    from pathlib import Path

    zip_path = Path("reports/rsna/evidence_packages") / f"{report_id}_evidence_package.zip"

    if not zip_path.exists():
        return {
            "status": "not_found",
            "phase": "AHOS 41.2.4",
            "report_id": report_id
        }

    return FileResponse(
        path=str(zip_path),
        filename=zip_path.name,
        media_type="application/zip"
    )


@router.post("/reports/{report_id}/clinical-review")
async def clinical_review(report_id: str, request: ClinicalReviewRequest):
    review = save_review(
        report_id=report_id,
        reviewer_name=request.reviewer_name,
        decision=request.decision,
        comments=request.comments
    )

    return {
        "status": "success",
        "phase": "AHOS 41.2.4",
        "review": review
    }


@router.get("/clinical-reviews")
async def clinical_reviews(limit: int = 20):
    reviews = list_reviews(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.4",
        "count": len(reviews),
        "reviews": reviews
    }



class ReviewDecisionRequest(BaseModel):
    reviewer_name: str
    decision: str
    comments: str



@router.post("/reports/{report_id}/decision")
async def review_decision(report_id: str, request: ReviewDecisionRequest):
    result = create_decision(
        report_id=report_id,
        reviewer_name=request.reviewer_name,
        decision=request.decision,
        comments=request.comments
    )

    return {
        "status": "success",
        "phase": "AHOS 41.2.5",
        "result": result
    }


@router.get("/review-decisions")
async def review_decisions(limit: int = 20):
    decisions = list_decisions(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.5",
        "count": len(decisions),
        "decisions": decisions
    }


@router.get("/reports/{report_id}/decision-status")
async def decision_status(report_id: str):
    return {
        "status": "success",
        "phase": "AHOS 41.2.5",
        "result": get_decision_status(report_id)
    }



class LockReportRequest(BaseModel):
    signed_by: str



@router.post("/reports/{report_id}/lock")
async def lock_radiology_report(report_id: str, request: LockReportRequest):
    result = lock_report(
        report_id=report_id,
        signed_by=request.signed_by
    )

    return {
        "status": "success",
        "phase": "AHOS 41.2.6",
        "result": result
    }


@router.get("/reports/{report_id}/lock-status")
async def radiology_report_lock_status(report_id: str):
    return {
        "status": "success",
        "phase": "AHOS 41.2.6",
        "result": get_lock_status(report_id)
    }


@router.get("/locked-reports")
async def locked_reports(limit: int = 20):
    reports = list_locked_reports(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.6",
        "count": len(reports),
        "locked_reports": reports
    }




@router.post("/reports/{report_id}/blockchain/register")
async def blockchain_register_report(report_id: str):
    result = register_locked_report_on_chain(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.2.7",
        "result": result
    }


@router.get("/reports/{report_id}/blockchain/verify")
async def blockchain_verify_report(report_id: str):
    result = verify_locked_report_chain(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.2.7",
        "result": result
    }


@router.get("/blockchain/blocks")
async def blockchain_blocks(limit: int = 20):
    blocks = list_chain_blocks(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.7",
        "count": len(blocks),
        "blocks": blocks
    }




@router.get("/reports/{report_id}/integrity/verify")
async def integrity_verify(report_id: str):
    result = verify_integrity(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.2.8",
        "result": result
    }


@router.get("/integrity/alerts")
async def integrity_alerts(limit: int = 20):
    alerts = list_integrity_alerts(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.8",
        "count": len(alerts),
        "alerts": alerts
    }


@router.post("/reports/{report_id}/integrity/simulate-tamper")
async def integrity_simulate_tamper(report_id: str):
    result = simulate_tamper(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.2.8",
        "result": result
    }



class IntegrityRecoveryRequest(BaseModel):
    recovered_by: str



@router.post("/reports/{report_id}/integrity/recover")
async def integrity_recover(report_id: str, request: IntegrityRecoveryRequest):
    result = recover_integrity(
        report_id=report_id,
        recovered_by=request.recovered_by
    )

    return {
        "status": "success",
        "phase": "AHOS 41.2.9",
        "result": result
    }


@router.get("/integrity/recoveries")
async def integrity_recoveries(limit: int = 20):
    recoveries = list_recoveries(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.2.9",
        "count": len(recoveries),
        "recoveries": recoveries
    }




@router.post("/reports/{report_id}/regulatory/export")
async def regulatory_export(report_id: str):
    result = build_regulatory_export(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.3.0",
        "result": result
    }


@router.get("/regulatory/exports")
async def regulatory_exports(limit: int = 20):
    exports = list_regulatory_exports(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.3.0",
        "count": len(exports),
        "exports": exports
    }




@router.post("/reports/{report_id}/regulatory/dossier")
async def regulatory_dossier(report_id: str):
    result = generate_regulatory_pdf_dossier(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.3.1",
        "result": result
    }


@router.get("/regulatory/dossiers")
async def regulatory_dossiers(limit: int = 20):
    dossiers = list_regulatory_dossiers(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.3.1",
        "count": len(dossiers),
        "dossiers": dossiers
    }




@router.post("/reports/{report_id}/regulatory/submission-package")
async def regulatory_submission_package(report_id: str):
    result = build_submission_package(report_id)

    return {
        "status": "success",
        "phase": "AHOS 41.3.2",
        "result": result
    }


@router.get("/regulatory/submission-packages")
async def regulatory_submission_packages(limit: int = 20):
    packages = list_submission_packages(limit)

    return {
        "status": "success",
        "phase": "AHOS 41.3.2",
        "count": len(packages),
        "packages": packages
    }


@router.get("/regulatory/dossiers/{filename:path}/download")
async def download_regulatory_dossier(filename: str):
    file_path = Path("reports/rsna/regulatory_dossiers") / Path(filename).name

    if not file_path.exists():
        return {
            "status": "not_found",
            "phase": "AHOS 41.3.2",
            "filename": filename
        }

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/pdf"
    )


@router.get("/regulatory/submissions/{filename:path}/download")
async def download_regulatory_submission(filename: str):
    file_path = Path("reports/rsna/regulatory_submissions") / Path(filename).name

    if not file_path.exists():
        return {
            "status": "not_found",
            "phase": "AHOS 41.3.2",
            "filename": filename
        }

    return FileResponse(
        path=str(file_path),
        filename=file_path.name,
        media_type="application/zip"
    )









@router.get("/reports/{report_id}/regulatory/dossier-download")
async def download_regulatory_dossier(report_id: str):
    content = f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Kids [3 0 R] /Count 1 >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 160 >>
stream
BT
/F1 18 Tf
72 720 Td
(AHOS Regulatory PDF Dossier) Tj
0 -30 Td
(Report ID: {report_id}) Tj
0 -30 Td
(Status: Generated successfully) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
trailer
<< /Root 1 0 R >>
%%EOF
"""
    return Response(
        content=content.encode("utf-8"),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{report_id}_regulatory_dossier.pdf"'
        },
    )
@router.get("/reports/{report_id}/regulatory/submission-download")
async def download_regulatory_submission(report_id: str):
    buffer = io.BytesIO()

    manifest = {
        "project": "AI Hospital Alliance AHOS",
        "module": "AHOS 41.3.2 Regulatory Submission Package",
        "report_id": report_id,
        "status": "generated",
        "timestamp": time.time()
    }

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(manifest, indent=2))
        z.writestr("dossier/README.txt", "AHOS Regulatory Dossier")
        z.writestr("clinical_evidence/README.txt", "Clinical Evidence")
        z.writestr("risk_management/README.txt", "Risk Management")
        z.writestr("validation/README.txt", "Validation Evidence")
        z.writestr("traceability/README.txt", "Traceability Matrix")
        z.writestr("cybersecurity/README.txt", "Cybersecurity Evidence")
        z.writestr("post_market/README.txt", "Post Market Surveillance")

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{report_id}_submission_package.zip"'
        },
    )
@router.get("/regulatory/file-download/{kind}/{report_id}")
async def regulatory_file_download_clean(kind: str, report_id: str):
    from pathlib import Path
    from fastapi import Response

    if kind == "pdf":
        folder = Path("reports/rsna/regulatory_dossiers")
        pattern = f"*{report_id}*.pdf"
        media = "application/pdf"
    elif kind == "zip":
        folder = Path("reports/rsna/regulatory_submissions")
        pattern = f"*{report_id}*.zip"
        media = "application/zip"
    else:
        return {"status": "invalid_kind", "allowed": ["pdf", "zip"]}

    files = sorted(folder.glob(pattern), reverse=True)

    if not files:
        return {
            "status": "not_found",
            "folder": str(folder),
            "pattern": pattern,
            "report_id": report_id
        }

    file_path = files[0]

    return Response(
        content=file_path.read_bytes(),
        media_type=media,
        headers={
            "Content-Disposition": f'attachment; filename="{file_path.name}"'
        }
    )
