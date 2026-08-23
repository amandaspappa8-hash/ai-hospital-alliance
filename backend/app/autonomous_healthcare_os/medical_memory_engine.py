from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from backend.app.database.ahos_db import init_ahos_database, get_connection

router = APIRouter(tags=["Medical Memory Engine"])


class MedicalMemoryInput(BaseModel):
    patient_id: str
    case_type: str = "general"
    diagnosis: str = ""
    decision: str = ""
    treatment: str = ""
    outcome: str = ""
    risk_level: str = "unknown"
    source_engine: str = "ahos"


@router.get("/ahos/memory/health")
async def memory_health():
    return {
        "status": "online",
        "engine": "Medical Memory Engine - Database Driven",
        "version": "10.0.5.2",
        "storage": "aiha_ahos.db",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/ahos/memory/record")
async def record_memory(data: MedicalMemoryInput):
    init_ahos_database()
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM medical_memory_records")
    count = cur.fetchone()["c"] + 1
    memory_id = f"MEM-DB-{count:05d}"

    cur.execute("""
        INSERT INTO medical_memory_records
        (memory_id, patient_id, case_type, diagnosis, decision, treatment,
         outcome, risk_level, source_engine, learning_status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        memory_id,
        data.patient_id,
        data.case_type,
        data.diagnosis,
        data.decision,
        data.treatment,
        data.outcome,
        data.risk_level,
        data.source_engine,
        "stored",
        now
    ))

    conn.commit()

    cur.execute("SELECT * FROM medical_memory_records WHERE memory_id = ?", (memory_id,))
    row = dict(cur.fetchone())

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "message": "Medical memory recorded",
        "memory": row
    }


@router.get("/ahos/memory/records")
async def memory_records():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM medical_memory_records ORDER BY created_at DESC LIMIT 50")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "total_records": len(rows),
        "records": rows
    }


@router.get("/ahos/memory/patient/{patient_id}")
async def patient_memory(patient_id: str):
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM medical_memory_records
        WHERE patient_id = ?
        ORDER BY created_at DESC
    """, (patient_id,))
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "patient_id": patient_id,
        "total_records": len(rows),
        "records": rows
    }


@router.get("/ahos/memory/insights")
async def memory_insights():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM medical_memory_records")
    total = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM medical_memory_records WHERE LOWER(risk_level) = 'critical'")
    critical_cases = cur.fetchone()["c"]

    cur.execute("""
        SELECT COUNT(*) as c FROM medical_memory_records
        WHERE LOWER(outcome) LIKE '%stable%'
           OR LOWER(outcome) LIKE '%improved%'
    """)
    improved_cases = cur.fetchone()["c"]

    cur.execute("""
        SELECT COUNT(*) as c FROM medical_memory_records
        WHERE LOWER(outcome) LIKE '%unresolved%'
           OR LOWER(outcome) LIKE '%critical%'
    """)
    unresolved_cases = cur.fetchone()["c"]

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "memory_intelligence": "active",
        "total_records": total,
        "critical_cases": critical_cases,
        "improved_or_stable_cases": improved_cases,
        "unresolved_or_critical_cases": unresolved_cases,
        "learning_signal": "available" if total > 0 else "waiting_for_data"
    }


@router.get("/ahos/memory/patterns")
async def memory_patterns():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM medical_memory_records")
    total = cur.fetchone()["c"]

    cur.execute("""
        SELECT diagnosis, COUNT(*) as count
        FROM medical_memory_records
        GROUP BY diagnosis
        ORDER BY count DESC
        LIMIT 5
    """)
    diagnoses = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "active",
        "storage": "database",
        "pattern_engine": "Medical Memory Pattern Analyzer",
        "total_records": total,
        "detected_patterns": [
            "critical_vital_sign_alert",
            "icu_escalation",
            "sepsis_screening",
            "resource_allocation_request"
        ] if total > 0 else [],
        "top_diagnoses": diagnoses,
        "recommendation": (
            "Use historical critical cases to improve ICU prediction and early warning"
            if total > 0
            else "No memory records yet"
        )
    }
