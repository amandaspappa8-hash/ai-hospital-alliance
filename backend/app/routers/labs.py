from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from pydantic import BaseModel

from .deps import (
    get_current_user,
    get_verified_principal_tenant,
    rate_limit_middleware,
)


router = APIRouter(
    prefix="/labs",
    tags=["Labs"],
    dependencies=[
        Depends(get_current_user),
        Depends(rate_limit_middleware),
    ],
)


class LabOrderCreateRequest(BaseModel):
    patientId: str
    patientName: str
    section: Optional[str] = ""
    tests: List[str] = []
    priority: Optional[str] = "Routine"
    status: Optional[str] = "Pending"


class LabResultRequest(BaseModel):
    result: str
    status: Optional[str] = "Completed"


def _scope(
    request: Request,
) -> tuple[int, str]:
    return get_verified_principal_tenant(
        request
    )


# AHOS-R13C17E disabled secondary route: @router.get("/catalog")
def get_labs_catalog():
    from ..main import SERVICES

    return SERVICES["labs"].get_catalog()


# AHOS-R13C17E disabled secondary route: @router.get("/orders")
def get_lab_orders(
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES["labs"].list_orders(
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc


# AHOS-R13C17E disabled secondary route: @router.get("/orders/{patient_id}")
def get_lab_orders_by_patient(
    patient_id: str,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES[
            "labs"
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
def create_lab_order(
    payload: LabOrderCreateRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    if not payload.tests:
        raise HTTPException(
            status_code=400,
            detail="At least one test is required",
        )

    order_payload = {
        "patientId":
            payload.patientId,
        "patientName":
            payload.patientName,
        "section":
            payload.section,
        "tests":
            list(payload.tests),
        "priority":
            payload.priority or "Routine",
        "status":
            payload.status or "Pending",
        "result":
            "",
    }

    try:
        return SERVICES["labs"].create_order(
            order_payload,
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
    except ValueError as exc:
        if str(exc) == "Patient not found":
            raise HTTPException(
                status_code=404,
                detail="Patient not found",
            ) from exc
        raise


# AHOS-R13C17E disabled secondary route: @router.post("/results/{order_id}")
def create_lab_result(
    order_id: str,
    payload: LabResultRequest,
    request: Request,
):
    from ..main import SERVICES

    principal_user_id, tenant_id = _scope(
        request
    )

    try:
        return SERVICES["labs"].set_result(
            order_id,
            {
                "result":
                    payload.result,
                "status":
                    payload.status
                    or "Completed",
            },
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
