import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_recovery_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_integrity_recovery_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recovery_id TEXT UNIQUE,
        report_id TEXT,
        action TEXT,
        old_lock_hash TEXT,
        new_lock_hash TEXT,
        old_signature_hash TEXT,
        new_signature_hash TEXT,
        recovery_status TEXT,
        recovered_by TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def get_latest_decision(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT decision, clinical_status, reviewer_name, comments, created_at
    FROM rsna_review_decisions
    WHERE report_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

def get_locked_report(report_id: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT report_id, lock_id, final_status, signed_by, signature_hash, lock_hash, locked_at
    FROM rsna_locked_reports
    WHERE report_id = ?
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

def get_latest_block_hash():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    SELECT block_hash
    FROM rsna_report_blockchain
    ORDER BY id DESC
    LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    return row[0] if row else "GENESIS"

def sha(payload: dict):
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()

def recover_integrity(report_id: str, recovered_by: str):
    init_recovery_db()

    decision = get_latest_decision(report_id)
    locked = get_locked_report(report_id)

    if not decision:
        return {
            "status": "blocked",
            "reason": "NO_DECISION_FOUND",
            "report_id": report_id
        }

    if decision["decision"] != "APPROVED":
        return {
            "status": "blocked",
            "reason": "LATEST_DECISION_NOT_APPROVED",
            "latest_decision": decision["decision"],
            "report_id": report_id
        }

    if not locked:
        return {
            "status": "blocked",
            "reason": "LOCK_RECORD_NOT_FOUND",
            "report_id": report_id
        }

    old_lock_hash = locked["lock_hash"]
    old_signature_hash = locked["signature_hash"]

    signature_payload = {
        "report_id": report_id,
        "signed_by": recovered_by,
        "decision": decision,
        "recovered_at": datetime.utcnow().isoformat() + "Z"
    }

    new_signature_hash = sha(signature_payload)

    lock_payload = {
        "report_id": report_id,
        "signed_by": recovered_by,
        "signature_hash": new_signature_hash,
        "decision": decision,
        "recovery": True
    }

    new_lock_hash = sha(lock_payload)

    recovery_id = "RECOVERY-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")
    new_lock_id = "LOCK-RECOVERED-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    UPDATE rsna_locked_reports
    SET
        lock_id = ?,
        final_status = ?,
        signed_by = ?,
        signature_hash = ?,
        lock_hash = ?,
        immutable_notice = ?,
        locked_at = ?
    WHERE report_id = ?
    """, (
        new_lock_id,
        "FINAL_LOCKED_APPROVED_RECOVERED",
        recovered_by,
        new_signature_hash,
        new_lock_hash,
        "Recovered and re-locked after integrity violation. Treat as immutable after recovery.",
        datetime.utcnow().isoformat() + "Z",
        report_id
    ))

    cur.execute("""
    INSERT INTO rsna_integrity_recovery_log (
        recovery_id,
        report_id,
        action,
        old_lock_hash,
        new_lock_hash,
        old_signature_hash,
        new_signature_hash,
        recovery_status,
        recovered_by,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        recovery_id,
        report_id,
        "RE_LOCK_AND_RE_REGISTER",
        old_lock_hash,
        new_lock_hash,
        old_signature_hash,
        new_signature_hash,
        "RECOVERED",
        recovered_by,
        datetime.utcnow().isoformat() + "Z"
    ))

    previous_hash = get_latest_block_hash()

    block_payload = {
        "report_id": report_id,
        "lock_hash": new_lock_hash,
        "signature_hash": new_signature_hash,
        "signed_by": recovered_by,
        "previous_hash": previous_hash,
        "recovery_id": recovery_id,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    block_hash = sha(block_payload)
    block_id = "BLOCK-RECOVERY-" + block_hash[:24]

    cur.execute("""
    INSERT INTO rsna_report_blockchain (
        block_id,
        report_id,
        previous_hash,
        block_hash,
        lock_hash,
        signature_hash,
        signed_by,
        verification_status,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        block_id,
        report_id,
        previous_hash,
        block_hash,
        new_lock_hash,
        new_signature_hash,
        recovered_by,
        "RECOVERED_VERIFIABLE",
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "recovered",
        "phase": "AHOS 41.2.9",
        "report_id": report_id,
        "recovery_id": recovery_id,
        "new_lock_id": new_lock_id,
        "new_block_id": block_id,
        "previous_hash": previous_hash,
        "new_lock_hash": new_lock_hash,
        "new_signature_hash": new_signature_hash,
        "verification_status": "RECOVERED_VERIFIABLE"
    }

def list_recoveries(limit: int = 20):
    init_recovery_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        recovery_id,
        report_id,
        action,
        recovery_status,
        recovered_by,
        created_at
    FROM rsna_integrity_recovery_log
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows
