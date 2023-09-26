from typing import Optional

import attr


@attr.s
class Entity:
    """
    Ce type d'objet a une identité. Elle est portée par le champs `id` qui représente
    la clé primaire dans la base de donnée
    """
    id: Optional[int] = attr.ib(default=None, kw_only=True)


class Record:
    """
    Ce type d'objet n'a pas d'identité. Il est stocké en base sous la forme
    d'un document json.
    """
