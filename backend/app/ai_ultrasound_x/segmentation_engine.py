import numpy as np
import torch
from backend.app.ai_ultrasound_x.unet_model import model, device

def run_segmentation_demo():
    model.eval()

    with torch.no_grad():
        x = torch.rand(1, 1, 256, 256).to(device)
        y = model(x)
        mask = torch.sigmoid(y).cpu().numpy()[0, 0]

    confidence = float(np.mean(mask))
    lesion_area = int(np.sum(mask > 0.5))

    risk_level = "HIGH" if lesion_area > 32000 else "MODERATE" if lesion_area > 18000 else "LOW"

    return {
        "model": "MONAI UNet",
        "device": device,
        "mask_shape": list(mask.shape),
        "confidence": confidence,
        "lesion_area": lesion_area,
        "risk_level": risk_level,
        "segmentation_status": "completed"
    }
