import json
import sqlite3
from pathlib import Path
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

DB_PATH = "data/processed/rsna/rsna_reports.db"
DOSSIER_DIR = Path("reports/rsna/regulatory_dossiers")
DOSSIER_DIR.mkdir(parents=True, exist_ok=True)

def fetch_latest(table, report_id):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f"SELECT * FROM {table} WHERE report_id = ? ORDER BY id DESC LIMIT 1",
        (report_id,)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def generate_regulatory_pdf_dossier(report_id: str):
    locked = fetch_latest("rsna_locked_reports", report_id)
    decision = fetch_latest("rsna_review_decisions", report_id)
    blockchain = fetch_latest("rsna_report_blockchain", report_id)
    recovery = fetch_latest("rsna_integrity_recovery_log", report_id)
    alert = fetch_latest("rsna_integrity_alerts", report_id)

    if not locked:
        return {
            "status": "blocked",
            "reason": "LOCKED_REPORT_NOT_FOUND",
            "report_id": report_id
        }

    dossier_id = "REG-DOSSIER-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    pdf_path = DOSSIER_DIR / f"{dossier_id}.pdf"
    json_path = DOSSIER_DIR / f"{dossier_id}.json"

    data = {
        "dossier_id": dossier_id,
        "phase": "AHOS 41.3.1",
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "locked_report": locked,
        "clinical_decision": decision,
        "blockchain_verification": blockchain,
        "integrity_recovery": recovery,
        "integrity_alert": alert,
        "regulatory_statement": {
            "fda_samd": "Evidence supports Software as a Medical Device regulatory preparation.",
            "eu_mdr_ce": "Evidence supports EU MDR / CE technical documentation preparation.",
            "clinical_governance": "Radiologist review, lock, verification, and recovery workflow documented.",
            "disclaimer": "This is a research regulatory dossier and not a final official FDA/CE submission."
        }
    }

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AHOS 41.3.1 Regulatory PDF Dossier", styles["Title"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph(f"Dossier ID: {dossier_id}", styles["Normal"]))
    story.append(Paragraph(f"Report ID: {report_id}", styles["Normal"]))
    story.append(Paragraph(f"Generated At: {data['created_at']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("1. Executive Regulatory Summary", styles["Heading2"]))
    story.append(Paragraph("This dossier consolidates radiology AI governance evidence for FDA SaMD and EU CE/MDR preparation.", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2. Final Locked Report", styles["Heading2"]))
    for k, v in (locked or {}).items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Clinical Review Decision", styles["Heading2"]))
    for k, v in (decision or {}).items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4. Blockchain-Style Verification", styles["Heading2"]))
    for k, v in (blockchain or {}).items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("5. Integrity Recovery", styles["Heading2"]))
    for k, v in (recovery or {}).items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. Integrity Alerts", styles["Heading2"]))
    if alert:
        for k, v in alert.items():
            story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))
    else:
        story.append(Paragraph("No active integrity alerts found.", styles["Normal"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. FDA / CE Readiness Statement", styles["Heading2"]))
    for k, v in data["regulatory_statement"].items():
        story.append(Paragraph(f"<b>{k}</b>: {v}", styles["Normal"]))

    doc = SimpleDocTemplate(str(pdf_path))
    doc.build(story)

    return {
        "status": "created",
        "phase": "AHOS 41.3.1",
        "report_id": report_id,
        "dossier_id": dossier_id,
        "pdf_file": str(pdf_path),
        "json_file": str(json_path)
    }

def list_regulatory_dossiers(limit: int = 20):
    files = []
    for p in sorted(DOSSIER_DIR.glob("*.pdf"), reverse=True)[:limit]:
        files.append({
            "pdf_file": str(p),
            "size_bytes": p.stat().st_size
        })
    return files
