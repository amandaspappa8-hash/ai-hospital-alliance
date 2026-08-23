"""
AHOS Phase 40.2.4.10
Approved Enforcement Baseline
"""

def classify_approved(path:str)->str:

    p = path.rstrip("/") or "/"

    PUBLIC = {
        "/",
        "/health",
        "/ready",
        "/system-health",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/docs/oauth2-redirect",
    }

    if p in PUBLIC:
        return "PUBLIC"

    if "/admin" in p:
        return "ADMIN"

    return "PROTECTED"
