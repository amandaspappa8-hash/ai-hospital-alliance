import torch
from monai.networks.nets import UNet

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def get_model():
    model = UNet(
        spatial_dims=2,
        in_channels=1,
        out_channels=1,
        channels=(16, 32, 64, 128),
        strides=(2, 2, 2),
        num_res_units=2,
    )
    return model.to(device)
