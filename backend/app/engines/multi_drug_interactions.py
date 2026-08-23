from fastapi import APIRouter

router = APIRouter(prefix="/multi-drug", tags=["Multi Drug Interactions"])

@router.post("/check")
def check_interactions(payload: dict):
    drugs = payload.get("drugs", [])
    return {
        "drugs": drugs,
        "interactions": [
            {
                "severity": "high",
                "risk": "Bleeding risk",
                "drugs": ["Warfarin", "Aspirin"],
                "recommendation": "Doctor and pharmacist review required"
            },
            {
                "severity": "moderate",
                "risk": "Renal toxicity",
                "drugs": ["Ibuprofen"],
                "recommendation": "Monitor kidney function"
            }
        ]
    }
