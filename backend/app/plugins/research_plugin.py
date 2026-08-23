from backend.app.plugins.base import AHOSPlugin


def register(app):
    from backend.app.ahos_33_0.autonomous_medical_research_discovery_network import router as ahos33_router
    from backend.app.ahos_34_0.autonomous_medical_innovation_drug_discovery_ecosystem import router as ahos34_router
    from backend.app.ahos_39_0.autonomous_universal_medical_network import router as ahos39_router
    from backend.app.ahos_40_0.autonomous_medical_supercivilization_platform import router as ahos40_router

    # AHOS R13C.16A: AHOS 33.0 already registered directly in main.py
    # app.include_router(ahos33_router)
    # AHOS R13C.16A: AHOS 34.0 already registered directly in main.py
    # app.include_router(ahos34_router)
    app.include_router(ahos39_router)
    app.include_router(ahos40_router)


plugin = AHOSPlugin(
    name="AHOS Research & Supercivilization Plugin",
    version="1.0.0",
    category="research",
    register=register,
    description="Registers research, discovery, universal medical network and supercivilization routers"
)
