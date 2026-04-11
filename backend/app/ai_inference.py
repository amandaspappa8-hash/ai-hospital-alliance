from pathlib import Path
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Linear(64, 2)

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)
        return self.classifier(x)

model = SimpleCNN().to(device)
MODEL_PATH = Path("backend/app/model.pth")
MODEL_LOADED = False

if MODEL_PATH.exists():
    try:
        state = torch.load(str(MODEL_PATH), map_location=device)
        model.load_state_dict(state)
        model.eval()
        MODEL_LOADED = True
        print(f"[AI] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"[AI] Failed to load model: {e}")
else:
    print(f"[AI] Warning: model file not found at {MODEL_PATH}. AI image inference disabled.")

transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
])

CLASS_NAMES = ["Normal", "Abnormal"]

def predict_image(image_path: str):
    if not MODEL_LOADED:
        return {
            "success": False,
            "error": "Model file not available",
            "details": f"Missing model at {MODEL_PATH}"
        }

    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image)
            probs = torch.softmax(outputs, dim=1)
            pred = torch.argmax(probs, dim=1).item()
            confidence = float(probs[0][pred].item())

        return {
            "success": True,
            "prediction": CLASS_NAMES[pred],
            "confidence": round(confidence, 4)
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Prediction failed",
            "details": str(e)
        }
