from monai.networks.nets import UNet
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = UNet(
    spatial_dims=2,
    in_channels=1,
    out_channels=1,
    channels=(16, 32, 64, 128),
    strides=(2, 2, 2),
    num_res_units=2,
).to(device)

def get_model_info():
    return {
        "model": "MONAI UNet",
        "device": device,
        "status": "initialized"
    }

if __name__ == "__main__":
    print(get_model_info())
