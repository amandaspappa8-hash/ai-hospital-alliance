from fastapi import APIRouter, WebSocket, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import asyncio

from backend.app.db import get_db
from backend.app.models import Alert

router = APIRouter(prefix="/enterprise-notifications", tags=["Enterprise Notifications"])


@router.get("/")
def list_notifications(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.created_at.desc()).limit(50).all()

    notifications = [
        {
            "id": a.id,
            "severity": a.severity,
            "type": a.source,
            "message": a.message,
            "unread": not bool(a.is_read),
            "patient_id": a.patient_id,
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in alerts
    ]

    return {
        "unread_count": sum(1 for n in notifications if n["unread"]),
        "notifications": notifications,
    }


@router.post("/mark-read")
def mark_read(db: Session = Depends(get_db)):
    updated = (
        db.query(Alert)
        .filter(Alert.is_read == False)
        .update({"is_read": True}, synchronize_session=False)
    )
    db.commit()
    return {"updated": True, "updated_count": updated, "unread_count": 0}


@router.websocket("/ws/live-clinical-events")
async def live_events(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({
            "timestamp": datetime.utcnow().isoformat(),
            "severity": "high",
            "event": "critical_lab",
            "message": "Critical lab alert: potassium 6.2 mmol/L",
        })
        await asyncio.sleep(8)
