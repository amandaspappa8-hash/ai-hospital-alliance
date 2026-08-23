from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from backend.app.database.ahos_db import init_ahos_database, get_connection

router = APIRouter(tags=["Global Patient State Engine"])


class PatientStateInput(BaseModel):
    patient_id: str
    heart_rate: int = 0
    spo2: int = 0
    systolic_bp: int = 0
    temperature: float = 0
    risk_level: str = "unknown"
    diagnosis: str = ""
    treatment_plan: str = ""
    workflow_status: str = ""
    digital_twin_status: str = "active"


@router.get("/ahos/patient-state/health")
async def patient_state_health():
    return {
        "status": "online",
        "engine": "Global Patient State Engine - Database Driven",
        "version": "10.0.5.1",
        "storage": "aiha_ahos.db",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/ahos/patient-state/update")
async def update_patient_state(data: PatientStateInput):
    init_ahos_database()
    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO patient_states
        (patient_id, heart_rate, spo2, systolic_bp, temperature, risk_level,
         diagnosis, treatment_plan, workflow_status, digital_twin_status, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.patient_id,
        data.heart_rate,
        data.spo2,
        data.systolic_bp,
        data.temperature,
        data.risk_level,
        data.diagnosis,
        data.treatment_plan,
        data.workflow_status,
        data.digital_twin_status,
        now
    ))

    conn.commit()

    cur.execute("SELECT * FROM patient_states WHERE patient_id = ?", (data.patient_id,))
    row = dict(cur.fetchone())

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "patient_state": row
    }


@router.get("/ahos/patient-state/summary")
async def patient_summary():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM patient_states")
    total = cur.fetchone()["c"]

    def count_risk(risk):
        cur.execute("SELECT COUNT(*) as c FROM patient_states WHERE LOWER(risk_level)=?", (risk,))
        return cur.fetchone()["c"]

    result = {
        "status": "success",
        "storage": "database",
        "total_patients": total,
        "critical": count_risk("critical"),
        "high": count_risk("high"),
        "moderate": count_risk("moderate"),
        "stable": count_risk("stable")
    }

    conn.close()
    return result


@router.get("/ahos/patient-state")
async def all_patient_states():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patient_states ORDER BY updated_at DESC")
    rows = [dict(row) for row in cur.fetchall()]

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "total_patients": len(rows),
        "patients": rows
    }


@router.get("/ahos/patient-state/{patient_id}")
async def get_patient_state(patient_id: str):
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patient_states WHERE patient_id = ?", (patient_id,))
    row = cur.fetchone()

    conn.close()

    if not row:
        return {
            "status": "not_found",
            "storage": "database",
            "patient_id": patient_id
        }

    return {
        "status": "success",
        "storage": "database",
        "patient_state": dict(row)
    }
