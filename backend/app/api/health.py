import os
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    from ..db import health_check
    db_status = health_check()

    required_vars = ["DATABASE_URL", "SECRET_KEY"]
    missing = [v for v in required_vars if not os.environ.get(v)]

    anthropic = bool(os.environ.get("ANTHROPIC_API_KEY","").strip() and
                     os.environ.get("ANTHROPIC_API_KEY") != "your-key-here")

    status = "healthy" if db_status["db"] == "ok" and not missing else "degraded"

    return {
        "status": status,
        "db": db_status,
        "ai": {"anthropic": "ok" if anthropic else "missing"},
        "env": {"missing_vars": missing},
        "version": "2.0.0"
    }
