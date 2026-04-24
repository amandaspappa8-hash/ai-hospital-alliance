import os, json, httpx
from typing import Dict, Any
from ..services.clinical_rules import evaluate_chest_pain, evaluate_shortness_of_breath
from ..services.order_engine import chest_pain_orders, shortness_of_breath_orders

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

def ask_groq(prompt: str) -> dict:
    key = os.environ.get("GROQ_API_KEY", "")
    if not key:
        return {}
    try:
        res = httpx.post(
            GROQ_URL,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": "You are an expert clinical AI. Respond ONLY with valid JSON, no markdown."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.3,
            },
            timeout=20.0
        )
        text = res.json()["choices"][0]["message"]["content"]
        text = text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(text)
    except Exception as e:
        print(f"Groq error: {e}")
        return {}

def run_clinical_workflow(payload: Dict[str, Any]) -> Dict[str, Any]:
    chief = (payload.get("chief_complaint") or "").strip().lower()
    symptoms = [s.lower() for s in payload.get("symptoms", [])]

    # Try Groq AI first
    groq_key = os.environ.get("GROQ_API_KEY", "")
    if groq_key:
        prompt = f"""Clinical triage for:
Chief complaint: {payload.get('chief_complaint', '')}
Symptoms: {', '.join(payload.get('symptoms', []))}
Age: {payload.get('age', 'unknown')} Gender: {payload.get('gender', 'unknown')}

Return JSON with these exact keys:
{{
  "triage_level": "critical|urgent|semi-urgent|low",
  "urgency_score": 0-10,
  "route_to": ["dept1", "dept2"],
  "suggested_orders": [{{"name": "...", "priority": "stat|urgent|routine", "category": "Lab|Imaging|Medication|Consult"}}],
  "red_flags": ["flag1"],
  "next_actions": ["action1"],
  "rationale": ["reason1"]
}}"""
        ai_result = ask_groq(prompt)
        if ai_result and "triage_level" in ai_result:
            ai_result["chief_complaint"] = payload.get("chief_complaint")
            return ai_result

    # Fallback to rules
    if "chest pain" in chief or "chest pain" in symptoms:
        assessment = evaluate_chest_pain(payload)
        triage = assessment["triage_level"]
        route_to = ["Emergency", "Cardiology"] if triage in ["urgent", "critical"] else ["Internal Medicine"]
        return {
            "chief_complaint": payload.get("chief_complaint"),
            "triage_level": triage,
            "urgency_score": assessment["urgency_score"],
            "route_to": route_to,
            "suggested_orders": chest_pain_orders(triage),
            "red_flags": assessment["red_flags"],
            "next_actions": ["Immediate physician review", "Place patient on monitor"],
            "rationale": assessment["rationale"],
        }

    if "shortness of breath" in chief or "dyspnea" in chief:
        assessment = evaluate_shortness_of_breath(payload)
        triage = assessment["triage_level"]
        route_to = ["Emergency", "Pulmonology"] if triage in ["urgent", "critical"] else ["Internal Medicine"]
        return {
            "chief_complaint": payload.get("chief_complaint"),
            "triage_level": triage,
            "urgency_score": assessment["urgency_score"],
            "route_to": route_to,
            "suggested_orders": shortness_of_breath_orders(triage),
            "red_flags": assessment["red_flags"],
            "next_actions": ["Immediate respiratory assessment"],
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
