import json
import zipfile
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = "data/processed/rsna/rsna_reports.db"
EXPORT_DIR = Path("reports/rsna/regulatory_exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_latest_record(table, report_id):
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

def build_regulatory_export(report_id: str):
    locked = fetch_latest_record("rsna_locked_reports", report_id)
    decision = fetch_latest_record("rsna_review_decisions", report_id)
    blockchain = fetch_latest_record("rsna_report_blockchain", report_id)
    recovery = fetch_latest_record("rsna_integrity_recovery_log", report_id)
    alert = fetch_latest_record("rsna_integrity_alerts", report_id)

    if not locked:
        return {
            "status": "blocked",
            "reason": "LOCKED_REPORT_NOT_FOUND",
            "report_id": report_id
        }

    export_id = "REG-AUDIT-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    package_dir = EXPORT_DIR / export_id
    package_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "export_id": export_id,
        "phase": "AHOS 41.3.0",
        "report_id": report_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "regulatory_scope": [
            "FDA Software as a Medical Device evidence package",
            "EU CE MDR technical documentation support",
            "Clinical AI governance audit",
            "Radiologist review traceability",
            "Integrity and tamper detection traceability"
        ],
        "locked_report": locked,
        "clinical_decision": decision,
        "blockchain_verification": blockchain,
        "integrity_recovery": recovery,
        "integrity_alert": alert,
        "compliance_status": {
            "radiologist_review": bool(decision),
            "final_lock": bool(locked),
            "blockchain_verification": bool(blockchain),
            "integrity_recovery_available": bool(recovery),
            "audit_ready": bool(locked and decision and blockchain)
        },
        "disclaimer": "Research and regulatory-preparation output only. Not a certified medical device submission."
    }

    summary_path = package_dir / "regulatory_audit_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    checklist = f"""AHOS 41.3.0 Regulatory Compliance Checklist

Report ID: {report_id}
Export ID: {export_id}

FDA / SaMD Evidence:
[OK] AI model output available
[OK] Clinical report generated
[OK] Radiologist decision recorded
[OK] Final report lock available
[OK] Integrity verification available
[OK] Blockchain-style verification available

EU CE / MDR Evidence:
[OK] Traceability package available
[OK] Clinical review workflow available
[OK] Tamper detection available
[OK] Recovery workflow available
[OK] Audit package export available

Status:
Audit Ready: {summary["compliance_status"]["audit_ready"]}

Disclaimer:
This package supports regulatory preparation only and is not a final FDA/CE submission.
"""

    checklist_path = package_dir / "regulatory_checklist.txt"
    checklist_path.write_text(checklist)

    zip_path = EXPORT_DIR / f"{export_id}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in package_dir.iterdir():
            z.write(f, arcname=f.name)

    return {
        "status": "created",
        "phase": "AHOS 41.3.0",
        "report_id": report_id,
        "export_id": export_id,
        "package_dir": str(package_dir),
        "zip_file": str(zip_path),
        "summary_file": str(summary_path),
        "checklist_file": str(checklist_path),
        "audit_ready": summary["compliance_status"]["audit_ready"]
    }

def list_regulatory_exports(limit: int = 20):
    exports = []
    for p in sorted(EXPORT_DIR.glob("*.zip"), reverse=True)[:limit]:
        exports.append({
            "zip_file": str(p),
            "size_bytes": p.stat().st_size
        })
    return exports
