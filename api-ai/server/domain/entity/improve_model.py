from datetime import datetime
from typing import Optional

import attr

from server.domain.entity.base import Entity


@attr.s
class ImproveModel(Entity):
    img_bytes: bytes = attr.ib()
    model_name: str = attr.ib()
    prediction: str = attr.ib()
    is_valid: bool = attr.ib()
    created_at: Optional[datetime] = attr.ib(default=None)
    updated_at: Optional[datetime] = attr.ib(default=None)
