from fastapi import APIRouter
from datetime import datetime
import requests

router = APIRouter(
    prefix="/aiha/10.2",
    tags=["AIHA 10.2 Autonomous Clinical Story Engine"]
)

TIMELINE_URL = "http://127.0.0.1:8000/aiha/10.1/timeline"


def classify_risk(events):
    critical = len([e for e in events if e.get("severity") == "CRITICAL"])
    warning = len([e for e in events if e.get("severity") == "WARNING"])

    if critical >= 2:
        return "HIGH"
    if critical == 1 or warning >= 2:
        return "MODERATE"
    return "LOW"


def extract_key_findings(events):
    findings = []

    for e in events:
        payload = e.get("payload", {})
        etype = e.get("type", "")

        if etype == "LABORATORY":
            if "rule_results" in payload:
                critical = [r for r in payload.get("rule_results", []) if r.get("status") == "critical"]
                abnormal = [r for r in payload.get("rule_results", []) if r.get("status") in ["high", "low"]]

                for r in critical[:3]:
                    findings.append(
                        f"Critical lab: {r.get('test')} {r.get('value')} — {r.get('interpretation')}"
                    )

                for r in abnormal[:5]:
                    findings.append(
                        f"Abnormal lab: {r.get('test')} {r.get('value')}"
                    )
            else:
                findings.append(
                    f"Laboratory result: {payload.get('test', 'Lab')} — {payload.get('flag', 'recorded')}"
                )

        elif etype == "RADIOLOGY":
            findings.append(
                f"Radiology: {payload.get('modality', 'Imaging')} — "
                f"{payload.get('finding', 'finding recorded')} "
                f"with risk {payload.get('risk_level', 'unknown')}"
            )

        elif etype == "DECISION":
            alerts = ", ".join(payload.get("alerts", []))
            findings.append(
                f"Decision alert: {payload.get('decision_type', 'clinical decision')} — "
                f"{alerts or payload.get('recommendation', 'review required')}"
            )

        elif etype == "PATIENT_STATE":
            findings.append(
                f"Vitals: HR {payload.get('heart_rate', 'N/A')}, "
                f"SpO2 {payload.get('spo2', 'N/A')}, "
                f"risk {payload.get('risk_level', 'unknown')}"
            )

    return findings[:12]


def make_recommendations(risk, findings):
    text = " ".join(findings).lower()
    recs = []

    if risk == "HIGH":
        recs.append("Escalate patient to senior clinical review.")
    elif risk == "MODERATE":
        recs.append("Continue close monitoring and repeat assessment.")
    else:
        recs.append("Continue routine monitoring.")

    if "troponin" in text:
        recs.append("Urgent ECG and cardiology review recommended.")

    if "creatinine" in text or "potassium" in text:
        recs.append("Nephrology review and electrolyte monitoring recommended.")

    if "glucose" in text:
        recs.append("Start or review glucose management protocol.")

    if "bleeding risk" in text or "warfarin" in text or "aspirin" in text:
        recs.append("Medication reconciliation and bleeding-risk review by pharmacist/doctor.")

    if "radiology" in text:
        recs.append("Review imaging findings with radiology and correlate clinically.")

    return list(dict.fromkeys(recs))[:6]


@router.get("/health")
def health():
    return {
        "status": "online",
        "engine": "Autonomous Clinical Story Engine",
        "stage": "AI Hospital Alliance 10.2",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/story/{patient_id}")
def clinical_story(patient_id: str):
    timeline_response = requests.get(f"{TIMELINE_URL}/{patient_id}", timeout=10)
    timeline_data = timeline_response.json()

    events = timeline_data.get("timeline", [])
    risk = classify_risk(events)
    findings = extract_key_findings(events)
    recommendations = make_recommendations(risk, findings)

    first_event = events[-1]["timestamp"] if events else None
    last_event = events[0]["timestamp"] if events else None

    thirty_sec_summary = (
        f"Patient {patient_id} has {len(events)} timeline events. "
        f"Current overall risk is {risk}. "
        f"Key issues include: " + "; ".join(findings[:3]) + "."
        if findings else
        f"Patient {patient_id} has no significant clinical events recorded."
    )

    two_min_summary = (
        f"Patient {patient_id} clinical timeline from {first_event} to {last_event}. "
        f"The system detected {timeline_data.get('critical_count', 0)} critical events, "
        f"{timeline_data.get('warning_count', 0)} warning events, and "
        f"{timeline_data.get('normal_count', 0)} normal events. "
        f"Main findings: " + " | ".join(findings[:8]) + ". "
        f"Recommended actions: " + " | ".join(recommendations)
    )

    full_story_lines = [
        f"Autonomous Clinical Story for patient {patient_id}",
        f"Overall risk: {risk}",
        f"Timeline events: {len(events)}",
        "",
        "Clinical sequence:"
    ]

    for e in reversed(events):
        full_story_lines.append(
            f"- {e.get('timestamp')} | {e.get('severity')} | {e.get('source')} | {e.get('title')}"
        )

    full_story_lines.extend([
        "",
        "Key findings:",
        *[f"- {x}" for x in findings],
        "",
        "Recommendations:",
        *[f"- {x}" for x in recommendations],
    ])

    return {
        "status": "success",
        "patient_id": patient_id,
        "risk": risk,
        "event_count": len(events),
        "critical_count": timeline_data.get("critical_count", 0),
        "warning_count": timeline_data.get("warning_count", 0),
        "normal_count": timeline_data.get("normal_count", 0),
        "key_findings": findings,
        "recommendations": recommendations,
        "doctor_briefing": {
            "30_sec_summary": thirty_sec_summary,
            "2_min_summary": two_min_summary,
            "full_story": "\n".join(full_story_lines)
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
