from backend.app.engines.contracts.reconciliation_engine_contract import _build_medication_reconciliation
from backend.app.engines.drug_intel.recommendations import _build_medication_recommendations
from backend.app.engines.contracts.dose_safety_engine_contract import _analyze_dose_safety, _analyze_drug_interactions


def test_reconciliation():
    meds = ["aspirin 81 mg", "ibuprofen 400 mg"]
    result = _build_medication_reconciliation(meds)
    assert result is not None


def test_recommendations():
    result = _build_medication_recommendations(["aspirin 81 mg"], 45)
    assert result is not None


def test_dose_safety():
    result = _analyze_dose_safety(["paracetamol 1000 mg"], 45)
    assert result is not None

def test_drug_interactions():
    result = _analyze_drug_interactions(["warfarin 5 mg", "ibuprofen 400 mg"])
    assert result is not None
