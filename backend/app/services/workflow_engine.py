from typing import Dict, Any
from ..services.clinical_rules import evaluate_chest_pain, evaluate_shortness_of_breath
from ..services.order_engine import chest_pain_orders, shortness_of_breath_orders


def run_clinical_workflow(payload: Dict[str, Any]) -> Dict[str, Any]:
    chief = (payload.get("chief_complaint") or "").strip().lower()
    symptoms = [s.lower() for s in payload.get("symptoms", [])]

    if "chest pain" in chief or "chest pain" in symptoms:
        assessment = evaluate_chest_pain(payload)
        triage = assessment["triage_level"]

        route_to = ["Emergency", "Cardiology"] if triage in ["urgent", "critical"] else ["Internal Medicine"]
        next_actions = [
            "Immediate physician review",
            "Place patient on monitor",
            "Prepare suggested orders for approval",
        ]

        if triage == "critical":
            next_actions.insert(0, "Escalate immediately to emergency team")

        return {
            "chief_complaint": payload.get("chief_complaint"),
            "triage_level": triage,
            "urgency_score": assessment["urgency_score"],
            "route_to": route_to,
            "suggested_orders": chest_pain_orders(triage),
            "red_flags": assessment["red_flags"],
            "next_actions": next_actions,
            "rationale": assessment["rationale"],
        }

    if (
        "shortness of breath" in chief
        or "shortness of breath" in symptoms
        or "dyspnea" in chief
        or "dyspnea" in symptoms
    ):
        assessment = evaluate_shortness_of_breath(payload)
        triage = assessment["triage_level"]

        route_to = ["Emergency", "Pulmonology"] if triage in ["urgent", "critical"] else ["Internal Medicine"]
        next_actions = [
            "Immediate respiratory assessment",
            "Check oxygen support need",
            "Prepare suggested orders for approval",
        ]

        if triage == "critical":
            next_actions.insert(0, "Escalate immediately to emergency team")

        return {
            "chief_complaint": payload.get("chief_complaint"),
            "triage_level": triage,
            "urgency_score": assessment["urgency_score"],
            "route_to": route_to,
            "suggested_orders": shortness_of_breath_orders(triage),
            "red_flags": assessment["red_flags"],
            "next_actions": next_actions,
            "rationale": assessment["rationale"],
        }

    return {
        "chief_complaint": payload.get("chief_complaint"),
        "triage_level": "low",
        "urgency_score": 0,
        "route_to": ["General Triage"],
        "suggested_orders": [],
        "red_flags": [],
        "next_actions": ["Standard triage assessment"],
        "rationale": ["No specialized workflow matched."],
    }
