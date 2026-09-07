from backend.app.services.ai.drug_intel_service import DrugIntelService


class FakeMarRepository:
    def __init__(self):
        self.items = {
            "P-001": [
                {"medication": "aspirin 81 mg"},
                {"medication": "ibuprofen 400 mg"},
            ]
        }

    def list_by_patient(self, patient_id):
        return list(self.items.get(patient_id, []))


def test_reconciliation_service_contract():
    service = DrugIntelService(FakeMarRepository())

    captured = {}

    def builder(medications):
        captured["medications"] = medications
        return {
            "count": len(medications),
            "medications": medications,
        }

    result = service.reconciliation_for_patient(
        "P-001",
        builder,
    )

    assert captured["medications"] == [
        "aspirin 81 mg",
        "ibuprofen 400 mg",
    ]
    assert result["count"] == 2


def test_recommendations_service_contract():
    service = DrugIntelService(FakeMarRepository())

    def builder(medications, age):
        return {
            "medications": medications,
            "age": age,
            "recommendations": ["review"],
        }

    result = service.recommendations_from_payload(
        ["aspirin 81 mg"],
        45,
        builder,
    )

    assert result == {
        "medications": ["aspirin 81 mg"],
        "age": 45,
        "recommendations": ["review"],
    }


def test_dose_safety_service_contract():
    service = DrugIntelService(FakeMarRepository())

    def analyzer(medications, age):
        return {
            "medications": medications,
            "age": age,
            "safe": True,
        }

    result = service.dose_safety_from_payload(
        ["paracetamol 1000 mg"],
        45,
        analyzer,
    )

    assert result == {
        "medications": ["paracetamol 1000 mg"],
        "age": 45,
        "safe": True,
    }


def test_drug_interactions_service_contract():
    service = DrugIntelService(FakeMarRepository())

    def analyzer(medications):
        return {
            "medications": medications,
            "interaction_count": 1,
        }

    result = service.interactions_from_payload(
        [
            "warfarin 5 mg",
            "ibuprofen 400 mg",
        ],
        analyzer,
    )

    assert result["medications"] == [
        "warfarin 5 mg",
        "ibuprofen 400 mg",
    ]
    assert result["interaction_count"] == 1
