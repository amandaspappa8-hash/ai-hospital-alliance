from backend.app.plugins.base import AHOSPlugin


def register(app):
    from backend.app.ahos_36_0.autonomous_global_healthcare_operating_civilization import router as ahos36_router
    from backend.app.ahos_37_0.autonomous_planetary_healthcare_intelligence_platform import router as ahos37_router
    from backend.app.ahos_38_0.autonomous_interplanetary_healthcare_intelligence_platform import router as ahos38_router

    app.include_router(ahos36_router)
    app.include_router(ahos37_router)
    app.include_router(ahos38_router)


plugin = AHOSPlugin(
    name="AHOS Global Intelligence Plugin",
    version="1.0.0",
    category="global-intelligence",
    register=register,
    description="Registers AHOS 36.0, 37.0 and 38.0 global/planetary/interplanetary intelligence routers"
)
