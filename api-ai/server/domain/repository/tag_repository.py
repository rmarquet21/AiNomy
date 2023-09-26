from abc import abstractmethod
from typing import Optional

from server.domain.entity.tag import Tag


class TagRepository:

    @abstractmethod
    def get_tag_by_id(self, tag_id: str) -> Optional[Tag]:
        """
        Get the details of the tag.

        :param tag_id: The tag id.
        :return: The details of the tag.
        """
        raise NotImplementedError()
