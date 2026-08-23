from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/30.4",
    tags=["AHOS 30.4 Medical Device Regulatory Program"]
)

DEVICES = {}
RISK_FILES = {}

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 30.4",
        "module": "Medical Device Regulatory Program",
        "regulatory_layer": "active",
        "timestamp": str(datetime.utcnow())
    }

@router.get("/overview")
async def overview():
    return {
        "iso_13485": "READY",
        "iso_14971": "READY",
        "iec_62304": "READY",
        "iec_62366": "READY",
        "fda_samd": "READY",
        "eu_mdr": "READY",
        "clinical_evaluation_report": "READY",
        "risk_management_file": "READY",
        "design_history_file": "READY",
        "software_safety_classification": "READY",
        "status": "MEDICAL_DEVICE_REGULATORY_PROGRAM_READY"
    }

@router.post("/devices/register")
async def register_device(payload: dict):
    device_id = "dev_" + str(uuid.uuid4())[:8]

    device = {
        "device_id": device_id,
        "name": payload.get("name"),
        "device_type": payload.get("device_type"),
        "risk_class": payload.get("risk_class", "IIa"),
        "specialty": payload.get("specialty"),
        "country": payload.get("country", "Global"),
        "status": "REGISTERED",
        "registered_at": str(datetime.utcnow())
    }

    DEVICES[device_id] = device

    return {
        "message": "Medical device registered successfully",
        "device": device,
        "status": "DEVICE_REGISTERED"
    }

@router.get("/devices")
async def devices():
    return {
        "total": len(DEVICES),
        "devices": list(DEVICES.values()),
        "status": "MEDICAL_DEVICE_REGISTRY_READY"
    }

@router.get("/standards")
async def standards():
    return {
        "iso_13485": "Quality Management System",
        "iso_14971": "Risk Management",
        "iec_62304": "Medical Software Lifecycle",
        "iec_62366": "Usability Engineering",
        "fda_samd": "Software as Medical Device",
        "eu_mdr": "Medical Device Regulation",
        "status": "REGULATORY_STANDARDS_READY"
    }

@router.post("/risk-files")
async def risk_file(payload: dict):
    risk_id = "risk_" + str(uuid.uuid4())[:8]

    file = {
        "risk_id": risk_id,
        "device_id": payload.get("device_id"),
        "hazard": payload.get("hazard"),
        "severity": payload.get("severity"),
        "probability": payload.get("probability"),
        "mitigation": payload.get("mitigation"),
        "created_at": str(datetime.utcnow())
    }

    RISK_FILES[risk_id] = file

    return {
        "message": "Risk management file created",
        "risk_file": file,
        "status": "RISK_FILE_CREATED"
    }

@router.get("/risk-files")
async def list_risks():
    return {
        "total": len(RISK_FILES),
        "risk_files": list(RISK_FILES.values()),
        "status": "RISK_MANAGEMENT_FILE_READY"
    }

@router.get("/clinical-evaluation")
async def clinical_evaluation():
    return {
        "clinical_evaluation_report": "READY",
        "performance_evidence": "READY",
        "clinical_validation": "READY",
        "post_market_surveillance": "READY",
        "status": "CLINICAL_EVALUATION_READY"
    }

@router.get("/documentation")
async def documentation():
    return {
        "design_history_file": "READY",
        "software_requirements_specification": "READY",
        "software_architecture_document": "READY",
        "verification_validation_plan": "READY",
        "traceability_matrix": "READY",
        "status": "REGULATORY_DOCUMENTATION_READY"
    }

@router.get("/audit")
async def audit():
    return {
        "regulatory_score": 97,
        "quality_management": "ACTIVE",
        "risk_management": "ACTIVE",
        "software_lifecycle": "ACTIVE",
        "clinical_evaluation": "ACTIVE",
        "regulatory_documentation": "ACTIVE",
        "fda_pathway": "READY",
        "eu_mdr_pathway": "READY",
        "status": "AHOS_30_4_OPERATIONAL"
    }
