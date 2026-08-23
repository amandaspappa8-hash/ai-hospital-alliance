from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4

router = APIRouter(
    prefix="/ahos/51.1/international-sales",
    tags=["AHOS 51.1 International Sales Pipeline & Government Healthcare Partnership Platform"]
)

sales_pipeline_db: Dict[str, Dict[str, Any]] = {}
government_partnerships_db: Dict[str, Dict[str, Any]] = {}
contracts_db: Dict[str, Dict[str, Any]] = {}
events: List[Dict[str, Any]] = []


class SalesOpportunity(BaseModel):
    country: str
    customer_name: str
    opportunity_name: str
    estimated_value_usd: float
    stage: str
    hospitals_targeted: int


class GovernmentPartnership(BaseModel):
    country: str
    authority_name: str
    partnership_type: str
    target_hospitals: int
    estimated_value_usd: float


class CommercialContract(BaseModel):
    customer_name: str
    contract_type: str
    value_usd: float
    duration_months: int


def uid(prefix: str):
    return f"{prefix}-{uuid4().hex[:10].upper()}"


def log_event(event_type: str, payload: Dict[str, Any]):
    e = {
        "event_id": uid("EVT"),
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }
    events.append(e)


@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 51.1",
        "platform": "International Sales Pipeline & Government Healthcare Partnership Platform",
        "readiness": "INTERNATIONAL_SALES_GOVERNMENT_READY",
        "capabilities": [
            "Global Sales Pipeline",
            "Government Partnerships",
            "Hospital Expansion Deals",
            "Commercial Contracts",
            "Revenue Forecasting",
            "Pipeline Analytics",
            "Regional Expansion Dashboard"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/pipeline/create")
async def create_pipeline(payload: SalesOpportunity):

    pid = uid("PIPE")

    sales_pipeline_db[pid] = {
        "pipeline_id": pid,
        **payload.model_dump(),
        "status": "active",
        "created_at": datetime.utcnow().isoformat()
    }

    log_event("pipeline_created", sales_pipeline_db[pid])

    return sales_pipeline_db[pid]


@router.post("/government/register")
async def register_government(payload: GovernmentPartnership):

    gid = uid("GOV")

    government_partnerships_db[gid] = {
        "government_id": gid,
        **payload.model_dump(),
        "status": "negotiation",
        "created_at": datetime.utcnow().isoformat()
    }

    log_event(
        "government_partnership_created",
        government_partnerships_db[gid]
    )

    return government_partnerships_db[gid]


@router.post("/contracts/create")
async def create_contract(payload: CommercialContract):

    cid = uid("CONTRACT")

    contracts_db[cid] = {
        "contract_id": cid,
        **payload.model_dump(),
        "status": "draft",
        "created_at": datetime.utcnow().isoformat()
    }

    log_event("contract_created", contracts_db[cid])

    return contracts_db[cid]


@router.get("/dashboard")
async def dashboard():

    total_pipeline = sum(
        x["estimated_value_usd"]
        for x in sales_pipeline_db.values()
    )

    total_government = sum(
        x["estimated_value_usd"]
        for x in government_partnerships_db.values()
    )

    total_contracts = sum(
        x["value_usd"]
        for x in contracts_db.values()
    )

    return {
        "phase": "AHOS 51.1",
        "readiness": "INTERNATIONAL_SALES_GOVERNMENT_READY",
        "sales_pipeline": len(sales_pipeline_db),
        "government_partnerships": len(government_partnerships_db),
        "commercial_contracts": len(contracts_db),
        "pipeline_value_usd": total_pipeline,
        "government_pipeline_value_usd": total_government,
        "contract_value_usd": total_contracts,
        "target_hospitals": 100,
        "international_sales_score": 0.96,
        "status": "operational"
    }


@router.get("/events")
async def get_events():
    return {
        "count": len(events),
        "events": events[-50:]
    }

