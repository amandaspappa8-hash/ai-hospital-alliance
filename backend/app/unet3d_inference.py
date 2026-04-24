import random

def segment_3d(volume=None) -> dict:
    return {"success": True, "message": "3D segmentation demo", "output_shape": [1,1,32,64,64], "volume_ml": round(random.uniform(5, 120), 1)}
