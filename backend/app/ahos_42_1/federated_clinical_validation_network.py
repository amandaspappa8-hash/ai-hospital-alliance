from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/42.1",
    tags=["AHOS 42.1 Federated Clinical Validation Network"]
)

hospital_nodes = {}
validation_cases = []

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 42.1",
        "service": "Federated Clinical Validation Network"
    }

@router.post("/node/register")
async def register_node(
    hospital_name: str,
    country: str
):
    nid = str(uuid.uuid4())

    hospital_nodes[nid] = {
        "node_id": nid,
        "hospital_name": hospital_name,
        "country": country,
        "registered_at": datetime.utcnow().isoformat(),
        "total_cases": 0
    }

    return hospital_nodes[nid]

@router.post("/case/add")
async def add_case(
    node_id: str,
    ground_truth: int,
    prediction: int
):
    if node_id not in hospital_nodes:
        return {"error": "Node not found"}

    cid = str(uuid.uuid4())

    case = {
        "case_id": cid,
        "node_id": node_id,
        "ground_truth": ground_truth,
        "prediction": prediction,
        "created_at": datetime.utcnow().isoformat()
    }

    validation_cases.append(case)
    hospital_nodes[node_id]["total_cases"] += 1

    return case

@router.get("/node/{nid}")
async def get_node(nid: str):
    return hospital_nodes.get(
        nid,
        {"error": "Node not found"}
    )

@router.get("/metrics/global")
async def global_metrics():
    tp = fp = tn = fn = 0

    for c in validation_cases:
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
        "total_nodes": len(hospital_nodes),
        "total_cases": len(validation_cases),
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "global_sensitivity": round(sensitivity,4),
        "global_specificity": round(specificity,4),
        "global_accuracy": round(accuracy,4),
        "global_roc_auc_estimate": round(roc_auc,4)
    }

@router.get("/dashboard")
async def dashboard():
    return {
        "phase": "AHOS 42.1",
        "total_nodes": len(hospital_nodes),
        "total_cases": len(validation_cases),
        "nodes": list(hospital_nodes.values())
    }

@router.get("/kpis")
async def kpis():
    return {
        "phase": "AHOS 42.1",
        "federated_validation_status": "ACTIVE",
        "multi_center_trials": len(hospital_nodes),
        "validation_cases": len(validation_cases)
    }
