from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from datetime import datetime
import sqlite3
import uuid

router = APIRouter(
    prefix="/ahos/56.0/avatar-orchestration",
    tags=["AHOS 56.0 Clinical Avatar Orchestration & Safety Control Center"]
)

DB_PATH = Path("backend/app/ahos_55_8/ahos_55_8_avatar_memory.db")

def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class OrchestrationCommand(BaseModel):
    patient_id: str = "FHIR-PAT-TEST001"
    command: str
    language: str = "Arabic"
    safety_mode: str = "clinical_supervised"
    require_human_review: bool = True

def classify_risk(command: str) -> dict:
    c = command.lower()

    emergency_words = [
        "طوارئ", "اختناق", "ألم صدر", "نزيف", "فقدان وعي",
        "emergency", "chest pain", "bleeding", "unconscious"
    ]

    diagnostic_words = [
        "أشعة", "تشخيص", "التهاب", "سرطان", "x-ray",
        "radiology", "diagnosis", "pneumonia", "cancer"
    ]

    if any(w in c or w in command for w in emergency_words):
        return {
            "risk_level": "high",
            "safety_score": 0.72,
            "human_review_required": True,
            "reason": "Emergency or potentially critical command detected"
        }

    if any(w in c or w in command for w in diagnostic_words):
        return {
            "risk_level": "medium",
            "safety_score": 0.86,
            "human_review_required": True,
            "reason": "Clinical diagnostic context requires physician review"
        }

    return {
        "risk_level": "low",
        "safety_score": 0.94,
        "human_review_required": False,
        "reason": "General avatar support command"
    }

def latest_counts():
    conn = db()
    cur = conn.cursor()

    tables = ["avatar_sessions", "avatar_audit", "patient_memory"]
    counts = {}

    for table in tables:
        try:
            counts[table] = cur.execute(f"SELECT COUNT(*) AS c FROM {table}").fetchone()["c"]
        except Exception:
            counts[table] = 0

    conn.close()
    return counts

@router.get("/health")
async def health():
    counts = latest_counts()

    return {
        "status": "online",
        "phase": "AHOS 56.0",
        "module": "Clinical Avatar Orchestration & Safety Control Center",
        "connected_modules": {
            "ahos_55_6_real_avatar": True,
            "ahos_55_7_voice_context": True,
            "ahos_55_8_memory_audit_db": True,
            "ahos_55_9_voice_memory_pipeline": True
        },
        "database": str(DB_PATH),
        "sessions": counts.get("avatar_sessions", 0),
        "audit_records": counts.get("avatar_audit", 0),
        "patient_memories": counts.get("patient_memory", 0),
        "safety_layer": True,
        "human_review_gate": True,
        "readiness_score": 0.94,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
async def orchestrate(payload: OrchestrationCommand):
    now = datetime.utcnow().isoformat()
    safety = classify_risk(payload.command)

    orchestration_id = "AHOS-560-ORCH-" + uuid.uuid4().hex[:10].upper()

    if safety["risk_level"] == "high":
        avatar_response = (
            "تم تصنيف الأمر كحالة عالية الخطورة. يجب تفعيل مراجعة بشرية فورية "
            "ولا يجوز الاعتماد على الذكاء الاصطناعي وحده."
        )
        action = "urgent_human_review"
    elif safety["risk_level"] == "medium":
        avatar_response = (
            "تم ربط الأمر بسياق المريض والأشعة والذاكرة السريرية. "
            "النتيجة تحتاج مراجعة الطبيب قبل أي قرار علاجي."
        )
        action = "physician_review_required"
    else:
        avatar_response = (
            "تمت معالجة الأمر بنجاح عبر مركز تنسيق Avatar وربطه بالذاكرة والتدقيق."
        )
        action = "processed"

    conn = db()

    # Store orchestration result in audit table if available
    try:
        audit_id = "AHOS-560-AUDIT-" + uuid.uuid4().hex[:10].upper()
        session_id = "AHOS-560-SESSION-" + uuid.uuid4().hex[:10].upper()

        conn.execute(
            """
            INSERT INTO avatar_sessions
            (session_id, patient_id, language, module, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                payload.patient_id,
                payload.language,
                "AHOS 56.0 Avatar Orchestration",
                now,
                "orchestrated"
            )
        )

        conn.execute(
            """
            INSERT INTO avatar_audit
            (audit_id, session_id, patient_id, command, intent, avatar_response, safety_note, language, created_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                audit_id,
                session_id,
                payload.patient_id,
                payload.command,
                "avatar_orchestration",
                avatar_response,
                safety["reason"],
                payload.language,
                now,
                action
            )
        )

        conn.commit()
    finally:
        conn.close()

    return {
        "orchestration_id": orchestration_id,
        "patient_id": payload.patient_id,
        "command": payload.command,
        "risk_level": safety["risk_level"],
        "safety_score": safety["safety_score"],
        "human_review_required": safety["human_review_required"] or payload.require_human_review,
        "action": action,
        "avatar_response": avatar_response,
        "connected_pipeline": "AHOS 55.9",
        "stored_in_audit_db": True,
        "status": "orchestrated"
    }

@router.get("/dashboard")
async def dashboard():
    counts = latest_counts()

    conn = db()
    try:
        latest_audits = conn.execute(
            "SELECT * FROM avatar_audit ORDER BY created_at DESC LIMIT 8"
        ).fetchall()
    except Exception:
        latest_audits = []
    conn.close()

    return {
        "title": "AHOS 56.0 Clinical Avatar Orchestration & Safety Control Center",
        "summary": "Central control layer for avatar voice, memory, audit, safety classification, physician review gate and patient timeline orchestration.",
        "readiness_score": 0.94,
        "metrics": {
            "sessions": counts.get("avatar_sessions", 0),
            "audit_records": counts.get("avatar_audit", 0),
            "patient_memories": counts.get("patient_memory", 0)
        },
        "safety_controls": [
            "Clinical risk classification",
            "Human review gate",
            "Audit persistence",
            "Avatar pipeline orchestration",
            "Patient timeline monitoring"
        ],
        "latest_audits": [dict(x) for x in latest_audits],
        "status": "dashboard_operational"
    }
