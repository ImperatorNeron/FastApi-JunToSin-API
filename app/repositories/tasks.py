from app.models.tasks import Task
from app.utils.repositories import SQLAlchemyRepository


class TaskRepository(SQLAlchemyRepository):
    model = Task
