import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_clinical_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_id TEXT UNIQUE,
        generated_at TEXT,
        image_path TEXT,
        ai_model TEXT,
        threshold REAL,
        pneumonia_probability REAL,
        prediction TEXT,
        risk_level TEXT,
        exam TEXT,
        impression TEXT,
        recommendation TEXT,
        disclaimer TEXT,
        report_json TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_report(report: dict):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    ai = report.get("ai_result", {})
    clinical = report.get("clinical_report", {})

    cur.execute("""
    INSERT OR REPLACE INTO rsna_clinical_reports (
        report_id,
        generated_at,
        image_path,
        ai_model,
        threshold,
        pneumonia_probability,
        prediction,
        risk_level,
        exam,
        impression,
        recommendation,
        disclaimer,
        report_json,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report.get("report_id"),
        report.get("generated_at"),
        report.get("image_path"),
        report.get("ai_model"),
        report.get("threshold"),
        ai.get("pneumonia_probability"),
        ai.get("prediction"),
        ai.get("risk_level"),
        clinical.get("exam"),
        clinical.get("impression"),
        clinical.get("recommendation"),
        clinical.get("disclaimer"),
        json.dumps(report, ensure_ascii=False),
        datetime.utcnow().isoformat() + "Z",
    ))

    conn.commit()
    conn.close()

    return {
        "status": "saved",
        "database": DB_PATH,
        "report_id": report.get("report_id")
    }

def list_reports(limit: int = 20):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        report_id,
        generated_at,
        image_path,
        pneumonia_probability,
        prediction,
        risk_level,
        impression,
        recommendation
    FROM rsna_clinical_reports
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    return rows

def get_report(report_id: str):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT report_json
    FROM rsna_clinical_reports
    WHERE report_id = ?
    """, (report_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return json.loads(row["report_json"])
