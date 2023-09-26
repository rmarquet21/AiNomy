from abc import abstractmethod
from typing import Optional

from server.domain.entity.key_factor import KeyFactor


class KeyFactorRepository:

    @abstractmethod
    def get_key_factor_by_id(self, key_factor_id: str) -> Optional[KeyFactor]:
        """
        Get the details of the key factor.

        :param key_factor_id: The key factor id.
        :return: The details of the key factor.
        """
        raise NotImplementedError()
