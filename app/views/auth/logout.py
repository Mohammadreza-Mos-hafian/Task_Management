from flask import redirect, url_for
from flask.views import MethodView
from flask_login import current_user

from app.services import LogoutServiceLayer
from app.database import session_scope


class Logout(MethodView):
    @staticmethod
    def get():
        service = LogoutServiceLayer(session_scope)

        if service.logout(int(current_user.id)):
            return redirect(url_for("main_page"))

        return redirect(url_for("dashboard.view"))
