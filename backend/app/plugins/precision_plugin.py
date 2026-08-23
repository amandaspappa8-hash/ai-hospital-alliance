from backend.app.plugins.base import AHOSPlugin


def register(app):
    from backend.app.ahos_35_0.autonomous_global_precision_medicine_platform import router as ahos35_router

    app.include_router(ahos35_router)


plugin = AHOSPlugin(
    name="AHOS Precision Medicine Plugin",
    version="1.0.0",
    category="precision-medicine",
    register=register,
    description="Registers AHOS 35.0 Precision Medicine and Digital Human router"
)
