from typing import Any

import sqlalchemy
from sqlalchemy.ext.declarative import declared_attr


@sqlalchemy.orm.as_declarative()
class Base:
    id: Any
    __name__: str

    # noinspection PyMethodParameters
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
