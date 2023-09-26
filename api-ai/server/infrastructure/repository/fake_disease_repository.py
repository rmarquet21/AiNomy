from typing import Optional

from injector import inject

from server.domain.entity.disease import Disease
from server.domain.repository.disease_repository import DiseaseRepository
from server.infrastructure.repository.helper.fake_datasources import FakeDatasources
from server.lib.list_utils import first


class FakeDiseaseRepository(DiseaseRepository):
    @inject
    def __init__(self, fake_datasources: FakeDatasources):
        self._diseases = fake_datasources.get(Disease, 'diseases')

    def get_disease_by_name(self, disease: str):
        return first(self._diseases, lambda d: d.name.lower() == disease.lower())

    def get_diseases(self):
        return self._diseases
