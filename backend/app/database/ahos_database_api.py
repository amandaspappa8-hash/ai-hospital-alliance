from fastapi import APIRouter
from datetime import datetime
from backend.app.database.ahos_db import get_connection

router = APIRouter(tags=["AHOS Persistent Database"])


@router.get("/ahos/db/health")
async def ahos_db_health():
    return {
        "status": "online",
        "engine": "AHOS Persistent Medical Intelligence Database",
        "version": "10.0.1",
        "timestamp": datetime.utcnow().isoformat()
    }




@router.get("/ahos/db/tables")
async def ahos_db_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row["name"] for row in cur.fetchall()]

    result = {}

    for table in tables:
        cur.execute(f"SELECT COUNT(*) as count FROM {table}")
        result[table] = cur.fetchone()["count"]

    conn.close()

    return {
        "status": "success",
        "tables": result
    }


@router.post("/ahos/db/seed-demo")
async def seed_demo_data():
    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    cur.execute("""
    INSERT OR IGNORE INTO hospital_nodes
    (node_id, name, city, country, status, node_type, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "NODE-TRIPOLI-001",
        "Tripoli Central AI Hospital",
        "Tripoli",
        "Libya",
        "online",
        "primary_hospital_node",
        now
    ))

    cur.execute("""
    INSERT OR IGNORE INTO hospital_nodes
    (node_id, name, city, country, status, node_type, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        "NODE-STOCKHOLM-001",
        "Stockholm Medical Intelligence Node",
        "Stockholm",
        "Sweden",
        "online",
        "federated_hospital_node",
        now
    ))

    cur.execute("""
    INSERT OR REPLACE INTO patient_states
    (patient_id, heart_rate, spo2, systolic_bp, temperature, risk_level,
     diagnosis, treatment_plan, workflow_status, digital_twin_status, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "P-1001",
        132,
        89,
        85,
        39.2,
        "critical",
        "Sepsis Suspected",
        "ICU Observation",
        "Critical Care",
        "active",
        now
    ))

    cur.execute("""
    INSERT OR IGNORE INTO medical_memory_records
    (memory_id, patient_id, case_type, diagnosis, decision, treatment, outcome,
     risk_level, source_engine, learning_status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        "MEM-00001",
        "P-1001",
        "critical_care",
        "Sepsis Suspected",
        "ICU escalation and sepsis screening",
        "ICU Observation",
        "stable under monitoring",
        "critical",
        "autonomous_decision_supervisor",
        "stored",
        now
    ))

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": "Demo medical intelligence data seeded"
    }


@router.get("/ahos/db/patient-states")
async def db_patient_states():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patient_states ORDER BY updated_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "patient_states": rows
    }


@router.get("/ahos/db/memory")
async def db_memory():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medical_memory_records ORDER BY created_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "memory_records": rows
    }


@router.get("/ahos/db/hospital-nodes")
async def db_hospital_nodes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM hospital_nodes ORDER BY created_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "hospital_nodes": rows
    }
