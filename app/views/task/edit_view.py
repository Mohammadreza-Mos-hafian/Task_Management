from flask.views import MethodView
from flask import render_template, redirect, url_for, request

from sqlalchemy.orm import Session

from app.forms import EditForm
from app.services import TaskServiceLayer
from app.database import session_scope
from app.helpers import show_task_status
from app.enums import TaskStatus


class EditView(MethodView):
    def get(self, id):
        service = TaskServiceLayer(session_scope)
        task = service.get_task_data(id)

        form = EditForm(data={
            "title": task.title,
            "deadline": task.deadline,
            "description": task.description,
            "status": task.status
        })

        return render_template("task/edit.html",
                               form=form,
                               task=task,
                               statuses=show_task_status(TaskStatus)
                               )

    def post(self, id):
        service = TaskServiceLayer(session_scope)

        task = service.get_task_data(id)
        task = task if task else None

        form = EditForm(formdata=request.form)
        form._task_instance = task

        if form.validate_on_submit():
            form_data = request.form.to_dict()
            if task:
                service.update(
                    id,
                    form_data["title"],
                    form_data["deadline"],
                    form_data["description"],
                    int(form_data["status"])
                )

                return redirect(url_for("task.index_view"))

        return render_template("task/edit.html",
                               form=form,
                               task=task,
                               statuses=show_task_status(TaskStatus)
                               )
