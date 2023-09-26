from server.domain.repository.prediction_pneumonia_repository import PredictionPneumoniaRepository


class FakePredictionPneumoniaRepository(PredictionPneumoniaRepository):

    def get_prediction_pneumonia(self, img_bytes: bytes) -> dict:
        return {
            "prediction": "pneumonia",
        }
