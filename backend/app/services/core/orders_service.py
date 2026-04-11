class OrdersService:
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def list_orders(self, patient_id: str):
        return self.orders_repository.list_by_patient(patient_id)

    def create_order(self, patient_id: str, payload: dict):
        return self.orders_repository.create(patient_id, payload)
