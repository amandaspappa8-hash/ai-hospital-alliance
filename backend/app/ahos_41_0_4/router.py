from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.ahos_41_0_4.infer_rsna_baseline import predict

router = APIRouter(
    prefix="/ahos/41.0/rsna-radiology-ai",
    tags=["AHOS 41.0 RSNA Radiology AI"]
)

class RSNAInferenceRequest(BaseModel):
    image_path: str

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.0.6",
        "module": "RSNA Radiology AI API",
        "model": "ResNet18 baseline",
        "dataset": "RSNA Pneumonia Detection Challenge"
    }

@router.post("/predict")
async def predict_rsna(request: RSNAInferenceRequest):
    return {
        "status": "success",
        "phase": "AHOS 41.0.6",
        "result": predict(request.image_path)
    }
