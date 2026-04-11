from typing import List, Dict, Any


HIGH_RISK_CHEST_PAIN_SIGNS = {
    "sweating",
    "diaphoresis",
    "nausea",
    "shortness of breath",
    "radiating pain",
    "jaw pain",
    "left arm pain",
    "dizziness",
    "syncope",
}


def normalize_text(items: List[str]) -> List[str]:
    return [i.strip().lower() for i in items if i and i.strip()]


def evaluate_chest_pain(payload: Dict[str, Any]) -> Dict[str, Any]:
    chief = (payload.get("chief_complaint") or "").strip().lower()
    symptoms = set(normalize_text(payload.get("symptoms", [])))
    age = payload.get("age")
    vitals = payload.get("vitals") or {}

    score = 0
    rationale = []
    red_flags = []

    if "chest pain" in chief or "chest pain" in symptoms:
        score += 3
        rationale.append("Chest pain identified as main complaint.")

    matched_risk = symptoms.intersection(HIGH_RISK_CHEST_PAIN_SIGNS)
    if matched_risk:
        score += len(matched_risk)
        rationale.append(f"High-risk associated symptoms present: {', '.join(sorted(matched_risk))}.")
        red_flags.extend(sorted(matched_risk))

    if age and age >= 40:
        score += 1
        rationale.append("Age 40 or above increases cardiac risk context.")

    hr = vitals.get("hr")
    spo2 = vitals.get("spo2")
    bp = (vitals.get("bp") or "").strip()

    if hr and hr >= 110:
        score += 2
        rationale.append("Tachycardia detected.")
        red_flags.append("tachycardia")

    if spo2 and spo2 < 94:
        score += 2
        rationale.append("Low oxygen saturation detected.")
        red_flags.append("low oxygen saturation")

    if bp:
        try:
            systolic = int(bp.split("/")[0])
            if systolic < 90:
                score += 3
                rationale.append("Hypotension detected.")
                red_flags.append("hypotension")
        except Exception:
            pass

    if score >= 8:
        triage = "critical"
    elif score >= 5:
        triage = "urgent"
    else:
        triage = "moderate"

    return {
        "triage_level": triage,
        "urgency_score": score,
        "red_flags": sorted(set(red_flags)),
        "rationale": rationale,
    }
