from fastapi import APIRouter
from pathlib import Path
import json

router = APIRouter(
    prefix="/ahos/40.5/security",
    tags=["AHOS Phase 40.5 Security Integration"],
)

AUDIT_LOG = Path("reports/security_audit.jsonl")


@router.get("/health")
async def health():
    return {
        "phase": "40.5",
        "status": "ok",
        "audit_log_exists": AUDIT_LOG.exists(),
    }


@router.get("/audit/events")
async def audit_events(limit: int = 50):

    if not AUDIT_LOG.exists():
        return {
            "count": 0,
            "events": [],
        }

    events = []

    with AUDIT_LOG.open() as f:
        for line in f.readlines()[-limit:]:
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    return {
        "count": len(events),
        "events": events,
    }
