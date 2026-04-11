from fastapi import APIRouter
from datetime import datetime, timezone
import os

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": os.getenv("APP_NAME", "AI Hospital Assistant API"),
        "environment": os.getenv("APP_ENV", "development"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@router.get("/ready")
def ready():
    required = ["APP_ENV"]
    missing = [key for key in required if not os.getenv(key)]

    return {
        "ready": len(missing) == 0,
        "missing_env": missing,
        "environment": os.getenv("APP_ENV", "development"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
