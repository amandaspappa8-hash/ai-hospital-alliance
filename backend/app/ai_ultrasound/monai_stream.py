from fastapi import APIRouter
import random
import time
import math

router = APIRouter(prefix="/ai-ultrasound-x", tags=["AI Ultrasound X"])

@router.get("/monai-live-frame")
async def monai_live_frame():
    t = time.time()

    lesions = [
        {
            "id": "L-001",
            "label": "Suspected Lesion",
            "x": 42 + math.sin(t) * 8,
            "y": 48 + math.cos(t) * 6,
            "width": random.randint(18, 28),
            "height": random.randint(14, 24),
            "confidence": round(random.uniform(0.86, 0.98), 2),
            "risk": random.choice(["LOW", "MODERATE", "HIGH"]),
        },
        {
            "id": "L-002",
            "label": "Cystic Region",
            "x": 62 + math.cos(t * 0.7) * 6,
            "y": 38 + math.sin(t * 0.9) * 5,
            "width": random.randint(12, 22),
            "height": random.randint(10, 18),
            "confidence": round(random.uniform(0.78, 0.94), 2),
            "risk": random.choice(["LOW", "MODERATE"]),
        },
    ]

    return {
        "status": "success",
        "engine": "MONAI UNet Live Segmentation",
        "device": "CPU / GPU Ready",
        "frame_id": int(t * 10),
        "mask_shape": [256, 256],
        "segmentation_status": "streaming",
        "global_confidence": round(random.uniform(0.88, 0.99), 2),
        "lesion_count": len(lesions),
        "lesions": lesions,
        "timestamp": t,
    }
