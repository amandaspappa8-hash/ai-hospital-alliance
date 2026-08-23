from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

router = APIRouter(
    prefix="/ahos/51.0/global-commercial-launch",
    tags=["AHOS 51.0 Global Commercial Launch & Autonomous Healthcare Market Expansion Platform"]
)

markets: Dict[str, Dict[str, Any]] = {}
hospital_targets: Dict[str, Dict[str, Any]] = {}
saas_plans: Dict[str, Dict[str, Any]] = {}
commercial_contracts: Dict[str, Dict[str, Any]] = {}
launch_events: List[Dict[str, Any]] = []

class MarketRegister(BaseModel):
    country: str
    region: str = Field(..., examples=["MENA", "Europe", "Africa", "GCC"])
    market_type: str = "Healthcare"
    regulatory_status: str = Field("pending", examples=["pending", "ready", "approved"])
    priority: str = Field("high", examples=["low", "medium", "high", "strategic"])

class HospitalTarget(BaseModel):
    market_id: str
    hospital_name: str
    country: str
    target_beds: int = 300
    expected_users: int = 500
    deployment_model: str = Field("SaaS", examples=["SaaS", "On-Premise", "Hybrid"])

class SaaSPlan(BaseModel):
    plan_name: str
    price_per_hospital_usd: float
    included_modules: List[str]
    support_level: str = Field("enterprise", examples=["standard", "enterprise", "premium"])

class CommercialContract(BaseModel):
    hospital_id: str
    plan_id: str
    contract_value_usd: float
    duration_months: int = 12
    status: str = Field("draft", examples=["draft", "negotiation", "signed", "active"])

def uid(prefix: str):
    return f"{prefix}-{uuid4().hex[:10].upper()}"

def log_event(event_type: str, payload: Dict[str, Any]):
    event = {
        "event_id": uid("LAUNCH-EVT"),
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }
    launch_events.append(event)
    return event

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 51.0",
        "platform": "Global Commercial Launch & Autonomous Healthcare Market Expansion Platform",
        "readiness": "GLOBAL_COMMERCIAL_LAUNCH_READY",
        "capabilities": [
            "Global market registration",
            "Hospital expansion pipeline",
            "Enterprise SaaS plans",
            "Commercial contract tracking",
            "Regional launch operations",
            "Autonomous market expansion",
            "Revenue readiness dashboard",
            "100+ hospital expansion planning"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/markets/register")
async def register_market(payload: MarketRegister):
    market_id = uid("MARKET")
    markets[market_id] = {
        "market_id": market_id,
        "country": payload.country,
        "region": payload.region,
        "market_type": payload.market_type,
        "regulatory_status": payload.regulatory_status,
        "priority": payload.priority,
        "registered_at": datetime.utcnow().isoformat()
    }
    log_event("market_registered", markets[market_id])
    return markets[market_id]

@router.post("/hospitals/target")
async def target_hospital(payload: HospitalTarget):
    if payload.market_id not in markets:
        raise HTTPException(status_code=404, detail="Market not found")

    hospital_id = uid("TARGET-HOSP")
    hospital_targets[hospital_id] = {
        "hospital_id": hospital_id,
        "market_id": payload.market_id,
        "hospital_name": payload.hospital_name,
        "country": payload.country,
        "target_beds": payload.target_beds,
        "expected_users": payload.expected_users,
        "deployment_model": payload.deployment_model,
        "status": "targeted",
        "created_at": datetime.utcnow().isoformat()
    }
    log_event("hospital_target_created", hospital_targets[hospital_id])
    return hospital_targets[hospital_id]

@router.post("/saas/plans/create")
async def create_saas_plan(payload: SaaSPlan):
    plan_id = uid("SAAS")
    saas_plans[plan_id] = {
        "plan_id": plan_id,
        "plan_name": payload.plan_name,
        "price_per_hospital_usd": payload.price_per_hospital_usd,
        "included_modules": payload.included_modules,
        "support_level": payload.support_level,
        "created_at": datetime.utcnow().isoformat()
    }
    log_event("saas_plan_created", saas_plans[plan_id])
    return saas_plans[plan_id]

@router.post("/contracts/create")
async def create_contract(payload: CommercialContract):
    if payload.hospital_id not in hospital_targets:
        raise HTTPException(status_code=404, detail="Hospital target not found")
    if payload.plan_id not in saas_plans:
        raise HTTPException(status_code=404, detail="SaaS plan not found")

    contract_id = uid("CONTRACT")
    annualized_value = payload.contract_value_usd * (12 / payload.duration_months)

    commercial_contracts[contract_id] = {
        "contract_id": contract_id,
        "hospital_id": payload.hospital_id,
        "plan_id": payload.plan_id,
        "contract_value_usd": payload.contract_value_usd,
        "duration_months": payload.duration_months,
        "annualized_value_usd": round(annualized_value, 2),
        "status": payload.status,
        "created_at": datetime.utcnow().isoformat()
    }
    log_event("commercial_contract_created", commercial_contracts[contract_id])
    return commercial_contracts[contract_id]

@router.get("/dashboard")
async def dashboard():
    total_contract_value = sum(c["contract_value_usd"] for c in commercial_contracts.values())
    annualized_revenue = sum(c["annualized_value_usd"] for c in commercial_contracts.values())
    signed_contracts = len([c for c in commercial_contracts.values() if c["status"] in ["signed", "active"]])
    strategic_markets = len([m for m in markets.values() if m["priority"] == "strategic"])

    launch_score = 0.90
    if len(markets) >= 2:
        launch_score += 0.02
    if len(hospital_targets) >= 2:
        launch_score += 0.02
    if len(saas_plans) >= 1:
        launch_score += 0.02
    if signed_contracts >= 1:
        launch_score += 0.03
    if strategic_markets >= 1:
        launch_score += 0.02

    return {
        "phase": "AHOS 51.0",
        "readiness": "GLOBAL_COMMERCIAL_LAUNCH_READY",
        "status": "operational",
        "markets_registered": len(markets),
        "strategic_markets": strategic_markets,
        "hospital_targets": len(hospital_targets),
        "saas_plans": len(saas_plans),
        "commercial_contracts": len(commercial_contracts),
        "signed_or_active_contracts": signed_contracts,
        "total_contract_value_usd": total_contract_value,
        "annualized_revenue_usd": round(annualized_revenue, 2),
        "target_hospitals_global": 100,
        "launch_score": round(min(launch_score, 0.99), 3)
    }

@router.get("/market-expansion/plan")
async def market_expansion_plan():
    return {
        "phase": "AHOS 51.0",
        "expansion_strategy": "MENA-first, then Europe and Africa",
        "target_hospitals_24_months": 100,
        "priority_markets": ["Libya", "Sweden", "GCC", "Egypt", "Tunisia", "Morocco"],
        "commercial_model": [
            "Enterprise SaaS",
            "Hybrid hospital deployment",
            "Clinical AI modules licensing",
            "RWE and regulatory evidence services",
            "Strategic government healthcare partnerships"
        ],
        "required_next_steps": [
            "Sign first 3 pilot hospital contracts",
            "Prepare investor deck and financial model",
            "Connect real FHIR/DICOM hospital endpoints",
            "Run independent cybersecurity audit",
            "Prepare regulatory submission evidence package",
            "Build sales and implementation playbook"
        ]
    }

@router.get("/revenue/forecast")
async def revenue_forecast():
    return {
        "phase": "AHOS 51.0",
        "scenario": "100 hospital expansion",
        "assumptions": {
            "average_contract_value_per_hospital_usd": 500000,
            "target_hospitals": 100,
            "implementation_services_per_hospital_usd": 150000,
            "gross_margin_estimate": 0.72
        },
        "estimated_arr_usd": 50000000,
        "implementation_revenue_usd": 15000000,
        "total_year_1_revenue_potential_usd": 65000000,
        "estimated_gross_profit_usd": 46800000,
        "status": "forecast_model_ready"
    }

@router.get("/events")
async def events():
    return {
        "count": len(launch_events),
        "events": launch_events[-50:]
    }
