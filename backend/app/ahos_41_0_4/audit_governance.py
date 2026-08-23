import sqlite3
import json
import hashlib
from datetime import datetime
from pathlib import Path

DB_PATH = "data/processed/rsna/rsna_reports.db"

def init_audit_db():
    Path("data/processed/rsna").mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_ai_audit_trail (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE,
        event_type TEXT,
        report_id TEXT,
        model_name TEXT,
        model_version TEXT,
        dataset_name TEXT,
        threshold REAL,
        input_image TEXT,
        prediction TEXT,
        probability REAL,
        risk_level TEXT,
        governance_status TEXT,
        safety_status TEXT,
        event_json TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS rsna_model_registry (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT UNIQUE,
        model_version TEXT,
        dataset_name TEXT,
        training_samples INTEGER,
        validation_samples INTEGER,
        threshold REAL,
        accuracy REAL,
        precision_score REAL,
        recall_score REAL,
        f1_score REAL,
        governance_status TEXT,
        registered_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def create_event_id(payload: dict):
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]

def log_ai_event(report: dict):
    init_audit_db()

    ai = report.get("ai_result", {})
    payload = {
        "report_id": report.get("report_id"),
        "image_path": report.get("image_path"),
        "model": report.get("ai_model"),
        "threshold": report.get("threshold"),
        "prediction": ai.get("prediction"),
        "probability": ai.get("pneumonia_probability"),
        "risk": ai.get("risk_level"),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    event_id = "AUDIT-" + create_event_id(payload)

    governance_status = "RESEARCH_ONLY"
    safety_status = "RADIOLOGIST_REVIEW_REQUIRED"

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO rsna_ai_audit_trail (
        event_id,
        event_type,
        report_id,
        model_name,
        model_version,
        dataset_name,
        threshold,
        input_image,
        prediction,
        probability,
        risk_level,
        governance_status,
        safety_status,
        event_json,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id,
        "RSNA_RADIOLOGY_AI_INFERENCE",
        report.get("report_id"),
        report.get("ai_model"),
        "AHOS-41.1-RSNA-2000",
        "RSNA Pneumonia Detection Challenge",
        report.get("threshold"),
        report.get("image_path"),
        ai.get("prediction"),
        ai.get("pneumonia_probability"),
        ai.get("risk_level"),
        governance_status,
        safety_status,
        json.dumps(payload, ensure_ascii=False),
        payload["created_at"]
    ))

    conn.commit()
    conn.close()

    return {
        "event_id": event_id,
        "governance_status": governance_status,
        "safety_status": safety_status
    }

def register_model():
    init_audit_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO rsna_model_registry (
        model_name,
        model_version,
        dataset_name,
        training_samples,
        validation_samples,
        threshold,
        accuracy,
        precision_score,
        recall_score,
        f1_score,
        governance_status,
        registered_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "rsna_resnet18_2000.pt",
        "AHOS-41.1-RSNA-2000",
        "RSNA Pneumonia Detection Challenge",
        1600,
        400,
        0.30,
        0.857,
        0.6564,
        0.7589,
        0.7039,
        "RESEARCH_ONLY_NOT_DIAGNOSTIC",
        datetime.utcnow().isoformat() + "Z"
    ))

    conn.commit()
    conn.close()

    return {
        "status": "registered",
        "model": "rsna_resnet18_2000.pt",
        "version": "AHOS-41.1-RSNA-2000"
    }

def list_audit_events(limit: int = 20):
    init_audit_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        event_id,
        event_type,
        report_id,
        model_name,
        threshold,
        prediction,
        probability,
        risk_level,
        governance_status,
        safety_status,
        created_at
    FROM rsna_ai_audit_trail
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def list_models():
    init_audit_db()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
    SELECT
        model_name,
        model_version,
        dataset_name,
        training_samples,
        validation_samples,
        threshold,
        accuracy,
        precision_score,
        recall_score,
        f1_score,
        governance_status,
        registered_at
    FROM rsna_model_registry
    ORDER BY id DESC
    """)

    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
