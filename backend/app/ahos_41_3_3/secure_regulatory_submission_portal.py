from fastapi import APIRouter, UploadFile, File
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/41.3.3",
    tags=["AHOS 41.3.3 Secure Regulatory Submission Portal"]
)

submissions = {}

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.3.3",
        "service": "Secure Regulatory Submission Portal"
    }

@router.post("/submission/create")
async def create_submission(
    authority: str,
    product_name: str
):
    sid = str(uuid.uuid4())

    submissions[sid] = {
        "submission_id": sid,
        "authority": authority,
        "product_name": product_name,
        "status": "DRAFT",
        "created_at": datetime.utcnow().isoformat()
    }

    return submissions[sid]

@router.get("/submission/{sid}")
async def get_submission(sid: str):
    return submissions.get(
        sid,
        {"error": "Submission not found"}
    )

@router.post("/submission/{sid}/upload")
async def upload_file(
    sid: str,
    file: UploadFile = File(...)
):
    if sid not in submissions:
        return {"error": "Submission not found"}

    submissions[sid]["uploaded_file"] = file.filename
    submissions[sid]["status"] = "FILES_UPLOADED"

    return {
        "submission_id": sid,
        "filename": file.filename,
        "status": "FILES_UPLOADED"
    }

@router.post("/submission/{sid}/submit")
async def submit(sid: str):
    if sid not in submissions:
        return {"error": "Submission not found"}

    submissions[sid]["status"] = "SUBMITTED"
    submissions[sid]["submitted_at"] = datetime.utcnow().isoformat()

    return submissions[sid]

@router.get("/dashboard")
async def dashboard():
    return {
        "phase": "AHOS 41.3.3",
        "total_submissions": len(submissions),
        "submissions": list(submissions.values())
    }
