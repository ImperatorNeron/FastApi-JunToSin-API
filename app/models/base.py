from sqlalchemy import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
)

from app.settings.settings import settings


class BaseModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention=settings.database.naming_convention)

    @declared_attr.directive
    def __tablename__(self) -> str:
        table_title = self.__name__.lower()
        if table_title.endswith("y"):
            return f"{table_title[:-1]}ies"
        if table_title.endswith(("s", "x", "z", "ch", "sh")):
            return f"{table_title}es"
        return f"{table_title}s"

    # TODO: add to_read_model abstract class
