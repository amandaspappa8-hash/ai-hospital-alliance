from fastapi import APIRouter
from backend.app.service_registry.registry import (
    list_services,
    get_service_by_name,
    get_services_by_category,
    service_summary
)

router = APIRouter(
    prefix="/services",
    tags=["AHOS Service Registry"]
)


@router.get("/health")
async def health():
    return {
        "status": "online",
        "service_registry": "active"
    }


@router.get("/summary")
async def summary():
    return service_summary()


@router.get("/list")
async def services():
    return {
        "services": list_services(),
        "status": "SERVICES_READY"
    }


@router.get("/category/{category}")
async def by_category(category: str):
    return {
        "category": category,
        "services": get_services_by_category(category),
        "status": "CATEGORY_SERVICES_READY"
    }


@router.get("/name/{name}")
async def by_name(name: str):
    service = get_service_by_name(name)

    if not service:
        return {
            "service": None,
            "status": "SERVICE_NOT_FOUND"
        }

    return {
        "service": service,
        "status": "SERVICE_FOUND"
    }
