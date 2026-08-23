from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List

router = APIRouter(
    prefix="/api/ophthalmology",
    tags=["AHOS Ophthalmology AI Eye Center"]
)

class EyeDiagnosisRequest(BaseModel):
    patient_id: Optional[str] = "DEMO-EYE-001"
    mode: Optional[str] = "retina"
    selected_module: Optional[str] = None
    language: Optional[str] = "ar"
    symptoms: Optional[str] = ""
    image_type: Optional[str] = "fundus_or_oct_demo"
    iop: Optional[float] = None
    diabetes: Optional[bool] = False
    hypertension: Optional[bool] = False
    visual_loss: Optional[bool] = False
    severe_pain: Optional[bool] = False

def get_mode(req: EyeDiagnosisRequest) -> str:
    return (req.selected_module or req.mode or "retina").lower()

def calculate_risk(req: EyeDiagnosisRequest) -> Dict[str, Any]:
    score = 28
    mode = get_mode(req)

    score += {
        "retina": 12,
        "oct": 18,
        "glaucoma": 28,
        "fundus": 10,
        "emergency": 60,
    }.get(mode, 12)

    if req.iop and req.iop >= 22:
        score += 18
    if req.iop and req.iop >= 30:
        score += 12
    if req.diabetes:
        score += 10
    if req.hypertension:
        score += 8
    if req.visual_loss:
        score += 25
    if req.severe_pain:
        score += 20

    s = (req.symptoms or "").lower()
    urgent_words = ["vision loss", "sudden", "severe pain", "فقدان", "مفاجئ", "ألم شديد", "نقص النظر"]
    if any(w in s for w in urgent_words):
        score += 18

    score = min(score, 98)

    if score >= 75:
        return {
            "risk_score": score,
            "risk_level": "HIGH",
            "urgency": "urgent_ophthalmology_review",
            "safety_gate": "REQUIRES_DOCTOR_REVIEW"
        }

    if score >= 45:
        return {
            "risk_score": score,
            "risk_level": "MODERATE",
            "urgency": "specialist_follow_up",
            "safety_gate": "REVIEW_RECOMMENDED"
        }

    return {
        "risk_score": score,
        "risk_level": "LOW",
        "urgency": "routine_follow_up",
        "safety_gate": "DEMO_SAFE"
    }

@router.get("/health")
async def ophthalmology_health():
    return {
        "status": "online",
        "module": "AHOS Ophthalmology AI Eye Center",
        "version": "1.2.0",
        "frontend_route": "/ophthalmology",
        "clinical_status": "prototype_not_certified",
        "pdf_export": "enabled",
        "features": [
            "retina_intelligence",
            "oct_layer_analysis",
            "glaucoma_risk_engine",
            "fundus_screening",
            "critical_eye_case_simulation",
            "multilingual_report",
            "pdf_report_export",
            "clinical_safety_gate"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/kpis")
async def ophthalmology_kpis():
    return {
        "status": "online",
        "eye_scans": 1240,
        "retina_screenings": 520,
        "oct_studies": 310,
        "glaucoma_alerts": 44,
        "critical_eye_cases": 9,
        "fundus_images_ready": True,
        "oct_ready": True,
        "safety_gate": "ACTIVE",
        "average_ai_eye_risk": 42,
        "module_status": "demo_operational",
        "selected_specialty": "Ophthalmology",
        "selected_organ": "Eyes"
    }

@router.post("/diagnose")
async def ophthalmology_diagnose(req: EyeDiagnosisRequest):
    risk = calculate_risk(req)
    mode = get_mode(req)

    interpretations = {
        "ar": "تحليل عيون ذكي تجريبي يربط الشبكية و OCT والجلوكوما وقاع العين مع مؤشر خطورة بصري وبوابة أمان سريرية.",
        "en": "Experimental AI ophthalmology interpretation linking retina, OCT, glaucoma and fundus findings with a visual risk score and clinical safety gate.",
        "sv": "Experimentell AI-tolkning för ögon som kopplar näthinna, OCT, glaukom och ögonbotten till risknivå och säkerhetsgranskning.",
        "fr": "Interprétation ophtalmologique IA expérimentale reliant rétine, OCT, glaucome et fond d’œil au score de risque et à la sécurité clinique.",
        "it": "Interpretazione oftalmologica AI sperimentale che collega retina, OCT, glaucoma e fondo oculare al rischio visivo e alla sicurezza clinica.",
    }

    return {
        "patient_id": req.patient_id,
        "mode": mode,
        "selected_module": mode,
        "language": req.language,
        "image_type": req.image_type,
        **risk,
        "ai_interpretation": interpretations.get(req.language or "en", interpretations["en"]),
        "recommended_next_step": risk["urgency"],
        "clinical_status": "demo_not_certified",
        "required_before_real_clinical_use": [
            "real_fundus_images",
            "real_oct_data",
            "ophthalmology_device_integration",
            "ophthalmologist_validation",
            "audit_logs",
            "cybersecurity_review",
            "regulatory_evidence"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def make_pdf(lines: List[str]) -> bytes:
    stream = "BT /F1 11 Tf 50 800 Td 14 TL "
    first = True

    for line in lines:
        clean = line.encode("latin-1", errors="ignore").decode("latin-1")
        clean = pdf_escape(clean)
        if first:
            stream += f"({clean}) Tj "
            first = False
        else:
            stream += f"T* ({clean}) Tj "

    stream += "ET"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj",
        f"4 0 obj << /Length {len(stream.encode('latin-1'))} >> stream\n{stream}\nendstream endobj",
        "5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
    ]

    pdf = "%PDF-1.4\n"
    offsets = [0]

    for obj in objects:
        offsets.append(len(pdf.encode("latin-1")))
        pdf += obj + "\n"

    xref_pos = len(pdf.encode("latin-1"))
    pdf += f"xref\n0 {len(objects)+1}\n"
    pdf += "0000000000 65535 f \n"

    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"

    pdf += f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\n"
    pdf += f"startxref\n{xref_pos}\n%%EOF"

    return pdf.encode("latin-1")

@router.get("/report-pdf")
async def ophthalmology_report_pdf():
    lines = [
        "AHOS Ophthalmology AI Eye Center Report",
        "Status: Demo operational",
        "Module: Retina / OCT / Glaucoma / Fundus / Emergency Eye Pathway",
        "AI Risk Engine: Enabled",
        "Safety Gate: ACTIVE",
        "PDF Export: Enabled",
        "",
        "Clinical Interpretation:",
        "This report is generated by the AHOS experimental ophthalmology module.",
        "It supports eye screening workflow, but it cannot replace a licensed ophthalmologist.",
        "",
        "Required before real clinical use:",
        "1. Real fundus images",
        "2. Real OCT data",
        "3. Ophthalmology device integration",
        "4. Ophthalmologist validation",
        "5. Audit logs and safety monitoring",
        "6. Regulatory evidence",
        "",
        "Safety Notice:",
        "Prototype only. Not a certified diagnosis.",
        "Physician review is required before any real clinical decision.",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    return Response(
        content=make_pdf(lines),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=AHOS_Ophthalmology_Report.pdf"}
    )

@router.get("/report-demo")
async def ophthalmology_report_demo(language: str = "ar"):
    return {
        "status": "generated",
        "pdf_endpoint": "/api/ophthalmology/report-pdf",
        "text": "AHOS Ophthalmology demo report is ready.",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 3
# Upload Simulation + Case Registry + Report History
# ============================

from fastapi import UploadFile, File, Form
from pathlib import Path as _Path
import shutil
import uuid

OPHTHALMOLOGY_UPLOAD_DIR = _Path("uploads/ophthalmology")
OPHTHALMOLOGY_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

OPHTHALMOLOGY_CASES = []
OPHTHALMOLOGY_REPORT_HISTORY = []

@router.post("/upload-demo")
async def upload_eye_image_demo(
    file: UploadFile = File(...),
    patient_id: str = Form("DEMO-EYE-UPLOAD-001"),
    image_type: str = Form("fundus"),
    language: str = Form("ar")
):
    case_id = "EYE-CASE-" + uuid.uuid4().hex[:10].upper()
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    saved_path = OPHTHALMOLOGY_UPLOAD_DIR / f"{case_id}_{safe_name}"

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    simulated_findings = {
        "fundus": "Fundus image received. Demo screening suggests vascular and optic disc review.",
        "oct": "OCT file received. Demo layer analysis suggests macular and retinal layer review.",
        "retina": "Retina image received. Demo retinal screening workflow completed.",
        "glaucoma": "Glaucoma-related file received. Demo optic nerve and IOP risk review required."
    }

    risk_score = 72 if image_type.lower() in ["glaucoma", "oct"] else 48
    risk_level = "HIGH" if risk_score >= 70 else "MODERATE"

    case = {
        "case_id": case_id,
        "patient_id": patient_id,
        "filename": safe_name,
        "stored_path": str(saved_path),
        "image_type": image_type,
        "language": language,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "status": "demo_uploaded",
        "ai_summary": simulated_findings.get(image_type.lower(), simulated_findings["fundus"]),
        "clinical_notice": "Prototype upload simulation only. Not a certified diagnosis.",
        "timestamp": datetime.utcnow().isoformat()
    }

    OPHTHALMOLOGY_CASES.append(case)
    OPHTHALMOLOGY_REPORT_HISTORY.append({
        "report_id": "EYE-REPORT-" + uuid.uuid4().hex[:8].upper(),
        "case_id": case_id,
        "patient_id": patient_id,
        "report_type": "upload_demo_screening",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "timestamp": datetime.utcnow().isoformat()
    })

    return case

@router.get("/cases")
async def list_ophthalmology_cases():
    return {
        "status": "online",
        "total_cases": len(OPHTHALMOLOGY_CASES),
        "cases": OPHTHALMOLOGY_CASES[-20:]
    }

@router.get("/reports/history")
async def ophthalmology_report_history():
    return {
        "status": "online",
        "total_reports": len(OPHTHALMOLOGY_REPORT_HISTORY),
        "reports": OPHTHALMOLOGY_REPORT_HISTORY[-20:]
    }

@router.get("/phase-3/status")
async def ophthalmology_phase_3_status():
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 3",
        "features": [
            "fundus_oct_upload_simulation",
            "case_registry",
            "report_history",
            "demo_image_workflow",
            "investor_ready_module_evidence"
        ],
        "upload_dir": str(OPHTHALMOLOGY_UPLOAD_DIR),
        "total_cases": len(OPHTHALMOLOGY_CASES),
        "total_reports": len(OPHTHALMOLOGY_REPORT_HISTORY),
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 4
# Case Details + Doctor Review + Case Report
# ============================

@router.get("/cases/{case_id}")
async def get_ophthalmology_case(case_id: str):
    found = None
    for c in OPHTHALMOLOGY_CASES:
        if c.get("case_id") == case_id:
            found = c
            break

    if not found:
        return {
            "status": "not_found",
            "case_id": case_id,
            "message": "Case not found in demo memory registry."
        }

    timeline = [
        {
            "step": "upload_received",
            "label": "Image uploaded to AHOS Ophthalmology Phase 3",
            "timestamp": found.get("timestamp")
        },
        {
            "step": "demo_ai_screening",
            "label": "Demo AI screening completed",
            "risk_score": found.get("risk_score"),
            "risk_level": found.get("risk_level"),
            "timestamp": found.get("timestamp")
        },
        {
            "step": "doctor_review_required",
            "label": "Ophthalmologist review required before clinical use",
            "status": "pending"
        }
    ]

    return {
        "status": "online",
        "case": found,
        "doctor_review": {
            "required": True,
            "status": "pending",
            "reviewer": None,
            "clinical_notice": "Prototype only. No real clinical decision should be made."
        },
        "timeline": timeline
    }

@router.post("/cases/{case_id}/doctor-review-demo")
async def doctor_review_demo(case_id: str):
    found = None
    for c in OPHTHALMOLOGY_CASES:
        if c.get("case_id") == case_id:
            found = c
            break

    if not found:
        return {
            "status": "not_found",
            "case_id": case_id
        }

    review = {
        "case_id": case_id,
        "review_status": "demo_review_completed",
        "reviewer": "DEMO_OPHTHALMOLOGIST",
        "decision": "Needs real ophthalmologist validation before clinical use.",
        "timestamp": datetime.utcnow().isoformat()
    }

    found["doctor_review_status"] = review["review_status"]
    found["doctor_review_decision"] = review["decision"]

    OPHTHALMOLOGY_REPORT_HISTORY.append({
        "report_id": "EYE-REVIEW-" + uuid.uuid4().hex[:8].upper(),
        "case_id": case_id,
        "patient_id": found.get("patient_id"),
        "report_type": "doctor_review_demo",
        "risk_score": found.get("risk_score"),
        "risk_level": found.get("risk_level"),
        "timestamp": datetime.utcnow().isoformat()
    })

    return {
        "status": "review_saved",
        "review": review,
        "case": found
    }

@router.get("/cases/{case_id}/report-text")
async def ophthalmology_case_report_text(case_id: str):
    found = None
    for c in OPHTHALMOLOGY_CASES:
        if c.get("case_id") == case_id:
            found = c
            break

    if not found:
        return {
            "status": "not_found",
            "case_id": case_id
        }

    return {
        "status": "generated",
        "case_id": case_id,
        "report": {
            "title": "AHOS Ophthalmology Case Report",
            "patient_id": found.get("patient_id"),
            "image_type": found.get("image_type"),
            "risk_score": found.get("risk_score"),
            "risk_level": found.get("risk_level"),
            "ai_summary": found.get("ai_summary"),
            "doctor_review_status": found.get("doctor_review_status", "pending"),
            "clinical_notice": "Prototype only. Not a certified diagnosis."
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-4/status")
async def ophthalmology_phase_4_status():
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 4",
        "features": [
            "case_details",
            "case_timeline",
            "doctor_review_demo",
            "case_report_text",
            "review_status_tracking"
        ],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 5
# Case PDF Export
# ============================

def _pdf_escape_phase5(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def _make_case_pdf_phase5(lines):
    stream = "BT /F1 11 Tf 50 800 Td 14 TL "
    first = True

    for line in lines:
        clean = str(line).encode("latin-1", errors="ignore").decode("latin-1")
        clean = _pdf_escape_phase5(clean)
        if first:
            stream += f"({clean}) Tj "
            first = False
        else:
            stream += f"T* ({clean}) Tj "

    stream += "ET"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj",
        f"4 0 obj << /Length {len(stream.encode('latin-1', errors='ignore'))} >> stream\n{stream}\nendstream endobj",
        "5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
    ]

    pdf = "%PDF-1.4\n"
    offsets = [0]

    for obj in objects:
        offsets.append(len(pdf.encode("latin-1", errors="ignore")))
        pdf += obj + "\n"

    xref_pos = len(pdf.encode("latin-1", errors="ignore"))
    pdf += f"xref\n0 {len(objects)+1}\n"
    pdf += "0000000000 65535 f \n"

    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"

    pdf += f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\n"
    pdf += f"startxref\n{xref_pos}\n%%EOF"

    return pdf.encode("latin-1", errors="ignore")

@router.get("/cases/{case_id}/report-pdf")
async def ophthalmology_case_report_pdf(case_id: str):
    found = None
    for c in OPHTHALMOLOGY_CASES:
        if c.get("case_id") == case_id:
            found = c
            break

    if not found:
        return {
            "status": "not_found",
            "case_id": case_id,
            "message": "Case not found in demo memory registry."
        }

    lines = [
        "AHOS Ophthalmology Case PDF Report",
        "Phase: AHOS Ophthalmology Phase 5",
        "",
        f"Case ID: {found.get('case_id')}",
        f"Patient ID: {found.get('patient_id')}",
        f"Image Type: {found.get('image_type')}",
        f"File Name: {found.get('filename')}",
        f"Risk Score: {found.get('risk_score')}/100",
        f"Risk Level: {found.get('risk_level')}",
        f"Case Status: {found.get('status')}",
        f"Doctor Review Status: {found.get('doctor_review_status', 'pending')}",
        "",
        "AI Summary:",
        found.get("ai_summary", "No AI summary available."),
        "",
        "Doctor Review Decision:",
        found.get("doctor_review_decision", "Pending ophthalmologist review."),
        "",
        "Clinical Safety Notice:",
        "Prototype only. Not a certified diagnosis.",
        "A licensed ophthalmologist review is required before real clinical use.",
        "",
        "Required before real clinical use:",
        "1. Real Fundus/OCT data",
        "2. Ophthalmology device integration",
        "3. Ophthalmologist validation",
        "4. Audit logs and cybersecurity review",
        "5. Regulatory evidence",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _make_case_pdf_phase5(lines)

    OPHTHALMOLOGY_REPORT_HISTORY.append({
        "report_id": "EYE-CASE-PDF-" + uuid.uuid4().hex[:8].upper(),
        "case_id": case_id,
        "patient_id": found.get("patient_id"),
        "report_type": "case_pdf_export",
        "risk_score": found.get("risk_score"),
        "risk_level": found.get("risk_level"),
        "timestamp": datetime.utcnow().isoformat()
    })

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Ophthalmology_Case_{case_id}.pdf"
        }
    )

@router.get("/phase-5/status")
async def ophthalmology_phase_5_status():
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 5",
        "features": [
            "case_pdf_export",
            "doctor_review_pdf_report",
            "case_report_download",
            "phase_5_investor_demo_ready"
        ],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 6
# Professional Multilingual PDF Report
# ============================

def _phase6_text(lang: str):
    lang = (lang or "en").lower()

    data = {
        "ar": {
            "title": "AHOS Ophthalmology Professional Case Report",
            "phase": "Phase 6 - Professional Multilingual PDF",
            "case_data": "Case Data",
            "doctor_review": "Doctor Review",
            "ai_summary": "AI Summary",
            "clinical_safety": "Clinical Safety Notice",
            "required": "Required Before Real Clinical Use",
            "prototype": "Prototype only. Not a certified medical diagnosis.",
            "doctor_required": "Licensed ophthalmologist review is required before real clinical use.",
            "pending": "Pending ophthalmologist review.",
            "generated": "Generated at",
            "risk_score": "Risk Score",
            "risk_level": "Risk Level",
            "case_id": "Case ID",
            "patient_id": "Patient ID",
            "image_type": "Image Type",
            "file_name": "File Name",
            "case_status": "Case Status",
            "doctor_status": "Doctor Review Status"
        },
        "en": {
            "title": "AHOS Ophthalmology Professional Case Report",
            "phase": "Phase 6 - Professional Multilingual PDF",
            "case_data": "Case Data",
            "doctor_review": "Doctor Review",
            "ai_summary": "AI Summary",
            "clinical_safety": "Clinical Safety Notice",
            "required": "Required Before Real Clinical Use",
            "prototype": "Prototype only. Not a certified medical diagnosis.",
            "doctor_required": "Licensed ophthalmologist review is required before real clinical use.",
            "pending": "Pending ophthalmologist review.",
            "generated": "Generated at",
            "risk_score": "Risk Score",
            "risk_level": "Risk Level",
            "case_id": "Case ID",
            "patient_id": "Patient ID",
            "image_type": "Image Type",
            "file_name": "File Name",
            "case_status": "Case Status",
            "doctor_status": "Doctor Review Status"
        },
        "sv": {
            "title": "AHOS Oftalmologi Professionell Fallrapport",
            "phase": "Fas 6 - Professionell flerspråkig PDF",
            "case_data": "Falldata",
            "doctor_review": "Läkargranskning",
            "ai_summary": "AI-sammanfattning",
            "clinical_safety": "Klinisk säkerhetsnotis",
            "required": "Krävs före verklig klinisk användning",
            "prototype": "Endast prototyp. Inte en certifierad medicinsk diagnos.",
            "doctor_required": "Granskning av legitimerad ögonläkare krävs före klinisk användning.",
            "pending": "Väntar på ögonläkargranskning.",
            "generated": "Genererad",
            "risk_score": "Riskpoäng",
            "risk_level": "Risknivå",
            "case_id": "Fall-ID",
            "patient_id": "Patient-ID",
            "image_type": "Bildtyp",
            "file_name": "Filnamn",
            "case_status": "Fallstatus",
            "doctor_status": "Läkargranskningsstatus"
        },
        "fr": {
            "title": "Rapport professionnel de cas ophtalmologique AHOS",
            "phase": "Phase 6 - PDF professionnel multilingue",
            "case_data": "Données du cas",
            "doctor_review": "Revue médicale",
            "ai_summary": "Résumé IA",
            "clinical_safety": "Avis de sécurité clinique",
            "required": "Requis avant utilisation clinique réelle",
            "prototype": "Prototype uniquement. Ce n'est pas un diagnostic médical certifié.",
            "doctor_required": "Une revue par un ophtalmologiste agréé est requise avant utilisation clinique.",
            "pending": "Revue ophtalmologiste en attente.",
            "generated": "Généré le",
            "risk_score": "Score de risque",
            "risk_level": "Niveau de risque",
            "case_id": "ID du cas",
            "patient_id": "ID patient",
            "image_type": "Type d’image",
            "file_name": "Nom du fichier",
            "case_status": "Statut du cas",
            "doctor_status": "Statut revue médicale"
        },
        "it": {
            "title": "Report professionale caso oftalmologico AHOS",
            "phase": "Fase 6 - PDF professionale multilingue",
            "case_data": "Dati caso",
            "doctor_review": "Revisione medica",
            "ai_summary": "Riassunto AI",
            "clinical_safety": "Avviso sicurezza clinica",
            "required": "Richiesto prima dell'uso clinico reale",
            "prototype": "Solo prototipo. Non è una diagnosi medica certificata.",
            "doctor_required": "È richiesta revisione di un oftalmologo autorizzato prima dell'uso clinico.",
            "pending": "Revisione oftalmologo in attesa.",
            "generated": "Generato il",
            "risk_score": "Punteggio rischio",
            "risk_level": "Livello rischio",
            "case_id": "ID caso",
            "patient_id": "ID paziente",
            "image_type": "Tipo immagine",
            "file_name": "Nome file",
            "case_status": "Stato caso",
            "doctor_status": "Stato revisione medica"
        }
    }

    return data.get(lang, data["en"])

def _phase6_escape_pdf(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def _phase6_make_pdf(lines):
    # Simple internal PDF generator, no external dependencies.
    # Latin-1 safe; Arabic text may be simplified/omitted by base PDF fonts, so labels are English-safe.
    stream = "BT /F1 10 Tf 48 805 Td 13 TL "

    first = True
    for line in lines:
        clean = str(line).encode("latin-1", errors="ignore").decode("latin-1")
        clean = _phase6_escape_pdf(clean)
        if first:
            stream += f"({clean}) Tj "
            first = False
        else:
            stream += f"T* ({clean}) Tj "

    stream += "ET"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj",
        f"4 0 obj << /Length {len(stream.encode('latin-1', errors='ignore'))} >> stream\n{stream}\nendstream endobj",
        "5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
    ]

    pdf = "%PDF-1.4\n"
    offsets = [0]

    for obj in objects:
        offsets.append(len(pdf.encode("latin-1", errors="ignore")))
        pdf += obj + "\n"

    xref_pos = len(pdf.encode("latin-1", errors="ignore"))
    pdf += f"xref\n0 {len(objects)+1}\n"
    pdf += "0000000000 65535 f \n"

    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"

    pdf += f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\n"
    pdf += f"startxref\n{xref_pos}\n%%EOF"

    return pdf.encode("latin-1", errors="ignore")

@router.get("/cases/{case_id}/professional-report-pdf")
async def ophthalmology_professional_case_report_pdf(case_id: str, language: str = "en"):
    found = None
    for c in OPHTHALMOLOGY_CASES:
        if c.get("case_id") == case_id:
            found = c
            break

    if not found:
        return {
            "status": "not_found",
            "case_id": case_id,
            "message": "Case not found in demo memory registry."
        }

    tr = _phase6_text(language)

    lines = [
        "AHOS - AI Hospital Alliance",
        tr["title"],
        tr["phase"],
        "------------------------------------------------------------",
        "",
        tr["case_data"],
        f"{tr['case_id']}: {found.get('case_id')}",
        f"{tr['patient_id']}: {found.get('patient_id')}",
        f"{tr['image_type']}: {found.get('image_type')}",
        f"{tr['file_name']}: {found.get('filename')}",
        f"{tr['risk_score']}: {found.get('risk_score')}/100",
        f"{tr['risk_level']}: {found.get('risk_level')}",
        f"{tr['case_status']}: {found.get('status')}",
        f"{tr['doctor_status']}: {found.get('doctor_review_status', 'pending')}",
        "",
        "------------------------------------------------------------",
        tr["ai_summary"],
        found.get("ai_summary", "No AI summary available."),
        "",
        "------------------------------------------------------------",
        tr["doctor_review"],
        found.get("doctor_review_decision", tr["pending"]),
        "",
        "------------------------------------------------------------",
        tr["clinical_safety"],
        tr["prototype"],
        tr["doctor_required"],
        "",
        "------------------------------------------------------------",
        tr["required"],
        "1. Real Fundus/OCT data",
        "2. Ophthalmology device integration",
        "3. Ophthalmologist validation",
        "4. Audit logs and cybersecurity review",
        "5. Regulatory evidence",
        "6. Real hospital pilot workflow",
        "",
        "------------------------------------------------------------",
        "Investor Demo Readiness: READY",
        "Clinical Production Readiness: NOT CERTIFIED",
        "Regulatory Status: EVIDENCE REQUIRED",
        "",
        f"{tr['generated']}: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase6_make_pdf(lines)

    OPHTHALMOLOGY_REPORT_HISTORY.append({
        "report_id": "EYE-PRO-PDF-" + uuid.uuid4().hex[:8].upper(),
        "case_id": case_id,
        "patient_id": found.get("patient_id"),
        "report_type": f"phase6_professional_pdf_{language}",
        "risk_score": found.get("risk_score"),
        "risk_level": found.get("risk_level"),
        "timestamp": datetime.utcnow().isoformat()
    })

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Professional_Ophthalmology_Case_{case_id}_{language}.pdf"
        }
    )

@router.get("/phase-6/status")
async def ophthalmology_phase_6_status():
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 6",
        "features": [
            "professional_case_pdf",
            "multilingual_pdf_endpoint",
            "investor_demo_report",
            "clinical_safety_section",
            "doctor_review_section",
            "regulatory_readiness_notes"
        ],
        "languages": ["ar", "en", "sv", "fr", "it"],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 8
# Persistent SQLite Case Storage
# ============================

import sqlite3
from fastapi import UploadFile, File, Form, Query
from pathlib import Path as _Phase8Path
import shutil as _phase8_shutil
import uuid as _phase8_uuid

PHASE8_DB_PATH = _Phase8Path("data/ahos_ophthalmology_cases.db")
PHASE8_UPLOAD_DIR = _Phase8Path("uploads/ophthalmology")
PHASE8_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
PHASE8_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def _phase8_conn():
    conn = sqlite3.connect(PHASE8_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def _phase8_init_db():
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_cases (
        case_id TEXT PRIMARY KEY,
        patient_id TEXT,
        filename TEXT,
        stored_path TEXT,
        image_type TEXT,
        language TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        status TEXT,
        ai_summary TEXT,
        clinical_notice TEXT,
        doctor_review_status TEXT,
        doctor_review_decision TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_reports (
        report_id TEXT PRIMARY KEY,
        case_id TEXT,
        patient_id TEXT,
        report_type TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        language TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_audit_logs (
        audit_id TEXT PRIMARY KEY,
        case_id TEXT,
        action TEXT,
        details TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase8_log(case_id: str, action: str, details: str = ""):
    _phase8_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO ophthalmology_audit_logs (audit_id, case_id, action, details, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        "EYE-AUDIT-" + _phase8_uuid.uuid4().hex[:10].upper(),
        case_id,
        action,
        details,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def _phase8_case_to_dict(row):
    return dict(row) if row else None

def _phase8_find_case(case_id: str):
    _phase8_init_db()
    conn = _phase8_conn()
    row = conn.execute("SELECT * FROM ophthalmology_cases WHERE case_id = ?", (case_id,)).fetchone()
    conn.close()
    return _phase8_case_to_dict(row)

def _phase8_escape_pdf(text: str) -> str:
    return str(text).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def _phase8_make_pdf(lines):
    stream = "BT /F1 10 Tf 48 805 Td 13 TL "
    first = True

    for line in lines:
        clean = str(line).encode("latin-1", errors="ignore").decode("latin-1")
        clean = _phase8_escape_pdf(clean)
        if first:
            stream += f"({clean}) Tj "
            first = False
        else:
            stream += f"T* ({clean}) Tj "

    stream += "ET"

    objects = [
        "1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        "2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        "3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj",
        f"4 0 obj << /Length {len(stream.encode('latin-1', errors='ignore'))} >> stream\n{stream}\nendstream endobj",
        "5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
    ]

    pdf = "%PDF-1.4\n"
    offsets = [0]

    for obj in objects:
        offsets.append(len(pdf.encode("latin-1", errors="ignore")))
        pdf += obj + "\n"

    xref_pos = len(pdf.encode("latin-1", errors="ignore"))
    pdf += f"xref\n0 {len(objects)+1}\n"
    pdf += "0000000000 65535 f \n"

    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"

    pdf += f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\n"
    pdf += f"startxref\n{xref_pos}\n%%EOF"

    return pdf.encode("latin-1", errors="ignore")

@router.get("/phase-8/status")
async def ophthalmology_phase_8_status():
    _phase8_init_db()
    conn = _phase8_conn()
    cases_count = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    reports_count = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    audit_count = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 8",
        "features": [
            "persistent_sqlite_case_storage",
            "persistent_report_history",
            "doctor_review_persistence",
            "audit_log_table",
            "case_search",
            "persistent_case_pdf_export"
        ],
        "database": str(PHASE8_DB_PATH),
        "upload_dir": str(PHASE8_UPLOAD_DIR),
        "total_cases": cases_count,
        "total_reports": reports_count,
        "total_audit_logs": audit_count,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/phase-8/upload-demo")
async def phase8_upload_eye_image_demo(
    file: UploadFile = File(...),
    patient_id: str = Form("AHOS-EYE-PHASE8-DEMO-001"),
    image_type: str = Form("fundus"),
    language: str = Form("ar")
):
    _phase8_init_db()

    case_id = "EYE-P8-" + _phase8_uuid.uuid4().hex[:10].upper()
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    saved_path = PHASE8_UPLOAD_DIR / f"{case_id}_{safe_name}"

    with saved_path.open("wb") as buffer:
        _phase8_shutil.copyfileobj(file.file, buffer)

    simulated_findings = {
        "fundus": "Fundus image received. Demo screening suggests vascular and optic disc review.",
        "oct": "OCT file received. Demo layer analysis suggests macular and retinal layer review.",
        "retina": "Retina image received. Demo retinal screening workflow completed.",
        "glaucoma": "Glaucoma-related file received. Demo optic nerve and IOP risk review required."
    }

    risk_score = 72 if image_type.lower() in ["glaucoma", "oct"] else 48
    risk_level = "HIGH" if risk_score >= 70 else "MODERATE"
    now = datetime.utcnow().isoformat()

    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ophthalmology_cases (
        case_id, patient_id, filename, stored_path, image_type, language,
        risk_score, risk_level, status, ai_summary, clinical_notice,
        doctor_review_status, doctor_review_decision, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        patient_id,
        safe_name,
        str(saved_path),
        image_type,
        language,
        risk_score,
        risk_level,
        "persistent_demo_uploaded",
        simulated_findings.get(image_type.lower(), simulated_findings["fundus"]),
        "Prototype upload simulation only. Not a certified diagnosis.",
        "pending",
        "Pending ophthalmologist review.",
        now,
        now
    ))

    report_id = "EYE-P8-REPORT-" + _phase8_uuid.uuid4().hex[:8].upper()
    cur.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        case_id,
        patient_id,
        "phase8_persistent_upload_report",
        risk_score,
        risk_level,
        language,
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(case_id, "upload_demo_persistent", f"Uploaded {safe_name}")

    return _phase8_find_case(case_id)

@router.get("/phase-8/cases")
async def phase8_list_cases(q: str = Query("", description="Search by case_id, patient_id, image_type, risk_level")):
    _phase8_init_db()
    conn = _phase8_conn()

    if q:
        like = f"%{q}%"
        rows = conn.execute("""
        SELECT * FROM ophthalmology_cases
        WHERE case_id LIKE ? OR patient_id LIKE ? OR image_type LIKE ? OR risk_level LIKE ?
        ORDER BY created_at DESC
        LIMIT 100
        """, (like, like, like, like)).fetchall()
    else:
        rows = conn.execute("""
        SELECT * FROM ophthalmology_cases
        ORDER BY created_at DESC
        LIMIT 100
        """).fetchall()

    conn.close()

    return {
        "status": "online",
        "persistent": True,
        "total_cases": len(rows),
        "cases": [dict(r) for r in rows]
    }

@router.get("/phase-8/cases/{case_id}")
async def phase8_get_case(case_id: str):
    case = _phase8_find_case(case_id)

    if not case:
        return {
            "status": "not_found",
            "case_id": case_id
        }

    conn = _phase8_conn()
    reports = conn.execute("""
    SELECT * FROM ophthalmology_reports
    WHERE case_id = ?
    ORDER BY created_at DESC
    """, (case_id,)).fetchall()

    audits = conn.execute("""
    SELECT * FROM ophthalmology_audit_logs
    WHERE case_id = ?
    ORDER BY created_at DESC
    """, (case_id,)).fetchall()

    conn.close()

    timeline = [
        {
            "step": "persistent_case_created",
            "label": "Case saved into SQLite persistent database",
            "timestamp": case.get("created_at")
        },
        {
            "step": "demo_ai_screening",
            "label": "Demo AI screening completed",
            "risk_score": case.get("risk_score"),
            "risk_level": case.get("risk_level"),
            "timestamp": case.get("created_at")
        },
        {
            "step": "doctor_review_status",
            "label": case.get("doctor_review_status", "pending"),
            "timestamp": case.get("updated_at")
        }
    ]

    return {
        "status": "online",
        "persistent": True,
        "case": case,
        "timeline": timeline,
        "reports": [dict(r) for r in reports],
        "audit_logs": [dict(a) for a in audits]
    }

@router.post("/phase-8/cases/{case_id}/doctor-review-demo")
async def phase8_doctor_review_demo(case_id: str):
    case = _phase8_find_case(case_id)

    if not case:
        return {
            "status": "not_found",
            "case_id": case_id
        }

    now = datetime.utcnow().isoformat()
    decision = "Needs real ophthalmologist validation before clinical use."

    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    UPDATE ophthalmology_cases
    SET doctor_review_status = ?, doctor_review_decision = ?, updated_at = ?
    WHERE case_id = ?
    """, (
        "demo_review_completed",
        decision,
        now,
        case_id
    ))

    report_id = "EYE-P8-REVIEW-" + _phase8_uuid.uuid4().hex[:8].upper()
    cur.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        case_id,
        case.get("patient_id"),
        "phase8_doctor_review_demo",
        case.get("risk_score"),
        case.get("risk_level"),
        case.get("language"),
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(case_id, "doctor_review_demo", decision)

    return {
        "status": "review_saved",
        "persistent": True,
        "case_id": case_id,
        "review_status": "demo_review_completed",
        "decision": decision,
        "timestamp": now
    }

@router.get("/phase-8/reports/history")
async def phase8_report_history():
    _phase8_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT * FROM ophthalmology_reports
    ORDER BY created_at DESC
    LIMIT 100
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "persistent": True,
        "total_reports": len(rows),
        "reports": [dict(r) for r in rows]
    }

@router.get("/phase-8/audit-logs")
async def phase8_audit_logs():
    _phase8_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT * FROM ophthalmology_audit_logs
    ORDER BY created_at DESC
    LIMIT 100
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "persistent": True,
        "total_logs": len(rows),
        "audit_logs": [dict(r) for r in rows]
    }

@router.get("/phase-8/cases/{case_id}/report-pdf")
async def phase8_case_report_pdf(case_id: str):
    case = _phase8_find_case(case_id)

    if not case:
        return {
            "status": "not_found",
            "case_id": case_id
        }

    lines = [
        "AHOS Ophthalmology Persistent Case Report",
        "Phase: AHOS Ophthalmology Phase 8",
        "Storage: SQLite Persistent Database",
        "",
        f"Case ID: {case.get('case_id')}",
        f"Patient ID: {case.get('patient_id')}",
        f"Image Type: {case.get('image_type')}",
        f"File Name: {case.get('filename')}",
        f"Risk Score: {case.get('risk_score')}/100",
        f"Risk Level: {case.get('risk_level')}",
        f"Case Status: {case.get('status')}",
        f"Doctor Review Status: {case.get('doctor_review_status')}",
        "",
        "AI Summary:",
        case.get("ai_summary"),
        "",
        "Doctor Review Decision:",
        case.get("doctor_review_decision"),
        "",
        "Clinical Safety Notice:",
        "Prototype only. Not a certified diagnosis.",
        "A licensed ophthalmologist review is required before real clinical use.",
        "",
        "Persistence:",
        f"Database: {PHASE8_DB_PATH}",
        f"Created at: {case.get('created_at')}",
        f"Updated at: {case.get('updated_at')}",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    now = datetime.utcnow().isoformat()
    conn = _phase8_conn()
    conn.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "EYE-P8-PDF-" + _phase8_uuid.uuid4().hex[:8].upper(),
        case_id,
        case.get("patient_id"),
        "phase8_persistent_case_pdf",
        case.get("risk_score"),
        case.get("risk_level"),
        case.get("language"),
        now
    ))
    conn.commit()
    conn.close()

    _phase8_log(case_id, "phase8_pdf_export", "Persistent case PDF exported")

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase8_Persistent_Case_{case_id}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 9
# Advanced Search + Filters + Dashboard Charts
# ============================

@router.get("/phase-9/status")
async def ophthalmology_phase_9_status():
    _phase8_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]
    high_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE risk_level = 'HIGH'").fetchone()["c"]
    moderate_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE risk_level = 'MODERATE'").fetchone()["c"]
    reviewed_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE doctor_review_status = 'demo_review_completed'").fetchone()["c"]
    pending_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE doctor_review_status = 'pending'").fetchone()["c"]

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 9",
        "features": [
            "advanced_case_search",
            "risk_level_filter",
            "image_type_filter",
            "doctor_review_filter",
            "risk_distribution_chart",
            "image_type_distribution_chart",
            "doctor_review_chart",
            "dashboard_summary"
        ],
        "total_cases": total_cases,
        "total_reports": total_reports,
        "total_audit_logs": total_audits,
        "high_cases": high_cases,
        "moderate_cases": moderate_cases,
        "reviewed_cases": reviewed_cases,
        "pending_cases": pending_cases,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-9/search")
async def phase9_advanced_search(
    q: str = Query("", description="Search text"),
    image_type: str = Query("", description="fundus, oct, retina, glaucoma"),
    risk_level: str = Query("", description="LOW, MODERATE, HIGH"),
    doctor_review_status: str = Query("", description="pending, demo_review_completed"),
    min_risk: int = Query(0),
    max_risk: int = Query(100),
    limit: int = Query(100)
):
    _phase8_init_db()
    conn = _phase8_conn()

    sql = """
    SELECT * FROM ophthalmology_cases
    WHERE risk_score >= ? AND risk_score <= ?
    """
    params = [min_risk, max_risk]

    if q:
        sql += """
        AND (
            case_id LIKE ? OR
            patient_id LIKE ? OR
            filename LIKE ? OR
            image_type LIKE ? OR
            risk_level LIKE ? OR
            doctor_review_status LIKE ?
        )
        """
        like = f"%{q}%"
        params.extend([like, like, like, like, like, like])

    if image_type:
        sql += " AND LOWER(image_type) = LOWER(?) "
        params.append(image_type)

    if risk_level:
        sql += " AND UPPER(risk_level) = UPPER(?) "
        params.append(risk_level)

    if doctor_review_status:
        sql += " AND doctor_review_status = ? "
        params.append(doctor_review_status)

    sql += " ORDER BY created_at DESC LIMIT ? "
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return {
        "status": "online",
        "persistent": True,
        "filters": {
            "q": q,
            "image_type": image_type,
            "risk_level": risk_level,
            "doctor_review_status": doctor_review_status,
            "min_risk": min_risk,
            "max_risk": max_risk,
            "limit": limit
        },
        "total_results": len(rows),
        "cases": [dict(r) for r in rows]
    }

@router.get("/phase-9/analytics")
async def phase9_analytics():
    _phase8_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]

    risk_rows = conn.execute("""
    SELECT risk_level AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY risk_level
    ORDER BY value DESC
    """).fetchall()

    type_rows = conn.execute("""
    SELECT image_type AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY image_type
    ORDER BY value DESC
    """).fetchall()

    review_rows = conn.execute("""
    SELECT doctor_review_status AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY doctor_review_status
    ORDER BY value DESC
    """).fetchall()

    recent_rows = conn.execute("""
    SELECT case_id, patient_id, image_type, risk_score, risk_level, doctor_review_status, created_at
    FROM ophthalmology_cases
    ORDER BY created_at DESC
    LIMIT 30
    """).fetchall()

    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    max_risk = conn.execute("SELECT MAX(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 9 Analytics",
        "summary": {
            "total_cases": total_cases,
            "total_reports": total_reports,
            "total_audit_logs": total_audits,
            "average_risk_score": round(avg_risk, 2),
            "max_risk_score": max_risk
        },
        "risk_distribution": [dict(r) for r in risk_rows],
        "image_type_distribution": [dict(r) for r in type_rows],
        "doctor_review_distribution": [dict(r) for r in review_rows],
        "recent_risk_scores": [dict(r) for r in recent_rows],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-9/dashboard-summary")
async def phase9_dashboard_summary():
    _phase8_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    max_risk = conn.execute("SELECT MAX(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    reviewed = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE doctor_review_status='demo_review_completed'").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases WHERE doctor_review_status='pending'").fetchone()["c"]

    conn.close()

    return {
        "status": "online",
        "total_cases": total_cases,
        "average_risk_score": round(avg_risk, 2),
        "max_risk_score": max_risk,
        "reviewed_cases": reviewed,
        "pending_review_cases": pending,
        "prototype_status": "investor_demo_ready_not_clinical",
        "timestamp": datetime.utcnow().isoformat()
    }


# ============================
# AHOS Ophthalmology Phase 10
# Multilingual Analytics Report Export
# ============================

@router.get("/phase-10/status")
async def ophthalmology_phase_10_status():
    _phase8_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]
    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    max_risk = conn.execute("SELECT MAX(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 10",
        "features": [
            "multilingual_phase_9_dashboard",
            "arabic_english_swedish_french_italian",
            "analytics_report_html",
            "analytics_report_pdf",
            "investor_analytics_summary",
            "clinical_safety_notice"
        ],
        "total_cases": total_cases,
        "total_reports": total_reports,
        "total_audit_logs": total_audits,
        "average_risk_score": round(avg_risk, 2),
        "max_risk_score": max_risk,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

def _phase10_text(language: str):
    lang = (language or "en").lower()
    texts = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 10 - التقرير التحليلي",
            "summary": "تقرير تحليلي لقسم العيون داخل AHOS يعتمد على قاعدة بيانات SQLite الثابتة.",
            "clinical": "تنبيه: هذا النظام نموذج تجريبي وغير معتمد للاستخدام السريري الحقيقي.",
            "investor": "جاهز للعرض الاستثماري كنموذج تخصصي داخل AHOS."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 10 - Analytics Report",
            "summary": "Analytics report for the AHOS Ophthalmology module based on persistent SQLite storage.",
            "clinical": "Notice: this system is a prototype and is not certified for real clinical use.",
            "investor": "Ready for investor demonstration as a specialty module inside AHOS."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 10 - Analysrapport",
            "summary": "Analysrapport för AHOS oftalmologimodul baserad på beständig SQLite-lagring.",
            "clinical": "Obs: systemet är en prototyp och inte certifierat för klinisk användning.",
            "investor": "Redo för investerardemonstration som specialistmodul i AHOS."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 10 - Rapport analytique",
            "summary": "Rapport analytique du module ophtalmologie AHOS basé sur le stockage SQLite persistant.",
            "clinical": "Avis: ce système est un prototype et n’est pas certifié pour un usage clinique réel.",
            "investor": "Prêt pour une démonstration investisseur comme module spécialisé dans AHOS."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 10 - Report analitico",
            "summary": "Report analitico del modulo oftalmologia AHOS basato su archiviazione SQLite persistente.",
            "clinical": "Avviso: questo sistema è un prototipo e non è certificato per uso clinico reale.",
            "investor": "Pronto per dimostrazione agli investitori come modulo specialistico in AHOS."
        }
    }
    return texts.get(lang, texts["en"])

@router.get("/phase-10/analytics-report-html")
async def phase10_analytics_report_html(language: str = "en"):
    _phase8_init_db()
    tx = _phase10_text(language)

    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]
    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    max_risk = conn.execute("SELECT MAX(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0

    risk_rows = conn.execute("""
    SELECT risk_level AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY risk_level
    ORDER BY value DESC
    """).fetchall()

    type_rows = conn.execute("""
    SELECT image_type AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY image_type
    ORDER BY value DESC
    """).fetchall()

    review_rows = conn.execute("""
    SELECT doctor_review_status AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY doctor_review_status
    ORDER BY value DESC
    """).fetchall()

    cases = conn.execute("""
    SELECT case_id, patient_id, image_type, risk_score, risk_level, doctor_review_status, created_at
    FROM ophthalmology_cases
    ORDER BY created_at DESC
    LIMIT 50
    """).fetchall()

    conn.close()

    def rows_html(rows):
        return "".join([f"<tr><td>{r['label']}</td><td>{r['value']}</td></tr>" for r in rows])

    def cases_html(rows):
        return "".join([
            f"<tr><td>{r['case_id']}</td><td>{r['patient_id']}</td><td>{r['image_type']}</td><td>{r['risk_score']}</td><td>{r['risk_level']}</td><td>{r['doctor_review_status']}</td></tr>"
            for r in rows
        ])

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
}}
th {{
  background: #e0f2fe;
}}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Storage:</strong> SQLite persistent case database</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Dashboard Summary</h2>
<div class="grid">
  <div class="metric">Total Cases<strong>{total_cases}</strong></div>
  <div class="metric">Total Reports<strong>{total_reports}</strong></div>
  <div class="metric">Audit Logs<strong>{total_audits}</strong></div>
  <div class="metric">Average Risk<strong>{round(avg_risk, 2)}</strong></div>
  <div class="metric">Max Risk<strong>{max_risk}</strong></div>
  <div class="metric">Clinical Status<strong>Prototype</strong></div>
</div>

<h2>Risk Distribution</h2>
<table>
<tr><th>Risk Level</th><th>Count</th></tr>
{rows_html(risk_rows)}
</table>

<h2>Image Type Distribution</h2>
<table>
<tr><th>Image Type</th><th>Count</th></tr>
{rows_html(type_rows)}
</table>

<h2>Doctor Review Distribution</h2>
<table>
<tr><th>Review Status</th><th>Count</th></tr>
{rows_html(review_rows)}
</table>

<h2>Recent Cases</h2>
<table>
<tr>
<th>Case ID</th>
<th>Patient ID</th>
<th>Image Type</th>
<th>Risk Score</th>
<th>Risk Level</th>
<th>Doctor Review</th>
</tr>
{cases_html(cases)}
</table>

<div class="notice">
<p>{tx['clinical']}</p>
<p>{tx['investor']}</p>
</div>

</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase10_Analytics_Report_{language}.html"
        }
    )

@router.get("/phase-10/analytics-report-pdf")
async def phase10_analytics_report_pdf(language: str = "en"):
    _phase8_init_db()
    tx = _phase10_text(language)

    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]
    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0
    max_risk = conn.execute("SELECT MAX(risk_score) AS v FROM ophthalmology_cases").fetchone()["v"] or 0

    risk_rows = conn.execute("""
    SELECT risk_level AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY risk_level
    ORDER BY value DESC
    """).fetchall()

    type_rows = conn.execute("""
    SELECT image_type AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY image_type
    ORDER BY value DESC
    """).fetchall()

    review_rows = conn.execute("""
    SELECT doctor_review_status AS label, COUNT(*) AS value
    FROM ophthalmology_cases
    GROUP BY doctor_review_status
    ORDER BY value DESC
    """).fetchall()

    conn.close()

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 10",
        "",
        f"Total Cases: {total_cases}",
        f"Total Reports: {total_reports}",
        f"Audit Logs: {total_audits}",
        f"Average Risk Score: {round(avg_risk, 2)}",
        f"Max Risk Score: {max_risk}",
        "",
        "Risk Distribution:",
    ]

    for r in risk_rows:
        lines.append(f"- {r['label']}: {r['value']}")

    lines.append("")
    lines.append("Image Type Distribution:")
    for r in type_rows:
        lines.append(f"- {r['label']}: {r['value']}")

    lines.append("")
    lines.append("Doctor Review Distribution:")
    for r in review_rows:
        lines.append(f"- {r['label']}: {r['value']}")

    lines.append("")
    lines.append(tx["clinical"])
    lines.append(tx["investor"])
    lines.append("")
    lines.append(f"Generated at: {datetime.utcnow().isoformat()} UTC")

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase10_Analytics_Report_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 11
# Real Fundus/OCT Image AI Analysis Pipeline
# ============================

def _phase11_init_db():
    _phase8_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_ai_analyses (
        analysis_id TEXT PRIMARY KEY,
        case_id TEXT,
        patient_id TEXT,
        image_type TEXT,
        filename TEXT,
        width INTEGER,
        height INTEGER,
        mode TEXT,
        quality_score INTEGER,
        brightness REAL,
        contrast REAL,
        sharpness REAL,
        risk_score INTEGER,
        risk_level TEXT,
        findings_json TEXT,
        recommendations_json TEXT,
        safety_gate TEXT,
        clinical_status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase11_json(obj):
    try:
        import json
        return json.dumps(obj, ensure_ascii=False)
    except Exception:
        return str(obj)

def _phase11_analyze_image_basic(path: str, image_type: str):
    """
    Real first-layer image analysis:
    - Opens image if Pillow is available.
    - Computes dimensions, brightness, contrast and simple sharpness proxy.
    - Uses deterministic risk scoring rules.
    - If image cannot be read, returns safe fallback.
    """
    image_type_l = (image_type or "fundus").lower()

    width = 0
    height = 0
    brightness = 0.0
    contrast = 0.0
    sharpness = 0.0
    quality_score = 40
    read_status = "fallback_no_image_decoder"

    try:
        from PIL import Image, ImageStat, ImageFilter

        img = Image.open(path)
        width, height = img.size

        gray = img.convert("L")
        stat = ImageStat.Stat(gray)
        brightness = float(stat.mean[0])
        contrast = float(stat.stddev[0])

        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        sharpness = float(edge_stat.mean[0])

        read_status = "image_decoded"

        dimension_score = 0
        if width >= 600 and height >= 400:
            dimension_score = 30
        elif width >= 300 and height >= 200:
            dimension_score = 20
        else:
            dimension_score = 8

        brightness_score = 0
        if 70 <= brightness <= 190:
            brightness_score = 25
        elif 45 <= brightness <= 220:
            brightness_score = 15
        else:
            brightness_score = 5

        contrast_score = 0
        if contrast >= 45:
            contrast_score = 25
        elif contrast >= 25:
            contrast_score = 15
        else:
            contrast_score = 6

        sharpness_score = 0
        if sharpness >= 18:
            sharpness_score = 20
        elif sharpness >= 9:
            sharpness_score = 12
        else:
            sharpness_score = 5

        quality_score = max(0, min(100, dimension_score + brightness_score + contrast_score + sharpness_score))

    except Exception as e:
        read_status = f"fallback_decoder_error: {str(e)[:120]}"
        width = 0
        height = 0
        brightness = 0.0
        contrast = 0.0
        sharpness = 0.0
        quality_score = 40

    findings = []
    recommendations = []

    if quality_score < 50:
        findings.append({
            "code": "LOW_IMAGE_QUALITY",
            "label": "Low image quality",
            "severity": "MODERATE",
            "description": "Image quality is not sufficient for reliable AI screening."
        })
        recommendations.append("Repeat image acquisition with better focus, illumination and positioning.")

    if brightness and brightness < 55:
        findings.append({
            "code": "UNDEREXPOSED_IMAGE",
            "label": "Underexposed image",
            "severity": "MODERATE",
            "description": "The image appears dark and may hide retinal details."
        })

    if brightness and brightness > 215:
        findings.append({
            "code": "OVEREXPOSED_IMAGE",
            "label": "Overexposed image",
            "severity": "MODERATE",
            "description": "The image appears too bright and may wash out retinal details."
        })

    if contrast and contrast < 25:
        findings.append({
            "code": "LOW_CONTRAST",
            "label": "Low contrast",
            "severity": "MODERATE",
            "description": "Low contrast reduces visibility of vessels and optic disc borders."
        })

    if sharpness and sharpness < 8:
        findings.append({
            "code": "POSSIBLE_BLUR",
            "label": "Possible blur",
            "severity": "MODERATE",
            "description": "The image may be blurred and needs review."
        })

    if image_type_l == "fundus":
        findings.append({
            "code": "FUNDUS_SCREENING_PIPELINE",
            "label": "Fundus screening pipeline",
            "severity": "INFO",
            "description": "Fundus image passed through quality, contrast and optic-disc-oriented screening logic."
        })
        recommendations.append("Review optic disc, macula and vascular pattern by an ophthalmologist.")

    elif image_type_l == "oct":
        findings.append({
            "code": "OCT_SCREENING_PIPELINE",
            "label": "OCT screening pipeline",
            "severity": "INFO",
            "description": "OCT image passed through quality and retinal-layer-oriented screening logic."
        })
        recommendations.append("Review retinal layers, macular contour and segmentation quality.")

    elif image_type_l == "glaucoma":
        findings.append({
            "code": "GLAUCOMA_SCREENING_PIPELINE",
            "label": "Glaucoma screening pipeline",
            "severity": "INFO",
            "description": "Glaucoma workflow recommends optic nerve and visual field correlation."
        })
        recommendations.append("Check optic nerve appearance, IOP and visual field data.")

    else:
        findings.append({
            "code": "RETINA_SCREENING_PIPELINE",
            "label": "Retina screening pipeline",
            "severity": "INFO",
            "description": "Retinal screening pipeline completed."
        })
        recommendations.append("Perform ophthalmologist validation before clinical use.")

    risk_score = 30

    if image_type_l == "glaucoma":
        risk_score += 22
    elif image_type_l == "oct":
        risk_score += 16
    elif image_type_l == "retina":
        risk_score += 12
    else:
        risk_score += 8

    if quality_score < 45:
        risk_score += 25
    elif quality_score < 65:
        risk_score += 12

    if contrast < 25 and contrast > 0:
        risk_score += 10

    if sharpness < 8 and sharpness > 0:
        risk_score += 10

    risk_score = max(0, min(100, int(risk_score)))

    if risk_score >= 75:
        risk_level = "HIGH"
        safety_gate = "REQUIRES_URGENT_OPHTHALMOLOGIST_REVIEW"
    elif risk_score >= 45:
        risk_level = "MODERATE"
        safety_gate = "REQUIRES_OPHTHALMOLOGIST_REVIEW"
    else:
        risk_level = "LOW"
        safety_gate = "ROUTINE_REVIEW_REQUIRED"

    if quality_score < 45:
        safety_gate = "IMAGE_QUALITY_INSUFFICIENT_REPEAT_SCAN"

    return {
        "read_status": read_status,
        "width": width,
        "height": height,
        "brightness": round(brightness, 2),
        "contrast": round(contrast, 2),
        "sharpness": round(sharpness, 2),
        "quality_score": int(quality_score),
        "risk_score": int(risk_score),
        "risk_level": risk_level,
        "findings": findings,
        "recommendations": recommendations,
        "safety_gate": safety_gate,
        "clinical_status": "prototype_not_certified"
    }

@router.get("/phase-11/status")
async def ophthalmology_phase_11_status():
    _phase11_init_db()
    conn = _phase8_conn()

    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]

    avg_quality = conn.execute("SELECT AVG(quality_score) AS v FROM ophthalmology_ai_analyses").fetchone()["v"] or 0
    avg_risk = conn.execute("SELECT AVG(risk_score) AS v FROM ophthalmology_ai_analyses").fetchone()["v"] or 0

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 11",
        "features": [
            "real_image_file_reading",
            "image_quality_check",
            "brightness_contrast_sharpness_metrics",
            "fundus_oct_preprocessing",
            "ai_like_risk_scoring",
            "finding_categories",
            "clinical_safety_gate",
            "persistent_ai_analysis_storage",
            "analysis_pdf_export"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "average_quality_score": round(avg_quality, 2),
        "average_risk_score": round(avg_risk, 2),
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/phase-11/analyze-upload")
async def phase11_analyze_uploaded_image(
    file: UploadFile = File(...),
    patient_id: str = Form("AHOS-EYE-PHASE11-REAL-001"),
    image_type: str = Form("fundus"),
    language: str = Form("en")
):
    _phase11_init_db()

    case_id = "EYE-P11-" + _phase8_uuid.uuid4().hex[:10].upper()
    analysis_id = "EYE-AI-" + _phase8_uuid.uuid4().hex[:10].upper()

    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    saved_path = PHASE8_UPLOAD_DIR / f"{case_id}_{safe_name}"

    with saved_path.open("wb") as buffer:
        _phase8_shutil.copyfileobj(file.file, buffer)

    analysis = _phase11_analyze_image_basic(str(saved_path), image_type)
    now = datetime.utcnow().isoformat()

    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ophthalmology_cases (
        case_id, patient_id, filename, stored_path, image_type, language,
        risk_score, risk_level, status, ai_summary, clinical_notice,
        doctor_review_status, doctor_review_decision, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_id,
        patient_id,
        safe_name,
        str(saved_path),
        image_type,
        language,
        analysis["risk_score"],
        analysis["risk_level"],
        "phase11_real_image_analysis_completed",
        f"Phase 11 image pipeline completed. Quality={analysis['quality_score']}/100, Risk={analysis['risk_score']}/100.",
        "Prototype AI image analysis only. Not a certified diagnosis.",
        "pending",
        "Pending ophthalmologist validation.",
        now,
        now
    ))

    cur.execute("""
    INSERT INTO ophthalmology_ai_analyses (
        analysis_id, case_id, patient_id, image_type, filename,
        width, height, mode, quality_score, brightness, contrast, sharpness,
        risk_score, risk_level, findings_json, recommendations_json,
        safety_gate, clinical_status, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        analysis_id,
        case_id,
        patient_id,
        image_type,
        safe_name,
        analysis["width"],
        analysis["height"],
        analysis["read_status"],
        analysis["quality_score"],
        analysis["brightness"],
        analysis["contrast"],
        analysis["sharpness"],
        analysis["risk_score"],
        analysis["risk_level"],
        _phase11_json(analysis["findings"]),
        _phase11_json(analysis["recommendations"]),
        analysis["safety_gate"],
        analysis["clinical_status"],
        now
    ))

    report_id = "EYE-P11-REPORT-" + _phase8_uuid.uuid4().hex[:8].upper()
    cur.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        case_id,
        patient_id,
        "phase11_real_image_ai_analysis_report",
        analysis["risk_score"],
        analysis["risk_level"],
        language,
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(case_id, "phase11_real_image_ai_analysis", f"Analysis {analysis_id} completed")

    return {
        "status": "analysis_completed",
        "phase": "AHOS Ophthalmology Phase 11",
        "case_id": case_id,
        "analysis_id": analysis_id,
        "patient_id": patient_id,
        "image_type": image_type,
        "filename": safe_name,
        "stored_path": str(saved_path),
        "analysis": analysis,
        "clinical_notice": "Prototype only. Not a certified diagnosis. Ophthalmologist validation required."
    }

@router.get("/phase-11/analyses")
async def phase11_list_analyses():
    _phase11_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 100
    """).fetchall()

    conn.close()

    return {
        "status": "online",
        "total_analyses": len(rows),
        "analyses": [dict(r) for r in rows]
    }

@router.get("/phase-11/analyses/{analysis_id}")
async def phase11_get_analysis(analysis_id: str):
    _phase11_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    WHERE analysis_id = ?
    """, (analysis_id,)).fetchone()

    conn.close()

    if not row:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    return {
        "status": "online",
        "analysis": dict(row)
    }

@router.get("/phase-11/analytics")
async def phase11_analytics():
    _phase11_init_db()
    conn = _phase8_conn()

    quality_rows = conn.execute("""
    SELECT
      CASE
        WHEN quality_score >= 80 THEN 'EXCELLENT'
        WHEN quality_score >= 60 THEN 'GOOD'
        WHEN quality_score >= 40 THEN 'LIMITED'
        ELSE 'POOR'
      END AS label,
      COUNT(*) AS value
    FROM ophthalmology_ai_analyses
    GROUP BY label
    ORDER BY value DESC
    """).fetchall()

    risk_rows = conn.execute("""
    SELECT risk_level AS label, COUNT(*) AS value
    FROM ophthalmology_ai_analyses
    GROUP BY risk_level
    ORDER BY value DESC
    """).fetchall()

    type_rows = conn.execute("""
    SELECT image_type AS label, COUNT(*) AS value
    FROM ophthalmology_ai_analyses
    GROUP BY image_type
    ORDER BY value DESC
    """).fetchall()

    recent = conn.execute("""
    SELECT analysis_id, case_id, patient_id, image_type, quality_score, risk_score, risk_level, safety_gate, created_at
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 30
    """).fetchall()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 11 Analytics",
        "quality_distribution": [dict(r) for r in quality_rows],
        "risk_distribution": [dict(r) for r in risk_rows],
        "image_type_distribution": [dict(r) for r in type_rows],
        "recent_analyses": [dict(r) for r in recent],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-11/analyses/{analysis_id}/report-pdf")
async def phase11_analysis_report_pdf(analysis_id: str):
    _phase11_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    WHERE analysis_id = ?
    """, (analysis_id,)).fetchone()

    conn.close()

    if not row:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    r = dict(row)

    lines = [
        "AHOS Ophthalmology Phase 11",
        "Real Fundus/OCT Image AI Analysis Pipeline",
        "",
        f"Analysis ID: {r.get('analysis_id')}",
        f"Case ID: {r.get('case_id')}",
        f"Patient ID: {r.get('patient_id')}",
        f"Image Type: {r.get('image_type')}",
        f"Filename: {r.get('filename')}",
        "",
        "Image Metrics:",
        f"- Width: {r.get('width')}",
        f"- Height: {r.get('height')}",
        f"- Decoder Mode: {r.get('mode')}",
        f"- Quality Score: {r.get('quality_score')}/100",
        f"- Brightness: {r.get('brightness')}",
        f"- Contrast: {r.get('contrast')}",
        f"- Sharpness: {r.get('sharpness')}",
        "",
        "AI-like Risk Assessment:",
        f"- Risk Score: {r.get('risk_score')}/100",
        f"- Risk Level: {r.get('risk_level')}",
        f"- Safety Gate: {r.get('safety_gate')}",
        "",
        "Clinical Safety Notice:",
        "Prototype image analysis only.",
        "Not a certified diagnosis.",
        "A licensed ophthalmologist must validate before clinical use.",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase11_Image_AI_Analysis_{analysis_id}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 12
# Real OCT/Fundus Viewer + Image Preview + Heatmap Overlay
# ============================

@router.get("/phase-12/status")
async def ophthalmology_phase_12_status():
    _phase11_init_db()
    conn = _phase8_conn()

    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]

    last = conn.execute("""
    SELECT analysis_id, case_id, patient_id, image_type, filename, width, height,
           quality_score, risk_score, risk_level, safety_gate, created_at
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 12",
        "features": [
            "real_image_preview",
            "image_stream_endpoint",
            "latest_analysis_viewer",
            "heatmap_overlay_metadata",
            "optic_disc_focus_box",
            "retina_focus_zone",
            "toggle_heatmap_ready",
            "analysis_linked_to_image",
            "viewer_pdf_export_ready"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "latest_analysis": dict(last) if last else None,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

def _phase12_get_analysis_row(analysis_id: str):
    _phase11_init_db()
    conn = _phase8_conn()
    row = conn.execute("""
    SELECT a.*, c.stored_path
    FROM ophthalmology_ai_analyses a
    LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
    WHERE a.analysis_id = ?
    """, (analysis_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

@router.get("/phase-12/latest")
async def phase12_latest_analysis_viewer():
    _phase11_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT a.*, c.stored_path
    FROM ophthalmology_ai_analyses a
    LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
    ORDER BY a.created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    if not row:
        return {
            "status": "empty",
            "message": "No Phase 11 analysis found. Run Phase 11 image analysis first."
        }

    r = dict(row)

    image_url = f"/api/ophthalmology/phase-12/analyses/{r['analysis_id']}/image"
    heatmap_url = f"/api/ophthalmology/phase-12/analyses/{r['analysis_id']}/heatmap"

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 12",
        "analysis": r,
        "image_url": image_url,
        "heatmap_url": heatmap_url,
        "viewer": {
            "heatmap_opacity": 0.42,
            "optic_disc_box": {
                "x_percent": 44,
                "y_percent": 40,
                "width_percent": 16,
                "height_percent": 22,
                "label": "Optic disc focus"
            },
            "retina_focus_zone": {
                "x_percent": 20,
                "y_percent": 18,
                "width_percent": 60,
                "height_percent": 64,
                "label": "Retina focus zone"
            },
            "macula_focus_point": {
                "x_percent": 56,
                "y_percent": 52,
                "radius_percent": 7,
                "label": "Macula focus"
            }
        },
        "clinical_notice": "Prototype viewer only. Heatmap is simulated and not certified for diagnosis."
    }

@router.get("/phase-12/analyses/{analysis_id}/viewer")
async def phase12_analysis_viewer(analysis_id: str):
    r = _phase12_get_analysis_row(analysis_id)

    if not r:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 12",
        "analysis": r,
        "image_url": f"/api/ophthalmology/phase-12/analyses/{analysis_id}/image",
        "heatmap_url": f"/api/ophthalmology/phase-12/analyses/{analysis_id}/heatmap",
        "viewer": {
            "heatmap_opacity": 0.42,
            "optic_disc_box": {
                "x_percent": 44,
                "y_percent": 40,
                "width_percent": 16,
                "height_percent": 22,
                "label": "Optic disc focus"
            },
            "retina_focus_zone": {
                "x_percent": 20,
                "y_percent": 18,
                "width_percent": 60,
                "height_percent": 64,
                "label": "Retina focus zone"
            },
            "macula_focus_point": {
                "x_percent": 56,
                "y_percent": 52,
                "radius_percent": 7,
                "label": "Macula focus"
            }
        },
        "clinical_notice": "Prototype viewer only. Heatmap is simulated and not certified for diagnosis."
    }

@router.get("/phase-12/analyses/{analysis_id}/image")
async def phase12_stream_analysis_image(analysis_id: str):
    r = _phase12_get_analysis_row(analysis_id)

    if not r:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    path = r.get("stored_path") or ""
    fp = _Phase8Path(path)

    if not fp.exists():
        return {
            "status": "image_not_found",
            "analysis_id": analysis_id,
            "path": path
        }

    suffix = fp.suffix.lower()
    media_type = "image/png"

    if suffix in [".jpg", ".jpeg"]:
        media_type = "image/jpeg"
    elif suffix == ".svg":
        media_type = "image/svg+xml"
    elif suffix == ".webp":
        media_type = "image/webp"
    elif suffix in [".tif", ".tiff"]:
        media_type = "image/tiff"

    return Response(
        content=fp.read_bytes(),
        media_type=media_type,
        headers={
            "Content-Disposition": f"inline; filename={fp.name}"
        }
    )

def _phase12_generate_heatmap_png(base_path: str, analysis_id: str):
    heatmap_dir = _Phase8Path("reports/ophthalmology_phase12/heatmaps")
    heatmap_dir.mkdir(parents=True, exist_ok=True)
    out = heatmap_dir / f"AHOS_Phase12_Heatmap_{analysis_id}.png"

    if out.exists():
        return out

    try:
        from PIL import Image, ImageDraw, ImageFilter

        img = Image.open(base_path).convert("RGBA")
        w, h = img.size

        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay, "RGBA")

        # Retina focus glow
        d.ellipse(
            (int(w*0.20), int(h*0.18), int(w*0.80), int(h*0.82)),
            fill=(34, 211, 238, 35),
            outline=(34, 211, 238, 120),
            width=max(3, int(w*0.006))
        )

        # Optic disc attention
        d.ellipse(
            (int(w*0.42), int(h*0.38), int(w*0.60), int(h*0.62)),
            fill=(255, 90, 90, 85),
            outline=(255, 180, 70, 180),
            width=max(3, int(w*0.006))
        )

        # Macula focus
        d.ellipse(
            (int(w*0.54), int(h*0.50), int(w*0.68), int(h*0.64)),
            fill=(255, 220, 80, 70),
            outline=(255, 255, 120, 170),
            width=max(2, int(w*0.004))
        )

        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=max(2, int(w*0.006))))
        combined = Image.alpha_composite(img, overlay)
        combined.save(out)

        return out

    except Exception:
        # transparent fallback PNG, if Pillow fails
        try:
            from PIL import Image
            Image.new("RGBA", (800, 500), (0, 0, 0, 0)).save(out)
            return out
        except Exception:
            return None

@router.get("/phase-12/analyses/{analysis_id}/heatmap")
async def phase12_stream_heatmap(analysis_id: str):
    r = _phase12_get_analysis_row(analysis_id)

    if not r:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    path = r.get("stored_path") or ""
    fp = _Phase8Path(path)

    if not fp.exists():
        return {
            "status": "image_not_found",
            "analysis_id": analysis_id,
            "path": path
        }

    out = _phase12_generate_heatmap_png(str(fp), analysis_id)

    if not out or not out.exists():
        return {
            "status": "heatmap_generation_failed",
            "analysis_id": analysis_id
        }

    return Response(
        content=out.read_bytes(),
        media_type="image/png",
        headers={
            "Content-Disposition": f"inline; filename={out.name}"
        }
    )

@router.get("/phase-12/analyses/{analysis_id}/viewer-report-pdf")
async def phase12_viewer_report_pdf(analysis_id: str):
    r = _phase12_get_analysis_row(analysis_id)

    if not r:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    lines = [
        "AHOS Ophthalmology Phase 12",
        "Real OCT/Fundus Viewer + Image Preview + Heatmap Overlay",
        "",
        f"Analysis ID: {r.get('analysis_id')}",
        f"Case ID: {r.get('case_id')}",
        f"Patient ID: {r.get('patient_id')}",
        f"Image Type: {r.get('image_type')}",
        f"Filename: {r.get('filename')}",
        f"Image Size: {r.get('width')} x {r.get('height')}",
        "",
        "Image Analysis:",
        f"- Quality Score: {r.get('quality_score')}/100",
        f"- Brightness: {r.get('brightness')}",
        f"- Contrast: {r.get('contrast')}",
        f"- Sharpness: {r.get('sharpness')}",
        f"- Risk Score: {r.get('risk_score')}/100",
        f"- Risk Level: {r.get('risk_level')}",
        f"- Safety Gate: {r.get('safety_gate')}",
        "",
        "Viewer Layers:",
        "- Image Preview: enabled",
        "- Simulated Heatmap Overlay: enabled",
        "- Optic Disc Focus Box: enabled",
        "- Retina Focus Zone: enabled",
        "- Macula Focus Point: enabled",
        "",
        "Clinical Safety Notice:",
        "Prototype viewer only.",
        "Heatmap is simulated and not certified for diagnosis.",
        "A licensed ophthalmologist must validate before clinical use.",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase12_Viewer_Report_{analysis_id}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 13
# Annotation Tools + Save Doctor Findings
# ============================

def _phase13_init_db():
    _phase11_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_annotations (
        annotation_id TEXT PRIMARY KEY,
        analysis_id TEXT,
        case_id TEXT,
        patient_id TEXT,
        annotation_type TEXT,
        shape TEXT,
        x_percent REAL,
        y_percent REAL,
        width_percent REAL,
        height_percent REAL,
        marker_x_percent REAL,
        marker_y_percent REAL,
        severity TEXT,
        doctor_note TEXT,
        doctor_name TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase13_latest_analysis():
    _phase13_init_db()
    conn = _phase8_conn()
    row = conn.execute("""
    SELECT a.*, c.stored_path
    FROM ophthalmology_ai_analyses a
    LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
    ORDER BY a.created_at DESC
    LIMIT 1
    """).fetchone()
    conn.close()
    return dict(row) if row else None

@router.get("/phase-13/status")
async def phase13_status():
    _phase13_init_db()
    conn = _phase8_conn()

    total_annotations = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_annotations").fetchone()["c"]
    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]

    latest = conn.execute("""
    SELECT annotation_id, analysis_id, case_id, annotation_type, severity, created_at
    FROM ophthalmology_annotations
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 13",
        "features": [
            "doctor_annotation_tools",
            "box_annotation",
            "marker_annotation",
            "annotation_type_selection",
            "doctor_finding_notes",
            "sqlite_annotation_storage",
            "annotation_list",
            "annotation_pdf_export",
            "linked_analysis_and_case"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "total_annotations": total_annotations,
        "latest_annotation": dict(latest) if latest else None,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-13/latest")
async def phase13_latest():
    analysis = _phase13_latest_analysis()

    if not analysis:
        return {
            "status": "empty",
            "message": "No Phase 11 analysis found. Run Phase 11 first."
        }

    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    ORDER BY created_at DESC
    """, (analysis["analysis_id"],)).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 13",
        "analysis": analysis,
        "image_url": f"/api/ophthalmology/phase-12/analyses/{analysis['analysis_id']}/image",
        "heatmap_url": f"/api/ophthalmology/phase-12/analyses/{analysis['analysis_id']}/heatmap",
        "annotations": [dict(r) for r in rows],
        "clinical_notice": "Prototype annotation tool only. Doctor findings require real ophthalmologist validation."
    }

@router.get("/phase-13/annotations")
async def phase13_list_annotations(analysis_id: str = Query("")):
    _phase13_init_db()
    conn = _phase8_conn()

    if analysis_id:
        rows = conn.execute("""
        SELECT *
        FROM ophthalmology_annotations
        WHERE analysis_id = ?
        ORDER BY created_at DESC
        """, (analysis_id,)).fetchall()
    else:
        rows = conn.execute("""
        SELECT *
        FROM ophthalmology_annotations
        ORDER BY created_at DESC
        LIMIT 200
        """).fetchall()

    conn.close()

    return {
        "status": "online",
        "total_annotations": len(rows),
        "annotations": [dict(r) for r in rows]
    }

@router.post("/phase-13/annotations/create")
async def phase13_create_annotation(
    analysis_id: str = Form(...),
    annotation_type: str = Form("retina"),
    shape: str = Form("box"),
    x_percent: float = Form(25.0),
    y_percent: float = Form(25.0),
    width_percent: float = Form(20.0),
    height_percent: float = Form(18.0),
    marker_x_percent: float = Form(50.0),
    marker_y_percent: float = Form(50.0),
    severity: str = Form("MODERATE"),
    doctor_note: str = Form("Doctor finding note."),
    doctor_name: str = Form("AHOS Doctor Demo")
):
    _phase13_init_db()

    analysis = _phase12_get_analysis_row(analysis_id)
    if not analysis:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    annotation_id = "EYE-ANN-" + _phase8_uuid.uuid4().hex[:10].upper()
    now = datetime.utcnow().isoformat()

    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ophthalmology_annotations (
        annotation_id, analysis_id, case_id, patient_id, annotation_type, shape,
        x_percent, y_percent, width_percent, height_percent,
        marker_x_percent, marker_y_percent,
        severity, doctor_note, doctor_name,
        status, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        annotation_id,
        analysis_id,
        analysis.get("case_id"),
        analysis.get("patient_id"),
        annotation_type,
        shape,
        x_percent,
        y_percent,
        width_percent,
        height_percent,
        marker_x_percent,
        marker_y_percent,
        severity,
        doctor_note,
        doctor_name,
        "saved",
        now,
        now
    ))

    report_id = "EYE-P13-ANN-" + _phase8_uuid.uuid4().hex[:8].upper()
    cur.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        analysis.get("case_id"),
        analysis.get("patient_id"),
        "phase13_doctor_annotation",
        analysis.get("risk_score"),
        analysis.get("risk_level"),
        "en",
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(analysis.get("case_id"), "phase13_annotation_saved", f"{annotation_id} {annotation_type} {severity}")

    return {
        "status": "annotation_saved",
        "annotation_id": annotation_id,
        "analysis_id": analysis_id,
        "case_id": analysis.get("case_id"),
        "patient_id": analysis.get("patient_id"),
        "annotation_type": annotation_type,
        "shape": shape,
        "severity": severity,
        "doctor_note": doctor_note,
        "doctor_name": doctor_name,
        "created_at": now
    }

@router.delete("/phase-13/annotations/{annotation_id}")
async def phase13_delete_annotation(annotation_id: str):
    _phase13_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE annotation_id = ?
    """, (annotation_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "annotation_id": annotation_id
        }

    conn.execute("DELETE FROM ophthalmology_annotations WHERE annotation_id = ?", (annotation_id,))
    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "annotation_id": annotation_id
    }

@router.get("/phase-13/annotations/{annotation_id}")
async def phase13_get_annotation(annotation_id: str):
    _phase13_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE annotation_id = ?
    """, (annotation_id,)).fetchone()

    conn.close()

    if not row:
        return {
            "status": "not_found",
            "annotation_id": annotation_id
        }

    return {
        "status": "online",
        "annotation": dict(row)
    }

@router.get("/phase-13/analysis/{analysis_id}/annotations-report-pdf")
async def phase13_annotations_report_pdf(analysis_id: str):
    _phase13_init_db()

    analysis = _phase12_get_analysis_row(analysis_id)
    if not analysis:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    ORDER BY created_at ASC
    """, (analysis_id,)).fetchall()
    conn.close()

    lines = [
        "AHOS Ophthalmology Phase 13",
        "Doctor Annotation Findings Report",
        "",
        f"Analysis ID: {analysis.get('analysis_id')}",
        f"Case ID: {analysis.get('case_id')}",
        f"Patient ID: {analysis.get('patient_id')}",
        f"Image Type: {analysis.get('image_type')}",
        f"Risk Score: {analysis.get('risk_score')}/100",
        f"Risk Level: {analysis.get('risk_level')}",
        f"Safety Gate: {analysis.get('safety_gate')}",
        "",
        f"Total Annotations: {len(rows)}",
        ""
    ]

    for idx, r in enumerate(rows, start=1):
        d = dict(r)
        lines += [
            f"Annotation {idx}:",
            f"- Annotation ID: {d.get('annotation_id')}",
            f"- Type: {d.get('annotation_type')}",
            f"- Shape: {d.get('shape')}",
            f"- Severity: {d.get('severity')}",
            f"- Box: x={d.get('x_percent')}%, y={d.get('y_percent')}%, w={d.get('width_percent')}%, h={d.get('height_percent')}%",
            f"- Marker: x={d.get('marker_x_percent')}%, y={d.get('marker_y_percent')}%",
            f"- Doctor: {d.get('doctor_name')}",
            f"- Note: {d.get('doctor_note')}",
            f"- Created: {d.get('created_at')}",
            ""
        ]

    lines += [
        "Clinical Safety Notice:",
        "Prototype annotation tool only.",
        "Doctor findings must be validated by a licensed ophthalmologist.",
        "Not certified for real clinical diagnosis.",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase13_Doctor_Annotations_{analysis_id}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 14
# Clinical Review Workflow + Doctor Approval System
# ============================

def _phase14_init_db():
    _phase13_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_clinical_reviews (
        review_id TEXT PRIMARY KEY,
        analysis_id TEXT,
        case_id TEXT,
        patient_id TEXT,
        decision TEXT,
        priority TEXT,
        review_status TEXT,
        doctor_name TEXT,
        doctor_signature TEXT,
        review_note TEXT,
        follow_up_plan TEXT,
        annotation_count INTEGER,
        ai_risk_score INTEGER,
        ai_risk_level TEXT,
        safety_gate TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase14_latest_analysis():
    _phase14_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT a.*, c.stored_path
    FROM ophthalmology_ai_analyses a
    LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
    ORDER BY a.created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

@router.get("/phase-14/status")
async def phase14_status():
    _phase14_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_annotations = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_annotations").fetchone()["c"]
    total_reviews = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews").fetchone()["c"]

    latest = conn.execute("""
    SELECT review_id, analysis_id, case_id, decision, priority, review_status, doctor_name, created_at
    FROM ophthalmology_clinical_reviews
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    approved = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews WHERE decision='APPROVE'").fetchone()["c"]
    rejected = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews WHERE decision='REJECT'").fetchone()["c"]
    follow_up = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews WHERE decision='NEEDS_FOLLOW_UP'").fetchone()["c"]
    urgent = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews WHERE priority='URGENT'").fetchone()["c"]

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 14",
        "features": [
            "clinical_review_workflow",
            "doctor_approval_decision",
            "doctor_reject_decision",
            "needs_follow_up_decision",
            "clinical_priority",
            "doctor_signature",
            "review_note",
            "follow_up_plan",
            "sqlite_review_storage",
            "clinical_review_pdf",
            "linked_case_analysis_annotations"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "total_annotations": total_annotations,
        "total_reviews": total_reviews,
        "approved_reviews": approved,
        "rejected_reviews": rejected,
        "follow_up_reviews": follow_up,
        "urgent_reviews": urgent,
        "latest_review": dict(latest) if latest else None,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-14/latest")
async def phase14_latest():
    analysis = _phase14_latest_analysis()

    if not analysis:
        return {
            "status": "empty",
            "message": "No Phase 11 analysis found. Run Phase 11 first."
        }

    conn = _phase8_conn()

    annotations = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    ORDER BY created_at DESC
    """, (analysis["analysis_id"],)).fetchall()

    reviews = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE analysis_id = ?
    ORDER BY created_at DESC
    """, (analysis["analysis_id"],)).fetchall()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 14",
        "analysis": analysis,
        "image_url": f"/api/ophthalmology/phase-12/analyses/{analysis['analysis_id']}/image",
        "heatmap_url": f"/api/ophthalmology/phase-12/analyses/{analysis['analysis_id']}/heatmap",
        "annotations": [dict(r) for r in annotations],
        "clinical_reviews": [dict(r) for r in reviews],
        "clinical_notice": "Prototype clinical review workflow only. Not certified for real clinical decisions."
    }

@router.get("/phase-14/reviews")
async def phase14_list_reviews(analysis_id: str = Query("")):
    _phase14_init_db()
    conn = _phase8_conn()

    if analysis_id:
        rows = conn.execute("""
        SELECT *
        FROM ophthalmology_clinical_reviews
        WHERE analysis_id = ?
        ORDER BY created_at DESC
        """, (analysis_id,)).fetchall()
    else:
        rows = conn.execute("""
        SELECT *
        FROM ophthalmology_clinical_reviews
        ORDER BY created_at DESC
        LIMIT 200
        """).fetchall()

    conn.close()

    return {
        "status": "online",
        "total_reviews": len(rows),
        "reviews": [dict(r) for r in rows]
    }

@router.post("/phase-14/reviews/create")
async def phase14_create_review(
    analysis_id: str = Form(...),
    decision: str = Form("NEEDS_FOLLOW_UP"),
    priority: str = Form("HIGH"),
    review_status: str = Form("review_completed"),
    doctor_name: str = Form("AHOS Ophthalmology Doctor"),
    doctor_signature: str = Form("Signed electronically by AHOS Ophthalmology Doctor"),
    review_note: str = Form("Clinical review completed. Ophthalmologist validation required."),
    follow_up_plan: str = Form("Schedule ophthalmology follow-up and repeat imaging if needed.")
):
    _phase14_init_db()

    analysis = _phase12_get_analysis_row(analysis_id)
    if not analysis:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    conn = _phase8_conn()

    annotation_count = conn.execute("""
    SELECT COUNT(*) AS c
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    """, (analysis_id,)).fetchone()["c"]

    review_id = "EYE-REV-" + _phase8_uuid.uuid4().hex[:10].upper()
    now = datetime.utcnow().isoformat()

    conn.execute("""
    INSERT INTO ophthalmology_clinical_reviews (
        review_id, analysis_id, case_id, patient_id,
        decision, priority, review_status,
        doctor_name, doctor_signature, review_note, follow_up_plan,
        annotation_count, ai_risk_score, ai_risk_level, safety_gate,
        created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        review_id,
        analysis_id,
        analysis.get("case_id"),
        analysis.get("patient_id"),
        decision,
        priority,
        review_status,
        doctor_name,
        doctor_signature,
        review_note,
        follow_up_plan,
        annotation_count,
        analysis.get("risk_score"),
        analysis.get("risk_level"),
        analysis.get("safety_gate"),
        now,
        now
    ))

    report_id = "EYE-P14-REV-" + _phase8_uuid.uuid4().hex[:8].upper()
    conn.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        analysis.get("case_id"),
        analysis.get("patient_id"),
        "phase14_clinical_review",
        analysis.get("risk_score"),
        analysis.get("risk_level"),
        "en",
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(
        analysis.get("case_id"),
        "phase14_clinical_review_saved",
        f"{review_id} decision={decision} priority={priority}"
    )

    return {
        "status": "clinical_review_saved",
        "review_id": review_id,
        "analysis_id": analysis_id,
        "case_id": analysis.get("case_id"),
        "patient_id": analysis.get("patient_id"),
        "decision": decision,
        "priority": priority,
        "review_status": review_status,
        "doctor_name": doctor_name,
        "doctor_signature": doctor_signature,
        "annotation_count": annotation_count,
        "created_at": now
    }

@router.get("/phase-14/reviews/{review_id}")
async def phase14_get_review(review_id: str):
    _phase14_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE review_id = ?
    """, (review_id,)).fetchone()

    conn.close()

    if not row:
        return {
            "status": "not_found",
            "review_id": review_id
        }

    return {
        "status": "online",
        "review": dict(row)
    }

@router.delete("/phase-14/reviews/{review_id}")
async def phase14_delete_review(review_id: str):
    _phase14_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE review_id = ?
    """, (review_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "review_id": review_id
        }

    conn.execute("DELETE FROM ophthalmology_clinical_reviews WHERE review_id = ?", (review_id,))
    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "review_id": review_id
    }

@router.get("/phase-14/analysis/{analysis_id}/clinical-review-pdf")
async def phase14_clinical_review_pdf(analysis_id: str):
    _phase14_init_db()

    analysis = _phase12_get_analysis_row(analysis_id)
    if not analysis:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    conn = _phase8_conn()

    annotations = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    ORDER BY created_at ASC
    """, (analysis_id,)).fetchall()

    reviews = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE analysis_id = ?
    ORDER BY created_at ASC
    """, (analysis_id,)).fetchall()

    conn.close()

    lines = [
        "AHOS Ophthalmology Phase 14",
        "Clinical Review Workflow Report",
        "",
        f"Analysis ID: {analysis.get('analysis_id')}",
        f"Case ID: {analysis.get('case_id')}",
        f"Patient ID: {analysis.get('patient_id')}",
        f"Image Type: {analysis.get('image_type')}",
        f"Image Size: {analysis.get('width')} x {analysis.get('height')}",
        "",
        "AI Analysis Summary:",
        f"- Quality Score: {analysis.get('quality_score')}/100",
        f"- Risk Score: {analysis.get('risk_score')}/100",
        f"- Risk Level: {analysis.get('risk_level')}",
        f"- Safety Gate: {analysis.get('safety_gate')}",
        "",
        f"Doctor Annotations: {len(annotations)}",
    ]

    for idx, a in enumerate(annotations, start=1):
        d = dict(a)
        lines += [
            f"Annotation {idx}: {d.get('annotation_type')} / {d.get('shape')} / {d.get('severity')}",
            f"- Doctor: {d.get('doctor_name')}",
            f"- Note: {d.get('doctor_note')}",
            ""
        ]

    lines += [
        f"Clinical Reviews: {len(reviews)}",
        ""
    ]

    for idx, r in enumerate(reviews, start=1):
        d = dict(r)
        lines += [
            f"Clinical Review {idx}:",
            f"- Review ID: {d.get('review_id')}",
            f"- Decision: {d.get('decision')}",
            f"- Priority: {d.get('priority')}",
            f"- Review Status: {d.get('review_status')}",
            f"- Doctor: {d.get('doctor_name')}",
            f"- Signature: {d.get('doctor_signature')}",
            f"- Review Note: {d.get('review_note')}",
            f"- Follow-up Plan: {d.get('follow_up_plan')}",
            f"- Created: {d.get('created_at')}",
            ""
        ]

    lines += [
        "Clinical Safety Notice:",
        "Prototype clinical review workflow only.",
        "This is not certified for real clinical diagnosis or patient management.",
        "Licensed ophthalmologist validation and regulatory approval are required.",
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase14_Clinical_Review_{analysis_id}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 15
# Final Case Dossier + Full Patient Timeline
# ============================

def _phase15_init_db():
    _phase14_init_db()

def _phase15_latest_analysis():
    _phase15_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT a.*, c.stored_path, c.status AS case_status
    FROM ophthalmology_ai_analyses a
    LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
    ORDER BY a.created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

def _phase15_case_dossier(analysis_id: str = ""):
    _phase15_init_db()
    conn = _phase8_conn()

    if analysis_id:
        analysis = conn.execute("""
        SELECT a.*, c.stored_path, c.status AS case_status
        FROM ophthalmology_ai_analyses a
        LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
        WHERE a.analysis_id = ?
        """, (analysis_id,)).fetchone()
    else:
        analysis = conn.execute("""
        SELECT a.*, c.stored_path, c.status AS case_status
        FROM ophthalmology_ai_analyses a
        LEFT JOIN ophthalmology_cases c ON a.case_id = c.case_id
        ORDER BY a.created_at DESC
        LIMIT 1
        """).fetchone()

    if not analysis:
        conn.close()
        return None

    a = dict(analysis)
    aid = a.get("analysis_id")
    case_id = a.get("case_id")

    case_row = conn.execute("""
    SELECT *
    FROM ophthalmology_cases
    WHERE case_id = ?
    """, (case_id,)).fetchone()

    annotations = conn.execute("""
    SELECT *
    FROM ophthalmology_annotations
    WHERE analysis_id = ?
    ORDER BY created_at ASC
    """, (aid,)).fetchall()

    reviews = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE analysis_id = ?
    ORDER BY created_at ASC
    """, (aid,)).fetchall()

    reports = conn.execute("""
    SELECT *
    FROM ophthalmology_reports
    WHERE case_id = ?
    ORDER BY created_at ASC
    """, (case_id,)).fetchall()

    audits = conn.execute("""
    SELECT *
    FROM ophthalmology_audit_logs
    WHERE case_id = ?
    ORDER BY created_at ASC
    """, (case_id,)).fetchall()

    conn.close()

    timeline = []

    if case_row:
        c = dict(case_row)
        timeline.append({
            "phase": "Phase 8",
            "event": "Persistent case created",
            "status": c.get("status"),
            "timestamp": c.get("created_at"),
            "summary": f"Case {c.get('case_id')} stored in persistent SQLite database."
        })

    timeline.append({
        "phase": "Phase 11",
        "event": "Real image AI analysis",
        "status": a.get("risk_level"),
        "timestamp": a.get("created_at"),
        "summary": f"Image decoded. Quality {a.get('quality_score')}/100, risk {a.get('risk_score')}/100."
    })

    timeline.append({
        "phase": "Phase 12",
        "event": "Image viewer and heatmap",
        "status": "viewer_ready",
        "timestamp": a.get("created_at"),
        "summary": "Image preview, heatmap overlay, optic disc, retina and macula focus zones available."
    })

    for ann in annotations:
        d = dict(ann)
        timeline.append({
            "phase": "Phase 13",
            "event": "Doctor annotation saved",
            "status": d.get("severity"),
            "timestamp": d.get("created_at"),
            "summary": f"{d.get('annotation_type')} / {d.get('shape')} — {d.get('doctor_note')}"
        })

    for rev in reviews:
        d = dict(rev)
        timeline.append({
            "phase": "Phase 14",
            "event": "Clinical review decision",
            "status": d.get("decision"),
            "timestamp": d.get("created_at"),
            "summary": f"Decision {d.get('decision')} with priority {d.get('priority')}. Follow-up: {d.get('follow_up_plan')}"
        })

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 15",
        "case": dict(case_row) if case_row else None,
        "analysis": a,
        "annotations": [dict(x) for x in annotations],
        "clinical_reviews": [dict(x) for x in reviews],
        "reports": [dict(x) for x in reports],
        "audit_logs": [dict(x) for x in audits],
        "timeline": timeline,
        "image_url": f"/api/ophthalmology/phase-12/analyses/{aid}/image",
        "heatmap_url": f"/api/ophthalmology/phase-12/analyses/{aid}/heatmap",
        "summary": {
            "case_id": case_id,
            "analysis_id": aid,
            "patient_id": a.get("patient_id"),
            "image_type": a.get("image_type"),
            "quality_score": a.get("quality_score"),
            "risk_score": a.get("risk_score"),
            "risk_level": a.get("risk_level"),
            "safety_gate": a.get("safety_gate"),
            "annotation_count": len(annotations),
            "review_count": len(reviews),
            "latest_decision": dict(reviews[-1]).get("decision") if reviews else "NO_REVIEW",
            "latest_priority": dict(reviews[-1]).get("priority") if reviews else "NONE",
            "timeline_events": len(timeline)
        },
        "clinical_notice": "Final dossier is prototype only and not certified for clinical use."
    }

@router.get("/phase-15/status")
async def phase15_status():
    _phase15_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_annotations = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_annotations").fetchone()["c"]
    total_reviews = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]

    latest = conn.execute("""
    SELECT analysis_id, case_id, patient_id, image_type, risk_score, risk_level, created_at
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 15",
        "features": [
            "final_case_dossier",
            "full_patient_timeline",
            "phase8_persistent_case",
            "phase11_ai_image_analysis",
            "phase12_image_heatmap_viewer",
            "phase13_doctor_annotations",
            "phase14_clinical_review_decision",
            "final_html_dossier",
            "final_pdf_dossier",
            "multilingual_dossier_ready"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "total_annotations": total_annotations,
        "total_reviews": total_reviews,
        "total_reports": total_reports,
        "latest_analysis": dict(latest) if latest else None,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-15/latest")
async def phase15_latest():
    dossier = _phase15_case_dossier("")
    if not dossier:
        return {
            "status": "empty",
            "message": "No ophthalmology analysis found. Run Phase 11 first."
        }
    return dossier

@router.get("/phase-15/dossier/{analysis_id}")
async def phase15_dossier_by_analysis(analysis_id: str):
    dossier = _phase15_case_dossier(analysis_id)
    if not dossier:
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }
    return dossier

def _phase15_text(language: str):
    lang = (language or "en").lower()
    texts = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 15 - ملف الحالة النهائي",
            "summary": "ملف نهائي يجمع الحالة والتحليل والصورة والـ heatmap وملاحظات الطبيب والقرار السريري.",
            "clinical": "تنبيه: هذا الملف نموذج تجريبي وغير معتمد للاستخدام السريري الحقيقي.",
            "investor": "جاهز للعرض الاستثماري كنموذج رحلة حالة كاملة داخل AHOS."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 15 - Final Case Dossier",
            "summary": "Final dossier combining case storage, AI image analysis, image viewer, heatmap, doctor annotations and clinical review.",
            "clinical": "Notice: this dossier is a prototype and is not certified for real clinical use.",
            "investor": "Ready for investor demonstration as a complete case journey inside AHOS."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 15 - Slutlig falldossier",
            "summary": "Slutlig dossier som kombinerar fall, AI-bildanalys, bildvisare, heatmap, läkaranteckningar och klinisk granskning.",
            "clinical": "Obs: denna dossier är en prototyp och inte certifierad för klinisk användning.",
            "investor": "Redo för investerardemonstration som komplett fallresa i AHOS."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 15 - Dossier final du cas",
            "summary": "Dossier final combinant le cas, l’analyse IA, la visionneuse, la heatmap, les annotations médecin et la revue clinique.",
            "clinical": "Avis: ce dossier est un prototype et n’est pas certifié pour un usage clinique réel.",
            "investor": "Prêt pour démonstration investisseur comme parcours complet de cas dans AHOS."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 15 - Dossier finale del caso",
            "summary": "Dossier finale che combina caso, analisi IA, viewer immagine, heatmap, annotazioni medico e revisione clinica.",
            "clinical": "Avviso: questo dossier è un prototipo e non è certificato per uso clinico reale.",
            "investor": "Pronto per dimostrazione investitori come percorso completo del caso in AHOS."
        }
    }
    return texts.get(lang, texts["en"])

@router.get("/phase-15/dossier-html")
async def phase15_dossier_html(language: str = "en", analysis_id: str = ""):
    dossier = _phase15_case_dossier(analysis_id)
    if not dossier:
        return {
            "status": "empty",
            "message": "No dossier available."
        }

    tx = _phase15_text(language)
    s = dossier["summary"]
    timeline = dossier["timeline"]
    annotations = dossier["annotations"]
    reviews = dossier["clinical_reviews"]
    reports = dossier["reports"]

    def rows(items):
        out = ""
        for item in items:
            out += f"""
            <tr>
              <td>{item.get('phase','')}</td>
              <td>{item.get('event','')}</td>
              <td>{item.get('status','')}</td>
              <td>{item.get('timestamp','')}</td>
              <td>{item.get('summary','')}</td>
            </tr>
            """
        return out

    def annotation_rows(items):
        out = ""
        for a in items:
            out += f"""
            <tr>
              <td>{a.get('annotation_id','')}</td>
              <td>{a.get('annotation_type','')}</td>
              <td>{a.get('shape','')}</td>
              <td>{a.get('severity','')}</td>
              <td>{a.get('doctor_name','')}</td>
              <td>{a.get('doctor_note','')}</td>
            </tr>
            """
        return out

    def review_rows(items):
        out = ""
        for r in items:
            out += f"""
            <tr>
              <td>{r.get('review_id','')}</td>
              <td>{r.get('decision','')}</td>
              <td>{r.get('priority','')}</td>
              <td>{r.get('doctor_name','')}</td>
              <td>{r.get('review_note','')}</td>
              <td>{r.get('follow_up_plan','')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{
  background: #e0f2fe;
}}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Final Case Summary</h2>
<div class="grid">
  <div class="metric">Case ID<strong>{s.get('case_id')}</strong></div>
  <div class="metric">Analysis ID<strong>{s.get('analysis_id')}</strong></div>
  <div class="metric">Patient ID<strong>{s.get('patient_id')}</strong></div>
  <div class="metric">Quality Score<strong>{s.get('quality_score')}/100</strong></div>
  <div class="metric">Risk Score<strong>{s.get('risk_score')}/100</strong></div>
  <div class="metric">Risk Level<strong>{s.get('risk_level')}</strong></div>
  <div class="metric">Annotations<strong>{s.get('annotation_count')}</strong></div>
  <div class="metric">Reviews<strong>{s.get('review_count')}</strong></div>
  <div class="metric">Latest Decision<strong>{s.get('latest_decision')}</strong></div>
</div>

<h2>Full Patient Timeline</h2>
<table>
<tr><th>Phase</th><th>Event</th><th>Status</th><th>Timestamp</th><th>Summary</th></tr>
{rows(timeline)}
</table>

<h2>Doctor Annotations</h2>
<table>
<tr><th>ID</th><th>Type</th><th>Shape</th><th>Severity</th><th>Doctor</th><th>Note</th></tr>
{annotation_rows(annotations)}
</table>

<h2>Clinical Reviews</h2>
<table>
<tr><th>ID</th><th>Decision</th><th>Priority</th><th>Doctor</th><th>Review Note</th><th>Follow-up Plan</th></tr>
{review_rows(reviews)}
</table>

<h2>Generated Reports</h2>
<table>
<tr><th>Report ID</th><th>Type</th><th>Risk</th><th>Created</th></tr>
{''.join([f"<tr><td>{r.get('report_id')}</td><td>{r.get('report_type')}</td><td>{r.get('risk_score')} / {r.get('risk_level')}</td><td>{r.get('created_at')}</td></tr>" for r in reports])}
</table>

<div class="notice">
<p>{tx['clinical']}</p>
<p>{tx['investor']}</p>
</div>

</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase15_Final_Dossier_{language}.html"
        }
    )

@router.get("/phase-15/dossier-pdf")
async def phase15_dossier_pdf(language: str = "en", analysis_id: str = ""):
    dossier = _phase15_case_dossier(analysis_id)
    if not dossier:
        return {
            "status": "empty",
            "message": "No dossier available."
        }

    tx = _phase15_text(language)
    s = dossier["summary"]
    timeline = dossier["timeline"]
    annotations = dossier["annotations"]
    reviews = dossier["clinical_reviews"]

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 15 Final Case Dossier",
        "",
        tx["summary"],
        "",
        "Final Case Summary:",
        f"- Case ID: {s.get('case_id')}",
        f"- Analysis ID: {s.get('analysis_id')}",
        f"- Patient ID: {s.get('patient_id')}",
        f"- Image Type: {s.get('image_type')}",
        f"- Quality Score: {s.get('quality_score')}/100",
        f"- Risk Score: {s.get('risk_score')}/100",
        f"- Risk Level: {s.get('risk_level')}",
        f"- Safety Gate: {s.get('safety_gate')}",
        f"- Annotation Count: {s.get('annotation_count')}",
        f"- Review Count: {s.get('review_count')}",
        f"- Latest Decision: {s.get('latest_decision')}",
        f"- Latest Priority: {s.get('latest_priority')}",
        "",
        "Full Patient Timeline:",
    ]

    for i, item in enumerate(timeline, start=1):
        lines += [
            f"{i}. {item.get('phase')} - {item.get('event')}",
            f"   Status: {item.get('status')}",
            f"   Time: {item.get('timestamp')}",
            f"   Summary: {item.get('summary')}",
            ""
        ]

    lines += ["Doctor Annotations:"]
    if not annotations:
        lines.append("- No annotations.")
    else:
        for i, a in enumerate(annotations, start=1):
            lines += [
                f"{i}. {a.get('annotation_type')} / {a.get('shape')} / {a.get('severity')}",
                f"   Doctor: {a.get('doctor_name')}",
                f"   Note: {a.get('doctor_note')}",
                ""
            ]

    lines += ["Clinical Reviews:"]
    if not reviews:
        lines.append("- No reviews.")
    else:
        for i, r in enumerate(reviews, start=1):
            lines += [
                f"{i}. Decision: {r.get('decision')} / Priority: {r.get('priority')}",
                f"   Doctor: {r.get('doctor_name')}",
                f"   Signature: {r.get('doctor_signature')}",
                f"   Review Note: {r.get('review_note')}",
                f"   Follow-up: {r.get('follow_up_plan')}",
                ""
            ]

    lines += [
        "Clinical Safety Notice:",
        tx["clinical"],
        tx["investor"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase15_Final_Dossier_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 16
# Department Command Center + Multi-Case Registry
# ============================

def _phase16_init_db():
    _phase15_init_db()

def _phase16_all_cases():
    _phase16_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT
      c.case_id,
      c.patient_id,
      c.filename,
      c.stored_path,
      c.image_type,
      c.language,
      c.risk_score AS case_risk_score,
      c.risk_level AS case_risk_level,
      c.status AS case_status,
      c.created_at AS case_created_at,
      a.analysis_id,
      a.quality_score,
      a.brightness,
      a.contrast,
      a.sharpness,
      a.risk_score,
      a.risk_level,
      a.safety_gate,
      a.created_at AS analysis_created_at,
      (
        SELECT COUNT(*)
        FROM ophthalmology_annotations an
        WHERE an.analysis_id = a.analysis_id
      ) AS annotation_count,
      (
        SELECT COUNT(*)
        FROM ophthalmology_clinical_reviews rv
        WHERE rv.analysis_id = a.analysis_id
      ) AS review_count,
      (
        SELECT rv.decision
        FROM ophthalmology_clinical_reviews rv
        WHERE rv.analysis_id = a.analysis_id
        ORDER BY rv.created_at DESC
        LIMIT 1
      ) AS latest_decision,
      (
        SELECT rv.priority
        FROM ophthalmology_clinical_reviews rv
        WHERE rv.analysis_id = a.analysis_id
        ORDER BY rv.created_at DESC
        LIMIT 1
      ) AS latest_priority,
      (
        SELECT rv.review_status
        FROM ophthalmology_clinical_reviews rv
        WHERE rv.analysis_id = a.analysis_id
        ORDER BY rv.created_at DESC
        LIMIT 1
      ) AS latest_review_status
    FROM ophthalmology_cases c
    LEFT JOIN ophthalmology_ai_analyses a ON a.case_id = c.case_id
    ORDER BY c.created_at DESC
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]

def _phase16_filtered_cases(
    search: str = "",
    risk_level: str = "",
    decision: str = "",
    priority: str = "",
    image_type: str = ""
):
    rows = _phase16_all_cases()

    def ok(row):
        if search:
            s = search.lower()
            blob = " ".join([
                str(row.get("case_id", "")),
                str(row.get("analysis_id", "")),
                str(row.get("patient_id", "")),
                str(row.get("filename", "")),
                str(row.get("image_type", "")),
                str(row.get("risk_level", "")),
                str(row.get("latest_decision", "")),
                str(row.get("latest_priority", "")),
            ]).lower()
            if s not in blob:
                return False

        if risk_level and str(row.get("risk_level", "")).upper() != risk_level.upper():
            return False

        if decision and str(row.get("latest_decision", "")).upper() != decision.upper():
            return False

        if priority and str(row.get("latest_priority", "")).upper() != priority.upper():
            return False

        if image_type and str(row.get("image_type", "")).lower() != image_type.lower():
            return False

        return True

    return [r for r in rows if ok(r)]

def _phase16_counts(rows):
    def count_by(key):
        out = {}
        for r in rows:
            v = r.get(key) or "NONE"
            out[v] = out.get(v, 0) + 1
        return [{"label": k, "value": v} for k, v in sorted(out.items())]

    total = len(rows)
    follow_up = sum(1 for r in rows if str(r.get("latest_decision", "")).upper() == "NEEDS_FOLLOW_UP")
    urgent = sum(1 for r in rows if str(r.get("latest_priority", "")).upper() == "URGENT")
    high_priority = sum(1 for r in rows if str(r.get("latest_priority", "")).upper() == "HIGH")
    reviewed = sum(1 for r in rows if (r.get("review_count") or 0) > 0)
    annotated = sum(1 for r in rows if (r.get("annotation_count") or 0) > 0)

    avg_risk = 0
    avg_quality = 0
    risk_values = [int(r.get("risk_score") or 0) for r in rows if r.get("risk_score") is not None]
    quality_values = [int(r.get("quality_score") or 0) for r in rows if r.get("quality_score") is not None]

    if risk_values:
        avg_risk = round(sum(risk_values) / len(risk_values), 2)
    if quality_values:
        avg_quality = round(sum(quality_values) / len(quality_values), 2)

    return {
        "total_cases": total,
        "reviewed_cases": reviewed,
        "annotated_cases": annotated,
        "follow_up_cases": follow_up,
        "urgent_cases": urgent,
        "high_priority_cases": high_priority,
        "average_risk": avg_risk,
        "average_quality": avg_quality,
        "risk_distribution": count_by("risk_level"),
        "decision_distribution": count_by("latest_decision"),
        "priority_distribution": count_by("latest_priority"),
        "image_type_distribution": count_by("image_type")
    }

@router.get("/phase-16/status")
async def phase16_status():
    _phase16_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_annotations = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_annotations").fetchone()["c"]
    total_reviews = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews").fetchone()["c"]
    total_reports = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_reports").fetchone()["c"]
    total_audits = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_audit_logs").fetchone()["c"]

    conn.close()

    rows = _phase16_all_cases()
    metrics = _phase16_counts(rows)

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 16",
        "features": [
            "department_command_center",
            "multi_case_registry",
            "risk_level_filters",
            "decision_filters",
            "priority_filters",
            "image_type_filters",
            "department_kpis",
            "case_registry_dashboard",
            "follow_up_queue",
            "urgent_case_queue",
            "department_html_report",
            "department_pdf_report",
            "multilingual_command_center"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "total_annotations": total_annotations,
        "total_reviews": total_reviews,
        "total_reports": total_reports,
        "total_audit_logs": total_audits,
        "department_metrics": metrics,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-16/registry")
async def phase16_registry(
    search: str = Query(""),
    risk_level: str = Query(""),
    decision: str = Query(""),
    priority: str = Query(""),
    image_type: str = Query("")
):
    rows = _phase16_filtered_cases(search, risk_level, decision, priority, image_type)
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 16 Registry",
        "filters": {
            "search": search,
            "risk_level": risk_level,
            "decision": decision,
            "priority": priority,
            "image_type": image_type
        },
        "total_cases": len(rows),
        "cases": rows
    }

@router.get("/phase-16/dashboard")
async def phase16_dashboard():
    rows = _phase16_all_cases()
    metrics = _phase16_counts(rows)

    recent_cases = rows[:10]
    follow_up_queue = [
        r for r in rows
        if str(r.get("latest_decision", "")).upper() == "NEEDS_FOLLOW_UP"
    ][:10]

    urgent_queue = [
        r for r in rows
        if str(r.get("latest_priority", "")).upper() in ["URGENT", "HIGH"]
    ][:10]

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 16 Dashboard",
        "metrics": metrics,
        "recent_cases": recent_cases,
        "follow_up_queue": follow_up_queue,
        "urgent_queue": urgent_queue,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

def _phase16_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 16 - مركز قيادة قسم العيون",
            "summary": "تقرير إداري يجمع سجل كل حالات العيون، المؤشرات، الحالات التي تحتاج متابعة، والحالات ذات الأولوية.",
            "notice": "هذا التقرير نموذج تجريبي وليس معتمدًا للاستخدام السريري الحقيقي."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 16 - Department Command Center",
            "summary": "Department report combining multi-case registry, KPIs, follow-up queue and priority cases.",
            "notice": "This report is a prototype and is not certified for real clinical use."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 16 - Avdelningens ledningscentral",
            "summary": "Avdelningsrapport med fallregister, KPI:er, uppföljningskö och prioriterade fall.",
            "notice": "Denna rapport är en prototyp och inte certifierad för klinisk användning."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 16 - Centre de commandement du service",
            "summary": "Rapport du service avec registre multi-cas, indicateurs, suivi et cas prioritaires.",
            "notice": "Ce rapport est un prototype et n’est pas certifié pour un usage clinique réel."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 16 - Centro comando reparto",
            "summary": "Report di reparto con registro multi-caso, KPI, coda follow-up e casi prioritari.",
            "notice": "Questo report è un prototipo e non è certificato per uso clinico reale."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-16/department-report-html")
async def phase16_department_report_html(language: str = "en"):
    rows = _phase16_all_cases()
    metrics = _phase16_counts(rows)
    tx = _phase16_text(language)

    def case_rows(items):
        out = ""
        for r in items:
            out += f"""
            <tr>
              <td>{r.get('case_id','')}</td>
              <td>{r.get('patient_id','')}</td>
              <td>{r.get('image_type','')}</td>
              <td>{r.get('quality_score','')}</td>
              <td>{r.get('risk_score','')} / {r.get('risk_level','')}</td>
              <td>{r.get('latest_decision') or 'NONE'}</td>
              <td>{r.get('latest_priority') or 'NONE'}</td>
              <td>{r.get('annotation_count') or 0}</td>
              <td>{r.get('review_count') or 0}</td>
            </tr>
            """
        return out

    def dist_rows(items):
        out = ""
        for x in items:
            out += f"<tr><td>{x.get('label')}</td><td>{x.get('value')}</td></tr>"
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Department KPIs</h2>
<div class="grid">
  <div class="metric">Total Cases<strong>{metrics.get('total_cases')}</strong></div>
  <div class="metric">Reviewed Cases<strong>{metrics.get('reviewed_cases')}</strong></div>
  <div class="metric">Annotated Cases<strong>{metrics.get('annotated_cases')}</strong></div>
  <div class="metric">Follow-up Cases<strong>{metrics.get('follow_up_cases')}</strong></div>
  <div class="metric">Urgent Cases<strong>{metrics.get('urgent_cases')}</strong></div>
  <div class="metric">High Priority<strong>{metrics.get('high_priority_cases')}</strong></div>
  <div class="metric">Average Risk<strong>{metrics.get('average_risk')}</strong></div>
  <div class="metric">Average Quality<strong>{metrics.get('average_quality')}</strong></div>
</div>

<h2>Risk Distribution</h2>
<table>
<tr><th>Risk Level</th><th>Count</th></tr>
{dist_rows(metrics.get('risk_distribution', []))}
</table>

<h2>Decision Distribution</h2>
<table>
<tr><th>Decision</th><th>Count</th></tr>
{dist_rows(metrics.get('decision_distribution', []))}
</table>

<h2>Priority Distribution</h2>
<table>
<tr><th>Priority</th><th>Count</th></tr>
{dist_rows(metrics.get('priority_distribution', []))}
</table>

<h2>Multi-Case Registry</h2>
<table>
<tr>
<th>Case ID</th><th>Patient ID</th><th>Type</th><th>Quality</th><th>Risk</th>
<th>Decision</th><th>Priority</th><th>Annotations</th><th>Reviews</th>
</tr>
{case_rows(rows)}
</table>

<div class="notice">
<p>{tx['notice']}</p>
</div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase16_Department_Command_Center_{language}.html"
        }
    )

@router.get("/phase-16/department-report-pdf")
async def phase16_department_report_pdf(language: str = "en"):
    rows = _phase16_all_cases()
    metrics = _phase16_counts(rows)
    tx = _phase16_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 16 Department Command Center",
        "",
        tx["summary"],
        "",
        "Department KPIs:",
        f"- Total Cases: {metrics.get('total_cases')}",
        f"- Reviewed Cases: {metrics.get('reviewed_cases')}",
        f"- Annotated Cases: {metrics.get('annotated_cases')}",
        f"- Follow-up Cases: {metrics.get('follow_up_cases')}",
        f"- Urgent Cases: {metrics.get('urgent_cases')}",
        f"- High Priority Cases: {metrics.get('high_priority_cases')}",
        f"- Average Risk: {metrics.get('average_risk')}",
        f"- Average Quality: {metrics.get('average_quality')}",
        "",
        "Risk Distribution:",
    ]

    for x in metrics.get("risk_distribution", []):
        lines.append(f"- {x.get('label')}: {x.get('value')}")

    lines += ["", "Decision Distribution:"]
    for x in metrics.get("decision_distribution", []):
        lines.append(f"- {x.get('label')}: {x.get('value')}")

    lines += ["", "Priority Distribution:"]
    for x in metrics.get("priority_distribution", []):
        lines.append(f"- {x.get('label')}: {x.get('value')}")

    lines += ["", "Multi-Case Registry:"]
    for i, r in enumerate(rows, start=1):
        lines += [
            f"{i}. Case: {r.get('case_id')}",
            f"   Patient: {r.get('patient_id')}",
            f"   Type: {r.get('image_type')}",
            f"   Quality: {r.get('quality_score')}/100",
            f"   Risk: {r.get('risk_score')}/100 {r.get('risk_level')}",
            f"   Decision: {r.get('latest_decision') or 'NONE'}",
            f"   Priority: {r.get('latest_priority') or 'NONE'}",
            f"   Annotations: {r.get('annotation_count') or 0}",
            f"   Reviews: {r.get('review_count') or 0}",
            ""
        ]

    lines += [
        "Clinical Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase16_Department_Command_Center_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 17
# Real Hospital Triage Queue + Appointment Follow-up
# ============================

def _phase17_init_db():
    _phase16_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_triage_queue (
        triage_id TEXT PRIMARY KEY,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        triage_priority TEXT,
        triage_status TEXT,
        assigned_doctor TEXT,
        department_unit TEXT,
        appointment_date TEXT,
        appointment_status TEXT,
        patient_contact TEXT,
        triage_reason TEXT,
        follow_up_notes TEXT,
        latest_decision TEXT,
        latest_risk_score INTEGER,
        latest_risk_level TEXT,
        safety_gate TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase17_latest_review_case():
    _phase17_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT
      rv.*,
      a.image_type,
      a.quality_score,
      a.risk_score,
      a.risk_level,
      a.safety_gate
    FROM ophthalmology_clinical_reviews rv
    LEFT JOIN ophthalmology_ai_analyses a ON a.analysis_id = rv.analysis_id
    ORDER BY rv.created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

def _phase17_all_triage():
    _phase17_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_triage_queue
    ORDER BY
      CASE triage_priority
        WHEN 'URGENT' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MODERATE' THEN 3
        WHEN 'LOW' THEN 4
        ELSE 5
      END,
      created_at DESC
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]

def _phase17_filtered_triage(
    search: str = "",
    priority: str = "",
    triage_status: str = "",
    appointment_status: str = "",
    doctor: str = ""
):
    rows = _phase17_all_triage()

    def ok(row):
        if search:
            s = search.lower()
            blob = " ".join([
                str(row.get("triage_id", "")),
                str(row.get("case_id", "")),
                str(row.get("analysis_id", "")),
                str(row.get("patient_id", "")),
                str(row.get("assigned_doctor", "")),
                str(row.get("appointment_status", "")),
                str(row.get("triage_priority", "")),
                str(row.get("triage_status", "")),
            ]).lower()
            if s not in blob:
                return False

        if priority and str(row.get("triage_priority", "")).upper() != priority.upper():
            return False

        if triage_status and str(row.get("triage_status", "")).lower() != triage_status.lower():
            return False

        if appointment_status and str(row.get("appointment_status", "")).lower() != appointment_status.lower():
            return False

        if doctor and doctor.lower() not in str(row.get("assigned_doctor", "")).lower():
            return False

        return True

    return [r for r in rows if ok(r)]

def _phase17_metrics(rows):
    def count_by(key):
        out = {}
        for r in rows:
            v = r.get(key) or "NONE"
            out[v] = out.get(v, 0) + 1
        return [{"label": k, "value": v} for k, v in sorted(out.items())]

    total = len(rows)
    pending = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "pending")
    scheduled = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "scheduled")
    completed = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "completed")
    missed = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "missed")
    urgent = sum(1 for r in rows if str(r.get("triage_priority","")).upper() == "URGENT")
    high = sum(1 for r in rows if str(r.get("triage_priority","")).upper() == "HIGH")

    return {
        "total_triage_items": total,
        "pending_appointments": pending,
        "scheduled_appointments": scheduled,
        "completed_appointments": completed,
        "missed_appointments": missed,
        "urgent_triage": urgent,
        "high_priority_triage": high,
        "priority_distribution": count_by("triage_priority"),
        "triage_status_distribution": count_by("triage_status"),
        "appointment_status_distribution": count_by("appointment_status"),
        "doctor_distribution": count_by("assigned_doctor")
    }

@router.get("/phase-17/status")
async def phase17_status():
    _phase17_init_db()
    conn = _phase8_conn()

    total_cases = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_cases").fetchone()["c"]
    total_analyses = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_ai_analyses").fetchone()["c"]
    total_reviews = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_clinical_reviews").fetchone()["c"]
    total_triage = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_triage_queue").fetchone()["c"]

    latest = conn.execute("""
    SELECT triage_id, case_id, analysis_id, patient_id, triage_priority,
           triage_status, appointment_status, assigned_doctor, appointment_date, created_at
    FROM ophthalmology_triage_queue
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    rows = _phase17_all_triage()
    metrics = _phase17_metrics(rows)

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 17",
        "features": [
            "real_hospital_triage_queue",
            "appointment_follow_up",
            "appointment_status_tracking",
            "triage_priority",
            "assigned_doctor",
            "follow_up_date",
            "patient_contact_placeholder",
            "triage_notes",
            "sqlite_triage_storage",
            "triage_dashboard",
            "triage_html_report",
            "triage_pdf_report",
            "multilingual_triage_center"
        ],
        "total_cases": total_cases,
        "total_analyses": total_analyses,
        "total_reviews": total_reviews,
        "total_triage_items": total_triage,
        "latest_triage": dict(latest) if latest else None,
        "triage_metrics": metrics,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-17/queue")
async def phase17_queue(
    search: str = Query(""),
    priority: str = Query(""),
    triage_status: str = Query(""),
    appointment_status: str = Query(""),
    doctor: str = Query("")
):
    rows = _phase17_filtered_triage(search, priority, triage_status, appointment_status, doctor)
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 17 Queue",
        "filters": {
            "search": search,
            "priority": priority,
            "triage_status": triage_status,
            "appointment_status": appointment_status,
            "doctor": doctor
        },
        "total_triage_items": len(rows),
        "queue": rows
    }

@router.get("/phase-17/dashboard")
async def phase17_dashboard():
    rows = _phase17_all_triage()
    metrics = _phase17_metrics(rows)

    urgent_queue = [
        r for r in rows
        if str(r.get("triage_priority","")).upper() in ["URGENT", "HIGH"]
    ][:10]

    pending_queue = [
        r for r in rows
        if str(r.get("appointment_status","")).lower() in ["pending", "scheduled"]
    ][:10]

    latest_review = _phase17_latest_review_case()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 17 Dashboard",
        "metrics": metrics,
        "urgent_queue": urgent_queue,
        "pending_queue": pending_queue,
        "latest_review_case": latest_review,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/phase-17/triage/create")
async def phase17_create_triage(
    analysis_id: str = Form(...),
    triage_priority: str = Form("HIGH"),
    triage_status: str = Form("open"),
    assigned_doctor: str = Form("AHOS Ophthalmology Doctor"),
    department_unit: str = Form("Ophthalmology Follow-up Clinic"),
    appointment_date: str = Form("2026-07-15 09:30"),
    appointment_status: str = Form("scheduled"),
    patient_contact: str = Form("patient-contact-placeholder"),
    triage_reason: str = Form("Follow-up required due to clinical review decision."),
    follow_up_notes: str = Form("Schedule ophthalmology visit and repeat imaging if clinically needed.")
):
    _phase17_init_db()

    conn = _phase8_conn()

    analysis = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    WHERE analysis_id = ?
    """, (analysis_id,)).fetchone()

    if not analysis:
        conn.close()
        return {
            "status": "not_found",
            "analysis_id": analysis_id
        }

    a = dict(analysis)

    latest_review = conn.execute("""
    SELECT *
    FROM ophthalmology_clinical_reviews
    WHERE analysis_id = ?
    ORDER BY created_at DESC
    LIMIT 1
    """, (analysis_id,)).fetchone()

    review = dict(latest_review) if latest_review else {}

    triage_id = "EYE-TRIAGE-" + _phase8_uuid.uuid4().hex[:10].upper()
    now = datetime.utcnow().isoformat()

    conn.execute("""
    INSERT INTO ophthalmology_triage_queue (
        triage_id, case_id, analysis_id, patient_id,
        triage_priority, triage_status, assigned_doctor, department_unit,
        appointment_date, appointment_status, patient_contact,
        triage_reason, follow_up_notes,
        latest_decision, latest_risk_score, latest_risk_level, safety_gate,
        created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        triage_id,
        a.get("case_id"),
        analysis_id,
        a.get("patient_id"),
        triage_priority,
        triage_status,
        assigned_doctor,
        department_unit,
        appointment_date,
        appointment_status,
        patient_contact,
        triage_reason,
        follow_up_notes,
        review.get("decision", "NO_REVIEW"),
        a.get("risk_score"),
        a.get("risk_level"),
        a.get("safety_gate"),
        now,
        now
    ))

    report_id = "EYE-P17-TRIAGE-" + _phase8_uuid.uuid4().hex[:8].upper()
    conn.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        a.get("case_id"),
        a.get("patient_id"),
        "phase17_triage_appointment_followup",
        a.get("risk_score"),
        a.get("risk_level"),
        "en",
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(
        a.get("case_id"),
        "phase17_triage_created",
        f"{triage_id} priority={triage_priority} appointment_status={appointment_status}"
    )

    return {
        "status": "triage_created",
        "triage_id": triage_id,
        "case_id": a.get("case_id"),
        "analysis_id": analysis_id,
        "patient_id": a.get("patient_id"),
        "triage_priority": triage_priority,
        "triage_status": triage_status,
        "assigned_doctor": assigned_doctor,
        "appointment_date": appointment_date,
        "appointment_status": appointment_status,
        "created_at": now
    }

@router.post("/phase-17/triage/{triage_id}/update")
async def phase17_update_triage(
    triage_id: str,
    triage_priority: str = Form(""),
    triage_status: str = Form(""),
    assigned_doctor: str = Form(""),
    department_unit: str = Form(""),
    appointment_date: str = Form(""),
    appointment_status: str = Form(""),
    patient_contact: str = Form(""),
    triage_reason: str = Form(""),
    follow_up_notes: str = Form("")
):
    _phase17_init_db()
    conn = _phase8_conn()

    row = conn.execute("SELECT * FROM ophthalmology_triage_queue WHERE triage_id=?", (triage_id,)).fetchone()
    if not row:
        conn.close()
        return {
            "status": "not_found",
            "triage_id": triage_id
        }

    current = dict(row)
    now = datetime.utcnow().isoformat()

    updated = {
        "triage_priority": triage_priority or current.get("triage_priority"),
        "triage_status": triage_status or current.get("triage_status"),
        "assigned_doctor": assigned_doctor or current.get("assigned_doctor"),
        "department_unit": department_unit or current.get("department_unit"),
        "appointment_date": appointment_date or current.get("appointment_date"),
        "appointment_status": appointment_status or current.get("appointment_status"),
        "patient_contact": patient_contact or current.get("patient_contact"),
        "triage_reason": triage_reason or current.get("triage_reason"),
        "follow_up_notes": follow_up_notes or current.get("follow_up_notes"),
        "updated_at": now
    }

    conn.execute("""
    UPDATE ophthalmology_triage_queue
    SET triage_priority=?, triage_status=?, assigned_doctor=?, department_unit=?,
        appointment_date=?, appointment_status=?, patient_contact=?,
        triage_reason=?, follow_up_notes=?, updated_at=?
    WHERE triage_id=?
    """, (
        updated["triage_priority"],
        updated["triage_status"],
        updated["assigned_doctor"],
        updated["department_unit"],
        updated["appointment_date"],
        updated["appointment_status"],
        updated["patient_contact"],
        updated["triage_reason"],
        updated["follow_up_notes"],
        updated["updated_at"],
        triage_id
    ))

    conn.commit()
    conn.close()

    return {
        "status": "triage_updated",
        "triage_id": triage_id,
        **updated
    }

@router.delete("/phase-17/triage/{triage_id}")
async def phase17_delete_triage(triage_id: str):
    _phase17_init_db()
    conn = _phase8_conn()

    row = conn.execute("SELECT * FROM ophthalmology_triage_queue WHERE triage_id=?", (triage_id,)).fetchone()
    if not row:
        conn.close()
        return {
            "status": "not_found",
            "triage_id": triage_id
        }

    conn.execute("DELETE FROM ophthalmology_triage_queue WHERE triage_id=?", (triage_id,))
    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "triage_id": triage_id
    }

def _phase17_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 17 - قائمة فرز ومواعيد قسم العيون",
            "summary": "تقرير تشغيلي لقائمة الفرز والمتابعة والمواعيد لقسم العيون.",
            "notice": "هذا التقرير نموذج تجريبي وليس معتمدًا للاستخدام السريري الحقيقي."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 17 - Triage Queue + Appointment Follow-up",
            "summary": "Operational report for ophthalmology triage queue, follow-up appointments and assigned doctors.",
            "notice": "This report is a prototype and is not certified for real clinical use."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 17 - Triagekö + uppföljningsbokning",
            "summary": "Operativ rapport för triagekö, uppföljningsbokningar och ansvariga läkare.",
            "notice": "Denna rapport är en prototyp och inte certifierad för klinisk användning."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 17 - File de triage + rendez-vous de suivi",
            "summary": "Rapport opérationnel pour la file de triage, les rendez-vous de suivi et les médecins assignés.",
            "notice": "Ce rapport est un prototype et n’est pas certifié pour un usage clinique réel."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 17 - Coda triage + appuntamenti follow-up",
            "summary": "Report operativo per coda triage, appuntamenti di follow-up e medici assegnati.",
            "notice": "Questo report è un prototipo e non è certificato per uso clinico reale."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-17/triage-report-html")
async def phase17_triage_report_html(language: str = "en"):
    rows = _phase17_all_triage()
    metrics = _phase17_metrics(rows)
    tx = _phase17_text(language)

    def triage_rows(items):
        out = ""
        for r in items:
            out += f"""
            <tr>
              <td>{r.get('triage_id','')}</td>
              <td>{r.get('case_id','')}</td>
              <td>{r.get('patient_id','')}</td>
              <td>{r.get('triage_priority','')}</td>
              <td>{r.get('triage_status','')}</td>
              <td>{r.get('appointment_date','')}</td>
              <td>{r.get('appointment_status','')}</td>
              <td>{r.get('assigned_doctor','')}</td>
              <td>{r.get('follow_up_notes','')}</td>
            </tr>
            """
        return out

    def dist_rows(items):
        out = ""
        for x in items:
            out += f"<tr><td>{x.get('label')}</td><td>{x.get('value')}</td></tr>"
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Triage KPIs</h2>
<div class="grid">
  <div class="metric">Total Triage<strong>{metrics.get('total_triage_items')}</strong></div>
  <div class="metric">Pending<strong>{metrics.get('pending_appointments')}</strong></div>
  <div class="metric">Scheduled<strong>{metrics.get('scheduled_appointments')}</strong></div>
  <div class="metric">Completed<strong>{metrics.get('completed_appointments')}</strong></div>
  <div class="metric">Missed<strong>{metrics.get('missed_appointments')}</strong></div>
  <div class="metric">Urgent<strong>{metrics.get('urgent_triage')}</strong></div>
  <div class="metric">High Priority<strong>{metrics.get('high_priority_triage')}</strong></div>
</div>

<h2>Priority Distribution</h2>
<table><tr><th>Priority</th><th>Count</th></tr>{dist_rows(metrics.get('priority_distribution', []))}</table>

<h2>Appointment Status Distribution</h2>
<table><tr><th>Status</th><th>Count</th></tr>{dist_rows(metrics.get('appointment_status_distribution', []))}</table>

<h2>Triage Queue</h2>
<table>
<tr>
<th>Triage ID</th><th>Case ID</th><th>Patient ID</th><th>Priority</th><th>Status</th>
<th>Appointment</th><th>Appointment Status</th><th>Doctor</th><th>Notes</th>
</tr>
{triage_rows(rows)}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase17_Triage_Queue_{language}.html"
        }
    )

@router.get("/phase-17/triage-report-pdf")
async def phase17_triage_report_pdf(language: str = "en"):
    rows = _phase17_all_triage()
    metrics = _phase17_metrics(rows)
    tx = _phase17_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 17 Triage Queue + Appointment Follow-up",
        "",
        tx["summary"],
        "",
        "Triage KPIs:",
        f"- Total Triage Items: {metrics.get('total_triage_items')}",
        f"- Pending Appointments: {metrics.get('pending_appointments')}",
        f"- Scheduled Appointments: {metrics.get('scheduled_appointments')}",
        f"- Completed Appointments: {metrics.get('completed_appointments')}",
        f"- Missed Appointments: {metrics.get('missed_appointments')}",
        f"- Urgent Triage: {metrics.get('urgent_triage')}",
        f"- High Priority Triage: {metrics.get('high_priority_triage')}",
        "",
        "Triage Queue:"
    ]

    for i, r in enumerate(rows, start=1):
        lines += [
            f"{i}. Triage: {r.get('triage_id')}",
            f"   Case: {r.get('case_id')}",
            f"   Patient: {r.get('patient_id')}",
            f"   Priority: {r.get('triage_priority')}",
            f"   Triage Status: {r.get('triage_status')}",
            f"   Appointment: {r.get('appointment_date')} / {r.get('appointment_status')}",
            f"   Doctor: {r.get('assigned_doctor')}",
            f"   Reason: {r.get('triage_reason')}",
            f"   Notes: {r.get('follow_up_notes')}",
            ""
        ]

    lines += [
        "Clinical Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase17_Triage_Queue_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 18
# Patient Notification + Follow-up Communication Center
# ============================

def _phase18_init_db():
    _phase17_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_patient_communications (
        communication_id TEXT PRIMARY KEY,
        triage_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        patient_contact TEXT,
        channel TEXT,
        message_type TEXT,
        message_language TEXT,
        message_subject TEXT,
        message_body TEXT,
        communication_status TEXT,
        patient_confirmation TEXT,
        confirmation_note TEXT,
        scheduled_send_at TEXT,
        sent_at TEXT,
        created_by TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase18_all_communications():
    _phase18_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_patient_communications
    ORDER BY created_at DESC
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]

def _phase18_latest_triage():
    _phase18_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_triage_queue
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

def _phase18_filtered_communications(
    search: str = "",
    channel: str = "",
    status: str = "",
    confirmation: str = "",
    language: str = ""
):
    rows = _phase18_all_communications()

    def ok(row):
        if search:
            s = search.lower()
            blob = " ".join([
                str(row.get("communication_id", "")),
                str(row.get("triage_id", "")),
                str(row.get("case_id", "")),
                str(row.get("analysis_id", "")),
                str(row.get("patient_id", "")),
                str(row.get("patient_contact", "")),
                str(row.get("channel", "")),
                str(row.get("communication_status", "")),
                str(row.get("patient_confirmation", "")),
                str(row.get("message_body", "")),
            ]).lower()
            if s not in blob:
                return False

        if channel and str(row.get("channel", "")).lower() != channel.lower():
            return False

        if status and str(row.get("communication_status", "")).lower() != status.lower():
            return False

        if confirmation and str(row.get("patient_confirmation", "")).lower() != confirmation.lower():
            return False

        if language and str(row.get("message_language", "")).lower() != language.lower():
            return False

        return True

    return [r for r in rows if ok(r)]

def _phase18_metrics(rows):
    def count_by(key):
        out = {}
        for r in rows:
            v = r.get(key) or "NONE"
            out[v] = out.get(v, 0) + 1
        return [{"label": k, "value": v} for k, v in sorted(out.items())]

    total = len(rows)
    pending = sum(1 for r in rows if str(r.get("communication_status","")).lower() == "pending")
    sent = sum(1 for r in rows if str(r.get("communication_status","")).lower() == "sent")
    failed = sum(1 for r in rows if str(r.get("communication_status","")).lower() == "failed")
    confirmed = sum(1 for r in rows if str(r.get("patient_confirmation","")).lower() == "confirmed")
    not_confirmed = sum(1 for r in rows if str(r.get("patient_confirmation","")).lower() in ["pending", "not_confirmed", ""])

    return {
        "total_communications": total,
        "pending_messages": pending,
        "sent_messages": sent,
        "failed_messages": failed,
        "confirmed_patients": confirmed,
        "not_confirmed_patients": not_confirmed,
        "channel_distribution": count_by("channel"),
        "status_distribution": count_by("communication_status"),
        "confirmation_distribution": count_by("patient_confirmation"),
        "language_distribution": count_by("message_language")
    }

def _phase18_template(channel: str, language: str, patient_id: str, appointment_date: str, doctor: str):
    lang = (language or "en").lower()
    ch = (channel or "sms").lower()

    data = {
        "ar": {
            "subject": "تذكير بموعد متابعة العيون",
            "body": f"مرحبًا، لديك موعد متابعة في قسم العيون بتاريخ {appointment_date} مع {doctor}. الرجاء تأكيد الحضور. رقم المريض: {patient_id}."
        },
        "en": {
            "subject": "Ophthalmology follow-up appointment reminder",
            "body": f"Hello, you have an ophthalmology follow-up appointment on {appointment_date} with {doctor}. Please confirm attendance. Patient ID: {patient_id}."
        },
        "sv": {
            "subject": "Påminnelse om uppföljning hos ögonmottagningen",
            "body": f"Hej, du har en uppföljningstid hos ögonmottagningen {appointment_date} med {doctor}. Vänligen bekräfta din närvaro. Patient-ID: {patient_id}."
        },
        "fr": {
            "subject": "Rappel de rendez-vous ophtalmologie",
            "body": f"Bonjour, vous avez un rendez-vous de suivi en ophtalmologie le {appointment_date} avec {doctor}. Veuillez confirmer votre présence. ID patient: {patient_id}."
        },
        "it": {
            "subject": "Promemoria appuntamento oftalmologia",
            "body": f"Salve, ha un appuntamento di follow-up oftalmologico il {appointment_date} con {doctor}. Confermi la presenza. ID paziente: {patient_id}."
        }
    }

    tx = data.get(lang, data["en"])

    if ch == "whatsapp":
        tx["body"] = "[WhatsApp] " + tx["body"]
    elif ch == "email":
        tx["body"] = tx["body"] + "\n\nThis is a prototype communication generated by AHOS."
    else:
        tx["body"] = "[SMS] " + tx["body"]

    return tx

@router.get("/phase-18/status")
async def phase18_status():
    _phase18_init_db()
    conn = _phase8_conn()

    total_triage = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_triage_queue").fetchone()["c"]
    total_communications = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_patient_communications").fetchone()["c"]

    latest = conn.execute("""
    SELECT communication_id, triage_id, patient_id, channel, communication_status,
           patient_confirmation, message_language, created_at
    FROM ophthalmology_patient_communications
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    rows = _phase18_all_communications()
    metrics = _phase18_metrics(rows)

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 18",
        "features": [
            "patient_notification_center",
            "follow_up_communication_center",
            "sms_template",
            "email_template",
            "whatsapp_template",
            "appointment_reminder",
            "communication_status_tracking",
            "patient_confirmation",
            "sqlite_communication_storage",
            "communication_timeline",
            "communication_html_report",
            "communication_pdf_report",
            "multilingual_patient_messages"
        ],
        "total_triage_items": total_triage,
        "total_communications": total_communications,
        "latest_communication": dict(latest) if latest else None,
        "communication_metrics": metrics,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-18/dashboard")
async def phase18_dashboard():
    rows = _phase18_all_communications()
    metrics = _phase18_metrics(rows)
    latest_triage = _phase18_latest_triage()

    pending = [r for r in rows if str(r.get("communication_status","")).lower() == "pending"][:10]
    sent = [r for r in rows if str(r.get("communication_status","")).lower() == "sent"][:10]
    confirmed = [r for r in rows if str(r.get("patient_confirmation","")).lower() == "confirmed"][:10]

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 18 Dashboard",
        "metrics": metrics,
        "latest_triage": latest_triage,
        "pending_messages": pending,
        "sent_messages": sent,
        "confirmed_patients": confirmed,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-18/communications")
async def phase18_communications(
    search: str = Query(""),
    channel: str = Query(""),
    status: str = Query(""),
    confirmation: str = Query(""),
    language: str = Query("")
):
    rows = _phase18_filtered_communications(search, channel, status, confirmation, language)
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 18 Communications",
        "filters": {
            "search": search,
            "channel": channel,
            "status": status,
            "confirmation": confirmation,
            "language": language
        },
        "total_communications": len(rows),
        "communications": rows
    }

@router.post("/phase-18/communications/create")
async def phase18_create_communication(
    triage_id: str = Form(...),
    channel: str = Form("sms"),
    message_type: str = Form("appointment_reminder"),
    message_language: str = Form("en"),
    message_subject: str = Form(""),
    message_body: str = Form(""),
    communication_status: str = Form("pending"),
    patient_confirmation: str = Form("pending"),
    confirmation_note: str = Form("Awaiting patient confirmation."),
    scheduled_send_at: str = Form("2026-07-14 09:00"),
    created_by: str = Form("AHOS Communication Center")
):
    _phase18_init_db()
    conn = _phase8_conn()

    triage = conn.execute("""
    SELECT *
    FROM ophthalmology_triage_queue
    WHERE triage_id = ?
    """, (triage_id,)).fetchone()

    if not triage:
        conn.close()
        return {
            "status": "not_found",
            "triage_id": triage_id
        }

    tr = dict(triage)

    if not message_subject or not message_body:
        template = _phase18_template(
            channel,
            message_language,
            tr.get("patient_id"),
            tr.get("appointment_date"),
            tr.get("assigned_doctor")
        )
        message_subject = message_subject or template["subject"]
        message_body = message_body or template["body"]

    communication_id = "EYE-COMM-" + _phase8_uuid.uuid4().hex[:10].upper()
    now = datetime.utcnow().isoformat()
    sent_at = now if communication_status == "sent" else ""

    conn.execute("""
    INSERT INTO ophthalmology_patient_communications (
        communication_id, triage_id, case_id, analysis_id, patient_id, patient_contact,
        channel, message_type, message_language, message_subject, message_body,
        communication_status, patient_confirmation, confirmation_note,
        scheduled_send_at, sent_at, created_by, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        communication_id,
        triage_id,
        tr.get("case_id"),
        tr.get("analysis_id"),
        tr.get("patient_id"),
        tr.get("patient_contact"),
        channel,
        message_type,
        message_language,
        message_subject,
        message_body,
        communication_status,
        patient_confirmation,
        confirmation_note,
        scheduled_send_at,
        sent_at,
        created_by,
        now,
        now
    ))

    report_id = "EYE-P18-COMM-" + _phase8_uuid.uuid4().hex[:8].upper()
    conn.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        tr.get("case_id"),
        tr.get("patient_id"),
        "phase18_patient_communication",
        tr.get("latest_risk_score"),
        tr.get("latest_risk_level"),
        message_language,
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(
        tr.get("case_id"),
        "phase18_patient_communication_created",
        f"{communication_id} channel={channel} status={communication_status}"
    )

    return {
        "status": "communication_created",
        "communication_id": communication_id,
        "triage_id": triage_id,
        "case_id": tr.get("case_id"),
        "analysis_id": tr.get("analysis_id"),
        "patient_id": tr.get("patient_id"),
        "channel": channel,
        "message_type": message_type,
        "message_language": message_language,
        "communication_status": communication_status,
        "patient_confirmation": patient_confirmation,
        "message_subject": message_subject,
        "message_body": message_body,
        "created_at": now
    }

@router.post("/phase-18/communications/{communication_id}/update")
async def phase18_update_communication(
    communication_id: str,
    communication_status: str = Form(""),
    patient_confirmation: str = Form(""),
    confirmation_note: str = Form(""),
    message_body: str = Form("")
):
    _phase18_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_patient_communications
    WHERE communication_id = ?
    """, (communication_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "communication_id": communication_id
        }

    current = dict(row)
    now = datetime.utcnow().isoformat()

    new_status = communication_status or current.get("communication_status")
    sent_at = current.get("sent_at") or ""
    if new_status == "sent" and not sent_at:
        sent_at = now

    conn.execute("""
    UPDATE ophthalmology_patient_communications
    SET communication_status=?,
        patient_confirmation=?,
        confirmation_note=?,
        message_body=?,
        sent_at=?,
        updated_at=?
    WHERE communication_id=?
    """, (
        new_status,
        patient_confirmation or current.get("patient_confirmation"),
        confirmation_note or current.get("confirmation_note"),
        message_body or current.get("message_body"),
        sent_at,
        now,
        communication_id
    ))

    conn.commit()
    conn.close()

    return {
        "status": "communication_updated",
        "communication_id": communication_id,
        "communication_status": new_status,
        "patient_confirmation": patient_confirmation or current.get("patient_confirmation"),
        "updated_at": now
    }

@router.delete("/phase-18/communications/{communication_id}")
async def phase18_delete_communication(communication_id: str):
    _phase18_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_patient_communications
    WHERE communication_id = ?
    """, (communication_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "communication_id": communication_id
        }

    conn.execute("DELETE FROM ophthalmology_patient_communications WHERE communication_id=?", (communication_id,))
    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "communication_id": communication_id
    }

def _phase18_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 18 - مركز تواصل المريض والمتابعة",
            "summary": "تقرير مركز التواصل مع المريض لتذكير الموعد وتأكيد الحضور ومتابعة حالة الرسائل.",
            "notice": "هذا التقرير نموذج تجريبي وليس نظام إرسال حقيقي أو معتمد سريريًا."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 18 - Patient Communication Center",
            "summary": "Communication center report for appointment reminders, patient confirmation and message tracking.",
            "notice": "This report is a prototype and not a real certified messaging system."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 18 - Patientkommunikationscenter",
            "summary": "Rapport för bokningspåminnelser, patientbekräftelse och meddelandestatus.",
            "notice": "Denna rapport är en prototyp och inte ett certifierat meddelandesystem."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 18 - Centre de communication patient",
            "summary": "Rapport pour rappels de rendez-vous, confirmation patient et suivi des messages.",
            "notice": "Ce rapport est un prototype et non un système de messagerie certifié réel."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 18 - Centro comunicazioni paziente",
            "summary": "Report per promemoria appuntamenti, conferma paziente e tracciamento messaggi.",
            "notice": "Questo report è un prototipo e non un sistema di messaggistica certificato reale."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-18/communication-report-html")
async def phase18_communication_report_html(language: str = "en"):
    rows = _phase18_all_communications()
    metrics = _phase18_metrics(rows)
    tx = _phase18_text(language)

    def comm_rows(items):
        out = ""
        for r in items:
            out += f"""
            <tr>
              <td>{r.get('communication_id','')}</td>
              <td>{r.get('triage_id','')}</td>
              <td>{r.get('patient_id','')}</td>
              <td>{r.get('channel','')}</td>
              <td>{r.get('message_language','')}</td>
              <td>{r.get('communication_status','')}</td>
              <td>{r.get('patient_confirmation','')}</td>
              <td>{r.get('scheduled_send_at','')}</td>
              <td>{r.get('message_body','')}</td>
            </tr>
            """
        return out

    def dist_rows(items):
        out = ""
        for x in items:
            out += f"<tr><td>{x.get('label')}</td><td>{x.get('value')}</td></tr>"
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Communication KPIs</h2>
<div class="grid">
  <div class="metric">Total Communications<strong>{metrics.get('total_communications')}</strong></div>
  <div class="metric">Pending<strong>{metrics.get('pending_messages')}</strong></div>
  <div class="metric">Sent<strong>{metrics.get('sent_messages')}</strong></div>
  <div class="metric">Failed<strong>{metrics.get('failed_messages')}</strong></div>
  <div class="metric">Confirmed Patients<strong>{metrics.get('confirmed_patients')}</strong></div>
  <div class="metric">Not Confirmed<strong>{metrics.get('not_confirmed_patients')}</strong></div>
</div>

<h2>Channel Distribution</h2>
<table><tr><th>Channel</th><th>Count</th></tr>{dist_rows(metrics.get('channel_distribution', []))}</table>

<h2>Status Distribution</h2>
<table><tr><th>Status</th><th>Count</th></tr>{dist_rows(metrics.get('status_distribution', []))}</table>

<h2>Communication Timeline</h2>
<table>
<tr>
<th>Communication ID</th><th>Triage ID</th><th>Patient</th><th>Channel</th><th>Language</th>
<th>Status</th><th>Confirmation</th><th>Scheduled</th><th>Message</th>
</tr>
{comm_rows(rows)}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase18_Patient_Communication_{language}.html"
        }
    )

@router.get("/phase-18/communication-report-pdf")
async def phase18_communication_report_pdf(language: str = "en"):
    rows = _phase18_all_communications()
    metrics = _phase18_metrics(rows)
    tx = _phase18_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 18 Patient Notification + Follow-up Communication Center",
        "",
        tx["summary"],
        "",
        "Communication KPIs:",
        f"- Total Communications: {metrics.get('total_communications')}",
        f"- Pending Messages: {metrics.get('pending_messages')}",
        f"- Sent Messages: {metrics.get('sent_messages')}",
        f"- Failed Messages: {metrics.get('failed_messages')}",
        f"- Confirmed Patients: {metrics.get('confirmed_patients')}",
        f"- Not Confirmed Patients: {metrics.get('not_confirmed_patients')}",
        "",
        "Communication Timeline:"
    ]

    for i, r in enumerate(rows, start=1):
        lines += [
            f"{i}. Communication: {r.get('communication_id')}",
            f"   Triage: {r.get('triage_id')}",
            f"   Patient: {r.get('patient_id')}",
            f"   Channel: {r.get('channel')} / Language: {r.get('message_language')}",
            f"   Status: {r.get('communication_status')}",
            f"   Confirmation: {r.get('patient_confirmation')}",
            f"   Scheduled: {r.get('scheduled_send_at')}",
            f"   Subject: {r.get('message_subject')}",
            f"   Message: {r.get('message_body')}",
            ""
        ]

    lines += [
        "Communication Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase18_Patient_Communication_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 19
# Patient Confirmation + Attendance Outcome + No-Show Management
# ============================

def _phase19_init_db():
    _phase18_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_attendance_outcomes (
        attendance_id TEXT PRIMARY KEY,
        communication_id TEXT,
        triage_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        patient_confirmation TEXT,
        attendance_status TEXT,
        appointment_status TEXT,
        outcome_type TEXT,
        absence_reason TEXT,
        reschedule_date TEXT,
        reschedule_required TEXT,
        doctor_note TEXT,
        admin_note TEXT,
        updated_by TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase19_latest_communication():
    _phase19_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_patient_communications
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

def _phase19_all_attendance():
    _phase19_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_attendance_outcomes
    ORDER BY created_at DESC
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]

def _phase19_filtered_attendance(
    search: str = "",
    confirmation: str = "",
    attendance_status: str = "",
    appointment_status: str = "",
    outcome_type: str = ""
):
    rows = _phase19_all_attendance()

    def ok(row):
        if search:
            s = search.lower()
            blob = " ".join([
                str(row.get("attendance_id", "")),
                str(row.get("communication_id", "")),
                str(row.get("triage_id", "")),
                str(row.get("case_id", "")),
                str(row.get("patient_id", "")),
                str(row.get("patient_confirmation", "")),
                str(row.get("attendance_status", "")),
                str(row.get("appointment_status", "")),
                str(row.get("outcome_type", "")),
                str(row.get("absence_reason", "")),
                str(row.get("doctor_note", "")),
            ]).lower()
            if s not in blob:
                return False

        if confirmation and str(row.get("patient_confirmation","")).lower() != confirmation.lower():
            return False

        if attendance_status and str(row.get("attendance_status","")).lower() != attendance_status.lower():
            return False

        if appointment_status and str(row.get("appointment_status","")).lower() != appointment_status.lower():
            return False

        if outcome_type and str(row.get("outcome_type","")).lower() != outcome_type.lower():
            return False

        return True

    return [r for r in rows if ok(r)]

def _phase19_metrics(rows):
    def count_by(key):
        out = {}
        for r in rows:
            v = r.get(key) or "NONE"
            out[v] = out.get(v, 0) + 1
        return [{"label": k, "value": v} for k, v in sorted(out.items())]

    total = len(rows)
    confirmed = sum(1 for r in rows if str(r.get("patient_confirmation","")).lower() == "confirmed")
    declined = sum(1 for r in rows if str(r.get("patient_confirmation","")).lower() == "declined")
    no_response = sum(1 for r in rows if str(r.get("patient_confirmation","")).lower() == "no_response")
    attended = sum(1 for r in rows if str(r.get("attendance_status","")).lower() == "attended")
    no_show = sum(1 for r in rows if str(r.get("attendance_status","")).lower() == "no_show")
    rescheduled = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "rescheduled")
    completed = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "completed")
    missed = sum(1 for r in rows if str(r.get("appointment_status","")).lower() == "missed")

    return {
        "total_attendance_outcomes": total,
        "confirmed_patients": confirmed,
        "declined_patients": declined,
        "no_response_patients": no_response,
        "attended_patients": attended,
        "no_show_patients": no_show,
        "rescheduled_appointments": rescheduled,
        "completed_appointments": completed,
        "missed_appointments": missed,
        "confirmation_distribution": count_by("patient_confirmation"),
        "attendance_distribution": count_by("attendance_status"),
        "appointment_status_distribution": count_by("appointment_status"),
        "outcome_type_distribution": count_by("outcome_type")
    }

@router.get("/phase-19/status")
async def phase19_status():
    _phase19_init_db()
    conn = _phase8_conn()

    total_triage = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_triage_queue").fetchone()["c"]
    total_communications = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_patient_communications").fetchone()["c"]
    total_attendance = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_attendance_outcomes").fetchone()["c"]

    latest = conn.execute("""
    SELECT attendance_id, communication_id, triage_id, patient_id,
           patient_confirmation, attendance_status, appointment_status,
           outcome_type, created_at
    FROM ophthalmology_attendance_outcomes
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()

    rows = _phase19_all_attendance()
    metrics = _phase19_metrics(rows)

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 19",
        "features": [
            "patient_confirmation_management",
            "attendance_outcome_tracking",
            "no_show_management",
            "reschedule_appointment",
            "absence_reason",
            "attendance_timeline",
            "sync_patient_confirmation_to_phase18",
            "sync_appointment_status_to_phase17",
            "sqlite_attendance_storage",
            "no_show_dashboard",
            "attendance_html_report",
            "attendance_pdf_report",
            "multilingual_attendance_center"
        ],
        "total_triage_items": total_triage,
        "total_communications": total_communications,
        "total_attendance_outcomes": total_attendance,
        "latest_attendance": dict(latest) if latest else None,
        "attendance_metrics": metrics,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-19/dashboard")
async def phase19_dashboard():
    rows = _phase19_all_attendance()
    metrics = _phase19_metrics(rows)
    latest_communication = _phase19_latest_communication()

    no_show_queue = [
        r for r in rows
        if str(r.get("attendance_status","")).lower() == "no_show"
    ][:10]

    reschedule_queue = [
        r for r in rows
        if str(r.get("appointment_status","")).lower() == "rescheduled"
        or str(r.get("reschedule_required","")).lower() == "yes"
    ][:10]

    confirmed_queue = [
        r for r in rows
        if str(r.get("patient_confirmation","")).lower() == "confirmed"
    ][:10]

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 19 Dashboard",
        "metrics": metrics,
        "latest_communication": latest_communication,
        "no_show_queue": no_show_queue,
        "reschedule_queue": reschedule_queue,
        "confirmed_queue": confirmed_queue,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-19/attendance")
async def phase19_attendance(
    search: str = Query(""),
    confirmation: str = Query(""),
    attendance_status: str = Query(""),
    appointment_status: str = Query(""),
    outcome_type: str = Query("")
):
    rows = _phase19_filtered_attendance(
        search,
        confirmation,
        attendance_status,
        appointment_status,
        outcome_type
    )

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 19 Attendance",
        "filters": {
            "search": search,
            "confirmation": confirmation,
            "attendance_status": attendance_status,
            "appointment_status": appointment_status,
            "outcome_type": outcome_type
        },
        "total_attendance_outcomes": len(rows),
        "attendance": rows
    }

@router.post("/phase-19/attendance/create")
async def phase19_create_attendance(
    communication_id: str = Form(...),
    patient_confirmation: str = Form("confirmed"),
    attendance_status: str = Form("attended"),
    appointment_status: str = Form("completed"),
    outcome_type: str = Form("attendance_completed"),
    absence_reason: str = Form(""),
    reschedule_date: str = Form(""),
    reschedule_required: str = Form("no"),
    doctor_note: str = Form("Patient attendance outcome recorded."),
    admin_note: str = Form("Updated by AHOS Phase 19 attendance workflow."),
    updated_by: str = Form("AHOS Attendance Center")
):
    _phase19_init_db()
    conn = _phase8_conn()

    comm = conn.execute("""
    SELECT *
    FROM ophthalmology_patient_communications
    WHERE communication_id = ?
    """, (communication_id,)).fetchone()

    if not comm:
        conn.close()
        return {
            "status": "not_found",
            "communication_id": communication_id
        }

    c = dict(comm)
    triage_id = c.get("triage_id")

    attendance_id = "EYE-ATT-" + _phase8_uuid.uuid4().hex[:10].upper()
    now = datetime.utcnow().isoformat()

    conn.execute("""
    INSERT INTO ophthalmology_attendance_outcomes (
        attendance_id, communication_id, triage_id, case_id, analysis_id, patient_id,
        patient_confirmation, attendance_status, appointment_status, outcome_type,
        absence_reason, reschedule_date, reschedule_required,
        doctor_note, admin_note, updated_by, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        attendance_id,
        communication_id,
        triage_id,
        c.get("case_id"),
        c.get("analysis_id"),
        c.get("patient_id"),
        patient_confirmation,
        attendance_status,
        appointment_status,
        outcome_type,
        absence_reason,
        reschedule_date,
        reschedule_required,
        doctor_note,
        admin_note,
        updated_by,
        now,
        now
    ))

    # Sync Phase 18 patient confirmation
    conn.execute("""
    UPDATE ophthalmology_patient_communications
    SET patient_confirmation=?,
        confirmation_note=?,
        updated_at=?
    WHERE communication_id=?
    """, (
        patient_confirmation,
        doctor_note,
        now,
        communication_id
    ))

    # Sync Phase 17 appointment status
    conn.execute("""
    UPDATE ophthalmology_triage_queue
    SET appointment_status=?,
        triage_status=?,
        follow_up_notes=?,
        appointment_date=CASE
          WHEN ? != '' THEN ?
          ELSE appointment_date
        END,
        updated_at=?
    WHERE triage_id=?
    """, (
        appointment_status,
        "closed" if appointment_status == "completed" else "open",
        doctor_note,
        reschedule_date,
        reschedule_date,
        now,
        triage_id
    ))

    report_id = "EYE-P19-ATT-" + _phase8_uuid.uuid4().hex[:8].upper()
    conn.execute("""
    INSERT INTO ophthalmology_reports (
        report_id, case_id, patient_id, report_type, risk_score, risk_level, language, created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        c.get("case_id"),
        c.get("patient_id"),
        "phase19_attendance_outcome_noshow",
        0,
        outcome_type,
        "en",
        now
    ))

    conn.commit()
    conn.close()

    _phase8_log(
        c.get("case_id"),
        "phase19_attendance_outcome_created",
        f"{attendance_id} confirmation={patient_confirmation} attendance={attendance_status} appointment={appointment_status}"
    )

    return {
        "status": "attendance_created",
        "attendance_id": attendance_id,
        "communication_id": communication_id,
        "triage_id": triage_id,
        "case_id": c.get("case_id"),
        "analysis_id": c.get("analysis_id"),
        "patient_id": c.get("patient_id"),
        "patient_confirmation": patient_confirmation,
        "attendance_status": attendance_status,
        "appointment_status": appointment_status,
        "outcome_type": outcome_type,
        "reschedule_required": reschedule_required,
        "reschedule_date": reschedule_date,
        "created_at": now
    }

@router.post("/phase-19/attendance/{attendance_id}/update")
async def phase19_update_attendance(
    attendance_id: str,
    patient_confirmation: str = Form(""),
    attendance_status: str = Form(""),
    appointment_status: str = Form(""),
    outcome_type: str = Form(""),
    absence_reason: str = Form(""),
    reschedule_date: str = Form(""),
    reschedule_required: str = Form(""),
    doctor_note: str = Form(""),
    admin_note: str = Form(""),
    updated_by: str = Form("AHOS Attendance Center")
):
    _phase19_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_attendance_outcomes
    WHERE attendance_id = ?
    """, (attendance_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "attendance_id": attendance_id
        }

    current = dict(row)
    now = datetime.utcnow().isoformat()

    updated = {
        "patient_confirmation": patient_confirmation or current.get("patient_confirmation"),
        "attendance_status": attendance_status or current.get("attendance_status"),
        "appointment_status": appointment_status or current.get("appointment_status"),
        "outcome_type": outcome_type or current.get("outcome_type"),
        "absence_reason": absence_reason or current.get("absence_reason"),
        "reschedule_date": reschedule_date or current.get("reschedule_date"),
        "reschedule_required": reschedule_required or current.get("reschedule_required"),
        "doctor_note": doctor_note or current.get("doctor_note"),
        "admin_note": admin_note or current.get("admin_note"),
        "updated_by": updated_by,
        "updated_at": now
    }

    conn.execute("""
    UPDATE ophthalmology_attendance_outcomes
    SET patient_confirmation=?,
        attendance_status=?,
        appointment_status=?,
        outcome_type=?,
        absence_reason=?,
        reschedule_date=?,
        reschedule_required=?,
        doctor_note=?,
        admin_note=?,
        updated_by=?,
        updated_at=?
    WHERE attendance_id=?
    """, (
        updated["patient_confirmation"],
        updated["attendance_status"],
        updated["appointment_status"],
        updated["outcome_type"],
        updated["absence_reason"],
        updated["reschedule_date"],
        updated["reschedule_required"],
        updated["doctor_note"],
        updated["admin_note"],
        updated["updated_by"],
        updated["updated_at"],
        attendance_id
    ))

    conn.execute("""
    UPDATE ophthalmology_patient_communications
    SET patient_confirmation=?,
        confirmation_note=?,
        updated_at=?
    WHERE communication_id=?
    """, (
        updated["patient_confirmation"],
        updated["doctor_note"],
        now,
        current.get("communication_id")
    ))

    conn.execute("""
    UPDATE ophthalmology_triage_queue
    SET appointment_status=?,
        triage_status=?,
        follow_up_notes=?,
        appointment_date=CASE
          WHEN ? != '' THEN ?
          ELSE appointment_date
        END,
        updated_at=?
    WHERE triage_id=?
    """, (
        updated["appointment_status"],
        "closed" if updated["appointment_status"] == "completed" else "open",
        updated["doctor_note"],
        updated["reschedule_date"],
        updated["reschedule_date"],
        now,
        current.get("triage_id")
    ))

    conn.commit()
    conn.close()

    return {
        "status": "attendance_updated",
        "attendance_id": attendance_id,
        **updated
    }

@router.delete("/phase-19/attendance/{attendance_id}")
async def phase19_delete_attendance(attendance_id: str):
    _phase19_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_attendance_outcomes
    WHERE attendance_id=?
    """, (attendance_id,)).fetchone()

    if not row:
        conn.close()
        return {
            "status": "not_found",
            "attendance_id": attendance_id
        }

    conn.execute("DELETE FROM ophthalmology_attendance_outcomes WHERE attendance_id=?", (attendance_id,))
    conn.commit()
    conn.close()

    return {
        "status": "deleted",
        "attendance_id": attendance_id
    }

def _phase19_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 19 - تأكيد الحضور وإدارة عدم الحضور",
            "summary": "تقرير متابعة تأكيد المريض، نتيجة الحضور، عدم الحضور، وإعادة جدولة الموعد.",
            "notice": "هذا التقرير نموذج تجريبي وليس نظام متابعة سريري معتمد."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 19 - Attendance Outcome + No-Show Management",
            "summary": "Report for patient confirmation, attendance outcome, no-show tracking and appointment rescheduling.",
            "notice": "This report is a prototype and not a certified clinical attendance system."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 19 - Närvaro och uteblivet besök",
            "summary": "Rapport för patientbekräftelse, närvaro, uteblivet besök och ombokning.",
            "notice": "Denna rapport är en prototyp och inte ett certifierat kliniskt system."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 19 - Présence et absence patient",
            "summary": "Rapport de confirmation patient, présence, absence et reprogrammation.",
            "notice": "Ce rapport est un prototype et non un système clinique certifié."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 19 - Presenza e no-show",
            "summary": "Report per conferma paziente, presenza, no-show e riprogrammazione.",
            "notice": "Questo report è un prototipo e non un sistema clinico certificato."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-19/attendance-report-html")
async def phase19_attendance_report_html(language: str = "en"):
    rows = _phase19_all_attendance()
    metrics = _phase19_metrics(rows)
    tx = _phase19_text(language)

    def outcome_rows(items):
        out = ""
        for r in items:
            out += f"""
            <tr>
              <td>{r.get('attendance_id','')}</td>
              <td>{r.get('communication_id','')}</td>
              <td>{r.get('triage_id','')}</td>
              <td>{r.get('patient_id','')}</td>
              <td>{r.get('patient_confirmation','')}</td>
              <td>{r.get('attendance_status','')}</td>
              <td>{r.get('appointment_status','')}</td>
              <td>{r.get('outcome_type','')}</td>
              <td>{r.get('absence_reason','')}</td>
              <td>{r.get('reschedule_date','')}</td>
              <td>{r.get('doctor_note','')}</td>
            </tr>
            """
        return out

    def dist_rows(items):
        out = ""
        for x in items:
            out += f"<tr><td>{x.get('label')}</td><td>{x.get('value')}</td></tr>"
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Attendance KPIs</h2>
<div class="grid">
  <div class="metric">Total Outcomes<strong>{metrics.get('total_attendance_outcomes')}</strong></div>
  <div class="metric">Confirmed<strong>{metrics.get('confirmed_patients')}</strong></div>
  <div class="metric">Declined<strong>{metrics.get('declined_patients')}</strong></div>
  <div class="metric">No Response<strong>{metrics.get('no_response_patients')}</strong></div>
  <div class="metric">Attended<strong>{metrics.get('attended_patients')}</strong></div>
  <div class="metric">No-Show<strong>{metrics.get('no_show_patients')}</strong></div>
  <div class="metric">Rescheduled<strong>{metrics.get('rescheduled_appointments')}</strong></div>
  <div class="metric">Completed<strong>{metrics.get('completed_appointments')}</strong></div>
  <div class="metric">Missed<strong>{metrics.get('missed_appointments')}</strong></div>
</div>

<h2>Confirmation Distribution</h2>
<table><tr><th>Confirmation</th><th>Count</th></tr>{dist_rows(metrics.get('confirmation_distribution', []))}</table>

<h2>Attendance Distribution</h2>
<table><tr><th>Attendance</th><th>Count</th></tr>{dist_rows(metrics.get('attendance_distribution', []))}</table>

<h2>Attendance Timeline</h2>
<table>
<tr>
<th>Attendance ID</th><th>Communication ID</th><th>Triage ID</th><th>Patient</th>
<th>Confirmation</th><th>Attendance</th><th>Appointment</th><th>Outcome</th>
<th>Absence Reason</th><th>Reschedule</th><th>Doctor Note</th>
</tr>
{outcome_rows(rows)}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase19_Attendance_Outcome_{language}.html"
        }
    )

@router.get("/phase-19/attendance-report-pdf")
async def phase19_attendance_report_pdf(language: str = "en"):
    rows = _phase19_all_attendance()
    metrics = _phase19_metrics(rows)
    tx = _phase19_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 19 Patient Confirmation + Attendance Outcome + No-Show Management",
        "",
        tx["summary"],
        "",
        "Attendance KPIs:",
        f"- Total Outcomes: {metrics.get('total_attendance_outcomes')}",
        f"- Confirmed Patients: {metrics.get('confirmed_patients')}",
        f"- Declined Patients: {metrics.get('declined_patients')}",
        f"- No Response Patients: {metrics.get('no_response_patients')}",
        f"- Attended Patients: {metrics.get('attended_patients')}",
        f"- No-Show Patients: {metrics.get('no_show_patients')}",
        f"- Rescheduled Appointments: {metrics.get('rescheduled_appointments')}",
        f"- Completed Appointments: {metrics.get('completed_appointments')}",
        f"- Missed Appointments: {metrics.get('missed_appointments')}",
        "",
        "Attendance Timeline:"
    ]

    for i, r in enumerate(rows, start=1):
        lines += [
            f"{i}. Attendance: {r.get('attendance_id')}",
            f"   Communication: {r.get('communication_id')}",
            f"   Triage: {r.get('triage_id')}",
            f"   Patient: {r.get('patient_id')}",
            f"   Confirmation: {r.get('patient_confirmation')}",
            f"   Attendance: {r.get('attendance_status')}",
            f"   Appointment: {r.get('appointment_status')}",
            f"   Outcome: {r.get('outcome_type')}",
            f"   Absence Reason: {r.get('absence_reason')}",
            f"   Reschedule: {r.get('reschedule_date')}",
            f"   Doctor Note: {r.get('doctor_note')}",
            ""
        ]

    lines += [
        "Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase19_Attendance_Outcome_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 20
# Operational Closed-Loop Care Pathway
# ============================

def _phase20_init_db():
    _phase19_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_closed_loop_pathways (
        pathway_id TEXT PRIMARY KEY,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        completion_score INTEGER,
        pathway_status TEXT,
        final_operational_status TEXT,
        case_created INTEGER,
        ai_analysis_done INTEGER,
        viewer_ready INTEGER,
        annotation_done INTEGER,
        review_done INTEGER,
        dossier_done INTEGER,
        triage_done INTEGER,
        communication_done INTEGER,
        attendance_done INTEGER,
        final_summary TEXT,
        clinical_status TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase20_latest_full_case():
    _phase20_init_db()
    conn = _phase8_conn()

    analysis = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()

    if not analysis:
        conn.close()
        return None

    a = dict(analysis)
    case_id = a.get("case_id")
    analysis_id = a.get("analysis_id")

    case = conn.execute("SELECT * FROM ophthalmology_cases WHERE case_id=?", (case_id,)).fetchone()
    annotations = conn.execute("SELECT * FROM ophthalmology_annotations WHERE analysis_id=? ORDER BY created_at DESC", (analysis_id,)).fetchall()
    reviews = conn.execute("SELECT * FROM ophthalmology_clinical_reviews WHERE analysis_id=? ORDER BY created_at DESC", (analysis_id,)).fetchall()
    reports = conn.execute("SELECT * FROM ophthalmology_reports WHERE case_id=? ORDER BY created_at DESC", (case_id,)).fetchall()
    triage = conn.execute("SELECT * FROM ophthalmology_triage_queue WHERE analysis_id=? ORDER BY created_at DESC", (analysis_id,)).fetchall()
    communications = conn.execute("SELECT * FROM ophthalmology_patient_communications WHERE analysis_id=? ORDER BY created_at DESC", (analysis_id,)).fetchall()
    attendance = conn.execute("SELECT * FROM ophthalmology_attendance_outcomes WHERE analysis_id=? ORDER BY created_at DESC", (analysis_id,)).fetchall()

    conn.close()

    return {
        "case": dict(case) if case else None,
        "analysis": a,
        "annotations": [dict(x) for x in annotations],
        "reviews": [dict(x) for x in reviews],
        "reports": [dict(x) for x in reports],
        "triage": [dict(x) for x in triage],
        "communications": [dict(x) for x in communications],
        "attendance": [dict(x) for x in attendance]
    }

def _phase20_compute_pathway(bundle):
    if not bundle:
        return None

    case = bundle.get("case")
    analysis = bundle.get("analysis")
    annotations = bundle.get("annotations", [])
    reviews = bundle.get("reviews", [])
    reports = bundle.get("reports", [])
    triage = bundle.get("triage", [])
    communications = bundle.get("communications", [])
    attendance = bundle.get("attendance", [])

    case_created = 1 if case else 0
    ai_analysis_done = 1 if analysis else 0
    viewer_ready = 1 if analysis else 0
    annotation_done = 1 if annotations else 0
    review_done = 1 if reviews else 0
    dossier_done = 1 if reports else 0
    triage_done = 1 if triage else 0
    communication_done = 1 if communications else 0
    attendance_done = 1 if attendance else 0

    flags = [
        case_created,
        ai_analysis_done,
        viewer_ready,
        annotation_done,
        review_done,
        dossier_done,
        triage_done,
        communication_done,
        attendance_done
    ]

    completion_score = int(round(sum(flags) / len(flags) * 100))

    latest_attendance = attendance[0] if attendance else {}
    latest_triage = triage[0] if triage else {}
    latest_review = reviews[0] if reviews else {}

    attendance_status = str(latest_attendance.get("attendance_status", "")).lower()
    appointment_status = str(latest_attendance.get("appointment_status", latest_triage.get("appointment_status", ""))).lower()
    review_decision = str(latest_review.get("decision", "")).upper()

    if completion_score >= 100 and attendance_status == "attended" and appointment_status == "completed":
        pathway_status = "COMPLETED"
        final_status = "CLOSED_LOOP_COMPLETED"
    elif attendance_status == "no_show" or appointment_status == "missed":
        pathway_status = "NO_SHOW"
        final_status = "NO_SHOW_REQUIRES_FOLLOW_UP"
    elif appointment_status == "rescheduled":
        pathway_status = "RESCHEDULED"
        final_status = "RESCHEDULED_CONTINUE_TRACKING"
    elif review_decision in ["REJECTED", "NEEDS_FOLLOW_UP"] or completion_score < 100:
        pathway_status = "IN_PROGRESS"
        final_status = "CARE_PATHWAY_IN_PROGRESS"
    else:
        pathway_status = "NEEDS_REVIEW"
        final_status = "REQUIRES_OPERATIONAL_REVIEW"

    timeline = []

    if case:
        timeline.append({
            "phase": "Phase 8",
            "event": "Persistent case created",
            "status": case.get("status", "created"),
            "timestamp": case.get("created_at", ""),
            "summary": f"Case {case.get('case_id')} stored in persistent SQLite case storage."
        })

    if analysis:
        timeline.append({
            "phase": "Phase 11",
            "event": "Real image AI analysis",
            "status": analysis.get("risk_level", ""),
            "timestamp": analysis.get("created_at", ""),
            "summary": f"Image decoded. Quality {analysis.get('quality_score')}/100, risk {analysis.get('risk_score')}/100."
        })

        timeline.append({
            "phase": "Phase 12",
            "event": "Viewer and heatmap ready",
            "status": "viewer_ready",
            "timestamp": analysis.get("created_at", ""),
            "summary": "Image viewer, heatmap overlay, optic disc, retina and macula focus zones available."
        })

    for ann in annotations[:3]:
        timeline.append({
            "phase": "Phase 13",
            "event": "Doctor annotation saved",
            "status": ann.get("severity", ""),
            "timestamp": ann.get("created_at", ""),
            "summary": f"{ann.get('annotation_type')} / {ann.get('shape')} — {ann.get('doctor_note')}"
        })

    for rv in reviews[:3]:
        timeline.append({
            "phase": "Phase 14",
            "event": "Clinical review decision",
            "status": rv.get("decision", ""),
            "timestamp": rv.get("created_at", ""),
            "summary": f"Decision {rv.get('decision')} with priority {rv.get('priority')}. {rv.get('follow_up_plan')}"
        })

    if reports:
        timeline.append({
            "phase": "Phase 15",
            "event": "Final dossier generated",
            "status": "dossier_ready",
            "timestamp": reports[0].get("created_at", ""),
            "summary": f"{len(reports)} case reports are available for the pathway."
        })

    for tr in triage[:3]:
        timeline.append({
            "phase": "Phase 17",
            "event": "Triage and appointment",
            "status": tr.get("appointment_status", ""),
            "timestamp": tr.get("created_at", ""),
            "summary": f"Triage {tr.get('triage_id')} priority {tr.get('triage_priority')} appointment {tr.get('appointment_date')}."
        })

    for cm in communications[:3]:
        timeline.append({
            "phase": "Phase 18",
            "event": "Patient communication",
            "status": cm.get("communication_status", ""),
            "timestamp": cm.get("created_at", ""),
            "summary": f"{cm.get('channel')} message {cm.get('communication_status')}, confirmation {cm.get('patient_confirmation')}."
        })

    for at in attendance[:3]:
        timeline.append({
            "phase": "Phase 19",
            "event": "Attendance outcome",
            "status": at.get("attendance_status", ""),
            "timestamp": at.get("created_at", ""),
            "summary": f"Confirmation {at.get('patient_confirmation')}, attendance {at.get('attendance_status')}, appointment {at.get('appointment_status')}."
        })

    final_summary = (
        f"Closed-loop pathway status: {final_status}. "
        f"Completion score: {completion_score}%. "
        f"Case moved through image analysis, viewer, annotation, clinical review, triage, communication and attendance tracking."
    )

    return {
        "case_id": analysis.get("case_id") if analysis else "",
        "analysis_id": analysis.get("analysis_id") if analysis else "",
        "patient_id": analysis.get("patient_id") if analysis else "",
        "completion_score": completion_score,
        "pathway_status": pathway_status,
        "final_operational_status": final_status,
        "flags": {
            "case_created": case_created,
            "ai_analysis_done": ai_analysis_done,
            "viewer_ready": viewer_ready,
            "annotation_done": annotation_done,
            "review_done": review_done,
            "dossier_done": dossier_done,
            "triage_done": triage_done,
            "communication_done": communication_done,
            "attendance_done": attendance_done
        },
        "timeline": timeline,
        "latest": {
            "case": case,
            "analysis": analysis,
            "annotation": annotations[0] if annotations else None,
            "review": reviews[0] if reviews else None,
            "triage": triage[0] if triage else None,
            "communication": communications[0] if communications else None,
            "attendance": attendance[0] if attendance else None
        },
        "counts": {
            "annotations": len(annotations),
            "reviews": len(reviews),
            "reports": len(reports),
            "triage": len(triage),
            "communications": len(communications),
            "attendance": len(attendance)
        },
        "final_summary": final_summary
    }

def _phase20_save_pathway(pathway):
    if not pathway:
        return None

    _phase20_init_db()
    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT pathway_id FROM ophthalmology_closed_loop_pathways
    WHERE case_id=? AND analysis_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (pathway.get("case_id"), pathway.get("analysis_id"))).fetchone()

    pathway_id = old["pathway_id"] if old else "EYE-LOOP-" + _phase8_uuid.uuid4().hex[:10].upper()
    flags = pathway.get("flags", {})

    if old:
        conn.execute("""
        UPDATE ophthalmology_closed_loop_pathways
        SET completion_score=?,
            pathway_status=?,
            final_operational_status=?,
            case_created=?,
            ai_analysis_done=?,
            viewer_ready=?,
            annotation_done=?,
            review_done=?,
            dossier_done=?,
            triage_done=?,
            communication_done=?,
            attendance_done=?,
            final_summary=?,
            clinical_status=?,
            updated_at=?
        WHERE pathway_id=?
        """, (
            pathway.get("completion_score"),
            pathway.get("pathway_status"),
            pathway.get("final_operational_status"),
            flags.get("case_created"),
            flags.get("ai_analysis_done"),
            flags.get("viewer_ready"),
            flags.get("annotation_done"),
            flags.get("review_done"),
            flags.get("dossier_done"),
            flags.get("triage_done"),
            flags.get("communication_done"),
            flags.get("attendance_done"),
            pathway.get("final_summary"),
            "prototype_not_certified",
            now,
            pathway_id
        ))
    else:
        conn.execute("""
        INSERT INTO ophthalmology_closed_loop_pathways (
            pathway_id, case_id, analysis_id, patient_id,
            completion_score, pathway_status, final_operational_status,
            case_created, ai_analysis_done, viewer_ready, annotation_done, review_done,
            dossier_done, triage_done, communication_done, attendance_done,
            final_summary, clinical_status, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pathway_id,
            pathway.get("case_id"),
            pathway.get("analysis_id"),
            pathway.get("patient_id"),
            pathway.get("completion_score"),
            pathway.get("pathway_status"),
            pathway.get("final_operational_status"),
            flags.get("case_created"),
            flags.get("ai_analysis_done"),
            flags.get("viewer_ready"),
            flags.get("annotation_done"),
            flags.get("review_done"),
            flags.get("dossier_done"),
            flags.get("triage_done"),
            flags.get("communication_done"),
            flags.get("attendance_done"),
            pathway.get("final_summary"),
            "prototype_not_certified",
            now,
            now
        ))

    conn.commit()
    conn.close()

    pathway["pathway_id"] = pathway_id
    return pathway

@router.get("/phase-20/status")
async def phase20_status():
    _phase20_init_db()
    bundle = _phase20_latest_full_case()
    pathway = _phase20_compute_pathway(bundle)
    saved = _phase20_save_pathway(pathway) if pathway else None

    conn = _phase8_conn()
    total_pathways = conn.execute("SELECT COUNT(*) AS c FROM ophthalmology_closed_loop_pathways").fetchone()["c"]
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 20",
        "features": [
            "closed_loop_care_pathway",
            "phase_8_to_phase_19_unified_timeline",
            "completion_score",
            "final_operational_status",
            "case_journey_summary",
            "care_pathway_flags",
            "pathway_sqlite_storage",
            "closed_loop_dashboard",
            "final_operational_html_report",
            "final_operational_pdf_report",
            "multilingual_closed_loop_report"
        ],
        "total_pathways": total_pathways,
        "latest_pathway": saved,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-20/pathway")
async def phase20_pathway():
    bundle = _phase20_latest_full_case()
    pathway = _phase20_compute_pathway(bundle)

    if not pathway:
        return {
            "status": "empty",
            "phase": "AHOS Ophthalmology Phase 20",
            "message": "No AI analysis case found yet."
        }

    saved = _phase20_save_pathway(pathway)

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 20 Pathway",
        "pathway": saved,
        "bundle": bundle,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-20/pathways")
async def phase20_pathways():
    _phase20_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_closed_loop_pathways
    ORDER BY updated_at DESC
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 20 Pathways",
        "total_pathways": len(rows),
        "pathways": [dict(r) for r in rows]
    }

def _phase20_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 20 - مسار الرعاية التشغيلي المغلق",
            "summary": "تقرير نهائي يجمع رحلة الحالة من رفع الصورة حتى التحليل والمراجعة والموعد والتواصل والحضور.",
            "notice": "هذا التقرير نموذج تشغيلي تجريبي وليس نظامًا سريريًا معتمدًا."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 20 - Operational Closed-Loop Care Pathway",
            "summary": "Final operational report combining the case journey from image upload to AI analysis, review, appointment, communication and attendance outcome.",
            "notice": "This report is a prototype operational report and not a certified clinical system."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 20 - Sluten operativ vårdkedja",
            "summary": "Slutrapport som samlar fallresan från bilduppladdning till analys, granskning, tidbokning, kommunikation och närvaro.",
            "notice": "Denna rapport är en operativ prototyp och inte ett certifierat kliniskt system."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 20 - Parcours de soins opérationnel fermé",
            "summary": "Rapport final combinant le parcours du cas depuis l’image jusqu’à l’analyse, revue, rendez-vous, communication et présence.",
            "notice": "Ce rapport est un prototype opérationnel et non un système clinique certifié."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 20 - Percorso assistenziale operativo chiuso",
            "summary": "Report finale che combina il percorso del caso dall’immagine ad analisi, revisione, appuntamento, comunicazione e presenza.",
            "notice": "Questo report è un prototipo operativo e non un sistema clinico certificato."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-20/closed-loop-report-html")
async def phase20_closed_loop_report_html(language: str = "en"):
    bundle = _phase20_latest_full_case()
    pathway = _phase20_compute_pathway(bundle)
    pathway = _phase20_save_pathway(pathway) if pathway else None
    tx = _phase20_text(language)

    if not pathway:
        html = f"<html><body><h1>{tx['title']}</h1><p>No pathway data found.</p></body></html>"
        return Response(content=html, media_type="text/html; charset=utf-8")

    def flag_rows(flags):
        out = ""
        for k, v in flags.items():
            out += f"<tr><td>{k}</td><td>{'DONE' if v else 'MISSING'}</td></tr>"
        return out

    def timeline_rows(items):
        out = ""
        for x in items:
            out += f"""
            <tr>
              <td>{x.get('phase','')}</td>
              <td>{x.get('event','')}</td>
              <td>{x.get('status','')}</td>
              <td>{x.get('timestamp','')}</td>
              <td>{x.get('summary','')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Closed-Loop Summary</h2>
<div class="grid">
  <div class="metric">Pathway ID<strong>{pathway.get('pathway_id')}</strong></div>
  <div class="metric">Case ID<strong>{pathway.get('case_id')}</strong></div>
  <div class="metric">Patient ID<strong>{pathway.get('patient_id')}</strong></div>
  <div class="metric">Completion<strong>{pathway.get('completion_score')}%</strong></div>
  <div class="metric">Pathway Status<strong>{pathway.get('pathway_status')}</strong></div>
  <div class="metric">Final Status<strong>{pathway.get('final_operational_status')}</strong></div>
</div>

<div class="card"><p>{pathway.get('final_summary')}</p></div>

<h2>Completion Flags</h2>
<table><tr><th>Step</th><th>Status</th></tr>{flag_rows(pathway.get('flags', {}))}</table>

<h2>Full Patient Timeline</h2>
<table>
<tr><th>Phase</th><th>Event</th><th>Status</th><th>Timestamp</th><th>Summary</th></tr>
{timeline_rows(pathway.get('timeline', []))}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""
    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Content-Disposition": f"inline; filename=AHOS_Phase20_Closed_Loop_Care_Pathway_{language}.html"}
    )

@router.get("/phase-20/closed-loop-report-pdf")
async def phase20_closed_loop_report_pdf(language: str = "en"):
    bundle = _phase20_latest_full_case()
    pathway = _phase20_compute_pathway(bundle)
    pathway = _phase20_save_pathway(pathway) if pathway else None
    tx = _phase20_text(language)

    if not pathway:
        lines = [tx["title"], "", "No pathway data found."]
    else:
        lines = [
            tx["title"],
            "",
            "Project: AI Hospital Alliance / AHOS",
            "Module: Ophthalmology AI Eye Center",
            "Phase: 20 Operational Closed-Loop Care Pathway",
            "",
            tx["summary"],
            "",
            f"Pathway ID: {pathway.get('pathway_id')}",
            f"Case ID: {pathway.get('case_id')}",
            f"Analysis ID: {pathway.get('analysis_id')}",
            f"Patient ID: {pathway.get('patient_id')}",
            f"Completion Score: {pathway.get('completion_score')}%",
            f"Pathway Status: {pathway.get('pathway_status')}",
            f"Final Operational Status: {pathway.get('final_operational_status')}",
            "",
            "Completion Flags:"
        ]

        for k, v in pathway.get("flags", {}).items():
            lines.append(f"- {k}: {'DONE' if v else 'MISSING'}")

        lines += [
            "",
            "Full Patient Timeline:"
        ]

        for i, x in enumerate(pathway.get("timeline", []), start=1):
            lines += [
                f"{i}. {x.get('phase')} - {x.get('event')}",
                f"   Status: {x.get('status')}",
                f"   Time: {x.get('timestamp')}",
                f"   Summary: {x.get('summary')}",
                ""
            ]

        lines += [
            "Final Summary:",
            pathway.get("final_summary"),
            "",
            "Safety Notice:",
            tx["notice"],
            "",
            f"Generated at: {datetime.utcnow().isoformat()} UTC"
        ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=AHOS_Phase20_Closed_Loop_Care_Pathway_{language}.pdf"}
    )


# ============================
# AHOS Ophthalmology Phase 21
# Real Hospital Pilot Readiness + Governance Checklist
# ============================

def _phase21_init_db():
    _phase20_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_pilot_readiness (
        readiness_id TEXT PRIMARY KEY,
        pathway_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        technical_readiness INTEGER,
        pilot_readiness_score INTEGER,
        clinical_safety_score INTEGER,
        doctor_validation_score INTEGER,
        data_governance_score INTEGER,
        cybersecurity_score INTEGER,
        regulatory_score INTEGER,
        operational_score INTEGER,
        communication_score INTEGER,
        closed_loop_score INTEGER,
        go_no_go_decision TEXT,
        governance_status TEXT,
        regulatory_status TEXT,
        clinical_production_status TEXT,
        final_summary TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_pilot_risk_register (
        risk_id TEXT PRIMARY KEY,
        readiness_id TEXT,
        risk_category TEXT,
        risk_title TEXT,
        risk_level TEXT,
        risk_description TEXT,
        mitigation_plan TEXT,
        owner TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase21_latest_pathway():
    _phase21_init_db()
    conn = _phase8_conn()

    row = conn.execute("""
    SELECT *
    FROM ophthalmology_closed_loop_pathways
    ORDER BY updated_at DESC
    LIMIT 1
    """).fetchone()

    conn.close()
    return dict(row) if row else None

def _phase21_checklist_from_pathway(pathway):
    if not pathway:
        return {
            "technical_readiness": 0,
            "pilot_readiness_score": 0,
            "clinical_safety_score": 0,
            "doctor_validation_score": 0,
            "data_governance_score": 0,
            "cybersecurity_score": 0,
            "regulatory_score": 0,
            "operational_score": 0,
            "communication_score": 0,
            "closed_loop_score": 0,
            "items": []
        }

    completion = int(pathway.get("completion_score") or 0)

    items = [
        {
            "category": "Clinical Safety",
            "item": "Clinical safety notice displayed and prototype status visible",
            "status": "DONE",
            "score": 80,
            "evidence": "Prototype safety gates are present in the ophthalmology workflow."
        },
        {
            "category": "Doctor Validation",
            "item": "Doctor annotation and clinical review workflow exists",
            "status": "DONE" if pathway.get("annotation_done") and pathway.get("review_done") else "NEEDS_REVIEW",
            "score": 75 if pathway.get("annotation_done") and pathway.get("review_done") else 40,
            "evidence": "Phase 13 and Phase 14 provide annotation and clinical review."
        },
        {
            "category": "Data Governance",
            "item": "Persistent SQLite storage, report history, audit logs and timeline available",
            "status": "DONE",
            "score": 75,
            "evidence": "Case storage, communications, attendance and pathway records are saved."
        },
        {
            "category": "Cybersecurity",
            "item": "Local prototype security configured, but real hospital security audit required",
            "status": "NEEDS_REVIEW",
            "score": 55,
            "evidence": "Local JWT/security keys exist, but production security assessment is required."
        },
        {
            "category": "Regulatory",
            "item": "Prototype reports exist, but formal SaMD regulatory evidence is required",
            "status": "EVIDENCE_REQUIRED",
            "score": 45,
            "evidence": "PDF/HTML reports exist but no certified clinical validation package."
        },
        {
            "category": "Operational Readiness",
            "item": "Closed-loop care pathway works from image to attendance outcome",
            "status": "DONE" if completion >= 100 else "IN_PROGRESS",
            "score": 95 if completion >= 100 else completion,
            "evidence": f"Closed-loop completion score is {completion}%."
        },
        {
            "category": "Patient Communication",
            "item": "Patient notification and confirmation workflow available",
            "status": "DONE" if pathway.get("communication_done") and pathway.get("attendance_done") else "IN_PROGRESS",
            "score": 90 if pathway.get("communication_done") and pathway.get("attendance_done") else 50,
            "evidence": "Phase 18 and Phase 19 provide communication and attendance outcome."
        },
        {
            "category": "Closed-loop Pathway",
            "item": "Unified operational timeline and final pathway status available",
            "status": "DONE" if pathway.get("final_operational_status") == "CLOSED_LOOP_COMPLETED" else "NEEDS_REVIEW",
            "score": 100 if pathway.get("final_operational_status") == "CLOSED_LOOP_COMPLETED" else 60,
            "evidence": f"Final status: {pathway.get('final_operational_status')}."
        }
    ]

    clinical_safety_score = 80
    doctor_validation_score = 75
    data_governance_score = 75
    cybersecurity_score = 55
    regulatory_score = 45
    operational_score = 95 if completion >= 100 else completion
    communication_score = 90 if pathway.get("communication_done") and pathway.get("attendance_done") else 50
    closed_loop_score = 100 if pathway.get("final_operational_status") == "CLOSED_LOOP_COMPLETED" else 60

    technical_readiness = completion
    pilot_readiness_score = int(round((
        clinical_safety_score +
        doctor_validation_score +
        data_governance_score +
        cybersecurity_score +
        regulatory_score +
        operational_score +
        communication_score +
        closed_loop_score
    ) / 8))

    return {
        "technical_readiness": technical_readiness,
        "pilot_readiness_score": pilot_readiness_score,
        "clinical_safety_score": clinical_safety_score,
        "doctor_validation_score": doctor_validation_score,
        "data_governance_score": data_governance_score,
        "cybersecurity_score": cybersecurity_score,
        "regulatory_score": regulatory_score,
        "operational_score": operational_score,
        "communication_score": communication_score,
        "closed_loop_score": closed_loop_score,
        "items": items
    }

def _phase21_risks():
    return [
        {
            "risk_category": "Prototype Risk",
            "risk_title": "System is not certified for clinical use",
            "risk_level": "HIGH",
            "risk_description": "The ophthalmology module is a technical prototype and cannot be used as a certified diagnosis system.",
            "mitigation_plan": "Keep prototype notice visible, require ophthalmologist validation and formal clinical study.",
            "owner": "Clinical Governance Board",
            "status": "OPEN"
        },
        {
            "risk_category": "AI Safety",
            "risk_title": "False positive / false negative risk",
            "risk_level": "HIGH",
            "risk_description": "AI-like image analysis may miss or overcall findings without validated model performance.",
            "mitigation_plan": "Use ophthalmologist review, benchmark on real fundus/OCT datasets, and measure sensitivity/specificity.",
            "owner": "AI Safety Lead",
            "status": "OPEN"
        },
        {
            "risk_category": "Image Quality",
            "risk_title": "Low quality fundus/OCT images",
            "risk_level": "MEDIUM",
            "risk_description": "Dark, blurred or incomplete images can reduce interpretation quality.",
            "mitigation_plan": "Add acquisition quality gate, device calibration and repeat imaging workflow.",
            "owner": "Ophthalmology Imaging Lead",
            "status": "OPEN"
        },
        {
            "risk_category": "Data Protection",
            "risk_title": "Patient privacy and GDPR/HIPAA requirements",
            "risk_level": "HIGH",
            "risk_description": "Real pilot requires patient privacy, consent, access control and secure storage.",
            "mitigation_plan": "Implement RBAC, consent workflow, encryption, audit logs and hospital DPA.",
            "owner": "Data Protection Officer",
            "status": "OPEN"
        },
        {
            "risk_category": "Cybersecurity",
            "risk_title": "Production cybersecurity audit required",
            "risk_level": "HIGH",
            "risk_description": "Local development security is insufficient for real hospital deployment.",
            "mitigation_plan": "Perform penetration test, threat model, key management, secrets rotation and SOC monitoring.",
            "owner": "Security Officer",
            "status": "OPEN"
        },
        {
            "risk_category": "Regulatory",
            "risk_title": "SaMD evidence required",
            "risk_level": "HIGH",
            "risk_description": "Clinical production use requires regulatory pathway and evidence package.",
            "mitigation_plan": "Prepare ISO 13485/14971/62304 alignment, clinical evaluation and post-market plan.",
            "owner": "Regulatory Lead",
            "status": "OPEN"
        }
    ]

def _phase21_decision(scores):
    pilot_score = scores.get("pilot_readiness_score", 0)
    tech = scores.get("technical_readiness", 0)
    regulatory = scores.get("regulatory_score", 0)
    cybersecurity = scores.get("cybersecurity_score", 0)

    if tech >= 100 and pilot_score >= 75 and regulatory < 70:
        return {
            "go_no_go_decision": "READY_FOR_INTERNAL_PILOT",
            "go_no_go_label": "Ready for supervised internal pilot only",
            "go_no_go_reason": "Technical closed-loop is complete, but regulatory and cybersecurity evidence still require real hospital review."
        }

    if pilot_score >= 65:
        return {
            "go_no_go_decision": "NEEDS_GOVERNANCE_REVIEW",
            "go_no_go_label": "Needs governance review",
            "go_no_go_reason": "Pilot readiness is promising but requires governance, cybersecurity and clinical validation review."
        }

    return {
        "go_no_go_decision": "NOT_READY_FOR_CLINICAL_USE",
        "go_no_go_label": "Not ready for clinical use",
        "go_no_go_reason": "Readiness score is insufficient for pilot deployment."
    }

def _phase21_save_readiness():
    _phase21_init_db()
    pathway = _phase21_latest_pathway()
    scores = _phase21_checklist_from_pathway(pathway)
    decision = _phase21_decision(scores)

    if not pathway:
        return None

    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT readiness_id FROM ophthalmology_pilot_readiness
    WHERE pathway_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (pathway.get("pathway_id"),)).fetchone()

    readiness_id = old["readiness_id"] if old else "EYE-PILOT-" + _phase8_uuid.uuid4().hex[:10].upper()

    final_summary = (
        f"Technical readiness {scores.get('technical_readiness')}%. "
        f"Pilot readiness score {scores.get('pilot_readiness_score')}%. "
        f"Decision: {decision.get('go_no_go_decision')}. "
        "This is suitable for supervised internal pilot demonstration only, not certified clinical production."
    )

    if old:
        conn.execute("""
        UPDATE ophthalmology_pilot_readiness
        SET technical_readiness=?,
            pilot_readiness_score=?,
            clinical_safety_score=?,
            doctor_validation_score=?,
            data_governance_score=?,
            cybersecurity_score=?,
            regulatory_score=?,
            operational_score=?,
            communication_score=?,
            closed_loop_score=?,
            go_no_go_decision=?,
            governance_status=?,
            regulatory_status=?,
            clinical_production_status=?,
            final_summary=?,
            updated_at=?
        WHERE readiness_id=?
        """, (
            scores.get("technical_readiness"),
            scores.get("pilot_readiness_score"),
            scores.get("clinical_safety_score"),
            scores.get("doctor_validation_score"),
            scores.get("data_governance_score"),
            scores.get("cybersecurity_score"),
            scores.get("regulatory_score"),
            scores.get("operational_score"),
            scores.get("communication_score"),
            scores.get("closed_loop_score"),
            decision.get("go_no_go_decision"),
            "NEEDS_REAL_HOSPITAL_GOVERNANCE_REVIEW",
            "EVIDENCE_REQUIRED",
            "NOT_CERTIFIED",
            final_summary,
            now,
            readiness_id
        ))
    else:
        conn.execute("""
        INSERT INTO ophthalmology_pilot_readiness (
            readiness_id, pathway_id, case_id, analysis_id, patient_id,
            technical_readiness, pilot_readiness_score,
            clinical_safety_score, doctor_validation_score, data_governance_score,
            cybersecurity_score, regulatory_score, operational_score,
            communication_score, closed_loop_score,
            go_no_go_decision, governance_status, regulatory_status,
            clinical_production_status, final_summary,
            created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            readiness_id,
            pathway.get("pathway_id"),
            pathway.get("case_id"),
            pathway.get("analysis_id"),
            pathway.get("patient_id"),
            scores.get("technical_readiness"),
            scores.get("pilot_readiness_score"),
            scores.get("clinical_safety_score"),
            scores.get("doctor_validation_score"),
            scores.get("data_governance_score"),
            scores.get("cybersecurity_score"),
            scores.get("regulatory_score"),
            scores.get("operational_score"),
            scores.get("communication_score"),
            scores.get("closed_loop_score"),
            decision.get("go_no_go_decision"),
            "NEEDS_REAL_HOSPITAL_GOVERNANCE_REVIEW",
            "EVIDENCE_REQUIRED",
            "NOT_CERTIFIED",
            final_summary,
            now,
            now
        ))

    # Reset and insert risk register for current readiness
    conn.execute("DELETE FROM ophthalmology_pilot_risk_register WHERE readiness_id=?", (readiness_id,))
    for risk in _phase21_risks():
        risk_id = "EYE-RISK-" + _phase8_uuid.uuid4().hex[:10].upper()
        conn.execute("""
        INSERT INTO ophthalmology_pilot_risk_register (
            risk_id, readiness_id, risk_category, risk_title, risk_level,
            risk_description, mitigation_plan, owner, status, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            risk_id,
            readiness_id,
            risk["risk_category"],
            risk["risk_title"],
            risk["risk_level"],
            risk["risk_description"],
            risk["mitigation_plan"],
            risk["owner"],
            risk["status"],
            now,
            now
        ))

    conn.commit()
    conn.close()

    return {
        "readiness_id": readiness_id,
        "pathway": pathway,
        "scores": scores,
        "decision": decision,
        "governance_status": "NEEDS_REAL_HOSPITAL_GOVERNANCE_REVIEW",
        "regulatory_status": "EVIDENCE_REQUIRED",
        "clinical_production_status": "NOT_CERTIFIED",
        "final_summary": final_summary,
        "risks": _phase21_risks(),
        "created_or_updated_at": now
    }

@router.get("/phase-21/status")
async def phase21_status():
    data = _phase21_save_readiness()

    if not data:
        return {
            "status": "online",
            "phase": "AHOS Ophthalmology Phase 21",
            "message": "No Phase 20 pathway found yet.",
            "clinical_status": "prototype_not_certified",
            "timestamp": datetime.utcnow().isoformat()
        }

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 21",
        "features": [
            "real_hospital_pilot_readiness_dashboard",
            "governance_checklist",
            "clinical_safety_checklist",
            "doctor_validation_checklist",
            "data_governance_checklist",
            "cybersecurity_checklist",
            "regulatory_readiness",
            "pilot_risk_register",
            "go_no_go_decision",
            "pilot_readiness_html_report",
            "pilot_readiness_pdf_report",
            "multilingual_governance_report"
        ],
        "readiness": data,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-21/readiness")
async def phase21_readiness():
    data = _phase21_save_readiness()
    if not data:
        return {"status": "empty", "message": "No pathway found."}

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 21 Readiness",
        **data,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-21/risks")
async def phase21_risks():
    data = _phase21_save_readiness()
    readiness_id = data.get("readiness_id") if data else ""

    _phase21_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_risk_register
    WHERE readiness_id=?
    ORDER BY risk_level DESC, created_at DESC
    """, (readiness_id,)).fetchall()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 21 Risk Register",
        "readiness_id": readiness_id,
        "total_risks": len(rows),
        "risks": [dict(r) for r in rows]
    }

@router.get("/phase-21/readiness-list")
async def phase21_readiness_list():
    _phase21_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_readiness
    ORDER BY updated_at DESC
    """).fetchall()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 21 Readiness List",
        "total_readiness_records": len(rows),
        "records": [dict(r) for r in rows]
    }

def _phase21_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 21 - جاهزية تجربة المستشفى والحوكمة",
            "summary": "تقرير جاهزية Pilot لقسم العيون مع قائمة حوكمة وسلامة ومخاطر وقرار Go / No-Go.",
            "notice": "هذا التقرير يؤكد جاهزية عرض Pilot داخلي فقط، وليس اعتمادًا للاستخدام السريري الحقيقي."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 21 - Pilot Readiness + Governance Checklist",
            "summary": "Pilot readiness report for ophthalmology with governance checklist, safety checklist, risk register and Go / No-Go decision.",
            "notice": "This report supports supervised internal pilot readiness only and is not clinical certification."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 21 - Pilotberedskap och styrning",
            "summary": "Pilotberedskapsrapport med styrningschecklista, säkerhet, riskregister och Go/No-Go-beslut.",
            "notice": "Rapporten stödjer endast intern pilotberedskap och är inte klinisk certifiering."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 21 - Préparation pilote et gouvernance",
            "summary": "Rapport de préparation pilote avec gouvernance, sécurité, registre des risques et décision Go/No-Go.",
            "notice": "Ce rapport soutient uniquement un pilote interne supervisé et n’est pas une certification clinique."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 21 - Prontezza pilota e governance",
            "summary": "Report di prontezza pilota con checklist governance, sicurezza, rischi e decisione Go/No-Go.",
            "notice": "Questo report supporta solo un pilota interno supervisionato e non è certificazione clinica."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-21/pilot-readiness-report-html")
async def phase21_pilot_readiness_report_html(language: str = "en"):
    data = _phase21_save_readiness()
    tx = _phase21_text(language)

    if not data:
        html = f"<html><body><h1>{tx['title']}</h1><p>No readiness data found.</p></body></html>"
        return Response(content=html, media_type="text/html; charset=utf-8")

    scores = data["scores"]
    decision = data["decision"]
    items = scores.get("items", [])
    risks = data.get("risks", [])
    pathway = data.get("pathway", {})

    def score_cards():
        keys = [
            ("Technical", "technical_readiness"),
            ("Pilot Readiness", "pilot_readiness_score"),
            ("Clinical Safety", "clinical_safety_score"),
            ("Doctor Validation", "doctor_validation_score"),
            ("Data Governance", "data_governance_score"),
            ("Cybersecurity", "cybersecurity_score"),
            ("Regulatory", "regulatory_score"),
            ("Operational", "operational_score"),
            ("Communication", "communication_score"),
            ("Closed-loop", "closed_loop_score"),
        ]
        out = ""
        for label, key in keys:
            out += f'<div class="metric">{label}<strong>{scores.get(key)}%</strong></div>'
        return out

    def checklist_rows():
        out = ""
        for x in items:
            out += f"""
            <tr>
              <td>{x.get('category')}</td>
              <td>{x.get('item')}</td>
              <td>{x.get('status')}</td>
              <td>{x.get('score')}%</td>
              <td>{x.get('evidence')}</td>
            </tr>
            """
        return out

    def risk_rows():
        out = ""
        for r in risks:
            out += f"""
            <tr>
              <td>{r.get('risk_category')}</td>
              <td>{r.get('risk_title')}</td>
              <td>{r.get('risk_level')}</td>
              <td>{r.get('risk_description')}</td>
              <td>{r.get('mitigation_plan')}</td>
              <td>{r.get('owner')}</td>
              <td>{r.get('status')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
.decision {{
  background: #ecfdf5;
  border: 1px solid #10b981;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Pilot Readiness Summary</h2>
<div class="grid">
  <div class="metric">Readiness ID<strong>{data.get('readiness_id')}</strong></div>
  <div class="metric">Pathway ID<strong>{pathway.get('pathway_id')}</strong></div>
  <div class="metric">Case ID<strong>{pathway.get('case_id')}</strong></div>
  <div class="metric">Patient ID<strong>{pathway.get('patient_id')}</strong></div>
</div>

<h2>Scores</h2>
<div class="grid">{score_cards()}</div>

<h2>Go / No-Go Decision</h2>
<div class="decision">
  <p><strong>{decision.get('go_no_go_decision')}</strong></p>
  <p>{decision.get('go_no_go_label')}</p>
  <p>{decision.get('go_no_go_reason')}</p>
</div>

<h2>Governance Status</h2>
<div class="card">
<p><strong>Governance:</strong> {data.get('governance_status')}</p>
<p><strong>Regulatory:</strong> {data.get('regulatory_status')}</p>
<p><strong>Clinical Production:</strong> {data.get('clinical_production_status')}</p>
<p>{data.get('final_summary')}</p>
</div>

<h2>Governance Checklist</h2>
<table>
<tr><th>Category</th><th>Item</th><th>Status</th><th>Score</th><th>Evidence</th></tr>
{checklist_rows()}
</table>

<h2>Risk Register</h2>
<table>
<tr><th>Category</th><th>Risk</th><th>Level</th><th>Description</th><th>Mitigation</th><th>Owner</th><th>Status</th></tr>
{risk_rows()}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase21_Pilot_Readiness_Governance_{language}.html"
        }
    )

@router.get("/phase-21/pilot-readiness-report-pdf")
async def phase21_pilot_readiness_report_pdf(language: str = "en"):
    data = _phase21_save_readiness()
    tx = _phase21_text(language)

    if not data:
        lines = [tx["title"], "", "No readiness data found."]
    else:
        scores = data["scores"]
        decision = data["decision"]
        pathway = data.get("pathway", {})

        lines = [
            tx["title"],
            "",
            "Project: AI Hospital Alliance / AHOS",
            "Module: Ophthalmology AI Eye Center",
            "Phase: 21 Real Hospital Pilot Readiness + Governance Checklist",
            "",
            tx["summary"],
            "",
            f"Readiness ID: {data.get('readiness_id')}",
            f"Pathway ID: {pathway.get('pathway_id')}",
            f"Case ID: {pathway.get('case_id')}",
            f"Analysis ID: {pathway.get('analysis_id')}",
            f"Patient ID: {pathway.get('patient_id')}",
            "",
            "Readiness Scores:",
            f"- Technical Readiness: {scores.get('technical_readiness')}%",
            f"- Pilot Readiness Score: {scores.get('pilot_readiness_score')}%",
            f"- Clinical Safety: {scores.get('clinical_safety_score')}%",
            f"- Doctor Validation: {scores.get('doctor_validation_score')}%",
            f"- Data Governance: {scores.get('data_governance_score')}%",
            f"- Cybersecurity: {scores.get('cybersecurity_score')}%",
            f"- Regulatory: {scores.get('regulatory_score')}%",
            f"- Operational: {scores.get('operational_score')}%",
            f"- Communication: {scores.get('communication_score')}%",
            f"- Closed-loop: {scores.get('closed_loop_score')}%",
            "",
            "Go / No-Go Decision:",
            f"- Decision: {decision.get('go_no_go_decision')}",
            f"- Label: {decision.get('go_no_go_label')}",
            f"- Reason: {decision.get('go_no_go_reason')}",
            "",
            "Governance Status:",
            f"- Governance: {data.get('governance_status')}",
            f"- Regulatory: {data.get('regulatory_status')}",
            f"- Clinical Production: {data.get('clinical_production_status')}",
            "",
            "Governance Checklist:"
        ]

        for i, item in enumerate(scores.get("items", []), start=1):
            lines += [
                f"{i}. {item.get('category')} - {item.get('status')} - {item.get('score')}%",
                f"   {item.get('item')}",
                f"   Evidence: {item.get('evidence')}",
                ""
            ]

        lines += ["Risk Register:"]
        for i, r in enumerate(data.get("risks", []), start=1):
            lines += [
                f"{i}. {r.get('risk_title')} [{r.get('risk_level')}]",
                f"   Category: {r.get('risk_category')}",
                f"   Description: {r.get('risk_description')}",
                f"   Mitigation: {r.get('mitigation_plan')}",
                f"   Owner: {r.get('owner')} | Status: {r.get('status')}",
                ""
            ]

        lines += [
            "Final Summary:",
            data.get("final_summary"),
            "",
            "Safety Notice:",
            tx["notice"],
            "",
            f"Generated at: {datetime.utcnow().isoformat()} UTC"
        ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase21_Pilot_Readiness_Governance_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 22
# Real Hospital Pilot Execution Plan + Study Protocol
# ============================

def _phase22_init_db():
    _phase21_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_pilot_protocols (
        protocol_id TEXT PRIMARY KEY,
        readiness_id TEXT,
        pathway_id TEXT,
        case_id TEXT,
        patient_id TEXT,
        study_title TEXT,
        pilot_site TEXT,
        principal_investigator TEXT,
        study_objective TEXT,
        study_duration TEXT,
        target_cases INTEGER,
        pilot_departments TEXT,
        device_source TEXT,
        protocol_status TEXT,
        execution_status TEXT,
        ethics_status TEXT,
        governance_status TEXT,
        clinical_production_status TEXT,
        go_no_go_decision TEXT,
        pilot_protocol_score INTEGER,
        final_summary TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_pilot_protocol_items (
        item_id TEXT PRIMARY KEY,
        protocol_id TEXT,
        section TEXT,
        item_title TEXT,
        item_description TEXT,
        item_status TEXT,
        item_score INTEGER,
        owner TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase22_latest_readiness():
    _phase22_init_db()
    conn = _phase8_conn()
    row = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_readiness
    ORDER BY updated_at DESC
    LIMIT 1
    """).fetchone()
    conn.close()
    return dict(row) if row else None

def _phase22_default_protocol(readiness):
    if not readiness:
        return None

    pilot_readiness = int(readiness.get("pilot_readiness_score") or 0)
    technical = int(readiness.get("technical_readiness") or 0)

    protocol_score = int(round((pilot_readiness + technical + 80) / 3))

    if protocol_score >= 80 and readiness.get("go_no_go_decision") == "READY_FOR_INTERNAL_PILOT":
        execution_status = "READY_TO_START_SUPERVISED_PILOT"
        go_no_go = "READY_TO_START_SUPERVISED_PILOT"
    elif protocol_score >= 65:
        execution_status = "NEEDS_PROTOCOL_APPROVAL"
        go_no_go = "NEEDS_PROTOCOL_APPROVAL"
    else:
        execution_status = "NOT_READY_FOR_PILOT"
        go_no_go = "NOT_READY_FOR_PILOT"

    return {
        "study_title": "AHOS Ophthalmology AI Eye Center Supervised Pilot Study",
        "pilot_site": "Real Hospital Ophthalmology Department - Pilot Site Placeholder",
        "principal_investigator": "AHOS Ophthalmology Principal Investigator",
        "study_objective": "Evaluate supervised ophthalmology AI workflow for image quality, AI risk scoring, doctor validation, follow-up workflow and patient attendance outcomes.",
        "study_duration": "12 weeks supervised pilot",
        "target_cases": 50,
        "pilot_departments": "Ophthalmology, Imaging, Outpatient Follow-up, Clinical Governance",
        "device_source": "Fundus/OCT device integration placeholder",
        "protocol_status": "READY_DRAFT",
        "execution_status": execution_status,
        "ethics_status": "NEEDS_ETHICS_APPROVAL",
        "governance_status": "NEEDS_HOSPITAL_GOVERNANCE_APPROVAL",
        "clinical_production_status": "NOT_CERTIFIED",
        "go_no_go_decision": go_no_go,
        "pilot_protocol_score": protocol_score,
        "final_summary": (
            f"Pilot execution protocol is prepared as a supervised internal pilot draft. "
            f"Technical readiness is {technical}%, pilot readiness is {pilot_readiness}%, "
            f"protocol score is {protocol_score}%. Ethics and hospital governance approval are still required."
        )
    }

def _phase22_protocol_items():
    return [
        {
            "section": "Study Protocol",
            "item_title": "Study objective defined",
            "item_description": "Pilot objective covers AI image analysis, doctor validation, safety monitoring and follow-up outcome.",
            "item_status": "READY",
            "item_score": 90,
            "owner": "Principal Investigator"
        },
        {
            "section": "Inclusion Criteria",
            "item_title": "Eligible ophthalmology imaging cases",
            "item_description": "Patients requiring Fundus/OCT screening, acceptable image quality, consent and ophthalmologist review.",
            "item_status": "READY",
            "item_score": 85,
            "owner": "Ophthalmology Team"
        },
        {
            "section": "Exclusion Criteria",
            "item_title": "Unsafe or incomplete cases excluded",
            "item_description": "Very poor image quality, missing consent, emergency cases needing direct intervention and incomplete data.",
            "item_status": "READY",
            "item_score": 85,
            "owner": "Clinical Governance"
        },
        {
            "section": "Doctor Validation Workflow",
            "item_title": "Human-in-the-loop validation",
            "item_description": "AI analysis must be reviewed by ophthalmologist with annotation, clinical decision and safety override.",
            "item_status": "READY",
            "item_score": 90,
            "owner": "Ophthalmologist"
        },
        {
            "section": "Clinical Study KPIs",
            "item_title": "Pilot KPIs defined",
            "item_description": "Doctor agreement, image quality acceptance, follow-up completion, no-show rate, safety incidents and false positive/negative tracking.",
            "item_status": "READY",
            "item_score": 85,
            "owner": "Pilot Data Lead"
        },
        {
            "section": "Safety Monitoring",
            "item_title": "Safety escalation plan required",
            "item_description": "Safety gate, urgent review, incident log and escalation plan must be reviewed before live pilot.",
            "item_status": "NEEDS_APPROVAL",
            "item_score": 70,
            "owner": "Clinical Safety Officer"
        },
        {
            "section": "Data Collection",
            "item_title": "Pilot data collection plan",
            "item_description": "Case data, image metadata, AI score, doctor decision, patient follow-up, attendance and audit trail.",
            "item_status": "READY",
            "item_score": 85,
            "owner": "Data Governance Lead"
        },
        {
            "section": "Ethics and Consent",
            "item_title": "Ethics and consent approval",
            "item_description": "Patient consent, data privacy, de-identification, hospital approval and governance approval required.",
            "item_status": "NEEDS_APPROVAL",
            "item_score": 60,
            "owner": "Ethics Committee"
        },
        {
            "section": "Pilot Timeline",
            "item_title": "Pilot timeline prepared",
            "item_description": "Preparation, staff training, first 10 test cases, first 50 cases, interim review and final pilot report.",
            "item_status": "READY",
            "item_score": 85,
            "owner": "Pilot Manager"
        }
    ]

def _phase22_save_protocol():
    _phase22_init_db()
    readiness = _phase22_latest_readiness()
    if not readiness:
        return None

    protocol = _phase22_default_protocol(readiness)
    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT protocol_id FROM ophthalmology_pilot_protocols
    WHERE readiness_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (readiness.get("readiness_id"),)).fetchone()

    protocol_id = old["protocol_id"] if old else "EYE-PROTOCOL-" + _phase8_uuid.uuid4().hex[:10].upper()

    if old:
        conn.execute("""
        UPDATE ophthalmology_pilot_protocols
        SET study_title=?,
            pilot_site=?,
            principal_investigator=?,
            study_objective=?,
            study_duration=?,
            target_cases=?,
            pilot_departments=?,
            device_source=?,
            protocol_status=?,
            execution_status=?,
            ethics_status=?,
            governance_status=?,
            clinical_production_status=?,
            go_no_go_decision=?,
            pilot_protocol_score=?,
            final_summary=?,
            updated_at=?
        WHERE protocol_id=?
        """, (
            protocol["study_title"],
            protocol["pilot_site"],
            protocol["principal_investigator"],
            protocol["study_objective"],
            protocol["study_duration"],
            protocol["target_cases"],
            protocol["pilot_departments"],
            protocol["device_source"],
            protocol["protocol_status"],
            protocol["execution_status"],
            protocol["ethics_status"],
            protocol["governance_status"],
            protocol["clinical_production_status"],
            protocol["go_no_go_decision"],
            protocol["pilot_protocol_score"],
            protocol["final_summary"],
            now,
            protocol_id
        ))
    else:
        conn.execute("""
        INSERT INTO ophthalmology_pilot_protocols (
            protocol_id, readiness_id, pathway_id, case_id, patient_id,
            study_title, pilot_site, principal_investigator, study_objective,
            study_duration, target_cases, pilot_departments, device_source,
            protocol_status, execution_status, ethics_status, governance_status,
            clinical_production_status, go_no_go_decision, pilot_protocol_score,
            final_summary, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            protocol_id,
            readiness.get("readiness_id"),
            readiness.get("pathway_id"),
            readiness.get("case_id"),
            readiness.get("patient_id"),
            protocol["study_title"],
            protocol["pilot_site"],
            protocol["principal_investigator"],
            protocol["study_objective"],
            protocol["study_duration"],
            protocol["target_cases"],
            protocol["pilot_departments"],
            protocol["device_source"],
            protocol["protocol_status"],
            protocol["execution_status"],
            protocol["ethics_status"],
            protocol["governance_status"],
            protocol["clinical_production_status"],
            protocol["go_no_go_decision"],
            protocol["pilot_protocol_score"],
            protocol["final_summary"],
            now,
            now
        ))

    conn.execute("DELETE FROM ophthalmology_pilot_protocol_items WHERE protocol_id=?", (protocol_id,))
    for item in _phase22_protocol_items():
        item_id = "EYE-PITEM-" + _phase8_uuid.uuid4().hex[:10].upper()
        conn.execute("""
        INSERT INTO ophthalmology_pilot_protocol_items (
            item_id, protocol_id, section, item_title, item_description,
            item_status, item_score, owner, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item_id,
            protocol_id,
            item["section"],
            item["item_title"],
            item["item_description"],
            item["item_status"],
            item["item_score"],
            item["owner"],
            now,
            now
        ))

    conn.commit()
    conn.close()

    protocol["protocol_id"] = protocol_id
    protocol["readiness_id"] = readiness.get("readiness_id")
    protocol["pathway_id"] = readiness.get("pathway_id")
    protocol["case_id"] = readiness.get("case_id")
    protocol["patient_id"] = readiness.get("patient_id")
    protocol["items"] = _phase22_protocol_items()
    protocol["created_or_updated_at"] = now

    return {
        "protocol": protocol,
        "readiness": readiness
    }

@router.get("/phase-22/status")
async def phase22_status():
    data = _phase22_save_protocol()

    if not data:
        return {
            "status": "online",
            "phase": "AHOS Ophthalmology Phase 22",
            "message": "No Phase 21 readiness record found yet.",
            "clinical_status": "prototype_not_certified",
            "timestamp": datetime.utcnow().isoformat()
        }

    protocol = data["protocol"]

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 22",
        "features": [
            "real_hospital_pilot_execution_plan",
            "pilot_study_protocol",
            "inclusion_criteria",
            "exclusion_criteria",
            "doctor_validation_workflow",
            "clinical_study_kpis",
            "safety_monitoring_plan",
            "data_collection_plan",
            "ethics_consent_checklist",
            "pilot_timeline",
            "pilot_go_no_go_decision",
            "pilot_protocol_sqlite_storage",
            "pilot_protocol_html_report",
            "pilot_protocol_pdf_report",
            "multilingual_pilot_protocol"
        ],
        "protocol": protocol,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-22/protocol")
async def phase22_protocol():
    data = _phase22_save_protocol()
    if not data:
        return {"status": "empty", "message": "No readiness record found."}

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 22 Protocol",
        **data,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-22/protocol-list")
async def phase22_protocol_list():
    _phase22_init_db()
    conn = _phase8_conn()

    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_protocols
    ORDER BY updated_at DESC
    """).fetchall()

    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 22 Protocol List",
        "total_protocols": len(rows),
        "protocols": [dict(r) for r in rows]
    }

@router.get("/phase-22/protocol-items")
async def phase22_protocol_items():
    data = _phase22_save_protocol()
    if not data:
        return {"status": "empty", "items": []}

    protocol_id = data["protocol"]["protocol_id"]

    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_protocol_items
    WHERE protocol_id=?
    ORDER BY section, created_at
    """, (protocol_id,)).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 22 Protocol Items",
        "protocol_id": protocol_id,
        "total_items": len(rows),
        "items": [dict(r) for r in rows]
    }

def _phase22_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 22 - خطة تنفيذ Pilot وبروتوكول الدراسة",
            "summary": "تقرير بروتوكول Pilot داخل مستشفى حقيقي مع معايير الإدخال والاستبعاد، تحقق الطبيب، خطة السلامة، وخطة جمع البيانات.",
            "notice": "هذا التقرير بروتوكول Pilot تجريبي ويحتاج موافقة أخلاقية وحوكمة قبل أي استخدام سريري حقيقي."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 22 - Pilot Execution Plan + Study Protocol",
            "summary": "Real hospital pilot protocol with inclusion/exclusion criteria, doctor validation workflow, safety monitoring and data collection plan.",
            "notice": "This is a pilot protocol draft and requires ethics and governance approval before any real clinical use."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 22 - Pilotplan och studieprotokoll",
            "summary": "Pilotprotokoll med inklusions-/exklusionskriterier, läkarevalidering, säkerhetsövervakning och datainsamling.",
            "notice": "Detta är ett utkast till pilotprotokoll och kräver etik- och styrningsgodkännande."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 22 - Plan pilote et protocole d’étude",
            "summary": "Protocole pilote avec critères inclusion/exclusion, validation médecin, sécurité et collecte de données.",
            "notice": "Ceci est un protocole pilote préliminaire nécessitant approbation éthique et gouvernance."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 22 - Piano pilota e protocollo studio",
            "summary": "Protocollo pilota con criteri inclusione/esclusione, validazione medica, sicurezza e raccolta dati.",
            "notice": "Questo è un protocollo pilota bozza e richiede approvazione etica e governance."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-22/pilot-protocol-report-html")
async def phase22_pilot_protocol_report_html(language: str = "en"):
    data = _phase22_save_protocol()
    tx = _phase22_text(language)

    if not data:
        html = f"<html><body><h1>{tx['title']}</h1><p>No protocol data found.</p></body></html>"
        return Response(content=html, media_type="text/html; charset=utf-8")

    protocol = data["protocol"]
    readiness = data["readiness"]
    items = protocol.get("items", [])

    def item_rows():
        out = ""
        for x in items:
            out += f"""
            <tr>
              <td>{x.get('section')}</td>
              <td>{x.get('item_title')}</td>
              <td>{x.get('item_description')}</td>
              <td>{x.get('item_status')}</td>
              <td>{x.get('item_score')}%</td>
              <td>{x.get('owner')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Pilot Protocol Summary</h2>
<div class="grid">
  <div class="metric">Protocol ID<strong>{protocol.get('protocol_id')}</strong></div>
  <div class="metric">Readiness ID<strong>{protocol.get('readiness_id')}</strong></div>
  <div class="metric">Case ID<strong>{protocol.get('case_id')}</strong></div>
  <div class="metric">Patient ID<strong>{protocol.get('patient_id')}</strong></div>
  <div class="metric">Protocol Score<strong>{protocol.get('pilot_protocol_score')}%</strong></div>
  <div class="metric">Execution<strong>{protocol.get('execution_status')}</strong></div>
  <div class="metric">Ethics<strong>{protocol.get('ethics_status')}</strong></div>
  <div class="metric">Governance<strong>{protocol.get('governance_status')}</strong></div>
</div>

<h2>Study Protocol</h2>
<div class="card">
<p><strong>Study Title:</strong> {protocol.get('study_title')}</p>
<p><strong>Pilot Site:</strong> {protocol.get('pilot_site')}</p>
<p><strong>Principal Investigator:</strong> {protocol.get('principal_investigator')}</p>
<p><strong>Objective:</strong> {protocol.get('study_objective')}</p>
<p><strong>Duration:</strong> {protocol.get('study_duration')}</p>
<p><strong>Target Cases:</strong> {protocol.get('target_cases')}</p>
<p><strong>Departments:</strong> {protocol.get('pilot_departments')}</p>
<p><strong>Device Source:</strong> {protocol.get('device_source')}</p>
</div>

<h2>Protocol Items</h2>
<table>
<tr><th>Section</th><th>Item</th><th>Description</th><th>Status</th><th>Score</th><th>Owner</th></tr>
{item_rows()}
</table>

<h2>Go / No-Go</h2>
<div class="card">
<p><strong>Decision:</strong> {protocol.get('go_no_go_decision')}</p>
<p><strong>Clinical Production:</strong> {protocol.get('clinical_production_status')}</p>
<p>{protocol.get('final_summary')}</p>
<p><strong>Linked Phase 21 Readiness:</strong> {readiness.get('go_no_go_decision')} / {readiness.get('pilot_readiness_score')}%</p>
</div>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={
            "Content-Disposition": f"inline; filename=AHOS_Phase22_Pilot_Execution_Protocol_{language}.html"
        }
    )

@router.get("/phase-22/pilot-protocol-report-pdf")
async def phase22_pilot_protocol_report_pdf(language: str = "en"):
    data = _phase22_save_protocol()
    tx = _phase22_text(language)

    if not data:
        lines = [tx["title"], "", "No protocol data found."]
    else:
        protocol = data["protocol"]
        readiness = data["readiness"]

        lines = [
            tx["title"],
            "",
            "Project: AI Hospital Alliance / AHOS",
            "Module: Ophthalmology AI Eye Center",
            "Phase: 22 Real Hospital Pilot Execution Plan + Study Protocol",
            "",
            tx["summary"],
            "",
            f"Protocol ID: {protocol.get('protocol_id')}",
            f"Readiness ID: {protocol.get('readiness_id')}",
            f"Case ID: {protocol.get('case_id')}",
            f"Patient ID: {protocol.get('patient_id')}",
            "",
            "Study Protocol:",
            f"- Study Title: {protocol.get('study_title')}",
            f"- Pilot Site: {protocol.get('pilot_site')}",
            f"- Principal Investigator: {protocol.get('principal_investigator')}",
            f"- Objective: {protocol.get('study_objective')}",
            f"- Duration: {protocol.get('study_duration')}",
            f"- Target Cases: {protocol.get('target_cases')}",
            f"- Departments: {protocol.get('pilot_departments')}",
            f"- Device Source: {protocol.get('device_source')}",
            "",
            "Execution Status:",
            f"- Protocol Status: {protocol.get('protocol_status')}",
            f"- Execution Status: {protocol.get('execution_status')}",
            f"- Ethics Status: {protocol.get('ethics_status')}",
            f"- Governance Status: {protocol.get('governance_status')}",
            f"- Clinical Production: {protocol.get('clinical_production_status')}",
            f"- Go / No-Go: {protocol.get('go_no_go_decision')}",
            f"- Protocol Score: {protocol.get('pilot_protocol_score')}%",
            "",
            "Protocol Items:"
        ]

        for i, item in enumerate(protocol.get("items", []), start=1):
            lines += [
                f"{i}. {item.get('section')} - {item.get('item_title')}",
                f"   Status: {item.get('item_status')} | Score: {item.get('item_score')}%",
                f"   Description: {item.get('item_description')}",
                f"   Owner: {item.get('owner')}",
                ""
            ]

        lines += [
            "Linked Phase 21 Readiness:",
            f"- Decision: {readiness.get('go_no_go_decision')}",
            f"- Pilot Readiness: {readiness.get('pilot_readiness_score')}%",
            "",
            "Final Summary:",
            protocol.get("final_summary"),
            "",
            "Safety Notice:",
            tx["notice"],
            "",
            f"Generated at: {datetime.utcnow().isoformat()} UTC"
        ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=AHOS_Phase22_Pilot_Execution_Protocol_{language}.pdf"
        }
    )


# ============================
# AHOS Ophthalmology Phase 23
# Pilot Case Enrollment + Doctor Agreement Tracking
# ============================

def _phase23_init_db():
    _phase22_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_pilot_enrollments (
        enrollment_id TEXT PRIMARY KEY,
        protocol_id TEXT,
        readiness_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        enrollment_status TEXT,
        consent_status TEXT,
        image_quality_status TEXT,
        doctor_review_status TEXT,
        validation_status TEXT,
        enrollment_note TEXT,
        created_by TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_doctor_agreements (
        agreement_id TEXT PRIMARY KEY,
        enrollment_id TEXT,
        protocol_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        ai_risk_score INTEGER,
        ai_risk_level TEXT,
        ai_finding TEXT,
        doctor_decision TEXT,
        doctor_diagnosis TEXT,
        agreement_status TEXT,
        disagreement_reason TEXT,
        safety_override TEXT,
        follow_up_required TEXT,
        validation_status TEXT,
        doctor_name TEXT,
        doctor_note TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase23_latest_protocol():
    _phase23_init_db()
    conn = _phase8_conn()
    row = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_protocols
    ORDER BY updated_at DESC
    LIMIT 1
    """).fetchone()
    conn.close()
    return dict(row) if row else None

def _phase23_latest_analysis():
    _phase23_init_db()
    conn = _phase8_conn()
    row = conn.execute("""
    SELECT *
    FROM ophthalmology_ai_analyses
    ORDER BY created_at DESC
    LIMIT 1
    """).fetchone()
    conn.close()
    return dict(row) if row else None

def _phase23_get_or_create_enrollment():
    _phase23_init_db()
    protocol = _phase23_latest_protocol()
    analysis = _phase23_latest_analysis()

    if not protocol or not analysis:
        return None

    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_enrollments
    WHERE protocol_id=? AND analysis_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (protocol.get("protocol_id"), analysis.get("analysis_id"))).fetchone()

    if old:
        enrollment = dict(old)
        conn.close()
        return enrollment

    enrollment_id = "EYE-ENROLL-" + _phase8_uuid.uuid4().hex[:10].upper()

    enrollment = {
        "enrollment_id": enrollment_id,
        "protocol_id": protocol.get("protocol_id"),
        "readiness_id": protocol.get("readiness_id"),
        "case_id": analysis.get("case_id"),
        "analysis_id": analysis.get("analysis_id"),
        "patient_id": analysis.get("patient_id"),
        "enrollment_status": "ENROLLED",
        "consent_status": "CONSENT_COMPLETED",
        "image_quality_status": "ACCEPTED_LIMITED_QUALITY",
        "doctor_review_status": "READY_FOR_DOCTOR_REVIEW",
        "validation_status": "PILOT_VALIDATION_IN_PROGRESS",
        "enrollment_note": "Pilot case enrolled under Phase 22 supervised pilot protocol.",
        "created_by": "AHOS Pilot Enrollment Center",
        "created_at": now,
        "updated_at": now
    }

    conn.execute("""
    INSERT INTO ophthalmology_pilot_enrollments (
        enrollment_id, protocol_id, readiness_id, case_id, analysis_id, patient_id,
        enrollment_status, consent_status, image_quality_status, doctor_review_status,
        validation_status, enrollment_note, created_by, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        enrollment["enrollment_id"],
        enrollment["protocol_id"],
        enrollment["readiness_id"],
        enrollment["case_id"],
        enrollment["analysis_id"],
        enrollment["patient_id"],
        enrollment["enrollment_status"],
        enrollment["consent_status"],
        enrollment["image_quality_status"],
        enrollment["doctor_review_status"],
        enrollment["validation_status"],
        enrollment["enrollment_note"],
        enrollment["created_by"],
        enrollment["created_at"],
        enrollment["updated_at"]
    ))

    conn.commit()
    conn.close()
    return enrollment

def _phase23_get_or_create_agreement():
    _phase23_init_db()
    enrollment = _phase23_get_or_create_enrollment()
    analysis = _phase23_latest_analysis()

    if not enrollment or not analysis:
        return None

    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT *
    FROM ophthalmology_doctor_agreements
    WHERE enrollment_id=? AND analysis_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (enrollment.get("enrollment_id"), analysis.get("analysis_id"))).fetchone()

    if old:
        agreement = dict(old)
        conn.close()
        return agreement

    ai_risk_score = int(analysis.get("risk_score") or 0)
    ai_risk_level = str(analysis.get("risk_level") or "UNKNOWN")

    doctor_decision = "NEEDS_FOLLOW_UP"
    doctor_diagnosis = "Moderate ophthalmology risk; image quality is limited and optic disc area requires ophthalmologist follow-up."
    agreement_status = "AGREE"
    disagreement_reason = ""
    safety_override = "NO"
    follow_up_required = "YES"
    validation_status = "VALIDATION_REVIEWED"

    agreement_id = "EYE-AGR-" + _phase8_uuid.uuid4().hex[:10].upper()

    agreement = {
        "agreement_id": agreement_id,
        "enrollment_id": enrollment.get("enrollment_id"),
        "protocol_id": enrollment.get("protocol_id"),
        "case_id": enrollment.get("case_id"),
        "analysis_id": enrollment.get("analysis_id"),
        "patient_id": enrollment.get("patient_id"),
        "ai_risk_score": ai_risk_score,
        "ai_risk_level": ai_risk_level,
        "ai_finding": "AI pipeline detected moderate ophthalmology risk with limited image quality.",
        "doctor_decision": doctor_decision,
        "doctor_diagnosis": doctor_diagnosis,
        "agreement_status": agreement_status,
        "disagreement_reason": disagreement_reason,
        "safety_override": safety_override,
        "follow_up_required": follow_up_required,
        "validation_status": validation_status,
        "doctor_name": "AHOS Pilot Ophthalmologist",
        "doctor_note": "Doctor agrees with AI risk category for supervised pilot tracking. This is not a certified diagnosis.",
        "created_at": now,
        "updated_at": now
    }

    conn.execute("""
    INSERT INTO ophthalmology_doctor_agreements (
        agreement_id, enrollment_id, protocol_id, case_id, analysis_id, patient_id,
        ai_risk_score, ai_risk_level, ai_finding, doctor_decision, doctor_diagnosis,
        agreement_status, disagreement_reason, safety_override, follow_up_required,
        validation_status, doctor_name, doctor_note, created_at, updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        agreement["agreement_id"],
        agreement["enrollment_id"],
        agreement["protocol_id"],
        agreement["case_id"],
        agreement["analysis_id"],
        agreement["patient_id"],
        agreement["ai_risk_score"],
        agreement["ai_risk_level"],
        agreement["ai_finding"],
        agreement["doctor_decision"],
        agreement["doctor_diagnosis"],
        agreement["agreement_status"],
        agreement["disagreement_reason"],
        agreement["safety_override"],
        agreement["follow_up_required"],
        agreement["validation_status"],
        agreement["doctor_name"],
        agreement["doctor_note"],
        agreement["created_at"],
        agreement["updated_at"]
    ))

    conn.execute("""
    UPDATE ophthalmology_pilot_enrollments
    SET doctor_review_status=?,
        validation_status=?,
        updated_at=?
    WHERE enrollment_id=?
    """, (
        "DOCTOR_REVIEW_COMPLETED",
        "VALIDATION_REVIEWED",
        now,
        enrollment.get("enrollment_id")
    ))

    conn.commit()
    conn.close()
    return agreement

def _phase23_metrics():
    _phase23_init_db()
    conn = _phase8_conn()

    enrollments = [dict(r) for r in conn.execute("SELECT * FROM ophthalmology_pilot_enrollments ORDER BY created_at DESC").fetchall()]
    agreements = [dict(r) for r in conn.execute("SELECT * FROM ophthalmology_doctor_agreements ORDER BY created_at DESC").fetchall()]

    total_enrolled = len(enrollments)
    total_agreements = len(agreements)

    consent_completed = sum(1 for e in enrollments if e.get("consent_status") == "CONSENT_COMPLETED")
    doctor_reviewed = sum(1 for e in enrollments if e.get("doctor_review_status") == "DOCTOR_REVIEW_COMPLETED")
    validation_completed = sum(1 for a in agreements if a.get("validation_status") == "VALIDATION_REVIEWED")

    agree = sum(1 for a in agreements if a.get("agreement_status") == "AGREE")
    disagree = sum(1 for a in agreements if a.get("agreement_status") == "DISAGREE")
    partial = sum(1 for a in agreements if a.get("agreement_status") == "PARTIAL")
    safety_override_count = sum(1 for a in agreements if a.get("safety_override") == "YES")
    follow_up_required = sum(1 for a in agreements if a.get("follow_up_required") == "YES")

    agreement_rate = round((agree / total_agreements) * 100, 2) if total_agreements else 0
    disagreement_rate = round((disagree / total_agreements) * 100, 2) if total_agreements else 0
    partial_rate = round((partial / total_agreements) * 100, 2) if total_agreements else 0
    review_completion_rate = round((doctor_reviewed / total_enrolled) * 100, 2) if total_enrolled else 0

    conn.close()

    return {
        "total_enrolled": total_enrolled,
        "total_agreements": total_agreements,
        "consent_completed": consent_completed,
        "doctor_reviewed": doctor_reviewed,
        "validation_completed": validation_completed,
        "agree": agree,
        "disagree": disagree,
        "partial": partial,
        "safety_override_count": safety_override_count,
        "follow_up_required": follow_up_required,
        "agreement_rate": agreement_rate,
        "disagreement_rate": disagreement_rate,
        "partial_agreement_rate": partial_rate,
        "review_completion_rate": review_completion_rate,
        "sensitivity_placeholder": 0,
        "specificity_placeholder": 0,
        "false_positive_tracking": 0,
        "false_negative_tracking": 0,
        "enrollments": enrollments,
        "agreements": agreements
    }

@router.get("/phase-23/status")
async def phase23_status():
    _phase23_init_db()
    metrics = _phase23_metrics()
    latest_enrollment = metrics["enrollments"][0] if metrics["enrollments"] else None
    latest_agreement = metrics["agreements"][0] if metrics["agreements"] else None

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 23",
        "features": [
            "pilot_case_enrollment_registry",
            "doctor_agreement_tracking",
            "ai_vs_doctor_comparison",
            "agreement_rate_dashboard",
            "disagreement_tracking",
            "partial_agreement_tracking",
            "safety_override_tracking",
            "validation_case_status",
            "prototype_validation_metrics",
            "enrollment_timeline",
            "pilot_agreement_html_report",
            "pilot_agreement_pdf_report",
            "multilingual_agreement_report"
        ],
        "metrics": metrics,
        "latest_enrollment": latest_enrollment,
        "latest_agreement": latest_agreement,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/phase-23/enroll-demo")
async def phase23_enroll_demo():
    enrollment = _phase23_get_or_create_enrollment()
    if not enrollment:
        return {
            "status": "error",
            "message": "No Phase 22 protocol or Phase 11 analysis found."
        }

    return {
        "status": "enrolled",
        "phase": "AHOS Ophthalmology Phase 23",
        "enrollment": enrollment,
        "persistent": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/phase-23/doctor-agreement-demo")
async def phase23_doctor_agreement_demo():
    agreement = _phase23_get_or_create_agreement()
    if not agreement:
        return {
            "status": "error",
            "message": "No enrollment or analysis found."
        }

    return {
        "status": "agreement_saved",
        "phase": "AHOS Ophthalmology Phase 23",
        "agreement": agreement,
        "persistent": True,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-23/enrollments")
async def phase23_enrollments():
    _phase23_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_pilot_enrollments
    ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 23 Enrollments",
        "total_enrollments": len(rows),
        "enrollments": [dict(r) for r in rows]
    }

@router.get("/phase-23/agreements")
async def phase23_agreements():
    _phase23_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_doctor_agreements
    ORDER BY created_at DESC
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 23 Doctor Agreements",
        "total_agreements": len(rows),
        "agreements": [dict(r) for r in rows]
    }

@router.get("/phase-23/dashboard")
async def phase23_dashboard():
    metrics = _phase23_metrics()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 23 Dashboard",
        "metrics": metrics,
        "agreement_distribution": [
            {"label": "AGREE", "value": metrics["agree"]},
            {"label": "DISAGREE", "value": metrics["disagree"]},
            {"label": "PARTIAL", "value": metrics["partial"]}
        ],
        "validation_distribution": [
            {"label": "VALIDATION_REVIEWED", "value": metrics["validation_completed"]},
            {"label": "PENDING", "value": max(metrics["total_enrolled"] - metrics["validation_completed"], 0)}
        ],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

def _phase23_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 23 - تسجيل حالات Pilot وتتبع توافق الطبيب",
            "summary": "تقرير تسجيل حالات Pilot ومقارنة نتيجة AI مع قرار الطبيب ومؤشرات التوافق والتحقق.",
            "notice": "هذا تقرير تحقق Pilot تجريبي ولا يمثل اعتمادًا سريريًا أو قياس أداء نهائي."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 23 - Pilot Case Enrollment + Doctor Agreement Tracking",
            "summary": "Pilot enrollment and doctor agreement report comparing AI output with ophthalmologist decision and validation status.",
            "notice": "This is a prototype pilot validation report and not a certified performance study."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 23 - Pilotregistrering och läkarsamstämmighet",
            "summary": "Rapport för pilotfallregistrering och jämförelse mellan AI-resultat och ögonläkarens beslut.",
            "notice": "Detta är en prototyp för pilotvalidering och inte en certifierad prestandastudie."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 23 - Inclusion pilote et accord médecin",
            "summary": "Rapport d’inclusion pilote comparant la sortie IA avec la décision de l’ophtalmologue.",
            "notice": "Ceci est un rapport prototype de validation pilote, non une étude certifiée."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 23 - Arruolamento pilota e accordo medico",
            "summary": "Report di arruolamento pilota che confronta output AI e decisione dell’oculista.",
            "notice": "Questo è un report prototipo di validazione pilota, non uno studio certificato."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-23/agreement-report-html")
async def phase23_agreement_report_html(language: str = "en"):
    metrics = _phase23_metrics()
    tx = _phase23_text(language)

    enrollments = metrics.get("enrollments", [])
    agreements = metrics.get("agreements", [])

    def enrollment_rows():
        out = ""
        for e in enrollments:
            out += f"""
            <tr>
              <td>{e.get('enrollment_id')}</td>
              <td>{e.get('protocol_id')}</td>
              <td>{e.get('case_id')}</td>
              <td>{e.get('patient_id')}</td>
              <td>{e.get('enrollment_status')}</td>
              <td>{e.get('consent_status')}</td>
              <td>{e.get('doctor_review_status')}</td>
              <td>{e.get('validation_status')}</td>
            </tr>
            """
        return out

    def agreement_rows():
        out = ""
        for a in agreements:
            out += f"""
            <tr>
              <td>{a.get('agreement_id')}</td>
              <td>{a.get('enrollment_id')}</td>
              <td>{a.get('ai_risk_score')} / {a.get('ai_risk_level')}</td>
              <td>{a.get('doctor_decision')}</td>
              <td>{a.get('agreement_status')}</td>
              <td>{a.get('safety_override')}</td>
              <td>{a.get('follow_up_required')}</td>
              <td>{a.get('validation_status')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Pilot Agreement KPIs</h2>
<div class="grid">
  <div class="metric">Enrolled Cases<strong>{metrics.get('total_enrolled')}</strong></div>
  <div class="metric">Doctor Agreements<strong>{metrics.get('total_agreements')}</strong></div>
  <div class="metric">Consent Completed<strong>{metrics.get('consent_completed')}</strong></div>
  <div class="metric">Doctor Reviewed<strong>{metrics.get('doctor_reviewed')}</strong></div>
  <div class="metric">Agreement Rate<strong>{metrics.get('agreement_rate')}%</strong></div>
  <div class="metric">Disagreement Rate<strong>{metrics.get('disagreement_rate')}%</strong></div>
  <div class="metric">Partial Rate<strong>{metrics.get('partial_agreement_rate')}%</strong></div>
  <div class="metric">Safety Override<strong>{metrics.get('safety_override_count')}</strong></div>
  <div class="metric">Follow-up Required<strong>{metrics.get('follow_up_required')}</strong></div>
  <div class="metric">Validation Reviewed<strong>{metrics.get('validation_completed')}</strong></div>
</div>

<h2>Enrollment Registry</h2>
<table>
<tr><th>Enrollment ID</th><th>Protocol</th><th>Case</th><th>Patient</th><th>Status</th><th>Consent</th><th>Doctor Review</th><th>Validation</th></tr>
{enrollment_rows()}
</table>

<h2>Doctor Agreement Tracking</h2>
<table>
<tr><th>Agreement ID</th><th>Enrollment</th><th>AI Risk</th><th>Doctor Decision</th><th>Agreement</th><th>Override</th><th>Follow-up</th><th>Validation</th></tr>
{agreement_rows()}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Content-Disposition": f"inline; filename=AHOS_Phase23_Pilot_Agreement_Report_{language}.html"}
    )

@router.get("/phase-23/agreement-report-pdf")
async def phase23_agreement_report_pdf(language: str = "en"):
    metrics = _phase23_metrics()
    tx = _phase23_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 23 Pilot Case Enrollment + Doctor Agreement Tracking",
        "",
        tx["summary"],
        "",
        "Pilot Agreement KPIs:",
        f"- Total Enrolled Cases: {metrics.get('total_enrolled')}",
        f"- Total Agreements: {metrics.get('total_agreements')}",
        f"- Consent Completed: {metrics.get('consent_completed')}",
        f"- Doctor Reviewed: {metrics.get('doctor_reviewed')}",
        f"- Validation Completed: {metrics.get('validation_completed')}",
        f"- Agreement Rate: {metrics.get('agreement_rate')}%",
        f"- Disagreement Rate: {metrics.get('disagreement_rate')}%",
        f"- Partial Agreement Rate: {metrics.get('partial_agreement_rate')}%",
        f"- Safety Override Count: {metrics.get('safety_override_count')}",
        f"- Follow-up Required: {metrics.get('follow_up_required')}",
        f"- Sensitivity Placeholder: {metrics.get('sensitivity_placeholder')}",
        f"- Specificity Placeholder: {metrics.get('specificity_placeholder')}",
        "",
        "Enrollment Registry:"
    ]

    for i, e in enumerate(metrics.get("enrollments", []), start=1):
        lines += [
            f"{i}. Enrollment ID: {e.get('enrollment_id')}",
            f"   Protocol ID: {e.get('protocol_id')}",
            f"   Case ID: {e.get('case_id')}",
            f"   Analysis ID: {e.get('analysis_id')}",
            f"   Patient ID: {e.get('patient_id')}",
            f"   Consent: {e.get('consent_status')} | Review: {e.get('doctor_review_status')}",
            f"   Validation: {e.get('validation_status')}",
            ""
        ]

    lines += ["Doctor Agreement Tracking:"]
    for i, a in enumerate(metrics.get("agreements", []), start=1):
        lines += [
            f"{i}. Agreement ID: {a.get('agreement_id')}",
            f"   Enrollment ID: {a.get('enrollment_id')}",
            f"   AI Risk: {a.get('ai_risk_score')} / {a.get('ai_risk_level')}",
            f"   AI Finding: {a.get('ai_finding')}",
            f"   Doctor Decision: {a.get('doctor_decision')}",
            f"   Doctor Diagnosis: {a.get('doctor_diagnosis')}",
            f"   Agreement: {a.get('agreement_status')}",
            f"   Safety Override: {a.get('safety_override')}",
            f"   Follow-up Required: {a.get('follow_up_required')}",
            f"   Validation Status: {a.get('validation_status')}",
            f"   Doctor: {a.get('doctor_name')}",
            f"   Note: {a.get('doctor_note')}",
            ""
        ]

    lines += [
        "Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=AHOS_Phase23_Pilot_Agreement_Report_{language}.pdf"}
    )


# ============================
# AHOS Ophthalmology Phase 24
# Pilot Validation Analytics + Performance Evidence Report
# ============================

def _phase24_init_db():
    _phase23_init_db()
    conn = _phase8_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_validation_evidence_reports (
        evidence_id TEXT PRIMARY KEY,
        protocol_id TEXT,
        enrollment_count INTEGER,
        agreement_count INTEGER,
        agreement_rate REAL,
        disagreement_rate REAL,
        partial_agreement_rate REAL,
        review_completion_rate REAL,
        sensitivity_placeholder REAL,
        specificity_placeholder REAL,
        true_positive_count INTEGER,
        true_negative_count INTEGER,
        false_positive_count INTEGER,
        false_negative_count INTEGER,
        safety_override_count INTEGER,
        follow_up_required_count INTEGER,
        validation_evidence_score INTEGER,
        evidence_status TEXT,
        regulatory_evidence_status TEXT,
        clinical_production_status TEXT,
        final_summary TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ophthalmology_fp_fn_registry (
        registry_id TEXT PRIMARY KEY,
        agreement_id TEXT,
        enrollment_id TEXT,
        case_id TEXT,
        analysis_id TEXT,
        patient_id TEXT,
        ai_risk_score INTEGER,
        ai_risk_level TEXT,
        doctor_decision TEXT,
        agreement_status TEXT,
        evidence_type TEXT,
        evidence_reason TEXT,
        safety_impact TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def _phase24_collect_metrics():
    _phase24_init_db()
    conn = _phase8_conn()

    enrollments = [dict(r) for r in conn.execute("""
        SELECT * FROM ophthalmology_pilot_enrollments
        ORDER BY created_at DESC
    """).fetchall()]

    agreements = [dict(r) for r in conn.execute("""
        SELECT * FROM ophthalmology_doctor_agreements
        ORDER BY created_at DESC
    """).fetchall()]

    total_enrolled = len(enrollments)
    total_agreements = len(agreements)

    agree = sum(1 for a in agreements if a.get("agreement_status") == "AGREE")
    disagree = sum(1 for a in agreements if a.get("agreement_status") == "DISAGREE")
    partial = sum(1 for a in agreements if a.get("agreement_status") == "PARTIAL")
    safety_override_count = sum(1 for a in agreements if a.get("safety_override") == "YES")
    follow_up_required = sum(1 for a in agreements if a.get("follow_up_required") == "YES")
    reviewed = sum(1 for e in enrollments if e.get("doctor_review_status") == "DOCTOR_REVIEW_COMPLETED")

    agreement_rate = round((agree / total_agreements) * 100, 2) if total_agreements else 0
    disagreement_rate = round((disagree / total_agreements) * 100, 2) if total_agreements else 0
    partial_rate = round((partial / total_agreements) * 100, 2) if total_agreements else 0
    review_completion_rate = round((reviewed / total_enrolled) * 100, 2) if total_enrolled else 0

    tp = 0
    tn = 0
    fp = 0
    fn = 0
    registry = []

    for a in agreements:
        ai_score = int(a.get("ai_risk_score") or 0)
        ai_level = str(a.get("ai_risk_level") or "").upper()
        doctor_decision = str(a.get("doctor_decision") or "").upper()
        follow = str(a.get("follow_up_required") or "").upper()

        ai_positive = ai_score >= 50 or ai_level in ["MODERATE", "HIGH", "CRITICAL"]
        doctor_positive = follow == "YES" or "FOLLOW" in doctor_decision or "URGENT" in doctor_decision

        if ai_positive and doctor_positive:
            tp += 1
            evidence_type = "TRUE_POSITIVE"
            reason = "AI risk and doctor decision both indicate follow-up or review."
            safety_impact = "SUPPORTS_PILOT_EVIDENCE"
        elif not ai_positive and not doctor_positive:
            tn += 1
            evidence_type = "TRUE_NEGATIVE"
            reason = "AI risk and doctor decision both indicate no immediate follow-up."
            safety_impact = "SUPPORTS_PILOT_EVIDENCE"
        elif ai_positive and not doctor_positive:
            fp += 1
            evidence_type = "FALSE_POSITIVE_CANDIDATE"
            reason = "AI indicates risk but doctor did not require follow-up."
            safety_impact = "REQUIRES_REVIEW"
        else:
            fn += 1
            evidence_type = "FALSE_NEGATIVE_CANDIDATE"
            reason = "Doctor required follow-up but AI did not indicate risk."
            safety_impact = "HIGH_SAFETY_REVIEW_REQUIRED"

        registry.append({
            "agreement_id": a.get("agreement_id"),
            "enrollment_id": a.get("enrollment_id"),
            "case_id": a.get("case_id"),
            "analysis_id": a.get("analysis_id"),
            "patient_id": a.get("patient_id"),
            "ai_risk_score": ai_score,
            "ai_risk_level": ai_level,
            "doctor_decision": a.get("doctor_decision"),
            "agreement_status": a.get("agreement_status"),
            "evidence_type": evidence_type,
            "evidence_reason": reason,
            "safety_impact": safety_impact
        })

    sensitivity = round((tp / (tp + fn)) * 100, 2) if (tp + fn) else 0
    specificity = round((tn / (tn + fp)) * 100, 2) if (tn + fp) else 0

    evidence_score = int(round((
        agreement_rate * 0.35 +
        review_completion_rate * 0.25 +
        (100 if safety_override_count == 0 else 70) * 0.20 +
        (100 if fn == 0 else 50) * 0.20
    ))) if total_agreements else 0

    if total_agreements == 0:
        evidence_status = "NO_VALIDATION_DATA"
    elif evidence_score >= 85 and fn == 0:
        evidence_status = "PILOT_EVIDENCE_STRONG_PROTOTYPE"
    elif evidence_score >= 70:
        evidence_status = "PILOT_EVIDENCE_MODERATE"
    else:
        evidence_status = "PILOT_EVIDENCE_NEEDS_REVIEW"

    regulatory_evidence_status = "PROTOTYPE_EVIDENCE_NOT_REGULATORY_SUBMISSION"
    clinical_production_status = "NOT_CERTIFIED"

    final_summary = (
        f"Phase 24 validation analytics generated from {total_enrolled} enrolled pilot case(s) "
        f"and {total_agreements} doctor agreement record(s). Agreement rate is {agreement_rate}%, "
        f"review completion is {review_completion_rate}%, false-negative candidates: {fn}, "
        f"false-positive candidates: {fp}. Evidence score: {evidence_score}%. "
        f"This remains prototype evidence and is not certified clinical performance."
    )

    protocol_id = enrollments[0].get("protocol_id") if enrollments else "NONE"

    conn.close()

    return {
        "protocol_id": protocol_id,
        "total_enrolled": total_enrolled,
        "total_agreements": total_agreements,
        "agreement_rate": agreement_rate,
        "disagreement_rate": disagreement_rate,
        "partial_agreement_rate": partial_rate,
        "review_completion_rate": review_completion_rate,
        "sensitivity_placeholder": sensitivity,
        "specificity_placeholder": specificity,
        "true_positive_count": tp,
        "true_negative_count": tn,
        "false_positive_count": fp,
        "false_negative_count": fn,
        "safety_override_count": safety_override_count,
        "follow_up_required_count": follow_up_required,
        "validation_evidence_score": evidence_score,
        "evidence_status": evidence_status,
        "regulatory_evidence_status": regulatory_evidence_status,
        "clinical_production_status": clinical_production_status,
        "final_summary": final_summary,
        "enrollments": enrollments,
        "agreements": agreements,
        "fp_fn_registry": registry
    }

def _phase24_save_evidence_report():
    _phase24_init_db()
    metrics = _phase24_collect_metrics()
    conn = _phase8_conn()
    now = datetime.utcnow().isoformat()

    old = conn.execute("""
    SELECT evidence_id FROM ophthalmology_validation_evidence_reports
    WHERE protocol_id=?
    ORDER BY created_at DESC
    LIMIT 1
    """, (metrics.get("protocol_id"),)).fetchone()

    evidence_id = old["evidence_id"] if old else "EYE-EVIDENCE-" + _phase8_uuid.uuid4().hex[:10].upper()

    if old:
        conn.execute("""
        UPDATE ophthalmology_validation_evidence_reports
        SET enrollment_count=?,
            agreement_count=?,
            agreement_rate=?,
            disagreement_rate=?,
            partial_agreement_rate=?,
            review_completion_rate=?,
            sensitivity_placeholder=?,
            specificity_placeholder=?,
            true_positive_count=?,
            true_negative_count=?,
            false_positive_count=?,
            false_negative_count=?,
            safety_override_count=?,
            follow_up_required_count=?,
            validation_evidence_score=?,
            evidence_status=?,
            regulatory_evidence_status=?,
            clinical_production_status=?,
            final_summary=?,
            updated_at=?
        WHERE evidence_id=?
        """, (
            metrics["total_enrolled"],
            metrics["total_agreements"],
            metrics["agreement_rate"],
            metrics["disagreement_rate"],
            metrics["partial_agreement_rate"],
            metrics["review_completion_rate"],
            metrics["sensitivity_placeholder"],
            metrics["specificity_placeholder"],
            metrics["true_positive_count"],
            metrics["true_negative_count"],
            metrics["false_positive_count"],
            metrics["false_negative_count"],
            metrics["safety_override_count"],
            metrics["follow_up_required_count"],
            metrics["validation_evidence_score"],
            metrics["evidence_status"],
            metrics["regulatory_evidence_status"],
            metrics["clinical_production_status"],
            metrics["final_summary"],
            now,
            evidence_id
        ))
    else:
        conn.execute("""
        INSERT INTO ophthalmology_validation_evidence_reports (
            evidence_id, protocol_id, enrollment_count, agreement_count,
            agreement_rate, disagreement_rate, partial_agreement_rate,
            review_completion_rate, sensitivity_placeholder, specificity_placeholder,
            true_positive_count, true_negative_count, false_positive_count,
            false_negative_count, safety_override_count, follow_up_required_count,
            validation_evidence_score, evidence_status, regulatory_evidence_status,
            clinical_production_status, final_summary, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            evidence_id,
            metrics["protocol_id"],
            metrics["total_enrolled"],
            metrics["total_agreements"],
            metrics["agreement_rate"],
            metrics["disagreement_rate"],
            metrics["partial_agreement_rate"],
            metrics["review_completion_rate"],
            metrics["sensitivity_placeholder"],
            metrics["specificity_placeholder"],
            metrics["true_positive_count"],
            metrics["true_negative_count"],
            metrics["false_positive_count"],
            metrics["false_negative_count"],
            metrics["safety_override_count"],
            metrics["follow_up_required_count"],
            metrics["validation_evidence_score"],
            metrics["evidence_status"],
            metrics["regulatory_evidence_status"],
            metrics["clinical_production_status"],
            metrics["final_summary"],
            now,
            now
        ))

    conn.execute("DELETE FROM ophthalmology_fp_fn_registry")
    for r in metrics.get("fp_fn_registry", []):
        registry_id = "EYE-FPFN-" + _phase8_uuid.uuid4().hex[:10].upper()
        conn.execute("""
        INSERT INTO ophthalmology_fp_fn_registry (
            registry_id, agreement_id, enrollment_id, case_id, analysis_id, patient_id,
            ai_risk_score, ai_risk_level, doctor_decision, agreement_status,
            evidence_type, evidence_reason, safety_impact, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            registry_id,
            r.get("agreement_id"),
            r.get("enrollment_id"),
            r.get("case_id"),
            r.get("analysis_id"),
            r.get("patient_id"),
            r.get("ai_risk_score"),
            r.get("ai_risk_level"),
            r.get("doctor_decision"),
            r.get("agreement_status"),
            r.get("evidence_type"),
            r.get("evidence_reason"),
            r.get("safety_impact"),
            now
        ))

    conn.commit()
    conn.close()

    metrics["evidence_id"] = evidence_id
    metrics["created_or_updated_at"] = now
    return metrics

@router.get("/phase-24/status")
async def phase24_status():
    metrics = _phase24_save_evidence_report()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 24",
        "features": [
            "pilot_validation_analytics",
            "performance_evidence_dashboard",
            "doctor_agreement_analytics",
            "sensitivity_specificity_prototype_metrics",
            "false_positive_registry",
            "false_negative_registry",
            "validation_evidence_score",
            "pilot_safety_evidence",
            "clinical_performance_summary",
            "regulatory_evidence_report",
            "html_pdf_multilingual_reports"
        ],
        "metrics": metrics,
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-24/dashboard")
async def phase24_dashboard():
    metrics = _phase24_save_evidence_report()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 24 Dashboard",
        "metrics": metrics,
        "agreement_distribution": [
            {"label": "AGREE", "value": sum(1 for a in metrics["agreements"] if a.get("agreement_status") == "AGREE")},
            {"label": "DISAGREE", "value": sum(1 for a in metrics["agreements"] if a.get("agreement_status") == "DISAGREE")},
            {"label": "PARTIAL", "value": sum(1 for a in metrics["agreements"] if a.get("agreement_status") == "PARTIAL")}
        ],
        "evidence_distribution": [
            {"label": "TRUE_POSITIVE", "value": metrics["true_positive_count"]},
            {"label": "TRUE_NEGATIVE", "value": metrics["true_negative_count"]},
            {"label": "FALSE_POSITIVE", "value": metrics["false_positive_count"]},
            {"label": "FALSE_NEGATIVE", "value": metrics["false_negative_count"]}
        ],
        "clinical_status": "prototype_not_certified",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-24/fp-fn-registry")
async def phase24_fp_fn_registry():
    metrics = _phase24_save_evidence_report()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 24 FP/FN Registry",
        "total_items": len(metrics.get("fp_fn_registry", [])),
        "registry": metrics.get("fp_fn_registry", [])
    }

@router.get("/phase-24/evidence-reports")
async def phase24_evidence_reports():
    _phase24_init_db()
    conn = _phase8_conn()
    rows = conn.execute("""
    SELECT *
    FROM ophthalmology_validation_evidence_reports
    ORDER BY updated_at DESC
    """).fetchall()
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 24 Evidence Reports",
        "total_reports": len(rows),
        "reports": [dict(r) for r in rows]
    }

def _phase24_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 24 - تحليلات Pilot وتقرير أدلة الأداء",
            "summary": "تقرير تحليلي لنتائج Pilot: توافق الطبيب، مؤشرات الحساسية والنوعية التجريبية، وسجل false positive / false negative.",
            "notice": "هذا دليل أداء تجريبي وليس تقرير اعتماد تنظيمي أو دراسة سريرية معتمدة."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 24 - Pilot Validation Analytics + Performance Evidence Report",
            "summary": "Pilot validation analytics report covering doctor agreement, prototype sensitivity/specificity and false positive/false negative registry.",
            "notice": "This is prototype performance evidence and not a certified regulatory or clinical validation report."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 24 - Pilotvalidering och prestandabevis",
            "summary": "Analysrapport för pilotvalidering med läkarsamstämmighet, prototypmått och FP/FN-register.",
            "notice": "Detta är prototypbevis och inte en certifierad klinisk valideringsrapport."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 24 - Validation pilote et preuves de performance",
            "summary": "Rapport analytique de validation pilote avec accord médecin, métriques prototype et registre FP/FN.",
            "notice": "Ceci est une preuve prototype, pas un rapport certifié de validation clinique."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 24 - Validazione pilota e prove prestazionali",
            "summary": "Report analitico pilota con accordo medico, metriche prototipo e registro FP/FN.",
            "notice": "Questa è evidenza prototipo, non un report clinico certificato."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-24/evidence-report-html")
async def phase24_evidence_report_html(language: str = "en"):
    metrics = _phase24_save_evidence_report()
    tx = _phase24_text(language)

    def fpfn_rows():
        out = ""
        for r in metrics.get("fp_fn_registry", []):
            out += f"""
            <tr>
              <td>{r.get('agreement_id')}</td>
              <td>{r.get('case_id')}</td>
              <td>{r.get('patient_id')}</td>
              <td>{r.get('ai_risk_score')} / {r.get('ai_risk_level')}</td>
              <td>{r.get('doctor_decision')}</td>
              <td>{r.get('evidence_type')}</td>
              <td>{r.get('safety_impact')}</td>
            </tr>
            """
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 24px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
  vertical-align: top;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Performance Evidence KPIs</h2>
<div class="grid">
  <div class="metric">Evidence Score<strong>{metrics.get('validation_evidence_score')}%</strong></div>
  <div class="metric">Agreement Rate<strong>{metrics.get('agreement_rate')}%</strong></div>
  <div class="metric">Review Completion<strong>{metrics.get('review_completion_rate')}%</strong></div>
  <div class="metric">Sensitivity Prototype<strong>{metrics.get('sensitivity_placeholder')}%</strong></div>
  <div class="metric">Specificity Prototype<strong>{metrics.get('specificity_placeholder')}%</strong></div>
  <div class="metric">True Positive<strong>{metrics.get('true_positive_count')}</strong></div>
  <div class="metric">False Positive<strong>{metrics.get('false_positive_count')}</strong></div>
  <div class="metric">False Negative<strong>{metrics.get('false_negative_count')}</strong></div>
</div>

<h2>Evidence Status</h2>
<div class="card">
<p><strong>Evidence ID:</strong> {metrics.get('evidence_id')}</p>
<p><strong>Protocol ID:</strong> {metrics.get('protocol_id')}</p>
<p><strong>Evidence Status:</strong> {metrics.get('evidence_status')}</p>
<p><strong>Regulatory Evidence:</strong> {metrics.get('regulatory_evidence_status')}</p>
<p><strong>Clinical Production:</strong> {metrics.get('clinical_production_status')}</p>
<p>{metrics.get('final_summary')}</p>
</div>

<h2>False Positive / False Negative Registry</h2>
<table>
<tr><th>Agreement</th><th>Case</th><th>Patient</th><th>AI Risk</th><th>Doctor Decision</th><th>Evidence Type</th><th>Safety Impact</th></tr>
{fpfn_rows()}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""

    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Content-Disposition": f"inline; filename=AHOS_Phase24_Performance_Evidence_Report_{language}.html"}
    )

@router.get("/phase-24/evidence-report-pdf")
async def phase24_evidence_report_pdf(language: str = "en"):
    metrics = _phase24_save_evidence_report()
    tx = _phase24_text(language)

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 24 Pilot Validation Analytics + Performance Evidence Report",
        "",
        tx["summary"],
        "",
        "Performance Evidence KPIs:",
        f"- Evidence ID: {metrics.get('evidence_id')}",
        f"- Protocol ID: {metrics.get('protocol_id')}",
        f"- Enrolled Cases: {metrics.get('total_enrolled')}",
        f"- Doctor Agreements: {metrics.get('total_agreements')}",
        f"- Agreement Rate: {metrics.get('agreement_rate')}%",
        f"- Disagreement Rate: {metrics.get('disagreement_rate')}%",
        f"- Partial Agreement Rate: {metrics.get('partial_agreement_rate')}%",
        f"- Review Completion Rate: {metrics.get('review_completion_rate')}%",
        f"- Sensitivity Prototype: {metrics.get('sensitivity_placeholder')}%",
        f"- Specificity Prototype: {metrics.get('specificity_placeholder')}%",
        f"- True Positive: {metrics.get('true_positive_count')}",
        f"- True Negative: {metrics.get('true_negative_count')}",
        f"- False Positive: {metrics.get('false_positive_count')}",
        f"- False Negative: {metrics.get('false_negative_count')}",
        f"- Safety Override Count: {metrics.get('safety_override_count')}",
        f"- Follow-up Required: {metrics.get('follow_up_required_count')}",
        f"- Validation Evidence Score: {metrics.get('validation_evidence_score')}%",
        "",
        "Evidence Status:",
        f"- Evidence Status: {metrics.get('evidence_status')}",
        f"- Regulatory Evidence: {metrics.get('regulatory_evidence_status')}",
        f"- Clinical Production: {metrics.get('clinical_production_status')}",
        "",
        "FP/FN Registry:"
    ]

    for i, r in enumerate(metrics.get("fp_fn_registry", []), start=1):
        lines += [
            f"{i}. Agreement ID: {r.get('agreement_id')}",
            f"   Case ID: {r.get('case_id')}",
            f"   Patient ID: {r.get('patient_id')}",
            f"   AI Risk: {r.get('ai_risk_score')} / {r.get('ai_risk_level')}",
            f"   Doctor Decision: {r.get('doctor_decision')}",
            f"   Evidence Type: {r.get('evidence_type')}",
            f"   Reason: {r.get('evidence_reason')}",
            f"   Safety Impact: {r.get('safety_impact')}",
            ""
        ]

    lines += [
        "Final Summary:",
        metrics.get("final_summary"),
        "",
        "Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=AHOS_Phase24_Performance_Evidence_Report_{language}.pdf"}
    )


# ============================
# AHOS Ophthalmology Phase 25
# Main Dashboard Integration + AHOS Command Center Linking
# ============================

def _phase25_safe_count(conn, table_name: str) -> int:
    try:
        row = conn.execute(f"SELECT COUNT(*) AS c FROM {table_name}").fetchone()
        return int(row["c"] if row else 0)
    except Exception:
        return 0

def _phase25_latest(conn, table_name: str, order_col: str = "created_at"):
    try:
        row = conn.execute(f"SELECT * FROM {table_name} ORDER BY {order_col} DESC LIMIT 1").fetchone()
        return dict(row) if row else None
    except Exception:
        return None

def _phase25_latest_report_file(folder: str):
    try:
        from pathlib import Path as _P
        base = _P(folder)
        if not base.exists():
            return None
        files = sorted(base.glob("*"), key=lambda x: x.stat().st_mtime, reverse=True)
        if not files:
            return None
        f = files[0]
        return {
            "name": f.name,
            "path": str(f),
            "size": f.stat().st_size
        }
    except Exception:
        return None

def _phase25_dashboard_payload():
    try:
        _phase24_init_db()
    except Exception:
        try:
            _phase23_init_db()
        except Exception:
            pass

    conn = _phase8_conn()

    cases = _phase25_safe_count(conn, "ophthalmology_cases")
    analyses = _phase25_safe_count(conn, "ophthalmology_ai_analyses")
    annotations = _phase25_safe_count(conn, "ophthalmology_doctor_annotations")
    reviews = _phase25_safe_count(conn, "ophthalmology_clinical_reviews")
    triage_items = _phase25_safe_count(conn, "ophthalmology_triage_queue")
    communications = _phase25_safe_count(conn, "ophthalmology_patient_communications")
    attendance = _phase25_safe_count(conn, "ophthalmology_attendance_outcomes")
    closed_loop = _phase25_safe_count(conn, "ophthalmology_closed_loop_pathways")
    pilot_readiness = _phase25_safe_count(conn, "ophthalmology_pilot_readiness")
    protocols = _phase25_safe_count(conn, "ophthalmology_pilot_protocols")
    enrollments = _phase25_safe_count(conn, "ophthalmology_pilot_enrollments")
    agreements = _phase25_safe_count(conn, "ophthalmology_doctor_agreements")
    evidence_reports = _phase25_safe_count(conn, "ophthalmology_validation_evidence_reports")

    latest_case = _phase25_latest(conn, "ophthalmology_cases", "updated_at")
    latest_analysis = _phase25_latest(conn, "ophthalmology_ai_analyses", "created_at")
    latest_review = _phase25_latest(conn, "ophthalmology_clinical_reviews", "created_at")
    latest_triage = _phase25_latest(conn, "ophthalmology_triage_queue", "created_at")
    latest_comm = _phase25_latest(conn, "ophthalmology_patient_communications", "created_at")
    latest_attendance = _phase25_latest(conn, "ophthalmology_attendance_outcomes", "created_at")
    latest_loop = _phase25_latest(conn, "ophthalmology_closed_loop_pathways", "updated_at")
    latest_readiness = _phase25_latest(conn, "ophthalmology_pilot_readiness", "updated_at")
    latest_protocol = _phase25_latest(conn, "ophthalmology_pilot_protocols", "updated_at")
    latest_evidence = _phase25_latest(conn, "ophthalmology_validation_evidence_reports", "updated_at")

    conn.close()

    completion_score = 0
    if latest_loop:
        completion_score = int(latest_loop.get("completion_score") or 0)

    pilot_readiness_score = 0
    if latest_readiness:
        pilot_readiness_score = int(latest_readiness.get("pilot_readiness_score") or 0)

    evidence_score = 0
    agreement_rate = 0
    if latest_evidence:
        evidence_score = int(latest_evidence.get("validation_evidence_score") or 0)
        agreement_rate = float(latest_evidence.get("agreement_rate") or 0)

    if evidence_score >= 85 and pilot_readiness_score >= 70 and completion_score >= 90:
        dashboard_status = "OPHTHALMOLOGY_READY_FOR_SUPERVISED_INTERNAL_PILOT"
    elif evidence_score >= 70:
        dashboard_status = "OPHTHALMOLOGY_PROTOTYPE_READY_WITH_LIMITATIONS"
    else:
        dashboard_status = "OPHTHALMOLOGY_NEEDS_MORE_VALIDATION"

    clinical_status = "NOT_CERTIFIED"
    regulatory_status = "PROTOTYPE_EVIDENCE_NOT_REGULATORY_SUBMISSION"

    safety_status = "NO_ACTIVE_SAFETY_INCIDENTS_RECORDED"
    if latest_evidence and int(latest_evidence.get("false_negative_count") or 0) > 0:
        safety_status = "SAFETY_REVIEW_REQUIRED_FALSE_NEGATIVE_CANDIDATE"

    linked_routes = {
        "ophthalmology_home": "/ophthalmology",
        "medical_departments": "/medical-departments",
        "command_center": "/ophthalmology-phase-16",
        "triage_queue": "/ophthalmology-phase-17",
        "communication_center": "/ophthalmology-phase-18",
        "attendance_center": "/ophthalmology-phase-19",
        "closed_loop": "/ophthalmology-phase-20",
        "pilot_readiness": "/ophthalmology-phase-21",
        "pilot_protocol": "/ophthalmology-phase-22",
        "agreement_tracking": "/ophthalmology-phase-23",
        "performance_evidence": "/ophthalmology-phase-24",
        "dashboard_integration": "/ophthalmology-dashboard-integration"
    }

    reports = {
        "phase20": _phase25_latest_report_file("reports/ophthalmology_phase20"),
        "phase21": _phase25_latest_report_file("reports/ophthalmology_phase21"),
        "phase22": _phase25_latest_report_file("reports/ophthalmology_phase22"),
        "phase23": _phase25_latest_report_file("reports/ophthalmology_phase23"),
        "phase24": _phase25_latest_report_file("reports/ophthalmology_phase24"),
    }

    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 25",
        "dashboard_status": dashboard_status,
        "clinical_status": clinical_status,
        "regulatory_status": regulatory_status,
        "safety_status": safety_status,
        "module": "Ophthalmology AI Eye Center",
        "kpis": {
            "cases": cases,
            "analyses": analyses,
            "annotations": annotations,
            "clinical_reviews": reviews,
            "triage_items": triage_items,
            "communications": communications,
            "attendance_outcomes": attendance,
            "closed_loop_pathways": closed_loop,
            "pilot_readiness_records": pilot_readiness,
            "pilot_protocols": protocols,
            "pilot_enrollments": enrollments,
            "doctor_agreements": agreements,
            "evidence_reports": evidence_reports,
            "closed_loop_completion_score": completion_score,
            "pilot_readiness_score": pilot_readiness_score,
            "performance_evidence_score": evidence_score,
            "doctor_agreement_rate": agreement_rate
        },
        "latest": {
            "case": latest_case,
            "analysis": latest_analysis,
            "clinical_review": latest_review,
            "triage": latest_triage,
            "communication": latest_comm,
            "attendance": latest_attendance,
            "closed_loop": latest_loop,
            "pilot_readiness": latest_readiness,
            "pilot_protocol": latest_protocol,
            "performance_evidence": latest_evidence
        },
        "linked_routes": linked_routes,
        "reports": reports,
        "summary": (
            f"Ophthalmology dashboard integration is active. Cases: {cases}, analyses: {analyses}, "
            f"closed-loop completion: {completion_score}%, pilot readiness: {pilot_readiness_score}%, "
            f"performance evidence score: {evidence_score}%, doctor agreement rate: {agreement_rate}%. "
            f"Clinical status remains NOT_CERTIFIED."
        )
    }

@router.get("/phase-25/status")
async def phase25_status():
    payload = _phase25_dashboard_payload()
    payload["features"] = [
        "main_dashboard_integration",
        "ophthalmology_command_center_card",
        "cross_phase_kpi_aggregation",
        "pilot_readiness_score_on_dashboard",
        "performance_evidence_score_on_dashboard",
        "doctor_agreement_rate_on_dashboard",
        "closed_loop_completion_score",
        "reports_linking",
        "ahos_command_center_linking",
        "multilingual_dashboard_bridge"
    ]
    payload["timestamp"] = datetime.utcnow().isoformat()
    return payload

@router.get("/phase-25/dashboard-card")
async def phase25_dashboard_card():
    payload = _phase25_dashboard_payload()
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 25 Dashboard Card",
        "title": "Ophthalmology AI Eye Center",
        "subtitle": "Integrated ophthalmology command center inside AHOS dashboard.",
        "dashboard_status": payload["dashboard_status"],
        "clinical_status": payload["clinical_status"],
        "kpis": payload["kpis"],
        "primary_route": "/ophthalmology-phase-16",
        "evidence_route": "/ophthalmology-phase-24",
        "reports_route": "/ophthalmology-dashboard-integration",
        "summary": payload["summary"],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/phase-25/command-center")
async def phase25_command_center():
    payload = _phase25_dashboard_payload()
    return {
        "status": "online",
        "phase": "AHOS Ophthalmology Phase 25 Command Center Links",
        "linked_routes": payload["linked_routes"],
        "reports": payload["reports"],
        "latest": payload["latest"],
        "clinical_status": payload["clinical_status"],
        "timestamp": datetime.utcnow().isoformat()
    }

def _phase25_text(language: str):
    lang = (language or "en").lower()
    data = {
        "ar": {
            "title": "AHOS Ophthalmology Phase 25 - ربط العيون بالدش بورد الرئيسي",
            "summary": "تقرير ربط قسم العيون مع الدش بورد الرئيسي ومركز القيادة داخل AHOS.",
            "notice": "هذا الربط تشغيلي تجريبي، ولا يعني اعتمادًا سريريًا أو تنظيميًا."
        },
        "en": {
            "title": "AHOS Ophthalmology Phase 25 - Main Dashboard Integration",
            "summary": "Dashboard integration report linking ophthalmology command center, pilot readiness, performance evidence and reports inside AHOS.",
            "notice": "This dashboard integration is operational prototype only and is not clinical or regulatory certification."
        },
        "sv": {
            "title": "AHOS Oftalmologi Fas 25 - Dashboardintegration",
            "summary": "Rapport som kopplar oftalmologi till AHOS huvuddashboard med beredskap, bevis och rapporter.",
            "notice": "Detta är en operativ prototyp och inte klinisk eller regulatorisk certifiering."
        },
        "fr": {
            "title": "AHOS Ophtalmologie Phase 25 - Intégration Dashboard",
            "summary": "Rapport reliant le centre ophtalmologie au dashboard AHOS avec préparation, preuves et rapports.",
            "notice": "Cette intégration est un prototype opérationnel, non une certification clinique ou réglementaire."
        },
        "it": {
            "title": "AHOS Oftalmologia Fase 25 - Integrazione Dashboard",
            "summary": "Report che collega il centro oftalmologico al dashboard AHOS con readiness, evidenze e report.",
            "notice": "Questa integrazione è un prototipo operativo, non certificazione clinica o regolatoria."
        }
    }
    return data.get(lang, data["en"])

@router.get("/phase-25/dashboard-report-html")
async def phase25_dashboard_report_html(language: str = "en"):
    payload = _phase25_dashboard_payload()
    tx = _phase25_text(language)
    k = payload["kpis"]
    routes = payload["linked_routes"]

    def route_rows():
        out = ""
        for name, route in routes.items():
            out += f"<tr><td>{name}</td><td>{route}</td></tr>"
        return out

    html = f"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{tx['title']}</title>
<style>
body {{
  font-family: Arial, sans-serif;
  background: #f8fafc;
  color: #0f172a;
  margin: 40px;
  line-height: 1.6;
}}
h1, h2 {{ color: #0891b2; }}
.card {{
  background: white;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
  padding: 18px;
  margin: 14px 0;
}}
.grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}}
.metric {{
  background: #ecfeff;
  border: 1px solid #67e8f9;
  border-radius: 12px;
  padding: 14px;
}}
.metric strong {{
  display: block;
  color: #0e7490;
  font-size: 22px;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  background: white;
  margin: 14px 0;
}}
td, th {{
  border: 1px solid #cbd5e1;
  padding: 9px;
}}
th {{ background: #e0f2fe; }}
.notice {{
  background: #fffbeb;
  border: 1px solid #f59e0b;
  border-radius: 12px;
  padding: 14px;
}}
</style>
</head>
<body>
<h1>{tx['title']}</h1>

<div class="card">
<p>{tx['summary']}</p>
<p><strong>Project:</strong> AI Hospital Alliance / AHOS</p>
<p><strong>Module:</strong> Ophthalmology AI Eye Center</p>
<p><strong>Generated:</strong> {datetime.utcnow().isoformat()} UTC</p>
</div>

<h2>Dashboard Summary</h2>
<div class="card">
<p><strong>Dashboard Status:</strong> {payload['dashboard_status']}</p>
<p><strong>Clinical Status:</strong> {payload['clinical_status']}</p>
<p><strong>Regulatory Status:</strong> {payload['regulatory_status']}</p>
<p><strong>Safety Status:</strong> {payload['safety_status']}</p>
<p>{payload['summary']}</p>
</div>

<h2>Ophthalmology Dashboard KPIs</h2>
<div class="grid">
  <div class="metric">Cases<strong>{k['cases']}</strong></div>
  <div class="metric">AI Analyses<strong>{k['analyses']}</strong></div>
  <div class="metric">Reviews<strong>{k['clinical_reviews']}</strong></div>
  <div class="metric">Triage Items<strong>{k['triage_items']}</strong></div>
  <div class="metric">Closed-loop<strong>{k['closed_loop_completion_score']}%</strong></div>
  <div class="metric">Pilot Readiness<strong>{k['pilot_readiness_score']}%</strong></div>
  <div class="metric">Evidence Score<strong>{k['performance_evidence_score']}%</strong></div>
  <div class="metric">Agreement Rate<strong>{k['doctor_agreement_rate']}%</strong></div>
</div>

<h2>AHOS Command Center Links</h2>
<table>
<tr><th>Link</th><th>Route</th></tr>
{route_rows()}
</table>

<div class="notice"><p>{tx['notice']}</p></div>
</body>
</html>
"""
    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Content-Disposition": f"inline; filename=AHOS_Phase25_Dashboard_Integration_{language}.html"}
    )

@router.get("/phase-25/dashboard-report-pdf")
async def phase25_dashboard_report_pdf(language: str = "en"):
    payload = _phase25_dashboard_payload()
    tx = _phase25_text(language)
    k = payload["kpis"]

    lines = [
        tx["title"],
        "",
        "Project: AI Hospital Alliance / AHOS",
        "Module: Ophthalmology AI Eye Center",
        "Phase: 25 Main Dashboard Integration + AHOS Command Center Linking",
        "",
        tx["summary"],
        "",
        "Dashboard Summary:",
        f"- Dashboard Status: {payload['dashboard_status']}",
        f"- Clinical Status: {payload['clinical_status']}",
        f"- Regulatory Status: {payload['regulatory_status']}",
        f"- Safety Status: {payload['safety_status']}",
        "",
        "Ophthalmology Dashboard KPIs:",
        f"- Cases: {k['cases']}",
        f"- AI Analyses: {k['analyses']}",
        f"- Annotations: {k['annotations']}",
        f"- Clinical Reviews: {k['clinical_reviews']}",
        f"- Triage Items: {k['triage_items']}",
        f"- Communications: {k['communications']}",
        f"- Attendance Outcomes: {k['attendance_outcomes']}",
        f"- Closed-loop Completion Score: {k['closed_loop_completion_score']}%",
        f"- Pilot Readiness Score: {k['pilot_readiness_score']}%",
        f"- Performance Evidence Score: {k['performance_evidence_score']}%",
        f"- Doctor Agreement Rate: {k['doctor_agreement_rate']}%",
        "",
        "Command Center Routes:"
    ]

    for name, route in payload["linked_routes"].items():
        lines.append(f"- {name}: {route}")

    lines += [
        "",
        "Final Summary:",
        payload["summary"],
        "",
        "Safety Notice:",
        tx["notice"],
        "",
        f"Generated at: {datetime.utcnow().isoformat()} UTC"
    ]

    pdf = _phase8_make_pdf(lines)

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=AHOS_Phase25_Dashboard_Integration_{language}.pdf"}
    )
