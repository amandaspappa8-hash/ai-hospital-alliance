from pathlib import Path
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SimpleUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
        )
        self.decoder = nn.Sequential(
            nn.Conv2d(32, 16, 3, padding=1),
            nn.ReLU(),
            nn.Conv2d(16, 1, 1),
            nn.Sigmoid(),
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

model = SimpleUNet().to(device)
MODEL_PATH = Path("backend/app/unet.pth")
MODEL_LOADED = False

if MODEL_PATH.exists():
    try:
        state = torch.load(str(MODEL_PATH), map_location=device)
        model.load_state_dict(state)
        model.eval()
        MODEL_LOADED = True
        print(f"[UNET] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"[UNET] Failed to load model: {e}")
else:
    print(f"[UNET] Warning: model file not found at {MODEL_PATH}. Image segmentation disabled.")

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

def segment_image(image_path: str):
    if not MODEL_LOADED:
        return {
            "success": False,
            "error": "UNet model file not available",
            "details": f"Missing model at {MODEL_PATH}"
        }

    try:
        image = Image.open(image_path).convert("RGB")
        tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            mask = model(tensor)

        return {
            "success": True,
            "message": "Segmentation completed",
            "mask_shape": list(mask.shape)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Segmentation failed",
            "details": str(e)
        }
