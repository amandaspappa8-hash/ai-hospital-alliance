from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any, List
from uuid import uuid4
import random
import time

router = APIRouter(
    prefix="/ahos/49.0.5/global-monitoring",
    tags=["AHOS 49.0.5 Global Healthcare Monitoring Platform"]
)

hospital_metrics: Dict[str, Dict[str, Any]] = {}
api_metrics: List[Dict[str, Any]] = []
ai_metrics: List[Dict[str, Any]] = []
alerts: List[Dict[str, Any]] = []
incidents: List[Dict[str, Any]] = []

def create_alert(level: str, title: str, message: str):
    alert = {
        "alert_id": "ALERT-" + uuid4().hex[:10].upper(),
        "level": level,
        "title": title,
        "message": message,
        "created_at": datetime.utcnow().isoformat()
    }
    alerts.append(alert)
    return alert

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 49.0.5",
        "platform": "Global Healthcare Monitoring Platform",
        "readiness": "GLOBAL_HEALTHCARE_MONITORING_READY",
        "capabilities": [
            "Global Monitoring Dashboard",
            "Hospital Health Metrics",
            "API Metrics",
            "AI Metrics",
            "FHIR/DICOM Monitoring",
            "SLA Monitoring",
            "Incident Detection",
            "Alert Engine"
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/metrics/hospital/{hospital_id}")
async def generate_hospital_metrics(hospital_id: str):
    metrics = {
        "hospital_id": hospital_id,
        "cpu_usage": round(random.uniform(20,95),2),
        "memory_usage": round(random.uniform(20,95),2),
        "disk_usage": round(random.uniform(20,90),2),
        "fhir_requests": random.randint(100,5000),
        "dicom_requests": random.randint(50,3000),
        "active_patients": random.randint(50,5000),
        "active_users": random.randint(10,500),
        "api_latency_ms": random.randint(20,900),
        "generated_at": datetime.utcnow().isoformat()
    }

    hospital_metrics[hospital_id] = metrics

    if metrics["cpu_usage"] > 90:
        create_alert(
            "CRITICAL",
            "High CPU Usage",
            f"{hospital_id} CPU usage exceeded 90%"
        )

    if metrics["api_latency_ms"] > 800:
        create_alert(
            "HIGH",
            "API Latency",
            f"{hospital_id} API latency exceeded 800ms"
        )

    return metrics

@router.post("/metrics/api")
async def api_metric():
    metric = {
        "metric_id": "API-" + uuid4().hex[:8].upper(),
        "requests_per_minute": random.randint(100,10000),
        "error_rate": round(random.uniform(0,5),2),
        "avg_latency_ms": random.randint(10,800),
        "uptime_percent": round(random.uniform(98,100),3),
        "timestamp": datetime.utcnow().isoformat()
    }

    api_metrics.append(metric)

    if metric["error_rate"] > 3:
        create_alert(
            "HIGH",
            "API Error Rate",
            f"Error rate reached {metric['error_rate']}%"
        )

    return metric

@router.post("/metrics/ai")
async def ai_metric():
    metric = {
        "metric_id": "AI-" + uuid4().hex[:8].upper(),
        "models_online": random.randint(5,100),
        "predictions_per_hour": random.randint(1000,100000),
        "avg_inference_ms": random.randint(20,600),
        "accuracy_score": round(random.uniform(0.85,0.99),3),
        "f1_score": round(random.uniform(0.80,0.98),3),
        "timestamp": datetime.utcnow().isoformat()
    }

    ai_metrics.append(metric)

    if metric["accuracy_score"] < 0.90:
        create_alert(
            "MEDIUM",
            "AI Accuracy Drop",
            f"Accuracy dropped to {metric['accuracy_score']}"
        )

    return metric

@router.post("/incidents/create")
async def create_incident():
    incident = {
        "incident_id": "INC-" + uuid4().hex[:10].upper(),
        "severity": random.choice(
            ["LOW","MEDIUM","HIGH","CRITICAL"]
        ),
        "service": random.choice(
            ["FHIR","DICOM","DATABASE","AI","AUTH"]
        ),
        "status": "open",
        "created_at": datetime.utcnow().isoformat()
    }

    incidents.append(incident)

    if incident["severity"] == "CRITICAL":
        create_alert(
            "CRITICAL",
            "Critical Incident",
            incident["service"]
        )

    return incident

@router.get("/dashboard")
async def dashboard():
    total_hospitals = len(hospital_metrics)
    total_alerts = len(alerts)
    total_incidents = len(incidents)

    critical_alerts = len([
        a for a in alerts
        if a["level"] == "CRITICAL"
    ])

    status = "HEALTHY"

    if critical_alerts > 0:
        status = "CRITICAL"
    elif total_alerts > 5:
        status = "DEGRADED"

    return {
        "phase": "AHOS 49.0.5",
        "readiness": "GLOBAL_HEALTHCARE_MONITORING_READY",
        "global_status": status,
        "monitored_hospitals": total_hospitals,
        "api_metrics": len(api_metrics),
        "ai_metrics": len(ai_metrics),
        "alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "incidents": total_incidents,
        "sla_percent": 99.95,
        "monitoring_score": 0.95,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/alerts")
async def get_alerts():
    return {
        "count": len(alerts),
        "alerts": alerts[-50:]
    }

@router.get("/incidents")
async def get_incidents():
    return {
        "count": len(incidents),
        "incidents": incidents[-50:]
    }

@router.get("/metrics/prometheus")
async def prometheus_metrics():
    return {
        "ahos_uptime_seconds": int(time.time()),
        "ahos_hospitals_total": len(hospital_metrics),
        "ahos_alerts_total": len(alerts),
        "ahos_incidents_total": len(incidents),
        "ahos_api_metrics_total": len(api_metrics),
        "ahos_ai_metrics_total": len(ai_metrics)
    }
