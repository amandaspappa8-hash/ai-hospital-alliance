import sqlite3
import hashlib
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_blockchain_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_report_blockchain (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        block_id TEXT UNIQUE,
        report_id TEXT,
        previous_hash TEXT,
        block_hash TEXT,
        lock_hash TEXT,
        signature_hash TEXT,
        signed_by TEXT,
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
    SELECT
        report_id,
        lock_id,
        final_status,
        signed_by,
        signature_hash,
        lock_hash,
        locked_at
    FROM rsna_locked_reports
    WHERE report_id = ?
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    return dict(row) if row else None

def get_latest_block_hash():
    init_blockchain_db()

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

    if not row:
        return "GENESIS"

    return row[0]

def calculate_block_hash(payload: dict):
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()

def register_locked_report_on_chain(report_id: str):
    init_blockchain_db()

    locked = get_locked_report(report_id)

    if not locked:
        return {
            "status": "blocked",
            "reason": "REPORT_NOT_LOCKED",
            "report_id": report_id
        }

    previous_hash = get_latest_block_hash()

    payload = {
        "report_id": report_id,
        "lock_hash": locked["lock_hash"],
        "signature_hash": locked["signature_hash"],
        "signed_by": locked["signed_by"],
        "previous_hash": previous_hash,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    block_hash = calculate_block_hash(payload)
    block_id = "BLOCK-" + block_hash[:24]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO rsna_report_blockchain (
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
        locked["lock_hash"],
        locked["signature_hash"],
        locked["signed_by"],
        "REGISTERED_VERIFIABLE",
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "registered",
        "phase": "AHOS 41.2.7",
        "block_id": block_id,
        "report_id": report_id,
        "previous_hash": previous_hash,
        "block_hash": block_hash,
        "verification_status": "REGISTERED_VERIFIABLE"
    }

def verify_locked_report_chain(report_id: str):
    init_blockchain_db()

    locked = get_locked_report(report_id)

    if not locked:
        return {
            "status": "failed",
            "reason": "REPORT_NOT_LOCKED",
            "report_id": report_id
        }

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        block_id,
        report_id,
        previous_hash,
        block_hash,
        lock_hash,
        signature_hash,
        signed_by,
        verification_status,
        created_at
    FROM rsna_report_blockchain
    WHERE report_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {
            "status": "failed",
            "reason": "NO_BLOCKCHAIN_RECORD",
            "report_id": report_id
        }

    block = dict(row)

    lock_match = block["lock_hash"] == locked["lock_hash"]
    signature_match = block["signature_hash"] == locked["signature_hash"]

    verified = lock_match and signature_match

    return {
        "status": "verified" if verified else "tampered",
        "phase": "AHOS 41.2.7",
        "report_id": report_id,
        "block_id": block["block_id"],
        "lock_match": lock_match,
        "signature_match": signature_match,
        "block_hash": block["block_hash"],
        "verification_status": block["verification_status"],
        "verified": verified
    }

def list_chain_blocks(limit: int = 20):
    init_blockchain_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        block_id,
        report_id,
        previous_hash,
        block_hash,
        verification_status,
        created_at
    FROM rsna_report_blockchain
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows
