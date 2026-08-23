import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_review_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_clinical_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_id TEXT UNIQUE,
        report_id TEXT,
        reviewer_name TEXT,
        decision TEXT,
        comments TEXT,
        reviewed_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_review(report_id: str, reviewer_name: str, decision: str, comments: str):
    init_review_db()

    review_id = "REVIEW-" + report_id + "-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO rsna_clinical_reviews (
        review_id,
        report_id,
        reviewer_name,
        decision,
        comments,
        reviewed_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        review_id,
        report_id,
        reviewer_name,
        decision,
        comments,
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "saved",
        "review_id": review_id,
        "report_id": report_id,
        "decision": decision
    }

def list_reviews(limit: int = 20):
    init_review_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        review_id,
        report_id,
        reviewer_name,
        decision,
        comments,
        reviewed_at
    FROM rsna_clinical_reviews
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows
