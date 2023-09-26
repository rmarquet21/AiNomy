from typing import Optional

from injector import inject

from server.domain.entity.category import Category
from server.domain.repository.category_repository import CategoryRepository
from server.infrastructure.repository.helper.fake_datasources import FakeDatasources
from server.lib.list_utils import first


class FakeCategoryRepository(CategoryRepository):
    @inject
    def __init__(self, fake_datasources: FakeDatasources):
        self._categories = fake_datasources.get(Category, 'categories')

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        return first(self._categories, lambda c: c.id == category_id)
