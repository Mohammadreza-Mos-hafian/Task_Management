from flask.views import MethodView
from flask import redirect, url_for

from app.database import session_scope
from app.services import TaskServiceLayer


class DeleteView(MethodView):
    def get(self, id):
        service = TaskServiceLayer(session_scope)
        service.delete(id)

        return redirect(url_for("task.index_view"))
