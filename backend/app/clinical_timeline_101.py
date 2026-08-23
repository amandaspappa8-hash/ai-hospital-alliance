from fastapi import APIRouter
from pathlib import Path
from datetime import datetime
import sqlite3, json

router = APIRouter(prefix="/aiha/10.1", tags=["AIHA 10.1 Unified Clinical Timeline"])

DB_PATH = Path("aiha_1007_live.db")

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def parse_json(value):
    if not value:
        return {}
    try:
        return json.loads(value) if isinstance(value, str) else value
    except Exception:
        return {"raw": value}

def severity_for(kind, payload):
    text = json.dumps(payload).lower()
    if "critical" in text or "high" in text or "bleeding risk" in text:
        return "CRITICAL"
    if "moderate" in text or "abnormal" in text:
        return "WARNING"
    return "NORMAL"

@router.get("/health")
def health():
    return {
        "status": "online",
        "engine": "Unified Clinical Timeline Engine",
        "stage": "AI Hospital Alliance 10.1",
        "database": str(DB_PATH),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

@router.get("/timeline/{patient_id}")
def patient_timeline(patient_id: str):
    conn = db()
    events = []

    for r in conn.execute("SELECT * FROM patient_states WHERE patient_id=? ORDER BY created_at DESC", (patient_id,)).fetchall():
        payload = parse_json(r["data"])
        events.append({
            "id": f"STATE-{r['id']}",
            "type": "PATIENT_STATE",
            "title": "Live patient state updated",
            "source": "GMIN",
            "severity": severity_for("state", payload),
            "timestamp": r["created_at"],
            "payload": payload
        })

    for r in conn.execute("SELECT * FROM medical_memory_records WHERE patient_id=? ORDER BY created_at DESC", (patient_id,)).fetchall():
        payload = parse_json(r["data"])
        memory_type = str(r["memory_type"]).upper()
        events.append({
            "id": f"MEM-{r['id']}",
            "type": memory_type,
            "title": f"{memory_type} memory created",
            "source": memory_type,
            "severity": severity_for(memory_type, payload),
            "timestamp": r["created_at"],
            "payload": payload
        })

    for r in conn.execute("SELECT * FROM decision_logs WHERE patient_id=? ORDER BY created_at DESC", (patient_id,)).fetchall():
        payload = parse_json(r["data"])
        events.append({
            "id": f"DEC-{r['id']}",
            "type": "DECISION",
            "title": f"Decision Supervisor: {r['decision_type']}",
            "source": "Decision Supervisor",
            "severity": "CRITICAL" if str(r["risk_level"]).upper() == "HIGH" else "WARNING",
            "timestamp": r["created_at"],
            "payload": payload
        })

    events = sorted(events, key=lambda x: x["timestamp"], reverse=True)

    conn.close()

    return {
        "status": "success",
        "patient_id": patient_id,
        "timeline_count": len(events),
        "critical_count": len([e for e in events if e["severity"] == "CRITICAL"]),
        "warning_count": len([e for e in events if e["severity"] == "WARNING"]),
        "normal_count": len([e for e in events if e["severity"] == "NORMAL"]),
        "timeline": events,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
