from datetime import datetime
from typing import Optional

from server.domain.entity.base import Entity

import attr


@attr.s
class Disease(Entity):
    name: str = attr.ib()
    description: str = attr.ib()
    key_factors: list = attr.ib(default=[])
    category_id: int = attr.ib(default=None)
    tags: list = attr.ib(default=[])
    created_at: Optional[datetime] = attr.ib(default=None)
    updated_at: Optional[datetime] = attr.ib(default=None)
