from datetime import datetime
from typing import Any, Dict, Optional
import re

from fastapi import APIRouter
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter(prefix="/api/avatar/v3", tags=["AHOS Avatar V3 Command"])


class AvatarV3CommandRequest(BaseModel):
    organ: Optional[str] = "Brain"
    department: Optional[str] = "None"
    language: Optional[str] = "EN"
    kpis: Optional[Dict[str, Any]] = {}
    command: Optional[str] = "Generate avatar medical report"


@router.get("/health")
async def health():
    return {
        "status": "online",
        "module": "AHOS Medical Hologram Avatar V3 Command",
        "version": "3.0",
        "pdf_export": "enabled",
        "timestamp": datetime.utcnow().isoformat(),
    }


def build_avatar_report(payload: AvatarV3CommandRequest) -> Dict[str, Any]:
    organ = payload.organ or "Brain"
    department = payload.department or "None"
    language = payload.language or "EN"
    kpis = payload.kpis or {}
    command = payload.command or "Generate avatar medical report"

    organ_context = {
        "Brain": "Neurology context: MRI review, neurological safety check, and physician validation are required.",
        "Heart": "Cardiology context: ECG, ultrasound, heart rate, and cardiovascular review are required.",
        "Lungs": "Pulmonology context: oxygen level, X-ray, respiratory status, and safety review are required.",
        "Liver": "Gastroenterology context: liver ultrasound, lab review, and hepatic safety assessment are required.",
        "Kidneys": "Nephrology context: renal ultrasound, kidney function, fluid balance, and safety review are required.",
    }

    interpretation = organ_context.get(
        organ,
        "General medical context: clinical safety review and physician validation are required.",
    )

    return {
        "title": "AHOS Avatar Medical Report",
        "status": "generated",
        "language": language,
        "selected_organ": organ,
        "selected_department": department,
        "received_command": command,
        "clinical_interpretation": interpretation,
        "dashboard_context": {
            "patients": kpis.get("total_patients", 0),
            "doctors": kpis.get("available_doctors", 0),
            "active_alerts": kpis.get("active_alerts", 0),
            "critical_alerts": kpis.get("critical_alerts", 0),
            "radiology_studies": kpis.get("radiology_studies", 0),
            "ultrasound_studies": kpis.get("ultrasound_studies", 0),
            "critical_lab_results": kpis.get("critical_lab_results", 0),
            "low_stock_drugs": kpis.get("low_stock_drugs", 0),
            "hospitals": kpis.get("hospitals", 0),
        },
        "safety_notice": (
            "Prototype response only. This is not a certified diagnosis. "
            "Physician review and clinical safety validation are required before real clinical use."
        ),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.post("/command")
async def avatar_command(payload: AvatarV3CommandRequest):
    return build_avatar_report(payload)


def pdf_escape(text: Any) -> str:
    s = str(text)
    s = s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    s = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "?", s)
    return s


def make_simple_pdf(lines):
    # Minimal valid PDF generated with standard Helvetica font.
    # Good for local demo export without external dependencies.
    objects = []
    stream_lines = ["BT", "/F1 12 Tf", "50 790 Td", "16 TL"]

    first = True
    for line in lines:
        safe = pdf_escape(line)
        if first:
            stream_lines.append(f"({safe}) Tj")
            first = False
        else:
            stream_lines.append("T*")
            stream_lines.append(f"({safe}) Tj")

    stream_lines.append("ET")
    stream = "\n".join(stream_lines).encode("latin-1", errors="replace")

    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
    )
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")

    pdf = bytearray()
    pdf.extend(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]

    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{i} 0 obj\n".encode())
        pdf.extend(obj)
        pdf.extend(b"\nendobj\n")

    xref_pos = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n".encode())
    pdf.extend(b"0000000000 65535 f \n")

    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())

    pdf.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    )
    return bytes(pdf)


@router.post("/report-pdf")
async def avatar_report_pdf(payload: AvatarV3CommandRequest):
    report = build_avatar_report(payload)
    ctx = report["dashboard_context"]

    lines = [
        "AHOS Avatar Medical Report",
        "Medical Hologram Avatar v3.0",
        "",
        f"Generated at: {report['timestamp']}",
        f"Language: {report['language']}",
        f"Selected organ: {report['selected_organ']}",
        f"Selected department: {report['selected_department']}",
        "",
        "Clinical interpretation:",
        report["clinical_interpretation"],
        "",
        "Live dashboard context:",
        f"Patients: {ctx['patients']}",
        f"Doctors: {ctx['doctors']}",
        f"Active alerts: {ctx['active_alerts']}",
        f"Critical alerts: {ctx['critical_alerts']}",
        f"Radiology studies: {ctx['radiology_studies']}",
        f"Ultrasound studies: {ctx['ultrasound_studies']}",
        f"Critical lab results: {ctx['critical_lab_results']}",
        f"Low stock drugs: {ctx['low_stock_drugs']}",
        f"Hospitals: {ctx['hospitals']}",
        "",
        "Safety notice:",
        report["safety_notice"],
        "",
        "Status: Prototype demo report. Not for real clinical diagnosis.",
    ]

    pdf_bytes = make_simple_pdf(lines)

    filename = f"AHOS_Avatar_V3_Report_{report['selected_organ']}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )
