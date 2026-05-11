from fastapi import Depends
from .deps import get_current_user
from fastapi import Depends
from .deps import get_current_user, rate_limit_middleware
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/labs", tags=["Labs"], dependencies=[Depends(get_current_user), Depends(rate_limit_middleware)])

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

@router.get("/catalog")
def get_labs_catalog():
    from ..main import LAB_CATALOG
    return LAB_CATALOG

@router.get("/orders")
def get_lab_orders():
    from ..main import LAB_ORDERS
    return LAB_ORDERS

@router.get("/orders/{patient_id}")
def get_lab_orders_by_patient(patient_id: str):
    from ..main import LAB_ORDERS
    return [o for o in LAB_ORDERS if o["patientId"] == patient_id]

@router.post("/orders")
def create_lab_order(payload: LabOrderCreateRequest):
    from ..main import LAB_ORDERS
    if not payload.tests:
        raise HTTPException(status_code=400, detail="At least one test is required")
    new_order = {
        "id": f"L-{4000 + len(LAB_ORDERS) + 1}",
        "patientId": payload.patientId,
        "patientName": payload.patientName,
        "section": payload.section,
        "tests": payload.tests,
        "priority": payload.priority or "Routine",
        "status": payload.status or "Pending",
        "result": "",
    }
    LAB_ORDERS.append(new_order)
    return new_order

@router.post("/results/{order_id}")
def create_lab_result(order_id: str, payload: LabResultRequest):
    from ..main import LAB_ORDERS
    for order in LAB_ORDERS:
        if order["id"] == order_id:
            order["result"] = payload.result
            order["status"] = payload.status or "Completed"
            return order
    raise HTTPException(status_code=404, detail="Lab order not found")
