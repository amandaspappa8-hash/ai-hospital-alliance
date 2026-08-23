from fastapi import APIRouter

router = APIRouter(
    prefix="/aghos/25.2/event-monitoring",
    tags=["AGHOS 25.2 Real-Time Event Monitoring Center"]
)

@router.get("/dashboard")
def dashboard():
    return {
        "monitoring_status": "ONLINE",
        "persistent_storage": "active",
        "decision_logs": 2,
        "bus_events": 2,
        "critical_decisions": 2,
        "high_priority_events": 2,
        "main_target_engine": "icu_engine",
        "websockets": {
            "clinical_events": "/ws/clinical-events",
            "live_clinical_events": "/ws/live-clinical-events"
        },
        "event_stream": [
            {
                "event_id": "BUS-DB-00002",
                "source_engine": "decision_supervisor_database_adapter",
                "target_engine": "icu_engine",
                "event_type": "critical_decision_persisted",
                "priority": "high",
                "patient_id": "P-2002",
                "recommended_action": "icu_escalation"
            },
            {
                "event_id": "BUS-DB-00001",
                "source_engine": "patient_monitoring",
                "target_engine": "icu_engine",
                "event_type": "critical_vital_sign_alert",
                "priority": "high",
                "patient_id": "P-1001",
                "risk": "critical"
            }
        ]
    }
