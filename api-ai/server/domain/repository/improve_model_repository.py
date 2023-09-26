from abc import abstractmethod

from server.domain.entity.improve_model import ImproveModel


class ImproveModelRepository:
    @abstractmethod
    def save_improve_model(self, improve_model: ImproveModel) -> ImproveModel:
        """
        Save the image and the prediction in the database.

        :param improve_model: ImproveModel
        """
        raise NotImplementedError()
