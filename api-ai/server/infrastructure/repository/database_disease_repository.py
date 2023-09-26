from typing import Optional

from injector import inject

from server.domain.datastore import Datastore
from server.domain.entity.disease import Disease
from server.domain.repository.disease_repository import DiseaseRepository
from server.infrastructure.model.base import DiseaseModel
from server.lib import attr_mapping


class DatabaseDiseaseRepository(DiseaseRepository):

    @inject
    def __init__(self, datastore: Datastore):
        self.datastore = datastore

    def get_disease_by_name(self, disease: str):
        disease = self.datastore.session.query(DiseaseModel) \
            .filter(DiseaseModel.name.ilike(disease)) \
            .first()

        if disease is None:
            return None

        return attr_mapping.to_entity(Disease, disease)

    def get_diseases(self):
        diseases = self.datastore.session.query(DiseaseModel).all()
        return [attr_mapping.to_entity(Disease, disease) for disease in diseases]
