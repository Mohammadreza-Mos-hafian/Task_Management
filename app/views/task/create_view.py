from flask import render_template, redirect, url_for, request
from flask.views import MethodView

from app.forms import CreateForm
from app.services import TaskServiceLayer
from app.database import session_scope


class CreateView(MethodView):
    @staticmethod
    def get():
        form = CreateForm()
        return render_template("task/create.html", form=form)

    @staticmethod
    def post():
        form = CreateForm()

        if form.validate_on_submit():
            service = TaskServiceLayer(session_scope)

            service.create(
                form=form,
                title=form.title.data,
                deadline=form.deadline.data,
                description=form.description.data
            )

            return redirect(url_for("task.index_view", page=1))

        return render_template("task/create.html", form=form)
