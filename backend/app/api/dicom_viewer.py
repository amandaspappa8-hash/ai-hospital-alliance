from fastapi import APIRouter, Depends, HTTPException

from backend.app.routers.deps import get_current_user


router = APIRouter(prefix="/api/dicom", tags=["AHOS 54.2 Real DICOM Viewer"])


@router.get("/health")
async def dicom_health():
    return {"status": "online", "phase": "AHOS 54.2"}


@router.get("/study/{study_uid}")
async def get_dicom_study(
    study_uid: str,
    current_user: dict = Depends(get_current_user),
):
    principal_user_id = current_user.get("sub")
    tenant_id = current_user.get("tenant_id")

    try:
        principal_user_id = int(principal_user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=403,
            detail="Invalid authenticated principal scope",
        )

    if tenant_id is None or not str(tenant_id).strip():
        raise HTTPException(
            status_code=403,
            detail="Invalid authenticated tenant scope",
        )

    # Runtime import avoids an application-start circular import while
    # reusing the canonical service registry already owned by main.py.
    from backend.app.main import SERVICES

    radiology_service = SERVICES["radiology"]

    try:
        study = radiology_service.get_study_by_uid(
            study_uid,
            tenant_id=str(tenant_id),
            principal_user_id=principal_user_id,
        )
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        )

    if not study:
        return {
            "status": "not_found",
            "study_uid": study_uid,
        }

    study = dict(study)

    study["ohif_url_direct"] = (
        f"http://127.0.0.1:3005/viewer?StudyInstanceUIDs={study['dicom_study_uid']}"
        if study.get("dicom_study_uid")
        else "http://127.0.0.1:3005"
    )

    study["orthanc_explorer_url"] = (
        f"http://127.0.0.1:8042/app/explorer.html#study?uuid={study['orthanc_id']}"
        if study.get("orthanc_id")
        else None
    )

    return {
        "status": "success",
        "real_data": True,
        "study": study,
    }
