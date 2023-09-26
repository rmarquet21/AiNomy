from typing import Optional

from injector import inject

from server.domain.entity.tag import Tag
from server.domain.repository.tag_repository import TagRepository
from server.infrastructure.repository.helper.fake_datasources import FakeDatasources
from server.lib.list_utils import first


class FakeTagRepository(TagRepository):
    @inject
    def __init__(self, fake_datasources: FakeDatasources):
        self._tags = fake_datasources.get(Tag, 'tags')

    def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        return first(self._tags, lambda c: c.id == tag_id)
