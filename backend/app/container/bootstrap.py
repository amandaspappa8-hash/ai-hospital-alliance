from backend.app.container.container import container


def bootstrap_services():

    container.register(
        "agi_service",
        "AHOS AGI Service"
    )

    container.register(
        "civilization_service",
        "AHOS Civilization Service"
    )

    container.register(
        "research_service",
        "AHOS Research Service"
    )

    container.register(
        "drug_discovery_service",
        "AHOS Drug Discovery Service"
    )

    container.register(
        "precision_medicine_service",
        "AHOS Precision Medicine Service"
    )

    container.register(
        "global_intelligence_service",
        "AHOS Global Civilization Service"
    )

    container.register(
        "planetary_service",
        "AHOS Planetary Intelligence Service"
    )

    container.register(
        "interplanetary_service",
        "AHOS Interplanetary Intelligence Service"
    )

    container.register(
        "universal_network_service",
        "AHOS Universal Medical Network Service"
    )

    container.register(
        "supercivilization_service",
        "AHOS Medical Supercivilization Service"
    )
