import json
from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image
)
from reportlab.lib.styles import getSampleStyleSheet

PDF_DIR = "reports/rsna/pdf"
JSON_DIR = "reports/rsna/json"

Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
Path(JSON_DIR).mkdir(parents=True, exist_ok=True)


def export_json_xai(report):
    report_id = report["report_id"]
    path = f"{JSON_DIR}/{report_id}_xai.json"

    with open(path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return path


def export_pdf_xai(report):
    report_id = report["report_id"]
    path = f"{PDF_DIR}/{report_id}_xai.pdf"

    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AHOS RSNA Explainable AI Clinical Report</b>", styles["Title"]))
    story.append(Spacer(1, 18))

    ai = report.get("ai_result", {})
    clinical = report.get("clinical_report", {})
    xai = report.get("xai", {})

    fields = [
        ("Report ID", report.get("report_id")),
        ("Generated At", report.get("generated_at")),
        ("Model", report.get("ai_model")),
        ("Threshold", str(report.get("threshold"))),
        ("Probability", str(ai.get("pneumonia_probability"))),
        ("Prediction", ai.get("prediction")),
        ("Risk", ai.get("risk_level")),
        ("Impression", clinical.get("impression")),
        ("Recommendation", clinical.get("recommendation")),
        ("XAI Heatmap", xai.get("heatmap")),
        ("XAI Overlay", xai.get("overlay")),
    ]

    for title, value in fields:
        story.append(Paragraph(f"<b>{title}</b>: {value}", styles["BodyText"]))
        story.append(Spacer(1, 8))

    overlay = xai.get("overlay")
    heatmap = xai.get("heatmap")

    if overlay and Path(overlay).exists():
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Grad-CAM Overlay</b>", styles["Heading2"]))
        story.append(Image(overlay, width=300, height=300))

    if heatmap and Path(heatmap).exists():
        story.append(Spacer(1, 12))
        story.append(Paragraph("<b>Grad-CAM Heatmap</b>", styles["Heading2"]))
        story.append(Image(heatmap, width=300, height=300))

    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>Disclaimer:</b> This is an AI-assisted research output, not a final medical diagnosis. "
        "Final interpretation must be made by a licensed radiologist.",
        styles["BodyText"]
    ))

    doc.build(story)
    return path
