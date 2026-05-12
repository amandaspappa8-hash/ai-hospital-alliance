from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from .deps import get_current_user, rate_limit_middleware

router = APIRouter(
    prefix="/ai/clinical-brain",
    tags=["AI Clinical Brain"],
    dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)]
)

class VitalSigns(BaseModel):
    temperature: Optional[float] = None
    bloodPressure: Optional[str] = None
    heartRate: Optional[int] = None
    respiratoryRate: Optional[int] = None
    oxygenSaturation: Optional[float] = None

class LabResult(BaseModel):
    name: str
    value: str
    unit: Optional[str] = ""
    isAbnormal: Optional[bool] = False

class ClinicalBrainRequest(BaseModel):
    patientId: str
    age: int
    gender: str
    chiefComplaint: str
    symptoms: List[str] = []
    vitals: Optional[VitalSigns] = None
    currentMedications: List[str] = []
    labResults: List[LabResult] = []
    radiologyFindings: Optional[str] = ""
    medicalHistory: Optional[str] = ""
    doctorNotes: Optional[str] = ""

@router.post("/analyze")
def clinical_brain_analyze(
    request: ClinicalBrainRequest,
    current_user: dict = Depends(get_current_user)
):
    from ..services.ai_engine import ask_ai
    import json, re

    vitals_text = ""
    if request.vitals:
        v = request.vitals
        vitals_text = f"Vitals: Temp={v.temperature}C, BP={v.bloodPressure}, HR={v.heartRate}, RR={v.respiratoryRate}, SpO2={v.oxygenSaturation}%"

    labs_text = ""
    if request.labResults:
        labs_text = "Labs: " + ", ".join([
            f"{l.name}={l.value}{l.unit}{'(ABNORMAL)' if l.isAbnormal else ''}"
            for l in request.labResults
        ])

    prompt = f"""You are a clinical AI assistant. Analyze this patient and respond ONLY with valid JSON.

Patient: {request.age}y {request.gender}, Complaint: {request.chiefComplaint}
Symptoms: {', '.join(request.symptoms)}
History: {request.medicalHistory or 'None'}
Medications: {', '.join(request.currentMedications) or 'None'}
{vitals_text}
{labs_text}
Radiology: {request.radiologyFindings or 'None'}
Notes: {request.doctorNotes or 'None'}

Respond ONLY with this JSON (no other text):
{{
  "riskScore": 75,
  "riskLevel": "High",
  "differentialDiagnosis": [
    {{"diagnosis": "Community Acquired Pneumonia", "probability": "70%", "reasoning": "Fever, cough, consolidation on CT"}},
    {{"diagnosis": "COVID-19", "probability": "20%", "reasoning": "Respiratory symptoms, low SpO2"}}
  ],
  "recommendedTreatment": ["Amoxicillin-Clavulanate 875mg BID", "Oxygen therapy", "IV fluids"],
  "drugInteractionAlerts": ["Monitor blood glucose with antibiotics in diabetic patient"],
  "criticalAlerts": ["SpO2 91% - requires oxygen supplementation"],
  "recommendedTests": ["Blood cultures", "Procalcitonin", "D-dimer"],
  "disposition": "Ward",
  "followUpPlan": "Repeat CXR in 48 hours, monitor SpO2",
  "clinicalSummary": "45yo male with signs consistent with pneumonia requiring hospital admission"
}}"""

    try:
        response = ask_ai(prompt, provider="auto")
        # محاولة استخراج JSON من الرد
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response)
        result["patientId"] = request.patientId
        result["analyzedBy"] = "AI Clinical Brain v1 (Ollama)"
        return result
    except Exception as e:
        return {
            "patientId": request.patientId,
            "analyzedBy": "AI Clinical Brain v1",
            "riskScore": 0,
            "riskLevel": "Unknown",
            "clinicalSummary": f"Analysis error: {str(e)}",
            "rawResponse": response if 'response' in locals() else "No response"
        }

@router.get("/status")
def clinical_brain_status():
    return {
        "status": "online",
        "version": "1.0.0",
        "engine": "Ollama (llama3.2:3b)",
        "capabilities": [
            "Differential Diagnosis",
            "Treatment Recommendations", 
            "Drug Interaction Detection",
            "Risk Scoring",
            "ICU/Ward Disposition",
            "Critical Alert Detection"
        ]
    }
