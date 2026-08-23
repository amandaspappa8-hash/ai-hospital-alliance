import cv2
import torch
import numpy as np
import torch.nn as nn
from pathlib import Path
from PIL import Image
from torchvision import models
from torchvision import transforms

MODEL_PATH = "models/rsna/rsna_resnet18_2000.pt"

HEATMAP_DIR = "reports/rsna/heatmaps"
OVERLAY_DIR = "reports/rsna/overlays"

Path(HEATMAP_DIR).mkdir(parents=True, exist_ok=True)
Path(OVERLAY_DIR).mkdir(parents=True, exist_ok=True)


def load_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(
        model.fc.in_features,
        1
    )

    model.load_state_dict(
        torch.load(
            MODEL_PATH,
            map_location="cpu"
        )
    )

    model.eval()

    return model


def preprocess(image_path):

    img = Image.open(
        image_path
    ).convert("L")

    transform = transforms.Compose([
        transforms.Grayscale(
            num_output_channels=3
        ),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])

    x = transform(img).unsqueeze(0)

    return x


def generate_gradcam(image_path):

    model = load_model()

    target_layer = model.layer4[-1]

    gradients = []
    activations = []

    def forward_hook(module, inp, out):
        activations.append(out)

    def backward_hook(module, grad_in, grad_out):
        gradients.append(grad_out[0])

    target_layer.register_forward_hook(
        forward_hook
    )

    target_layer.register_full_backward_hook(
        backward_hook
    )

    x = preprocess(image_path)

    output = model(x)

    prob = torch.sigmoid(
        output
    )[0].item()

    model.zero_grad()

    output.backward()

    grads = gradients[0]
    acts = activations[0]

    weights = grads.mean(
        dim=(2, 3),
        keepdim=True
    )

    cam = (
        weights * acts
    ).sum(
        dim=1
    ).squeeze()

    cam = cam.detach().numpy()

    cam = np.maximum(cam, 0)

    cam = cam / (
        cam.max() + 1e-8
    )

    return prob, cam


def save_heatmap(image_path):

    prob, cam = generate_gradcam(
        image_path
    )

    original = cv2.imread(
        image_path
    )

    original = cv2.resize(
        original,
        (224, 224)
    )

    heatmap = cv2.resize(
        cam,
        (224, 224)
    )

    heatmap = np.uint8(
        heatmap * 255
    )

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    overlay = cv2.addWeighted(
        original,
        0.5,
        heatmap_color,
        0.5,
        0
    )

    name = Path(
        image_path
    ).stem

    heatmap_path = (
        f"{HEATMAP_DIR}/{name}.png"
    )

    overlay_path = (
        f"{OVERLAY_DIR}/{name}.png"
    )

    cv2.imwrite(
        heatmap_path,
        heatmap_color
    )

    cv2.imwrite(
        overlay_path,
        overlay
    )

    return {
        "probability": round(
            prob,
            4
        ),
        "heatmap": heatmap_path,
        "overlay": overlay_path
    }
