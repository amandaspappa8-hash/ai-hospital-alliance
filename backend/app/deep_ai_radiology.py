import torch
import numpy as np

# نموذج بسيط (placeholder)
class SimpleRadiologyModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = torch.nn.Flatten()
        self.fc = torch.nn.Linear(256*256, 2)

    def forward(self, x):
        x = self.flatten(x)
        return self.fc(x)

model = SimpleRadiologyModel()

def analyze_image(image_array):
    x = torch.tensor(image_array, dtype=torch.float32).unsqueeze(0)
    output = model(x)
    probs = torch.softmax(output, dim=1).detach().numpy()[0]

    return {
        "normal": float(probs[0]),
        "abnormal": float(probs[1])
    }
