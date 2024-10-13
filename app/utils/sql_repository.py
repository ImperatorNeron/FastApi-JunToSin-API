from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from pydantic import BaseModel
from sqlalchemy import (
    Result,
    select,
    update,
)
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all():
        raise NotImplementedError

    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def update_one():
        raise NotImplementedError

    @abstractmethod
    async def delete_one():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def __get_one_model(self, item_id: int):
        item = await self.session.get(self.model, item_id)
        return item

    async def get_all(self):
        result: "Result" = await self.session.execute(select(self.model))
        return [item.to_read_model() for item in list(result.scalars().all())]

    async def add_one(self, item_in: BaseModel):
        item = self.model(**item_in.model_dump())
        self.session.add(item)
        await self.session.commit()
        return item.to_read_model()

    async def get_one(self, item_id: int):
        item = await self.__get_one_model(item_id=item_id)
        return item.to_read_model()

    async def get_one_by_field(self, field_name: str, value):
        field = getattr(self.model, field_name, None)
        result = await self.session.execute(select(self.model).where(field == value))
        item = result.scalars().first()
        return item.to_read_model() if item else None

    async def update_one(self, item_id: int, item_in: BaseModel):
        item = await self.__get_one_model(item_id=item_id)

        for key, value in item_in.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        await self.session.commit()
        return item.to_read_model()

    async def update_one_by_field(
        self, field_name: str, field_value: Any, item_in: BaseModel,
    ):
        field = getattr(self.model, field_name)

        result: "Result" = await self.session.execute(
            update(self.model)
            .where(field == field_value)
            .values(**item_in.model_dump(exclude_unset=True))
            .returning(self.model),
        )
        await self.session.commit()
        return result.scalars().first().to_read_model()

    async def delete_one(self, item_id: int):
        item = await self.__get_one_model(item_id=item_id)
        await self.session.delete(item)
        await self.session.commit()
