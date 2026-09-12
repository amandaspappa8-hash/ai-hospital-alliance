from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .deps import (
    get_current_user,
    get_verified_principal_tenant,
    rate_limit_middleware,
)


router = APIRouter(
    prefix="/nursing",
    tags=["Nursing"],
    dependencies=[
        Depends(get_current_user),
        Depends(rate_limit_middleware),
    ],
)


class NursingVitalRequest(BaseModel):
    temperature: Optional[str] = ""
    bloodPressure: Optional[str] = ""
    heartRate: Optional[str] = ""
    respiratoryRate: Optional[str] = ""
    oxygenSaturation: Optional[str] = ""
    time: Optional[str] = ""


class NursingNoteRequest(BaseModel):
    text: str


def _scope(request: Request) -> tuple[int, str]:
    return get_verified_principal_tenant(request)


# AHOS-R13C17E disabled secondary route: @router.get("/vitals/{patient_id}")
def get_nursing_vitals(
    patient_id: str,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(request)

    try:
        return SERVICES["nursing"].list_vitals(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.post("/vitals/{patient_id}")
def create_nursing_vital(
    patient_id: str,
    payload: NursingVitalRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(request)

    try:
        return SERVICES["nursing"].create_vital(
            patient_id,
            {
                "temperature": payload.temperature,
                "bloodPressure": payload.bloodPressure,
                "heartRate": payload.heartRate,
                "respiratoryRate": payload.respiratoryRate,
                "oxygenSaturation": payload.oxygenSaturation,
                "time": payload.time,
            },
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.get("/notes/{patient_id}")
def get_nursing_notes(
    patient_id: str,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(request)

    try:
        return SERVICES["nursing"].list_notes(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.post("/notes/{patient_id}")
def create_nursing_note(
    patient_id: str,
    payload: NursingNoteRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(request)

    try:
        return SERVICES["nursing"].create_note(
            patient_id,
            payload.text,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        ) from exc
