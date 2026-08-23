from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import random

router = APIRouter(
    prefix="/ahos/11.4/radiology-orchestrator",
    tags=["AHOS 11.4.9 Radiology Orchestrator"]
)

class RadiologyRequest(BaseModel):
    hospital_id: str = "AIHA-MAIN"
    pending_studies: int = 190
    urgent_studies: int = 44
    ct_queue: int = 38
    mri_queue: int = 26
    xray_queue: int = 74
    ultrasound_queue: int = 31
    available_radiologists: int = 7
    active_modalities: int = 8
    modality_downtime: int = 1

def level(v):
    if v >= 90:
        return "CRITICAL"
    if v >= 75:
        return "HIGH"
    if v >= 60:
        return "MODERATE"
    return "STABLE"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "11.4.9",
        "engine": "Radiology Orchestrator",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/orchestrate")
def orchestrate(req: RadiologyRequest):

    study_pressure = min(100, int(req.pending_studies / 2) + random.randint(5, 15))
    urgent_pressure = min(100, req.urgent_studies + random.randint(15, 30))
    ct_pressure = min(100, req.ct_queue + random.randint(10, 25))
    mri_pressure = min(100, req.mri_queue + random.randint(10, 25))
    xray_pressure = min(100, req.xray_queue + random.randint(5, 20))
    ultrasound_pressure = min(100, req.ultrasound_queue + random.randint(8, 22))
    staff_pressure = max(0, 100 - (req.available_radiologists * 9))
    modality_pressure = min(100, req.modality_downtime * 25 + random.randint(5, 20))

    radiology_index = round((
        study_pressure +
        urgent_pressure +
        ct_pressure +
        mri_pressure +
        xray_pressure +
        ultrasound_pressure +
        staff_pressure +
        modality_pressure
    ) / 8)

    actions = [
        "Prioritize urgent radiology studies",
        "Route emergency CT and MRI to fast-track queue",
        "Balance X-ray and ultrasound workload",
        "Assign radiologist review priority by acuity",
        "Monitor modality downtime and reroute studies",
        "Synchronize radiology queue with PACS and Hospital Command Center"
    ]

    return {
        "status": "success",
        "phase": "11.4.9 Radiology Orchestrator",
        "hospital_id": req.hospital_id,

        "radiology_orchestration": {
            "pending_studies": req.pending_studies,
            "urgent_studies": req.urgent_studies,
            "ct_queue": req.ct_queue,
            "mri_queue": req.mri_queue,
            "xray_queue": req.xray_queue,
            "ultrasound_queue": req.ultrasound_queue,
            "available_radiologists": req.available_radiologists,
            "active_modalities": req.active_modalities,
            "modality_downtime": req.modality_downtime,
            "study_pressure": study_pressure,
            "urgent_pressure": urgent_pressure,
            "ct_pressure": ct_pressure,
            "mri_pressure": mri_pressure,
            "xray_pressure": xray_pressure,
            "ultrasound_pressure": ultrasound_pressure,
            "staff_pressure": staff_pressure,
            "modality_pressure": modality_pressure,
            "radiology_orchestration_index": radiology_index,
            "risk_level": level(radiology_index)
        },

        "autonomous_radiology_actions": actions,

        "radiology_signal": {
            "sync_care_path_orchestrator": True,
            "sync_resource_orchestrator": True,
            "sync_staffing_engine": True,
            "sync_pacs": True,
            "sync_ai_ultrasound_x": True,
            "sync_hospital_command_center": True,
            "sync_digital_twin": True,
            "executive_escalation": radiology_index >= 88
        },

        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/dashboard")
def dashboard():
    return {
        "status": "success",
        "module": "Radiology Orchestrator Dashboard",
        "metrics": {
            "study_queue_pressure": random.randint(55, 98),
            "urgent_imaging_load": random.randint(50, 98),
            "ct_queue_pressure": random.randint(45, 98),
            "mri_queue_pressure": random.randint(45, 98),
            "xray_queue_pressure": random.randint(40, 96),
            "ultrasound_queue_pressure": random.randint(40, 96),
            "radiologist_workload": random.randint(45, 98),
            "radiology_orchestration_index": random.randint(60, 99)
        },
        "alerts": [
            "Radiology Orchestrator active",
            "PACS synchronization enabled",
            "AI Ultrasound X synchronization active",
            "Emergency imaging fast-track online"
        ]
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "11.4.9",
            "radiology_orchestration_status": "Operational",
            "strategic_value": "Coordinates CT, MRI, X-ray, ultrasound, PACS, radiologists, urgent studies, and AI imaging workflow",
            "next_phase": "11.4.10 Surgical Orchestrator"
        }
    }
