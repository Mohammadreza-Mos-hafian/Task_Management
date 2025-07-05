from flask import render_template
from flask_login import current_user
from flask.views import MethodView

from sqlalchemy import select, and_

from app.helpers import paginate
from app.models import Task


class IndexView(MethodView):
    @staticmethod
    def get():
        base_stmt = (
            select(Task)
            .where(and_(
                Task.user_id == current_user.id,
                Task.is_deleted == False
            ))
        )

        pagination = paginate(base_stmt)

        return render_template("task/index.html",
                               tasks=pagination["items"],
                               page=pagination["page"],
                               total_pages=pagination["total_pages"]
                               )
