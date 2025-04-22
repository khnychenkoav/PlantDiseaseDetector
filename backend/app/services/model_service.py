# services/model_service.py
import torch
from torchvision import models
import torch.nn as nn
import json
from PIL import Image
import torchvision.transforms as transforms


class ModelService:
    def __init__(self):
        self.model = None
        self.device = None
        self.class_names = None
        self.transforms = None

    def load_model(self):
        """Загрузка модели и ресурсов один раз"""
        self.model = models.resnet50(pretrained=False)
        num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(num_features, 38)

        self.model.load_state_dict(
            torch.load(
                "ml_model/Best-Resnet50-from-scratch-with-New-Plant-Disease.pth",
                map_location=torch.device("cpu"),
            )
        )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self.model.to(self.device)
        self.model.eval()

        self.transforms = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ]
        )

        with open("ml_model/class_disease.json", "r", encoding="utf-8") as f:
            self.class_names = json.load(f)

    def predict(self, image_path: str):
        """Выполнение предсказания"""
        image = Image.open(image_path).convert("RGB")
        image = self.transforms(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)

        return self.class_names[predicted.item()]


model_service = ModelService()
