import os
import torch
import numpy as np
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torch import nn, optim
from .unet_model import get_model

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SegDataset(Dataset):
    def __init__(self, img_dir, mask_dir):
        self.imgs = os.listdir(img_dir)
        self.img_dir = img_dir
        self.mask_dir = mask_dir

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        img_path = os.path.join(self.img_dir, self.imgs[idx])
        mask_path = os.path.join(self.mask_dir, self.imgs[idx])

        img = Image.open(img_path).convert("L").resize((256,256))
        mask = Image.open(mask_path).convert("L").resize((256,256))

        img = np.array(img) / 255.0
        mask = np.array(mask) / 255.0

        img = torch.tensor(img).unsqueeze(0).float()
        mask = torch.tensor(mask).unsqueeze(0).float()

        return img, mask

def train():
    dataset = SegDataset("ai-data-seg/images", "ai-data-seg/masks")
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = get_model()
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(5):
        total_loss = 0
        for imgs, masks in loader:
            imgs, masks = imgs.to(device), masks.to(device)

            preds = model(imgs)
            loss = loss_fn(preds, masks)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}")

    torch.save(model.state_dict(), "backend/app/unet.pth")
    print("UNet model saved!")

if __name__ == "__main__":
    train()
