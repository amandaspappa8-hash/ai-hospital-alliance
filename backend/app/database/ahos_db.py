import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("aiha_ahos.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_ahos_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medical_memory_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        memory_id TEXT UNIQUE,
        patient_id TEXT,
        case_type TEXT,
        diagnosis TEXT,
        decision TEXT,
        treatment TEXT,
        outcome TEXT,
        risk_level TEXT,
        source_engine TEXT,
        learning_status TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT UNIQUE,
        heart_rate INTEGER,
        spo2 INTEGER,
        systolic_bp INTEGER,
        temperature REAL,
        risk_level TEXT,
        diagnosis TEXT,
        treatment_plan TEXT,
        workflow_status TEXT,
        digital_twin_status TEXT,
        updated_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS decision_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        decision_id TEXT UNIQUE,
        patient_id TEXT,
        source_engine TEXT,
        event_type TEXT,
        priority TEXT,
        severity_score INTEGER,
        decision_level TEXT,
        recommended_actions TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bus_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT UNIQUE,
        source_engine TEXT,
        target_engine TEXT,
        event_type TEXT,
        priority TEXT,
        payload TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hospital_nodes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        node_id TEXT UNIQUE,
        name TEXT,
        city TEXT,
        country TEXT,
        status TEXT,
        node_type TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS global_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT UNIQUE,
        patient_id TEXT,
        alert_type TEXT,
        severity TEXT,
        message TEXT,
        source_engine TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "database": str(DB_PATH),
        "initialized_at": datetime.utcnow().isoformat()
    }
