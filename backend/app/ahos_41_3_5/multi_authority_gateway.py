from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/41.3.5",
    tags=["AHOS 41.3.5 Multi-Authority Submission Gateway"]
)

authorities = {
    "FDA": "United States",
    "EMA": "European Union",
    "MHRA": "United Kingdom",
    "SFDA": "Saudi Arabia",
    "HEALTH_CANADA": "Canada",
    "TGA": "Australia",
    "LIBYA_MOH": "Libya"
}

submissions = {}

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.3.5",
        "service": "Multi Authority Submission Gateway"
    }

@router.get("/authorities")
async def get_authorities():
    return authorities

@router.post("/submission")
async def create_submission(
    authority: str,
    product_name: str,
    dossier_id: str
):
    if authority not in authorities:
        return {"error": "Authority not supported"}

    sid = str(uuid.uuid4())

    submissions[sid] = {
        "submission_id": sid,
        "authority": authority,
        "country": authorities[authority],
        "product_name": product_name,
        "dossier_id": dossier_id,
        "status": "SUBMITTED",
        "submitted_at": datetime.utcnow().isoformat()
    }

    return submissions[sid]

@router.get("/submission/{sid}")
async def get_submission(sid: str):
    return submissions.get(
        sid,
        {"error": "Submission not found"}
    )

@router.get("/dashboard")
async def dashboard():
    return {
        "phase": "AHOS 41.3.5",
        "total_submissions": len(submissions),
        "submissions": list(submissions.values())
    }
