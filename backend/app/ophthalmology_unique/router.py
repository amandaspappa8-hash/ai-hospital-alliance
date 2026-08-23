from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

router = APIRouter(
    prefix="/api/ophthalmology",
    tags=["AHOS Official Ophthalmology Intelligence System"]
)

class OphthalmologyDiagnosisRequest(BaseModel):
    patient_id: Optional[str] = "DEMO-EYE-001"
    language: Optional[str] = "ar"
    selected_module: Optional[str] = "retina"
    symptoms: Optional[str] = ""
    iop: Optional[float] = None
    diabetes: Optional[bool] = False
    hypertension: Optional[bool] = False
    visual_loss: Optional[bool] = False
    severe_pain: Optional[bool] = False

def risk_engine(req: OphthalmologyDiagnosisRequest) -> Dict[str, Any]:
    score = 22

    module_weight = {
        "retina": 16,
        "oct": 20,
        "glaucoma": 30,
        "fundus": 14,
        "emergency": 58
    }

    score += module_weight.get((req.selected_module or "retina").lower(), 16)

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
            "urgency": "urgent_ophthalmologist_review",
            "safety_gate": "REQUIRES_DOCTOR_REVIEW"
        }

    if score >= 45:
        return {
            "risk_score": score,
            "risk_level": "MODERATE",
            "urgency": "specialist_follow_up_required",
            "safety_gate": "REVIEW_RECOMMENDED"
        }

    return {
        "risk_score": score,
        "risk_level": "LOW",
        "urgency": "routine_follow_up",
        "safety_gate": "DEMO_SAFE"
    }

# AHOS R13C.16E: secondary duplicate route disabled; canonical runtime owner retained.
# @router.get("/health")
async def health():
    return {
        "status": "ONLINE",
        "module": "AHOS Official Ophthalmology Intelligence System",
        "clinical_status": "prototype_not_certified",
        "frontend_route": "/ophthalmology",
        "preview_page": "/ophthalmology-preview.html",
        "version": "1.0.0",
        "features": [
            "retina_screening",
            "oct_layer_analysis",
            "glaucoma_risk_ai",
            "fundus_image_ai",
            "visual_acuity_context",
            "clinical_safety_gate",
            "multilingual_eye_report"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

# AHOS R13C.16E: secondary duplicate route disabled; canonical runtime owner retained.
# @router.get("/kpis")
async def kpis():
    return {
        "status": "ONLINE",
        "eye_scans": 12,
        "retina_screenings": 4,
        "oct_studies": 3,
        "glaucoma_alerts": 2,
        "critical_eye_cases": 1,
        "fundus_images_ready": True,
        "oct_ready": True,
        "safety_gate": "ACTIVE",
        "average_eye_risk_score": 78,
        "selected_specialty": "Ophthalmology",
        "selected_organ": "Eyes"
    }

# AHOS R13C.16E: secondary duplicate route disabled; canonical runtime owner retained.
# @router.post("/diagnose")
async def diagnose(req: OphthalmologyDiagnosisRequest):
    risk = risk_engine(req)

    interpretation = {
        "ar": "تحليل تجريبي لقسم العيون يربط الشبكية، OCT، الجلوكوما، قاع العين، ضغط العين، والأعراض مع بوابة أمان سريرية.",
        "en": "Experimental ophthalmology AI interpretation connecting retina, OCT, glaucoma, fundus, IOP, and symptoms with a clinical safety gate.",
        "sv": "Experimentell AI-tolkning för ögon som kopplar näthinna, OCT, glaukom, ögonbotten, ögontryck och symtom till säkerhetsgranskning.",
        "fr": "Interprétation IA ophtalmologique expérimentale reliant rétine, OCT, glaucome, fond d’œil, pression intraoculaire et symptômes.",
        "it": "Interpretazione AI oftalmologica sperimentale che collega retina, OCT, glaucoma, fondo oculare, pressione e sintomi."
    }

    return {
        "patient_id": req.patient_id,
        "selected_module": req.selected_module,
        "language": req.language,
        **risk,
        "ai_interpretation": interpretation.get(req.language or "en", interpretation["en"]),
        "required_before_real_use": [
            "real_fundus_images",
            "real_oct_data",
            "device_integration",
            "ophthalmologist_validation",
            "audit_logs",
            "regulatory_evidence"
        ],
        "clinical_notice": "Prototype only. Not a certified diagnosis. Physician review is required.",
        "timestamp": datetime.utcnow().isoformat()
    }

def simple_pdf(text: str) -> bytes:
    safe = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 11 Tf 50 780 Td 14 TL ({safe}) Tj ET"
    objects = []
    objects.append("1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj")
    objects.append("2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj")
    objects.append("3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj")
    objects.append(f"4 0 obj << /Length {len(stream.encode('latin-1', errors='ignore'))} >> stream\n{stream}\nendstream endobj")
    objects.append("5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj")
    pdf = "%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf.encode("latin-1", errors="ignore")))
        pdf += obj + "\n"
    xref_pos = len(pdf.encode("latin-1", errors="ignore"))
    pdf += f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n"
    for off in offsets[1:]:
        pdf += f"{off:010d} 00000 n \n"
    pdf += f"trailer << /Root 1 0 R /Size {len(objects)+1} >>\nstartxref\n{xref_pos}\n%%EOF"
    return pdf.encode("latin-1", errors="ignore")

# AHOS R13C.16E: secondary duplicate route disabled; canonical runtime owner retained.
# @router.get("/report-pdf")
async def report_pdf():
    text = (
        "AHOS Official Ophthalmology AI Report - Prototype Only\\n"
        "Module: Retina / OCT / Glaucoma / Fundus / Safety Gate\\n"
        "Status: Demo operational. Not certified clinical diagnosis.\\n"
        "Required: real fundus images, OCT data, validation, audit, regulatory evidence."
    )
    return Response(
        content=simple_pdf(text),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=AHOS_Ophthalmology_Report.pdf"}
    )
