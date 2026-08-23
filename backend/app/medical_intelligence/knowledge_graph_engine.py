from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/ai-ultrasound-x",
    tags=["AI Ultrasound X 9.1"]
)

class ClinicalCase(BaseModel):
    symptoms: list[str]
    labs: dict = {}
    imaging: str = ""
    medications: list[str] = []
    age: int = 0
    gender: str = ""

@router.get("/knowledge-graph-health")
def health():
    return {
        "status": "online",
        "version": "9.1",
        "engine": "Autonomous Medical Knowledge Graph Engine"
    }

@router.post("/medical-knowledge-graph")
def build_graph(case: ClinicalCase):

    diagnosis = "Renal Colic / Possible Ureteric Stone"

    graph = {
        "nodes": [
            {"id":"symptoms","type":"Symptoms","value":case.symptoms},
            {"id":"labs","type":"Laboratory","value":case.labs},
            {"id":"imaging","type":"Imaging","value":case.imaging},
            {"id":"medications","type":"Pharmacy","value":case.medications},
            {"id":"diagnosis","type":"Diagnosis","value":diagnosis},
            {"id":"icd11","type":"ICD11","value":"GB70"},
            {"id":"risk","type":"Risk","value":"HIGH"},
            {
                "id":"recommendation",
                "type":"Recommendation",
                "value":"Renal Ultrasound + CT KUB + Urology Follow-up"
            }
        ],

        "links":[
            {"source":"symptoms","target":"diagnosis"},
            {"source":"labs","target":"diagnosis"},
            {"source":"imaging","target":"diagnosis"},
            {"source":"medications","target":"risk"},
            {"source":"diagnosis","target":"icd11"},
            {"source":"diagnosis","target":"risk"},
            {"source":"risk","target":"recommendation"}
        ]
    }

    return {
        "platform":"AI Ultrasound X 9.1",
        "engine":"Autonomous Medical Knowledge Graph Engine",
        "status":"online",
        "graph":graph
    }
