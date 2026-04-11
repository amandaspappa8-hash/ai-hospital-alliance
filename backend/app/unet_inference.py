import torch
import numpy as np
from PIL import Image
from backend.app.unet_model import get_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = get_model()
model.load_state_dict(torch.load("backend/app/unet.pth", map_location=device))
model.eval()

def segment_image(path):
    img = Image.open(path).convert("L").resize((256,256))
    img = np.array(img) / 255.0

    x = torch.tensor(img).unsqueeze(0).unsqueeze(0).float().to(device)

    with torch.no_grad():
        pred = model(x)
        mask = torch.sigmoid(pred)[0][0].cpu().numpy()

    return mask.tolist()
