from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from ..routers.deps import (
    get_verified_principal_tenant,
)


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Unified Dashboard"],
)


@router.get("/overview")
async def overview(request: Request):
    from ..main import SERVICES

    (
        principal_user_id,
        tenant_id,
    ) = get_verified_principal_tenant(
        request
    )

    try:
        return SERVICES["dashboard"].overview(
            tenant_id=tenant_id,
            principal_user_id=principal_user_id,
        )

    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        ) from exc
