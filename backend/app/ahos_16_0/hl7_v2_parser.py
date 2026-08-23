from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter(
    prefix="/ahos/16.0/hl7-v2",
    tags=["AHOS 16.0.2 HL7 v2 Parser"]
)

class HL7MessageRequest(BaseModel):
    message: str = "MSH|^~\\&|AIHA|HOSPITAL|EMR|HOSPITAL|202606060000||ADT^A01|MSG00001|P|2.5\\rPID|||P-1001||Demo^Patient||19700101|U\\rPV1||I|WARD^101^1"

def parse_hl7(message: str):
    segments = message.replace("\\r", "\r").split("\r")
    parsed = {}

    for segment in segments:
        fields = segment.split("|")
        segment_name = fields[0]

        parsed[segment_name] = {
            "fields": fields[1:]
        }

    return parsed

@router.get("/health")
def health():
    return {
        "status": "online",
        "phase": "16.0.2",
        "engine": "HL7 v2 Parser",
        "timestamp": datetime.utcnow().isoformat()
    }

@router.post("/parse")
def parse_message(req: HL7MessageRequest):
    parsed = parse_hl7(req.message)

    return {
        "status": "success",
        "phase": "16.0.2 HL7 v2 Parser",
        "message_id": f"HL7-{uuid.uuid4()}",
        "parsed_message": parsed,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/demo/adt")
def demo_adt():
    msg = "MSH|^~\\&|AIHA|HOSPITAL|EMR|HOSPITAL|202606060000||ADT^A01|MSG00001|P|2.5\\rPID|||P-1001||Demo^Patient||19700101|U\\rPV1||I|WARD^101^1"

    return {
        "status": "success",
        "message_type": "ADT^A01",
        "raw_message": msg,
        "parsed": parse_hl7(msg)
    }

@router.get("/demo/oru")
def demo_oru():
    msg = "MSH|^~\\&|AIHA|LAB|EMR|HOSPITAL|202606060000||ORU^R01|MSG00002|P|2.5\\rPID|||P-1001||Demo^Patient\\rOBR|1|||AIHA^Lab Result\\rOBX|1|NM|AI_SCORE||88|score"

    return {
        "status": "success",
        "message_type": "ORU^R01",
        "raw_message": msg,
        "parsed": parse_hl7(msg)
    }

@router.get("/supported-messages")
def supported_messages():
    return {
        "status": "success",
        "supported_hl7_v2_messages": {
            "ADT": "Admission, Discharge, Transfer",
            "ORU": "Observation Result",
            "ORM": "Order Message",
            "MDM": "Medical Document Management",
            "SIU": "Scheduling Information"
        }
    }

@router.get("/mapping")
def mapping():
    return {
        "status": "success",
        "hl7_mapping": {
            "MSH": "Message Header",
            "PID": "Patient Identification",
            "PV1": "Patient Visit",
            "OBR": "Observation Request",
            "OBX": "Observation Result",
            "ORC": "Common Order",
            "TXA": "Document Notification"
        }
    }

@router.get("/executive-summary")
def executive_summary():
    return {
        "status": "success",
        "summary": {
            "phase": "16.0.2",
            "status": "HL7 v2 Parser Prototype Active",
            "strategic_value": "Starts hospital message interoperability for ADT, ORU, ORM, MDM, and enterprise integration",
            "next_phase": "16.0.3 Orthanc / OHIF PACS Production Bridge"
        }
    }
