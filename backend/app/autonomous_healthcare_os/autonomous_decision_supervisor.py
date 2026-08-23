from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
import json

from backend.app.database.ahos_db import init_ahos_database, get_connection

router = APIRouter(tags=["Autonomous Decision Supervisor"])


class SupervisorInput(BaseModel):
    patient_id: str = "P-1001"
    source_engine: str = "patient_monitoring"
    event_type: str = "clinical_event"
    priority: str = "normal"
    heart_rate: int | None = None
    spo2: int | None = None
    systolic_bp: int | None = None
    temperature: float | None = None
    risk: str = "unknown"


def calculate_decision(data: SupervisorInput):
    actions = []
    severity_score = 0

    if data.priority.lower() in ["critical", "high"]:
        severity_score += 30

    if data.risk.lower() in ["critical", "high"]:
        severity_score += 30

    if data.heart_rate is not None and data.heart_rate >= 130:
        severity_score += 20
        actions.append("doctor_alert")

    if data.spo2 is not None and data.spo2 < 90:
        severity_score += 25
        actions.append("icu_escalation")

    if data.systolic_bp is not None and data.systolic_bp < 90:
        severity_score += 20
        actions.append("shock_protocol_review")

    if data.temperature is not None and data.temperature >= 39:
        severity_score += 10
        actions.append("sepsis_screening")

    severity_score = min(severity_score, 100)

    if severity_score >= 75:
        decision_level = "critical"
        actions.extend([
            "command_center_notification",
            "resource_allocation_request",
            "digital_twin_update"
        ])
    elif severity_score >= 45:
        decision_level = "high"
        actions.extend([
            "clinical_team_notification",
            "monitoring_frequency_increase"
        ])
    elif severity_score >= 20:
        decision_level = "moderate"
        actions.append("continue_monitoring")
    else:
        decision_level = "stable"
        actions.append("routine_observation")

    unique_actions = list(dict.fromkeys(actions))

    return severity_score, decision_level, unique_actions


@router.get("/ahos/supervisor/health")
async def supervisor_health():
    return {
        "status": "online",
        "engine": "Autonomous Decision Supervisor - Database Driven",
        "version": "10.0.5.3",
        "storage": "aiha_ahos.db",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/ahos/supervisor/evaluate")
async def evaluate_event(data: SupervisorInput):
    init_ahos_database()

    severity_score, decision_level, unique_actions = calculate_decision(data)

    now = datetime.utcnow().isoformat()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM decision_logs")
    count = cur.fetchone()["c"] + 1
    decision_id = f"ADS-DB-{count:05d}"

    cur.execute("""
        INSERT INTO decision_logs
        (decision_id, patient_id, source_engine, event_type, priority,
         severity_score, decision_level, recommended_actions, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        decision_id,
        data.patient_id,
        data.source_engine,
        data.event_type,
        data.priority,
        severity_score,
        decision_level,
        json.dumps(unique_actions),
        "decision_persisted",
        now
    ))

    conn.commit()

    cur.execute("SELECT * FROM decision_logs WHERE decision_id = ?", (decision_id,))
    row = dict(cur.fetchone())

    try:
        row["recommended_actions"] = json.loads(row.get("recommended_actions") or "[]")
    except Exception:
        row["recommended_actions"] = []

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "message": "Autonomous decision generated and persisted",
        "decision": row
    }


@router.get("/ahos/supervisor/decisions")
async def supervisor_decisions():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM decision_logs
        ORDER BY created_at DESC
        LIMIT 20
    """)

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
        "storage": "database",
        "total_decisions": len(rows),
        "decisions": rows
    }


@router.get("/ahos/supervisor/metrics")
async def supervisor_metrics():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as c FROM decision_logs")
    total = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM decision_logs WHERE decision_level='critical'")
    critical = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) as c FROM decision_logs WHERE decision_level='high'")
    high = cur.fetchone()["c"]

    cur.execute("SELECT AVG(severity_score) as avg_score FROM decision_logs")
    avg_score = cur.fetchone()["avg_score"] or 0

    conn.close()

    return {
        "status": "success",
        "storage": "database",
        "total_decisions": total,
        "critical_decisions": critical,
        "high_decisions": high,
        "average_severity_score": round(avg_score, 2),
        "human_approval_required": True,
        "autonomous_execution": "assistive_only"
    }


@router.get("/ahos/supervisor/recommendations")
async def supervisor_recommendations():
    init_ahos_database()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT recommended_actions
        FROM decision_logs
        ORDER BY created_at DESC
        LIMIT 10
    """)

    action_count = {}

    for row in cur.fetchall():
        try:
            actions = json.loads(row["recommended_actions"] or "[]")
        except Exception:
            actions = []

        for action in actions:
            action_count[action] = action_count.get(action, 0) + 1

    conn.close()

    ranked = sorted(action_count.items(), key=lambda x: x[1], reverse=True)

    return {
        "status": "success",
        "storage": "database",
        "recommendations": [
            {"action": action, "count": count}
            for action, count in ranked
        ],
        "policy": "Medical Safety First",
        "human_approval_required": True
    }


@router.get("/ahos/supervisor/policy")
async def supervisor_policy():
    return {
        "status": "active",
        "policy": "Medical Safety First",
        "autonomous_execution": "assistive_only",
        "human_approval_required": True,
        "critical_actions": [
            "icu_escalation",
            "shock_protocol_review",
            "resource_allocation_request",
            "command_center_notification"
        ]
    }
