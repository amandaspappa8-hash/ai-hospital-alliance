from typing import Any


class InMemoryRadiologyRepository:
    def __init__(
        self, catalog_store: dict[str, Any], orders_store: list[dict[str, Any]]
    ):
        self.catalog_store = catalog_store
        self.orders_store = orders_store

    def get_catalog(self) -> dict[str, Any]:
        return dict(self.catalog_store)

    def list_orders(self) -> list[dict[str, Any]]:
        return list(self.orders_store)

    def list_orders_by_patient(self, patient_id: str) -> list[dict[str, Any]]:
        return [
            order for order in self.orders_store if order.get("patientId") == patient_id
        ]

    def get_study_by_uid(
        self,
        study_uid: str,
    ):
        orders = (
            self.orders_store.values()
            if isinstance(self.orders_store, dict)
            else self.orders_store
        )

        for order in orders:
            if not isinstance(order, dict):
                continue

            studies = order.get("studies") or []

            if not isinstance(studies, list):
                studies = []

            matched_study = None

            for study in studies:
                if not isinstance(study, dict):
                    continue

                identifiers = (
                    study.get("study_uid"),
                    study.get("studyUid"),
                    study.get("dicom_study_uid"),
                    study.get("StudyInstanceUID"),
                )

                if any(
                    value is not None
                    and str(value) == str(study_uid)
                    for value in identifiers
                ):
                    matched_study = study
                    break

            order_uid = order.get("study_uid")

            if (
                matched_study is None
                and (
                    order_uid is None
                    or str(order_uid) != str(study_uid)
                )
            ):
                continue

            study = matched_study or {}

            return {
                "patient_id": (
                    order.get("patient_id")
                    or order.get("patientId")
                ),
                "study_uid": (
                    order_uid
                    or study.get("study_uid")
                    or study.get("studyUid")
                    or study_uid
                ),
                "modality": study.get("modality"),
                "description": study.get("description"),
                "ohif_url": study.get("ohif_url"),
                "dicom_study_uid": (
                    study.get("dicom_study_uid")
                    or study.get("StudyInstanceUID")
                ),
                "orthanc_id": study.get("orthanc_id"),
            }

        return None

    def list_dashboard_studies(
        self,
    ) -> list[dict[str, Any]]:
        dashboard_studies: list[dict[str, Any]] = []

        for order in self.list_orders():
            studies = order.get("studies") or []

            if not isinstance(studies, list):
                studies = []

            order_uid = (
                order.get("study_uid")
                or order.get("studyUid")
                or order.get("dicom_study_uid")
                or order.get("StudyInstanceUID")
            )

            patient_id = (
                order.get("patient_id")
                or order.get("patientId")
                or ""
            )

            if not studies and order_uid:
                studies = [{}]

            for index, item in enumerate(studies):
                if not isinstance(item, dict):
                    continue

                study_uid = (
                    item.get("study_uid")
                    or item.get("studyUid")
                    or item.get("dicom_study_uid")
                    or item.get("StudyInstanceUID")
                )

                if (
                    not study_uid
                    and len(studies) == 1
                ):
                    study_uid = order_uid

                dashboard_studies.append(
                    {
                        "id": (
                            item.get("id")
                            or order.get("id")
                        ),
                        "tenant_id": (
                            item.get("tenant_id")
                            or order.get("tenant_id")
                        ),
                        "patient_id": patient_id,
                        "study_uid": study_uid,
                        "modality": item.get("modality"),
                        "description": (
                            item.get("description")
                            or item.get("study_description")
                        ),
                        "ohif_url": (
                            item.get("ohif_url")
                            or item.get("ohif_viewer_url")
                        ),
                        "dicom_study_uid": (
                            item.get("dicom_study_uid")
                            or item.get("StudyInstanceUID")
                            or study_uid
                        ),
                        "orthanc_id": item.get("orthanc_id"),
                        "created_at": (
                            item.get("created_at")
                            or order.get("created_at")
                        ),
                    }
                )

        return dashboard_studies

    def create_order(self, payload: dict[str, Any]) -> dict[str, Any]:
        numeric_ids: list[int] = []

        for order in self.orders_store:
            order_id = str(
                order.get("id", "")
            )

            if not order_id.startswith("RAD-"):
                continue

            suffix = order_id[4:]

            if suffix.isdigit():
                numeric_ids.append(
                    int(suffix)
                )

        next_number = (
            max(
                5000,
                max(
                    numeric_ids,
                    default=5000,
                ),
            )
            + 1
        )

        new_order = {
            "id": f"RAD-{next_number}",
            "patientId": payload.get(
                "patientId",
                "",
            ),
            "patientName": payload.get(
                "patientName",
                "",
            ),
            "section": payload.get(
                "section",
                "",
            ),
            "studies": list(
                payload.get(
                    "studies",
                    [],
                )
            ),
            "priority": (
                payload.get("priority")
                or "Routine"
            ),
            "status": (
                payload.get("status")
                or "Pending"
            ),
            "report": (
                payload.get(
                    "report",
                    "",
                )
                or ""
            ),
        }

        self.orders_store.append(
            new_order
        )

        return new_order

    def set_result(self, order_id: str | int, payload: dict[str, Any]) -> dict[str, Any] | None:
        for order in self.orders_store:
            if str(
                order.get(
                    "id",
                    "",
                )
            ) != str(order_id):
                continue

            order["report"] = (
                payload.get(
                    "report",
                    "",
                )
                or ""
            )

            order["status"] = (
                payload.get("status")
                or "Completed"
            )

            return order

        return None
