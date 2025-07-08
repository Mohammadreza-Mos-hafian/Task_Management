from flask.views import MethodView
from flask import redirect, url_for, flash

from app.services import FileServiceLayer
from app.database import session_scope
from app.enums import FlashMessage
from app.helpers import encode


class DownloadView(MethodView):
    def get(self, id):
        service = FileServiceLayer(session_scope)
        response = service.download(id)

        task = FileServiceLayer.get_task_data(id)

        if response:
            return response

        msg = FlashMessage.DOWNLOAD_FILE_FAILED
        flash(msg.message(), msg.category())

        return redirect(url_for("file.index_view", id=encode(task.id)))
