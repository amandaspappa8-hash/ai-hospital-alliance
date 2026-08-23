from fastapi import APIRouter
from datetime import datetime
import requests

router = APIRouter(
    prefix="/aiha/11.0",
    tags=["AIHA 11.0 Autonomous Medical Command Brain"]
)

BASE = "http://127.0.0.1:8000"

TIMELINE_URL = f"{BASE}/aiha/10.1/timeline"
STORY_URL = f"{BASE}/aiha/10.2/story"
REASON_URL = f"{BASE}/aiha/10.3/reason"
CARE_PLAN_URL = f"{BASE}/aiha/10.4/plan"
OUTCOME_URL = f"{BASE}/aiha/10.5/outcome-score"
PROGNOSIS_URL = f"{BASE}/aiha/10.5/prognosis"
EARLY_WARNING_URL = f"{BASE}/aiha/10.5/early-warning"


def safe_get(url: str):
    try:
        r = requests.get(url, timeout=10)
        return r.json()
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "url": url
        }


def extract_active_problems(reasoning: dict, care_plan: dict):
    problems = []

    for dx in reasoning.get("differential_diagnosis", []):
        problems.append({
            "problem": dx.get("diagnosis"),
            "confidence": dx.get("confidence"),
            "source": "Clinical Reasoning 10.3"
        })

    for item in care_plan.get("care_plan", {}).get("problem_list", []):
        name = item.get("problem")
        if name and name not in [p["problem"] for p in problems]:
            problems.append({
                "problem": name,
                "confidence": item.get("confidence"),
                "source": "Care Plan 10.4"
            })

    return problems


def build_command_status(risk: str, warning: dict):
    alert_level = warning.get("alert_level", "LOW")

    if risk == "HIGH" or alert_level == "HIGH":
        return "CRITICAL_COMMAND"
    if risk == "MODERATE" or alert_level == "MODERATE":
        return "ACTIVE_MONITORING"
    return "STABLE_COMMAND"


@router.get("/health")
def health():
    return {
        "status": "online",
        "stage": "AI Hospital Alliance 11.0",
        "engine": "Autonomous Medical Command Brain",
        "module": "11.0.1 Global Patient Understanding",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/brain/{patient_id}")
def global_patient_understanding(patient_id: str):
    timeline = safe_get(f"{TIMELINE_URL}/{patient_id}")
    story = safe_get(f"{STORY_URL}/{patient_id}")
    reasoning = safe_get(f"{REASON_URL}/{patient_id}")
    care_plan = safe_get(f"{CARE_PLAN_URL}/{patient_id}")
    outcome = safe_get(f"{OUTCOME_URL}/{patient_id}")
    prognosis = safe_get(f"{PROGNOSIS_URL}/{patient_id}")
    early_warning = safe_get(f"{EARLY_WARNING_URL}/{patient_id}")

    risk = reasoning.get("overall_risk") or story.get("risk") or prognosis.get("overall_prognosis") or "UNKNOWN"

    active_problems = extract_active_problems(reasoning, care_plan)

    command_status = build_command_status(risk, early_warning)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.1 Global Patient Understanding",
        "patient_id": patient_id,
        "command_status": command_status,
        "global_patient_understanding": {
            "overall_risk": risk,
            "timeline_events": timeline.get("timeline_count", 0),
            "critical_events": timeline.get("critical_count", 0),
            "warning_events": timeline.get("warning_count", 0),
            "normal_events": timeline.get("normal_count", 0),
            "active_problems": active_problems,
            "key_findings": story.get("key_findings", []),
            "clinical_reasoning": reasoning.get("clinical_reasoning", []),
            "recommendations": reasoning.get("recommendations", story.get("recommendations", [])),
            "care_plan": care_plan.get("care_plan", {}),
            "outcome_prediction": {
                "risk_score": outcome.get("risk_score"),
                "survival": outcome.get("survival"),
                "icu": outcome.get("icu"),
                "readmission": outcome.get("readmission"),
                "deterioration": outcome.get("deterioration"),
                "prognosis": prognosis.get("overall_prognosis"),
                "early_warning": early_warning.get("alert_level")
            }
        },
        "source_engines": {
            "timeline_10_1": timeline.get("status"),
            "story_10_2": story.get("status"),
            "reasoning_10_3": reasoning.get("status"),
            "care_plan_10_4": care_plan.get("status"),
            "outcome_10_5": outcome.get("status"),
            "prognosis_10_5": prognosis.get("status"),
            "early_warning_10_5": early_warning.get("status")
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def select_priority_problem(active_problems):
    if not active_problems:
        return "No active critical problem identified"

    priority_order = [
        "Acute Coronary Syndrome",
        "Acute Kidney Injury",
        "Medication Related Bleeding Risk",
        "High medication-related bleeding risk",
        "Uncontrolled Hyperglycemia"
    ]

    for target in priority_order:
        for p in active_problems:
            if p.get("problem") == target:
                return target

    return active_problems[0].get("problem", "Unknown clinical problem")


def build_unified_decision(understanding):
    risk = understanding.get("overall_risk", "UNKNOWN")
    problems = understanding.get("active_problems", [])
    outcome = understanding.get("outcome_prediction", {})
    care_plan = understanding.get("care_plan", {})

    priority_problem = select_priority_problem(problems)

    actions = care_plan.get("immediate_actions", [])
    consultations = care_plan.get("consultations", [])

    icu_probability = outcome.get("icu") or 0
    deterioration = outcome.get("deterioration") or 0
    early_warning = outcome.get("early_warning")

    if risk == "HIGH" or icu_probability >= 0.70 or early_warning == "HIGH":
        decision_level = "CRITICAL"
        final_decision = "High-risk patient requiring urgent senior clinical review and possible ICU escalation."
        escalation = "ICU_REVIEW"
    elif risk == "MODERATE" or deterioration >= 0.45:
        decision_level = "WARNING"
        final_decision = "Moderate-risk patient requiring close monitoring and repeated reassessment."
        escalation = "CLOSE_MONITORING"
    else:
        decision_level = "STABLE"
        final_decision = "Patient currently stable with routine monitoring."
        escalation = "ROUTINE"

    return {
        "decision_level": decision_level,
        "final_decision": final_decision,
        "priority_problem": priority_problem,
        "overall_risk": risk,
        "escalation": escalation,
        "required_consultations": consultations,
        "recommended_actions": actions[:8],
        "safety_flags": {
            "icu_probability": icu_probability,
            "deterioration_probability": deterioration,
            "early_warning": early_warning
        }
    }


@router.get("/decision/{patient_id}")
def unified_medical_decision(patient_id: str):
    brain = global_patient_understanding(patient_id)

    understanding = brain.get("global_patient_understanding", {})
    decision = build_unified_decision(understanding)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.2 Unified Medical Decision Engine",
        "patient_id": patient_id,
        "command_status": brain.get("command_status"),
        "unified_medical_decision": decision,
        "source": "11.0.1 Global Patient Understanding",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def calculate_escalation_score(decision):
    flags = decision.get("safety_flags", {})
    score = 0

    if decision.get("decision_level") == "CRITICAL":
        score += 40
    elif decision.get("decision_level") == "WARNING":
        score += 25
    else:
        score += 10

    score += int((flags.get("icu_probability") or 0) * 30)
    score += int((flags.get("deterioration_probability") or 0) * 20)

    if flags.get("early_warning") == "HIGH":
        score += 10

    return min(score, 100)


def classify_escalation(score):
    if score >= 90:
        return "EMERGENCY_RESPONSE"
    if score >= 75:
        return "ICU"
    if score >= 55:
        return "HDU"
    if score >= 30:
        return "CLOSE_MONITORING"
    return "ROUTINE"


def build_escalation_reasons(decision):
    reasons = []

    if decision.get("decision_level") == "CRITICAL":
        reasons.append("Unified Medical Decision classified patient as CRITICAL.")

    if decision.get("overall_risk") == "HIGH":
        reasons.append("Overall clinical risk is HIGH.")

    flags = decision.get("safety_flags", {})

    if (flags.get("icu_probability") or 0) >= 0.70:
        reasons.append(f"ICU probability is high: {flags.get('icu_probability')}.")

    if (flags.get("deterioration_probability") or 0) >= 0.50:
        reasons.append(f"Deterioration probability is high: {flags.get('deterioration_probability')}.")

    if flags.get("early_warning") == "HIGH":
        reasons.append("Early warning system is HIGH.")

    if decision.get("priority_problem"):
        reasons.append(f"Priority problem: {decision.get('priority_problem')}.")

    return reasons


@router.get("/escalation/{patient_id}")
def autonomous_escalation(patient_id: str):
    decision_response = unified_medical_decision(patient_id)
    decision = decision_response.get("unified_medical_decision", {})

    score = calculate_escalation_score(decision)
    level = classify_escalation(score)

    teams = list(dict.fromkeys(
        decision.get("required_consultations", []) +
        (["ICU Team"] if level in ["ICU", "EMERGENCY_RESPONSE"] else []) +
        (["Emergency Response Team"] if level == "EMERGENCY_RESPONSE" else [])
    ))

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.3 Autonomous Escalation Engine",
        "patient_id": patient_id,
        "escalation_level": level,
        "escalation_score": score,
        "reasons": build_escalation_reasons(decision),
        "required_teams": teams,
        "required_actions": decision.get("recommended_actions", []),
        "source": "11.0.2 Unified Medical Decision Engine",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/icu-candidates")
def icu_candidates():
    patient_ids = ["P-1001"]

    candidates = []
    for patient_id in patient_ids:
        result = autonomous_escalation(patient_id)
        if result.get("escalation_level") in ["ICU", "EMERGENCY_RESPONSE"]:
            candidates.append(result)

    return {
        "status": "success",
        "module": "11.0.3 ICU Candidates",
        "count": len(candidates),
        "candidates": candidates,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/emergency-candidates")
def emergency_candidates():
    patient_ids = ["P-1001"]

    candidates = []
    for patient_id in patient_ids:
        result = autonomous_escalation(patient_id)
        if result.get("escalation_level") == "EMERGENCY_RESPONSE":
            candidates.append(result)

    return {
        "status": "success",
        "module": "11.0.3 Emergency Candidates",
        "count": len(candidates),
        "candidates": candidates,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/escalation-dashboard")
def escalation_dashboard():
    patient_ids = ["P-1001"]

    results = [autonomous_escalation(pid) for pid in patient_ids]

    return {
        "status": "success",
        "module": "11.0.3 Escalation Dashboard",
        "total_patients": len(results),
        "emergency_response": len([r for r in results if r.get("escalation_level") == "EMERGENCY_RESPONSE"]),
        "icu": len([r for r in results if r.get("escalation_level") == "ICU"]),
        "hdu": len([r for r in results if r.get("escalation_level") == "HDU"]),
        "close_monitoring": len([r for r in results if r.get("escalation_level") == "CLOSE_MONITORING"]),
        "routine": len([r for r in results if r.get("escalation_level") == "ROUTINE"]),
        "patients": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


def agent_risk_score(level):
    return {
        "LOW": 25,
        "MODERATE": 55,
        "HIGH": 80,
        "CRITICAL": 95
    }.get(level, 40)


def build_medical_agents(patient_id: str):
    brain = global_patient_understanding(patient_id)
    decision_response = unified_medical_decision(patient_id)
    escalation_response = autonomous_escalation(patient_id)

    understanding = brain.get("global_patient_understanding", {})
    decision = decision_response.get("unified_medical_decision", {})
    escalation_level = escalation_response.get("escalation_level")

    findings_text = " ".join(understanding.get("key_findings", [])).lower()
    reasoning_text = " ".join(understanding.get("clinical_reasoning", [])).lower()

    agents = []

    radiology_risk = "HIGH" if "radiology" in findings_text and decision.get("overall_risk") == "HIGH" else "MODERATE"
    agents.append({
        "agent": "Radiology Agent",
        "domain": "Imaging",
        "risk": radiology_risk,
        "confidence": 0.86,
        "opinion": "Imaging findings require clinical correlation with current high-risk profile.",
        "recommendation": "Radiologist review and correlate with labs and vitals."
    })

    lab_risk = "CRITICAL" if any(x in findings_text for x in ["troponin", "creatinine", "potassium", "glucose"]) else "MODERATE"
    agents.append({
        "agent": "Laboratory Agent",
        "domain": "Laboratory",
        "risk": lab_risk,
        "confidence": 0.93,
        "opinion": "Critical or abnormal laboratory pattern detected.",
        "recommendation": "Repeat critical labs and monitor renal, cardiac, and metabolic markers."
    })

    pharmacy_risk = "CRITICAL" if "bleeding" in findings_text or "warfarin" in findings_text or "aspirin" in findings_text else "MODERATE"
    agents.append({
        "agent": "Pharmacy Agent",
        "domain": "Medication Safety",
        "risk": pharmacy_risk,
        "confidence": 0.91,
        "opinion": "Medication profile indicates elevated safety risk.",
        "recommendation": "Immediate medication reconciliation and bleeding-risk review."
    })

    cardiology_risk = "CRITICAL" if "troponin" in findings_text or "coronary" in reasoning_text else "MODERATE"
    agents.append({
        "agent": "Cardiology Agent",
        "domain": "Cardiology",
        "risk": cardiology_risk,
        "confidence": 0.94,
        "opinion": "Possible acute cardiac injury or ACS pathway activation needed.",
        "recommendation": "Urgent ECG, repeat troponin, and cardiology review."
    })

    nephrology_risk = "HIGH" if any(x in findings_text + reasoning_text for x in ["creatinine", "potassium", "kidney"]) else "LOW"
    agents.append({
        "agent": "Nephrology Agent",
        "domain": "Renal",
        "risk": nephrology_risk,
        "confidence": 0.88,
        "opinion": "Renal impairment or electrolyte disturbance suspected.",
        "recommendation": "Repeat renal function, potassium, eGFR, and monitor fluid balance."
    })

    icu_risk = "CRITICAL" if escalation_level in ["ICU", "EMERGENCY_RESPONSE"] else "MODERATE"
    agents.append({
        "agent": "ICU Agent",
        "domain": "Critical Care",
        "risk": icu_risk,
        "confidence": 0.90,
        "opinion": f"Escalation level is {escalation_level}.",
        "recommendation": "Assess monitored bed / ICU eligibility."
    })

    emergency_risk = "CRITICAL" if escalation_level == "EMERGENCY_RESPONSE" else "HIGH" if escalation_level == "ICU" else "MODERATE"
    agents.append({
        "agent": "Emergency Agent",
        "domain": "Emergency Response",
        "risk": emergency_risk,
        "confidence": 0.92,
        "opinion": "Emergency response level derived from command brain escalation.",
        "recommendation": "Activate emergency response workflow if clinically confirmed."
    })

    return agents


def calculate_agent_consensus(agents):
    scores = [agent_risk_score(a.get("risk")) for a in agents]
    if not scores:
        return 0

    avg = sum(scores) / len(scores)
    spread = max(scores) - min(scores)

    consensus = int(max(0, min(100, avg - (spread * 0.15))))
    return consensus


def detect_agent_conflicts(agents):
    risks = {a.get("agent"): a.get("risk") for a in agents}
    scores = {name: agent_risk_score(level) for name, level in risks.items()}

    conflicts = []
    for a, score_a in scores.items():
        for b, score_b in scores.items():
            if a >= b:
                continue
            if abs(score_a - score_b) >= 50:
                conflicts.append({
                    "agent_a": a,
                    "risk_a": risks[a],
                    "agent_b": b,
                    "risk_b": risks[b],
                    "gap": abs(score_a - score_b)
                })

    return conflicts


@router.get("/agents/{patient_id}")
def multi_agent_medical_command(patient_id: str):
    agents = build_medical_agents(patient_id)
    consensus_score = calculate_agent_consensus(agents)
    conflicts = detect_agent_conflicts(agents)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.4 Multi-Agent Medical Command System",
        "patient_id": patient_id,
        "active_agents": len(agents),
        "agents": agents,
        "consensus_score": consensus_score,
        "conflict_detected": len(conflicts) > 0,
        "conflicts": conflicts,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/consensus/{patient_id}")
def agent_consensus(patient_id: str):
    agent_result = multi_agent_medical_command(patient_id)
    agents = agent_result.get("agents", [])
    consensus_score = agent_result.get("consensus_score", 0)

    final_risk = "CRITICAL" if any(a.get("risk") == "CRITICAL" for a in agents) else "HIGH"

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.4 Agent Consensus",
        "patient_id": patient_id,
        "consensus_score": consensus_score,
        "agreement": "HIGH" if consensus_score >= 80 else "MODERATE" if consensus_score >= 60 else "LOW",
        "final_risk": final_risk,
        "agent_count": len(agents),
        "top_agents": [a for a in agents if a.get("risk") in ["HIGH", "CRITICAL"]],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/conflicts/{patient_id}")
def agent_conflicts(patient_id: str):
    agent_result = multi_agent_medical_command(patient_id)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.4 Conflict Detection",
        "patient_id": patient_id,
        "conflict_detected": agent_result.get("conflict_detected"),
        "conflicts": agent_result.get("conflicts", []),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/final-command/{patient_id}")
def final_agent_command(patient_id: str):
    decision_response = unified_medical_decision(patient_id)
    escalation_response = autonomous_escalation(patient_id)
    consensus_response = agent_consensus(patient_id)

    decision = decision_response.get("unified_medical_decision", {})

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.4 Final Multi-Agent Command",
        "patient_id": patient_id,
        "final_risk": consensus_response.get("final_risk"),
        "consensus_score": consensus_response.get("consensus_score"),
        "recommended_pathway": escalation_response.get("escalation_level"),
        "final_decision": decision.get("final_decision"),
        "priority_problem": decision.get("priority_problem"),
        "required_teams": escalation_response.get("required_teams", []),
        "required_actions": escalation_response.get("required_actions", []),
        "source_engines": [
            "11.0.1 Global Patient Understanding",
            "11.0.2 Unified Medical Decision",
            "11.0.3 Autonomous Escalation Engine",
            "11.0.4 Multi-Agent Medical Command System"
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


AGENT_WEIGHTS = {
    "Cardiology Agent": 0.20,
    "ICU Agent": 0.20,
    "Laboratory Agent": 0.20,
    "Radiology Agent": 0.15,
    "Pharmacy Agent": 0.15,
    "Emergency Agent": 0.05,
    "Nephrology Agent": 0.05,
}

RISK_NUMERIC = {
    "LOW": 25,
    "MODERATE": 55,
    "HIGH": 80,
    "CRITICAL": 95,
}


def risk_to_numeric(risk):
    return RISK_NUMERIC.get(risk, 40)


def numeric_to_risk(score):
    if score >= 85:
        return "CRITICAL"
    if score >= 70:
        return "HIGH"
    if score >= 45:
        return "MODERATE"
    return "LOW"


@router.get("/consensus-vote/{patient_id}")
def consensus_vote(patient_id: str):
    agent_result = multi_agent_medical_command(patient_id)
    agents = agent_result.get("agents", [])

    votes = []
    weighted_total = 0
    total_weight = 0

    for agent in agents:
        name = agent.get("agent")
        risk = agent.get("risk")
        confidence = agent.get("confidence", 0.8)
        weight = AGENT_WEIGHTS.get(name, 0.05)
        numeric = risk_to_numeric(risk)

        weighted_value = numeric * weight * confidence

        votes.append({
            "agent": name,
            "risk_vote": risk,
            "numeric_vote": numeric,
            "confidence": confidence,
            "weight": weight,
            "weighted_value": round(weighted_value, 2)
        })

        weighted_total += weighted_value
        total_weight += weight * confidence

    final_score = int(weighted_total / total_weight) if total_weight else 0

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.5 Consensus Voting Engine",
        "patient_id": patient_id,
        "votes": votes,
        "weighted_score": final_score,
        "final_risk_vote": numeric_to_risk(final_score),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/agreement-matrix/{patient_id}")
def agreement_matrix(patient_id: str):
    agent_result = multi_agent_medical_command(patient_id)
    agents = agent_result.get("agents", [])

    matrix = {}

    for a in agents:
        row = {}
        score_a = risk_to_numeric(a.get("risk"))

        for b in agents:
            score_b = risk_to_numeric(b.get("risk"))
            gap = abs(score_a - score_b)
            agreement = max(0, 100 - gap)
            row[b.get("agent")] = agreement

        matrix[a.get("agent")] = row

    avg_agreement = 0
    count = 0

    for a, row in matrix.items():
        for b, value in row.items():
            if a != b:
                avg_agreement += value
                count += 1

    avg_agreement = int(avg_agreement / count) if count else 0

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.5 Agreement Matrix",
        "patient_id": patient_id,
        "average_agreement": avg_agreement,
        "matrix": matrix,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/conflict-resolution/{patient_id}")
def conflict_resolution(patient_id: str):
    agent_result = multi_agent_medical_command(patient_id)
    conflicts = agent_result.get("conflicts", [])
    agents = agent_result.get("agents", [])

    if not conflicts:
        return {
            "status": "success",
            "stage": "AI Hospital Alliance 11.0",
            "module": "11.0.5 Conflict Resolution Engine",
            "patient_id": patient_id,
            "conflict_detected": False,
            "resolution": "No major conflict detected. Agent opinions are clinically aligned.",
            "dominant_agents": [
                a.get("agent") for a in agents
                if a.get("risk") in ["HIGH", "CRITICAL"]
            ],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    dominant = sorted(
        agents,
        key=lambda a: (risk_to_numeric(a.get("risk")) * a.get("confidence", 0.8)),
        reverse=True
    )[:3]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.5 Conflict Resolution Engine",
        "patient_id": patient_id,
        "conflict_detected": True,
        "conflicts": conflicts,
        "resolution": "Higher-risk, higher-confidence specialist agents dominate final consensus.",
        "dominant_agents": [a.get("agent") for a in dominant],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/final-consensus/{patient_id}")
def final_clinical_consensus(patient_id: str):
    vote = consensus_vote(patient_id)
    matrix = agreement_matrix(patient_id)
    resolution = conflict_resolution(patient_id)
    final_command = final_agent_command(patient_id)

    weighted_score = vote.get("weighted_score", 0)
    avg_agreement = matrix.get("average_agreement", 0)

    consensus_score = int((weighted_score * 0.6) + (avg_agreement * 0.4))

    confidence = round(min(0.98, max(0.50, consensus_score / 100)), 2)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.5 Final Clinical Consensus Engine",
        "patient_id": patient_id,
        "consensus_score": consensus_score,
        "agreement": "VERY_HIGH" if consensus_score >= 90 else "HIGH" if consensus_score >= 80 else "MODERATE",
        "conflict_detected": resolution.get("conflict_detected"),
        "final_risk": vote.get("final_risk_vote"),
        "recommended_pathway": final_command.get("recommended_pathway"),
        "priority_problem": final_command.get("priority_problem"),
        "confidence": confidence,
        "required_teams": final_command.get("required_teams", []),
        "required_actions": final_command.get("required_actions", []),
        "source_engines": [
            "11.0.4 Multi-Agent Medical Command System",
            "11.0.5 Consensus Voting",
            "11.0.5 Agreement Matrix",
            "11.0.5 Conflict Resolution"
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/consensus-dashboard")
def consensus_dashboard():
    patient_ids = ["P-1001"]
    results = [final_clinical_consensus(pid) for pid in patient_ids]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.5 Clinical Consensus Dashboard",
        "total_patients": len(results),
        "very_high_consensus": len([r for r in results if r.get("agreement") == "VERY_HIGH"]),
        "high_consensus": len([r for r in results if r.get("agreement") == "HIGH"]),
        "critical_patients": len([r for r in results if r.get("final_risk") == "CRITICAL"]),
        "conflicted_patients": len([r for r in results if r.get("conflict_detected")]),
        "patients": results,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/command-summary/{patient_id}")
def command_summary(patient_id: str):
    brain = global_patient_understanding(patient_id)
    decision = unified_medical_decision(patient_id)
    escalation = autonomous_escalation(patient_id)
    agents = multi_agent_medical_command(patient_id)
    consensus = final_clinical_consensus(patient_id)

    final = consensus

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Executive Command Summary Engine",
        "patient_id": patient_id,
        "overall_risk": final.get("final_risk"),
        "main_diagnosis": final.get("priority_problem"),
        "consensus_score": final.get("consensus_score"),
        "agreement": final.get("agreement"),
        "confidence": final.get("confidence"),
        "recommended_pathway": final.get("recommended_pathway"),
        "command_status": brain.get("command_status"),
        "decision_level": decision.get("unified_medical_decision", {}).get("decision_level"),
        "escalation_level": escalation.get("escalation_level"),
        "active_agents": agents.get("active_agents"),
        "required_teams": final.get("required_teams", []),
        "priority_actions": final.get("required_actions", [])[:8],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/executive-brief/{patient_id}")
def executive_brief(patient_id: str):
    summary = command_summary(patient_id)

    brief = (
        f"Patient {patient_id} is classified as {summary.get('overall_risk')} risk. "
        f"The primary problem is {summary.get('main_diagnosis')}. "
        f"Clinical consensus is {summary.get('consensus_score')}% with "
        f"{summary.get('agreement')} agreement. "
        f"Recommended pathway is {summary.get('recommended_pathway')}. "
        f"Immediate teams required: {', '.join(summary.get('required_teams', []))}."
    )

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Executive Brief Engine",
        "patient_id": patient_id,
        "brief_30_seconds": brief,
        "headline": f"{summary.get('overall_risk')} — {summary.get('main_diagnosis')}",
        "recommended_pathway": summary.get("recommended_pathway"),
        "consensus_score": summary.get("consensus_score"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/clinical-report/{patient_id}")
def clinical_report(patient_id: str):
    brain = global_patient_understanding(patient_id)
    final = final_clinical_consensus(patient_id)
    brief = executive_brief(patient_id)

    understanding = brain.get("global_patient_understanding", {})

    report = {
        "executive_brief": brief.get("brief_30_seconds"),
        "overall_risk": final.get("final_risk"),
        "priority_problem": final.get("priority_problem"),
        "recommended_pathway": final.get("recommended_pathway"),
        "consensus_score": final.get("consensus_score"),
        "confidence": final.get("confidence"),
        "timeline_summary": {
            "timeline_events": understanding.get("timeline_events"),
            "critical_events": understanding.get("critical_events"),
            "warning_events": understanding.get("warning_events"),
            "normal_events": understanding.get("normal_events")
        },
        "key_findings": understanding.get("key_findings", []),
        "clinical_reasoning": understanding.get("clinical_reasoning", []),
        "care_plan": understanding.get("care_plan", {}),
        "outcome_prediction": understanding.get("outcome_prediction", {}),
        "required_teams": final.get("required_teams", []),
        "required_actions": final.get("required_actions", [])
    }

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Clinical Report Generator",
        "patient_id": patient_id,
        "clinical_report": report,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/action-board/{patient_id}")
def action_board(patient_id: str):
    summary = command_summary(patient_id)

    actions = []
    for i, action in enumerate(summary.get("priority_actions", []), start=1):
        actions.append({
            "id": f"ACT-{i:03d}",
            "priority": "IMMEDIATE" if i <= 3 else "URGENT",
            "action": action,
            "status": "OPEN"
        })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Action Board",
        "patient_id": patient_id,
        "recommended_pathway": summary.get("recommended_pathway"),
        "total_actions": len(actions),
        "actions": actions,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/critical-patients")
def critical_patients():
    patient_ids = ["P-1001"]

    patients = []
    for pid in patient_ids:
        summary = command_summary(pid)
        if summary.get("overall_risk") in ["CRITICAL", "HIGH"]:
            patients.append(summary)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Critical Patients Registry",
        "count": len(patients),
        "patients": patients,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/executive-dashboard")
def executive_dashboard():
    patient_ids = ["P-1001"]
    summaries = [command_summary(pid) for pid in patient_ids]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.6 Hospital Executive Dashboard",
        "total_patients": len(summaries),
        "critical_patients": len([s for s in summaries if s.get("overall_risk") == "CRITICAL"]),
        "emergency_pathway": len([s for s in summaries if s.get("recommended_pathway") == "EMERGENCY_RESPONSE"]),
        "average_consensus": int(sum(s.get("consensus_score", 0) for s in summaries) / len(summaries)) if summaries else 0,
        "patients": summaries,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/hospital-overview")
def hospital_overview():
    patient_ids = ["P-1001"]
    summaries = [command_summary(pid) for pid in patient_ids]

    critical = [s for s in summaries if s.get("overall_risk") == "CRITICAL"]
    emergency = [s for s in summaries if s.get("recommended_pathway") == "EMERGENCY_RESPONSE"]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Hospital Overview Engine",
        "total_patients": len(summaries),
        "critical_patients": len(critical),
        "emergency_pathway_patients": len(emergency),
        "average_consensus": int(sum(s.get("consensus_score", 0) for s in summaries) / len(summaries)) if summaries else 0,
        "hospital_status": "CRITICAL_LOAD" if emergency else "STABLE",
        "patients": summaries,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/resource-pressure")
def resource_pressure():
    overview = hospital_overview()

    emergency_count = overview.get("emergency_pathway_patients", 0)
    critical_count = overview.get("critical_patients", 0)

    pressure_score = min(100, emergency_count * 45 + critical_count * 35)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Resource Pressure Engine",
        "pressure_score": pressure_score,
        "pressure_level": "HIGH" if pressure_score >= 70 else "MODERATE" if pressure_score >= 35 else "LOW",
        "icu_pressure": "HIGH" if emergency_count > 0 else "LOW",
        "emergency_pressure": "HIGH" if emergency_count > 0 else "LOW",
        "staffing_pressure": "MODERATE" if critical_count > 0 else "LOW",
        "recommendations": [
            "Prepare ICU / monitored bed availability.",
            "Notify emergency response leadership.",
            "Review cardiology and nephrology availability.",
            "Prioritize critical patient action board."
        ] if pressure_score >= 35 else [
            "Maintain routine hospital monitoring."
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/icu-overview")
def icu_overview():
    patient_ids = ["P-1001"]
    candidates = []

    for pid in patient_ids:
        summary = command_summary(pid)
        if summary.get("recommended_pathway") in ["ICU", "EMERGENCY_RESPONSE"]:
            candidates.append(summary)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 ICU Overview",
        "icu_candidates": len(candidates),
        "estimated_required_beds": len(candidates),
        "icu_status": "ACTIVATE_REVIEW" if candidates else "STABLE",
        "patients": candidates,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/emergency-load")
def emergency_load():
    patient_ids = ["P-1001"]
    emergency_patients = []

    for pid in patient_ids:
        summary = command_summary(pid)
        if summary.get("recommended_pathway") == "EMERGENCY_RESPONSE":
            emergency_patients.append(summary)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Emergency Load Engine",
        "emergency_patients": len(emergency_patients),
        "load_level": "HIGH" if emergency_patients else "LOW",
        "response_status": "EMERGENCY_RESPONSE_REQUIRED" if emergency_patients else "NORMAL_OPERATIONS",
        "patients": emergency_patients,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/high-risk-patients")
def high_risk_patients():
    patient_ids = ["P-1001"]
    patients = []

    for pid in patient_ids:
        summary = command_summary(pid)
        if summary.get("overall_risk") in ["CRITICAL", "HIGH"]:
            patients.append(summary)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 High Risk Patient Registry",
        "count": len(patients),
        "patients": patients,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/active-alerts")
def active_alerts():
    patient_ids = ["P-1001"]
    alerts = []

    for pid in patient_ids:
        summary = command_summary(pid)

        if summary.get("overall_risk") == "CRITICAL":
            alerts.append({
                "id": f"ALERT-{pid}-CRITICAL",
                "patient_id": pid,
                "level": "CRITICAL",
                "message": f"Critical patient detected: {summary.get('main_diagnosis')}",
                "pathway": summary.get("recommended_pathway"),
                "teams": summary.get("required_teams", [])
            })

        if summary.get("recommended_pathway") == "EMERGENCY_RESPONSE":
            alerts.append({
                "id": f"ALERT-{pid}-EMERGENCY",
                "patient_id": pid,
                "level": "EMERGENCY",
                "message": "Emergency response pathway recommended.",
                "pathway": "EMERGENCY_RESPONSE",
                "teams": summary.get("required_teams", [])
            })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Active Alerts Engine",
        "active_alerts": len(alerts),
        "alerts": alerts,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/bed-management")
def bed_management():
    icu = icu_overview()
    emergency = emergency_load()

    required_icu_beds = icu.get("estimated_required_beds", 0)
    emergency_patients = emergency.get("emergency_patients", 0)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Bed Management Engine",
        "required_icu_beds": required_icu_beds,
        "required_monitored_beds": required_icu_beds + emergency_patients,
        "bed_pressure": "HIGH" if required_icu_beds > 0 else "LOW",
        "recommendations": [
            "Reserve monitored/ICU bed for critical pathway patient.",
            "Prepare transfer workflow if ICU admission confirmed.",
            "Notify bed manager and charge nurse."
        ] if required_icu_beds > 0 else [
            "No immediate critical bed requirement detected."
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/hospital-command-dashboard")
def hospital_command_dashboard():
    overview = hospital_overview()
    pressure = resource_pressure()
    icu = icu_overview()
    emergency = emergency_load()
    high_risk = high_risk_patients()
    alerts = active_alerts()
    beds = bed_management()

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.7 Hospital Command Center",
        "hospital_status": overview.get("hospital_status"),
        "overview": overview,
        "resource_pressure": pressure,
        "icu_overview": icu,
        "emergency_load": emergency,
        "high_risk_patients": high_risk,
        "active_alerts": alerts,
        "bed_management": beds,
        "command_recommendation": "Activate hospital command review." if alerts.get("active_alerts", 0) > 0 else "Continue routine monitoring.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/global-alert-stream")
def global_alert_stream():
    alerts = active_alerts()
    pressure = resource_pressure()
    beds = bed_management()
    emergency = emergency_load()

    stream = []

    for alert in alerts.get("alerts", []):
        stream.append({
            "id": alert.get("id"),
            "type": "CLINICAL_ALERT",
            "level": alert.get("level"),
            "message": alert.get("message"),
            "patient_id": alert.get("patient_id"),
            "pathway": alert.get("pathway"),
            "teams": alert.get("teams", []),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    if pressure.get("pressure_level") == "HIGH":
        stream.append({
            "id": "ALERT-HOSPITAL-PRESSURE",
            "type": "RESOURCE_ALERT",
            "level": "HIGH",
            "message": "Hospital resource pressure is HIGH.",
            "pressure_score": pressure.get("pressure_score"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    if beds.get("bed_pressure") == "HIGH":
        stream.append({
            "id": "ALERT-BED-PRESSURE",
            "type": "BED_ALERT",
            "level": "HIGH",
            "message": "ICU / monitored bed pressure detected.",
            "required_icu_beds": beds.get("required_icu_beds"),
            "required_monitored_beds": beds.get("required_monitored_beds"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    if emergency.get("response_status") == "EMERGENCY_RESPONSE_REQUIRED":
        stream.append({
            "id": "ALERT-EMERGENCY-RESPONSE",
            "type": "EMERGENCY_ALERT",
            "level": "EMERGENCY",
            "message": "Emergency response workflow required.",
            "emergency_patients": emergency.get("emergency_patients"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Global Alert Stream",
        "total_alerts": len(stream),
        "alerts": stream,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/critical-alert-registry")
def critical_alert_registry():
    stream = global_alert_stream()
    critical = [
        a for a in stream.get("alerts", [])
        if a.get("level") in ["CRITICAL", "EMERGENCY", "HIGH"]
    ]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Critical Alert Registry",
        "count": len(critical),
        "alerts": critical,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/alert-prioritization")
def alert_prioritization():
    stream = global_alert_stream()

    priority_score = {
        "EMERGENCY": 100,
        "CRITICAL": 90,
        "HIGH": 75,
        "MODERATE": 50,
        "LOW": 25
    }

    alerts = sorted(
        stream.get("alerts", []),
        key=lambda a: priority_score.get(a.get("level"), 0),
        reverse=True
    )

    for i, alert in enumerate(alerts, start=1):
        alert["priority_rank"] = i
        alert["priority_score"] = priority_score.get(alert.get("level"), 0)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Alert Prioritization Engine",
        "count": len(alerts),
        "prioritized_alerts": alerts,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/hospital-surveillance")
def hospital_surveillance():
    overview = hospital_overview()
    pressure = resource_pressure()
    alerts = global_alert_stream()
    beds = bed_management()
    icu = icu_overview()
    emergency = emergency_load()

    risk_level = "CRITICAL" if overview.get("hospital_status") == "CRITICAL_LOAD" else "STABLE"

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Hospital Surveillance System",
        "surveillance_status": "ACTIVE",
        "hospital_risk_level": risk_level,
        "hospital_status": overview.get("hospital_status"),
        "resource_pressure": pressure.get("pressure_level"),
        "bed_pressure": beds.get("bed_pressure"),
        "icu_candidates": icu.get("icu_candidates"),
        "emergency_patients": emergency.get("emergency_patients"),
        "active_alerts": alerts.get("total_alerts"),
        "recommendation": "Maintain command center active monitoring." if risk_level == "CRITICAL" else "Routine surveillance.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/resource-warning-system")
def resource_warning_system():
    pressure = resource_pressure()
    beds = bed_management()
    icu = icu_overview()

    warnings = []

    if pressure.get("pressure_level") == "HIGH":
        warnings.append("High hospital resource pressure detected.")

    if beds.get("bed_pressure") == "HIGH":
        warnings.append("ICU / monitored bed pressure detected.")

    if icu.get("icu_candidates", 0) > 0:
        warnings.append("ICU candidate requires bed review.")

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Resource Warning System",
        "warning_count": len(warnings),
        "warnings": warnings,
        "resource_pressure": pressure,
        "bed_management": beds,
        "icu_overview": icu,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/icu-saturation-alerts")
def icu_saturation_alerts():
    icu = icu_overview()
    beds = bed_management()

    saturation_level = "HIGH" if icu.get("icu_candidates", 0) > 0 else "LOW"

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 ICU Saturation Alerts",
        "saturation_level": saturation_level,
        "icu_candidates": icu.get("icu_candidates"),
        "required_icu_beds": beds.get("required_icu_beds"),
        "alert": "ICU review and bed reservation required." if saturation_level == "HIGH" else "No ICU saturation signal detected.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/emergency-broadcast")
def emergency_broadcast():
    emergency = emergency_load()
    alerts = critical_alert_registry()

    should_broadcast = emergency.get("emergency_patients", 0) > 0

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Emergency Response Broadcast",
        "broadcast_required": should_broadcast,
        "broadcast_level": "EMERGENCY" if should_broadcast else "NONE",
        "message": "Emergency response required for critical patient pathway." if should_broadcast else "No emergency broadcast required.",
        "targets": [
            "Emergency Response Team",
            "ICU Team",
            "Cardiology",
            "Nursing Supervisor",
            "Bed Manager"
        ] if should_broadcast else [],
        "alerts": alerts.get("alerts", []),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/executive-alert-feed")
def executive_alert_feed():
    surveillance = hospital_surveillance()
    priority = alert_prioritization()
    broadcast = emergency_broadcast()

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Executive Alert Feed",
        "headline": f"Hospital status: {surveillance.get('hospital_status')}",
        "hospital_risk_level": surveillance.get("hospital_risk_level"),
        "top_alerts": priority.get("prioritized_alerts", [])[:5],
        "broadcast_required": broadcast.get("broadcast_required"),
        "executive_message": "Immediate hospital command review recommended." if broadcast.get("broadcast_required") else "No immediate executive escalation.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/global-alert-dashboard")
def global_alert_dashboard():
    stream = global_alert_stream()
    registry = critical_alert_registry()
    priority = alert_prioritization()
    surveillance = hospital_surveillance()
    resource = resource_warning_system()
    icu_alerts = icu_saturation_alerts()
    broadcast = emergency_broadcast()
    executive = executive_alert_feed()

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.8 Global Alerts & Hospital Surveillance System",
        "alert_summary": {
            "total_alerts": stream.get("total_alerts"),
            "critical_alerts": registry.get("count"),
            "broadcast_required": broadcast.get("broadcast_required"),
            "hospital_risk_level": surveillance.get("hospital_risk_level")
        },
        "global_alert_stream": stream,
        "critical_alert_registry": registry,
        "alert_prioritization": priority,
        "hospital_surveillance": surveillance,
        "resource_warning_system": resource,
        "icu_saturation_alerts": icu_alerts,
        "emergency_broadcast": broadcast,
        "executive_alert_feed": executive,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/bed-allocation")
def bed_allocation():
    beds = bed_management()
    high_risk = high_risk_patients()
    alerts = global_alert_stream()

    required_icu = beds.get("required_icu_beds", 0)
    required_monitored = beds.get("required_monitored_beds", 0)

    allocations = []

    for patient in high_risk.get("patients", []):
        patient_id = patient.get("patient_id")
        pathway = patient.get("recommended_pathway")

        bed_type = "ICU" if pathway == "EMERGENCY_RESPONSE" else "MONITORED_BED"

        allocations.append({
            "patient_id": patient_id,
            "bed_type": bed_type,
            "priority": "IMMEDIATE" if pathway == "EMERGENCY_RESPONSE" else "URGENT",
            "reason": patient.get("main_diagnosis"),
            "status": "PENDING_CONFIRMATION"
        })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Bed Allocation Engine",
        "required_icu_beds": required_icu,
        "required_monitored_beds": required_monitored,
        "active_alerts": alerts.get("total_alerts"),
        "allocations": allocations,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/icu-capacity")
def icu_capacity():
    icu = icu_overview()
    beds = bed_management()

    total_icu_beds = 20
    occupied_icu_beds = 14
    required_icu_beds = beds.get("required_icu_beds", 0)
    projected_occupied = occupied_icu_beds + required_icu_beds

    occupancy_rate = round(projected_occupied / total_icu_beds, 2)

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 ICU Capacity Manager",
        "total_icu_beds": total_icu_beds,
        "occupied_icu_beds": occupied_icu_beds,
        "required_icu_beds": required_icu_beds,
        "projected_occupied": projected_occupied,
        "occupancy_rate": occupancy_rate,
        "capacity_status": "HIGH_PRESSURE" if occupancy_rate >= 0.75 else "AVAILABLE",
        "icu_candidates": icu.get("icu_candidates"),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/emergency-queue")
def emergency_queue():
    emergency = emergency_load()
    priority = alert_prioritization()

    queue = []

    for alert in priority.get("prioritized_alerts", []):
        if alert.get("level") in ["EMERGENCY", "CRITICAL"]:
            queue.append({
                "queue_id": f"ERQ-{len(queue)+1:03d}",
                "patient_id": alert.get("patient_id", "HOSPITAL"),
                "level": alert.get("level"),
                "message": alert.get("message"),
                "priority_score": alert.get("priority_score"),
                "status": "WAITING_FOR_TEAM_ACKNOWLEDGEMENT"
            })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Emergency Queue Manager",
        "emergency_patients": emergency.get("emergency_patients"),
        "queue_length": len(queue),
        "queue": queue,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/or-scheduler")
def operating_room_scheduler():
    alerts = global_alert_stream()

    emergency_or_needed = any(
        a.get("level") == "EMERGENCY" for a in alerts.get("alerts", [])
    )

    schedule = []

    if emergency_or_needed:
        schedule.append({
            "or_id": "OR-EMERGENCY-01",
            "status": "RESERVE",
            "priority": "EMERGENCY",
            "reason": "Emergency response pathway active",
            "team": "Emergency Surgical / Critical Care Team"
        })

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Operating Room Scheduler",
        "emergency_or_needed": emergency_or_needed,
        "reserved_rooms": len(schedule),
        "schedule": schedule,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/staff-load")
def staff_load():
    alerts = global_alert_stream()
    pressure = resource_pressure()

    active_alerts_count = alerts.get("total_alerts", 0)
    pressure_level = pressure.get("pressure_level")

    staff_units = [
        {
            "unit": "Emergency",
            "load": "HIGH" if active_alerts_count > 0 else "LOW",
            "recommended_action": "Assign emergency response team."
        },
        {
            "unit": "ICU",
            "load": "HIGH" if pressure_level == "HIGH" else "MODERATE",
            "recommended_action": "Prepare ICU review and bed manager."
        },
        {
            "unit": "Cardiology",
            "load": "HIGH",
            "recommended_action": "Immediate cardiology availability required."
        },
        {
            "unit": "Nephrology",
            "load": "MODERATE",
            "recommended_action": "Review renal/electrolyte status."
        },
        {
            "unit": "Clinical Pharmacy",
            "load": "MODERATE",
            "recommended_action": "Medication safety review."
        }
    ]

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Staff Load Balancer",
        "overall_staff_pressure": "HIGH" if active_alerts_count > 0 else "LOW",
        "staff_units": staff_units,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/resource-distribution")
def resource_distribution():
    capacity = icu_capacity()
    beds = bed_allocation()
    staff = staff_load()
    emergency = emergency_queue()

    resources = {
        "icu_beds": {
            "required": capacity.get("required_icu_beds"),
            "available_estimate": max(0, capacity.get("total_icu_beds", 0) - capacity.get("projected_occupied", 0)),
            "status": capacity.get("capacity_status")
        },
        "monitored_beds": {
            "required": beds.get("required_monitored_beds"),
            "status": "ALLOCATE" if beds.get("required_monitored_beds", 0) > 0 else "STABLE"
        },
        "staff": staff.get("staff_units", []),
        "emergency_queue": emergency.get("queue_length")
    }

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Resource Distribution Engine",
        "resources": resources,
        "recommendation": "Prioritize ICU bed and emergency team allocation." if emergency.get("queue_length", 0) > 0 else "Routine distribution.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/hospital-kpis")
def hospital_kpis():
    overview = hospital_overview()
    alerts = global_alert_stream()
    capacity = icu_capacity()
    emergency = emergency_queue()
    pressure = resource_pressure()

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Hospital KPI Engine",
        "kpis": {
            "total_patients": overview.get("total_patients"),
            "critical_patients": overview.get("critical_patients"),
            "emergency_pathway_patients": overview.get("emergency_pathway_patients"),
            "active_alerts": alerts.get("total_alerts"),
            "icu_occupancy_rate": capacity.get("occupancy_rate"),
            "emergency_queue_length": emergency.get("queue_length"),
            "resource_pressure_score": pressure.get("pressure_score"),
            "average_consensus": overview.get("average_consensus")
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }


@router.get("/operations-dashboard")
def operations_dashboard():
    bed_alloc = bed_allocation()
    icu = icu_capacity()
    er = emergency_queue()
    ors = operating_room_scheduler()
    staff = staff_load()
    distribution = resource_distribution()
    kpis = hospital_kpis()

    return {
        "status": "success",
        "stage": "AI Hospital Alliance 11.0",
        "module": "11.0.9 Autonomous Hospital Operations Center",
        "operations_status": "ACTIVE_COMMAND" if kpis.get("kpis", {}).get("active_alerts", 0) > 0 else "NORMAL",
        "bed_allocation": bed_alloc,
        "icu_capacity": icu,
        "emergency_queue": er,
        "operating_room_scheduler": ors,
        "staff_load": staff,
        "resource_distribution": distribution,
        "hospital_kpis": kpis,
        "command_recommendation": "Activate hospital operations command review." if kpis.get("kpis", {}).get("active_alerts", 0) > 0 else "Continue routine operations.",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
