from fastapi import APIRouter

router = APIRouter(prefix="/clinical-drug", tags=["Clinical Drug Profile"])

@router.get("/{drug_name}")
def clinical_drug_profile(drug_name: str):
    return {
        "drug": drug_name,
        "indications": ["Bacterial infections"],
        "contraindications": ["Severe penicillin allergy"],
        "warnings": ["Risk of allergic reaction"],
        "pregnancy": "Use only if clearly needed",
        "renal_adjustment": {"egfr_below_30": "Dose reduction required"},
        "hepatic_adjustment": {"status": "Monitor liver enzymes"},
        "side_effects": ["Nausea", "Diarrhea", "Rash"],
        "black_box_warning": False,
        "drug_class": "Antibiotic",
        "atc_code": "J01CA04",
        "rxnorm_code": "723",
        "snomed_mapping": "372687004"
    }
