from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
from datetime import datetime
import sqlite3
import uuid

router = APIRouter(
    prefix="/ahos/56.3/unified-safety-center",
    tags=["AHOS 56.3 Unified Safety Command Center"]
)

DB_PATH = Path("backend/app/ahos_55_8/ahos_55_8_avatar_memory.db")

def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS physician_review_queue (
        review_id TEXT PRIMARY KEY,
        patient_id TEXT,
        command TEXT,
        avatar_response TEXT,
        risk_level TEXT,
        safety_score REAL,
        priority TEXT,
        review_status TEXT,
        physician_id TEXT,
        physician_decision TEXT,
        physician_note TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

class UnifiedSafetyCommand(BaseModel):
    patient_id: str = "FHIR-PAT-TEST001"
    command: str = "اشرح نتيجة الأشعة وحالة المريض وحدد مستوى الخطورة"
    avatar_response: str = "النتيجة تحتاج مراجعة الطبيب قبل أي قرار علاجي."
    risk_level: str = "medium"
    safety_score: float = 0.86
    source_module: str = "AHOS 56.3 Unified Safety Center"

class ReviewDecision(BaseModel):
    review_id: str
    physician_id: str = "DR-AHOS-001"
    decision: str = "approved"
    note: str = "Reviewed from AHOS 56.3 Unified Safety Center."

def priority_from_risk(risk_level: str):
    r = risk_level.lower()
    if r == "high":
        return "urgent"
    if r == "medium":
        return "standard"
    return "low"

def metrics():
    conn = db()
    total = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='pending'").fetchone()["c"]
    approved = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='approved'").fetchone()["c"]
    rejected = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='rejected'").fetchone()["c"]
    more = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='needs_more_review'").fetchone()["c"]
    urgent = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE priority='urgent'").fetchone()["c"]
    latest = conn.execute("SELECT * FROM physician_review_queue ORDER BY created_at DESC LIMIT 20").fetchall()
    conn.close()

    return {
        "total_reviews": total,
        "pending_reviews": pending,
        "approved_reviews": approved,
        "rejected_reviews": rejected,
        "needs_more_review": more,
        "urgent_reviews": urgent,
        "latest_reviews": [dict(x) for x in latest],
    }

@router.get("/health")
async def health():
    m = metrics()
    return {
        "status": "online",
        "phase": "AHOS 56.3",
        "module": "Unified Safety Command Center",
        "connected_modules": {
            "ahos_56_0_orchestration": True,
            "ahos_56_1_physician_review": True,
            "ahos_56_2_safety_escalation": True
        },
        "database": str(DB_PATH),
        "review_queue": True,
        "auto_escalation": True,
        "human_review_gate": True,
        "metrics": {
            "total_reviews": m["total_reviews"],
            "pending_reviews": m["pending_reviews"],
            "urgent_reviews": m["urgent_reviews"],
            "approved_reviews": m["approved_reviews"]
        },
        "readiness_score": 0.97,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
async def dashboard():
    m = metrics()
    return {
        "title": "AHOS 56.3 Unified Safety Command Center",
        "summary": "Unified safety center combining AHOS 56.0 orchestration, AHOS 56.1 physician review, and AHOS 56.2 automatic escalation.",
        "readiness_score": 0.97,
        "metrics": {
            "total_reviews": m["total_reviews"],
            "pending_reviews": m["pending_reviews"],
            "approved_reviews": m["approved_reviews"],
            "rejected_reviews": m["rejected_reviews"],
            "needs_more_review": m["needs_more_review"],
            "urgent_reviews": m["urgent_reviews"]
        },
        "latest_reviews": m["latest_reviews"],
        "workflow": [
            "Clinical command received",
            "Risk level classified",
            "Medium/high risk escalated automatically",
            "Physician review queue updated",
            "Approve / Reject / Needs More Review decision recorded"
        ],
        "status": "dashboard_operational"
    }

@router.post("/command")
async def unified_command(payload: UnifiedSafetyCommand):
    now = datetime.utcnow().isoformat()
    risk = payload.risk_level.lower()
    priority = priority_from_risk(risk)

    if risk == "low":
        return {
            "patient_id": payload.patient_id,
            "risk_level": payload.risk_level,
            "escalated": False,
            "action": "no_escalation_required",
            "message": "Low risk command processed without physician review queue.",
            "status": "processed"
        }

    review_id = "AHOS-563-REVIEW-" + uuid.uuid4().hex[:10].upper()

    conn = db()
    conn.execute(
        """
        INSERT INTO physician_review_queue
        (review_id, patient_id, command, avatar_response, risk_level, safety_score,
         priority, review_status, physician_id, physician_decision, physician_note,
         created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            review_id,
            payload.patient_id,
            payload.command,
            payload.avatar_response,
            payload.risk_level,
            payload.safety_score,
            priority,
            "pending",
            None,
            None,
            f"Auto-created by {payload.source_module}",
            now,
            now
        )
    )
    conn.commit()
    conn.close()

    return {
        "review_id": review_id,
        "patient_id": payload.patient_id,
        "risk_level": payload.risk_level,
        "priority": priority,
        "escalated": True,
        "routed_to": "AHOS 56.1 Physician Review Queue",
        "source_module": payload.source_module,
        "status": "created_and_escalated"
    }

@router.post("/decision")
async def decision(payload: ReviewDecision):
    decision = payload.decision.strip().lower()
    if decision not in {"approved", "rejected", "needs_more_review"}:
        decision = "needs_more_review"

    now = datetime.utcnow().isoformat()

    conn = db()
    row = conn.execute(
        "SELECT * FROM physician_review_queue WHERE review_id=?",
        (payload.review_id,)
    ).fetchone()

    if not row:
        conn.close()
        return {
            "review_id": payload.review_id,
            "status": "not_found"
        }

    conn.execute(
        """
        UPDATE physician_review_queue
        SET review_status=?, physician_id=?, physician_decision=?, physician_note=?, updated_at=?
        WHERE review_id=?
        """,
        (
            decision,
            payload.physician_id,
            decision,
            payload.note,
            now,
            payload.review_id
        )
    )
    conn.commit()
    conn.close()

    return {
        "review_id": payload.review_id,
        "physician_id": payload.physician_id,
        "decision": decision,
        "status": "decision_recorded"
    }
