from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

router = APIRouter(
    prefix="/ahos/49.0.7/strategic-partnerships",
    tags=["AHOS 49.0.7 Strategic Partnership Platform"]
)

partners_db: Dict[str, Dict[str, Any]] = {}
pipelines_db: Dict[str, Dict[str, Any]] = {}
mous_db: Dict[str, Dict[str, Any]] = {}
deals_db: Dict[str, Dict[str, Any]] = {}
partnership_events: List[Dict[str, Any]] = []

class PartnerRegister(BaseModel):
    partner_name: str
    partner_type: str = Field(..., examples=["hospital", "investor", "government", "pharma", "medtech", "university"])
    country: str
    city: Optional[str] = None
    contact_email: Optional[str] = None
    strategic_value: int = Field(..., ge=1, le=100)
    partnership_goal: str

class PipelineCreate(BaseModel):
    partner_id: str
    opportunity_name: str
    stage: str = Field("discovery", examples=["discovery", "evaluation", "negotiation", "mou", "signed"])
    estimated_value_usd: float = 0
    priority: str = Field("medium", examples=["low", "medium", "high", "strategic"])

class MoUCreate(BaseModel):
    partner_id: str
    title: str
    scope: str
    duration_months: int = 12
    status: str = Field("draft", examples=["draft", "under_review", "signed", "expired"])

class CommercialDeal(BaseModel):
    partner_id: str
    deal_name: str
    deal_type: str = Field(..., examples=["pilot", "saas", "licensing", "joint_venture", "investment"])
    value_usd: float
    probability_percent: int = Field(..., ge=0, le=100)

def log_event(event_type: str, payload: Dict[str, Any]):
    event = {
        "event_id": "PARTNER-EVT-" + uuid4().hex[:10].upper(),
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }
    partnership_events.append(event)
    return event

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 49.0.7",
        "platform": "Strategic Partnership Platform",
        "readiness": "STRATEGIC_PARTNERSHIP_READY",
        "capabilities": [
            "Partner Registry",
            "Hospital Partnership Pipeline",
            "Investor Partnership Dossier",
            "Pharma / MedTech Partnerships",
            "Government Health Authority Partnerships",
            "MoU Tracking",
            "Commercial Deal Readiness"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/partners/register")
async def register_partner(payload: PartnerRegister):
    partner_id = "PARTNER-" + uuid4().hex[:10].upper()

    readiness = "standard"
    if payload.strategic_value >= 85:
        readiness = "strategic_priority"
    elif payload.strategic_value >= 70:
        readiness = "high_value"

    partners_db[partner_id] = {
        "partner_id": partner_id,
        "partner_name": payload.partner_name,
        "partner_type": payload.partner_type,
        "country": payload.country,
        "city": payload.city,
        "contact_email": payload.contact_email,
        "strategic_value": payload.strategic_value,
        "partnership_goal": payload.partnership_goal,
        "readiness": readiness,
        "registered_at": datetime.utcnow().isoformat()
    }

    log_event("partner_registered", partners_db[partner_id])
    return partners_db[partner_id]

@router.post("/pipeline/create")
async def create_pipeline(payload: PipelineCreate):
    if payload.partner_id not in partners_db:
        raise HTTPException(status_code=404, detail="Partner not found")

    pipeline_id = "PIPE-" + uuid4().hex[:10].upper()

    pipelines_db[pipeline_id] = {
        "pipeline_id": pipeline_id,
        "partner_id": payload.partner_id,
        "opportunity_name": payload.opportunity_name,
        "stage": payload.stage,
        "estimated_value_usd": payload.estimated_value_usd,
        "priority": payload.priority,
        "created_at": datetime.utcnow().isoformat()
    }

    log_event("pipeline_created", pipelines_db[pipeline_id])
    return pipelines_db[pipeline_id]

@router.post("/mou/create")
async def create_mou(payload: MoUCreate):
    if payload.partner_id not in partners_db:
        raise HTTPException(status_code=404, detail="Partner not found")

    mou_id = "MOU-" + uuid4().hex[:10].upper()

    mous_db[mou_id] = {
        "mou_id": mou_id,
        "partner_id": payload.partner_id,
        "title": payload.title,
        "scope": payload.scope,
        "duration_months": payload.duration_months,
        "status": payload.status,
        "created_at": datetime.utcnow().isoformat()
    }

    log_event("mou_created", mous_db[mou_id])
    return mous_db[mou_id]

@router.post("/deals/create")
async def create_deal(payload: CommercialDeal):
    if payload.partner_id not in partners_db:
        raise HTTPException(status_code=404, detail="Partner not found")

    deal_id = "DEAL-" + uuid4().hex[:10].upper()
    weighted_value = payload.value_usd * (payload.probability_percent / 100)

    deal_status = "early"
    if payload.probability_percent >= 80:
        deal_status = "high_probability"
    elif payload.probability_percent >= 50:
        deal_status = "qualified"

    deals_db[deal_id] = {
        "deal_id": deal_id,
        "partner_id": payload.partner_id,
        "deal_name": payload.deal_name,
        "deal_type": payload.deal_type,
        "value_usd": payload.value_usd,
        "probability_percent": payload.probability_percent,
        "weighted_value_usd": round(weighted_value, 2),
        "deal_status": deal_status,
        "created_at": datetime.utcnow().isoformat()
    }

    log_event("commercial_deal_created", deals_db[deal_id])
    return deals_db[deal_id]

@router.get("/dashboard")
async def dashboard():
    total_pipeline_value = sum(p["estimated_value_usd"] for p in pipelines_db.values())
    total_deal_value = sum(d["value_usd"] for d in deals_db.values())
    weighted_deal_value = sum(d["weighted_value_usd"] for d in deals_db.values())

    strategic_partners = len([
        p for p in partners_db.values()
        if p["readiness"] == "strategic_priority"
    ])

    signed_mous = len([
        m for m in mous_db.values()
        if m["status"] == "signed"
    ])

    high_probability_deals = len([
        d for d in deals_db.values()
        if d["deal_status"] == "high_probability"
    ])

    readiness_score = 0.90
    if strategic_partners > 0:
        readiness_score += 0.03
    if signed_mous > 0:
        readiness_score += 0.03
    if high_probability_deals > 0:
        readiness_score += 0.04

    return {
        "phase": "AHOS 49.0.7",
        "readiness": "STRATEGIC_PARTNERSHIP_READY",
        "status": "operational",
        "partners": len(partners_db),
        "strategic_partners": strategic_partners,
        "pipeline_opportunities": len(pipelines_db),
        "mous": len(mous_db),
        "signed_mous": signed_mous,
        "commercial_deals": len(deals_db),
        "high_probability_deals": high_probability_deals,
        "total_pipeline_value_usd": total_pipeline_value,
        "total_deal_value_usd": total_deal_value,
        "weighted_deal_value_usd": round(weighted_deal_value, 2),
        "partnership_readiness_score": round(min(readiness_score, 0.99), 3)
    }

@router.get("/investor/dossier")
async def investor_dossier():
    return {
        "project": "AI Hospital Alliance (AHOS)",
        "phase": "AHOS 49.0.7",
        "target_valuation_usd": 5000000000,
        "platform_status": "Autonomous Global Healthcare Ecosystem",
        "commercial_readiness": True,
        "regulatory_readiness": True,
        "rwe_readiness": True,
        "monitoring_readiness": True,
        "partnership_readiness": True,
        "partners_registered": len(partners_db),
        "pipeline_value_usd": sum(p["estimated_value_usd"] for p in pipelines_db.values()),
        "deal_value_usd": sum(d["value_usd"] for d in deals_db.values()),
        "recommended_next_step": "Prepare signed MoUs, pilot contracts, financial model and investor deck"
    }

@router.get("/events")
async def events():
    return {
        "count": len(partnership_events),
        "events": partnership_events[-50:]
    }
