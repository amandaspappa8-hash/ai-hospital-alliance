from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import json

from backend.app.db import get_db

router = APIRouter(prefix="/audit", tags=["Audit Trail"])


def save_audit(
    db: Session,
    *,
    user_id: str,
    action: str,
    resource: str,
    resource_id=None,
    details=None,
    success=True,
):
    details_text = json.dumps(details or {}, ensure_ascii=False)

    db.execute(
        text("""
            INSERT INTO audit_logs
                (user_id, action, resource, resource_id, details, ip_address, success, timestamp)
            VALUES
                (:user_id, :action, :resource, :resource_id, :details, :ip_address, :success, :timestamp)
        """),
        {
            "user_id": user_id or "system",
            "action": action,
            "resource": resource,
            "resource_id": resource_id,
            "details": details_text,
            "ip_address": None,
            "success": success,
            "timestamp": datetime.utcnow(),
        },
    )

    db.commit()


def fetch_logs(db: Session, limit: int = 100):
    rows = db.execute(
        text("""
            SELECT
                id,
                user_id,
                action,
                resource,
                resource_id,
                details,
                ip_address,
                success,
                timestamp
            FROM audit_logs
            ORDER BY timestamp DESC
            LIMIT :limit
        """),
        {"limit": limit},
    ).mappings().all()

    return [
        {
            "id": r["id"],
            "timestamp": r["timestamp"].isoformat() if r["timestamp"] else None,
            "user_id": r["user_id"],
            "action": r["action"],
            "resource": r["resource"],
            "resource_id": r["resource_id"],
            "details": json.loads(r["details"]) if r["details"] else {},
            "ip_address": r["ip_address"],
            "success": r["success"],
        }
        for r in rows
    ]


@router.post("/log")
def log_action(payload: dict, db: Session = Depends(get_db)):
    entry = {
        "doctor": payload.get("doctor"),
        "ai_decision": payload.get("ai_decision"),
        "pharmacist": payload.get("pharmacist"),
        "status": payload.get("status"),
    }

    save_audit(
        db,
        user_id=payload.get("doctor") or payload.get("user_id") or "system",
        action="ai_decision.log",
        resource="AIRecommendation",
        resource_id=payload.get("patient_id"),
        details=entry,
        success=True,
    )

    return {
        "saved": True,
        "storage": "postgresql",
        "entry": entry,
    }


# AHOS-R13C17E disabled secondary route: @router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return {
        "storage": "postgresql",
        "logs": fetch_logs(db),
    }


@router.get("/persistent-logs")
def persistent_logs(db: Session = Depends(get_db)):
    return {
        "storage": "postgresql",
        "logs": fetch_logs(db),
    }


@router.post("/approve")
def approve_decision(payload: dict, db: Session = Depends(get_db)):
    entry = {
        "patient_id": payload.get("patient_id"),
        "doctor": payload.get("doctor"),
        "pharmacist": payload.get("pharmacist"),
        "ai_decision": payload.get("ai_decision"),
        "status": "approved",
        "approval_type": payload.get(
            "approval_type",
            "doctor_and_pharmacist",
        ),
        "medical_legal_note": (
            "Final decision approved by responsible clinician."
        ),
    }

    save_audit(
        db,
        user_id=payload.get("doctor") or "system",
        action="ai_decision.approve",
        resource="AIRecommendation",
        resource_id=payload.get("patient_id"),
        details=entry,
        success=True,
    )

    return {
        "approved": True,
        "storage": "postgresql",
        "entry": entry,
    }


@router.post("/reject")
def reject_decision(payload: dict, db: Session = Depends(get_db)):
    entry = {
        "patient_id": payload.get("patient_id"),
        "doctor": payload.get("doctor"),
        "pharmacist": payload.get("pharmacist"),
        "ai_decision": payload.get("ai_decision"),
        "status": "rejected",
        "reason": payload.get("reason"),
        "medical_legal_note": (
            "AI recommendation rejected by clinician."
        ),
    }

    save_audit(
        db,
        user_id=payload.get("doctor") or "system",
        action="ai_decision.reject",
        resource="AIRecommendation",
        resource_id=payload.get("patient_id"),
        details=entry,
        success=True,
    )

    return {
        "rejected": True,
        "storage": "postgresql",
        "entry": entry,
    }
