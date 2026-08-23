import json
from pathlib import Path
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

PDF_DIR = "reports/rsna/pdf"
JSON_DIR = "reports/rsna/json"

Path(PDF_DIR).mkdir(parents=True, exist_ok=True)
Path(JSON_DIR).mkdir(parents=True, exist_ok=True)


def export_json(report):

    report_id = report["report_id"]

    path = f"{JSON_DIR}/{report_id}.json"

    with open(path, "w") as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False
        )

    return path


def export_pdf(report):

    report_id = report["report_id"]

    path = f"{PDF_DIR}/{report_id}.pdf"

    doc = SimpleDocTemplate(path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            f"<b>AHOS RSNA Clinical Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    fields = [
        ("Report ID", report["report_id"]),
        ("Generated At", report["generated_at"]),
        ("Model", report["ai_model"]),
        ("Threshold", str(report["threshold"])),
        (
            "Probability",
            str(
                report["ai_result"][
                    "pneumonia_probability"
                ]
            )
        ),
        (
            "Prediction",
            report["ai_result"]["prediction"]
        ),
        (
            "Risk",
            report["ai_result"]["risk_level"]
        ),
        (
            "Impression",
            report["clinical_report"][
                "impression"
            ]
        ),
        (
            "Recommendation",
            report["clinical_report"][
                "recommendation"
            ]
        )
    ]

    for title, value in fields:

        story.append(
            Paragraph(
                f"<b>{title}</b>: {value}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 8))

    doc.build(story)

    return path
