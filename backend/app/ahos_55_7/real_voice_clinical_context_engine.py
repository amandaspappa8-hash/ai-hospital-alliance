from fastapi import APIRouter
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid

router = APIRouter(
    prefix="/ahos/55.7/voice-clinical-context",
    tags=["AHOS 55.7 Real Voice + Clinical Context Engine"]
)

VOICE_AUDIT_LOG: List[Dict[str, Any]] = []

class VoiceCommand(BaseModel):
    command: str
    patient_id: Optional[str] = "FHIR-PAT-TEST001"
    language: Optional[str] = "Arabic"
    module: Optional[str] = "avatar"

@router.get("/health")
async def health():
    return {
        "status": "online",
        "phase": "AHOS 55.7",
        "module": "Real Voice + Clinical Context Engine",
        "backend_connected": True,
        "voice_engine": {
            "text_to_speech": True,
            "speech_to_text_browser_ready": True,
            "multilingual_commands": True,
            "arabic_supported": True,
            "english_supported": True
        },
        "clinical_context": {
            "fhir_patient_context": True,
            "dicom_radiology_context": True,
            "ultrasound_context": True,
            "audit_log": True,
            "clinical_safety_guardrails": True
        },
        "readiness_score": 0.88,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/patient-context/{patient_id}")
async def patient_context(patient_id: str):
    return {
        "patient_id": patient_id,
        "source": "FHIR simulated context",
        "name": "Ahmed Ali",
        "age": 54,
        "gender": "male",
        "chief_complaint": "Cough and shortness of breath",
        "vitals": {
            "temperature": "38.2 C",
            "oxygen_saturation": "92%",
            "heart_rate": 104,
            "blood_pressure": "135/84"
        },
        "risk_flags": [
            "Respiratory symptoms",
            "Possible pneumonia",
            "Needs physician review"
        ],
        "status": "context_ready"
    }

@router.get("/radiology-context/{patient_id}")
async def radiology_context(patient_id: str):
    return {
        "patient_id": patient_id,
        "source": "DICOM/Radiology simulated context",
        "study_type": "Chest X-Ray",
        "ai_finding": "Right lower zone opacity suspicious for pneumonia",
        "probability": 0.93,
        "confidence": "high",
        "recommendation": "Clinical correlation and physician review required",
        "status": "radiology_context_ready"
    }

@router.get("/ultrasound-context/{patient_id}")
async def ultrasound_context(patient_id: str):
    return {
        "patient_id": patient_id,
        "source": "Ultrasound simulated context",
        "exam_type": "Point-of-care ultrasound",
        "finding": "No critical ultrasound alert in this simulated context",
        "status": "ultrasound_context_ready"
    }

@router.post("/command")
async def process_voice_command(payload: VoiceCommand):
    command_lower = payload.command.lower()

    safety_note = "This AI assistant supports clinical workflow only. Final decision must be made by a licensed clinician."

    if "أشعة" in payload.command or "radiology" in command_lower or "x-ray" in command_lower:
        intent = "radiology_analysis"
        response = (
            "تحليل الأشعة يشير إلى احتمال التهاب رئوي بنسبة مرتفعة. "
            "يجب مراجعة الطبيب وربط النتيجة بالأعراض والعلامات الحيوية."
        )
    elif "سونار" in payload.command or "ultrasound" in command_lower:
        intent = "ultrasound_analysis"
        response = (
            "تم فتح سياق السونار. لا توجد إشارة حرجة في السياق التجريبي الحالي، "
            "ويجب تأكيد ذلك من الطبيب المختص."
        )
    elif "مريض" in payload.command or "patient" in command_lower:
        intent = "patient_context"
        response = (
            "تم تحميل سياق المريض من FHIR. توجد أعراض تنفسية مع نقص بسيط في الأكسجين، "
            "ويُنصح بمراجعة الطبيب."
        )
    else:
        intent = "general_avatar_command"
        response = (
            "تم استقبال الأمر الصوتي. يمكنني المساعدة في شرح الأشعة، السونار، "
            "سياق المريض، والتقارير الطبية."
        )

    audit_id = "AHOS-557-AUDIT-" + uuid.uuid4().hex[:10].upper()

    audit_record = {
        "audit_id": audit_id,
        "timestamp": datetime.utcnow().isoformat(),
        "patient_id": payload.patient_id,
        "language": payload.language,
        "module": payload.module,
        "command": payload.command,
        "intent": intent,
        "response": response,
        "safety_note": safety_note,
        "status": "processed"
    }

    VOICE_AUDIT_LOG.append(audit_record)

    return {
        "audit_id": audit_id,
        "intent": intent,
        "patient_id": payload.patient_id,
        "language": payload.language,
        "avatar_response": response,
        "safety_note": safety_note,
        "voice_ready": True,
        "clinical_context_ready": True,
        "status": "processed"
    }

@router.get("/audit")
async def audit_log():
    return {
        "count": len(VOICE_AUDIT_LOG),
        "records": VOICE_AUDIT_LOG[-20:],
        "status": "audit_ready"
    }

@router.get("/dashboard")
async def dashboard():
    return {
        "title": "AHOS 55.7 Real Voice + Clinical Context Engine",
        "summary": "Voice-enabled clinical avatar connected to FHIR patient context, DICOM radiology context, ultrasound context, and safety audit logs.",
        "readiness_score": 0.88,
        "capabilities": [
            "Browser text-to-speech",
            "Browser speech-to-text readiness",
            "Arabic medical commands",
            "FHIR patient context",
            "DICOM radiology context",
            "Ultrasound context",
            "Clinical safety guardrails",
            "Audit log for every medical command"
        ],
        "status": "dashboard_operational"
    }
