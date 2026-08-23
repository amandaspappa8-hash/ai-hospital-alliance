from fastapi import APIRouter

router = APIRouter(prefix="/enterprise-dashboard", tags=["Enterprise Dashboard"])

@router.get("/metrics")
def metrics():
    return {
        "admissions": [12, 18, 15, 21, 25, 19, 28],
        "icu_load": 78,
        "medication_risks": {"high": 4, "moderate": 11, "low": 24},
        "ai_clinical_scores": [62, 70, 76, 81, 88],
        "labs_trend": [
            {"day": "Mon", "creatinine": 1.1, "egfr": 58},
            {"day": "Tue", "creatinine": 1.3, "egfr": 49},
            {"day": "Wed", "creatinine": 1.4, "egfr": 42},
        ],
    }
