import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_lock_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_locked_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lock_id TEXT UNIQUE,
        report_id TEXT UNIQUE,
        final_status TEXT,
        signed_by TEXT,
        signature_hash TEXT,
        lock_hash TEXT,
        immutable_notice TEXT,
        locked_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_latest_decision(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        decision,
        clinical_status,
        reviewer_name,
        comments,
        created_at
    FROM rsna_review_decisions
    WHERE report_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

def create_signature_hash(report_id: str, signed_by: str, decision: dict):
    payload = {
        "report_id": report_id,
        "signed_by": signed_by,
        "decision": decision,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def lock_report(report_id: str, signed_by: str):
    init_lock_db()

    decision = get_latest_decision(report_id)

    if not decision:
        return {
            "status": "blocked",
            "reason": "NO_REVIEW_DECISION_FOUND",
            "report_id": report_id
        }

    if decision["decision"] != "APPROVED":
        return {
            "status": "blocked",
            "reason": "LATEST_DECISION_NOT_APPROVED",
            "latest_decision": decision["decision"],
            "report_id": report_id
        }

    signature_hash = create_signature_hash(report_id, signed_by, decision)

    lock_payload = {
        "report_id": report_id,
        "signed_by": signed_by,
        "signature_hash": signature_hash,
        "decision": decision,
    }

    lock_hash = hashlib.sha256(
        json.dumps(lock_payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

    lock_id = "LOCK-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO rsna_locked_reports (
        lock_id,
        report_id,
        final_status,
        signed_by,
        signature_hash,
        lock_hash,
        immutable_notice,
        locked_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lock_id,
        report_id,
        "FINAL_LOCKED_APPROVED",
        signed_by,
        signature_hash,
        lock_hash,
        "This report is locked after radiologist approval and should be treated as immutable clinical documentation.",
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "locked",
        "lock_id": lock_id,
        "report_id": report_id,
        "final_status": "FINAL_LOCKED_APPROVED",
        "signed_by": signed_by,
        "signature_hash": signature_hash,
        "lock_hash": lock_hash
    }

def get_lock_status(report_id: str):
    init_lock_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        lock_id,
        report_id,
        final_status,
        signed_by,
        signature_hash,
        lock_hash,
        immutable_notice,
        locked_at
    FROM rsna_locked_reports
    WHERE report_id = ?
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {
            "status": "unlocked",
            "report_id": report_id
        }

    return dict(row)

def list_locked_reports(limit: int = 20):
    init_lock_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        lock_id,
        report_id,
        final_status,
        signed_by,
        locked_at
    FROM rsna_locked_reports
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows
