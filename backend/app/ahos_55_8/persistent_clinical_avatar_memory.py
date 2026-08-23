from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import sqlite3
import uuid
from pathlib import Path

router = APIRouter(
    prefix="/ahos/55.8/avatar-memory-audit",
    tags=["AHOS 55.8 Persistent Clinical Avatar Memory + Audit Database"]
)

DB_PATH = Path("backend/app/ahos_55_8/ahos_55_8_avatar_memory.db")

def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS avatar_sessions (
        session_id TEXT PRIMARY KEY,
        patient_id TEXT,
        language TEXT,
        module TEXT,
        created_at TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS avatar_audit (
        audit_id TEXT PRIMARY KEY,
        session_id TEXT,
        patient_id TEXT,
        command TEXT,
        intent TEXT,
        avatar_response TEXT,
        safety_note TEXT,
        language TEXT,
        created_at TEXT,
        status TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patient_memory (
        memory_id TEXT PRIMARY KEY,
        patient_id TEXT,
        memory_type TEXT,
        memory_text TEXT,
        source_module TEXT,
        created_at TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

class SessionCreate(BaseModel):
    patient_id: str = "FHIR-PAT-TEST001"
    language: str = "Arabic"
    module: str = "AHOS 55.8 Avatar Memory"

class AuditCreate(BaseModel):
    session_id: Optional[str] = None
    patient_id: str = "FHIR-PAT-TEST001"
    command: str
    intent: str = "clinical_avatar_command"
    avatar_response: str
    safety_note: str = "AI support only. Final decision must be made by a licensed clinician."
    language: str = "Arabic"

class MemoryCreate(BaseModel):
    patient_id: str = "FHIR-PAT-TEST001"
    memory_type: str = "clinical_context"
    memory_text: str
    source_module: str = "AHOS 55.8"

@router.get("/health")
async def health():
    conn = db()
    cur = conn.cursor()
    sessions = cur.execute("SELECT COUNT(*) AS c FROM avatar_sessions").fetchone()["c"]
    audits = cur.execute("SELECT COUNT(*) AS c FROM avatar_audit").fetchone()["c"]
    memories = cur.execute("SELECT COUNT(*) AS c FROM patient_memory").fetchone()["c"]
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS 55.8",
        "module": "Persistent Clinical Avatar Memory + Audit Database",
        "database": str(DB_PATH),
        "persistent_storage": True,
        "sessions": sessions,
        "audit_records": audits,
        "patient_memories": memories,
        "readiness_score": 0.90,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/session/create")
async def create_session(payload: SessionCreate):
    session_id = "AHOS-558-SESSION-" + uuid.uuid4().hex[:10].upper()
    created_at = datetime.utcnow().isoformat()

    conn = db()
    conn.execute(
        """
        INSERT INTO avatar_sessions
        (session_id, patient_id, language, module, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (session_id, payload.patient_id, payload.language, payload.module, created_at, "active")
    )
    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "patient_id": payload.patient_id,
        "language": payload.language,
        "status": "created"
    }

@router.post("/audit/create")
async def create_audit(payload: AuditCreate):
    audit_id = "AHOS-558-AUDIT-" + uuid.uuid4().hex[:10].upper()
    created_at = datetime.utcnow().isoformat()

    conn = db()
    conn.execute(
        """
        INSERT INTO avatar_audit
        (audit_id, session_id, patient_id, command, intent, avatar_response, safety_note, language, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            audit_id,
            payload.session_id,
            payload.patient_id,
            payload.command,
            payload.intent,
            payload.avatar_response,
            payload.safety_note,
            payload.language,
            created_at,
            "stored"
        )
    )
    conn.commit()
    conn.close()

    return {
        "audit_id": audit_id,
        "patient_id": payload.patient_id,
        "status": "stored"
    }

@router.post("/memory/create")
async def create_memory(payload: MemoryCreate):
    memory_id = "AHOS-558-MEMORY-" + uuid.uuid4().hex[:10].upper()
    created_at = datetime.utcnow().isoformat()

    conn = db()
    conn.execute(
        """
        INSERT INTO patient_memory
        (memory_id, patient_id, memory_type, memory_text, source_module, created_at, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            memory_id,
            payload.patient_id,
            payload.memory_type,
            payload.memory_text,
            payload.source_module,
            created_at,
            "stored"
        )
    )
    conn.commit()
    conn.close()

    return {
        "memory_id": memory_id,
        "patient_id": payload.patient_id,
        "status": "stored"
    }

@router.get("/patient/{patient_id}/timeline")
async def patient_timeline(patient_id: str):
    conn = db()

    sessions = conn.execute(
        "SELECT * FROM avatar_sessions WHERE patient_id=? ORDER BY created_at DESC LIMIT 20",
        (patient_id,)
    ).fetchall()

    audits = conn.execute(
        "SELECT * FROM avatar_audit WHERE patient_id=? ORDER BY created_at DESC LIMIT 20",
        (patient_id,)
    ).fetchall()

    memories = conn.execute(
        "SELECT * FROM patient_memory WHERE patient_id=? ORDER BY created_at DESC LIMIT 20",
        (patient_id,)
    ).fetchall()

    conn.close()

    return {
        "patient_id": patient_id,
        "sessions": [dict(x) for x in sessions],
        "audits": [dict(x) for x in audits],
        "memories": [dict(x) for x in memories],
        "status": "timeline_ready"
    }

@router.get("/dashboard")
async def dashboard():
    conn = db()
    cur = conn.cursor()

    sessions = cur.execute("SELECT COUNT(*) AS c FROM avatar_sessions").fetchone()["c"]
    audits = cur.execute("SELECT COUNT(*) AS c FROM avatar_audit").fetchone()["c"]
    memories = cur.execute("SELECT COUNT(*) AS c FROM patient_memory").fetchone()["c"]

    latest_audits = cur.execute(
        "SELECT * FROM avatar_audit ORDER BY created_at DESC LIMIT 10"
    ).fetchall()

    conn.close()

    return {
        "title": "AHOS 55.8 Persistent Clinical Avatar Memory + Audit Database",
        "summary": "Persistent database layer for avatar sessions, clinical commands, patient memory, safety audit logs and longitudinal patient context.",
        "readiness_score": 0.90,
        "metrics": {
            "sessions": sessions,
            "audit_records": audits,
            "patient_memories": memories
        },
        "latest_audits": [dict(x) for x in latest_audits],
        "status": "dashboard_operational"
    }
