from typing import Optional

from injector import inject

from server.domain.datastore import Datastore
from server.domain.entity.category import Category
from server.domain.repository.category_repository import CategoryRepository
from server.infrastructure.model.base import CategoryModel
from server.lib import attr_mapping


class DatabaseCategoryRepository(CategoryRepository):

    @inject
    def __init__(self, datastore: Datastore):
        self.datastore = datastore

    def get_category_by_id(self, category_id: str) -> Optional[Category]:
        category = self.datastore.session.query(CategoryModel) \
            .filter(CategoryModel.id == category_id) \
            .first()

        if category is None:
            return None

        return attr_mapping.to_entity(Category, category)
