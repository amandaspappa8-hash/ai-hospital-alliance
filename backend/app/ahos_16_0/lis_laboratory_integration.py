from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random
import uuid

router = APIRouter(
    prefix="/ahos/16.0/lis",
    tags=["AHOS 16.0.4 LIS Laboratory Integration"]
)

class LISOrderRequest(BaseModel):
    patient_id: str = "P-1001"
    encounter_id: str = "ENC-2026-001"
    test_code: str = "CBC"
    test_name: str = "Complete Blood Count"
    priority: str = "URGENT"

class LISResultRequest(BaseModel):
    patient_id: str = "P-1001"
    order_id: str = "LAB-ORDER-1001"
    test_code: str = "CBC"
    result_value: str = "Normal"
    unit: str = ""
    abnormal_flag: str = "N"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "16.0.4",
        "engine": "LIS Laboratory Integration",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/order")
def create_lab_order(req: LISOrderRequest):
    return {
        "status": "success",
        "order_id": f"LAB-{uuid.uuid4()}",
        "patient_id": req.patient_id,
        "encounter_id": req.encounter_id,
        "test_code": req.test_code,
        "test_name": req.test_name,
        "priority": req.priority,
        "lis_status": "ORDER_CREATED",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/result")
def receive_lab_result(req: LISResultRequest):
    return {
        "status": "success",
        "result_id": f"RES-{uuid.uuid4()}",
        "patient_id": req.patient_id,
        "order_id": req.order_id,
        "test_code": req.test_code,
        "result_value": req.result_value,
        "unit": req.unit,
        "abnormal_flag": req.abnormal_flag,
        "clinical_alert": req.abnormal_flag in ["H", "L", "HH", "LL", "A"],
        "lis_status": "RESULT_RECEIVED",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/demo-results/{patient_id}")
def demo_results(patient_id: str):
    return {
        "status": "success",
        "patient_id": patient_id,
        "results": [
            {"test": "WBC", "value": random.randint(4, 14), "unit": "10^9/L", "flag": random.choice(["N", "H"])},
            {"test": "Hemoglobin", "value": random.randint(10, 16), "unit": "g/dL", "flag": random.choice(["N", "L"])},
            {"test": "CRP", "value": random.randint(1, 120), "unit": "mg/L", "flag": random.choice(["N", "H"])},
            {"test": "Creatinine", "value": random.randint(60, 180), "unit": "umol/L", "flag": random.choice(["N", "H"])},
            {"test": "Troponin", "value": random.randint(1, 500), "unit": "ng/L", "flag": random.choice(["N", "H", "HH"])}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/critical-results")
def critical_results():
    return {
        "status": "success",
        "critical_results": [
            {
                "result_id": f"CRIT-{uuid.uuid4()}",
                "patient_id": f"P-{random.randint(1000,9999)}",
                "test": random.choice(["Troponin", "Potassium", "Glucose", "Creatinine", "Hemoglobin"]),
                "severity": random.choice(["HIGH", "CRITICAL"]),
                "requires_notification": True
            }
            for _ in range(5)
        ]
    }

@router.get("/mapping")
def mapping():
    return {
        "status": "success",
        "lis_mapping": {
            "LabOrder": "AIHA laboratory order workflow",
            "LabResult": "AIHA observation and clinical reasoning engine",
            "CriticalResult": "AIHA alert and escalation engine",
            "CBC": "Complete Blood Count panel",
            "LFT": "Liver Function Tests",
            "RFT": "Renal Function Tests",
            "CRP": "Inflammation marker",
            "Troponin": "Cardiac injury marker"
        }
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "metrics": {
            "lis_connection": random.randint(65, 98),
            "lab_order_flow": random.randint(65, 98),
            "result_ingestion": random.randint(65, 98),
            "critical_result_alerting": random.randint(60, 98),
            "lab_ai_interpretation": random.randint(60, 95),
            "lis_production_readiness": random.randint(60, 95)
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "16.0.4",
            "status": "LIS Laboratory Integration Prototype Active",
            "strategic_value": "Connects AHOS to lab orders, results, critical alerts, lab panels, and clinical reasoning workflows",
            "next_phase": "16.0.5 Pharmacy Production Engine"
        }
    }
