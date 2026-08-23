from fastapi import APIRouter
from backend.app.ai_core.engine import engine

router = APIRouter(prefix="/ai-engine", tags=["AI Engine"])

@router.get("/health")
def ai_health():
    return engine.health()

@router.get("/analyze/{patient_id}")
def analyze(patient_id: str):
    return engine.analyze_ct(patient_id)
