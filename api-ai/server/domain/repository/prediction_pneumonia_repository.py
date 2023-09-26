from abc import abstractmethod


class PredictionPneumoniaRepository:

    @abstractmethod
    def get_prediction_pneumonia(self, img_bytes: bytes) -> dict:
        """
        Get the prediction of pneumonia from the given image.

        :param img_bytes: The image in bytes.
        :return: The prediction of pneumonia.
        """
        raise NotImplementedError()
