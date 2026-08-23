from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
import shutil
import uuid
import numpy as np
from PIL import Image
import pydicom

router = APIRouter(prefix="/ai-ultrasound-x/dicom", tags=["AI Ultrasound X DICOM"])

UPLOAD_DIR = Path("uploaded_dicom")
PREVIEW_DIR = Path("generated_dicom_previews")

UPLOAD_DIR.mkdir(exist_ok=True)
PREVIEW_DIR.mkdir(exist_ok=True)


def safe_value(value):
    try:
        return str(value)
    except Exception:
        return None


def dicom_to_png(ds, output_path: Path):
    pixel_array = ds.pixel_array.astype(float)

    if pixel_array.ndim == 3:
        pixel_array = pixel_array[0]

    pixel_array = pixel_array - np.min(pixel_array)
    if np.max(pixel_array) > 0:
        pixel_array = pixel_array / np.max(pixel_array)

    image_array = (pixel_array * 255).astype(np.uint8)
    image = Image.fromarray(image_array)
    image.save(output_path)

    return output_path


@router.post("/upload")
async def upload_dicom(file: UploadFile = File(...)):
    file_id = f"DICOM-{uuid.uuid4().hex[:8]}"
    dicom_path = UPLOAD_DIR / f"{file_id}.dcm"
    preview_path = PREVIEW_DIR / f"{file_id}.png"

    with dicom_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ds = pydicom.dcmread(str(dicom_path))
        dicom_to_png(ds, preview_path)

        metadata = {
            "patient_name": safe_value(getattr(ds, "PatientName", "")),
            "patient_id": safe_value(getattr(ds, "PatientID", "")),
            "modality": safe_value(getattr(ds, "Modality", "")),
            "study_date": safe_value(getattr(ds, "StudyDate", "")),
            "study_description": safe_value(getattr(ds, "StudyDescription", "")),
            "series_description": safe_value(getattr(ds, "SeriesDescription", "")),
            "manufacturer": safe_value(getattr(ds, "Manufacturer", "")),
            "rows": safe_value(getattr(ds, "Rows", "")),
            "columns": safe_value(getattr(ds, "Columns", "")),
        }

        return {
            "status": "success",
            "message": "DICOM uploaded and preview generated",
            "file_id": file_id,
            "uploaded_at": datetime.utcnow().isoformat(),
            "dicom_path": str(dicom_path),
            "preview_url": f"/ai-ultrasound-x/dicom/preview/{file_id}",
            "metadata": metadata,
            "ai_status": "ready_for_real_inference"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": "Failed to process DICOM file",
            "error": str(e),
            "file_id": file_id
        }


@router.get("/preview/{file_id}")
def get_dicom_preview(file_id: str):
    preview_path = PREVIEW_DIR / f"{file_id}.png"

    if not preview_path.exists():
        return {
            "status": "not_found",
            "message": "Preview image not found"
        }

    return FileResponse(
        path=str(preview_path),
        media_type="image/png",
        filename=f"{file_id}.png"
    )
