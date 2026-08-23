from backend.app.service_registry.base import AHOSService


SERVICES = [
    AHOSService(
        name="AHOS AGI Service",
        version="1.0.0",
        category="agi",
        status="ACTIVE",
        endpoint="/ahos/32.0",
        description="Autonomous Healthcare AGI Platform"
    ),
    AHOSService(
        name="AHOS Civilization Service",
        version="1.0.0",
        category="civilization",
        status="ACTIVE",
        endpoint="/ahos/32.1",
        description="Autonomous Healthcare Civilization Platform"
    ),
    AHOSService(
        name="AHOS Research Service",
        version="1.0.0",
        category="research",
        status="ACTIVE",
        endpoint="/ahos/33.0",
        description="Autonomous Medical Research and Discovery Network"
    ),
    AHOSService(
        name="AHOS Drug Discovery Service",
        version="1.0.0",
        category="drug-discovery",
        status="ACTIVE",
        endpoint="/ahos/34.0",
        description="Autonomous Medical Innovation and Drug Discovery Ecosystem"
    ),
    AHOSService(
        name="AHOS Precision Medicine Service",
        version="1.0.0",
        category="precision-medicine",
        status="ACTIVE",
        endpoint="/ahos/35.0",
        description="Precision Medicine and Digital Human Platform"
    ),
    AHOSService(
        name="AHOS Global Civilization Service",
        version="1.0.0",
        category="global-intelligence",
        status="ACTIVE",
        endpoint="/ahos/36.0",
        description="Autonomous Global Healthcare Operating Civilization"
    ),
    AHOSService(
        name="AHOS Planetary Intelligence Service",
        version="1.0.0",
        category="planetary-intelligence",
        status="ACTIVE",
        endpoint="/ahos/37.0",
        description="Autonomous Planetary Healthcare Intelligence Platform"
    ),
    AHOSService(
        name="AHOS Interplanetary Intelligence Service",
        version="1.0.0",
        category="interplanetary-intelligence",
        status="ACTIVE",
        endpoint="/ahos/38.0",
        description="Autonomous Interplanetary Healthcare Intelligence Platform"
    ),
    AHOSService(
        name="AHOS Universal Medical Network Service",
        version="1.0.0",
        category="universal-medical-network",
        status="ACTIVE",
        endpoint="/ahos/39.0",
        description="Autonomous Universal Medical Network"
    ),
    AHOSService(
        name="AHOS Medical Supercivilization Service",
        version="1.0.0",
        category="supercivilization",
        status="ACTIVE",
        endpoint="/ahos/40.0",
        description="Autonomous Medical Supercivilization Platform"
    ),
]


def list_services():
    return [s.__dict__ for s in SERVICES]


def get_service_by_name(name: str):
    for service in SERVICES:
        if service.name.lower() == name.lower():
            return service.__dict__
    return None


def get_services_by_category(category: str):
    return [
        s.__dict__
        for s in SERVICES
        if s.category.lower() == category.lower()
    ]


def service_summary():
    return {
        "total_services": len(SERVICES),
        "active_services": len([s for s in SERVICES if s.status == "ACTIVE"]),
        "categories": sorted(list(set([s.category for s in SERVICES]))),
        "status": "SERVICE_REGISTRY_READY"
    }
