from abc import (
    ABC,
    abstractmethod,
)

from sqlalchemy import (
    Result,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def get_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result: "Result" = await self.session.execute(select(self.model))
        return [item.to_read_model() for item in list(result.scalars().all())]
