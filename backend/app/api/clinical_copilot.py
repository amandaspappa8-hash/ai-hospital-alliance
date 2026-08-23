from fastapi import APIRouter

router = APIRouter(prefix="/clinical-copilot", tags=["Sticky AI Clinical Assistant"])

@router.post("/ask")
def ask(payload: dict):
    task = payload.get("task", "summary")

    if task == "summarize":
        return {"reply": "Patient has hypertension, CAD, renal caution with eGFR 42, and medication safety review is recommended."}

    if task == "explain_labs":
        return {"reply": "Creatinine 1.4 and eGFR 42 suggest moderate renal impairment. Monitor nephrotoxic drugs."}

    if task == "suggest_orders":
        return {"reply": "Suggested orders: ECG, Troponin, Creatinine, LFT, medication interaction review."}

    if task == "medication_safety":
        return {"reply": "Review Metformin renal dosing and monitor Aspirin bleeding risk."}

    return {"reply": "Clinical Copilot ready."}
