from flask_login import current_user
from flask import current_app

from sqlalchemy.orm import Session

from datetime import date

from app.models import Task, User, File
from app.helpers import decode, upload_files, get_files_directory
from app.database import engine

from datetime import datetime

import os, shutil


class TaskServiceLayer:
    def __init__(self, session):
        self.session = session

    def create(self, form, title: str, deadline: date, description: str = ""):
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
            session.commit()

            if form.files.data:
                upload_dir = get_files_directory(current_user.id, task.id)
                os.makedirs(upload_dir, exist_ok=True)

                upload_files(form, task, File, upload_dir, session)

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

            upload_dir = get_files_directory(current_user.id, task.id)

            if task:
                task.is_deleted = True
                task.deleted_at = datetime.now()

                if task.files:
                    for file in task.files:
                        file.is_deleted = True
                        file.deleted_at = datetime.now()

                if os.path.exists(upload_dir):
                    shutil.rmtree(upload_dir)

    @staticmethod
    def get_task_data(task_id):
        t_id = decode(task_id)

        with Session(engine) as session:
            task = session.get(Task, t_id)

            return task
