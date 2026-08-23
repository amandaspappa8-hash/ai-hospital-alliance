from fastapi import APIRouter
from sqlalchemy import create_engine, text
import os

router = APIRouter(prefix="/api/dicom", tags=["AHOS 54.2 Real DICOM Viewer"])

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://ahos_admin:AHOS_2026_Strong_Password@127.0.0.1:5433/ahos_production"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@router.get("/health")
async def dicom_health():
    return {"status": "online", "phase": "AHOS 54.2"}

@router.get("/study/{study_uid}")
async def get_dicom_study(study_uid: str):
    with engine.connect() as conn:
        row = conn.execute(text("""
            SELECT patient_id, study_uid, modality, description,
                   ohif_url, dicom_study_uid, orthanc_id
            FROM radiology_studies
            WHERE study_uid = :uid
        """), {"uid": study_uid}).mappings().first()

    if not row:
        return {"status": "not_found", "study_uid": study_uid}

    study = dict(row)

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
        "study": study
    }
