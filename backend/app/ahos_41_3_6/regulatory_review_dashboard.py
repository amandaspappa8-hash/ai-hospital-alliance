from fastapi import APIRouter
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/41.3.6",
    tags=["AHOS 41.3.6 Regulatory Review Workflow Dashboard"]
)

reviews = {}

VALID_STATUS = [
    "SUBMITTED",
    "UNDER_REVIEW",
    "DEFICIENCY_REQUESTED",
    "RESUBMITTED",
    "APPROVED",
    "REJECTED"
]

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.3.6",
        "service": "Regulatory Review Workflow Dashboard"
    }

@router.post("/review/create")
async def create_review(
    authority: str,
    submission_id: str,
    product_name: str
):
    rid = str(uuid.uuid4())

    reviews[rid] = {
        "review_id": rid,
        "authority": authority,
        "submission_id": submission_id,
        "product_name": product_name,
        "status": "SUBMITTED",
        "reviewer": None,
        "comments": [],
        "created_at": datetime.utcnow().isoformat()
    }

    return reviews[rid]

@router.post("/review/{rid}/assign")
async def assign_reviewer(
    rid: str,
    reviewer_name: str
):
    if rid not in reviews:
        return {"error": "Review not found"}

    reviews[rid]["reviewer"] = reviewer_name
    reviews[rid]["status"] = "UNDER_REVIEW"

    return reviews[rid]

@router.post("/review/{rid}/comment")
async def add_comment(
    rid: str,
    comment: str
):
    if rid not in reviews:
        return {"error": "Review not found"}

    reviews[rid]["comments"].append({
        "comment": comment,
        "timestamp": datetime.utcnow().isoformat()
    })

    return reviews[rid]

@router.post("/review/{rid}/status")
async def update_status(
    rid: str,
    status: str
):
    if rid not in reviews:
        return {"error": "Review not found"}

    if status not in VALID_STATUS:
        return {"error": "Invalid status"}

    reviews[rid]["status"] = status
    reviews[rid]["updated_at"] = datetime.utcnow().isoformat()

    return reviews[rid]

@router.get("/review/{rid}")
async def get_review(rid: str):
    return reviews.get(
        rid,
        {"error": "Review not found"}
    )

@router.get("/dashboard")
async def dashboard():
    return {
        "phase": "AHOS 41.3.6",
        "total_reviews": len(reviews),
        "reviews": list(reviews.values())
    }

@router.get("/kpis")
async def kpis():
    summary = {
        s: 0 for s in VALID_STATUS
    }

    for r in reviews.values():
        summary[r["status"]] += 1

    return {
        "phase": "AHOS 41.3.6",
        "kpis": summary
    }
