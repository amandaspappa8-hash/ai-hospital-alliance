from fastapi import APIRouter
from backend.app.container.container import container

router = APIRouter(
    prefix="/container",
    tags=["Dependency Injection Container"]
)

@router.get("/health")
async def health():
    return {
        "status": "online",
        "dependency_injection": "active"
    }

@router.get("/services")
async def services():
    return {
        "services": container.list(),
        "total": len(container.list()),
        "status": "CONTAINER_READY"
    }

@router.get("/service/{name}")
async def service(name: str):
    svc = container.get(name)

    if svc is None:
        return {
            "status": "NOT_FOUND"
        }

    return {
        "service": name,
        "status": "FOUND"
    }
