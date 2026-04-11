import torch
from backend.app.unet3d_model import get_3d_model
from backend.app.dicom_3d import load_dicom_series

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = get_3d_model()
model.load_state_dict(torch.load("backend/app/unet3d.pth", map_location=device))
model.eval()

def segment_3d(folder):
    volume = load_dicom_series(folder)

    x = torch.tensor(volume).unsqueeze(0).unsqueeze(0).float().to(device)

    with torch.no_grad():
        pred = model(x)
        mask = torch.sigmoid(pred)[0][0].cpu().numpy()

    return mask.tolist()
