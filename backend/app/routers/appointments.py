from fastapi import APIRouter, Depends, HTTPException, Request
from .deps import (
    get_current_user,
    get_verified_principal_tenant,
    rate_limit_middleware,
)
from pydantic import BaseModel
from typing import Optional

router = APIRouter(tags=["Appointments"], dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)])

class AppointmentRequest(BaseModel):
    patientId: Optional[str] = ""
    patientName: Optional[str] = ""
    patient: Optional[str] = ""
    department: Optional[str] = ""
    doctor: Optional[str] = ""
    date: Optional[str] = ""
    time: Optional[str] = ""
    status: Optional[str] = "Scheduled"

# AHOS-R13C17E disabled secondary route: @router.get("/appointments")
def get_appointments(request: Request):
    from ..main import SERVICES

    principal_user_id, tenant_id = (
        get_verified_principal_tenant(request)
    )

    try:
        return SERVICES["appointments"].list_appointments(
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Tenant scope denied",
        ) from exc

# AHOS-R13C17E disabled secondary route: @router.post("/appointments")
def create_appointment(
    payload: AppointmentRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = (
        get_verified_principal_tenant(request)
    )

    try:
        return SERVICES["appointments"].create_appointment(
            {
                "patientId": payload.patientId or "",
                "patientName": payload.patientName or payload.patient or "",
                "department": payload.department,
                "doctor": payload.doctor,
                "date": payload.date or "",
                "time": payload.time,
                "status": payload.status or "Scheduled",
            },
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Tenant scope denied",
        ) from exc
    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
