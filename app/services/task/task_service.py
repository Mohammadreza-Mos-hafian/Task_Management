from flask_login import current_user

from datetime import date

from app.models import Task, User


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
