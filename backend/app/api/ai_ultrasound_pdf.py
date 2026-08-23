from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from pathlib import Path
from datetime import datetime
import qrcode

router = APIRouter(prefix="/ai-ultrasound-x/pdf", tags=["AI Ultrasound X PDF"])

PDF_DIR = Path("generated_reports")
PDF_DIR.mkdir(exist_ok=True)

ASSET_LOGOS = [
    Path("../src/assets/hospital-logo.png"),
    Path("../src/assets/logo.png"),
    Path("static/hospital-logo.png"),
]

def find_logo():
    for logo in ASSET_LOGOS:
        if logo.exists():
            return logo
    return None

@router.get("/verify/{report_id}")
def verify_report(report_id: str):
    return {
        "status": "verified",
        "report_id": report_id,
        "system": "AI Hospital Alliance",
        "module": "AI Ultrasound X",
        "verification": "Prototype QR verification active"
    }

@router.get("/generate/{report_id}")
def generate_pdf(report_id: str):
    pdf_path = PDF_DIR / f"{report_id}.pdf"
    qr_path = PDF_DIR / f"{report_id}_qr.png"

    verify_url = f"http://127.0.0.1:8000/ai-ultrasound-x/pdf/verify/{report_id}"
    qrcode.make(verify_url).save(qr_path)

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    logo = find_logo()
    if logo:
        elements.append(Image(str(logo), width=80, height=80))
        elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>AI Ultrasound X Clinical Report</b>", styles["Title"]))
    elements.append(Paragraph("<b>AI Hospital Alliance</b>", styles["Heading2"]))
    elements.append(Spacer(1, 16))

    elements.append(Paragraph(f"Generated: {datetime.utcnow().isoformat()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    data = [
        ["Field", "Value"],
        ["Report ID", report_id],
        ["Patient ID", "P-1001"],
        ["Patient Name", "Test Patient"],
        ["Study Type", "Ultrasound"],
        ["AI Model", "MONAI UNet"],
        ["Confidence", "51%"],
        ["Risk Level", "MODERATE"],
        ["Lesion Area", "28876"],
        ["Status", "AI Analysis Completed"],
    ]

    table = Table(data, colWidths=[180, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#00d4ff")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.black),
        ("GRID", (0,0), (-1,-1), 1, colors.HexColor("#374151")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 12),
        ("TOPPADDING", (0,0), (-1,-1), 10),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    elements.append(Paragraph(
        "<b>AI Findings:</b><br/>"
        "AI Ultrasound X generated this prototype medical imaging report using MONAI UNet. "
        "This report is prepared for future DICOM, heatmap, and surgical navigation integration.",
        styles["BodyText"]
    ))

    elements.append(Spacer(1, 30))

    signature_table = Table([
        ["Doctor Signature", "AI Verification QR"],
        ["__________________________", Image(str(qr_path), width=90, height=90)],
        ["Doctor Name: __________________", f"Verify ID: {report_id}"],
    ], colWidths=[300, 180])

    signature_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#9ca3af")),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (1,1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))

    elements.append(signature_table)

    doc.build(elements)

    return FileResponse(
        path=str(pdf_path),
        filename=f"{report_id}.pdf",
        media_type="application/pdf"
    )
