from __future__ import annotations

from datetime import datetime, timezone


class DashboardAggregationService:
    """Aggregate dashboard data without persistence access in the API layer."""

    def __init__(
        self,
        *,
        patients_service,
        radiology_service,
        physician_review_adapter,
        persistent_event_adapter,
        clinical_safety_adapter,
        legacy_operational_adapter,
    ) -> None:
        self.patients_service = (
            patients_service
        )
        self.radiology_service = (
            radiology_service
        )
        self.physician_review_adapter = (
            physician_review_adapter
        )
        self.persistent_event_adapter = (
            persistent_event_adapter
        )
        self.clinical_safety_adapter = (
            clinical_safety_adapter
        )
        self.legacy_operational_adapter = (
            legacy_operational_adapter
        )

    def overview(
        self,
        *,
        tenant_id: str,
        principal_user_id: int,
    ) -> dict:
        patients = (
            self.patients_service.list_patients(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )
        )

        studies = (
            self.radiology_service.list_dashboard_studies(
                tenant_id=tenant_id,
                principal_user_id=principal_user_id,
            )
        )

        total_patients = len(
            patients
            if isinstance(patients, list)
            else []
        )

        canonical_studies = [
            study
            for study in (
                studies
                if isinstance(studies, list)
                else []
            )
            if isinstance(study, dict)
        ]

        radiology_studies = len(
            canonical_studies
        )

        ultrasound_studies = sum(
            1
            for study in canonical_studies
            if str(
                study.get(
                    "modality",
                    "",
                )
                or ""
            ).strip().upper() == "US"
        )

        safety = (
            self.physician_review_adapter.read()
        )

        events = (
            self.persistent_event_adapter.read()
        )

        clinical_safety = (
            self.clinical_safety_adapter.read()
        )

        legacy = (
            self.legacy_operational_adapter.read()
        )

        return {
            "source":
                "ahos_canonical_persisted_sources",

            "real_data": True,

            "synthetic_metrics": False,

            "generated_at": datetime.now(
                timezone.utc
            ).isoformat(),

            "kpis": {
                "total_patients":
                    total_patients,

                "available_doctors":
                    legacy[
                        "available_doctors"
                    ],

                "active_alerts":
                    clinical_safety[
                        "active_alerts"
                    ],

                "critical_alerts":
                    clinical_safety[
                        "critical_alerts"
                    ],

                "radiology_studies":
                    radiology_studies,

                "ultrasound_studies":
                    ultrasound_studies,

                "critical_lab_results":
                    legacy[
                        "critical_lab_results"
                    ],

                "low_stock_drugs":
                    legacy[
                        "low_stock_drugs"
                    ],

                "hospitals":
                    legacy[
                        "hospitals"
                    ],

                "physician_reviews":
                    safety[
                        "total_reviews"
                    ],

                "pending_physician_reviews":
                    safety[
                        "pending_reviews"
                    ],

                "urgent_physician_reviews":
                    safety[
                        "urgent_reviews"
                    ],

                "patient_states":
                    events[
                        "patient_states"
                    ],

                "decision_logs":
                    events[
                        "decision_logs"
                    ],

                "bus_events":
                    events[
                        "bus_events"
                    ],

                "critical_decisions":
                    events[
                        "critical_decisions"
                    ],

                "high_priority_events":
                    events[
                        "high_priority_events"
                    ],
            },

            "safety": {
                "source":
                    "AHOS 56.x physician_review_queue",

                "available":
                    safety["available"],

                "total_reviews":
                    safety["total_reviews"],

                "pending_reviews":
                    safety["pending_reviews"],

                "approved_reviews":
                    safety["approved_reviews"],

                "rejected_reviews":
                    safety["rejected_reviews"],

                "needs_more_review":
                    safety["needs_more_review"],

                "urgent_reviews":
                    safety["urgent_reviews"],
            },

            "persistent_events": {
                "source":
                    "AHOS Persistent Events Database",

                **events,
            },

            "status":
                "dashboard_operational",
        }
