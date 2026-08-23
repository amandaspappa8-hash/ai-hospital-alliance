from backend.app.plugins.base import AHOSPlugin


def register(app):
    from backend.app.ahos_32_0.autonomous_healthcare_agi_platform import router as ahos32_router
    from backend.app.ahos_32_1.autonomous_healthcare_civilization_platform import router as ahos321_router

    app.include_router(ahos32_router)
    app.include_router(ahos321_router)


plugin = AHOSPlugin(
    name="AHOS AGI Plugin",
    version="1.0.0",
    category="agi",
    register=register,
    description="Registers AHOS 32.0 and AHOS 32.1 AGI/Civilization routers"
)
