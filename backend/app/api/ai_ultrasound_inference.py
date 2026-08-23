from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path
from datetime import datetime
import numpy as np
import pydicom
from PIL import Image, ImageFilter
import torch
from monai.networks.nets import UNet

router = APIRouter(prefix="/ai-ultrasound-x/inference", tags=["AI Ultrasound X Inference"])

UPLOAD_DIR = Path("uploaded_dicom")
OUTPUT_DIR = Path("generated_inference")
OUTPUT_DIR.mkdir(exist_ok=True)

device = torch.device("cpu")

model = UNet(
    spatial_dims=2,
    in_channels=1,
    out_channels=1,
    channels=(16, 32, 64),
    strides=(2, 2),
    num_res_units=2,
).to(device)

model.eval()

def normalize_image(arr):
    arr = arr.astype(np.float32)
    arr = arr - np.min(arr)
    if np.max(arr) > 0:
        arr = arr / np.max(arr)
    return arr

def extract_first_frame(ds):
    arr = ds.pixel_array
    if arr.ndim == 3:
        arr = arr[0]
    return arr

def create_heatmap(mask, output_path):
    mask = normalize_image(mask)
    heat = (mask * 255).astype(np.uint8)
    img = Image.fromarray(heat).convert("L")
    img = img.filter(ImageFilter.GaussianBlur(radius=5))
    color = Image.new("RGBA", img.size, (255, 0, 90, 0))
    color.putalpha(img)
    color.save(output_path)

def analyze_mask(mask):
    threshold = float(mask.mean() + mask.std())
    binary = mask > threshold
    ys, xs = np.where(binary)

    if len(xs) == 0 or len(ys) == 0:
        return {
            "lesion_detected": False,
            "confidence": 0.0,
            "lesion_area": 0,
            "center_x": None,
            "center_y": None,
            "bbox": None,
            "risk_level": "LOW"
        }

    area = int(binary.sum())
    center_x = int(xs.mean())
    center_y = int(ys.mean())

    bbox = {
        "x_min": int(xs.min()),
        "y_min": int(ys.min()),
        "x_max": int(xs.max()),
        "y_max": int(ys.max()),
    }

    confidence = float(np.clip(mask.max(), 0.0, 1.0))

    if area > 3000:
        risk = "HIGH"
    elif area > 1000:
        risk = "MODERATE"
    else:
        risk = "LOW"

    return {
        "lesion_detected": True,
        "confidence": round(confidence, 4),
        "lesion_area": area,
        "center_x": center_x,
        "center_y": center_y,
        "bbox": bbox,
        "risk_level": risk
    }

@router.get("/run/{file_id}")
def run_inference(file_id: str):
    dicom_path = UPLOAD_DIR / f"{file_id}.dcm"

    if not dicom_path.exists():
        return {
            "status": "not_found",
            "message": "DICOM file not found",
            "file_id": file_id
        }

    try:
        ds = pydicom.dcmread(str(dicom_path))
        frame = extract_first_frame(ds)
        frame = normalize_image(frame)

        image = Image.fromarray((frame * 255).astype(np.uint8)).resize((256, 256))
        arr = np.array(image).astype(np.float32) / 255.0
        tensor = torch.tensor(arr).unsqueeze(0).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor)
            mask = torch.sigmoid(output).cpu().numpy()[0, 0]

        heatmap_path = OUTPUT_DIR / f"{file_id}_heatmap.png"
        create_heatmap(mask, heatmap_path)
        analysis = analyze_mask(mask)

        return {
            "status": "success",
            "file_id": file_id,
            "model": "MONAI UNet Prototype",
            "device": "cpu",
            "created_at": datetime.utcnow().isoformat(),
            "heatmap_url": f"/generated_inference/{file_id}_heatmap.png",
            "analysis": analysis,
            "note": "Prototype inference. Not for clinical diagnosis."
        }

    except Exception as e:
        return {
            "status": "error",
            "file_id": file_id,
            "message": "Inference failed",
            "error": str(e)
        }

@router.get("/heatmap/{file_id}")
def get_heatmap(file_id: str):
    heatmap_path = OUTPUT_DIR / f"{file_id}_heatmap.png"

    if not heatmap_path.exists():
        return {
            "status": "not_found",
            "message": "Heatmap not found"
        }

    return FileResponse(
        path=str(heatmap_path),
        media_type="image/png",
        filename=f"{file_id}_heatmap.png"
    )

def extract_multi_lesions(mask, min_area: int = 80):
    from scipy import ndimage

    threshold = float(mask.mean() + mask.std())
    binary = mask > threshold

    labeled, num_features = ndimage.label(binary)
    objects = ndimage.find_objects(labeled)

    lesions = []

    for idx, slc in enumerate(objects, start=1):
        if slc is None:
            continue

        region = labeled[slc] == idx
        area = int(region.sum())

        if area < min_area:
            continue

        y_slice, x_slice = slc

        y_min = int(y_slice.start)
        y_max = int(y_slice.stop)
        x_min = int(x_slice.start)
        x_max = int(x_slice.stop)

        ys, xs = np.where(labeled == idx)

        if len(xs) == 0 or len(ys) == 0:
            continue

        center_x = int(xs.mean())
        center_y = int(ys.mean())

        region_values = mask[labeled == idx]
        confidence = float(np.clip(region_values.max(), 0.0, 1.0))

        if area > 3000:
            risk = "HIGH"
        elif area > 1000:
            risk = "MODERATE"
        else:
            risk = "LOW"

        lesions.append({
            "tracking_id": f"L-{len(lesions)+1:03d}",
            "confidence": round(confidence, 4),
            "risk_level": risk,
            "area": area,
            "center_x": center_x,
            "center_y": center_y,
            "bbox": {
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max,
            },
            "neural_class": f"{risk}_PATHOLOGY_REGION",
            "tracking_status": "ACTIVE"
        })

    lesions = sorted(
        lesions,
        key=lambda x: (x["risk_level"] == "HIGH", x["area"]),
        reverse=True
    )

    return lesions


@router.get("/multi/{file_id}")
def run_multi_lesion_inference(file_id: str):
    dicom_path = UPLOAD_DIR / f"{file_id}.dcm"

    if not dicom_path.exists():
        return {
            "status": "not_found",
            "message": "DICOM file not found",
            "file_id": file_id
        }

    try:
        ds = pydicom.dcmread(str(dicom_path))
        frame = extract_first_frame(ds)
        frame = normalize_image(frame)

        image = Image.fromarray((frame * 255).astype(np.uint8)).resize((256, 256))
        arr = np.array(image).astype(np.float32) / 255.0
        tensor = torch.tensor(arr).unsqueeze(0).unsqueeze(0).to(device)

        with torch.no_grad():
            output = model(tensor)
            mask = torch.sigmoid(output).cpu().numpy()[0, 0]

        heatmap_path = OUTPUT_DIR / f"{file_id}_multi_heatmap.png"
        create_heatmap(mask, heatmap_path)

        lesions = extract_multi_lesions(mask)

        return {
            "status": "success",
            "file_id": file_id,
            "model": "MONAI UNet Multi-Lesion Prototype",
            "device": "cpu",
            "created_at": datetime.utcnow().isoformat(),
            "heatmap_url": f"/generated_inference/{file_id}_multi_heatmap.png",
            "lesion_count": len(lesions),
            "lesions": lesions,
            "global_assessment": {
                "tracking_mode": "AUTONOMOUS_MULTI_TARGET",
                "highest_risk": lesions[0]["risk_level"] if lesions else "LOW",
                "system_status": "MULTI_LESION_TRACKING_ACTIVE" if lesions else "NO_ACTIVE_TARGETS"
            },
            "note": "Prototype multi-lesion AI tracking. Not for clinical diagnosis."
        }

    except Exception as e:
        return {
            "status": "error",
            "file_id": file_id,
            "message": "Multi-lesion inference failed",
            "error": str(e)
        }
