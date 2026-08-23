import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_tamper_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_integrity_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT UNIQUE,
        report_id TEXT,
        severity TEXT,
        alert_type TEXT,
        message TEXT,
        verification_status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_locked_report(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
    SELECT report_id, lock_hash, signature_hash, signed_by
    FROM rsna_locked_reports
    WHERE report_id = ?
    """, (report_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_latest_block(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
    SELECT report_id, block_hash, lock_hash, signature_hash, signed_by
    FROM rsna_report_blockchain
    WHERE report_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (report_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def create_alert(report_id: str, severity: str, alert_type: str, message: str, verification_status: str):
    init_tamper_db()

    payload = {
        "report_id": report_id,
        "severity": severity,
        "alert_type": alert_type,
        "message": message,
        "verification_status": verification_status,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    alert_id = "ALERT-" + hashlib.sha256(raw.encode()).hexdigest()[:24]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO rsna_integrity_alerts (
        alert_id,
        report_id,
        severity,
        alert_type,
        message,
        verification_status,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        alert_id,
        report_id,
        severity,
        alert_type,
        message,
        verification_status,
        payload["created_at"]
    ))

    conn.commit()
    conn.close()

    return {
        "alert_id": alert_id,
        "severity": severity,
        "alert_type": alert_type,
        "message": message,
        "verification_status": verification_status
    }

def verify_integrity(report_id: str):
    init_tamper_db()

    locked = get_locked_report(report_id)
    block = get_latest_block(report_id)

    if not locked:
        return create_alert(
            report_id,
            "HIGH",
            "LOCK_RECORD_MISSING",
            "Locked report record is missing.",
            "FAILED"
        )

    if not block:
        return create_alert(
            report_id,
            "HIGH",
            "BLOCKCHAIN_RECORD_MISSING",
            "Blockchain verification record is missing.",
            "FAILED"
        )

    issues = []

    if locked["lock_hash"] != block["lock_hash"]:
        issues.append("LOCK_HASH_MISMATCH")

    if locked["signature_hash"] != block["signature_hash"]:
        issues.append("SIGNATURE_HASH_MISMATCH")

    if locked["signed_by"] != block["signed_by"]:
        issues.append("SIGNER_MISMATCH")

    if issues:
        return create_alert(
            report_id,
            "CRITICAL",
            "INTEGRITY_VIOLATION",
            "Detected integrity violation: " + ", ".join(issues),
            "TAMPERED"
        )

    return {
        "status": "clean",
        "phase": "AHOS 41.2.8",
        "report_id": report_id,
        "verification_status": "VERIFIED_CLEAN",
        "message": "No tampering detected."
    }

def list_integrity_alerts(limit: int = 20):
    init_tamper_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        alert_id,
        report_id,
        severity,
        alert_type,
        message,
        verification_status,
        created_at
    FROM rsna_integrity_alerts
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows

def simulate_tamper(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    UPDATE rsna_locked_reports
    SET lock_hash = 'TAMPERED_LOCK_HASH'
    WHERE report_id = ?
    """, (report_id,))

    conn.commit()
    conn.close()

    return {
        "status": "simulated",
        "report_id": report_id,
        "message": "Lock hash was intentionally modified for tamper detection test."
    }
