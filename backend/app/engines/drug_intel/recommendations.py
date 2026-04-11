from typing import Any

def _build_medication_recommendations(medications: list[str], age: int | None):
    normalized = [_normalize_med_name(m) for m in medications if (m or "").strip()]
    recommendations = []

    duplicate_groups = _match_ingredient_groups(normalized)
    for ingredient, meds in duplicate_groups.items():
        recommendations.append({
            "priority": "high",
            "type": "stop_duplicate",
            "title": "Consider stopping duplicate ingredient exposure",
            "detail": f"Multiple products may contain {ingredient}: " + ", ".join(meds),
            "suggested_action": f"Review need for all {ingredient}-containing products and discontinue duplicates if clinically appropriate."
        })

    has_aspirin = any("aspirin" in med or "asa" in med for med in normalized)
    has_ibuprofen = any("ibuprofen" in med for med in normalized)
    has_warfarin = any("warfarin" in med for med in normalized)
    has_nsaid = any(_contains_any(med, NSAID_KEYWORDS) for med in normalized)

    if has_aspirin and has_ibuprofen:
        recommendations.append({
            "priority": "high",
            "type": "lower_risk_alternative",
            "title": "Consider avoiding dual NSAID exposure",
            "detail": "Aspirin and ibuprofen together may increase GI bleeding risk and reduce safety.",
            "suggested_action": "Review whether one NSAID can be discontinued or replaced with a lower-risk option depending on indication."
        })

    if has_warfarin and has_nsaid:
        recommendations.append({
            "priority": "high",
            "type": "bleeding_review",
            "title": "Immediate anticoagulant + NSAID review",
            "detail": "Warfarin with NSAIDs may significantly increase bleeding risk.",
            "suggested_action": "Consider non-NSAID pain strategy and pharmacist/physician review immediately."
        })

    for med in normalized:
        dose_mg = _extract_numeric_dose_mg(med)

        if dose_mg is not None:
            if "aspirin" in med and dose_mg >= 325:
                recommendations.append({
                    "priority": "moderate",
                    "type": "dose_review",
                    "title": "Aspirin dose review suggested",
                    "detail": f"{med} may require indication-specific confirmation.",
                    "suggested_action": "Confirm whether this is being used for analgesia, antiplatelet therapy, or another indication before continuing."
                })

            if ("acetaminophen" in med or "paracetamol" in med) and dose_mg >= 1000:
                recommendations.append({
                    "priority": "moderate",
                    "type": "dose_review",
                    "title": "High single-dose acetaminophen review",
                    "detail": f"{med} may warrant daily total dose verification.",
                    "suggested_action": "Review total 24-hour acetaminophen exposure and liver risk factors."
                })

        if _contains_any(med, RENAL_CAUTION_KEYWORDS):
            recommendations.append({
                "priority": "moderate",
                "type": "route_schedule_review",
                "title": "Renal-risk medication review",
                "detail": f"{med} may need renal function or hydration review.",
                "suggested_action": "Reassess dose, interval, and renal monitoring plan."
            })

        if _contains_any(med, HEPATIC_CAUTION_KEYWORDS):
            recommendations.append({
                "priority": "moderate",
                "type": "hepatic_review",
                "title": "Hepatic caution review",
                "detail": f"{med} may require liver-related review.",
                "suggested_action": "Reassess hepatic dose appropriateness and cumulative hepatotoxic burden."
            })

    if age is not None and age < 12 and any("aspirin" in med for med in normalized):
        recommendations.append({
            "priority": "high",
            "type": "pediatric_escalation",
            "title": "Pediatric escalation required",
            "detail": "Aspirin in pediatric patients may need urgent specialist review.",
            "suggested_action": "Escalate to physician/pharmacist and verify indication immediately."
        })

    if not recommendations:
        recommendations.append({
            "priority": "low",
            "type": "no_major_change",
            "title": "No major automated recommendation",
            "detail": "No strong automated change recommendation detected from current rule set.",
            "suggested_action": "Continue routine pharmacist review."
        })

    return {
        "age": age,
        "count": len(normalized),
        "medications": normalized,
        "recommendations": recommendations,
        "summary": {
            "has_recommendations": len(recommendations) > 0,
            "high_priority_count": len([r for r in recommendations if r["priority"] == "high"]),
            "moderate_priority_count": len([r for r in recommendations if r["priority"] == "moderate"]),
            "low_priority_count": len([r for r in recommendations if r["priority"] == "low"]),
        }
    }
