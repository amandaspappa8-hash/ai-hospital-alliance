import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

VALID_DECISIONS = {
    "APPROVED",
    "REJECTED",
    "REVIEW_REQUIRED",
    "ESCALATED"
}

def init_decision_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_review_decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision_id TEXT UNIQUE,
        report_id TEXT,
        reviewer_name TEXT,
        decision TEXT,
        clinical_status TEXT,
        comments TEXT,
        approved_for_use INTEGER,
        requires_second_review INTEGER,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_decision(report_id: str, reviewer_name: str, decision: str, comments: str):
    init_decision_db()

    decision = decision.upper().strip()

    if decision not in VALID_DECISIONS:
        return {
            "status": "invalid_decision",
            "allowed": sorted(list(VALID_DECISIONS))
        }

    approved_for_use = 1 if decision == "APPROVED" else 0
    requires_second_review = 1 if decision in ["REVIEW_REQUIRED", "ESCALATED"] else 0

    if decision == "APPROVED":
        clinical_status = "AI_REPORT_APPROVED_BY_RADIOLOGIST"
    elif decision == "REJECTED":
        clinical_status = "AI_REPORT_REJECTED_BY_RADIOLOGIST"
    elif decision == "ESCALATED":
        clinical_status = "ESCALATED_TO_SENIOR_RADIOLOGIST"
    else:
        clinical_status = "SECOND_REVIEW_REQUIRED"

    decision_id = "DECISION-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO rsna_review_decisions (
        decision_id,
        report_id,
        reviewer_name,
        decision,
        clinical_status,
        comments,
        approved_for_use,
        requires_second_review,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        decision_id,
        report_id,
        reviewer_name,
        decision,
        clinical_status,
        comments,
        approved_for_use,
        requires_second_review,
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "saved",
        "decision_id": decision_id,
        "report_id": report_id,
        "decision": decision,
        "clinical_status": clinical_status,
        "approved_for_use": bool(approved_for_use),
        "requires_second_review": bool(requires_second_review)
    }

def list_decisions(limit: int = 20):
    init_decision_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        decision_id,
        report_id,
        reviewer_name,
        decision,
        clinical_status,
        comments,
        approved_for_use,
        requires_second_review,
        created_at
    FROM rsna_review_decisions
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows

def get_decision_status(report_id: str):
    init_decision_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        decision_id,
        report_id,
        reviewer_name,
        decision,
        clinical_status,
        approved_for_use,
        requires_second_review,
        created_at
    FROM rsna_review_decisions
    WHERE report_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return {
            "status": "no_decision",
            "report_id": report_id,
            "clinical_status": "PENDING_REVIEW"
        }

    return dict(row)
