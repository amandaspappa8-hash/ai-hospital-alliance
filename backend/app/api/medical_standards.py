from fastapi import APIRouter

router = APIRouter(prefix="/medical-standards", tags=["Medical Standards"])

@router.get("/")
def get_medical_standards():
    return [
        {
            "name": "WHO ICD-11",
            "type": "Disease Classification",
            "status": "Connected",
            "organization": "World Health Organization",
            "usage": "Diagnosis coding and disease mapping"
        },
        {
            "name": "DSM-5",
            "type": "Mental Health Mapping",
            "status": "Reference Mapping",
            "organization": "American Psychiatric Association",
            "usage": "Psychiatric diagnostic support"
        },
        {
            "name": "SNOMED CT",
            "type": "Clinical Terminology",
            "status": "Planned",
            "organization": "SNOMED International",
            "usage": "Clinical concepts and terminology"
        },
        {
            "name": "RxNorm",
            "type": "Medication Intelligence",
            "status": "Connected",
            "organization": "U.S. National Library of Medicine",
            "usage": "Drug names, interactions, and medication mapping"
        },
        {
            "name": "LOINC",
            "type": "Laboratory Codes",
            "status": "Planned",
            "organization": "Regenstrief Institute",
            "usage": "Lab test codes and results mapping"
        }
    ]
