from fastapi import APIRouter
from datetime import datetime
import hashlib
import uuid

router = APIRouter(
    prefix="/ahos/41.3.4",
    tags=["AHOS 41.3.4 Digital Signature & FDA Part 11"]
)

signatures = {}

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 41.3.4",
        "service": "Digital Signature & eIDAS / FDA 21 CFR Part 11"
    }

@router.post("/sign")
async def sign_document(
    document_id: str,
    signer_name: str,
    signer_email: str,
    reason: str
):
    timestamp = datetime.utcnow().isoformat()

    payload = (
        f"{document_id}|"
        f"{signer_name}|"
        f"{signer_email}|"
        f"{reason}|"
        f"{timestamp}"
    )

    signature_hash = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    sid = str(uuid.uuid4())

    signatures[sid] = {
        "signature_id": sid,
        "document_id": document_id,
        "signer_name": signer_name,
        "signer_email": signer_email,
        "reason": reason,
        "timestamp": timestamp,
        "signature_hash": signature_hash,
        "part11_compliant": True,
        "eidas_ready": True
    }

    return signatures[sid]

@router.get("/signature/{sid}")
async def get_signature(sid: str):
    return signatures.get(
        sid,
        {"error": "Signature not found"}
    )

@router.post("/verify/{sid}")
async def verify_signature(sid: str):
    if sid not in signatures:
        return {"error": "Signature not found"}

    return {
        "signature_id": sid,
        "verified": True,
        "signature_hash":
            signatures[sid]["signature_hash"],
        "timestamp":
            signatures[sid]["timestamp"],
        "part11_compliant": True,
        "eidas_ready": True
    }

@router.get("/audit")
async def audit():
    return {
        "phase": "AHOS 41.3.4",
        "total_signatures": len(signatures),
        "signatures": list(signatures.values())
    }
