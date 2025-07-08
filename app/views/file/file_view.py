from flask.views import MethodView
from flask import render_template, redirect, url_for, flash

from app.forms import UploadFileForm
from app.services import FileServiceLayer, TaskServiceLayer
from app.database import session_scope
from app.enums import FlashMessage


class FileView(MethodView):
    def get(self, id):
        form = UploadFileForm()

        service = FileServiceLayer(session_scope)
        files = service.get_files(id)

        task = TaskServiceLayer.get_task_data(id)

        return render_template("file/index.html",
                               form=form,
                               files=files["items"],
                               task=task,
                               page=files["page"],
                               total_pages=files["total_pages"]
                               )

    def post(self, id):
        form = UploadFileForm()
        task = TaskServiceLayer.get_task_data(id)
        service = FileServiceLayer(session_scope)
        files = service.get_files(id)

        if form.validate_on_submit():
            service = FileServiceLayer(session_scope)
            is_uploaded = service.create(id, form)

            if is_uploaded:
                msg = FlashMessage.CREATE_FILE_SUCCESS
                flash(msg.message(), msg.category())

                return redirect(url_for("file.index_view", id=id))

        return render_template("file/index.html",
                               form=form,
                               files=files["items"],
                               task=task,
                               page=files["page"],
                               total_pages=files["total_pages"]
                               )
