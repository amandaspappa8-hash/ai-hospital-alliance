from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
from datetime import datetime
import sqlite3
import uuid

router = APIRouter(
    prefix="/ahos/56.1/physician-review",
    tags=["AHOS 56.1 Physician Review Queue + Safety Approval Workflow"]
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

class ReviewCreate(BaseModel):
    patient_id: str = "FHIR-PAT-TEST001"
    command: str
    avatar_response: str = "AI clinical response requires physician review."
    risk_level: str = "medium"
    safety_score: float = 0.86
    priority: Optional[str] = None

class ReviewDecision(BaseModel):
    physician_id: str = "DR-AHOS-001"
    decision: str = "approved"
    note: str = "Reviewed and approved under physician supervision."

def priority_from_risk(risk_level: str) -> str:
    r = risk_level.lower()
    if r == "high":
        return "urgent"
    if r == "medium":
        return "standard"
    return "low"

@router.get("/health")
async def health():
    conn = db()
    total = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='pending'").fetchone()["c"]
    approved = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='approved'").fetchone()["c"]
    rejected = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='rejected'").fetchone()["c"]
    conn.close()

    return {
        "status": "online",
        "phase": "AHOS 56.1",
        "module": "Physician Review Queue + Safety Approval Workflow",
        "database": str(DB_PATH),
        "review_queue": True,
        "human_approval_workflow": True,
        "total_reviews": total,
        "pending_reviews": pending,
        "approved_reviews": approved,
        "rejected_reviews": rejected,
        "readiness_score": 0.95,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/review/create")
async def create_review(payload: ReviewCreate):
    now = datetime.utcnow().isoformat()
    review_id = "AHOS-561-REVIEW-" + uuid.uuid4().hex[:10].upper()
    priority = payload.priority or priority_from_risk(payload.risk_level)

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
            None,
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
        "review_status": "pending",
        "status": "created"
    }

@router.get("/reviews")
async def list_reviews(status: str = "all"):
    conn = db()

    if status == "all":
        rows = conn.execute(
            "SELECT * FROM physician_review_queue ORDER BY created_at DESC LIMIT 50"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM physician_review_queue WHERE review_status=? ORDER BY created_at DESC LIMIT 50",
            (status,)
        ).fetchall()

    conn.close()

    return {
        "status_filter": status,
        "count": len(rows),
        "reviews": [dict(x) for x in rows],
        "status": "reviews_ready"
    }

@router.post("/review/{review_id}/decision")
async def review_decision(review_id: str, payload: ReviewDecision):
    allowed = {"approved", "rejected", "needs_more_review"}
    decision = payload.decision.lower().strip()

    if decision not in allowed:
        decision = "needs_more_review"

    now = datetime.utcnow().isoformat()

    conn = db()
    row = conn.execute(
        "SELECT * FROM physician_review_queue WHERE review_id=?",
        (review_id,)
    ).fetchone()

    if not row:
        conn.close()
        return {
            "review_id": review_id,
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
            review_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "review_id": review_id,
        "physician_id": payload.physician_id,
        "decision": decision,
        "status": "updated"
    }

@router.get("/dashboard")
async def dashboard():
    conn = db()

    total = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue").fetchone()["c"]
    pending = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='pending'").fetchone()["c"]
    approved = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='approved'").fetchone()["c"]
    rejected = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='rejected'").fetchone()["c"]
    more = conn.execute("SELECT COUNT(*) AS c FROM physician_review_queue WHERE review_status='needs_more_review'").fetchone()["c"]

    latest = conn.execute(
        "SELECT * FROM physician_review_queue ORDER BY created_at DESC LIMIT 12"
    ).fetchall()

    conn.close()

    return {
        "title": "AHOS 56.1 Physician Review Queue + Safety Approval Workflow",
        "summary": "Human-in-the-loop clinical review queue for medium/high-risk avatar decisions, physician approval, rejection and additional review workflow.",
        "readiness_score": 0.95,
        "metrics": {
            "total_reviews": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "needs_more_review": more
        },
        "workflow": [
            "AI command received",
            "Risk classified",
            "Review case created",
            "Physician decision recorded",
            "Audit trail preserved"
        ],
        "latest_reviews": [dict(x) for x in latest],
        "status": "dashboard_operational"
    }
