from abc import abstractmethod


class PredictionAlzheimerRepository:
    @abstractmethod
    def get_prediction_alzheimer(self, img_bytes: bytes) -> dict:
        """
        Get the prediction of alzheimer from the given image.

        :param img_bytes: The image in bytes.
        :return: The prediction of alzheimer.
        """
        raise NotImplementedError()
