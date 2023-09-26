from injector import inject

from server.domain.datastore import Datastore
from server.domain.entity.improve_model import ImproveModel
from server.domain.repository.improve_model_repository import ImproveModelRepository
from server.infrastructure.model.base import PredictionErrorModel
from server.lib import attr_mapping


class DatabaseImproveModelRepository(ImproveModelRepository):
    @inject
    def __init__(self, datastore: Datastore):
        self.datastore = datastore

    def save_improve_model(self, improve_model: ImproveModel) -> ImproveModel:
        model = attr_mapping.create_model(PredictionErrorModel, improve_model)
        self.datastore.session.add(model)
        self.datastore.session.commit()

        return model
