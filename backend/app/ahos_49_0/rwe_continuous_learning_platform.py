from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import uuid4

router = APIRouter(
    prefix="/ahos/49.0.6/rwe-continuous-learning",
    tags=["AHOS 49.0.6 Real World Evidence & Continuous Learning Platform"]
)

studies_db: Dict[str, Dict[str, Any]] = {}
cases_db: Dict[str, Dict[str, Any]] = {}
outcomes_db: Dict[str, Dict[str, Any]] = {}
feedback_db: List[Dict[str, Any]] = []
model_performance_db: Dict[str, Dict[str, Any]] = {}
learning_events: List[Dict[str, Any]] = []

class StudyCreate(BaseModel):
    study_name: str
    disease_area: str
    country: str
    hospital_id: str
    target_cases: int = 1000
    regulatory_pathway: str = "RWE"

class ClinicalCase(BaseModel):
    study_id: str
    patient_id: str
    diagnosis: str
    ai_prediction: str
    ai_confidence: float = Field(..., ge=0, le=1)
    clinician_decision: str
    agreement: bool

class OutcomeRecord(BaseModel):
    case_id: str
    outcome_type: str = Field(..., examples=["recovered", "improved", "stable", "worsened", "mortality"])
    days_to_outcome: int
    adverse_event: bool = False
    notes: Optional[str] = None

class ClinicianFeedback(BaseModel):
    case_id: str
    clinician_id: str
    rating: int = Field(..., ge=1, le=5)
    feedback_text: str
    suggested_correction: Optional[str] = None

class ModelPerformance(BaseModel):
    model_name: str
    model_version: str
    hospital_id: str
    accuracy: float = Field(..., ge=0, le=1)
    precision: float = Field(..., ge=0, le=1)
    recall: float = Field(..., ge=0, le=1)
    f1_score: float = Field(..., ge=0, le=1)
    sample_size: int

def log_learning_event(event_type: str, payload: Dict[str, Any]):
    event = {
        "event_id": "LEARN-" + uuid4().hex[:10].upper(),
        "event_type": event_type,
        "payload": payload,
        "created_at": datetime.utcnow().isoformat()
    }
    learning_events.append(event)
    return event

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 49.0.6",
        "platform": "Real World Evidence & Continuous Learning Platform",
        "readiness": "RWE_CONTINUOUS_LEARNING_READY",
        "capabilities": [
            "Clinical Evidence Registry",
            "Real World Evidence Metrics",
            "AI Feedback Loop",
            "Model Performance Tracking",
            "Outcome Monitoring",
            "Continuous Learning Engine",
            "Retraining Recommendation Engine"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/studies/create")
async def create_study(payload: StudyCreate):
    study_id = "RWE-STUDY-" + uuid4().hex[:10].upper()
    studies_db[study_id] = {
        "study_id": study_id,
        "study_name": payload.study_name,
        "disease_area": payload.disease_area,
        "country": payload.country,
        "hospital_id": payload.hospital_id,
        "target_cases": payload.target_cases,
        "regulatory_pathway": payload.regulatory_pathway,
        "status": "active",
        "created_at": datetime.utcnow().isoformat()
    }
    log_learning_event("study_created", studies_db[study_id])
    return studies_db[study_id]

@router.post("/cases/add")
async def add_case(payload: ClinicalCase):
    if payload.study_id not in studies_db:
        raise HTTPException(status_code=404, detail="Study not found")

    case_id = "RWE-CASE-" + uuid4().hex[:10].upper()

    risk_flag = "LOW"
    if payload.ai_confidence < 0.70 or not payload.agreement:
        risk_flag = "REVIEW_REQUIRED"

    cases_db[case_id] = {
        "case_id": case_id,
        "study_id": payload.study_id,
        "patient_id": payload.patient_id,
        "diagnosis": payload.diagnosis,
        "ai_prediction": payload.ai_prediction,
        "ai_confidence": payload.ai_confidence,
        "clinician_decision": payload.clinician_decision,
        "agreement": payload.agreement,
        "risk_flag": risk_flag,
        "added_at": datetime.utcnow().isoformat()
    }

    log_learning_event("clinical_case_added", cases_db[case_id])
    return cases_db[case_id]

@router.post("/outcomes/record")
async def record_outcome(payload: OutcomeRecord):
    if payload.case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Case not found")

    outcome_id = "OUTCOME-" + uuid4().hex[:10].upper()

    outcomes_db[outcome_id] = {
        "outcome_id": outcome_id,
        "case_id": payload.case_id,
        "outcome_type": payload.outcome_type,
        "days_to_outcome": payload.days_to_outcome,
        "adverse_event": payload.adverse_event,
        "notes": payload.notes,
        "recorded_at": datetime.utcnow().isoformat()
    }

    log_learning_event("outcome_recorded", outcomes_db[outcome_id])
    return outcomes_db[outcome_id]

@router.post("/feedback/clinician")
async def clinician_feedback(payload: ClinicianFeedback):
    if payload.case_id not in cases_db:
        raise HTTPException(status_code=404, detail="Case not found")

    feedback = {
        "feedback_id": "FDBK-" + uuid4().hex[:10].upper(),
        "case_id": payload.case_id,
        "clinician_id": payload.clinician_id,
        "rating": payload.rating,
        "feedback_text": payload.feedback_text,
        "suggested_correction": payload.suggested_correction,
        "created_at": datetime.utcnow().isoformat()
    }

    feedback_db.append(feedback)
    log_learning_event("clinician_feedback_received", feedback)
    return feedback

@router.post("/models/performance")
async def model_performance(payload: ModelPerformance):
    perf_id = "MODEL-PERF-" + uuid4().hex[:10].upper()

    retraining_needed = False
    reason = "performance_stable"

    if payload.accuracy < 0.90 or payload.f1_score < 0.88:
        retraining_needed = True
        reason = "performance_below_threshold"

    model_performance_db[perf_id] = {
        "performance_id": perf_id,
        "model_name": payload.model_name,
        "model_version": payload.model_version,
        "hospital_id": payload.hospital_id,
        "accuracy": payload.accuracy,
        "precision": payload.precision,
        "recall": payload.recall,
        "f1_score": payload.f1_score,
        "sample_size": payload.sample_size,
        "retraining_needed": retraining_needed,
        "reason": reason,
        "reported_at": datetime.utcnow().isoformat()
    }

    log_learning_event("model_performance_reported", model_performance_db[perf_id])
    return model_performance_db[perf_id]

@router.get("/evidence/dashboard")
async def evidence_dashboard():
    total_cases = len(cases_db)
    agreements = len([c for c in cases_db.values() if c["agreement"]])
    review_required = len([c for c in cases_db.values() if c["risk_flag"] == "REVIEW_REQUIRED"])
    adverse_events = len([o for o in outcomes_db.values() if o["adverse_event"]])
    retraining_flags = len([m for m in model_performance_db.values() if m["retraining_needed"]])

    physician_agreement_rate = round(agreements / total_cases, 3) if total_cases else 0

    evidence_score = 0.95
    if physician_agreement_rate < 0.85 and total_cases > 0:
        evidence_score -= 0.1
    if adverse_events > 0:
        evidence_score -= 0.05
    if retraining_flags > 0:
        evidence_score -= 0.05

    return {
        "phase": "AHOS 49.0.6",
        "readiness": "RWE_CONTINUOUS_LEARNING_READY",
        "active_studies": len(studies_db),
        "clinical_cases": total_cases,
        "outcomes_recorded": len(outcomes_db),
        "clinician_feedback": len(feedback_db),
        "model_performance_reports": len(model_performance_db),
        "physician_agreement_rate": physician_agreement_rate,
        "review_required_cases": review_required,
        "adverse_events": adverse_events,
        "retraining_flags": retraining_flags,
        "evidence_score": round(evidence_score, 3),
        "status": "operational"
    }

@router.get("/learning/recommendations")
async def learning_recommendations():
    recommendations = []

    for perf in model_performance_db.values():
        if perf["retraining_needed"]:
            recommendations.append({
                "type": "model_retraining",
                "model": perf["model_name"],
                "version": perf["model_version"],
                "hospital_id": perf["hospital_id"],
                "reason": perf["reason"],
                "priority": "HIGH"
            })

    if len([c for c in cases_db.values() if c["risk_flag"] == "REVIEW_REQUIRED"]) > 0:
        recommendations.append({
            "type": "clinical_review",
            "reason": "AI/clinician disagreement or low confidence",
            "priority": "MEDIUM"
        })

    if not recommendations:
        recommendations.append({
            "type": "continue_monitoring",
            "reason": "Evidence and model performance stable",
            "priority": "LOW"
        })

    return {
        "count": len(recommendations),
        "recommendations": recommendations
    }

@router.get("/events")
async def events():
    return {
        "count": len(learning_events),
        "events": learning_events[-50:]
    }
