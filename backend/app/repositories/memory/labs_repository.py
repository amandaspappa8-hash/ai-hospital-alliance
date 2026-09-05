from typing import Any


class InMemoryLabsRepository:

    def __init__(
        self,
        catalog_store: dict[str, Any],
        orders_store: list[dict[str, Any]],
    ):
        self.catalog_store = catalog_store
        self.orders_store = orders_store

    def get_catalog(self) -> dict[str, Any]:
        return dict(
            self.catalog_store
        )

    def list_orders(
        self,
    ) -> list[dict[str, Any]]:
        return list(
            self.orders_store
        )

    def list_orders_by_patient(
        self,
        patient_id: str,
    ) -> list[dict[str, Any]]:
        return [
            order
            for order in self.orders_store
            if order.get(
                "patientId"
            ) == patient_id
        ]

    def create_order(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        next_number = 4001

        numeric_ids = []

        for order in self.orders_store:
            order_id = str(
                order.get(
                    "id",
                    "",
                )
            )

            if not order_id.startswith(
                "L-"
            ):
                continue

            suffix = order_id[2:]

            if suffix.isdigit():
                numeric_ids.append(
                    int(suffix)
                )

        if numeric_ids:
            next_number = max(
                4000,
                max(numeric_ids),
            ) + 1

        new_order = {
            "id":
                f"L-{next_number}",
            "patientId":
                payload.get(
                    "patientId",
                    "",
                ),
            "patientName":
                payload.get(
                    "patientName",
                    "",
                ),
            "section":
                payload.get(
                    "section",
                    "",
                ),
            "tests":
                list(
                    payload.get(
                        "tests",
                        [],
                    )
                ),
            "priority":
                payload.get(
                    "priority"
                )
                or "Routine",
            "status":
                payload.get(
                    "status"
                )
                or "Pending",
            "result":
                payload.get(
                    "result",
                    "",
                )
                or "",
        }

        self.orders_store.append(
            new_order
        )

        return new_order

    def set_result(
        self,
        order_id: str | int,
        payload: dict[str, Any],
    ) -> dict[str, Any] | None:
        for order in self.orders_store:
            if str(
                order.get(
                    "id"
                )
            ) == str(order_id):
                order[
                    "result"
                ] = payload.get(
                    "result",
                    "",
                )

                order[
                    "status"
                ] = (
                    payload.get(
                        "status"
                    )
                    or "Completed"
                )

                return order

        return None
