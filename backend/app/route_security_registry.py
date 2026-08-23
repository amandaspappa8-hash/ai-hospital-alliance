"""
AHOS Phase 40.2.4.2
Route Security Registry
"""

PUBLIC_ROUTES = {
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
}

PROTECTED_PREFIXES = {
    "/api",
    "/patients",
    "/radiology",
    "/labs",
    "/pharmacy",
    "/doctors",
    "/appointments",
    "/nursing",
}

ADMIN_PREFIXES = {
    "/admin",
}

def classify(path: str) -> str:
    if path in PUBLIC_ROUTES:
        return "PUBLIC"

    for p in ADMIN_PREFIXES:
        if path.startswith(p):
            return "ADMIN"

    for p in PROTECTED_PREFIXES:
        if path.startswith(p):
            return "PROTECTED"

    return "PUBLIC"
