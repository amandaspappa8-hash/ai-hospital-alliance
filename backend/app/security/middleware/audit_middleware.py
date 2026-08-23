import json
import time
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware

AUDIT_LOG = Path("reports/security_audit.jsonl")

class AuditMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        start=time.time()

        response=await call_next(request)

        duration=round((time.time()-start)*1000,2)

        event={
            "path":request.url.path,
            "method":request.method,
            "status":response.status_code,
            "duration_ms":duration,
            "client":request.client.host if request.client else None
        }

        AUDIT_LOG.parent.mkdir(parents=True,exist_ok=True)

        with AUDIT_LOG.open("a") as f:
            f.write(json.dumps(event)+"\n")

        return response
