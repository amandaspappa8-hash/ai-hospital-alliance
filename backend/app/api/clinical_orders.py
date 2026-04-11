from fastapi import APIRouter
from ..schemas.routing import ClinicalRouteRequest
from ..services.workflow_engine import run_clinical_workflow
from ..state import ORDERS

router = APIRouter(prefix="/ai", tags=["AI Clinical Orders"])


@router.post("/clinical-route-and-create-orders/{patient_id}")
def clinical_route_and_create_orders(patient_id: str, payload: ClinicalRouteRequest):
    result = run_clinical_workflow(payload.model_dump())

    arr = ORDERS.setdefault(patient_id, [])

    existing_keys = {
        (str(order.get("type", "")).strip().lower(), str(order.get("status", "")).strip().lower())
        for order in arr
    }

    created = []
    skipped = []

    for item in result["suggested_orders"]:
        order_type = item["name"].strip()
        key = (order_type.lower(), "draft")

        if key in existing_keys:
            skipped.append(order_type)
            continue

        order = {
            "id": len(arr) + 1,
            "type": order_type,
            "department": result["route_to"][0] if result["route_to"] else "General",
            "note": f"AI suggested order ({item['priority']})",
            "status": "draft",
        }
        arr.append(order)
        created.append(order)
        existing_keys.add(key)

    return {
        "patient_id": patient_id,
        "clinical_route": result,
        "created_orders": created,
        "skipped_existing_orders": skipped,
    }
