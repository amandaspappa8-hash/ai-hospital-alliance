from fastapi import APIRouter

router = APIRouter(
    prefix="/plugins",
    tags=["AHOS Plugin Architecture"]
)

LOADED_PLUGINS = []


@router.get("/health")
async def health():
    return {
        "status": "online",
        "plugin_architecture": "active",
        "loaded_plugins": len(LOADED_PLUGINS)
    }


@router.get("/loaded")
async def loaded():
    return {
        "plugins": LOADED_PLUGINS,
        "total": len(LOADED_PLUGINS),
        "status": "PLUGINS_READY"
    }
