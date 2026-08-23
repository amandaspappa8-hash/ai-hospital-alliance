from fastapi import APIRouter, HTTPException
from datetime import datetime
from uuid import uuid4
import requests
import os

router = APIRouter(
    prefix="/ahos/52.2",
    tags=["AHOS 52.2 Live HAPI FHIR Integration & Real Resource Pull Platform"]
)

FHIR_BASE_URL = os.getenv(
    "FHIR_BASE_URL",
    "https://hapi.fhir.org/baseR4"
)

events = []

def uid(prefix):
    return f"{prefix}-{uuid4().hex[:10].upper()}"

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 52.2",
        "platform": "Live HAPI FHIR Integration & Real Resource Pull Platform",
        "fhir_base_url": FHIR_BASE_URL,
        "readiness": "LIVE_HAPI_FHIR_READY",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/fhir/test")
async def fhir_test():

    try:
        r = requests.get(
            f"{FHIR_BASE_URL}/metadata",
            timeout=20
        )

        return {
            "status": "connected",
            "http_status": r.status_code,
            "fhir_base_url": FHIR_BASE_URL,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/patients")
async def patients():

    r = requests.get(
        f"{FHIR_BASE_URL}/Patient?_count=10",
        timeout=30
    )

    if r.status_code != 200:
        raise HTTPException(
            status_code=r.status_code,
            detail="FHIR Patient Pull Failed"
        )

    bundle = r.json()

    event = {
        "event_id": uid("PAT"),
        "event": "patients_pulled",
        "count": len(bundle.get("entry", [])),
        "created_at": datetime.utcnow().isoformat()
    }

    events.append(event)

    return bundle


@router.get("/observations")
async def observations():

    r = requests.get(
        f"{FHIR_BASE_URL}/Observation?_count=10",
        timeout=30
    )

    if r.status_code != 200:
        raise HTTPException(
            status_code=r.status_code,
            detail="FHIR Observation Pull Failed"
        )

    bundle = r.json()

    event = {
        "event_id": uid("OBS"),
        "event": "observations_pulled",
        "count": len(bundle.get("entry", [])),
        "created_at": datetime.utcnow().isoformat()
    }

    events.append(event)

    return bundle


@router.get("/encounters")
async def encounters():

    r = requests.get(
        f"{FHIR_BASE_URL}/Encounter?_count=10",
        timeout=30
    )

    if r.status_code != 200:
        raise HTTPException(
            status_code=r.status_code,
            detail="FHIR Encounter Pull Failed"
        )

    bundle = r.json()

    event = {
        "event_id": uid("ENC"),
        "event": "encounters_pulled",
        "count": len(bundle.get("entry", [])),
        "created_at": datetime.utcnow().isoformat()
    }

    events.append(event)

    return bundle


@router.get("/dashboard")
async def dashboard():

    return {
        "phase": "AHOS 52.2",
        "readiness": "LIVE_HAPI_FHIR_READY",
        "fhir_base_url": FHIR_BASE_URL,
        "events": len(events),
        "status": "operational"
    }


@router.get("/events")
async def get_events():

    return {
        "count": len(events),
        "events": events[-50:]
    }

