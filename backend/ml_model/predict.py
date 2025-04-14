import json

import torchvision.transforms as transforms
from PIL import Image
import torch
from torchvision import models
import torch.nn as nn

model_resnet = models.resnet50(pretrained=False)

num_features = model_resnet.fc.in_features
model_resnet.fc = nn.Linear(num_features, 38)

model_resnet.load_state_dict(
    torch.load(
        "ml_model/Best-Resnet50-from-scratch-with-New-Plant-Disease.pth",
        map_location=torch.device("cpu"),
    )
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_resnet = model_resnet.to(device)
model_resnet.eval()


transforms = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

with open("ml_model/class_disease.json", "r", encoding="utf-8") as f:
    class_names = json.load(f)


def predict(
    image_path: str,
    model=model_resnet,
    device="cuda" if torch.cuda.is_available() else "cpu",
):
    model.eval()
    image = Image.open(image_path).convert("RGB")
    image = transforms(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)

    print(predicted.item())
    return class_names[predicted.item()]


if __name__ == "__main__":
    print(
        predict(
            "/home/traktor/ck/PlantDiseaseDetector/backend/ml_model/TomatoYellowCurlVirus2.jpeg",
            model_resnet,
        )
    )
