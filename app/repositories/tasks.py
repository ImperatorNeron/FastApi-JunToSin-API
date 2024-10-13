from app.models.tasks import Task
from app.utils.sql_repository import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
