import shutil
from pathlib import Path
import pydicom
import numpy as np
import cv2
from backend.app.ahos_41_0_4.clinical_report_2000 import generate_clinical_report
from backend.app.ahos_41_0_4.report_db_2000 import save_report
from backend.app.ahos_41_0_4.export_reports import export_pdf, export_json

UPLOAD_DIR = Path("uploads/rsna_dicom")
PNG_DIR = Path("uploads/rsna_png")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PNG_DIR.mkdir(parents=True, exist_ok=True)

def dicom_to_png(dicom_path: str):
    dcm = pydicom.dcmread(dicom_path)
    img = dcm.pixel_array.astype(np.float32)

    img = img - img.min()
    img = img / (img.max() + 1e-8)
    img = (img * 255).astype(np.uint8)
    img = cv2.resize(img, (224, 224))

    patient_id = getattr(dcm, "PatientID", Path(dicom_path).stem)
    out_path = PNG_DIR / f"{patient_id}.png"
    cv2.imwrite(str(out_path), img)

    return str(out_path)

def process_uploaded_dicom(src_path: str):
    src = Path(src_path)

    if not src.exists():
        raise FileNotFoundError(str(src))

    dst = UPLOAD_DIR / src.name

    if src.resolve() != dst.resolve():
        shutil.copy2(src, dst)

    png_path = dicom_to_png(str(dst))

    report = generate_clinical_report(png_path)
    saved = save_report(report)

    pdf_path = export_pdf(report)
    json_path = export_json(report)

    return {
        "dicom_file": str(dst),
        "png_file": png_path,
        "report": report,
        "database": saved,
        "exports": {
            "pdf": pdf_path,
            "json": json_path
        }
    }
