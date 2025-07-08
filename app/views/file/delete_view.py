from flask.views import MethodView
from flask import redirect, url_for, flash

from app.services import FileServiceLayer, TaskServiceLayer
from app.database import session_scope
from app.enums import FlashMessage
from app.helpers import encode


class DeleteFileView(MethodView):
    def get(self, id):
        service = FileServiceLayer(session_scope)
        service.delete(id)

        task = FileServiceLayer.get_task_data(id)

        msg = FlashMessage.DELETE_FILE_SUCCESS
        flash(msg.message(), msg.category())

        return redirect(url_for("file.index_view", id=encode(task.id)))
