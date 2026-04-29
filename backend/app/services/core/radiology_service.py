from fastapi import HTTPException


class RadiologyService:
    def __init__(self, radiology_repository):
        self.radiology_repository = radiology_repository

    def get_catalog(self):
        return self.radiology_repository.get_catalog()

    def list_orders(self):
        return self.radiology_repository.list_orders()

    def list_orders_by_patient(self, patient_id: str):
        return self.radiology_repository.list_orders_by_patient(patient_id)

    def create_order(self, payload: dict):
        return self.radiology_repository.create_order(payload)

    def set_result(self, order_id: str | int, payload: dict):
        order = self.radiology_repository.set_result(order_id, payload)
        if not order:
            raise HTTPException(status_code=404, detail="Radiology order not found")
        return order
