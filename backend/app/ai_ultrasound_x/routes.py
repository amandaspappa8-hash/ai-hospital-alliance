from fastapi import APIRouter
from backend.app.ai_ultrasound_x.inference_engine import engine
from backend.app.ai_ultrasound_x.segmentation_engine import run_segmentation_demo

router = APIRouter(prefix="/ai-ultrasound-x", tags=["AI Ultrasound X"])

@router.get("/health")
def health():
    return {
        "status": "online",
        "module": "AI Ultrasound X",
        "version": "3.3",
        "mode": engine.device
    }

@router.post("/analyze-demo")
def analyze_demo():
    result = engine.analyze([[0, 1], [2, 3]])
    return {
        "status": "success",
        "result": result
    }

@router.post("/segmentation-demo")
def segmentation_demo():
    result = run_segmentation_demo()
    return {
        "status": "success",
        "result": result
    }
