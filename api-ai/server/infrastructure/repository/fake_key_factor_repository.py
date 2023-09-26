from typing import Optional

from injector import inject

from server.domain.entity.key_factor import KeyFactor
from server.domain.repository.key_factor_repository import KeyFactorRepository
from server.infrastructure.repository.helper.fake_datasources import FakeDatasources
from server.lib.list_utils import first


class FakeKeyFactorRepository(KeyFactorRepository):
    @inject
    def __init__(self, fake_datasources: FakeDatasources):
        self._key_factors = fake_datasources.get(KeyFactor, 'key_factors')

    def get_key_factor_by_id(self, key_factor_id: str) -> Optional[KeyFactor]:
        return first(self._key_factors, lambda c: c.id == key_factor_id)
