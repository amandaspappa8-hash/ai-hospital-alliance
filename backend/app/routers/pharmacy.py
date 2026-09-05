from fastapi import Depends
from .deps import get_current_user
from fastapi import Depends
from .deps import get_current_user, rate_limit_middleware
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import urllib.parse
import json
from urllib.request import urlopen, Request

router = APIRouter(tags=["Pharmacy"], dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)])

class MARItemRequest(BaseModel):
    medication: str
    dose: str
    route: str
    schedule: str

class MARUpdateRequest(BaseModel):
    medication: str
    dose: str
    route: str
    schedule: str
    status: Optional[str] = "Pending"
    givenAt: Optional[str] = ""

class MARStatusRequest(BaseModel):
    status: str
    givenAt: Optional[str] = ""

class PharmacistReviewRequest(BaseModel):
    status: str
    note: Optional[str] = ""

@router.get("/mar/{patient_id}")
def get_mar(patient_id: str):
    from ..main import SERVICES
    return SERVICES["mar"].list_items(patient_id)

@router.post("/mar/{patient_id}")
def create_mar_item(patient_id: str, payload: MARItemRequest):
    from ..main import SERVICES
    return SERVICES["mar"].create_item(patient_id, {
        "medication": payload.medication,
        "dose": payload.dose,
        "route": payload.route,
        "schedule": payload.schedule,
        "status": "Pending",
    })

@router.put("/mar/{patient_id}/{item_id}")
def update_mar_item(patient_id: str, item_id: int, payload: MARUpdateRequest):
    from ..main import SERVICES
    payload_data = payload.model_dump()
    updated = SERVICES["mar"].update_item(
        patient_id,
        item_id,
        payload_data,
    )
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="MAR item not found",
        )
    return updated

@router.put("/mar/{patient_id}/{item_id}/pharmacist-review")
def pharmacist_review(patient_id: str, item_id: int, payload: PharmacistReviewRequest):
    from ..main import SERVICES
    payload_data = payload.model_dump()
    updated = SERVICES["mar"].set_pharmacy_review(
        patient_id,
        item_id,
        payload_data,
    )
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="MAR item not found",
        )
    return updated

@router.put("/mar/{patient_id}/{item_id}/status")
def update_mar_status(patient_id: str, item_id: int, payload: MARStatusRequest):
    from ..main import SERVICES
    payload_data = payload.model_dump()
    updated = SERVICES["mar"].set_status(
        patient_id,
        item_id,
        payload_data,
    )
    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="MAR item not found",
        )
    return updated

@router.delete("/mar/{patient_id}/{item_id}")
def delete_mar_item(patient_id: str, item_id: int):
    from ..main import SERVICES
    deleted = SERVICES["mar"].delete_item(
        patient_id,
        item_id,
    )
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="MAR item not found",
        )
    return {
        "deleted": True,
        "id": item_id,
    }

@router.get("/drug-intel/search")
def drug_intel_search(q: str = Query(..., min_length=2)):
    encoded = urllib.parse.quote(q)
    try:
        with urlopen(Request(f"https://rxnav.nlm.nih.gov/REST/drugs.json?name={encoded}",
            headers={"User-Agent": "AI-Hospital-Alliance"}), timeout=12) as r:
            rxnorm = json.loads(r.read().decode())
    except Exception:
        rxnorm = {}
    try:
        with urlopen(Request(f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:%22{encoded}%22&limit=3",
            headers={"User-Agent": "AI-Hospital-Alliance"}), timeout=12) as r:
            openfda = json.loads(r.read().decode())
    except Exception:
        openfda = {}
    return {"query": q, "rxnorm": rxnorm, "openfda": openfda}

@router.get("/drug-intel/dailymed")
def drug_intel_dailymed(name: str = Query(..., min_length=2)):
    encoded = urllib.parse.quote(name)
    try:
        with urlopen(Request(f"https://dailymed.nlm.nih.gov/dailymed/services/v2/spls.json?drug_name={encoded}",
            headers={"User-Agent": "AI-Hospital-Alliance"}), timeout=12) as r:
            return json.loads(r.read().decode())
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"DailyMed fetch failed: {exc}")
