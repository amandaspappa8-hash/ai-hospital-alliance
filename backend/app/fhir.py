"""
HL7 FHIR R4 API
International healthcare data exchange standard
"""

from datetime import datetime


def patient_to_fhir(patient) -> dict:
    """Convert internal Patient model to FHIR R4 Patient resource"""
    return {
        "resourceType": "Patient",
        "id": patient.id,
        "meta": {
            "versionId": "1",
            "lastUpdated": datetime.utcnow().isoformat() + "Z",
            "profile": ["http://hl7.org/fhir/StructureDefinition/Patient"],
        },
        "identifier": [
            {"system": "http://aiha.hospital/patients", "value": patient.id}
        ],
        "active": patient.status != "Discharged",
        "name": [
            {
                "use": "official",
                "text": patient.name,
                "family": patient.name.split()[-1],
                "given": [patient.name.split()[0]],
            }
        ],
        "gender": patient.gender.lower(),
        "telecom": [{"system": "phone", "value": patient.phone, "use": "mobile"}],
        "extension": [
            {
                "url": "http://aiha.hospital/fhir/condition",
                "valueString": patient.condition,
            },
            {
                "url": "http://aiha.hospital/fhir/department",
                "valueString": str(patient.department_id),
            },
        ],
    }


def observation_to_fhir(vital, patient_id: str) -> dict:
    """Convert vitals to FHIR Observation"""
    return {
        "resourceType": "Observation",
        "id": f"obs-{patient_id}-{datetime.utcnow().timestamp():.0f}",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "85353-1",
                    "display": "Vital signs panel",
                }
            ]
        },
        "subject": {"reference": f"Patient/{patient_id}"},
        "effectiveDateTime": datetime.utcnow().isoformat() + "Z",
        "component": [
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8867-4",
                            "display": "Heart rate",
                        }
                    ]
                },
                "valueQuantity": {
                    "value": float(vital.heart_rate),
                    "unit": "beats/min",
                    "system": "http://unitsofmeasure.org",
                    "code": "/min",
                },
            },
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "2708-6",
                            "display": "Oxygen saturation",
                        }
                    ]
                },
                "valueQuantity": {
                    "value": float(vital.oxygen_saturation),
                    "unit": "%",
                    "system": "http://unitsofmeasure.org",
                    "code": "%",
                },
            },
            {
                "code": {
                    "coding": [
                        {
                            "system": "http://loinc.org",
                            "code": "8310-5",
                            "display": "Body temperature",
                        }
                    ]
                },
                "valueQuantity": {
                    "value": float(vital.temperature),
                    "unit": "Cel",
                    "system": "http://unitsofmeasure.org",
                    "code": "Cel",
                },
            },
        ],
    }


def condition_to_fhir(patient) -> dict:
    """Convert patient condition to FHIR Condition"""
    return {
        "resourceType": "Condition",
        "id": f"cond-{patient.id}",
        "clinicalStatus": {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                    "code": "active",
                }
            ]
        },
        "subject": {"reference": f"Patient/{patient.id}"},
        "code": {"text": patient.condition},
        "recordedDate": datetime.utcnow().isoformat() + "Z",
    }


def bundle_response(resources: list, bundle_type: str = "searchset") -> dict:
    """Create FHIR Bundle"""
    return {
        "resourceType": "Bundle",
        "id": f"bundle-{datetime.utcnow().timestamp():.0f}",
        "type": bundle_type,
        "total": len(resources),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "entry": [
            {
                "resource": r,
                "fullUrl": f"http://aiha.hospital/fhir/{r['resourceType']}/{r['id']}",
            }
            for r in resources
        ],
    }
