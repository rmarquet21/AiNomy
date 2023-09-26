from typing import Optional

from injector import inject

from server.domain.datastore import Datastore
from server.domain.entity.key_factor import KeyFactor
from server.domain.repository.key_factor_repository import KeyFactorRepository
from server.infrastructure.model.base import KeyFactorModel
from server.lib import attr_mapping


class DatabaseKeyFactorRepository(KeyFactorRepository):

    @inject
    def __init__(self, datastore: Datastore):
        self.datastore = datastore

    def get_key_factor_by_id(self, key_factor_id: str) -> Optional[KeyFactor]:
        key_factor = self.datastore.session.query(KeyFactorModel) \
            .filter(KeyFactorModel.id == key_factor_id) \
            .first()

        if key_factor is None:
            return None

        return attr_mapping.to_entity(KeyFactor, key_factor)
