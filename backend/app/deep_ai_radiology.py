from pathlib import Path
import torch
import numpy as np
from PIL import Image

from .unet_model import get_model

MODEL_PATH = Path(__file__).with_name("unet.pth")
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "uploads" / "radiology_ai"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

_model = None

def load_model():
    global _model
    if _model is None:
        _model = get_model()
        _model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
        _model.eval()
    return _model

def analyze_image(img):
    if img is None:
        return {
            "abnormal": 0.0,
            "normal": 1.0,
            "finding": "No readable image found",
            "inference": "skipped"
        }

    model = load_model()

    arr = np.asarray(img, dtype="float32")
    if arr.ndim == 3:
        arr = arr.mean(axis=2)

    x = torch.tensor(arr).unsqueeze(0).unsqueeze(0)

    with torch.no_grad():
        mask = torch.sigmoid(model(x))[0, 0].numpy()

    abnormal = round(float(mask.mean()), 3)
    normal = round(1 - abnormal, 3)

    mask_path = OUTPUT_DIR / "last_unet_mask.png"
    heatmap_path = OUTPUT_DIR / "last_heatmap_overlay.png"

    Image.fromarray((mask * 255).astype("uint8")).save(mask_path)

    base = Image.fromarray((arr * 255).astype("uint8")).convert("RGBA").resize((128, 128))
    mask_img = Image.open(mask_path).convert("L").resize((128, 128))
    heat = Image.new("RGBA", base.size, (255, 0, 0, 0))
    heat.putalpha(mask_img.point(lambda p: int(p * 0.45)))
    Image.alpha_composite(base, heat).save(heatmap_path)

    return {
        "abnormal": abnormal,
        "normal": normal,
        "finding": "Real image → UNet mask + heatmap generated",
        "model_path": str(MODEL_PATH),
        "mask_path": str(mask_path),
        "heatmap_path": str(heatmap_path),
        "inference": "torch_unet_cpu"
    }
