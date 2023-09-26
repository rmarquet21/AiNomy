import io
import os

import torchvision
import torchvision.transforms as transform

import torch
import torch.nn as nn

from PIL import Image

from server import ROOT_DIR
from server.domain.repository.prediction_alzheimer_repository import PredictionAlzheimerRepository


class ModelAlzheimer(nn.Module):
    def __init__(self):
        super(ModelAlzheimer, self).__init__()

        # Load pre-trained ResNet50 model
        model = torchvision.models.resnet50(pretrained=True)

        num_ftrs = model.fc.in_features
            
        for param in model.fc.parameters():
            param.require_grad = False
            
        # Modify the output layer to have 4 labels
        model.fc = torch.nn.Sequential(
            torch.nn.Dropout(0, inplace=True),
            torch.nn.Linear(num_ftrs, 4),
        )

        self.model = model

    def forward(self, x):
        out = self.model(x)
        return out


class ModelPredictionAlzheimerRepository(PredictionAlzheimerRepository):
    def __init__(self):
        # load model
        self.model = ModelAlzheimer()
        self.model.load_state_dict(torch.load(os.path.join(ROOT_DIR, 'models', 'alzheimer.pt'), map_location=torch.device('cpu')))
        self.model.eval()

        self.classes = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']

    def get_prediction_alzheimer(self, img_bytes: bytes) -> list:
        img = self.transform_image(img_bytes)
        outputs = self.model(img)

        probabilities = outputs.softmax(dim=1).tolist()[0]

        result = []
        for i in range(len(self.classes)):
            result.append({'label': self.classes[i], 'probability': round(probabilities[i], 2) * 100})

        return result

    @staticmethod
    def transform_image(image_bytes: bytes):
        my_transforms = transform.Compose([
            transform.Resize((224, 224)),
            transform.ToTensor(),
            transform.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')
        return my_transforms(image).unsqueeze(0)
