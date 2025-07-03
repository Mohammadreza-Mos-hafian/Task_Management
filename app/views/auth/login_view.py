from flask import render_template, redirect, url_for, request, flash
from flask.views import MethodView

from sqlalchemy.orm import Session

from app.forms import LoginForm
from app.enums import FlashMessage
from app.services import LoginServiceLayer


class LoginView(MethodView):
    @staticmethod
    def get():
        form = LoginForm()
        return render_template("auth/login.html", form=form)

    @staticmethod
    def post():
        form = LoginForm()

        if form.validate_on_submit():
            service = LoginServiceLayer(Session)
            service.login(form.email.data)

            return redirect(url_for("dashboard.view"))

        for error in form.errors.values():
            if error[-1] == FlashMessage.LOGIN_FAILED.message():
                msg = FlashMessage.LOGIN_FAILED
                flash(msg.message(), msg.category())

                return redirect(url_for("auth.login_view"))

        return render_template("auth/login.html", form=form)
