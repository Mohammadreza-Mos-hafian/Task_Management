from flask_login import current_user
from flask import current_app, send_from_directory, flash, redirect, url_for

from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from app.helpers import decode, paginate, upload_files, encode, get_files_directory
from app.models import File, Task
from app.database import engine

from datetime import datetime

import os, mimetypes


class FileServiceLayer:
    def __init__(self, session):
        self.session = session

    def create(self, task_id, form):
        tid = decode(task_id)

        with self.session() as session:
            task = session.get(Task, tid)

            upload_dir = get_files_directory(current_user.id, task.id)
            os.makedirs(upload_dir, exist_ok=True)

            return upload_files(form, task, File, upload_dir, session)

    def delete(self, file_id):
        fid = decode(file_id)

        with self.session() as session:
            file = session.get(File, fid)

            if file:
                file.is_deleted = True
                file.deleted_at = datetime.now()

                if os.path.exists(file.file_path):
                    os.remove(file.file_path)

    def download(self, file_id):
        fid = decode(file_id)
        task_id_encode = ""

        with self.session() as session:
            file = session.get(File, fid)
            task_id_encode = encode(file.task.id)

            if file and file.task.user_id == current_user.id:
                directory = os.path.dirname(file.file_path)
                filename = os.path.basename(file.file_path)

                file_ext = os.path.splitext(filename)[1]
                original_name = file.original_name + file_ext

                mime_type, _ = mimetypes.guess_type(file.file_path)

                if os.path.exists(file.file_path):
                    return send_from_directory(
                        directory=directory,
                        path=filename,
                        as_attachment=True,
                        download_name=original_name,
                        mime_type=mime_type or "application/octet-stream"
                    )

        flash("File not found", "danger")
        return redirect(url_for("file.index_view", id=task_id_encode))

    def get_files(self, task_id):
        tid = decode(task_id)

        with self.session() as session:
            stmt = (
                select(File)
                .where(and_(
                    File.task_id == tid,
                    File.is_deleted == False
                ))
            )

            return paginate(stmt)

    @staticmethod
    def get_task_data(file_id):
        fid = decode(file_id)

        with Session(engine) as session:
            file = session.get(File, fid)

            if file and file.task:
                return file.task

        return None
