from datetime import datetime
from typing import Optional

import attr

from server.domain.entity.base import Entity


@attr.s
class Category(Entity):
    name: str = attr.ib()
    created_at: Optional[datetime] = attr.ib(default=None)
    updated_at: Optional[datetime] = attr.ib(default=None)
