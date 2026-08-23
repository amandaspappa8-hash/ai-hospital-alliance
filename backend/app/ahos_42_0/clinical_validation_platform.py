from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/42.0",
    tags=["AHOS 42.0 Clinical Validation & Real-World Evidence Platform"]
)

studies = {}
cases = []

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 42.0",
        "service": "Clinical Validation & Real-World Evidence Platform"
    }

@router.post("/study/create")
async def create_study(
    study_name: str,
    disease: str,
    authority: str
):
    sid = str(uuid.uuid4())

    studies[sid] = {
        "study_id": sid,
        "study_name": study_name,
        "disease": disease,
        "authority": authority,
        "created_at": datetime.utcnow().isoformat(),
        "total_cases": 0
    }

    return studies[sid]

@router.post("/case/add")
async def add_case(
    study_id: str,
    ground_truth: int,
    prediction: int
):
    if study_id not in studies:
        return {"error": "Study not found"}

    case = {
        "case_id": str(uuid.uuid4()),
        "study_id": study_id,
        "ground_truth": ground_truth,
        "prediction": prediction,
        "created_at": datetime.utcnow().isoformat()
    }

    cases.append(case)
    studies[study_id]["total_cases"] += 1

    return case

@router.get("/study/{sid}")
async def get_study(sid: str):
    return studies.get(sid, {"error": "Study not found"})

@router.get("/metrics/{sid}")
async def metrics(sid: str):
    if sid not in studies:
        return {"error": "Study not found"}

    tp = fp = tn = fn = 0

    for c in cases:
        if c["study_id"] != sid:
            continue

        gt = c["ground_truth"]
        pr = c["prediction"]

        if gt == 1 and pr == 1:
            tp += 1
        elif gt == 0 and pr == 1:
            fp += 1
        elif gt == 0 and pr == 0:
            tn += 1
        elif gt == 1 and pr == 0:
            fn += 1

    sensitivity = tp/(tp+fn) if (tp+fn) else 0
    specificity = tn/(tn+fp) if (tn+fp) else 0
    accuracy = (tp+tn)/max((tp+tn+fp+fn),1)
    roc_auc = (sensitivity + specificity)/2

    return {
        "study_id": sid,
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "sensitivity": round(sensitivity,4),
        "specificity": round(specificity,4),
        "accuracy": round(accuracy,4),
        "roc_auc_estimate": round(roc_auc,4)
    }

@router.get("/dashboard")
async def dashboard():
    return {
        "phase": "AHOS 42.0",
        "total_studies": len(studies),
        "total_cases": len(cases),
        "studies": list(studies.values())
    }

@router.get("/kpis")
async def kpis():
    return {
        "phase": "AHOS 42.0",
        "studies": len(studies),
        "cases": len(cases),
        "clinical_validation_status": "READY",
        "rwe_status": "ACTIVE"
    }
