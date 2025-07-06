from flask_login import current_user

from sqlalchemy.orm import Session

from datetime import date

from app.models import Task, User
from app.helpers import decode
from app.database import engine


class TaskServiceLayer:
    def __init__(self, session):
        self.session = session

    def create(self, title: str, deadline: date, description: str = ""):
        task = Task(
            title=title,
            deadline=deadline,
            description=description,
            status=1
        )

        with self.session() as session:
            user = session.get(User, current_user.id)
            task.user = user
            session.add(task)

    def update(self, task_id, title: str, deadline: str, description: str, status: int):
        tid = decode(task_id)

        with self.session() as session:
            task = session.get(Task, tid)

            if task:
                task.title = title
                task.deadline = deadline
                task.description = description
                task.status = status

    def delete(self, task_id):
        tid = decode(task_id)

        with self.session() as session:
            task = session.get(Task, tid)

            if task:
                task.is_deleted = True

    @staticmethod
    def get_task_data(task_id):
        t_id = decode(task_id)

        with Session(engine) as session:
            task = session.get(Task, t_id)

            return task
