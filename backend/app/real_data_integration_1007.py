from fastapi import APIRouter
from datetime import datetime
import sqlite3, json
from pathlib import Path

router = APIRouter(prefix="/aiha/10.0.7", tags=["AIHA 10.0.7 Real Database Integration"])

DB_PATH = Path("aiha_1007_live.db")

def now():
    return datetime.utcnow().isoformat() + "Z"

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_states (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        data TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS medical_memory_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        memory_type TEXT,
        data TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS decision_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        decision_type TEXT,
        risk_level TEXT,
        data TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS bus_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_type TEXT,
        source TEXT,
        data TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS global_alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        level TEXT,
        message TEXT,
        data TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS hospital_nodes (
        id TEXT PRIMARY KEY,
        name TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO hospital_nodes VALUES
    ('HN-TRIPOLI-001','Tripoli Central AI Hospital','online'),
    ('HN-STOCKHOLM-001','Stockholm Quantum Care','online')
    """)

    conn.commit()
    conn.close()

def insert_event(event_type, source, payload):
    conn = db()
    conn.execute(
        "INSERT INTO bus_events (event_type, source, data, created_at) VALUES (?, ?, ?, ?)",
        (event_type, source, json.dumps(payload), now())
    )
    conn.commit()
    conn.close()

init_db()

@router.get("/health")
def health():
    return {
        "status": "online",
        "stage": "AI Hospital Alliance 10.0.7",
        "engine": "SQLite Real Data Integration",
        "database": str(DB_PATH),
        "timestamp": now()
    }

@router.post("/gmin/patient-state")
def add_patient_state(data: dict):
    conn = db()
    patient_id = data.get("patient_id", "UNKNOWN")
    created_at = now()

    cur = conn.execute(
        "INSERT INTO patient_states (patient_id, data, created_at) VALUES (?, ?, ?)",
        (patient_id, json.dumps(data), created_at)
    )
    conn.commit()
    record = {"id": f"PS-{cur.lastrowid:04d}", "timestamp": created_at, **data}
    conn.close()

    insert_event("patient_state_updated", "GMIN", record)
    return {"status": "success", "patient_state": record}

@router.post("/radiology/to-memory")
def radiology_to_memory(data: dict):
    conn = db()
    patient_id = data.get("patient_id", "UNKNOWN")
    created_at = now()

    cur = conn.execute(
        "INSERT INTO medical_memory_records (patient_id, memory_type, data, created_at) VALUES (?, ?, ?, ?)",
        (patient_id, "radiology", json.dumps(data), created_at)
    )
    conn.commit()
    record = {"id": f"MEM-RAD-{cur.lastrowid:04d}", "memory_type": "radiology", "timestamp": created_at, **data}
    conn.close()

    insert_event("radiology_memory_created", "Radiology", record)
    return {"status": "success", "medical_memory": record}

@router.post("/laboratory/to-memory")
def laboratory_to_memory(data: dict):
    conn = db()
    patient_id = data.get("patient_id", "UNKNOWN")
    created_at = now()

    cur = conn.execute(
        "INSERT INTO medical_memory_records (patient_id, memory_type, data, created_at) VALUES (?, ?, ?, ?)",
        (patient_id, "laboratory", json.dumps(data), created_at)
    )
    conn.commit()
    record = {"id": f"MEM-LAB-{cur.lastrowid:04d}", "memory_type": "laboratory", "timestamp": created_at, **data}
    conn.close()

    insert_event("laboratory_memory_created", "Laboratory", record)
    return {"status": "success", "medical_memory": record}

@router.post("/pharmacy/to-decision")
def pharmacy_to_decision(data: dict):
    alerts = []
    medicine = str(data.get("medicine", "")).lower()

    if "aspirin" in medicine or "warfarin" in medicine:
        alerts.append("Bleeding risk medication detected")

    risk_level = "HIGH" if alerts else "LOW"
    recommendation = "Review by doctor/pharmacist" if alerts else "Medication appears acceptable"

    decision = {
        "decision_type": "pharmacy_supervision",
        "risk_level": risk_level,
        "alerts": alerts,
        "recommendation": recommendation,
        **data
    }

    conn = db()
    created_at = now()
    cur = conn.execute(
        "INSERT INTO decision_logs (patient_id, decision_type, risk_level, data, created_at) VALUES (?, ?, ?, ?, ?)",
        (data.get("patient_id", "UNKNOWN"), "pharmacy_supervision", risk_level, json.dumps(decision), created_at)
    )
    conn.commit()
    decision_record = {"id": f"DEC-PHARM-{cur.lastrowid:04d}", "timestamp": created_at, **decision}

    if alerts:
        conn.execute(
            "INSERT INTO global_alerts (level, message, data, created_at) VALUES (?, ?, ?, ?)",
            ("HIGH", "Pharmacy Decision Supervisor alert", json.dumps(decision_record), now())
        )
        conn.commit()

    conn.close()

    insert_event("pharmacy_decision_created", "Pharmacy", decision_record)
    return {"status": "success", "decision": decision_record}

@router.get("/dashboard/live")
def live_dashboard():
    conn = db()

    hospital_nodes = [dict(x) for x in conn.execute("SELECT * FROM hospital_nodes").fetchall()]
    patient_states = [dict(x) for x in conn.execute("SELECT * FROM patient_states ORDER BY id DESC LIMIT 20").fetchall()]
    memory = [dict(x) for x in conn.execute("SELECT * FROM medical_memory_records ORDER BY id DESC LIMIT 20").fetchall()]
    decisions = [dict(x) for x in conn.execute("SELECT * FROM decision_logs ORDER BY id DESC LIMIT 20").fetchall()]
    alerts = [dict(x) for x in conn.execute("SELECT * FROM global_alerts ORDER BY id DESC LIMIT 20").fetchall()]
    events = [dict(x) for x in conn.execute("SELECT * FROM bus_events ORDER BY id DESC LIMIT 30").fetchall()]

    metrics = {
        "hospital_nodes": conn.execute("SELECT COUNT(*) FROM hospital_nodes").fetchone()[0],
        "patient_states": conn.execute("SELECT COUNT(*) FROM patient_states").fetchone()[0],
        "medical_memory_records": conn.execute("SELECT COUNT(*) FROM medical_memory_records").fetchone()[0],
        "decision_logs": conn.execute("SELECT COUNT(*) FROM decision_logs").fetchone()[0],
        "global_alerts": conn.execute("SELECT COUNT(*) FROM global_alerts").fetchone()[0],
        "bus_events": conn.execute("SELECT COUNT(*) FROM bus_events").fetchone()[0],
    }

    conn.close()

    return {
        "status": "success",
        "database_mode": "sqlite_persistent",
        "gmin": {
            "hospital_nodes": hospital_nodes,
            "global_alerts": alerts,
            "patient_states": patient_states
        },
        "medical_memory": memory,
        "decision_logs": decisions,
        "bus_events": events,
        "metrics": metrics,
        "timestamp": now()
    }
