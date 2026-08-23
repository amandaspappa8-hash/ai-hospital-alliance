from fastapi import APIRouter

router = APIRouter(tags=["Hospital Digital Twin"])

@router.get("/digital-twin-health")
async def digital_twin_health():
    return {
        "status": "online",
        "engine": "Hospital Digital Twin",
        "version": "9.8"
    }

@router.get("/hospital-digital-twin")
async def hospital_digital_twin():
    return {
        "status": "active",
        "patients": 0,
        "beds": 0,
        "icu": 0,
        "resources": 0
    }
