from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/16.0/fhir-r4",
    tags=["AHOS 16.0.1 Real FHIR R4 Connector"]
)

class FHIRPatientRequest(BaseModel):
    patient_id: str = "P-1001"
    family_name: str = "Demo"
    given_name: str = "Patient"
    gender: str = "unknown"
    birth_date: str = "1970-01-01"

class FHIRObservationRequest(BaseModel):
    patient_id: str = "P-1001"
    code: str = "AIHA_SCORE"
    display: str = "AIHA Clinical Score"
    value: float = 88
    unit: str = "score"

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "16.0.1",
        "engine": "Real FHIR R4 Connector",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/patient")
def create_patient(req: FHIRPatientRequest):
    return {
        "resourceType": "Patient",
        "id": req.patient_id,
        "identifier": [
            {
                "system": "urn:aiha:patient",
                "value": req.patient_id
            }
        ],
        "name": [
            {
                "use": "official",
                "family": req.family_name,
                "given": [req.given_name]
            }
        ],
        "gender": req.gender,
        "birthDate": req.birth_date
    }

@router.post("/observation")
def create_observation(req: FHIRObservationRequest):
    return {
        "resourceType": "Observation",
        "id": str(uuid.uuid4()),
        "status": "final",
        "code": {
            "coding": [
                {
                    "system": "urn:aiha:codes",
                    "code": req.code,
                    "display": req.display
                }
            ],
            "text": req.display
        },
        "subject": {
            "reference": f"Patient/{req.patient_id}"
        },
        "valueQuantity": {
            "value": req.value,
            "unit": req.unit
        },
        "effectiveDateTime": datetime.utcnow().isoformat()
    }

@router.get("/capability-statement")
def capability_statement():
    return {
        "resourceType": "CapabilityStatement",
        "status": "active",
        "date": datetime.utcnow().isoformat(),
        "kind": "instance",
        "fhirVersion": "4.0.1",
        "format": ["json"],
        "rest": [
            {
                "mode": "server",
                "resource": [
                    {"type": "Patient"},
                    {"type": "Encounter"},
                    {"type": "Observation"},
                    {"type": "DiagnosticReport"},
                    {"type": "MedicationRequest"},
                    {"type": "ImagingStudy"}
                ]
            }
        ]
    }

@router.get("/mapping")
def mapping():
    return {
        "status": "success",
        "fhir_r4_mapping": {
            "Patient": "AIHA patient registry",
            "Encounter": "AIHA visit / admission workflow",
            "Observation": "Vitals, labs, clinical scores",
            "DiagnosticReport": "Radiology and laboratory reports",
            "MedicationRequest": "Smart pharmacy prescription engine",
            "ImagingStudy": "PACS / Orthanc / OHIF imaging workflow"
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "16.0.1",
            "status": "FHIR R4 Connector Prototype Active",
            "strategic_value": "Starts real enterprise interoperability foundation for AHOS",
            "next_phase": "16.0.2 HL7 v2 Parser"
        }
    }
