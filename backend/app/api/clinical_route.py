from fastapi import APIRouter
from ..schemas.routing import ClinicalRouteRequest, ClinicalRouteResponse
from ..services.workflow_engine import run_clinical_workflow

router = APIRouter(prefix="/ai", tags=["AI Clinical Workflow"])


@router.post("/clinical-route", response_model=ClinicalRouteResponse)
def clinical_route(payload: ClinicalRouteRequest):
    result = run_clinical_workflow(payload.model_dump())
    return result
