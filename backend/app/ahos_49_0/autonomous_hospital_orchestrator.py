from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

router = APIRouter(
    prefix="/ahos/49.0.4/autonomous-hospital-orchestrator",
    tags=["AHOS 49.0.4 Autonomous Hospital Orchestrator"]
)

beds_db: Dict[str, Dict[str, Any]] = {}
icu_units_db: Dict[str, Dict[str, Any]] = {}
emergency_cases_db: Dict[str, Dict[str, Any]] = {}
resources_db: Dict[str, Dict[str, Any]] = {}
orchestration_events: List[Dict[str, Any]] = []

class BedRegister(BaseModel):
    hospital_id: str
    ward: str
    bed_type: str = Field(..., examples=["general", "icu", "emergency", "surgery"])
    status: str = Field("available", examples=["available", "occupied", "cleaning", "maintenance"])
    tenant_id: str = "default_hospital"

class ICUCapacity(BaseModel):
    hospital_id: str
    total_icu_beds: int
    occupied_icu_beds: int
    ventilators_total: int
    ventilators_used: int
    staff_on_duty: int

class EmergencyCase(BaseModel):
    hospital_id: str
    patient_id: str
    chief_complaint: str
    severity_score: int = Field(..., ge=0, le=100)
    vitals_unstable: bool = False
    suspected_condition: Optional[str] = None

class ResourceRegister(BaseModel):
    hospital_id: str
    resource_name: str
    category: str = Field(..., examples=["staff", "equipment", "medication", "ambulance", "operating_room"])
    total: int
    available: int
    critical_threshold: int = 1

def clinical_priority(score: int, unstable: bool):
    if unstable or score >= 85:
        return "CRITICAL", "immediate_resuscitation"
    if score >= 65:
        return "HIGH", "urgent_physician_review"
    if score >= 35:
        return "MEDIUM", "standard_clinical_pathway"
    return "LOW", "routine_monitoring"

def log_event(event_type: str, payload: Dict[str, Any]):
    event = {
        "event_id": "ORCH-" + uuid4().hex[:10].upper(),
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }
    orchestration_events.append(event)
    return event

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 49.0.4",
        "platform": "Autonomous Hospital Orchestrator",
        "readiness": "AUTONOMOUS_HOSPITAL_ORCHESTRATOR_READY",
        "capabilities": [
            "Bed Management AI",
            "ICU Capacity Prediction",
            "Emergency Routing",
            "Resource Allocation",
            "Clinical Priority Engine",
            "Hospital Command Center"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/beds/register")
async def register_bed(payload: BedRegister):
    bed_id = "BED-" + uuid4().hex[:10].upper()
    beds_db[bed_id] = {
        "bed_id": bed_id,
        "hospital_id": payload.hospital_id,
        "ward": payload.ward,
        "bed_type": payload.bed_type,
        "status": payload.status,
        "tenant_id": payload.tenant_id,
        "registered_at": datetime.utcnow().isoformat()
    }
    log_event("bed_registered", beds_db[bed_id])
    return beds_db[bed_id]

@router.get("/beds/availability")
async def bed_availability(hospital_id: Optional[str] = None):
    beds = list(beds_db.values())
    if hospital_id:
        beds = [b for b in beds if b["hospital_id"] == hospital_id]

    total = len(beds)
    available = len([b for b in beds if b["status"] == "available"])
    occupied = len([b for b in beds if b["status"] == "occupied"])

    return {
        "hospital_id": hospital_id or "all",
        "total_beds": total,
        "available_beds": available,
        "occupied_beds": occupied,
        "availability_rate": round(available / total, 3) if total else 0
    }

@router.post("/icu/capacity")
async def icu_capacity(payload: ICUCapacity):
    icu_id = "ICU-" + uuid4().hex[:10].upper()
    occupancy_rate = payload.occupied_icu_beds / payload.total_icu_beds if payload.total_icu_beds else 0
    ventilator_usage = payload.ventilators_used / payload.ventilators_total if payload.ventilators_total else 0

    risk = "LOW"
    recommendation = "normal_operations"

    if occupancy_rate >= 0.9 or ventilator_usage >= 0.9:
        risk = "CRITICAL"
        recommendation = "activate_icu_surge_protocol"
    elif occupancy_rate >= 0.75 or ventilator_usage >= 0.75:
        risk = "HIGH"
        recommendation = "prepare_transfer_and_staffing_plan"
    elif occupancy_rate >= 0.55:
        risk = "MEDIUM"
        recommendation = "monitor_capacity_closely"

    icu_units_db[icu_id] = {
        "icu_id": icu_id,
        "hospital_id": payload.hospital_id,
        "total_icu_beds": payload.total_icu_beds,
        "occupied_icu_beds": payload.occupied_icu_beds,
        "ventilators_total": payload.ventilators_total,
        "ventilators_used": payload.ventilators_used,
        "staff_on_duty": payload.staff_on_duty,
        "occupancy_rate": round(occupancy_rate, 3),
        "ventilator_usage": round(ventilator_usage, 3),
        "risk_level": risk,
        "recommendation": recommendation,
        "reported_at": datetime.utcnow().isoformat()
    }

    log_event("icu_capacity_reported", icu_units_db[icu_id])
    return icu_units_db[icu_id]

@router.post("/emergency/triage")
async def emergency_triage(payload: EmergencyCase):
    case_id = "ER-" + uuid4().hex[:10].upper()
    priority, action = clinical_priority(payload.severity_score, payload.vitals_unstable)

    route = "general_emergency"
    if priority == "CRITICAL":
        route = "resuscitation_room"
    elif priority == "HIGH":
        route = "urgent_care_zone"
    elif priority == "MEDIUM":
        route = "standard_er_track"
    else:
        route = "fast_track"

    emergency_cases_db[case_id] = {
        "case_id": case_id,
        "hospital_id": payload.hospital_id,
        "patient_id": payload.patient_id,
        "chief_complaint": payload.chief_complaint,
        "severity_score": payload.severity_score,
        "vitals_unstable": payload.vitals_unstable,
        "suspected_condition": payload.suspected_condition,
        "clinical_priority": priority,
        "recommended_action": action,
        "routing_destination": route,
        "triaged_at": datetime.utcnow().isoformat()
    }

    log_event("emergency_triage_completed", emergency_cases_db[case_id])
    return emergency_cases_db[case_id]

@router.post("/resources/register")
async def register_resource(payload: ResourceRegister):
    resource_id = "RES-" + uuid4().hex[:10].upper()
    availability_rate = payload.available / payload.total if payload.total else 0
    status = "stable"

    if payload.available <= payload.critical_threshold:
        status = "critical"
    elif availability_rate <= 0.25:
        status = "low"

    resources_db[resource_id] = {
        "resource_id": resource_id,
        "hospital_id": payload.hospital_id,
        "resource_name": payload.resource_name,
        "category": payload.category,
        "total": payload.total,
        "available": payload.available,
        "critical_threshold": payload.critical_threshold,
        "availability_rate": round(availability_rate, 3),
        "resource_status": status,
        "registered_at": datetime.utcnow().isoformat()
    }

    log_event("resource_registered", resources_db[resource_id])
    return resources_db[resource_id]

@router.get("/command-center")
async def command_center():
    total_beds = len(beds_db)
    available_beds = len([b for b in beds_db.values() if b["status"] == "available"])
    critical_er = len([c for c in emergency_cases_db.values() if c["clinical_priority"] == "CRITICAL"])
    high_er = len([c for c in emergency_cases_db.values() if c["clinical_priority"] == "HIGH"])
    critical_resources = len([r for r in resources_db.values() if r["resource_status"] == "critical"])
    critical_icu = len([i for i in icu_units_db.values() if i["risk_level"] == "CRITICAL"])

    operational_risk = "LOW"
    if critical_er > 0 or critical_icu > 0 or critical_resources > 0:
        operational_risk = "CRITICAL"
    elif high_er > 0:
        operational_risk = "HIGH"
    elif total_beds and available_beds / total_beds < 0.25:
        operational_risk = "MEDIUM"

    return {
        "phase": "AHOS 49.0.4",
        "readiness": "AUTONOMOUS_HOSPITAL_ORCHESTRATOR_READY",
        "status": "operational",
        "total_beds": total_beds,
        "available_beds": available_beds,
        "icu_reports": len(icu_units_db),
        "emergency_cases": len(emergency_cases_db),
        "critical_emergency_cases": critical_er,
        "registered_resources": len(resources_db),
        "critical_resources": critical_resources,
        "critical_icu_units": critical_icu,
        "operational_risk": operational_risk,
        "orchestration_events": len(orchestration_events),
        "autonomous_score": 0.94
    }

@router.get("/events")
async def events():
    return {
        "count": len(orchestration_events),
        "events": orchestration_events[-25:]
    }
