from fastapi import APIRouter, Depends, Query
from .deps import get_current_user, rate_limit_middleware

router = APIRouter(
    prefix="/icd",
    tags=["ICD-11 / DSM-5"],
    dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)]
)

ICD11_DB = {
    "CA40": {"code": "CA40", "title": "Pneumonia", "category": "Respiratory", "chapter": "CA", "severity": "Moderate-Severe"},
    "CA40.0": {"code": "CA40.0", "title": "Pneumonia due to Streptococcus pneumoniae", "category": "Respiratory", "chapter": "CA", "severity": "Moderate-Severe"},
    "CA40.1": {"code": "CA40.1", "title": "Pneumonia due to Haemophilus influenzae", "category": "Respiratory", "chapter": "CA", "severity": "Moderate"},
    "CA22": {"code": "CA22", "title": "COVID-19", "category": "Infectious", "chapter": "CA", "severity": "Variable"},
    "CA22.0": {"code": "CA22.0", "title": "COVID-19, virus identified", "category": "Infectious", "chapter": "CA", "severity": "Variable"},
    "5A10": {"code": "5A10", "title": "Type 1 diabetes mellitus", "category": "Endocrine", "chapter": "5A", "severity": "Chronic"},
    "5A11": {"code": "5A11", "title": "Type 2 diabetes mellitus", "category": "Endocrine", "chapter": "5A", "severity": "Chronic"},
    "BA80": {"code": "BA80", "title": "Essential hypertension", "category": "Cardiovascular", "chapter": "BA", "severity": "Chronic"},
    "BA41": {"code": "BA41", "title": "Acute myocardial infarction", "category": "Cardiovascular", "chapter": "BA", "severity": "Critical"},
    "BA80.0": {"code": "BA80.0", "title": "Hypertensive heart disease", "category": "Cardiovascular", "chapter": "BA", "severity": "Moderate"},
    "8B11": {"code": "8B11", "title": "Ischaemic stroke", "category": "Neurological", "chapter": "8B", "severity": "Critical"},
    "8A00": {"code": "8A00", "title": "Epilepsy", "category": "Neurological", "chapter": "8A", "severity": "Moderate"},
    "GB04": {"code": "GB04", "title": "Acute kidney injury", "category": "Renal", "chapter": "GB", "severity": "Severe"},
    "GB60": {"code": "GB60", "title": "Chronic kidney disease", "category": "Renal", "chapter": "GB", "severity": "Chronic"},
    "DB92": {"code": "DB92", "title": "Sepsis", "category": "Systemic", "chapter": "DB", "severity": "Critical"},
    "DB94": {"code": "DB94", "title": "Septic shock", "category": "Systemic", "chapter": "DB", "severity": "Critical"},
    "CA21": {"code": "CA21", "title": "Acute bronchitis", "category": "Respiratory", "chapter": "CA", "severity": "Mild"},
    "CA23": {"code": "CA23", "title": "Bronchial asthma", "category": "Respiratory", "chapter": "CA", "severity": "Variable"},
    "CB24": {"code": "CB24", "title": "Chronic obstructive pulmonary disease", "category": "Respiratory", "chapter": "CB", "severity": "Chronic"},
    "DA91": {"code": "DA91", "title": "Acute appendicitis", "category": "Gastrointestinal", "chapter": "DA", "severity": "Moderate-Severe"},
    "DA40": {"code": "DA40", "title": "Gastroesophageal reflux disease", "category": "Gastrointestinal", "chapter": "DA", "severity": "Mild"},
    "DC10": {"code": "DC10", "title": "Liver cirrhosis", "category": "Hepatic", "chapter": "DC", "severity": "Severe"},
    "XH1": {"code": "XH1", "title": "Anaemia", "category": "Haematological", "chapter": "XH", "severity": "Variable"},
    "3A00": {"code": "3A00", "title": "Iron deficiency anaemia", "category": "Haematological", "chapter": "3A", "severity": "Mild-Moderate"},
    "2B30": {"code": "2B30", "title": "Lung cancer", "category": "Oncological", "chapter": "2B", "severity": "Critical"},
    "2C91": {"code": "2C91", "title": "Colorectal cancer", "category": "Oncological", "chapter": "2C", "severity": "Critical"},
}

DSM5_DB = {
    "296.23": {"code": "296.23", "title": "Major Depressive Disorder, Single Episode, Severe", "category": "Mood", "icd_equivalent": "6A70"},
    "296.89": {"code": "296.89", "title": "Bipolar II Disorder", "category": "Mood", "icd_equivalent": "6A61"},
    "295.90": {"code": "295.90", "title": "Schizophrenia", "category": "Psychotic", "icd_equivalent": "6A20"},
    "300.02": {"code": "300.02", "title": "Generalized Anxiety Disorder", "category": "Anxiety", "icd_equivalent": "6B00"},
    "309.81": {"code": "309.81", "title": "Post-Traumatic Stress Disorder", "category": "Trauma", "icd_equivalent": "6B40"},
    "303.90": {"code": "303.90", "title": "Alcohol Use Disorder, Severe", "category": "Substance", "icd_equivalent": "6C40"},
    "314.01": {"code": "314.01", "title": "ADHD, Combined Presentation", "category": "Neurodevelopmental", "icd_equivalent": "6A05"},
    "299.00": {"code": "299.00", "title": "Autism Spectrum Disorder", "category": "Neurodevelopmental", "icd_equivalent": "6A02"},
    "307.1": {"code": "307.1", "title": "Anorexia Nervosa", "category": "Eating", "icd_equivalent": "6B80"},
    "300.3": {"code": "300.3", "title": "Obsessive-Compulsive Disorder", "category": "OCD", "icd_equivalent": "6B20"},
}

@router.get("/search")
def search_icd(
    q: str = Query(..., min_length=2),
    db: str = Query("icd11", regex="^(icd11|dsm5|all)$")
):
    q_lower = q.lower()
    results = []
    if db in ("icd11", "all"):
        for code, data in ICD11_DB.items():
            if q_lower in data["title"].lower() or q_lower in code.lower() or q_lower in data["category"].lower():
                results.append({**data, "system": "ICD-11"})
    if db in ("dsm5", "all"):
        for code, data in DSM5_DB.items():
            if q_lower in data["title"].lower() or q_lower in code.lower():
                results.append({**data, "system": "DSM-5"})
    return {"query": q, "total": len(results), "results": results}

@router.get("/code/{code}")
def get_icd_code(code: str):
    code_upper = code.upper()
    if code_upper in ICD11_DB:
        return {**ICD11_DB[code_upper], "system": "ICD-11"}
    if code in DSM5_DB:
        return {**DSM5_DB[code], "system": "DSM-5"}
    return {"error": f"Code {code} not found"}

@router.get("/categories")
def get_categories():
    icd_cats = list(set(d["category"] for d in ICD11_DB.values()))
    dsm_cats = list(set(d["category"] for d in DSM5_DB.values()))
    return {
        "icd11_categories": sorted(icd_cats),
        "dsm5_categories": sorted(dsm_cats),
        "total_icd11_codes": len(ICD11_DB),
        "total_dsm5_codes": len(DSM5_DB)
    }

@router.post("/match-diagnosis")
def match_diagnosis(payload: dict):
    diagnosis_text = payload.get("diagnosis", "").lower()
    matches = []
    for code, data in ICD11_DB.items():
        title_lower = data["title"].lower()
        if any(word in title_lower for word in diagnosis_text.split() if len(word) > 3):
            matches.append({**data, "system": "ICD-11", "confidence": "High" if diagnosis_text in title_lower else "Medium"})
    return {"diagnosis": payload.get("diagnosis"), "icd_matches": matches[:5]}
