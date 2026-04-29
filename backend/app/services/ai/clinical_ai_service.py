class ClinicalAIService:
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def clinical_route(self, run_clinical_workflow, payload):
        return run_clinical_workflow(payload)

    def clinical_route_and_create_orders(
        self, run_clinical_workflow, patient_id: str, payload
    ):
        result = run_clinical_workflow(payload)

        created_orders = []
        for suggested in result.get("suggested_orders", []):
            created = self.orders_repository.create(
                patient_id,
                {
                    "item": suggested.get("name", ""),
                    "type": suggested.get("category", "General"),
                    "priority": suggested.get("priority", "routine"),
                    "status": "Pending",
                },
            )
            created_orders.append(created)

        return {
            "clinical_route": result,
            "created_orders": created_orders,
        }
