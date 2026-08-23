from fastapi import APIRouter
from datetime import datetime
import json

from backend.app.database.ahos_db import init_ahos_database, get_connection

router = APIRouter(tags=["Global Digital Twin Network"])


def rows(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    data = [dict(r) for r in cur.fetchall()]
    conn.close()
    return data


def one(query, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    r = cur.fetchone()
    conn.close()
    return dict(r) if r else {}


@router.get("/gmin/digital-twin/health")
async def digital_twin_health():
    init_ahos_database()
    return {
        "status": "online",
        "engine": "Global Digital Twin Network",
        "version": "10.0.6",
        "storage": "aiha_ahos.db",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/gmin/digital-twin/overview")
async def digital_twin_overview():
    init_ahos_database()

    patients = one("SELECT COUNT(*) as c FROM patient_states").get("c", 0)
    critical = one("SELECT COUNT(*) as c FROM patient_states WHERE LOWER(risk_level)='critical'").get("c", 0)
    high = one("SELECT COUNT(*) as c FROM patient_states WHERE LOWER(risk_level)='high'").get("c", 0)
    hospitals = one("SELECT COUNT(*) as c FROM hospital_nodes").get("c", 0)
    decisions = one("SELECT COUNT(*) as c FROM decision_logs").get("c", 0)
    events = one("SELECT COUNT(*) as c FROM bus_events").get("c", 0)
    memories = one("SELECT COUNT(*) as c FROM medical_memory_records").get("c", 0)

    return {
        "status": "success",
        "digital_twin": "active",
        "hospitals": hospitals,
        "patients": patients,
        "critical_patients": critical,
        "high_risk_patients": high,
        "decision_logs": decisions,
        "bus_events": events,
        "medical_memories": memories,
        "global_twin_sync": "active",
        "network_mode": "federated"
    }


@router.get("/gmin/digital-twin/hospitals")
async def digital_twin_hospitals():
    init_ahos_database()

    hospitals = rows("SELECT * FROM hospital_nodes ORDER BY created_at DESC")

    return {
        "status": "success",
        "total": len(hospitals),
        "hospitals": hospitals
    }


@router.get("/gmin/digital-twin/patients")
async def digital_twin_patients():
    init_ahos_database()

    patients = rows("SELECT * FROM patient_states ORDER BY updated_at DESC")

    return {
        "status": "success",
        "total": len(patients),
        "patients": patients
    }


@router.get("/gmin/digital-twin/events")
async def digital_twin_events():
    init_ahos_database()

    events = rows("SELECT * FROM bus_events ORDER BY created_at DESC LIMIT 20")

    for e in events:
        try:
            e["payload"] = json.loads(e.get("payload") or "{}")
        except Exception:
            e["payload"] = {}

    return {
        "status": "success",
        "total": len(events),
        "events": events
    }


@router.get("/gmin/digital-twin/decisions")
async def digital_twin_decisions():
    init_ahos_database()

    decisions = rows("SELECT * FROM decision_logs ORDER BY created_at DESC LIMIT 20")

    for d in decisions:
        try:
            d["recommended_actions"] = json.loads(d.get("recommended_actions") or "[]")
        except Exception:
            d["recommended_actions"] = []

    return {
        "status": "success",
        "total": len(decisions),
        "decisions": decisions
    }


@router.get("/gmin/digital-twin/risk-map")
async def digital_twin_risk_map():
    init_ahos_database()

    risk_levels = rows("""
        SELECT risk_level, COUNT(*) as count
        FROM patient_states
        GROUP BY risk_level
        ORDER BY count DESC
    """)

    decision_levels = rows("""
        SELECT decision_level, COUNT(*) as count
        FROM decision_logs
        GROUP BY decision_level
        ORDER BY count DESC
    """)

    event_priority = rows("""
        SELECT priority, COUNT(*) as count
        FROM bus_events
        GROUP BY priority
        ORDER BY count DESC
    """)

    return {
        "status": "success",
        "patient_risk_levels": risk_levels,
        "decision_levels": decision_levels,
        "event_priority": event_priority,
        "twin_risk_engine": "active"
    }
