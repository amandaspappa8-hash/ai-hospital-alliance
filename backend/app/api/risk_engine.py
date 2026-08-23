from fastapi import APIRouter

router = APIRouter(prefix="/risk-engine", tags=["AI Risk Engine"])

@router.post("/analyze")
def analyze(payload: dict):
    egfr = payload.get("egfr", 100)
    bp = payload.get("bp", "120/80")

    risks = []

    if egfr < 45:
        risks.append({
            "type": "renal_risk",
            "severity": "moderate",
            "recommendation": "Monitor renal function",
        })

    if str(bp).startswith("150") or "150" in str(bp):
        risks.append({
            "type": "cardiac_risk",
            "severity": "high",
            "recommendation": "Evaluate hypertension urgently",
        })

    return {"risks": risks}
