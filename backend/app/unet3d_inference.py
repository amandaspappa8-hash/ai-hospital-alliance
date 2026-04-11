from pathlib import Path
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Simple3DUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv3d(1, 8, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv3d(8, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv3d(16, 1, kernel_size=1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        return self.net(x)

model = Simple3DUNet().to(device)
MODEL_PATH = Path("backend/app/unet3d.pth")
MODEL_LOADED = False

if MODEL_PATH.exists():
    try:
        state = torch.load(str(MODEL_PATH), map_location=device)
        model.load_state_dict(state)
        model.eval()
        MODEL_LOADED = True
        print(f"[UNET3D] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"[UNET3D] Failed to load model: {e}")
else:
    print(f"[UNET3D] Warning: model file not found at {MODEL_PATH}. 3D segmentation disabled.")

def segment_3d(volume=None):
    if not MODEL_LOADED:
        return {
            "success": False,
            "error": "UNet3D model file not available",
            "details": f"Missing model at {MODEL_PATH}"
        }

    try:
        if volume is None:
            x = torch.randn(1, 1, 32, 64, 64).to(device)
        elif isinstance(volume, torch.Tensor):
            x = volume.to(device)
        else:
            x = torch.tensor(volume, dtype=torch.float32).to(device)

        with torch.no_grad():
            out = model(x)

        return {
            "success": True,
            "message": "3D segmentation completed",
            "output_shape": list(out.shape)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "3D segmentation failed",
            "details": str(e)
        }
