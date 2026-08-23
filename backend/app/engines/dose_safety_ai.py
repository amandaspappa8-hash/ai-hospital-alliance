from fastapi import APIRouter

router = APIRouter(prefix="/dose-safety", tags=["Dose Safety AI"])

@router.post("/analyze")
def analyze(payload: dict):
    egfr = payload.get("egfr", 100)

    result = {
        "egfr": egfr,
        "status": "safe",
        "recommendation": "Standard dosing"
    }

    if egfr < 60:
        result["status"] = "caution"
        result["recommendation"] = "Monitor renal function"

    if egfr < 30:
        result["status"] = "high-risk"
        result["recommendation"] = "Dose reduction required"

    return result
