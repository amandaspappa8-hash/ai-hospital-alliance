from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, List
import json

from backend.app.database.ahos_db import init_ahos_database, get_connection

router = APIRouter(tags=["AHOS Persistent Events"])


class PersistentDecisionInput(BaseModel):
    decision_id: str | None = None
    patient_id: str
    source_engine: str = "autonomous_decision_supervisor"
    event_type: str = "clinical_event"
    priority: str = "normal"
    severity_score: int = 0
    decision_level: str = "stable"
    recommended_actions: List[str] = []
    status: str = "decision_generated"


class PersistentBusEventInput(BaseModel):
    event_id: str | None = None
    source_engine: str
    target_engine: str
    event_type: str
    priority: str = "normal"
    payload: Dict[str, Any] = {}
    status: str = "delivered"


@router.get("/ahos/db/events/health")
async def events_db_health():
    init_ahos_database()
    return {
        "status": "online",
        "engine": "Persistent Decision Logs + Bus Events API",
        "version": "10.0.2",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/ahos/db/decision-log")
async def save_decision_log(data: PersistentDecisionInput):
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    decision_id = data.decision_id or f"DB-ADS-{int(datetime.utcnow().timestamp())}"

    cur.execute("""
    INSERT OR REPLACE INTO decision_logs
    (decision_id, patient_id, source_engine, event_type, priority,
     severity_score, decision_level, recommended_actions, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        decision_id,
        data.patient_id,
        data.source_engine,
        data.event_type,
        data.priority,
        data.severity_score,
        data.decision_level,
        json.dumps(data.recommended_actions),
        data.status,
        now
    ))

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": "Decision log persisted",
        "decision_id": decision_id
    }


@router.get("/ahos/db/decision-logs")
async def get_decision_logs():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM decision_logs ORDER BY created_at DESC")
    rows = []

    for row in cur.fetchall():
        item = dict(row)
        try:
            item["recommended_actions"] = json.loads(item.get("recommended_actions") or "[]")
        except Exception:
            item["recommended_actions"] = []
        rows.append(item)

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "decision_logs": rows
    }


@router.post("/ahos/db/bus-event")
async def save_bus_event(data: PersistentBusEventInput):
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()
    now = datetime.utcnow().isoformat()

    event_id = data.event_id or f"DB-BUS-{int(datetime.utcnow().timestamp())}"

    cur.execute("""
    INSERT OR REPLACE INTO bus_events
    (event_id, source_engine, target_engine, event_type, priority,
     payload, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event_id,
        data.source_engine,
        data.target_engine,
        data.event_type,
        data.priority,
        json.dumps(data.payload),
        data.status,
        now
    ))

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "message": "Bus event persisted",
        "event_id": event_id
    }


@router.get("/ahos/db/bus-events")
async def get_bus_events():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM bus_events ORDER BY created_at DESC")
    rows = []

    for row in cur.fetchall():
        item = dict(row)
        try:
            item["payload"] = json.loads(item.get("payload") or "{}")
        except Exception:
            item["payload"] = {}
        rows.append(item)

    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "bus_events": rows
    }


@router.get("/ahos/db/events/summary")
async def events_summary():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as count FROM decision_logs")
    decision_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM bus_events")
    bus_count = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM decision_logs WHERE decision_level='critical'")
    critical_decisions = cur.fetchone()["count"]

    cur.execute("SELECT COUNT(*) as count FROM bus_events WHERE priority='high' OR priority='critical'")
    high_priority_events = cur.fetchone()["count"]

    conn.close()

    return {
        "status": "success",
        "decision_logs": decision_count,
        "bus_events": bus_count,
        "critical_decisions": critical_decisions,
        "high_priority_events": high_priority_events,
        "persistent_event_storage": "active"
    }
