from server.domain.repository.prediction_alzheimer_repository import PredictionAlzheimerRepository


class FakePredictionAlzheimerRepository(PredictionAlzheimerRepository):
    def get_prediction_alzheimer(self, img_bytes: bytes) -> list:
        return [{'label': 'label', 'probability': 0.5}]
