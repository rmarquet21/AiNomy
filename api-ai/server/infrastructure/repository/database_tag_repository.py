from typing import Optional

from injector import inject

from server.domain.datastore import Datastore
from server.domain.entity.tag import Tag
from server.domain.repository.tag_repository import TagRepository
from server.infrastructure.model.base import TagModel
from server.lib import attr_mapping


class DatabaseTagRepository(TagRepository):

    @inject
    def __init__(self, datastore: Datastore):
        self.datastore = datastore

    def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        tag = self.datastore.session.query(TagModel) \
            .filter(TagModel.id == tag_id) \
            .first()

        if tag is None:
            return None

        return attr_mapping.to_entity(Tag, tag)
