from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .deps import (
    get_current_user,
    get_verified_principal_tenant,
    rate_limit_middleware,
)


router = APIRouter(
    prefix="/radiology",
    tags=["Radiology"],
    dependencies=[
        Depends(get_current_user),
        Depends(rate_limit_middleware),
    ],
)


class RadiologyOrderCreateRequest(BaseModel):
    patientId: str
    patientName: str
    section: Optional[str] = ""
    studies: List[str] = []
    priority: Optional[str] = "Routine"
    status: Optional[str] = "Pending"


class RadiologyReportRequest(BaseModel):
    report: str
    status: Optional[str] = "Completed"


def _scope(
    request: Request,
) -> tuple[int, str]:
    return get_verified_principal_tenant(
        request
    )


# AHOS-R13C17E disabled secondary route: @router.get("/catalog")
def get_radiology_catalog():
    from ..main import SERVICES

    return SERVICES["radiology"].get_catalog()


# AHOS-R13C17E disabled secondary route: @router.get("/orders")
def get_radiology_orders(
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES["radiology"].list_orders(
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.get("/orders/{patient_id}")
def get_radiology_orders_by_patient(
    patient_id: str,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES[
            "radiology"
        ].list_orders_by_patient(
            patient_id,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.post("/orders")
def create_radiology_order(
    payload: RadiologyOrderCreateRequest,
    request: Request,
):
    from ..main import SERVICES

    if not payload.studies:
        raise HTTPException(
            status_code=400,
            detail="At least one study is required",
        )

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES["radiology"].create_order(
            payload.model_dump(),
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.post("/results/{order_id}")
def create_radiology_report(
    order_id: str,
    payload: RadiologyReportRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES["radiology"].set_result(
            order_id,
            payload.model_dump(),
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
