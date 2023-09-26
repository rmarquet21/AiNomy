import io
import os

import torchvision.transforms as transform
from PIL import Image
from transformers import AutoModelForImageClassification

from server import ROOT_DIR
from server.domain.repository.prediction_pneumonia_repository import PredictionPneumoniaRepository


class ModelPredictionPneumoniaRepository(PredictionPneumoniaRepository):

    def __init__(self):
        self.model = AutoModelForImageClassification.from_pretrained(os.path.join(ROOT_DIR, "models", "pneumonia"))

    def get_prediction_pneumonia(self, img_bytes: bytes):
        img = self.transform_image(img_bytes)
        outputs = self.model(img)

        # get logits and transform to probabilities on 100%
        logits = outputs.logits
        probabilities = logits.softmax(dim=1).tolist()[0]

        # get labels
        labels = self.model.config.id2label

        # create list of dicts
        result = []
        for i in range(len(labels)):
            result.append({'label': labels[i], 'probability': round(probabilities[i], 2) * 100})

        return result

    @staticmethod
    def transform_image(image_bytes: bytes):
        my_transforms = transform.Compose([transform.Resize(224),
                                           transform.CenterCrop(224),
                                           transform.ToTensor(),
                                           ])
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')
        return my_transforms(image).unsqueeze(0)
