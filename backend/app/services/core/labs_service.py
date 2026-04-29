from fastapi import HTTPException


class LabsService:
    def __init__(self, labs_repository):
        self.labs_repository = labs_repository

    def get_catalog(self):
        return self.labs_repository.get_catalog()

    def list_orders(self):
        return self.labs_repository.list_orders()

    def list_orders_by_patient(self, patient_id: str):
        return self.labs_repository.list_orders_by_patient(patient_id)

    def create_order(self, payload: dict):
        return self.labs_repository.create_order(payload)

    def set_result(self, order_id: str | int, payload: dict):
        order = self.labs_repository.set_result(order_id, payload)
        if not order:
            raise HTTPException(status_code=404, detail="Lab order not found")
        return order
