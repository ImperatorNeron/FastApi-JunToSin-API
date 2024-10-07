from abc import (
    ABC,
    abstractmethod,
)

from pydantic import BaseModel
from sqlalchemy import (
    Result,
    select,
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
        item = await self.session.execute(select(self.model).where(field == value))
        return item.scalars().first().to_read_model()

    async def update_one(self, item_id: int, item_in: BaseModel):
        item = await self.__get_one_model(item_id=item_id)

        for key, value in item_in.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        await self.session.commit()
        return item.to_read_model()

    async def delete_one(self, item_id: int):
        item = await self.__get_one_model(item_id=item_id)
        await self.session.delete(item)
        await self.session.commit()
