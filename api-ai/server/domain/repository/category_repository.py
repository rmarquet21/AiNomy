from abc import abstractmethod
from typing import Optional

from server.domain.entity.category import Category


class CategoryRepository:

    @abstractmethod
    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        """
        Get the details of the category.

        :param category_id: The category id.
        :return: The details of the category.
        """
        raise NotImplementedError()
