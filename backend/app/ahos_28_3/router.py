from fastapi import APIRouter

router = APIRouter(
    prefix="/ahos/28.3",
    tags=["AHOS 28.3 FHIR R4"]
)

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 28.3",
        "module": "FHIR R4 Clinical Interoperability Layer",
        "fhir_status": "active"
    }

@router.get("/patients")
async def patients():
    return {
        "resource": "Patient",
        "fhir_version": "R4",
        "status": "ready"
    }

@router.get("/encounters")
async def encounters():
    return {
        "resource": "Encounter",
        "status": "ready"
    }

@router.get("/observations")
async def observations():
    return {
        "resource": "Observation",
        "status": "ready"
    }

@router.get("/medications")
async def medications():
    return {
        "resource": "MedicationRequest",
        "status": "ready"
    }

@router.get("/imaging")
async def imaging():
    return {
        "resource": "ImagingStudy",
        "orthanc": "connected",
        "status": "ready"
    }
