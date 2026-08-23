import sys
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image

MODEL_PATH = "models/rsna/rsna_resnet18_baseline.pt"

def load_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, 1)
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()
    return model

def predict(image_path):
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=3),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])

    img = Image.open(image_path).convert("L")
    x = transform(img).unsqueeze(0)

    model = load_model()

    with torch.no_grad():
        logit = model(x)
        prob = torch.sigmoid(logit).item()

    return {
        "image_path": image_path,
        "pneumonia_probability": round(prob, 4),
        "prediction": "PNEUMONIA_OPACITY" if prob >= 0.60 else "NO_PNEUMONIA_OPACITY",
        "risk_level": "HIGH" if prob >= 0.80 else "MODERATE" if prob >= 0.60 else "LOW"
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python infer_rsna_baseline.py <image_path>")
        sys.exit(1)

    result = predict(sys.argv[1])
    print(result)
