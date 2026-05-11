from fastapi import Depends
from .deps import get_current_user
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/radiology", tags=["Radiology"], dependencies=[Depends(get_current_user)])

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

@router.get("/catalog")
def get_radiology_catalog():
    from ..main import RADIOLOGY_CATALOG
    return RADIOLOGY_CATALOG

@router.get("/orders")
def get_radiology_orders():
    from ..main import RADIOLOGY_ORDERS
    return RADIOLOGY_ORDERS

@router.get("/orders/{patient_id}")
def get_radiology_orders_by_patient(patient_id: str):
    from ..main import RADIOLOGY_ORDERS
    return [o for o in RADIOLOGY_ORDERS if o["patientId"] == patient_id]

@router.post("/orders")
def create_radiology_order(payload: RadiologyOrderCreateRequest):
    from ..main import RADIOLOGY_ORDERS
    if not payload.studies:
        raise HTTPException(status_code=400, detail="At least one study is required")
    new_order = {
        "id": f"RAD-{5000 + len(RADIOLOGY_ORDERS) + 1}",
        "patientId": payload.patientId,
        "patientName": payload.patientName,
        "section": payload.section,
        "studies": payload.studies,
        "priority": payload.priority or "Routine",
        "status": payload.status or "Pending",
        "report": "",
    }
    RADIOLOGY_ORDERS.append(new_order)
    return new_order

@router.post("/results/{order_id}")
def create_radiology_report(order_id: str, payload: RadiologyReportRequest):
    from ..main import RADIOLOGY_ORDERS
    for order in RADIOLOGY_ORDERS:
        if order["id"] == order_id:
            order["report"] = payload.report
            order["status"] = payload.status or "Completed"
            return order
    raise HTTPException(status_code=404, detail="Radiology order not found")
