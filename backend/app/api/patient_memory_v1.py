from fastapi import APIRouter
from datetime import datetime
from pathlib import Path
import json

router = APIRouter(prefix="/patient-memory", tags=["AI Longitudinal Patient Memory"])

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MEMORY_FILE = PROJECT_ROOT / "patient_memory.json"

def read_memory():
    if not MEMORY_FILE.exists():
        return {}
    try:
        return json.loads(MEMORY_FILE.read_text())
    except Exception:
        return {}

def write_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

@router.post("/{patient_id}/add")
def add_memory(patient_id: str, payload: dict):
    memory = read_memory()

    if patient_id not in memory:
        memory[patient_id] = []

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "type": payload.get("type", "clinical_note"),
        "summary": payload.get("summary"),
        "source": payload.get("source", "AI Clinical"),
        "risk_level": payload.get("risk_level", "moderate")
    }

    memory[patient_id].append(entry)
    write_memory(memory)

    return {
        "saved": True,
        "patient_id": patient_id,
        "file": str(MEMORY_FILE),
        "entry": entry
    }

@router.get("/{patient_id}")
def get_memory(patient_id: str):
    memory = read_memory()
    return {
        "patient_id": patient_id,
        "file": str(MEMORY_FILE),
        "memory": memory.get(patient_id, [])
    }
