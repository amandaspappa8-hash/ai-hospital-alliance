from typing import List, Dict


def chest_pain_orders(triage_level: str) -> List[Dict]:
    orders = [
        {"name": "ECG", "priority": "stat", "category": "cardiac"},
        {"name": "Troponin", "priority": "urgent", "category": "lab"},
        {"name": "CBC", "priority": "urgent", "category": "lab"},
        {"name": "CMP", "priority": "urgent", "category": "lab"},
        {"name": "Chest X-ray", "priority": "urgent", "category": "imaging"},
        {"name": "Continuous vital monitoring", "priority": "stat", "category": "monitoring"},
    ]

    if triage_level == "moderate":
        for item in orders:
            if item["priority"] == "stat":
                item["priority"] = "urgent"

    return orders
